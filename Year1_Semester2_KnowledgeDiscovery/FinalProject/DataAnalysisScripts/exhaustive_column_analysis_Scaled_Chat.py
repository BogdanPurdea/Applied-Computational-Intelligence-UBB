import os
import re
import pickle
import warnings

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet,
    LogisticRegression,
)
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier,
    ExtraTreesRegressor,
    ExtraTreesClassifier,
    GradientBoostingRegressor,
    GradientBoostingClassifier,
    IsolationForest,
)
from sklearn.svm import SVR, SVC, OneClassSVM
from sklearn.neighbors import (
    KNeighborsRegressor,
    KNeighborsClassifier,
    LocalOutlierFactor,
)
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.inspection import permutation_importance
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import xgboost as xgb
import lightgbm as lgb

from mlxtend.frequent_patterns import apriori, association_rules

warnings.filterwarnings("ignore")

try:
    import catboost as cb
    HAS_CATBOOST = True
except ImportError:
    HAS_CATBOOST = False

try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False

try:
    import umap
    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False


# =============================================================================
# Configuration
# =============================================================================

DATASET_PATH = "Dataset/PreProcessedDataset.csv"
OUTPUT_DIR = "outputChat"
PLOTS_DIR = "plotsChat"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


# =============================================================================
# Helper functions
# =============================================================================

def sanitize_filename(value: str) -> str:
    """
    Convert a column name into a safe filename.
    """
    value = str(value)
    value = re.sub(r'[\\/*?:"<>|]', "_", value)
    value = value.replace(" ", "_").replace(",", "_").replace("/", "_")
    return value


def safe_mode(series: pd.Series, default="Missing"):
    """
    Return first mode safely.
    """
    mode = series.dropna().mode()
    return mode.iloc[0] if not mode.empty else default


def safe_pearson(x: pd.Series, y: pd.Series):
    """
    Pearson correlation with protection against constant columns.
    """
    if x.nunique(dropna=True) <= 1 or y.nunique(dropna=True) <= 1:
        return np.nan, np.nan
    return stats.pearsonr(x, y)


def safe_spearman(x: pd.Series, y: pd.Series):
    """
    Spearman correlation with protection against constant columns.
    """
    if x.nunique(dropna=True) <= 1 or y.nunique(dropna=True) <= 1:
        return np.nan, np.nan
    return stats.spearmanr(x, y)


def resolve_scaled_column(df: pd.DataFrame, original_col: str):
    """
    Resolve the scaled version of an original numeric column.

    Example:
        'resistance, tonn' -> 'resistance, tonn_scaled'

    If the original column is already scaled or no scaled equivalent exists,
    return the original column if present.
    """
    scaled_col = f"{original_col}_scaled"

    if scaled_col in df.columns:
        return scaled_col

    if original_col.endswith("_scaled") and original_col in df.columns:
        return original_col

    if original_col in df.columns:
        return original_col

    return None


def get_base_feature_name(col: str):
    """
    Remove '_scaled' suffix for more readable labels.
    """
    return col[:-7] if col.endswith("_scaled") else col


# =============================================================================
# Step 1: Load dataset
# =============================================================================

print("Step 1: Loading dataset...")

df = pd.read_csv(DATASET_PATH)

# Clean column headers
df.columns = df.columns.str.strip().str.replace(r'["\']', "", regex=True)

# Temporal and categorical columns based on the new dataset structure
temporal_cols = [
    "date",
    "time_temperature_measurement1",
    "time_temperature_measurement2",
    "sample_time_continuous_caster",
    "date_parsed",
    "timestamp",
]

categorical_cols = [
    "steel_type",
    "doc_requirement",
    "workpiece_slice_geometry",
    "alloy_type",
    "kind",
    "sleeve",
    "num_crystallizer",
    "num_stream",
    "shift",
    "RUL_class",
]

target_cols = ["RUL", "RUL_class", "RUL_fca_bin"]

encoded_cols = [c for c in df.columns if c.endswith("_encoded")]
scaled_cols = [c for c in df.columns if c.endswith("_scaled")]
fca_bin_cols = [c for c in df.columns if c.endswith("_fca_bin")]

# Parse timestamp robustly
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
else:
    df["timestamp"] = pd.to_datetime(
        df["date"].astype(str)
        + " "
        + df["sample_time_continuous_caster"].fillna("00:00:00").astype(str),
        errors="coerce",
    )

sort_cols = [
    c for c in ["sleeve", "num_crystallizer", "num_stream", "timestamp"]
    if c in df.columns
]

if sort_cols:
    df = df.sort_values(by=sort_cols).reset_index(drop=True)

# Drop rows with missing target
df_clean = df.dropna(subset=["RUL"]).reset_index(drop=True)

# Use only scaled numeric properties for numeric analytics and models
scaled_numeric_cols = [
    c for c in df_clean.columns
    if c.endswith("_scaled") and pd.api.types.is_numeric_dtype(df_clean[c])
]

if not scaled_numeric_cols:
    raise ValueError(
        "No '*_scaled' numeric columns were found. "
        "The script requires scaled dataset properties."
    )

# Use encoded categoricals only if needed for optional diagnostics.
# Core supervised models are intentionally trained on scaled properties only.
model_feature_cols = scaled_numeric_cols.copy()

print(f"Detected {len(model_feature_cols)} scaled model features.")


# =============================================================================
# Imputation
# =============================================================================

df_imputed = df_clean.copy()

for col in scaled_numeric_cols:
    median_value = df_imputed[col].median()
    df_imputed[col] = df_imputed[col].fillna(median_value)

for col in categorical_cols:
    if col in df_imputed.columns:
        df_imputed[col] = df_imputed[col].fillna(safe_mode(df_imputed[col]))

# If RUL_class is not present, create it
if "RUL_class" not in df_clean.columns:
    df_clean["RUL_class"] = np.select(
        [
            df_clean["RUL"] <= 150,
            df_clean["RUL"] <= 400,
            df_clean["RUL"] <= 800,
        ],
        ["Critical", "Low", "Medium"],
        default="Healthy",
    )
    df_imputed["RUL_class"] = df_clean["RUL_class"]

# Ensure RUL_class has no missing values
df_clean["RUL_class"] = df_clean["RUL_class"].fillna(
    pd.Series(
        np.select(
            [
                df_clean["RUL"] <= 150,
                df_clean["RUL"] <= 400,
                df_clean["RUL"] <= 800,
            ],
            ["Critical", "Low", "Medium"],
            default="Healthy",
        ),
        index=df_clean.index,
    )
)

df_imputed["RUL_class"] = df_clean["RUL_class"]


# =============================================================================
# Step 2: Column-by-column analysis on scaled properties
# =============================================================================

print("Step 2: Starting Column-by-Column Analysis on scaled properties...")

reports = []

# Original business columns to analyze.
# Numeric columns are automatically mapped to their *_scaled versions.
columns_to_analyze_original = [
    "date",
    "steel_type",
    "workpiece_slice_geometry",
    "steel_temperature_grab1, Celsius deg.",
    "resistance, tonn",
    "swing_frequency, amount/minute",
    "crystallizer_movement, mm",
    "alloy_speed, meter/minute",
    "water_consumption, liter/minute",
    "water_temperature_delta, Celsius deg.",
    "water_consumption_secondary_cooling_zone_num1, liter/minute",
    "C, %",
    "Si, %",
    "Mn,%",
    "S, %",
    "P, %",
    "temperature_difference",
    "total_cooling_consumption",
    "average_cooling_consumption",
    "impurity_index",
    "sleeve",
    "num_crystallizer",
    "num_stream",
]

columns_to_analyze = []

for col in columns_to_analyze_original:
    if col in temporal_cols or col in categorical_cols:
        if col in df_clean.columns:
            columns_to_analyze.append(col)
    else:
        scaled_col = resolve_scaled_column(df_clean, col)
        if scaled_col is not None:
            columns_to_analyze.append(scaled_col)

# De-duplicate while preserving order
columns_to_analyze = list(dict.fromkeys(columns_to_analyze))

for col in columns_to_analyze:
    if col not in df_clean.columns:
        continue

    print(f"  Analyzing column: {col}")

    md_sec = []
    base_col_name = get_base_feature_name(col)

    md_sec.append(f"\n# Column: `{col}`")

    unique_cnt = df_clean[col].nunique(dropna=True)
    miss_cnt = df_clean[col].isnull().sum()
    miss_pct = miss_cnt / len(df_clean) * 100
    examples = df_clean[col].dropna().head(3).tolist()

    if col in temporal_cols:
        col_type = "Temporal"
    elif col in categorical_cols:
        col_type = "Categorical / Identifier-like"
    elif col.endswith("_scaled"):
        col_type = "Numeric Scaled"
    elif pd.api.types.is_numeric_dtype(df_clean[col]):
        col_type = "Numeric"
    else:
        col_type = "Categorical / Identifier-like"

    md_sec.append("\n### 1. Metadata")
    md_sec.append(f"- **Inferred Data Type:** {col_type}")
    md_sec.append(f"- **Base Feature:** `{base_col_name}`")
    md_sec.append(f"- **Unique Values:** {unique_cnt}")
    md_sec.append(f"- **Missing Values:** {miss_cnt} ({miss_pct:.2f}%)")
    md_sec.append(f"- **Examples:** {examples}")

    md_sec.append("\n### 2. Descriptive Statistics")

    if col_type in ["Numeric", "Numeric Scaled"]:
        desc = df_clean[col].describe()
        skew = df_clean[col].skew()
        kurt = df_clean[col].kurt()

        md_sec.append(f"- **Mean:** {desc['mean']:.6f}")
        md_sec.append(f"- **Median:** {desc['50%']:.6f}")
        md_sec.append(f"- **Std Dev:** {desc['std']:.6f}")
        md_sec.append(f"- **Min / Max:** {desc['min']:.6f} / {desc['max']:.6f}")
        md_sec.append(f"- **Skewness / Kurtosis:** {skew:.6f} / {kurt:.6f}")

        plt.figure(figsize=(6, 4))
        sns.histplot(df_clean[col].dropna(), kde=True)
        plt.title(f"Distribution of {col}")
        plt.tight_layout()

        plot_path = os.path.join(PLOTS_DIR, f"{sanitize_filename(col)}.png")
        plt.savefig(plot_path)
        plt.close()

        md_sec.append(f"\n![Distribution](../plots/{os.path.basename(plot_path)})")

    elif col_type == "Categorical / Identifier-like":
        freqs = df_clean[col].value_counts(normalize=True).head(5).to_dict()

        md_sec.append("- **Top Categories Frequency:**")
        for cat, freq in freqs.items():
            md_sec.append(f"  - `{cat}`: {freq * 100:.2f}%")

        plt.figure(figsize=(6, 4))
        df_clean[col].value_counts().head(10).plot(kind="bar")
        plt.title(f"Top Categories of {col}")
        plt.tight_layout()

        plot_path = os.path.join(PLOTS_DIR, f"{sanitize_filename(col)}.png")
        plt.savefig(plot_path)
        plt.close()

        md_sec.append(f"\n![Categories](../plots/{os.path.basename(plot_path)})")

    else:
        val_dates = pd.to_datetime(df_clean[col], errors="coerce")
        md_sec.append(f"- **Min Date:** {val_dates.min()}")
        md_sec.append(f"- **Max Date:** {val_dates.max()}")
        md_sec.append(f"- **Span:** {val_dates.max() - val_dates.min()}")

    md_sec.append("\n### 3. Missing Value Analysis")

    missing_rul_mean = df_clean[df_clean[col].isnull()]["RUL"].mean()
    present_rul_mean = df_clean[df_clean[col].notnull()]["RUL"].mean()

    md_sec.append(
        f"- **Relationship to RUL:** Target RUL mean for missing values of `{col}` "
        f"is {missing_rul_mean:.2f} tons vs {present_rul_mean:.2f} tons when populated."
    )

    if col_type in ["Numeric", "Numeric Scaled"]:
        md_sec.append(
            "- **Handling Strategy:** Median imputation applied to scaled numeric feature."
        )
    else:
        md_sec.append(
            "- **Handling Strategy:** Mode imputation applied to categorical or temporal attribute where applicable."
        )

    if col_type in ["Numeric", "Numeric Scaled"]:
        q1 = df_clean[col].quantile(0.25)
        q3 = df_clean[col].quantile(0.75)
        iqr = q3 - q1

        iqr_outliers = (
            (df_clean[col] < q1 - 1.5 * iqr)
            | (df_clean[col] > q3 + 1.5 * iqr)
        ).sum()

        z_scores = np.abs(
            (df_clean[col] - df_clean[col].mean())
            / (df_clean[col].std() + 1e-5)
        )
        z_outliers = (z_scores > 3).sum()

        md_sec.append("\n### 4. Outlier Analysis")
        md_sec.append(
            f"- **IQR Outliers Count / %:** "
            f"{iqr_outliers} ({iqr_outliers / len(df_clean) * 100:.2f}%)"
        )
        md_sec.append(
            f"- **Z-Score Outliers Count / %:** "
            f"{z_outliers} ({z_outliers / len(df_clean) * 100:.2f}%)"
        )

    md_sec.append("\n### 5. Relationship with RUL")

    if col_type in ["Numeric", "Numeric Scaled"]:
        p_val, p_p = safe_pearson(df_imputed[col], df_imputed["RUL"])
        s_val, s_p = safe_spearman(df_imputed[col], df_imputed["RUL"])

        md_sec.append(
            f"- **Pearson Correlation with RUL:** r = {p_val:.6f} "
            f"(p = {p_p:.2e})"
        )
        md_sec.append(
            f"- **Spearman Rank Correlation:** rho = {s_val:.6f} "
            f"(p = {s_p:.2e})"
        )

    elif col_type == "Categorical / Identifier-like" and unique_cnt < 20:
        groups = [
            df_clean[df_clean[col] == val]["RUL"].values
            for val in df_clean[col].dropna().unique()
            if len(df_clean[df_clean[col] == val]) > 1
        ]

        if len(groups) > 1:
            f_val, p_p = stats.f_oneway(*groups)
            md_sec.append(
                f"- **ANOVA Test against RUL:** F-statistic = {f_val:.6f} "
                f"(p = {p_p:.2e})"
            )

    if col_type in ["Numeric", "Numeric Scaled"]:
        md_sec.append("\n### 6. Binned Conceptual Analysis FCA Scaling")

        fca_col = f"{base_col_name}_fca_bin"

        if fca_col in df_clean.columns:
            binned_rul = df_clean.groupby(fca_col)["RUL"].mean().to_dict()
            md_sec.append(f"- **Existing FCA Bin Column Used:** `{fca_col}`")
            md_sec.append("- **Mean RUL by existing FCA bin:**")
            for b, value in binned_rul.items():
                md_sec.append(f"  - `{b}`: {value:.2f} tons")
        else:
            edges = np.unique(
                np.percentile(df_imputed[col].dropna(), [0, 33.3, 66.6, 100])
            )

            if len(edges) > 1:
                labels = ["Low", "Medium", "High"][: len(edges) - 1]
                bins = pd.cut(
                    df_imputed[col],
                    bins=edges,
                    labels=labels,
                    include_lowest=True,
                    duplicates="drop",
                )

                binned_rul = df_clean.groupby(bins)["RUL"].mean().to_dict()

                md_sec.append("- **Mean RUL by quantile bin:**")
                for b, value in binned_rul.items():
                    md_sec.append(f"  - `{b}`: {value:.2f} tons")
            else:
                md_sec.append(
                    "- **Mean RUL by bin:** Only one bin available due to constant value."
                )

        md_sec.append(
            f"- **FCA Attribute Labels:** "
            f"`low_{base_col_name}`, `medium_{base_col_name}`, `high_{base_col_name}`"
        )

    md_sec.append("\n### 7. RUL Class Distribution")

    dist = pd.crosstab(
        df_clean["RUL_class"],
        df_clean[col].isna(),
        normalize="index",
    )

    md_sec.append("- **Class Distribution relative to column presence:**")
    for idx, row in dist.iterrows():
        md_sec.append(f"  - `{idx}`: {row.get(False, 0.0) * 100:.2f}% present")

    reports.append("\n".join(md_sec))


# =============================================================================
# Step 3: Supervised Learning - Regression on scaled properties
# =============================================================================

print("Step 3: Training Regressors on scaled properties...")

X = df_imputed[model_feature_cols].copy()
y = df_clean["RUL"].copy()

# Make feature names ML-library-safe but retain mapping
original_feature_names = X.columns.tolist()
safe_feature_names = (
    X.columns
    .str.replace(r"[,%\[\]{}: /]", "_", regex=True)
    .str.replace(r"_+", "_", regex=True)
    .str.strip("_")
)

feature_name_mapping = dict(zip(safe_feature_names, original_feature_names))
X.columns = safe_feature_names

# Group split by sleeve if available
if "sleeve" in df_clean.columns and df_clean["sleeve"].nunique(dropna=True) > 1:
    groups = df_clean["sleeve"]
else:
    groups = np.arange(len(df_clean))

gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups))

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]
y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

# Features are already scaled, but this additional scaler keeps distance-based
# and neural models numerically stable if upstream scaling was inconsistent.
distance_scaler = StandardScaler()
X_train_s = distance_scaler.fit_transform(X_train)
X_test_s = distance_scaler.transform(X_test)

reg_models = {
    "Linear Regression": LinearRegression(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "ElasticNet": ElasticNet(),
    "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=42),
    "Random Forest": RandomForestRegressor(
        n_estimators=20,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    ),
    "Extra Trees": ExtraTreesRegressor(
        n_estimators=20,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=20,
        max_depth=6,
        random_state=42,
    ),
    "XGBoost": xgb.XGBRegressor(
        n_estimators=20,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
        objective="reg:squarederror",
    ),
    "LightGBM": lgb.LGBMRegressor(
        n_estimators=20,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
        verbose=-1,
    ),
    "SVR": SVR(C=10.0),
    "KNN Regressor": KNeighborsRegressor(n_neighbors=5),
    "MLP Regressor": MLPRegressor(
        hidden_layer_sizes=(16, 8),
        max_iter=50,
        random_state=42,
    ),
}

if HAS_CATBOOST:
    reg_models["CatBoost"] = cb.CatBoostRegressor(
        iterations=20,
        depth=6,
        verbose=0,
        random_state=42,
    )

reg_results = []

for name, model in reg_models.items():
    try:
        if name in ["SVR", "KNN Regressor", "MLP Regressor"]:
            sub_idx = np.random.default_rng(42).choice(
                len(X_train_s),
                min(2000, len(X_train_s)),
                replace=False,
            )
            model.fit(X_train_s[sub_idx], y_train.iloc[sub_idx])
            preds = model.predict(X_test_s)
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        mape = np.mean(np.abs((y_test - preds) / (y_test + 1e-5)))

        reg_results.append(
            {
                "Model": name,
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
                "MAPE": mape,
            }
        )

    except Exception as e:
        print(f"  Regressor failed: {name}: {e}")
        reg_results.append(
            {
                "Model": name,
                "MAE": np.nan,
                "RMSE": np.nan,
                "R2": np.nan,
                "MAPE": np.nan,
            }
        )

df_reg_metrics = pd.DataFrame(reg_results)
df_reg_metrics.to_csv(
    os.path.join(OUTPUT_DIR, "model_comparison.csv"),
    index=False,
)


# =============================================================================
# Step 4: Supervised Learning - Classification on scaled properties
# =============================================================================

print("Step 4: Training Classifiers on scaled properties...")

le_class = LabelEncoder()
y_c = le_class.fit_transform(df_clean["RUL_class"])

y_train_c = y_c[train_idx]
y_test_c = y_c[test_idx]

clf_models = {
    "Logistic Regression": LogisticRegression(max_iter=100),
    "Decision Tree Classifier": DecisionTreeClassifier(
        max_depth=8,
        random_state=42,
    ),
    "Random Forest Classifier": RandomForestClassifier(
        n_estimators=20,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    ),
    "Extra Trees Classifier": ExtraTreesClassifier(
        n_estimators=20,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    ),
    "Gradient Boosting Classifier": GradientBoostingClassifier(
        n_estimators=20,
        max_depth=6,
        random_state=42,
    ),
    "XGBoost Classifier": xgb.XGBClassifier(
        n_estimators=20,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
        eval_metric="mlogloss",
    ),
    "LightGBM Classifier": lgb.LGBMClassifier(
        n_estimators=20,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
        verbose=-1,
    ),
    "SVM Classifier": SVC(),
    "KNN Classifier": KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes": GaussianNB(),
    "MLP Classifier": MLPClassifier(
        hidden_layer_sizes=(16, 8),
        max_iter=50,
        random_state=42,
    ),
}

if HAS_CATBOOST:
    clf_models["CatBoost Classifier"] = cb.CatBoostClassifier(
        iterations=20,
        depth=6,
        verbose=0,
        random_state=42,
    )

clf_results = []

for name, model in clf_models.items():
    try:
        if name in ["SVM Classifier", "KNN Classifier", "MLP Classifier"]:
            sub_idx = np.random.default_rng(42).choice(
                len(X_train_s),
                min(2000, len(X_train_s)),
                replace=False,
            )
            model.fit(X_train_s[sub_idx], y_train_c[sub_idx])
            preds = model.predict(X_test_s)
        else:
            model.fit(X_train, y_train_c)
            preds = model.predict(X_test)

        acc = accuracy_score(y_test_c, preds)
        prec = precision_score(
            y_test_c,
            preds,
            average="macro",
            zero_division=0,
        )
        rec = recall_score(
            y_test_c,
            preds,
            average="macro",
            zero_division=0,
        )
        f1 = f1_score(
            y_test_c,
            preds,
            average="macro",
            zero_division=0,
        )

        clf_results.append(
            {
                "Model": name,
                "Accuracy": acc,
                "Precision": prec,
                "Recall": rec,
                "F1-score": f1,
            }
        )

    except Exception as e:
        print(f"  Classifier failed: {name}: {e}")
        clf_results.append(
            {
                "Model": name,
                "Accuracy": np.nan,
                "Precision": np.nan,
                "Recall": np.nan,
                "F1-score": np.nan,
            }
        )

df_clf_metrics = pd.DataFrame(clf_results)
df_clf_metrics.to_csv(
    os.path.join(OUTPUT_DIR, "model_comparison_classifier.csv"),
    index=False,
)


# =============================================================================
# Step 5: Feature Importance Ranking on scaled properties
# =============================================================================

print("Step 5: Ranking scaled features...")

rf = RandomForestRegressor(
    n_estimators=20,
    max_depth=8,
    random_state=42,
    n_jobs=-1,
)

rf.fit(X, y)

df_feat_imp = pd.DataFrame(
    {
        "Feature": X.columns,
        "Original_Feature": [feature_name_mapping.get(c, c) for c in X.columns],
        "Importance": rf.feature_importances_,
    }
).sort_values(by="Importance", ascending=False)

df_feat_imp.to_csv(
    os.path.join(OUTPUT_DIR, "feature_importance.csv"),
    index=False,
)


# =============================================================================
# Step 6: Unsupervised Clustering and PCA on scaled properties
# =============================================================================

print("Step 6: Running Clustering and PCA on scaled properties...")

sample_size = min(1500, len(X))

X_sample_df = X.sample(sample_size, random_state=42)
X_sample = X_sample_df.values

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init="auto",
).fit(X_sample)

pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_sample)

plt.figure(figsize=(6, 4))
plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=kmeans.labels_,
    cmap="viridis",
    s=5,
)
plt.title("Operating Regimes in Latent Space PCA - Scaled Features")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "kmeans_operating_regimes.png"))
plt.close()

df_pca = pd.DataFrame(
    {
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
        "Cluster": kmeans.labels_,
    }
)

df_pca.to_csv(
    os.path.join(OUTPUT_DIR, "pca_kmeans_projection.csv"),
    index=False,
)


# =============================================================================
# Step 7: Association Rules on scaled properties
# =============================================================================

print("Step 7: Mining Association Rules on scaled properties...")

df_assoc = pd.DataFrame(index=df_clean.index)

association_source_cols = {
    "High_Temp_Scaled": "steel_temperature_grab1, Celsius deg._scaled",
    "High_Resistance_Scaled": "resistance, tonn_scaled",
    "High_Cooling_Scaled": "water_consumption, liter/minute_scaled",
    "High_Temp_Delta_Scaled": "water_temperature_delta, Celsius deg._scaled",
    "High_Total_Cooling_Scaled": "total_cooling_consumption_scaled",
    "High_Impurity_Index_Scaled": "impurity_index_scaled",
}

for item_name, source_col in association_source_cols.items():
    if source_col in df_imputed.columns:
        df_assoc[item_name] = (
            df_imputed[source_col] >= df_imputed[source_col].median()
        )

df_assoc["Critical_RUL"] = df_clean["RUL"] <= 150

# Ensure all columns are boolean and no missing values exist
df_assoc = df_assoc.fillna(False).astype(bool)

if df_assoc.shape[1] >= 2:
    freq_items = apriori(
        df_assoc,
        min_support=0.01,
        use_colnames=True,
    )

    if not freq_items.empty:
        rules = association_rules(
            freq_items,
            metric="confidence",
            min_threshold=0.3,
        )
    else:
        rules = pd.DataFrame()
else:
    freq_items = pd.DataFrame()
    rules = pd.DataFrame()

freq_items.to_csv(
    os.path.join(OUTPUT_DIR, "frequent_itemsets.csv"),
    index=False,
)

rules.to_csv(
    os.path.join(OUTPUT_DIR, "association_rules.csv"),
    index=False,
)


# =============================================================================
# Step 8: Compile Markdown and HTML Reports
# =============================================================================

print("Step 8: Assembling Final Markdown and HTML Reports...")

report_content = []

report_content.append(
    "# Exhaustive Column-by-Column Data Analysis and Knowledge Discovery Report"
)
report_content.append("\n**Dataset:** Continuous Casting of Steel SCADA Database")
report_content.append(f"**Total Records:** {len(df_clean)}")
report_content.append(
    f"**Numeric Feature Policy:** All numeric modeling and numeric analytics use "
    f"`*_scaled` columns only."
)
report_content.append(f"**Scaled Feature Count:** {len(model_feature_cols)}")

report_content.append("\n## Executive Summary and Industrial Discoveries")
report_content.append(
    "The pipeline has been refactored to operate on standardized numeric feature "
    "properties. This ensures that regression, classification, feature importance, "
    "clustering, PCA, and association-rule mining are executed against the scaled "
    "feature space instead of raw industrial measurements."
)

report_content.append("\n### Top 10 Critical Degradation Indicators")
report_content.append(
    "The following indicators should be interpreted through their corresponding "
    "`*_scaled` variables and validated against model-derived feature importance "
    "and association-rule outputs."
)
report_content.append(
    "1. **High scaled resistance** indicates abnormal crystallizer mechanical load."
)
report_content.append(
    "2. **High scaled alloy speed** may accelerate sleeve wear through increased throughput stress."
)
report_content.append(
    "3. **High scaled water temperature delta** may indicate inefficient thermal extraction."
)
report_content.append(
    "4. **High scaled impurity index** may increase defect-prone operating conditions."
)
report_content.append(
    "5. **High scaled crystallizer movement** may increase localized mechanical wear."
)
report_content.append(
    "6. **Abnormal scaled temperature difference** may expose unstable heat-transfer behavior."
)
report_content.append(
    "7. **High scaled total cooling consumption** may indicate compensatory cooling regimes."
)
report_content.append(
    "8. **Low or abnormal scaled primary cooling flow** may accelerate thermal fatigue."
)
report_content.append(
    "9. **Scaled chemistry indicators such as C, S, P, and Mn** should be monitored for composition-driven degradation."
)
report_content.append(
    "10. **Latent PCA and KMeans regimes** should be reviewed as operating-state clusters."
)

report_content.append("\n## Regression Model Comparison")
report_content.append(
    df_reg_metrics.sort_values("RMSE", na_position="last").to_markdown(index=False)
)

report_content.append("\n## Classification Model Comparison")
report_content.append(
    df_clf_metrics.sort_values("F1-score", ascending=False, na_position="last")
    .to_markdown(index=False)
)

report_content.append("\n## Top 25 Scaled Feature Importances")
report_content.append(df_feat_imp.head(25).to_markdown(index=False))

report_content.append("\n## Individual Column Analysis Reports")
report_content.extend(reports)

md_report_path = os.path.join(OUTPUT_DIR, "column_analysis_report.md")

with open(md_report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_content))


# Basic HTML wrapper
html_report_path = os.path.join(OUTPUT_DIR, "column_analysis_report.html")

html_body = "\n".join(report_content)

html_body = (
    html_body
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
)

html_body = re.sub(r"^# (.*)$", r"<h1>\1</h1>", html_body, flags=re.MULTILINE)
html_body = re.sub(r"^## (.*)$", r"<h2>\1</h2>", html_body, flags=re.MULTILINE)
html_body = re.sub(r"^### (.*)$", r"<h3>\1</h3>", html_body, flags=re.MULTILINE)
html_body = re.sub(r"^\- (.*)$", r"<li>\1</li>", html_body, flags=re.MULTILINE)
html_body = html_body.replace("\n", "<br>\n")

html_content = f"""
<html>
<head>
    <title>Scaled Feature Analysis Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }}
        pre {{
            background: #f4f4f4;
            padding: 10px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 4px;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_report_path, "w", encoding="utf-8") as f:
    f.write(html_content)


# =============================================================================
# Save pipeline metadata
# =============================================================================

metadata = {
    "scaled_numeric_features": model_feature_cols,
    "safe_feature_name_mapping": feature_name_mapping,
    "class_labels": list(le_class.classes_),
    "pca_explained_variance_ratio": pca.explained_variance_ratio_.tolist(),
}

with open(os.path.join(OUTPUT_DIR, "pipeline_metadata.pkl"), "wb") as f:
    pickle.dump(metadata, f)


print("Scaled column-by-column pipeline successfully executed.")
print("Generated files:")
print(f"  - {md_report_path}")
print(f"  - {html_report_path}")
print(f"  - {os.path.join(OUTPUT_DIR, 'model_comparison.csv')}")
print(f"  - {os.path.join(OUTPUT_DIR, 'model_comparison_classifier.csv')}")
print(f"  - {os.path.join(OUTPUT_DIR, 'feature_importance.csv')}")
print(f"  - {os.path.join(OUTPUT_DIR, 'association_rules.csv')}")
print(f"  - {os.path.join(OUTPUT_DIR, 'frequent_itemsets.csv')}")
print(f"  - {os.path.join(OUTPUT_DIR, 'pca_kmeans_projection.csv')}")
print(f"  - {os.path.join(OUTPUT_DIR, 'pipeline_metadata.pkl')}")