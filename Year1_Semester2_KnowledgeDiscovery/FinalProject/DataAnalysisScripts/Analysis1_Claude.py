import os
import re
import sys
import argparse
import logging
import traceback
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Optional imports
try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False

try:
    from mlxtend.frequent_patterns import fpgrowth, association_rules
    MLXTEND_AVAILABLE = True
except ImportError:
    MLXTEND_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def safe_execution(func):
    """Decorator to safely execute algorithms and return None on failure."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.warning(f"Error in {func.__name__}: {e}")
            logging.debug(traceback.format_exc())
            return None
    return wrapper


class UnsupervisedAnalyzer:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.df = None

        # Column groups detected from dataset structure
        self.scaled_cols = []       # columns ending in _scaled  → feature matrix
        self.encoded_cols = []      # columns ending in _encoded → already-numeric categoricals
        self.fca_bin_cols = []      # columns ending in _fca_bin → pre-binned for association rules

        # Aliases kept for backward-compatible internal references
        self.numeric_cols = []      # = scaled_cols
        self.categorical_cols = []  # = encoded_cols

        self.target_col = 'RUL'
        self.rul_class_col = 'RUL_class'

        self.preprocessed_df = None
        self.scaled_data = None     # numpy array: rows × _scaled features

        self.labels = {}
        self.embeddings = {}
        self.anomaly_scores = {}
        self.assoc_rules = None

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """
        Convert an arbitrary column name to a filesystem-safe string.
        Replaces any character that is not alphanumeric, a dash, or an
        underscore with '_', then collapses consecutive underscores.
        """
        safe = re.sub(r'[^\w\-]', '_', str(name))
        safe = re.sub(r'_+', '_', safe).strip('_')
        return safe[:100]  # cap length to avoid OS path-length issues

    # ------------------------------------------------------------------
    # Pipeline steps
    # ------------------------------------------------------------------

    def load_data(self):
        logging.info(f"Loading data from {self.input_file}")
        self.df = pd.read_csv(self.input_file, low_memory=False)

        # Detect column groups by suffix convention
        self.scaled_cols  = [c for c in self.df.columns if c.endswith('_scaled')]
        self.encoded_cols = [c for c in self.df.columns if c.endswith('_encoded')]
        self.fca_bin_cols = [c for c in self.df.columns if c.endswith('_fca_bin')]

        # Aliases
        self.numeric_cols     = self.scaled_cols
        self.categorical_cols = self.encoded_cols

        logging.info(
            f"Detected  {len(self.scaled_cols)} _scaled columns "
            f"| {len(self.encoded_cols)} _encoded columns "
            f"| {len(self.fca_bin_cols)} _fca_bin columns"
        )
        if not self.scaled_cols:
            raise ValueError(
                "No '_scaled' columns found. "
                "Please ensure the dataset contains pre-scaled features."
            )

    def preprocess_data(self):
        """
        The dataset already contains StandardScaled values in _scaled columns.
        We only need to:
          1. Drop rows where RUL is missing.
          2. Impute any residual NaN in scaled/encoded columns.
          3. Build the feature matrix from _scaled columns only.
          4. Ensure RUL_class exists (use pre-computed column when available).
        """
        logging.info("Preprocessing pre-scaled data...")
        df_clean = self.df.copy()

        # 1. Drop rows without RUL target
        if self.target_col in df_clean.columns:
            before = len(df_clean)
            df_clean = df_clean.dropna(subset=[self.target_col]).reset_index(drop=True)
            logging.info(f"Dropped {before - len(df_clean)} rows with missing '{self.target_col}'.")

        # 2. Impute residual NaN values in scaled columns
        if self.scaled_cols:
            num_imputer = SimpleImputer(strategy='median')
            df_clean[self.scaled_cols] = num_imputer.fit_transform(df_clean[self.scaled_cols])

        # 3. Impute encoded columns
        if self.encoded_cols:
            enc_imputer = SimpleImputer(strategy='most_frequent')
            df_clean[self.encoded_cols] = enc_imputer.fit_transform(df_clean[self.encoded_cols])

        # 4. Ensure RUL_class exists
        if self.rul_class_col not in df_clean.columns:
            if self.target_col in df_clean.columns:
                try:
                    df_clean[self.rul_class_col] = pd.qcut(
                        df_clean[self.target_col], q=3,
                        labels=['Critical', 'Low', 'Healthy'], duplicates='drop'
                    )
                    logging.info("Derived 'RUL_class' from RUL via quantile binning.")
                except ValueError:
                    df_clean[self.rul_class_col] = df_clean[self.target_col].astype(str)
            else:
                logging.warning("Neither 'RUL_class' nor 'RUL' columns found; RUL analysis will be skipped.")

        self.preprocessed_df = df_clean

        # 5. Feature matrix: _scaled columns only (already StandardScaled — no re-scaling)
        self.scaled_data = df_clean[self.scaled_cols].values.astype(float)
        logging.info(f"Feature matrix shape: {self.scaled_data.shape}")

    # ------------------------------------------------------------------
    # Clustering
    # ------------------------------------------------------------------

    @safe_execution
    def run_clustering(self):
        logging.info("Running clustering algorithms on pre-scaled features...")

        logging.info(" - K-Means (k=3)")
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.labels['KMeans'] = kmeans.fit_predict(self.scaled_data)

        logging.info(" - Hierarchical / Agglomerative (k=3)")
        hc = AgglomerativeClustering(n_clusters=3)
        self.labels['Hierarchical'] = hc.fit_predict(self.scaled_data)

        logging.info(" - DBSCAN")
        dbscan = DBSCAN(eps=3.0, min_samples=5)
        self.labels['DBSCAN'] = dbscan.fit_predict(self.scaled_data)

        logging.info(" - Gaussian Mixture Model (k=3)")
        gmm = GaussianMixture(n_components=3, random_state=42)
        self.labels['GMM'] = gmm.fit_predict(self.scaled_data)

    # ------------------------------------------------------------------
    # Anomaly detection
    # ------------------------------------------------------------------

    @safe_execution
    def run_anomaly_detection(self):
        logging.info("Running anomaly detection on pre-scaled features...")

        logging.info(" - Isolation Forest")
        iso = IsolationForest(contamination=0.05, random_state=42)
        self.labels['IsolationForest'] = iso.fit_predict(self.scaled_data)
        self.anomaly_scores['IsolationForest'] = iso.decision_function(self.scaled_data)

        logging.info(" - Local Outlier Factor")
        lof = LocalOutlierFactor(contamination=0.05)
        self.labels['LOF'] = lof.fit_predict(self.scaled_data)
        self.anomaly_scores['LOF'] = lof.negative_outlier_factor_

        logging.info(" - One-Class SVM")
        ocsvm = OneClassSVM(nu=0.05)
        self.labels['OneClassSVM'] = ocsvm.fit_predict(self.scaled_data)
        self.anomaly_scores['OneClassSVM'] = ocsvm.decision_function(self.scaled_data)

    # ------------------------------------------------------------------
    # Dimensionality reduction
    # ------------------------------------------------------------------

    @safe_execution
    def run_dimensionality_reduction(self):
        logging.info("Running dimensionality reduction on pre-scaled features...")

        logging.info(" - PCA (2 components)")
        pca = PCA(n_components=2, random_state=42)
        self.embeddings['PCA'] = pca.fit_transform(self.scaled_data)

        logging.info(" - t-SNE (2 components)")
        tsne = TSNE(n_components=2, random_state=42, init='pca', learning_rate='auto')
        self.embeddings['tSNE'] = tsne.fit_transform(self.scaled_data)

        if UMAP_AVAILABLE:
            logging.info(" - UMAP (2 components)")
            reducer = umap.UMAP(random_state=42)
            self.embeddings['UMAP'] = reducer.fit_transform(self.scaled_data)
        else:
            logging.info(" - UMAP skipped (package not installed).")

    # ------------------------------------------------------------------
    # Association rules — uses pre-binned _fca_bin columns directly
    # ------------------------------------------------------------------

    @safe_execution
    def run_association_rules(self):
        logging.info("Running association rules extraction...")

        if not MLXTEND_AVAILABLE:
            logging.warning("mlxtend not installed — skipping association rules.")
            return

        if not self.fca_bin_cols:
            logging.warning("No '_fca_bin' columns found — skipping association rules.")
            return

        # Use the pre-binned columns that the dataset already provides.
        # They already contain ordinal labels such as Low / Medium / High.
        df_bin = self.preprocessed_df[self.fca_bin_cols].copy().astype(str)

        # Bring in RUL_class as additional context if not already in fca_bin_cols
        if self.rul_class_col in self.preprocessed_df.columns:
            rul_bin_col = 'RUL_fca_bin'
            if rul_bin_col not in df_bin.columns:
                df_bin[rul_bin_col] = self.preprocessed_df[self.rul_class_col].astype(str)

        # One-hot encode and cast to bool (required by mlxtend)
        df_dummies = pd.get_dummies(df_bin).astype(bool)
        logging.info(
            f" - FP-Growth on {df_dummies.shape[1]} one-hot features "
            f"(min_support=0.15, max_len=3)"
        )

        frequent_itemsets = fpgrowth(
            df_dummies, min_support=0.15, use_colnames=True, max_len=3
        )

        if len(frequent_itemsets) == 0:
            logging.warning("No frequent itemsets found; consider lowering min_support.")
            return

        self.assoc_rules = association_rules(
            frequent_itemsets,
            metric="confidence",
            min_threshold=0.5,
            num_itemsets=len(frequent_itemsets),
        )
        out_path = os.path.join(self.output_dir, 'global_association_rules.csv')
        self.assoc_rules.to_csv(out_path, index=False)
        logging.info(
            f"Extracted {len(self.assoc_rules)} association rules → {out_path}"
        )

    # ------------------------------------------------------------------
    # Plotting helper
    # ------------------------------------------------------------------

    def _safe_plot(self, plot_func, filepath, *args, **kwargs):
        try:
            fig, ax = plt.subplots(figsize=(8, 6))
            kwargs.setdefault('ax', ax)
            plot_func(*args, **kwargs)
            plt.tight_layout()
            plt.savefig(filepath, dpi=100)
            plt.close(fig)
        except Exception as e:
            logging.warning(f"Plot failed [{os.path.basename(filepath)}]: {e}")
            plt.close('all')

    # ------------------------------------------------------------------
    # Per-column analysis
    # ------------------------------------------------------------------

    def analyze_column(self, col: str):
        """
        Generate per-column CSV summaries and scatter/distribution plots.
        Directory names are sanitized to be filesystem-safe.
        """
        safe_name = self._sanitize_name(col)
        col_dir   = os.path.join(self.output_dir, safe_name)
        plots_dir = os.path.join(col_dir, f"{safe_name}_plots")
        os.makedirs(plots_dir, exist_ok=True)

        df_col = self.preprocessed_df.copy()

        # Attach clustering / anomaly / embedding results as extra columns
        for k, v in self.labels.items():
            if v is not None:
                df_col[k] = v
        for k, v in self.anomaly_scores.items():
            if v is not None:
                df_col[f'{k}_score'] = v
        for k, v in self.embeddings.items():
            if v is not None:
                df_col[f'{k}_x'] = v[:, 0]
                df_col[f'{k}_y'] = v[:, 1]

        # All _scaled and _encoded columns are numeric; treat them uniformly
        is_num = True

        # ---- Descriptive profile ----
        profile = df_col[col].describe().to_frame()
        profile.to_csv(os.path.join(col_dir, f"{safe_name}_profile.csv"))

        # ---- Cluster summary ----
        active_cluster_cols = [k for k, v in self.labels.items() if v is not None]
        if active_cluster_cols:
            try:
                cluster_summary = df_col.groupby(active_cluster_cols)[col].describe()
                cluster_summary.to_csv(
                    os.path.join(col_dir, f"{safe_name}_cluster_summary.csv")
                )
            except Exception as e:
                logging.warning(f"Cluster summary skipped for '{col}': {e}")

        # ---- Anomaly summary ----
        present_anomaly_cols = [
            k for k in ('IsolationForest', 'LOF', 'OneClassSVM')
            if k in df_col.columns
        ]
        if present_anomaly_cols:
            try:
                anomaly_summary = df_col.groupby(present_anomaly_cols)[col].describe()
                anomaly_summary.to_csv(
                    os.path.join(col_dir, f"{safe_name}_anomaly_summary.csv")
                )
            except Exception as e:
                logging.warning(f"Anomaly summary skipped for '{col}': {e}")

        # ---- RUL class summary ----
        if self.rul_class_col in df_col.columns:
            try:
                rul_summary = df_col.groupby(self.rul_class_col)[col].describe()
                rul_summary.to_csv(
                    os.path.join(col_dir, f"{safe_name}_rul_class_summary.csv")
                )
            except Exception as e:
                logging.warning(f"RUL class summary skipped for '{col}': {e}")

        # ---- Association rules relevant to this column ----
        if self.assoc_rules is not None:
            try:
                col_str = str(col)
                mask = (
                    self.assoc_rules['antecedents'].apply(
                        lambda x: any(col_str in str(item) for item in x)
                    ) |
                    self.assoc_rules['consequents'].apply(
                        lambda x: any(col_str in str(item) for item in x)
                    )
                )
                col_rules = self.assoc_rules[mask]
                col_rules.to_csv(
                    os.path.join(col_dir, f"{safe_name}_association_rules.csv"),
                    index=False,
                )
            except Exception as e:
                logging.warning(f"Association rules output skipped for '{col}': {e}")

        # ================================================================
        # Plots
        # ================================================================

        # Distribution (histogram + KDE for numeric)
        self._safe_plot(
            sns.histplot,
            os.path.join(plots_dir, 'distribution.png'),
            data=df_col, x=col, kde=True
        )

        # Boxplot by RUL class
        if self.rul_class_col in df_col.columns:
            self._safe_plot(
                sns.boxplot,
                os.path.join(plots_dir, 'boxplot_rul_class.png'),
                data=df_col, x=self.rul_class_col, y=col
            )

        # Boxplot by clustering labels
        for algo in ('KMeans', 'GMM', 'DBSCAN', 'Hierarchical'):
            if algo in df_col.columns:
                self._safe_plot(
                    sns.boxplot,
                    os.path.join(plots_dir, f'value_by_{algo.lower()}.png'),
                    data=df_col, x=algo, y=col
                )

        # Anomaly score scatter (Isolation Forest)
        if 'IsolationForest_score' in df_col.columns:
            self._safe_plot(
                sns.scatterplot,
                os.path.join(plots_dir, 'anomaly_score_if.png'),
                data=df_col, x=col, y='IsolationForest_score'
            )

        # ---- 2-D Embedding scatters ----
        for embed_name in ('PCA', 'tSNE', 'UMAP'):
            x_col = f'{embed_name}_x'
            y_col = f'{embed_name}_y'
            if x_col not in df_col.columns:
                continue

            # Colour by this feature value (continuous → no hue truncation needed)
            try:
                self._safe_plot(
                    sns.scatterplot,
                    os.path.join(plots_dir, f'{embed_name.lower()}_scatter_col.png'),
                    data=df_col, x=x_col, y=y_col, hue=col,
                    palette='viridis', legend=False
                )
            except Exception as e:
                logging.warning(f"{embed_name} scatter (col) failed for '{col}': {e}")

            # Colour by RUL class
            if self.rul_class_col in df_col.columns:
                self._safe_plot(
                    sns.scatterplot,
                    os.path.join(plots_dir, f'{embed_name.lower()}_scatter_rul.png'),
                    data=df_col, x=x_col, y=y_col, hue=self.rul_class_col
                )

    # ------------------------------------------------------------------
    # Global output files
    # ------------------------------------------------------------------

    def generate_global_outputs(self):
        logging.info("Generating global outputs...")

        # Cluster assignment table
        cluster_df = pd.DataFrame(
            {k: v for k, v in self.labels.items() if v is not None}
        )
        cluster_df.to_csv(
            os.path.join(self.output_dir, 'global_cluster_assignments.csv'), index=False
        )

        # Anomaly score table
        anomaly_df = pd.DataFrame(
            {k: v for k, v in self.anomaly_scores.items() if v is not None}
        )
        anomaly_df.to_csv(
            os.path.join(self.output_dir, 'global_anomaly_scores.csv'), index=False
        )

        # 2-D embedding coordinates
        embed_dict = {}
        for k, v in self.embeddings.items():
            if v is not None:
                embed_dict[f'{k}_x'] = v[:, 0]
                embed_dict[f'{k}_y'] = v[:, 1]
        pd.DataFrame(embed_dict).to_csv(
            os.path.join(self.output_dir, 'global_dimensionality_embeddings.csv'),
            index=False,
        )

        # Markdown report
        report_path = os.path.join(self.output_dir, 'global_report.md')
        with open(report_path, 'w') as f:
            f.write("# Global Unsupervised Analysis Report\n\n")
            f.write("## Dataset Overview\n")
            f.write(f"- Total rows (after RUL filter): {len(self.preprocessed_df)}\n")
            f.write(f"- Pre-scaled feature columns (_scaled): {len(self.scaled_cols)}\n")
            f.write(f"- Encoded categorical columns (_encoded): {len(self.encoded_cols)}\n")
            f.write(f"- FCA-binned columns (_fca_bin): {len(self.fca_bin_cols)}\n")
            f.write(f"- Feature matrix shape: {self.scaled_data.shape}\n")
            f.write("\n> Data was already StandardScaled prior to ingestion. "
                    "No additional scaling was applied.\n")

            f.write("\n## Clustering\n")
            f.write("K-Means, Hierarchical (Agglomerative), DBSCAN, and GMM (k=3) "
                    "were applied directly on pre-scaled features.\n")
            for algo, lbl in self.labels.items():
                if lbl is not None:
                    unique = np.unique(lbl)
                    f.write(f"- **{algo}**: {len(unique)} unique labels → {unique.tolist()}\n")

            f.write("\n## Anomaly Detection\n")
            f.write("Isolation Forest, LOF, and One-Class SVM applied "
                    "(contamination / nu = 0.05).\n")
            for algo, scores in self.anomaly_scores.items():
                if scores is not None:
                    f.write(
                        f"- **{algo}**: score range "
                        f"[{scores.min():.4f}, {scores.max():.4f}]\n"
                    )

            f.write("\n## Dimensionality Reduction\n")
            f.write(f"- PCA (2 components): {'✓' if 'PCA' in self.embeddings else '✗'}\n")
            f.write(f"- t-SNE (2 components): {'✓' if 'tSNE' in self.embeddings else '✗'}\n")
            f.write(f"- UMAP installed: {UMAP_AVAILABLE} "
                    f"{'→ ✓ applied' if 'UMAP' in self.embeddings else ''}\n")

            f.write("\n## Association Rules\n")
            f.write(f"- mlxtend installed: {MLXTEND_AVAILABLE}\n")
            if self.assoc_rules is not None:
                f.write(f"- Rules extracted: {len(self.assoc_rules)}\n")
                f.write("- Source: pre-binned `_fca_bin` columns (no re-binning applied)\n")
            else:
                f.write("- No rules extracted (mlxtend missing or no frequent itemsets).\n")

            f.write("\n## Recommendations\n")
            f.write(
                "- Extract top confidence rules for FCA scaling in ToscanaJ "
                "focused on Critical RUL associations.\n"
                "- Review DBSCAN noise points (label = -1) as potential process anomalies.\n"
                "- Compare IsolationForest and LOF outlier sets for consensus anomalies.\n"
            )

        logging.info(f"Global report written to {report_path}")

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)

        self.load_data()
        self.preprocess_data()

        self.run_clustering()
        self.run_anomaly_detection()
        self.run_dimensionality_reduction()
        self.run_association_rules()

        # Analyse every _scaled and _encoded column individually
        cols_to_analyze = self.scaled_cols + self.encoded_cols
        logging.info(f"Analysing {len(cols_to_analyze)} columns individually...")

        for idx, col in enumerate(cols_to_analyze, start=1):
            logging.info(f"  [{idx}/{len(cols_to_analyze)}] {col}")
            self.analyze_column(col)

        self.generate_global_outputs()
        logging.info("Analysis complete.")


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

if __name__ == "__main__":
    from pathlib import Path

    # ------------------------------------------------------------
    # Resolve paths relative to this script location
    # ------------------------------------------------------------

    SCRIPT_DIR = Path(__file__).resolve().parent

    INPUT_FILE = SCRIPT_DIR / "Dataset" / "PreProcessedDataset.csv"
    OUTPUT_DIR = SCRIPT_DIR / "Analysis1_Outputs_Claude" / "unsupervised_scaled"

    # ------------------------------------------------------------
    # Run analysis
    # ------------------------------------------------------------

    analyzer = UnsupervisedAnalyzer(
        input_file=str(INPUT_FILE),
        output_dir=str(OUTPUT_DIR)
    )

    analyzer.run()