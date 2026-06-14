"""
CCM Knowledge Discovery / Data Mining Pipeline  –  Claude V4

Changes from V3:
  - Association rule mining: row-samples to 5 000 rows, raises min_support to
    0.15, and caps itemset size at max_len=3. This prevents the exponential
    candidate explosion that caused V3 to hang indefinitely on 43 one-hot columns.

Adapted for the new preprocessed dataset format where:
  - All numeric sensor columns are already StandardScaler-normalised (_scaled suffix).
  - FCA discretisation bins (_fca_bin suffix) are pre-computed.
  - RUL (raw, integer) and RUL_class are present as direct targets.
  - workpiece_slice_geometry is available only as workpiece_slice_geometry_encoded.
  - shift is a text column (Night / Morning / Afternoon).

Expected folder structure:
    script_folder/
    ├── Analysis1_Claude_V4.py
    ├── Dataset/
    │   └── PreProcessedDataset.csv
    └── Analysis1_Outputs_Claude_V4/
        └── plots/

Run:
    python Analysis1_Claude_V4.py
"""

from pathlib import Path
import os
import warnings

import numpy as np
import pandas as pd

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
)

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier,
    IsolationForest,
)

from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

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

# Cap on FCA/bin columns passed to Apriori to avoid OOM on large transaction matrices.
MAX_APRIORI_COLUMNS = 20
# Maximum rows sampled for Apriori (keeps candidate generation fast on large datasets).
APRIORI_MAX_ROWS = 5_000
# Apriori hyperparameters tuned to finish in seconds on the CCM dataset.
APRIORI_MIN_SUPPORT = 0.15   # raised from 0.08 — prunes rare itemsets early
APRIORI_MAX_LEN    = 3       # hard cap on itemset size; kills combinatorial explosion


# ============================================================
# Utility functions
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
# Plotting: generic helpers
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
# EDA plots
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

    # workpiece_slice_geometry is not present in the new format (encoded only) — skipped.
    # Use workpiece_slice_geometry_encoded as a numeric proxy for the groupby.
    if "workpiece_slice_geometry_encoded" in df.columns and TARGET_REGRESSION in df.columns:
        geom_rul = df.groupby("workpiece_slice_geometry_encoded")[TARGET_REGRESSION].mean().sort_values(ascending=False)
        plot_bar_from_series(
            geom_rul,
            title="Average RUL by Workpiece Geometry (encoded)",
            xlabel="Average RUL",
            ylabel="Geometry Code",
            path=os.path.join(plot_dir, "eda_average_rul_by_geometry_encoded.png"),
        )

    # shift is a text column in the new format — groupby works directly.
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

    # New format has no raw sensor columns — use the pre-scaled versions for scatter plots.
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
# Supervised learning: RUL regression
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

    # Plot: actual vs predicted
    plot_scatter(
        predictions_df["actual_RUL"],
        predictions_df["predicted_RUL"],
        title="RUL Regression: Actual vs Predicted",
        xlabel="Actual RUL",
        ylabel="Predicted RUL",
        path=os.path.join(plot_dir, "regression_actual_vs_predicted_rul.png"),
    )

    # Plot: residual distribution
    plot_histogram(
        predictions_df["error"],
        title="RUL Regression Error Distribution",
        xlabel="Prediction Error",
        ylabel="Frequency",
        path=os.path.join(plot_dir, "regression_error_distribution.png"),
    )

    # Plot: feature importance
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
# Supervised learning: RUL_class classification
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

    # Plot: feature importance
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
# Decision tree rule extraction
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
# Unsupervised matrix preparation
# ============================================================

def prepare_unsupervised_matrix(df: pd.DataFrame):
    """
    Builds the numeric feature matrix used for clustering, PCA and anomaly detection.

    Excluded columns (leakage / identifiers):
        - RUL, RUL_scaled, RUL_fca_bin  → direct or derived target
        - RUL_class                      → classification target
        - sleeve, num_crystallizer, num_stream → raw equipment IDs
          (already excluded by select_dtypes since they remain numeric but
          are high-cardinality identifiers — kept here for explicitness)
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
# Unsupervised learning: clustering
# ============================================================

def run_clustering(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running unsupervised clustering...")

    plot_dir = create_plot_dir(output_dir)

    _, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] == 0:
        print("[WARNING] No numerical columns available for clustering.")
        return

    kmeans = KMeans(
        n_clusters=4,
        random_state=RANDOM_STATE,
        n_init=10,
    )

    kmeans_labels = kmeans.fit_predict(X_scaled)

    dbscan = DBSCAN(
        eps=2.5,
        min_samples=10,
    )

    dbscan_labels = dbscan.fit_predict(X_scaled)

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

    if TARGET_REGRESSION in result.columns:
        summary = result.groupby("kmeans_cluster").agg(
            count=("kmeans_cluster", "size"),
            avg_RUL=(TARGET_REGRESSION, "mean"),
            median_RUL=(TARGET_REGRESSION, "median"),
            min_RUL=(TARGET_REGRESSION, "min"),
            max_RUL=(TARGET_REGRESSION, "max"),
        )
    else:
        summary = result.groupby("kmeans_cluster").agg(
            count=("kmeans_cluster", "size"),
        )

    summary.to_csv(os.path.join(output_dir, "kmeans_cluster_summary.csv"))

    # Plot: cluster counts
    cluster_counts = result["kmeans_cluster"].value_counts().sort_index()
    plot_bar_from_series(
        cluster_counts,
        title="K-Means Cluster Sizes",
        xlabel="Count",
        ylabel="Cluster",
        path=os.path.join(plot_dir, "clustering_kmeans_cluster_sizes.png"),
    )

    # Plot: average RUL by cluster
    if TARGET_REGRESSION in result.columns:
        avg_rul = result.groupby("kmeans_cluster")[TARGET_REGRESSION].mean().sort_values(ascending=False)
        plot_bar_from_series(
            avg_rul,
            title="Average RUL by K-Means Cluster",
            xlabel="Average RUL",
            ylabel="K-Means Cluster",
            path=os.path.join(plot_dir, "clustering_average_rul_by_kmeans_cluster.png"),
        )

    # Plot: DBSCAN cluster sizes
    dbscan_counts = result["dbscan_cluster"].value_counts().sort_index()
    plot_bar_from_series(
        dbscan_counts,
        title="DBSCAN Cluster Sizes",
        xlabel="Count",
        ylabel="DBSCAN Cluster",
        path=os.path.join(plot_dir, "clustering_dbscan_cluster_sizes.png"),
    )

    print("[RESULT] Clustering results and plots exported.")


# ============================================================
# PCA
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

    # Plot: PCA scatter
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

    # Plot: explained variance
    plt.figure(figsize=(8, 5))
    plt.bar(explained["component"], explained["explained_variance_ratio"])
    plt.title("PCA Explained Variance Ratio")
    plt.xlabel("Component")
    plt.ylabel("Explained Variance Ratio")
    save_current_plot(os.path.join(plot_dir, "pca_explained_variance.png"))

    print("[RESULT] PCA results and plots exported.")


# ============================================================
# Anomaly detection
# ============================================================

def run_anomaly_detection(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running anomaly detection...")

    plot_dir = create_plot_dir(output_dir)

    _, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] == 0:
        print("[WARNING] No numeric columns available for anomaly detection.")
        return

    iso = IsolationForest(
        n_estimators=300,
        contamination=0.05,
        random_state=RANDOM_STATE,
    )

    labels = iso.fit_predict(X_scaled)
    scores = iso.decision_function(X_scaled)

    anomaly_df = pd.DataFrame(
        {
            "anomaly_label": labels,
            "anomaly_score": scores,
        }
    )

    anomaly_df["is_anomaly"] = anomaly_df["anomaly_label"].map({1: 0, -1: 1})

    if TARGET_REGRESSION in df.columns:
        anomaly_df[TARGET_REGRESSION] = df[TARGET_REGRESSION].values

    if TARGET_CLASSIFICATION in df.columns:
        anomaly_df[TARGET_CLASSIFICATION] = df[TARGET_CLASSIFICATION].values

    anomaly_df.to_csv(os.path.join(output_dir, "anomaly_detection_results.csv"), index=False)

    # Plot: anomaly score distribution
    plot_histogram(
        anomaly_df["anomaly_score"],
        title="Isolation Forest Anomaly Score Distribution",
        xlabel="Anomaly Score",
        ylabel="Frequency",
        path=os.path.join(plot_dir, "anomaly_score_distribution.png"),
    )

    # Plot: anomaly count
    anomaly_counts = anomaly_df["is_anomaly"].map({0: "Normal", 1: "Anomaly"}).value_counts()
    plot_bar_from_series(
        anomaly_counts,
        title="Isolation Forest Normal vs Anomaly Count",
        xlabel="Count",
        ylabel="Label",
        path=os.path.join(plot_dir, "anomaly_normal_vs_anomaly_count.png"),
    )

    # Plot: RUL by anomaly state
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
# Association rule mining
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

    # ---- Memory guard -------------------------------------------------------
    # With 100+ fca_bin columns × 17 k rows the apriori dense matrix exceeds
    # 128 GiB. Prioritise RUL-related columns then fill up to the cap.
    target_cols = [c for c in bin_cols if "RUL" in c or TARGET_CLASSIFICATION in c]
    other_cols  = [c for c in bin_cols if c not in target_cols]
    bin_cols = (target_cols + other_cols)[:MAX_APRIORI_COLUMNS]
    print(f"[INFO] Association rule mining on {len(bin_cols)} FCA/bin columns "
          f"(capped at {MAX_APRIORI_COLUMNS}).")
    # -------------------------------------------------------------------------

    data = df[bin_cols].copy()
    data = data.fillna("Missing").astype(str)

    transactions = pd.DataFrame(index=data.index)

    for col in data.columns:
        dummies = pd.get_dummies(data[col], prefix=col)
        transactions = pd.concat([transactions, dummies], axis=1)

    transactions = transactions.astype(bool)

    # ---- Row sampling -------------------------------------------------------
    # mlxtend apriori builds a dense boolean matrix of shape
    # (n_rows, n_one_hot_cols). With 17 k rows and 43 columns the candidate
    # enumeration never terminates. We sample a stratified subset.
    if len(transactions) > APRIORI_MAX_ROWS:
        transactions = transactions.sample(
            n=APRIORI_MAX_ROWS,
            random_state=RANDOM_STATE,
            replace=False,
        )
        print(f"[INFO] Sampled {APRIORI_MAX_ROWS} rows for Apriori "
              f"(from {len(df)} total).")
    # -------------------------------------------------------------------------

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

    # Plot: top rules by lift
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
# First-layer text report
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

    # workpiece_slice_geometry not present in new format; use encoded proxy.
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
    OUTPUT_DIR = SCRIPT_DIR / "Analysis1_Outputs_Claude_V4"

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
