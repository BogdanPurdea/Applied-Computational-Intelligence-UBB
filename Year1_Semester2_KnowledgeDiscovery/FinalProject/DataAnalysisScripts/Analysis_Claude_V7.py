"""
CCM Knowledge Discovery / Data Mining Pipeline  –  Claude V7

Changes from V5:
  - Fixed DBSCAN visualisation:
      * Auto-estimate eps from the knee of the k-distance graph so DBSCAN
        actually produces meaningful clusters instead of all-noise or one
        giant cluster.
      * Fixed broken annotate() call in k-distance plot (missing xytext arg).
      * Richer DBSCAN PCA 2D scatter: distinct colours per cluster, noise
        points rendered as grey '×' with its own legend entry, cluster
        centroids annotated, point counts shown, and a separate noise-only
        highlight plot.
      * Added a DBSCAN RUL box-plot (mirrors the K-Means one from V5).
      * Graceful fallback when DBSCAN finds 0 clusters (pure noise).
  - All other sections (EDA, regression, classification, decision tree, PCA,
    K-Means, Isolation Forest, association rules) are identical to V5 and
    kept intact.

Expected folder structure (same as V5, outputs go to V7 folder):
    script_folder/
    ├── Analysis_Claude_V7.py
    ├── Dataset/
    │   └── PreProcessedDataset.csv
    └── Analysis1_Outputs_Claude_V7/
        └── plots/

Run:
    python Analysis_Claude_V7.py
"""

from pathlib import Path
import os
import warnings

import numpy as np
import pandas as pd

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    silhouette_score,
    silhouette_samples,
)

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier,
    IsolationForest,
)

from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

warnings.filterwarnings("ignore")

try:
    from mlxtend.frequent_patterns import apriori, association_rules

    MLXTEND_AVAILABLE = True
except ImportError:
    MLXTEND_AVAILABLE = False


# ============================================================
# Global configuration
# ============================================================

TARGET_REGRESSION = "RUL"
TARGET_CLASSIFICATION = "RUL_class"

RANDOM_STATE = 42

PLOT_DPI = 160
TOP_N_FEATURES = 25
TOP_N_CORRELATIONS = 25
TOP_N_ASSOCIATION_RULES = 20

# K-Means search range for elbow / silhouette curves
KMEANS_K_RANGE = range(2, 11)
# Final K chosen for the main clustering run
KMEANS_N_CLUSTERS = 4

# DBSCAN – min_samples is fixed; eps is AUTO-estimated from the k-distance knee.
# You can override eps by setting DBSCAN_EPS_OVERRIDE to a positive float.
DBSCAN_MIN_SAMPLES = 10
DBSCAN_EPS_OVERRIDE = None   # e.g. 2.5 — set to None to auto-detect

# Cap on FCA/bin columns passed to Apriori to avoid OOM on large transaction matrices.
MAX_APRIORI_COLUMNS = 20
# Maximum rows sampled for Apriori (keeps candidate generation fast on large datasets).
APRIORI_MAX_ROWS = 5_000
# Apriori hyperparameters tuned to finish in seconds on the CCM dataset.
APRIORI_MIN_SUPPORT = 0.15   # raised from 0.08 — prunes rare itemsets early
APRIORI_MAX_LEN    = 3       # hard cap on itemset size; kills combinatorial explosion


# ============================================================
# Colour palettes (consistent across all cluster plots)
# ============================================================

_CLUSTER_CMAP = "tab10"
_NOISE_COLOR = "#B0BEC5"   # light grey for noise / anomaly points

def _cluster_colours(n_colours: int):
    """Return a list of *n_colours* distinct colours from the qualitative tab10 cmap."""
    cmap = plt.get_cmap(_CLUSTER_CMAP)
    return [cmap(i % 10) for i in range(n_colours)]


# ============================================================
# Utility functions  (unchanged from V4/V5)
# ============================================================

def create_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def create_plot_dir(output_dir: str) -> str:
    plot_dir = os.path.join(output_dir, "plots")
    os.makedirs(plot_dir, exist_ok=True)
    return plot_dir


def save_current_plot(path: str) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close()


def safe_filename(name: str) -> str:
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ',', '%']
    result = str(name)
    for ch in invalid_chars:
        result = result.replace(ch, "_")
    result = result.replace(" ", "_")
    return result[:120]


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[INFO] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df.columns = [c.strip() for c in df.columns]

    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower() or "timestamp" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except Exception:
                pass

    return df


def remove_leakage_columns(df: pd.DataFrame, task: str, strict_no_resistance: bool = False) -> pd.DataFrame:
    """
    Removes target leakage columns.

    New preprocessed format notes:
        - RUL_scaled is a linear function of RUL → always dropped from features.
        - RUL_fca_bin is a binned version of RUL → always dropped from features.
        - RUL_class leaks the regression target for regression tasks.
        - RUL leaks the classification target for classification tasks.
        - strict_no_resistance=True additionally removes all resistance-related
          columns for a cleaner prognostic experiment.
    """

    cols_to_drop = []

    # Columns that directly leak the target regardless of task
    leakage_exact = [
        "RUL_scaled",
        "RUL_fca_bin",
    ]

    for col in df.columns:
        if col in leakage_exact:
            cols_to_drop.append(col)

    if task == "regression":
        if TARGET_CLASSIFICATION in df.columns:
            cols_to_drop.append(TARGET_CLASSIFICATION)

    if task == "classification":
        if TARGET_REGRESSION in df.columns:
            cols_to_drop.append(TARGET_REGRESSION)

    if strict_no_resistance:
        for col in df.columns:
            c = col.lower()
            if "resistance" in c:
                cols_to_drop.append(col)

    cols_to_drop = sorted(set([c for c in cols_to_drop if c in df.columns]))

    return df.drop(columns=cols_to_drop, errors="ignore")


def split_features_target(df: pd.DataFrame, target: str):
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' was not found in dataset.")

    y = df[target]
    X = df.drop(columns=[target])

    datetime_cols = X.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()
    X = X.drop(columns=datetime_cols, errors="ignore")

    return X, y


def get_column_types(X: pd.DataFrame):
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
    return numeric_cols, categorical_cols


def build_preprocessor(X: pd.DataFrame):
    numeric_cols, categorical_cols = get_column_types(X)

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols),
        ],
        remainder="drop",
    )

    return preprocessor, numeric_cols, categorical_cols


def export_feature_importance(pipeline: Pipeline, output_path: str) -> pd.DataFrame:
    model = pipeline.named_steps["model"]
    preprocessor = pipeline.named_steps["preprocess"]

    if not hasattr(model, "feature_importances_"):
        return pd.DataFrame()

    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        feature_names = [f"feature_{i}" for i in range(len(model.feature_importances_))]

    importance_df = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_,
        }
    ).sort_values(by="importance", ascending=False)

    importance_df.to_csv(output_path, index=False)
    print(f"[RESULT] Feature importance exported: {output_path}")

    return importance_df


# ============================================================
# Plotting: generic helpers  (unchanged from V4/V5)
# ============================================================

def plot_bar_from_series(series: pd.Series, title: str, xlabel: str, ylabel: str, path: str, top_n: int = None):
    s = series.dropna()

    if top_n is not None:
        s = s.head(top_n)

    if s.empty:
        return

    plt.figure(figsize=(12, max(5, 0.35 * len(s))))
    s.sort_values().plot(kind="barh")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    save_current_plot(path)


def plot_histogram(series: pd.Series, title: str, xlabel: str, ylabel: str, path: str, bins: int = 40):
    s = pd.to_numeric(series, errors="coerce").dropna()

    if s.empty:
        return

    plt.figure(figsize=(10, 6))
    plt.hist(s, bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    save_current_plot(path)


def plot_scatter(x, y, title: str, xlabel: str, ylabel: str, path: str):
    x = pd.to_numeric(pd.Series(x), errors="coerce")
    y = pd.to_numeric(pd.Series(y), errors="coerce")

    valid = x.notna() & y.notna()
    x = x[valid]
    y = y[valid]

    if len(x) == 0:
        return

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, s=18, alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    save_current_plot(path)


def plot_line_from_dataframe(df: pd.DataFrame, x_col: str, y_col: str, title: str, xlabel: str, ylabel: str, path: str):
    if x_col not in df.columns or y_col not in df.columns:
        return

    plot_df = df[[x_col, y_col]].dropna()

    if plot_df.empty:
        return

    plt.figure(figsize=(12, 6))
    plt.plot(plot_df[x_col], plot_df[y_col], marker="o", linewidth=1)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    save_current_plot(path)


# ============================================================
# EDA plots  (unchanged from V4/V5)
# ============================================================

def generate_eda_plots(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Generating EDA plots...")

    plot_dir = create_plot_dir(output_dir)

    if TARGET_REGRESSION in df.columns:
        plot_histogram(
            df[TARGET_REGRESSION],
            title="RUL Distribution",
            xlabel="RUL",
            ylabel="Frequency",
            path=os.path.join(plot_dir, "eda_rul_distribution.png"),
        )

    if TARGET_CLASSIFICATION in df.columns:
        class_counts = df[TARGET_CLASSIFICATION].astype(str).value_counts()
        plot_bar_from_series(
            class_counts,
            title="RUL Class Distribution",
            xlabel="Count",
            ylabel="RUL Class",
            path=os.path.join(plot_dir, "eda_rul_class_distribution.png"),
        )

    if "workpiece_slice_geometry_encoded" in df.columns and TARGET_REGRESSION in df.columns:
        geom_rul = df.groupby("workpiece_slice_geometry_encoded")[TARGET_REGRESSION].mean().sort_values(ascending=False)
        plot_bar_from_series(
            geom_rul,
            title="Average RUL by Workpiece Geometry (encoded)",
            xlabel="Average RUL",
            ylabel="Geometry Code",
            path=os.path.join(plot_dir, "eda_average_rul_by_geometry_encoded.png"),
        )

    if "shift" in df.columns and TARGET_REGRESSION in df.columns:
        shift_rul = df.groupby("shift")[TARGET_REGRESSION].mean().sort_values(ascending=False)
        plot_bar_from_series(
            shift_rul,
            title="Average RUL by Shift",
            xlabel="Average RUL",
            ylabel="Shift",
            path=os.path.join(plot_dir, "eda_average_rul_by_shift.png"),
        )

    if "num_stream" in df.columns and TARGET_REGRESSION in df.columns:
        stream_rul = df.groupby("num_stream")[TARGET_REGRESSION].mean().sort_values(ascending=False)
        plot_bar_from_series(
            stream_rul,
            title="Average RUL by Stream",
            xlabel="Average RUL",
            ylabel="Stream",
            path=os.path.join(plot_dir, "eda_average_rul_by_stream.png"),
        )

    if "num_crystallizer" in df.columns and TARGET_REGRESSION in df.columns:
        cryst_rul = df.groupby("num_crystallizer")[TARGET_REGRESSION].mean().sort_values(ascending=False)
        plot_bar_from_series(
            cryst_rul,
            title="Average RUL by Crystallizer",
            xlabel="Average RUL",
            ylabel="Crystallizer",
            path=os.path.join(plot_dir, "eda_average_rul_by_crystallizer.png"),
        )

    if "sleeve" in df.columns and TARGET_REGRESSION in df.columns:
        sleeve_rul = df.groupby("sleeve")[TARGET_REGRESSION].mean().sort_values(ascending=False)
        plot_bar_from_series(
            sleeve_rul,
            title="Top Sleeve Groups by Average RUL",
            xlabel="Average RUL",
            ylabel="Sleeve",
            path=os.path.join(plot_dir, "eda_average_rul_by_sleeve_top25.png"),
            top_n=25,
        )

    if TARGET_REGRESSION in df.columns:
        numeric_df = df.select_dtypes(include=[np.number])
        if TARGET_REGRESSION in numeric_df.columns:
            corr = numeric_df.corr(numeric_only=True)[TARGET_REGRESSION].drop(TARGET_REGRESSION)
            corr = corr.reindex(corr.abs().sort_values(ascending=False).index).head(TOP_N_CORRELATIONS)

            plot_bar_from_series(
                corr,
                title=f"Top {TOP_N_CORRELATIONS} Numerical Correlations with RUL",
                xlabel="Correlation with RUL",
                ylabel="Feature",
                path=os.path.join(plot_dir, "eda_top_correlations_with_rul.png"),
            )

    candidate_scatter_cols = [
        "resistance, tonn_scaled",
        "water_consumption, liter/minute_scaled",
        "water_temperature_delta, Celsius deg._scaled",
        "total_cooling_consumption_scaled",
        "average_cooling_consumption_scaled",
        "temperature_difference_scaled",
        "impurity_index_scaled",
        "steel_temperature_grab1, Celsius deg._scaled",
    ]

    if TARGET_REGRESSION in df.columns:
        for col in candidate_scatter_cols:
            if col in df.columns:
                plot_scatter(
                    df[col],
                    df[TARGET_REGRESSION],
                    title=f"RUL vs {col}",
                    xlabel=col,
                    ylabel="RUL",
                    path=os.path.join(plot_dir, f"eda_scatter_rul_vs_{safe_filename(col)}.png"),
                )

    if "timestamp" in df.columns and TARGET_REGRESSION in df.columns:
        temp = df.copy()
        temp["timestamp"] = pd.to_datetime(temp["timestamp"], errors="coerce")
        temp = temp.dropna(subset=["timestamp", TARGET_REGRESSION]).sort_values("timestamp")

        if not temp.empty:
            daily = temp.set_index("timestamp")[TARGET_REGRESSION].resample("D").mean().reset_index()
            plot_line_from_dataframe(
                daily,
                x_col="timestamp",
                y_col=TARGET_REGRESSION,
                title="Daily Average RUL Trend",
                xlabel="Date",
                ylabel="Average RUL",
                path=os.path.join(plot_dir, "eda_daily_average_rul_trend.png"),
            )

    print(f"[RESULT] EDA plots exported to: {plot_dir}")


# ============================================================
# Supervised learning: RUL regression  (unchanged from V4/V5)
# ============================================================

def run_rul_regression(df: pd.DataFrame, output_dir: str, strict_no_resistance: bool = False):
    print("\n[INFO] Running supervised RUL regression...")

    plot_dir = create_plot_dir(output_dir)

    df_model = remove_leakage_columns(
        df,
        task="regression",
        strict_no_resistance=strict_no_resistance,
    )

    X, y = split_features_target(df_model, TARGET_REGRESSION)

    valid_idx = y.notna()
    X = X.loc[valid_idx]
    y = pd.to_numeric(y.loc[valid_idx], errors="coerce")

    valid_idx = y.notna()
    X = X.loc[valid_idx]
    y = y.loc[valid_idx]

    if len(y) < 10:
        print("[WARNING] Not enough valid RUL samples for regression.")
        return

    preprocessor, _, _ = build_preprocessor(X)

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=RANDOM_STATE,
    )

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    metrics = pd.DataFrame(
        {
            "metric": ["MAE", "RMSE", "R2"],
            "value": [mae, rmse, r2],
        }
    )

    metrics_path = os.path.join(output_dir, "rul_regression_metrics.csv")
    metrics.to_csv(metrics_path, index=False)

    print("[RESULT] RUL Regression Metrics")
    print(metrics)

    predictions_df = pd.DataFrame(
        {
            "actual_RUL": y_test.values,
            "predicted_RUL": preds,
            "error": y_test.values - preds,
        }
    )

    predictions_path = os.path.join(output_dir, "rul_regression_predictions.csv")
    predictions_df.to_csv(predictions_path, index=False)

    importance_df = export_feature_importance(
        pipeline=pipeline,
        output_path=os.path.join(output_dir, "rul_regression_feature_importance.csv"),
    )

    plot_scatter(
        predictions_df["actual_RUL"],
        predictions_df["predicted_RUL"],
        title="RUL Regression: Actual vs Predicted",
        xlabel="Actual RUL",
        ylabel="Predicted RUL",
        path=os.path.join(plot_dir, "regression_actual_vs_predicted_rul.png"),
    )

    plot_histogram(
        predictions_df["error"],
        title="RUL Regression Error Distribution",
        xlabel="Prediction Error",
        ylabel="Frequency",
        path=os.path.join(plot_dir, "regression_error_distribution.png"),
    )

    if not importance_df.empty:
        top_features = importance_df.head(TOP_N_FEATURES).set_index("feature")["importance"]
        plot_bar_from_series(
            top_features,
            title=f"Top {TOP_N_FEATURES} Features for RUL Regression",
            xlabel="Importance",
            ylabel="Feature",
            path=os.path.join(plot_dir, "regression_feature_importance_top25.png"),
        )


# ============================================================
# Supervised learning: RUL_class classification  (unchanged from V4/V5)
# ============================================================

def run_rul_classification(df: pd.DataFrame, output_dir: str, strict_no_resistance: bool = False):
    print("\n[INFO] Running supervised RUL_class classification...")

    plot_dir = create_plot_dir(output_dir)

    df_model = remove_leakage_columns(
        df,
        task="classification",
        strict_no_resistance=strict_no_resistance,
    )

    X, y = split_features_target(df_model, TARGET_CLASSIFICATION)

    valid_idx = y.notna()
    X = X.loc[valid_idx]
    y = y.loc[valid_idx].astype(str)

    if len(y) < 10:
        print("[WARNING] Not enough valid RUL_class samples for classification.")
        return

    preprocessor, _, _ = build_preprocessor(X)

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )

    stratify = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=stratify,
    )

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    metrics = pd.DataFrame(
        {
            "metric": ["Accuracy", "Precision_macro", "Recall_macro", "F1_macro"],
            "value": [
                accuracy_score(y_test, preds),
                precision_score(y_test, preds, average="macro", zero_division=0),
                recall_score(y_test, preds, average="macro", zero_division=0),
                f1_score(y_test, preds, average="macro", zero_division=0),
            ],
        }
    )

    metrics.to_csv(
        os.path.join(output_dir, "rul_classification_metrics.csv"),
        index=False,
    )

    print("[RESULT] RUL_class Classification Metrics")
    print(metrics)

    report = classification_report(y_test, preds, zero_division=0)
    with open(os.path.join(output_dir, "rul_classification_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

    labels = sorted(y.unique())

    cm = pd.DataFrame(
        confusion_matrix(y_test, preds, labels=labels),
        index=labels,
        columns=labels,
    )

    cm.to_csv(os.path.join(output_dir, "rul_classification_confusion_matrix.csv"))

    predictions_df = pd.DataFrame(
        {
            "actual_RUL_class": y_test.values,
            "predicted_RUL_class": preds,
        }
    )

    predictions_df.to_csv(
        os.path.join(output_dir, "rul_classification_predictions.csv"),
        index=False,
    )

    importance_df = export_feature_importance(
        pipeline=pipeline,
        output_path=os.path.join(output_dir, "rul_classification_feature_importance.csv"),
    )

    # Plot: confusion matrix
    plt.figure(figsize=(8, 7))
    plt.imshow(cm.values, interpolation="nearest")
    plt.title("RUL_class Confusion Matrix")
    plt.xlabel("Predicted Class")
    plt.ylabel("Actual Class")
    plt.xticks(np.arange(len(labels)), labels, rotation=45, ha="right")
    plt.yticks(np.arange(len(labels)), labels)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, str(cm.values[i, j]), ha="center", va="center")

    plt.colorbar()
    save_current_plot(os.path.join(plot_dir, "classification_confusion_matrix.png"))

    if not importance_df.empty:
        top_features = importance_df.head(TOP_N_FEATURES).set_index("feature")["importance"]
        plot_bar_from_series(
            top_features,
            title=f"Top {TOP_N_FEATURES} Features for RUL_class Classification",
            xlabel="Importance",
            ylabel="Feature",
            path=os.path.join(plot_dir, "classification_feature_importance_top25.png"),
        )

    # Plot: actual vs predicted class counts
    actual_counts = pd.Series(y_test.values).value_counts().sort_index()
    predicted_counts = pd.Series(preds).value_counts().sort_index()
    combined = pd.DataFrame(
        {
            "actual": actual_counts,
            "predicted": predicted_counts,
        }
    ).fillna(0)

    plt.figure(figsize=(10, 6))
    combined.plot(kind="bar")
    plt.title("Actual vs Predicted RUL_class Distribution")
    plt.xlabel("RUL Class")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    save_current_plot(os.path.join(plot_dir, "classification_actual_vs_predicted_distribution.png"))


# ============================================================
# Decision tree rule extraction  (unchanged from V4/V5)
# ============================================================

def run_decision_tree_rules(df: pd.DataFrame, output_dir: str, strict_no_resistance: bool = False):
    print("\n[INFO] Extracting decision-tree rules...")

    plot_dir = create_plot_dir(output_dir)

    df_model = remove_leakage_columns(
        df,
        task="classification",
        strict_no_resistance=strict_no_resistance,
    )

    X, y = split_features_target(df_model, TARGET_CLASSIFICATION)

    valid_idx = y.notna()
    X = X.loc[valid_idx]
    y = y.loc[valid_idx].astype(str)

    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) == 0:
        print("[WARNING] No numeric columns available for decision tree rule extraction.")
        return

    X_num = X[numeric_cols].replace([np.inf, -np.inf], np.nan)
    X_num = X_num.fillna(X_num.median(numeric_only=True))

    clf = DecisionTreeClassifier(
        max_depth=4,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )

    clf.fit(X_num, y)

    rules = export_text(clf, feature_names=numeric_cols)

    with open(os.path.join(output_dir, "decision_tree_rules.txt"), "w", encoding="utf-8") as f:
        f.write(rules)

    print("[RESULT] Decision tree rules exported to decision_tree_rules.txt")

    importance = pd.Series(clf.feature_importances_, index=numeric_cols)
    importance = importance.sort_values(ascending=False)
    importance = importance[importance > 0]

    if not importance.empty:
        importance.to_csv(os.path.join(output_dir, "decision_tree_rule_feature_importance.csv"))

        plot_bar_from_series(
            importance.head(TOP_N_FEATURES),
            title="Decision Tree Rule Feature Importance",
            xlabel="Importance",
            ylabel="Feature",
            path=os.path.join(plot_dir, "decision_tree_rule_feature_importance.png"),
        )


# ============================================================
# Unsupervised matrix preparation  (unchanged from V4/V5)
# ============================================================

def prepare_unsupervised_matrix(df: pd.DataFrame):
    """
    Builds the numeric feature matrix used for clustering, PCA and anomaly detection.
    """
    exclude_cols = [
        TARGET_REGRESSION,
        TARGET_CLASSIFICATION,
        "RUL_scaled",
        "RUL_fca_bin",
        "sleeve",
        "num_crystallizer",
        "num_stream",
    ]

    X = df.drop(columns=[c for c in exclude_cols if c in df.columns], errors="ignore")
    X = X.select_dtypes(include=[np.number])
    X = X.replace([np.inf, -np.inf], np.nan)

    if X.shape[1] == 0:
        return X, np.empty((len(df), 0))

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    X_imputed = imputer.fit_transform(X)
    X_scaled = scaler.fit_transform(X_imputed)

    return X, X_scaled


# ============================================================
# Helper: 2D / 3D PCA projection (shared by clustering & anomaly)
# ============================================================

def _get_pca2d(X_scaled: np.ndarray) -> tuple:
    """
    Returns (pca_model, components_array) with 2 principal components.
    Components shape: (n_samples, 2).
    """
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    components = pca.fit_transform(X_scaled)
    return pca, components


def _get_pca3d(X_scaled: np.ndarray) -> np.ndarray:
    """Returns 3D PCA components array."""
    n_components = min(3, X_scaled.shape[1])
    pca = PCA(n_components=n_components, random_state=RANDOM_STATE)
    components = pca.fit_transform(X_scaled)
    return pca, components


# ============================================================
# K-Means rich visualisations  (from V5, unchanged)
# ============================================================

def _plot_kmeans_elbow(X_scaled: np.ndarray, k_range, plot_dir: str):
    """Inertia (within-cluster SSE) elbow curve."""
    print("[INFO]   Computing K-Means elbow curve...")
    inertias = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        km.fit(X_scaled)
        inertias.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(list(k_range), inertias, marker="o", linewidth=2, color="#2196F3")
    ax.fill_between(list(k_range), inertias, alpha=0.15, color="#2196F3")
    ax.set_title("K-Means – Elbow Curve (Inertia)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Clusters (k)")
    ax.set_ylabel("Inertia (Within-Cluster SSE)")
    ax.grid(True, linestyle="--", alpha=0.5)
    save_current_plot(os.path.join(plot_dir, "kmeans_elbow_curve.png"))


def _plot_kmeans_silhouette_curve(X_scaled: np.ndarray, k_range, plot_dir: str):
    """Average silhouette score for each k."""
    print("[INFO]   Computing K-Means silhouette scores...")
    sil_scores = []
    max_sil_rows = 5_000
    if X_scaled.shape[0] > max_sil_rows:
        rng = np.random.default_rng(RANDOM_STATE)
        idx = rng.choice(X_scaled.shape[0], max_sil_rows, replace=False)
        Xs = X_scaled[idx]
    else:
        Xs = X_scaled

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = km.fit_predict(Xs)
        score = silhouette_score(Xs, labels)
        sil_scores.append(score)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(list(k_range), sil_scores, marker="s", linewidth=2, color="#4CAF50")
    ax.fill_between(list(k_range), sil_scores, alpha=0.15, color="#4CAF50")
    ax.set_title("K-Means – Silhouette Score vs k", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Clusters (k)")
    ax.set_ylabel("Average Silhouette Score")
    ax.grid(True, linestyle="--", alpha=0.5)
    save_current_plot(os.path.join(plot_dir, "kmeans_silhouette_curve.png"))


def _plot_kmeans_silhouette_diagram(X_scaled: np.ndarray, labels: np.ndarray, k: int, plot_dir: str):
    """Per-sample silhouette coefficient diagram (like sklearn example)."""
    print("[INFO]   Plotting K-Means silhouette diagram...")
    max_rows = 5_000
    if X_scaled.shape[0] > max_rows:
        rng = np.random.default_rng(RANDOM_STATE)
        idx = rng.choice(X_scaled.shape[0], max_rows, replace=False)
        Xs = X_scaled[idx]
        ls = labels[idx]
    else:
        Xs = X_scaled
        ls = labels

    sample_sil = silhouette_samples(Xs, ls)
    colours = _cluster_colours(k)

    fig, ax = plt.subplots(figsize=(10, 7))
    y_lower = 10
    for i in range(k):
        cluster_vals = np.sort(sample_sil[ls == i])
        size_cluster = cluster_vals.shape[0]
        y_upper = y_lower + size_cluster
        ax.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            cluster_vals,
            facecolor=colours[i],
            alpha=0.8,
            label=f"Cluster {i}",
        )
        ax.text(-0.05, y_lower + 0.5 * size_cluster, str(i), fontsize=9)
        y_lower = y_upper + 10

    avg_score = np.mean(sample_sil)
    ax.axvline(x=avg_score, color="red", linestyle="--", label=f"Mean = {avg_score:.3f}")
    ax.set_title(f"K-Means Silhouette Diagram  (k={k})", fontsize=14, fontweight="bold")
    ax.set_xlabel("Silhouette Coefficient")
    ax.set_ylabel("Cluster")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(True, axis="x", linestyle="--", alpha=0.4)
    save_current_plot(os.path.join(plot_dir, "kmeans_silhouette_diagram.png"))


def _plot_kmeans_pca2d(components: np.ndarray, labels: np.ndarray, pca, k: int,
                       rul_values, plot_dir: str):
    """2D PCA scatter coloured by K-Means cluster."""
    print("[INFO]   Plotting K-Means 2D PCA scatter...")
    colours = _cluster_colours(k)

    fig, ax = plt.subplots(figsize=(10, 7))
    for i in range(k):
        mask = labels == i
        ax.scatter(
            components[mask, 0], components[mask, 1],
            s=14, alpha=0.65, color=colours[i], label=f"Cluster {i}",
        )

    ax.set_title("K-Means Clusters – PCA 2D Projection", fontsize=14, fontweight="bold")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
    ax.legend(title="Cluster", fontsize=9, loc="best")
    ax.grid(True, linestyle="--", alpha=0.3)
    save_current_plot(os.path.join(plot_dir, "kmeans_pca2d_scatter.png"))

    # Also colour by continuous RUL if available
    if rul_values is not None and len(rul_values) == len(components):
        fig, ax = plt.subplots(figsize=(10, 7))
        sc = ax.scatter(
            components[:, 0], components[:, 1],
            c=rul_values, cmap="plasma", s=14, alpha=0.65,
        )
        plt.colorbar(sc, ax=ax, label="RUL")
        # Overlay cluster centroids (recomputed in PCA space)
        for i in range(k):
            mask = labels == i
            cx, cy = components[mask, 0].mean(), components[mask, 1].mean()
            ax.scatter(cx, cy, marker="X", s=180, color="black", zorder=5,
                       edgecolors="white", linewidths=0.8)
            ax.text(cx, cy + 0.1, f"C{i}", fontsize=9, ha="center", color="black",
                    fontweight="bold")
        ax.set_title("K-Means Clusters – PCA 2D coloured by RUL", fontsize=14, fontweight="bold")
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
        ax.grid(True, linestyle="--", alpha=0.3)
        save_current_plot(os.path.join(plot_dir, "kmeans_pca2d_rul_heatmap.png"))


def _plot_kmeans_pca3d(components3d: np.ndarray, labels: np.ndarray, k: int, plot_dir: str):
    """3D PCA scatter coloured by K-Means cluster."""
    if components3d.shape[1] < 3:
        return
    print("[INFO]   Plotting K-Means 3D PCA scatter...")
    colours = _cluster_colours(k)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    for i in range(k):
        mask = labels == i
        ax.scatter(
            components3d[mask, 0], components3d[mask, 1], components3d[mask, 2],
            s=10, alpha=0.55, color=colours[i], label=f"Cluster {i}",
        )
    ax.set_title("K-Means Clusters – PCA 3D Projection", fontsize=13, fontweight="bold")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    ax.legend(title="Cluster", fontsize=8)
    save_current_plot(os.path.join(plot_dir, "kmeans_pca3d_scatter.png"))


def _plot_kmeans_centroid_heatmap(X_scaled: np.ndarray, labels: np.ndarray,
                                   feature_names: list, k: int, plot_dir: str):
    """Cluster centroid heatmap (top-N most variable features)."""
    print("[INFO]   Plotting K-Means centroid heatmap...")
    n_features_show = min(20, len(feature_names))

    centroids = np.array([X_scaled[labels == i].mean(axis=0) for i in range(k)])

    # pick features with highest variance across centroids
    feature_var = centroids.var(axis=0)
    top_idx = np.argsort(feature_var)[::-1][:n_features_show]
    centroid_subset = centroids[:, top_idx]
    feat_subset = [feature_names[i] for i in top_idx]

    fig, ax = plt.subplots(figsize=(max(8, n_features_show * 0.5), k + 2))
    im = ax.imshow(centroid_subset, aspect="auto", cmap="RdBu_r")
    ax.set_xticks(range(n_features_show))
    ax.set_xticklabels([f[:25] for f in feat_subset], rotation=60, ha="right", fontsize=8)
    ax.set_yticks(range(k))
    ax.set_yticklabels([f"Cluster {i}" for i in range(k)])
    ax.set_title("K-Means Centroid Heatmap\n(Top features by inter-cluster variance)",
                 fontsize=13, fontweight="bold")
    plt.colorbar(im, ax=ax, label="Normalised mean value")
    save_current_plot(os.path.join(plot_dir, "kmeans_centroid_heatmap.png"))


def _plot_kmeans_rul_boxplot(labels: np.ndarray, rul_values, k: int, plot_dir: str):
    """Box-plot of RUL distribution per K-Means cluster."""
    if rul_values is None:
        return
    print("[INFO]   Plotting K-Means RUL box-plot per cluster...")
    data_by_cluster = [rul_values[labels == i] for i in range(k)]
    data_by_cluster = [d[~np.isnan(d)] for d in data_by_cluster]

    colours = _cluster_colours(k)

    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(data_by_cluster, patch_artist=True, notch=False)

    for patch, colour in zip(bp["boxes"], colours):
        patch.set_facecolor(colour)
        patch.set_alpha(0.75)

    ax.set_xticks(range(1, k + 1))
    ax.set_xticklabels([f"Cluster {i}" for i in range(k)])
    ax.set_title("RUL Distribution per K-Means Cluster", fontsize=14, fontweight="bold")
    ax.set_xlabel("K-Means Cluster")
    ax.set_ylabel("RUL")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    save_current_plot(os.path.join(plot_dir, "kmeans_rul_boxplot.png"))


# ============================================================
# DBSCAN helpers  (V7: fixed + enhanced)
# ============================================================

def _estimate_dbscan_eps(X_scaled: np.ndarray, min_samples: int,
                         plot_dir: str) -> float:
    """
    Compute the k-distance graph, find the 'knee' automatically, and return
    the suggested eps value.

    The knee is located at the point of maximum curvature in the sorted
    k-distance curve (second-difference method).  We also save the plot with
    a vertical line showing the chosen knee index.

    FIX vs V5:
      - Added xytext parameter to annotate() so the arrow renders properly.
      - The knee index is computed and printed for transparency.
      - Returns the numeric eps value so run_clustering() can use it.
    """
    print("[INFO]   Computing DBSCAN k-distance curve and estimating eps...")

    max_rows = 5_000
    if X_scaled.shape[0] > max_rows:
        rng = np.random.default_rng(RANDOM_STATE)
        idx = rng.choice(X_scaled.shape[0], max_rows, replace=False)
        Xs = X_scaled[idx]
    else:
        Xs = X_scaled

    nbrs = NearestNeighbors(n_neighbors=min_samples).fit(Xs)
    distances, _ = nbrs.kneighbors(Xs)
    # k-th nearest neighbour distances, sorted descending (classic DBSCAN plot)
    kth_distances = np.sort(distances[:, -1])[::-1]

    # ---- Auto-detect knee (maximum second derivative) ----
    if len(kth_distances) >= 5:
        # Smooth slightly before differentiating to avoid noise spikes
        smooth_window = max(3, len(kth_distances) // 100)
        smoothed = np.convolve(
            kth_distances,
            np.ones(smooth_window) / smooth_window,
            mode="valid",
        )
        second_diff = np.diff(np.diff(smoothed))
        # The knee is where the curve bends the most — largest 2nd derivative
        # We look only in the first 60 % of the sorted curve (right half =
        # dense points; left half = sparse outliers)
        search_end = max(1, int(len(second_diff) * 0.6))
        knee_idx = int(np.argmax(second_diff[:search_end]))
        # Map back to original kth_distances index (offset by convolution shrink)
        knee_idx = min(knee_idx + smooth_window, len(kth_distances) - 1)
    else:
        knee_idx = len(kth_distances) // 2

    eps_auto = float(kth_distances[knee_idx])
    print(f"[INFO]   DBSCAN knee at index {knee_idx}, auto-estimated eps = {eps_auto:.4f}")

    # ---- Plot ----
    fig, ax = plt.subplots(figsize=(10, 5))
    x_vals = np.arange(len(kth_distances))
    ax.plot(x_vals, kth_distances, linewidth=1.5, color="#FF5722",
            label=f"{min_samples}-NN distance")
    ax.axhline(y=eps_auto, color="#1565C0", linestyle="--", linewidth=1.5,
               label=f"Auto eps ≈ {eps_auto:.3f}")
    ax.axvline(x=knee_idx, color="#1565C0", linestyle=":", linewidth=1.2, alpha=0.7)

    # Annotate the knee point — xytext is offset so the arrow is visible
    ax.annotate(
        f"Knee  (eps ≈ {eps_auto:.3f})",
        xy=(knee_idx, eps_auto),
        xytext=(knee_idx + max(10, int(len(kth_distances) * 0.05)),
                eps_auto + (kth_distances[0] - kth_distances[-1]) * 0.12),
        fontsize=9,
        color="#1565C0",
        arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.5),
    )

    ax.set_title(f"DBSCAN – k-Distance Graph  (k={min_samples})\n"
                 f"Auto-estimated eps = {eps_auto:.4f}",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Points sorted by k-NN distance (descending)")
    ax.set_ylabel(f"Distance to {min_samples}-th Nearest Neighbour")
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)
    save_current_plot(os.path.join(plot_dir, "dbscan_kdistance_plot.png"))

    return eps_auto


def _plot_dbscan_pca2d(components: np.ndarray, labels: np.ndarray,
                        pca, eps: float, min_samples: int, plot_dir: str):
    """
    2D PCA scatter coloured by DBSCAN cluster with noise points highlighted.

    FIX vs V5:
      - Noise points rendered as large grey '×' markers in the FOREGROUND so
        they are clearly visible even when clusters overlap them.
      - Each cluster gets an annotated centroid marker with the cluster id and
        point count.
      - A dedicated second figure shows ONLY noise vs non-noise for clarity.
      - Handles the edge case of zero clusters (pure noise).
    """
    print("[INFO]   Plotting DBSCAN 2D PCA scatter...")

    unique_labels = sorted(set(labels))
    cluster_labels = [l for l in unique_labels if l != -1]
    n_clusters = len(cluster_labels)

    colours = _cluster_colours(max(n_clusters, 1))

    # Map cluster id → colour
    colour_map = {}
    for ci, lbl in enumerate(cluster_labels):
        colour_map[lbl] = colours[ci % len(colours)]

    noise_mask = labels == -1
    n_noise = int(noise_mask.sum())
    n_total = len(labels)

    # ------------------------------------------------------------------
    # Figure 1: Full scatter (clusters + noise)
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 8))

    if n_clusters == 0:
        # Pure noise — draw all points in grey
        ax.scatter(
            components[:, 0], components[:, 1],
            s=18, alpha=0.6, color=_NOISE_COLOR,
            marker="x", label=f"Noise (n={n_total})",
        )
        ax.set_title(
            f"DBSCAN – PCA 2D  (eps={eps:.3f}, min_samples={min_samples})\n"
            f"⚠ All {n_total} points classified as NOISE — try a larger eps",
            fontsize=13, fontweight="bold", color="#B71C1C",
        )
    else:
        # Draw cluster points first (background)
        for lbl in cluster_labels:
            mask = labels == lbl
            cnt = int(mask.sum())
            ax.scatter(
                components[mask, 0], components[mask, 1],
                s=15, alpha=0.60,
                color=colour_map[lbl],
                label=f"Cluster {lbl}  (n={cnt})",
            )
            # Annotate centroid
            cx = components[mask, 0].mean()
            cy = components[mask, 1].mean()
            ax.scatter(cx, cy, marker="D", s=120, color=colour_map[lbl],
                       edgecolors="black", linewidths=0.8, zorder=6)
            ax.text(cx, cy, f" C{lbl}", fontsize=8, fontweight="bold",
                    color="black", zorder=7, va="center")

        # Draw noise points on TOP (foreground) so they are always visible
        if n_noise > 0:
            ax.scatter(
                components[noise_mask, 0], components[noise_mask, 1],
                s=22, alpha=0.75, color=_NOISE_COLOR,
                marker="x", linewidths=0.8,
                label=f"Noise  (n={n_noise}, {n_noise/n_total:.1%})",
                zorder=5,
            )

        noise_pct = f"{n_noise/n_total:.1%}" if n_noise > 0 else "0 %"
        ax.set_title(
            f"DBSCAN Clusters – PCA 2D Projection\n"
            f"eps={eps:.3f}  |  min_samples={min_samples}  |  "
            f"{n_clusters} cluster(s)  |  noise: {noise_pct}",
            fontsize=13, fontweight="bold",
        )

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
    ax.legend(title="DBSCAN label", fontsize=8, loc="best", markerscale=1.5,
              framealpha=0.85)
    ax.grid(True, linestyle="--", alpha=0.3)
    save_current_plot(os.path.join(plot_dir, "dbscan_pca2d_scatter.png"))

    # ------------------------------------------------------------------
    # Figure 2: Noise-highlight only (non-noise dimmed, noise bright red)
    # ------------------------------------------------------------------
    if n_noise > 0 and n_clusters > 0:
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        # All cluster points dimmed
        ax2.scatter(
            components[~noise_mask, 0], components[~noise_mask, 1],
            s=12, alpha=0.25, color="#90CAF9",
            label=f"Clustered points  (n={n_total - n_noise})",
        )
        # Noise points highlighted
        ax2.scatter(
            components[noise_mask, 0], components[noise_mask, 1],
            s=30, alpha=0.90, color="#EF5350",
            marker="x", linewidths=1.2,
            label=f"Noise / outliers  (n={n_noise})",
        )
        ax2.set_title(
            f"DBSCAN – Noise Points Highlighted\n"
            f"eps={eps:.3f}  |  min_samples={min_samples}  |  "
            f"noise rate: {n_noise/n_total:.1%}",
            fontsize=13, fontweight="bold",
        )
        ax2.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
        ax2.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
        ax2.legend(fontsize=9, loc="best", framealpha=0.85)
        ax2.grid(True, linestyle="--", alpha=0.3)
        save_current_plot(os.path.join(plot_dir, "dbscan_noise_highlight_scatter.png"))


def _plot_dbscan_cluster_sizes(labels: np.ndarray, plot_dir: str):
    """Bar chart of DBSCAN cluster sizes (noise shown separately)."""
    print("[INFO]   Plotting DBSCAN cluster sizes...")
    unique_labels, counts = np.unique(labels, return_counts=True)
    label_names = ["Noise" if l == -1 else f"Cluster {l}" for l in unique_labels]
    bar_colours = [_NOISE_COLOR if l == -1 else plt.get_cmap("tab10")(i % 10)
                   for i, l in enumerate(unique_labels)]

    fig, ax = plt.subplots(figsize=(max(8, len(unique_labels)), 5))
    bars = ax.bar(label_names, counts, color=bar_colours, edgecolor="white", linewidth=0.8)
    for bar, cnt in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(counts) * 0.01,
                str(cnt), ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("DBSCAN Cluster Sizes (incl. Noise)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Number of Points")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    save_current_plot(os.path.join(plot_dir, "dbscan_cluster_sizes_bar.png"))


def _plot_dbscan_rul_per_cluster(labels: np.ndarray, rul_values, plot_dir: str):
    """Average RUL per DBSCAN cluster (noise excluded from mean, shown separately)."""
    if rul_values is None:
        return
    print("[INFO]   Plotting DBSCAN average RUL per cluster...")
    unique_labels = sorted(set(labels))
    means, label_names = [], []
    for lbl in unique_labels:
        mask = labels == lbl
        vals = rul_values[mask]
        vals = vals[~np.isnan(vals)]
        if len(vals) > 0:
            means.append(vals.mean())
            label_names.append("Noise" if lbl == -1 else f"Cluster {lbl}")

    bar_colours = [_NOISE_COLOR if "Noise" in n else plt.get_cmap("tab10")(i % 10)
                   for i, n in enumerate(label_names)]

    fig, ax = plt.subplots(figsize=(max(8, len(label_names)), 5))
    bars = ax.bar(label_names, means, color=bar_colours, edgecolor="white", linewidth=0.8)
    for bar, val in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(means) * 0.01,
                f"{val:.1f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("DBSCAN – Average RUL per Cluster", fontsize=14, fontweight="bold")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Average RUL")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    save_current_plot(os.path.join(plot_dir, "dbscan_average_rul_per_cluster.png"))


def _plot_dbscan_rul_boxplot(labels: np.ndarray, rul_values, plot_dir: str):
    """
    Box-plot of RUL distribution per DBSCAN cluster.
    Noise group is included but styled distinctly (grey, hatched).

    V7 NEW – mirrors the K-Means RUL box-plot.
    """
    if rul_values is None:
        return
    print("[INFO]   Plotting DBSCAN RUL box-plot per label...")
    unique_labels = sorted(set(labels))
    data_groups, tick_labels, colours, hatches = [], [], [], []

    cluster_labels_only = [l for l in unique_labels if l != -1]
    cluster_colours = _cluster_colours(max(len(cluster_labels_only), 1))
    ci = 0

    for lbl in unique_labels:
        mask = labels == lbl
        vals = rul_values[mask]
        vals = vals[~np.isnan(vals)]
        if len(vals) == 0:
            continue
        data_groups.append(vals)
        if lbl == -1:
            tick_labels.append("Noise")
            colours.append(_NOISE_COLOR)
            hatches.append("//")
        else:
            tick_labels.append(f"Cluster {lbl}")
            colours.append(cluster_colours[ci % len(cluster_colours)])
            hatches.append("")
            ci += 1

    if len(data_groups) < 2:
        return   # nothing meaningful to compare

    fig, ax = plt.subplots(figsize=(max(8, len(data_groups) * 1.2), 6))
    bp = ax.boxplot(data_groups, patch_artist=True, notch=False)

    for patch, colour, hatch in zip(bp["boxes"], colours, hatches):
        patch.set_facecolor(colour)
        patch.set_alpha(0.75)
        patch.set_hatch(hatch)

    ax.set_xticks(range(1, len(tick_labels) + 1))
    ax.set_xticklabels(tick_labels, rotation=15, ha="right")
    ax.set_title("RUL Distribution per DBSCAN Label\n(Noise shown with hatching)",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("DBSCAN Label")
    ax.set_ylabel("RUL")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5)
    save_current_plot(os.path.join(plot_dir, "dbscan_rul_boxplot.png"))


# ============================================================
# Isolation Forest rich visualisations  (from V5, unchanged)
# ============================================================

def _plot_iforest_pca2d_scatter(components: np.ndarray, pca,
                                 is_anomaly: np.ndarray, scores: np.ndarray,
                                 plot_dir: str):
    print("[INFO]   Plotting Isolation Forest PCA 2D scatter...")

    # --- Panel 1: Normal vs Anomaly ---
    fig, ax = plt.subplots(figsize=(10, 7))
    normal_mask = is_anomaly == 0
    anomaly_mask = is_anomaly == 1
    ax.scatter(components[normal_mask, 0], components[normal_mask, 1],
               s=12, alpha=0.5, color="#42A5F5", label="Normal")
    ax.scatter(components[anomaly_mask, 0], components[anomaly_mask, 1],
               s=28, alpha=0.9, color="#EF5350", marker="^", label="Anomaly",
               edgecolors="darkred", linewidths=0.5)
    ax.set_title("Isolation Forest – Anomalies on PCA 2D Projection",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.3)
    save_current_plot(os.path.join(plot_dir, "iforest_pca2d_anomaly_scatter.png"))

    # --- Panel 2: Score heatmap ---
    fig, ax = plt.subplots(figsize=(10, 7))
    sc = ax.scatter(components[:, 0], components[:, 1],
                    c=scores, cmap="RdYlGn", s=14, alpha=0.7,
                    vmin=scores.min(), vmax=scores.max())
    plt.colorbar(sc, ax=ax, label="Anomaly Score (higher = more normal)")
    ax.set_title("Isolation Forest – Anomaly Score on PCA 2D",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
    ax.grid(True, linestyle="--", alpha=0.3)
    save_current_plot(os.path.join(plot_dir, "iforest_pca2d_score_heatmap.png"))


def _plot_iforest_score_distribution(scores: np.ndarray, is_anomaly: np.ndarray, plot_dir: str):
    print("[INFO]   Plotting Isolation Forest score distribution...")
    normal_scores = scores[is_anomaly == 0]
    anomaly_scores = scores[is_anomaly == 1]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(normal_scores, bins=50, alpha=0.6, color="#42A5F5",
            label=f"Normal (n={len(normal_scores)})", density=True)
    ax.hist(anomaly_scores, bins=30, alpha=0.7, color="#EF5350",
            label=f"Anomaly (n={len(anomaly_scores)})", density=True)
    ax.axvline(normal_scores.mean(), color="#1565C0", linestyle="--", linewidth=1.5,
               label=f"Normal mean={normal_scores.mean():.3f}")
    ax.axvline(anomaly_scores.mean(), color="#B71C1C", linestyle="--", linewidth=1.5,
               label=f"Anomaly mean={anomaly_scores.mean():.3f}")
    ax.set_title("Isolation Forest – Anomaly Score Distribution by Class",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Decision Function Score")
    ax.set_ylabel("Density")
    ax.legend(fontsize=9)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    save_current_plot(os.path.join(plot_dir, "iforest_score_distribution_by_class.png"))


def _plot_iforest_violin(scores: np.ndarray, is_anomaly: np.ndarray, plot_dir: str):
    print("[INFO]   Plotting Isolation Forest violin plot...")
    normal_scores = scores[is_anomaly == 0]
    anomaly_scores = scores[is_anomaly == 1]

    fig, ax = plt.subplots(figsize=(8, 6))
    parts = ax.violinplot([normal_scores, anomaly_scores],
                          positions=[1, 2], showmedians=True, showextrema=True)

    colours = ["#42A5F5", "#EF5350"]
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colours[i])
        pc.set_alpha(0.75)
    parts["cmedians"].set_color("black")
    parts["cmaxes"].set_color("grey")
    parts["cmins"].set_color("grey")
    parts["cbars"].set_color("grey")

    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Normal", "Anomaly"])
    ax.set_title("Isolation Forest – Score Violin Plot", fontsize=14, fontweight="bold")
    ax.set_ylabel("Decision Function Score")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    save_current_plot(os.path.join(plot_dir, "iforest_score_violin.png"))


def _plot_iforest_anomaly_by_rul_class(is_anomaly: np.ndarray, rul_class_values, plot_dir: str):
    if rul_class_values is None:
        return
    print("[INFO]   Plotting Isolation Forest anomaly rate per RUL_class...")
    tmp = pd.DataFrame({"is_anomaly": is_anomaly, "rul_class": rul_class_values})
    tmp = tmp.dropna(subset=["rul_class"])
    tmp["rul_class"] = tmp["rul_class"].astype(str)

    grouped = tmp.groupby("rul_class")["is_anomaly"].value_counts(normalize=True).unstack(fill_value=0)
    grouped.columns = ["Normal" if c == 0 else "Anomaly" for c in grouped.columns]
    if "Normal" not in grouped.columns:
        grouped["Normal"] = 0
    if "Anomaly" not in grouped.columns:
        grouped["Anomaly"] = 0
    grouped = grouped[["Normal", "Anomaly"]]

    fig, ax = plt.subplots(figsize=(max(8, len(grouped) * 0.8), 6))
    grouped.plot(kind="bar", stacked=True, ax=ax,
                 color=["#42A5F5", "#EF5350"], edgecolor="white", linewidth=0.5)
    ax.set_title("Isolation Forest – Anomaly Proportion per RUL_class",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("RUL Class")
    ax.set_ylabel("Proportion")
    ax.set_ylim(0, 1.05)
    ax.legend(title="State", fontsize=10)
    plt.xticks(rotation=30, ha="right")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    save_current_plot(os.path.join(plot_dir, "iforest_anomaly_proportion_per_rul_class.png"))


def _plot_iforest_rul_vs_score(scores: np.ndarray, rul_values, is_anomaly: np.ndarray, plot_dir: str):
    if rul_values is None:
        return
    print("[INFO]   Plotting Isolation Forest RUL vs score scatter...")
    valid = ~np.isnan(rul_values)
    r = rul_values[valid]
    s = scores[valid]
    a = is_anomaly[valid]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(r[a == 0], s[a == 0], s=12, alpha=0.5, color="#42A5F5", label="Normal")
    ax.scatter(r[a == 1], s[a == 1], s=28, alpha=0.85, color="#EF5350", marker="^",
               label="Anomaly", edgecolors="darkred", linewidths=0.5)
    ax.set_title("Isolation Forest – RUL vs Anomaly Score", fontsize=14, fontweight="bold")
    ax.set_xlabel("RUL")
    ax.set_ylabel("Anomaly Score (higher = more normal)")
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.3)
    save_current_plot(os.path.join(plot_dir, "iforest_rul_vs_score_scatter.png"))


# ============================================================
# Unsupervised learning: clustering  (V7 — fixed DBSCAN suite)
# ============================================================

def run_clustering(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running unsupervised clustering (K-Means + DBSCAN with rich plots)...")

    plot_dir = create_plot_dir(output_dir)

    X_df, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] == 0:
        print("[WARNING] No numerical columns available for clustering.")
        return

    feature_names = list(X_df.columns)

    # -----------------------------------------------------------------
    # RUL array for downstream plots (None if column absent)
    # -----------------------------------------------------------------
    rul_values = df[TARGET_REGRESSION].values.astype(float) if TARGET_REGRESSION in df.columns else None

    # -----------------------------------------------------------------
    # Shared PCA projections
    # -----------------------------------------------------------------
    pca2d, components2d = _get_pca2d(X_scaled)
    pca3d, components3d = _get_pca3d(X_scaled)

    # =================================================================
    # K-Means
    # =================================================================
    print("\n[INFO] --- K-Means clustering ---")

    _plot_kmeans_elbow(X_scaled, KMEANS_K_RANGE, plot_dir)
    _plot_kmeans_silhouette_curve(X_scaled, KMEANS_K_RANGE, plot_dir)

    kmeans = KMeans(n_clusters=KMEANS_N_CLUSTERS, random_state=RANDOM_STATE, n_init=10)
    kmeans_labels = kmeans.fit_predict(X_scaled)

    _plot_kmeans_silhouette_diagram(X_scaled, kmeans_labels, KMEANS_N_CLUSTERS, plot_dir)
    _plot_kmeans_pca2d(components2d, kmeans_labels, pca2d, KMEANS_N_CLUSTERS, rul_values, plot_dir)
    _plot_kmeans_pca3d(components3d, kmeans_labels, KMEANS_N_CLUSTERS, plot_dir)
    _plot_kmeans_centroid_heatmap(X_scaled, kmeans_labels, feature_names, KMEANS_N_CLUSTERS, plot_dir)
    _plot_kmeans_rul_boxplot(kmeans_labels, rul_values, KMEANS_N_CLUSTERS, plot_dir)

    cluster_counts = pd.Series(kmeans_labels).value_counts().sort_index()
    plot_bar_from_series(
        cluster_counts,
        title="K-Means Cluster Sizes",
        xlabel="Count",
        ylabel="Cluster",
        path=os.path.join(plot_dir, "clustering_kmeans_cluster_sizes.png"),
    )

    if rul_values is not None:
        avg_rul = pd.Series(rul_values).groupby(pd.Series(kmeans_labels)).mean().sort_values(ascending=False)
        plot_bar_from_series(
            avg_rul,
            title="Average RUL by K-Means Cluster",
            xlabel="Average RUL",
            ylabel="K-Means Cluster",
            path=os.path.join(plot_dir, "clustering_average_rul_by_kmeans_cluster.png"),
        )

    # =================================================================
    # DBSCAN  (V7: auto-eps + fixed plots)
    # =================================================================
    print("\n[INFO] --- DBSCAN clustering ---")

    # Step 1: estimate eps from k-distance plot (or use override)
    if DBSCAN_EPS_OVERRIDE is not None and DBSCAN_EPS_OVERRIDE > 0:
        eps = float(DBSCAN_EPS_OVERRIDE)
        print(f"[INFO]   Using manual eps override: {eps}")
        # Still produce the k-distance plot for reference
        _estimate_dbscan_eps(X_scaled, DBSCAN_MIN_SAMPLES, plot_dir)
    else:
        eps = _estimate_dbscan_eps(X_scaled, DBSCAN_MIN_SAMPLES, plot_dir)

    # Step 2: fit DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=DBSCAN_MIN_SAMPLES)
    dbscan_labels = dbscan.fit_predict(X_scaled)

    n_clusters_found = len(set(dbscan_labels) - {-1})
    n_noise_found = int((dbscan_labels == -1).sum())
    print(f"[INFO]   DBSCAN result: {n_clusters_found} cluster(s), "
          f"{n_noise_found} noise point(s) "
          f"({n_noise_found / len(dbscan_labels):.1%} of data)")

    # Step 3: rich plots
    _plot_dbscan_pca2d(components2d, dbscan_labels, pca2d, eps, DBSCAN_MIN_SAMPLES, plot_dir)
    _plot_dbscan_cluster_sizes(dbscan_labels, plot_dir)
    _plot_dbscan_rul_per_cluster(dbscan_labels, rul_values, plot_dir)
    _plot_dbscan_rul_boxplot(dbscan_labels, rul_values, plot_dir)

    # Legacy plot (V4/V5 compatibility)
    dbscan_counts = pd.Series(dbscan_labels).value_counts().sort_index()
    plot_bar_from_series(
        dbscan_counts,
        title="DBSCAN Cluster Sizes",
        xlabel="Count",
        ylabel="DBSCAN Cluster",
        path=os.path.join(plot_dir, "clustering_dbscan_cluster_sizes.png"),
    )

    # =================================================================
    # Save combined results CSV
    # =================================================================
    result = pd.DataFrame(
        {
            "kmeans_cluster": kmeans_labels,
            "dbscan_cluster": dbscan_labels,
        }
    )

    if TARGET_REGRESSION in df.columns:
        result[TARGET_REGRESSION] = df[TARGET_REGRESSION].values

    if TARGET_CLASSIFICATION in df.columns:
        result[TARGET_CLASSIFICATION] = df[TARGET_CLASSIFICATION].values

    result.to_csv(os.path.join(output_dir, "clustering_results.csv"), index=False)

    # K-Means summary CSV
    if TARGET_REGRESSION in result.columns:
        summary = result.groupby("kmeans_cluster").agg(
            count=("kmeans_cluster", "size"),
            avg_RUL=(TARGET_REGRESSION, "mean"),
            median_RUL=(TARGET_REGRESSION, "median"),
            min_RUL=(TARGET_REGRESSION, "min"),
            max_RUL=(TARGET_REGRESSION, "max"),
        )
    else:
        summary = result.groupby("kmeans_cluster").agg(count=("kmeans_cluster", "size"))

    summary.to_csv(os.path.join(output_dir, "kmeans_cluster_summary.csv"))

    print("[RESULT] Clustering results and plots exported.")


# ============================================================
# PCA  (unchanged from V4/V5)
# ============================================================

def run_pca(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running PCA dimensionality reduction...")

    plot_dir = create_plot_dir(output_dir)

    _, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] < 2:
        print("[WARNING] Not enough numeric features for PCA.")
        return

    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    components = pca.fit_transform(X_scaled)

    pca_df = pd.DataFrame(
        {
            "PC1": components[:, 0],
            "PC2": components[:, 1],
        }
    )

    if TARGET_REGRESSION in df.columns:
        pca_df[TARGET_REGRESSION] = df[TARGET_REGRESSION].values

    if TARGET_CLASSIFICATION in df.columns:
        pca_df[TARGET_CLASSIFICATION] = df[TARGET_CLASSIFICATION].values

    pca_df.to_csv(os.path.join(output_dir, "pca_2d_projection.csv"), index=False)

    explained = pd.DataFrame(
        {
            "component": ["PC1", "PC2"],
            "explained_variance_ratio": pca.explained_variance_ratio_,
        }
    )

    explained.to_csv(os.path.join(output_dir, "pca_explained_variance.csv"), index=False)

    plt.figure(figsize=(10, 7))

    if TARGET_CLASSIFICATION in pca_df.columns:
        classes = pca_df[TARGET_CLASSIFICATION].astype(str).unique()
        for cls in sorted(classes):
            subset = pca_df[pca_df[TARGET_CLASSIFICATION].astype(str) == cls]
            plt.scatter(subset["PC1"], subset["PC2"], s=18, alpha=0.7, label=cls)
        plt.legend(title="RUL_class")
    else:
        plt.scatter(pca_df["PC1"], pca_df["PC2"], s=18, alpha=0.7)

    plt.title("PCA 2D Projection")
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
    save_current_plot(os.path.join(plot_dir, "pca_2d_projection.png"))

    plt.figure(figsize=(8, 5))
    plt.bar(explained["component"], explained["explained_variance_ratio"])
    plt.title("PCA Explained Variance Ratio")
    plt.xlabel("Component")
    plt.ylabel("Explained Variance Ratio")
    save_current_plot(os.path.join(plot_dir, "pca_explained_variance.png"))

    print("[RESULT] PCA results and plots exported.")


# ============================================================
# Anomaly detection  (V5 — full visual suite, unchanged)
# ============================================================

def run_anomaly_detection(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running anomaly detection (Isolation Forest with rich plots)...")

    plot_dir = create_plot_dir(output_dir)

    X_df, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] == 0:
        print("[WARNING] No numeric columns available for anomaly detection.")
        return

    iso = IsolationForest(
        n_estimators=300,
        contamination=0.05,
        random_state=RANDOM_STATE,
    )

    raw_labels = iso.fit_predict(X_scaled)
    scores = iso.decision_function(X_scaled)
    is_anomaly = (raw_labels == -1).astype(int)

    rul_values = df[TARGET_REGRESSION].values.astype(float) if TARGET_REGRESSION in df.columns else None
    rul_class_values = df[TARGET_CLASSIFICATION].values if TARGET_CLASSIFICATION in df.columns else None

    anomaly_df = pd.DataFrame(
        {
            "anomaly_label": raw_labels,
            "anomaly_score": scores,
            "is_anomaly": is_anomaly,
        }
    )

    if TARGET_REGRESSION in df.columns:
        anomaly_df[TARGET_REGRESSION] = df[TARGET_REGRESSION].values

    if TARGET_CLASSIFICATION in df.columns:
        anomaly_df[TARGET_CLASSIFICATION] = df[TARGET_CLASSIFICATION].values

    anomaly_df.to_csv(os.path.join(output_dir, "anomaly_detection_results.csv"), index=False)

    pca2d, components2d = _get_pca2d(X_scaled)

    _plot_iforest_pca2d_scatter(components2d, pca2d, is_anomaly, scores, plot_dir)
    _plot_iforest_score_distribution(scores, is_anomaly, plot_dir)
    _plot_iforest_violin(scores, is_anomaly, plot_dir)
    _plot_iforest_anomaly_by_rul_class(is_anomaly, rul_class_values, plot_dir)
    _plot_iforest_rul_vs_score(scores, rul_values, is_anomaly, plot_dir)

    plot_histogram(
        anomaly_df["anomaly_score"],
        title="Isolation Forest Anomaly Score Distribution",
        xlabel="Anomaly Score",
        ylabel="Frequency",
        path=os.path.join(plot_dir, "anomaly_score_distribution.png"),
    )

    anomaly_counts = anomaly_df["is_anomaly"].map({0: "Normal", 1: "Anomaly"}).value_counts()
    plot_bar_from_series(
        anomaly_counts,
        title="Isolation Forest Normal vs Anomaly Count",
        xlabel="Count",
        ylabel="Label",
        path=os.path.join(plot_dir, "anomaly_normal_vs_anomaly_count.png"),
    )

    if TARGET_REGRESSION in anomaly_df.columns:
        avg_rul = anomaly_df.groupby("is_anomaly")[TARGET_REGRESSION].mean()
        avg_rul.index = avg_rul.index.map({0: "Normal", 1: "Anomaly"})
        plot_bar_from_series(
            avg_rul,
            title="Average RUL by Anomaly State",
            xlabel="Average RUL",
            ylabel="State",
            path=os.path.join(plot_dir, "anomaly_average_rul_by_state.png"),
        )

    print("[RESULT] Anomaly detection results and plots exported.")


# ============================================================
# Association rule mining  (unchanged from V4/V5)
# ============================================================

def run_association_rule_mining(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running association rule mining on FCA/bin columns...")

    plot_dir = create_plot_dir(output_dir)

    if not MLXTEND_AVAILABLE:
        print("[WARNING] mlxtend is not installed.")
        print("Install it with: pip install mlxtend")
        return

    bin_cols = [
        c for c in df.columns
        if c.endswith("_fca_bin") or c in [TARGET_CLASSIFICATION]
    ]

    if len(bin_cols) < 2:
        print("[WARNING] Not enough FCA/bin columns for association rule mining.")
        return

    target_cols = [c for c in bin_cols if "RUL" in c or TARGET_CLASSIFICATION in c]
    other_cols  = [c for c in bin_cols if c not in target_cols]
    bin_cols = (target_cols + other_cols)[:MAX_APRIORI_COLUMNS]
    print(f"[INFO] Association rule mining on {len(bin_cols)} FCA/bin columns "
          f"(capped at {MAX_APRIORI_COLUMNS}).")

    data = df[bin_cols].copy()
    data = data.fillna("Missing").astype(str)

    transactions = pd.DataFrame(index=data.index)

    for col in data.columns:
        dummies = pd.get_dummies(data[col], prefix=col)
        transactions = pd.concat([transactions, dummies], axis=1)

    transactions = transactions.astype(bool)

    if len(transactions) > APRIORI_MAX_ROWS:
        transactions = transactions.sample(
            n=APRIORI_MAX_ROWS,
            random_state=RANDOM_STATE,
            replace=False,
        )
        print(f"[INFO] Sampled {APRIORI_MAX_ROWS} rows for Apriori "
              f"(from {len(df)} total).")

    print(f"[INFO] Running Apriori: min_support={APRIORI_MIN_SUPPORT}, "
          f"max_len={APRIORI_MAX_LEN}, "
          f"{transactions.shape[1]} one-hot columns, "
          f"{len(transactions)} rows...")
    frequent_itemsets = apriori(
        transactions,
        min_support=APRIORI_MIN_SUPPORT,
        use_colnames=True,
        max_len=APRIORI_MAX_LEN,
    )

    if frequent_itemsets.empty:
        print("[WARNING] No frequent itemsets found. Try lowering min_support.")
        return

    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1.2,
    )

    if rules.empty:
        print("[WARNING] No association rules found. Try lowering min_threshold.")
        frequent_itemsets.to_csv(
            os.path.join(output_dir, "frequent_itemsets.csv"),
            index=False,
        )
        return

    rules["antecedents_str"] = rules["antecedents"].apply(lambda x: ", ".join(sorted(list(x))))
    rules["consequents_str"] = rules["consequents"].apply(lambda x: ", ".join(sorted(list(x))))

    rules["contains_RUL_target"] = rules["consequents_str"].apply(
        lambda x: ("RUL_class" in x) or ("RUL_fca_bin" in x)
    )

    rules = rules.sort_values(
        by=["contains_RUL_target", "lift", "confidence"],
        ascending=[False, False, False],
    )

    frequent_itemsets.to_csv(
        os.path.join(output_dir, "frequent_itemsets.csv"),
        index=False,
    )

    rules.to_csv(
        os.path.join(output_dir, "association_rules.csv"),
        index=False,
    )

    top_rules = rules.head(TOP_N_ASSOCIATION_RULES).copy()

    if not top_rules.empty:
        labels = [
            f"{row['antecedents_str']} => {row['consequents_str']}"
            for _, row in top_rules.iterrows()
        ]

        lift_series = pd.Series(top_rules["lift"].values, index=labels)

        plot_bar_from_series(
            lift_series,
            title=f"Top {TOP_N_ASSOCIATION_RULES} Association Rules by Lift",
            xlabel="Lift",
            ylabel="Rule",
            path=os.path.join(plot_dir, "association_rules_top_lift.png"),
        )

        confidence_series = pd.Series(top_rules["confidence"].values, index=labels)

        plot_bar_from_series(
            confidence_series,
            title=f"Top {TOP_N_ASSOCIATION_RULES} Association Rules by Confidence",
            xlabel="Confidence",
            ylabel="Rule",
            path=os.path.join(plot_dir, "association_rules_top_confidence.png"),
        )

    print("[RESULT] Association rules and plots exported.")


# ============================================================
# First-layer text report  (unchanged from V4/V5)
# ============================================================

def generate_first_layer_knowledge_report(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Generating first-layer knowledge report...")

    report_path = os.path.join(output_dir, "first_layer_knowledge_report.txt")

    lines = []

    lines.append("FIRST-LAYER KNOWLEDGE DISCOVERY REPORT")
    lines.append("=" * 70)
    lines.append("")

    lines.append(f"Dataset size: {df.shape[0]} rows, {df.shape[1]} columns")
    lines.append("")

    if TARGET_REGRESSION in df.columns:
        lines.append("RUL Summary")
        lines.append("-" * 70)
        lines.append(str(df[TARGET_REGRESSION].describe()))
        lines.append("")

    if TARGET_CLASSIFICATION in df.columns:
        lines.append("RUL_class Distribution")
        lines.append("-" * 70)
        lines.append(str(df[TARGET_CLASSIFICATION].value_counts(dropna=False)))
        lines.append("")

    if "workpiece_slice_geometry_encoded" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Average RUL by Workpiece Geometry (encoded code)")
        lines.append("-" * 70)
        lines.append(str(df.groupby("workpiece_slice_geometry_encoded")[TARGET_REGRESSION].agg(["count", "mean", "median", "min", "max"])))
        lines.append("")

    if "sleeve" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Sleeve-Level RUL Summary")
        lines.append("-" * 70)
        sleeve_summary = df.groupby("sleeve")[TARGET_REGRESSION].agg(["count", "mean", "min", "max"])
        lines.append(str(sleeve_summary.sort_values("mean").head(30)))
        lines.append("")

    if "num_stream" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Average RUL by Stream")
        lines.append("-" * 70)
        lines.append(str(df.groupby("num_stream")[TARGET_REGRESSION].agg(["count", "mean", "median", "min", "max"])))
        lines.append("")

    if "num_crystallizer" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Average RUL by Crystallizer")
        lines.append("-" * 70)
        lines.append(str(df.groupby("num_crystallizer")[TARGET_REGRESSION].agg(["count", "mean", "median", "min", "max"])))
        lines.append("")

    if "shift" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Average RUL by Shift")
        lines.append("-" * 70)
        lines.append(str(df.groupby("shift")[TARGET_REGRESSION].agg(["count", "mean", "median", "min", "max"])))
        lines.append("")

    if TARGET_REGRESSION in df.columns:
        numeric_df = df.select_dtypes(include=[np.number])
        if TARGET_REGRESSION in numeric_df.columns:
            corr = numeric_df.corr(numeric_only=True)[TARGET_REGRESSION].drop(TARGET_REGRESSION)
            corr = corr.sort_values(key=lambda x: x.abs(), ascending=False).head(30)

            lines.append("Top Numerical Correlations with RUL")
            lines.append("-" * 70)
            lines.append(str(corr))
            lines.append("")

    lines.append("Interpretable First-Layer Knowledge")
    lines.append("-" * 70)
    lines.append("1. RUL can be modeled as a supervised regression target.")
    lines.append("2. RUL_class can be modeled as a supervised classification target.")
    lines.append("3. Cooling variables are important candidates for sleeve degradation analysis.")
    lines.append("4. Steel chemistry variables should be treated as degradation context.")
    lines.append("5. Sleeve, crystallizer, and stream identifiers support equipment-specific degradation analysis.")
    lines.append("6. FCA/bin columns enable association rule mining and formal concept-style knowledge extraction.")
    lines.append("7. Clustering can reveal process regimes with different average RUL values.")
    lines.append("8. Isolation Forest can detect abnormal casts that may correspond to accelerated sleeve degradation.")
    lines.append("9. PCA can expose global separation between Healthy, Critical and transitional states.")
    lines.append("10. Feature-importance and decision-tree rules convert predictive models into interpretable industrial knowledge.")
    lines.append("")

    lines.append("Leakage Warning")
    lines.append("-" * 70)
    lines.append("RUL is derived from resistance. Therefore, resistance-related columns may dominate prediction.")
    lines.append("For a cleaner prognostic experiment, run the model with strict_no_resistance=True.")
    lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[RESULT] Knowledge report exported: {report_path}")


# ============================================================
# Main launcher using script-relative paths
# ============================================================

if __name__ == "__main__":
    # ------------------------------------------------------------
    # Resolve paths relative to this script location
    # ------------------------------------------------------------

    SCRIPT_DIR = Path(__file__).resolve().parent

    INPUT_FILE = SCRIPT_DIR / "Dataset" / "PreProcessedDataset.csv"
    OUTPUT_DIR = SCRIPT_DIR / "Analysis1_Outputs_Claude_V7"

    # ------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------

    STRICT_NO_RESISTANCE = False

    # Set STRICT_NO_RESISTANCE = True if you want to remove resistance columns:
    #   "resistance, tonn"
    #   "resistance, tonn_scaled"
    #   "resistance, tonn_fca_bin"
    #
    # This gives a cleaner predictive-maintenance experiment because RUL is
    # derived from resistance.

    # ------------------------------------------------------------
    # Create output directories
    # ------------------------------------------------------------

    create_output_dir(str(OUTPUT_DIR))
    create_plot_dir(str(OUTPUT_DIR))

    # ------------------------------------------------------------
    # Load and clean dataset
    # ------------------------------------------------------------

    df = load_dataset(str(INPUT_FILE))
    df = basic_cleaning(df)

    # ------------------------------------------------------------
    # First-layer descriptive report and EDA plots
    # ------------------------------------------------------------

    generate_first_layer_knowledge_report(df, str(OUTPUT_DIR))
    generate_eda_plots(df, str(OUTPUT_DIR))

    # ------------------------------------------------------------
    # Supervised learning: RUL regression
    # ------------------------------------------------------------

    if TARGET_REGRESSION in df.columns:
        run_rul_regression(
            df,
            str(OUTPUT_DIR),
            strict_no_resistance=STRICT_NO_RESISTANCE,
        )
    else:
        print("[WARNING] RUL column not found. Skipping regression.")

    # ------------------------------------------------------------
    # Supervised learning: RUL_class classification and rule extraction
    # ------------------------------------------------------------

    if TARGET_CLASSIFICATION in df.columns:
        run_rul_classification(
            df,
            str(OUTPUT_DIR),
            strict_no_resistance=STRICT_NO_RESISTANCE,
        )

        run_decision_tree_rules(
            df,
            str(OUTPUT_DIR),
            strict_no_resistance=STRICT_NO_RESISTANCE,
        )
    else:
        print("[WARNING] RUL_class column not found. Skipping classification and rule extraction.")

    # ------------------------------------------------------------
    # Unsupervised learning and data mining
    # ------------------------------------------------------------

    run_clustering(df, str(OUTPUT_DIR))
    run_pca(df, str(OUTPUT_DIR))
    run_anomaly_detection(df, str(OUTPUT_DIR))
    run_association_rule_mining(df, str(OUTPUT_DIR))

    print("\n[DONE] Knowledge Discovery pipeline completed.")
    print(f"[DONE] Input file: {INPUT_FILE}")
    print(f"[DONE] Results saved in: {OUTPUT_DIR}")
    print(f"[DONE] Plots saved in: {OUTPUT_DIR / 'plots'}")
