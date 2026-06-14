"""
CCM Knowledge Discovery Script
Author: Knowledge Discovery / Data Mining pipeline

Purpose:
- Load CCM mould sleeve dataset
- Clean and preprocess data
- Train supervised ML models for:
    1. RUL regression
    2. RUL_class classification
- Apply unsupervised ML for:
    1. Clustering
    2. Anomaly detection
    3. Dimensionality reduction
- Apply rule mining on FCA binned columns
- Export first-layer knowledge results

Usage:
    python ccm_knowledge_discovery.py --input dataset.csv --output results
"""

import argparse
import os
import warnings

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
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


# Optional rule mining dependency
try:
    from mlxtend.frequent_patterns import apriori, association_rules
    MLXTEND_AVAILABLE = True
except ImportError:
    MLXTEND_AVAILABLE = False


TARGET_REGRESSION = "RUL"
TARGET_CLASSIFICATION = "RUL_class"


def create_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[INFO] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove fully empty rows/columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # Strip column names
    df.columns = [c.strip() for c in df.columns]

    # Try parsing date fields where possible
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower() or "timestamp" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except Exception:
                pass

    return df


def remove_leakage_columns(df: pd.DataFrame, task: str) -> pd.DataFrame:
    """
    Removes target-leaking columns.

    For RUL regression:
        Remove RUL_class, RUL_fca_bin, scaled/binned target columns.
        Keep 'resistance, tonn' by default because RUL is calculated from resistance.
        But if your target scenario requires prediction without current resistance,
        remove it manually.

    For classification:
        Remove RUL and RUL_fca_bin.
    """

    leakage_patterns = [
        "RUL_scaled",
        "RUL_fca_bin",
    ]

    cols_to_drop = []

    for col in df.columns:
        for pattern in leakage_patterns:
            if pattern.lower() == col.lower():
                cols_to_drop.append(col)

    if task == "regression":
        cols_to_drop += [TARGET_CLASSIFICATION]

    if task == "classification":
        cols_to_drop += [TARGET_REGRESSION]

    cols_to_drop = [c for c in cols_to_drop if c in df.columns]

    return df.drop(columns=cols_to_drop, errors="ignore")


def split_features_target(df: pd.DataFrame, target: str):
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' was not found in dataset.")

    y = df[target]
    X = df.drop(columns=[target])

    # Remove datetime columns from direct ML pipeline
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
        ]
    )

    return preprocessor, numeric_cols, categorical_cols


def run_rul_regression(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running supervised RUL regression...")

    df_model = remove_leakage_columns(df, task="regression")
    X, y = split_features_target(df_model, TARGET_REGRESSION)

    # Drop rows without target
    valid_idx = y.notna()
    X = X.loc[valid_idx]
    y = y.loc[valid_idx]

    preprocessor, _, _ = build_preprocessor(X)

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        random_state=42,
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
        random_state=42,
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

    metrics.to_csv(os.path.join(output_dir, "rul_regression_metrics.csv"), index=False)

    print("[RESULT] RUL Regression Metrics")
    print(metrics)

    export_feature_importance(
        pipeline=pipeline,
        X=X,
        output_path=os.path.join(output_dir, "rul_regression_feature_importance.csv"),
    )

    predictions_df = pd.DataFrame(
        {
            "actual_RUL": y_test.values,
            "predicted_RUL": preds,
            "error": y_test.values - preds,
        }
    )

    predictions_df.to_csv(
        os.path.join(output_dir, "rul_regression_predictions.csv"),
        index=False,
    )


def run_rul_classification(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running supervised RUL_class classification...")

    df_model = remove_leakage_columns(df, task="classification")
    X, y = split_features_target(df_model, TARGET_CLASSIFICATION)

    valid_idx = y.notna()
    X = X.loc[valid_idx]
    y = y.loc[valid_idx].astype(str)

    preprocessor, _, _ = build_preprocessor(X)

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
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
        random_state=42,
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
    with open(os.path.join(output_dir, "rul_classification_report.txt"), "w") as f:
        f.write(report)

    cm = pd.DataFrame(
        confusion_matrix(y_test, preds),
        index=sorted(y.unique()),
        columns=sorted(y.unique()),
    )

    cm.to_csv(os.path.join(output_dir, "rul_classification_confusion_matrix.csv"))

    export_feature_importance(
        pipeline=pipeline,
        X=X,
        output_path=os.path.join(output_dir, "rul_classification_feature_importance.csv"),
    )

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


def run_decision_tree_rules(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Extracting decision-tree rules...")

    df_model = remove_leakage_columns(df, task="classification")
    X, y = split_features_target(df_model, TARGET_CLASSIFICATION)

    valid_idx = y.notna()
    X = X.loc[valid_idx]
    y = y.loc[valid_idx].astype(str)

    # For readable rules, use only numeric columns
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) == 0:
        print("[WARNING] No numeric columns available for decision tree rule extraction.")
        return

    X_num = X[numeric_cols].replace([np.inf, -np.inf], np.nan)
    X_num = X_num.fillna(X_num.median(numeric_only=True))

    clf = DecisionTreeClassifier(
        max_depth=4,
        min_samples_leaf=10,
        random_state=42,
        class_weight="balanced",
    )

    clf.fit(X_num, y)

    rules = export_text(clf, feature_names=numeric_cols)

    with open(os.path.join(output_dir, "decision_tree_rules.txt"), "w") as f:
        f.write(rules)

    print("[RESULT] Decision tree rules exported to decision_tree_rules.txt")


def export_feature_importance(pipeline: Pipeline, X: pd.DataFrame, output_path: str):
    model = pipeline.named_steps["model"]
    preprocessor = pipeline.named_steps["preprocess"]

    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        feature_names = [f"feature_{i}" for i in range(len(model.feature_importances_))]

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame(
            {
                "feature": feature_names,
                "importance": model.feature_importances_,
            }
        ).sort_values(by="importance", ascending=False)

        importance_df.to_csv(output_path, index=False)

        print(f"[RESULT] Feature importance exported: {output_path}")


def prepare_unsupervised_matrix(df: pd.DataFrame):
    """
    Uses numerical operational columns only.
    Removes target and obvious leakage columns.
    """

    exclude_cols = [
        TARGET_REGRESSION,
        TARGET_CLASSIFICATION,
        "RUL_fca_bin",
    ]

    X = df.drop(columns=[c for c in exclude_cols if c in df.columns], errors="ignore")
    X = X.select_dtypes(include=[np.number])
    X = X.replace([np.inf, -np.inf], np.nan)

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    X_imputed = imputer.fit_transform(X)
    X_scaled = scaler.fit_transform(X_imputed)

    return X, X_scaled


def run_clustering(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running unsupervised clustering...")

    X_original, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] == 0:
        print("[WARNING] No numerical columns available for clustering.")
        return

    # K-Means
    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10,
    )

    kmeans_labels = kmeans.fit_predict(X_scaled)

    # DBSCAN
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

    summary = result.groupby("kmeans_cluster").agg(
        count=("kmeans_cluster", "size"),
        avg_RUL=(TARGET_REGRESSION, "mean") if TARGET_REGRESSION in result.columns else ("kmeans_cluster", "size"),
    )

    summary.to_csv(os.path.join(output_dir, "kmeans_cluster_summary.csv"))

    print("[RESULT] Clustering results exported.")


def run_pca(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running PCA dimensionality reduction...")

    _, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] < 2:
        print("[WARNING] Not enough numeric features for PCA.")
        return

    pca = PCA(n_components=2, random_state=42)
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

    print("[RESULT] PCA results exported.")


def run_anomaly_detection(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running anomaly detection...")

    _, X_scaled = prepare_unsupervised_matrix(df)

    if X_scaled.shape[1] == 0:
        print("[WARNING] No numeric columns available for anomaly detection.")
        return

    iso = IsolationForest(
        n_estimators=300,
        contamination=0.05,
        random_state=42,
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

    print("[RESULT] Anomaly detection results exported.")


def run_association_rule_mining(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Running association rule mining on FCA/bin columns...")

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

    data = df[bin_cols].copy()
    data = data.fillna("Missing").astype(str)

    transactions = pd.DataFrame()

    for col in data.columns:
        dummies = pd.get_dummies(data[col], prefix=col)
        transactions = pd.concat([transactions, dummies], axis=1)

    transactions = transactions.astype(bool)

    frequent_itemsets = apriori(
        transactions,
        min_support=0.05,
        use_colnames=True,
    )

    if frequent_itemsets.empty:
        print("[WARNING] No frequent itemsets found. Try lowering min_support.")
        return

    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1.2,
    )

    # Prioritize rules that predict RUL_class or RUL-related bins
    rules["contains_RUL_target"] = rules["consequents"].apply(
        lambda x: any("RUL_class" in item or "RUL_fca_bin" in item for item in x)
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

    print("[RESULT] Association rules exported.")


def generate_first_layer_knowledge_report(df: pd.DataFrame, output_dir: str):
    print("\n[INFO] Generating first-layer knowledge report...")

    report_path = os.path.join(output_dir, "first_layer_knowledge_report.txt")

    lines = []

    lines.append("FIRST-LAYER KNOWLEDGE DISCOVERY REPORT")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Dataset size: {df.shape[0]} rows, {df.shape[1]} columns")
    lines.append("")

    if TARGET_REGRESSION in df.columns:
        lines.append("RUL Summary")
        lines.append("-" * 60)
        lines.append(str(df[TARGET_REGRESSION].describe()))
        lines.append("")

    if TARGET_CLASSIFICATION in df.columns:
        lines.append("RUL_class Distribution")
        lines.append("-" * 60)
        lines.append(str(df[TARGET_CLASSIFICATION].value_counts(dropna=False)))
        lines.append("")

    if "workpiece_slice_geometry" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Average RUL by Workpiece Geometry")
        lines.append("-" * 60)
        lines.append(str(df.groupby("workpiece_slice_geometry")[TARGET_REGRESSION].agg(["count", "mean", "median", "min", "max"])))
        lines.append("")

    if "sleeve" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Sleeve-Level RUL Summary")
        lines.append("-" * 60)
        sleeve_summary = df.groupby("sleeve")[TARGET_REGRESSION].agg(["count", "mean", "min", "max"])
        lines.append(str(sleeve_summary.sort_values("mean").head(20)))
        lines.append("")

    if "num_stream" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Average RUL by Stream")
        lines.append("-" * 60)
        lines.append(str(df.groupby("num_stream")[TARGET_REGRESSION].agg(["count", "mean", "median"])))
        lines.append("")

    if "shift" in df.columns and TARGET_REGRESSION in df.columns:
        lines.append("Average RUL by Shift")
        lines.append("-" * 60)
        lines.append(str(df.groupby("shift")[TARGET_REGRESSION].agg(["count", "mean", "median"])))
        lines.append("")

    # Correlation with RUL
    if TARGET_REGRESSION in df.columns:
        numeric_df = df.select_dtypes(include=[np.number])
        if TARGET_REGRESSION in numeric_df.columns:
            corr = numeric_df.corr(numeric_only=True)[TARGET_REGRESSION].drop(TARGET_REGRESSION)
            corr = corr.sort_values(key=lambda x: x.abs(), ascending=False).head(30)

            lines.append("Top Numerical Correlations with RUL")
            lines.append("-" * 60)
            lines.append(str(corr))
            lines.append("")

    lines.append("Interpretable First-Layer Knowledge")
    lines.append("-" * 60)
    lines.append("1. RUL can be modeled as a supervised regression target.")
    lines.append("2. RUL_class can be modeled as a supervised classification target.")
    lines.append("3. Cooling variables are important candidates for degradation analysis.")
    lines.append("4. Steel chemistry variables should be analyzed as degradation context.")
    lines.append("5. Sleeve, crystallizer, and stream identifiers support equipment-specific analysis.")
    lines.append("6. FCA/bin columns enable association rule mining and formal concept-style knowledge extraction.")
    lines.append("7. Clustering can reveal operating regimes with different average RUL values.")
    lines.append("8. Isolation Forest can identify abnormal casts that may correspond to accelerated sleeve degradation.")
    lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[RESULT] Knowledge report exported: {report_path}")


if __name__ == "__main__":
    from pathlib import Path

    # Resolve paths relative to this script location
    SCRIPT_DIR = Path(__file__).resolve().parent

    INPUT_FILE = SCRIPT_DIR / "Dataset" / "PreProcessedDataset.csv"
    OUTPUT_DIR = SCRIPT_DIR / "Analysis1_GPT" / "first_layer_kd"

    # Create output directory
    create_output_dir(str(OUTPUT_DIR))

    # Load and clean dataset
    df = load_dataset(str(INPUT_FILE))
    df = basic_cleaning(df)

    # Generate descriptive knowledge report
    generate_first_layer_knowledge_report(df, str(OUTPUT_DIR))

    # Supervised learning: RUL regression
    if TARGET_REGRESSION in df.columns:
        run_rul_regression(df, str(OUTPUT_DIR))
    else:
        print("[WARNING] RUL column not found. Skipping regression.")

    # Supervised learning: RUL_class classification and rule extraction
    if TARGET_CLASSIFICATION in df.columns:
        run_rul_classification(df, str(OUTPUT_DIR))
        run_decision_tree_rules(df, str(OUTPUT_DIR))
    else:
        print("[WARNING] RUL_class column not found. Skipping classification and rule extraction.")

    # Unsupervised learning and data mining
    run_clustering(df, str(OUTPUT_DIR))
    run_pca(df, str(OUTPUT_DIR))
    run_anomaly_detection(df, str(OUTPUT_DIR))
    run_association_rule_mining(df, str(OUTPUT_DIR))

    print("\n[DONE] Knowledge Discovery pipeline completed.")
    print(f"[DONE] Input file: {INPUT_FILE}")
    print(f"[DONE] Results saved in: {OUTPUT_DIR}")