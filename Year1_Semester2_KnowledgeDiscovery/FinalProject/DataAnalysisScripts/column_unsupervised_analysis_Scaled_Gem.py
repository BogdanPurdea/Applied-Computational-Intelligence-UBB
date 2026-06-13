import os
import argparse
import logging
import traceback
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Imports optional libraries.
try:
    import umap

    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False

try:
    from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules

    MLXTEND_AVAILABLE = True
except ImportError:
    MLXTEND_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def safe_execution(func):
    """Decorator to execute algorithms safely and return None upon failure."""

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
        self.numeric_cols = []
        self.categorical_cols = []
        self.scaled_cols = []
        self.fca_cols = []
        self.target_col = 'RUL'
        self.preprocessed_df = None
        self.scaled_data = None
        self.labels = {}
        self.embeddings = {}
        self.anomaly_scores = {}
        self.assoc_rules = None

    def load_data(self):
        logging.info(f"Loading data from {self.input_file}")
        self.df = pd.read_csv(self.input_file)

        # Identifies column types based on naming conventions and data types.
        for col in self.df.columns:
            if col == self.target_col or col == 'RUL_class':
                continue

            if col.endswith('_scaled'):
                self.scaled_cols.append(col)
            elif col.endswith('_fca_bin'):
                self.fca_cols.append(col)
            elif pd.api.types.is_numeric_dtype(self.df[col]):
                if self.df[col].nunique() < 10 and ('num' in col.lower() or 'id' in col.lower()):
                    self.categorical_cols.append(col)
                else:
                    self.numeric_cols.append(col)
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]) or 'date' in col.lower() or 'time' in col.lower():
                pass
            else:
                self.categorical_cols.append(col)

        logging.info(f"Identified {len(self.scaled_cols)} scaled columns and {len(self.fca_cols)} binned columns.")

    def preprocess_data(self):
        logging.info("Preprocessing data for unsupervised learning...")
        df_clean = self.df.copy()

        # Removes rows with missing target values.
        if self.target_col in df_clean.columns:
            df_clean = df_clean.dropna(subset=[self.target_col]).copy()

        num_imputer = SimpleImputer(strategy='median')

        # Imputes missing values for pre-scaled clustering features.
        if self.scaled_cols:
            self.scaled_data = num_imputer.fit_transform(df_clean[self.scaled_cols])
        else:
            logging.warning("No scaled columns found. Unsupervised learning requires scaled matrices.")
            self.scaled_data = np.array([])

        self.preprocessed_df = df_clean
        logging.info("Preprocessing complete.")

    @safe_execution
    def run_clustering(self):
        logging.info("Running clustering algorithms...")

        # Executes k-Means clustering.
        logging.info(" - k-Means")
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.labels['KMeans'] = kmeans.fit_predict(self.scaled_data)

        # Executes hierarchical clustering.
        logging.info(" - Hierarchical")
        hc = AgglomerativeClustering(n_clusters=3)
        self.labels['Hierarchical'] = hc.fit_predict(self.scaled_data)

        # Executes DBSCAN clustering.
        logging.info(" - DBSCAN")
        dbscan = DBSCAN(eps=3.0, min_samples=5)
        self.labels['DBSCAN'] = dbscan.fit_predict(self.scaled_data)

        # Executes Gaussian Mixture Model clustering.
        logging.info(" - GMM")
        gmm = GaussianMixture(n_components=3, random_state=42)
        self.labels['GMM'] = gmm.fit_predict(self.scaled_data)

    @safe_execution
    def run_anomaly_detection(self):
        logging.info("Running anomaly detection algorithms...")

        # Executes Isolation Forest.
        logging.info(" - Isolation Forest")
        iso = IsolationForest(contamination=0.05, random_state=42)
        self.labels['IsolationForest'] = iso.fit_predict(self.scaled_data)
        self.anomaly_scores['IsolationForest'] = iso.decision_function(self.scaled_data)

        # Executes Local Outlier Factor.
        logging.info(" - LOF")
        lof = LocalOutlierFactor(contamination=0.05)
        self.labels['LOF'] = lof.fit_predict(self.scaled_data)
        self.anomaly_scores['LOF'] = lof.negative_outlier_factor_

        # Executes One-Class Support Vector Machine.
        logging.info(" - One-Class SVM")
        ocsvm = OneClassSVM(nu=0.05)
        self.labels['OneClassSVM'] = ocsvm.fit_predict(self.scaled_data)
        self.anomaly_scores['OneClassSVM'] = ocsvm.decision_function(self.scaled_data)

    @safe_execution
    def run_dimensionality_reduction(self):
        logging.info("Running dimensionality reduction algorithms...")

        # Executes Principal Component Analysis.
        logging.info(" - PCA")
        pca = PCA(n_components=2, random_state=42)
        self.embeddings['PCA'] = pca.fit_transform(self.scaled_data)

        # Executes t-Distributed Stochastic Neighbor Embedding.
        logging.info(" - t-SNE")
        tsne = TSNE(n_components=2, random_state=42)
        self.embeddings['tSNE'] = tsne.fit_transform(self.scaled_data)

        # Executes Uniform Manifold Approximation and Projection.
        if UMAP_AVAILABLE:
            logging.info(" - UMAP")
            reducer = umap.UMAP(random_state=42)
            self.embeddings['UMAP'] = reducer.fit_transform(self.scaled_data)
        else:
            logging.info(" - UMAP skipped (not installed).")

    @safe_execution
    def run_association_rules(self):
        logging.info("Running association rules extraction...")
        if not MLXTEND_AVAILABLE:
            logging.warning("mlxtend module is not installed. Association rules extraction is skipped.")
            return

        if not self.fca_cols:
            logging.warning("No FCA bin columns found. Association rules extraction is skipped.")
            return

        # Extracts existing pre-binned categorical columns.
        df_bin = self.preprocessed_df[self.fca_cols].copy()

        # Converts categorical features into dummy indicators.
        df_dummies = pd.get_dummies(df_bin.astype(str))

        logging.info(" - Apriori / FP-Growth")

        # Generates frequent itemsets using the FP-growth algorithm.
        frequent_itemsets = fpgrowth(df_dummies, min_support=0.15, use_colnames=True, max_len=3)
        if len(frequent_itemsets) > 0:
            self.assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5,
                                                 num_itemsets=2)
            self.assoc_rules.to_csv(os.path.join(self.output_dir, 'global_association_rules.csv'), index=False)
        logging.info("Association rules extracted.")

    def _safe_plot(self, plot_func, filepath, *args, **kwargs):
        """Generates and saves a plot safely to the specified filepath."""
        try:
            plt.figure(figsize=(8, 6))
            plot_func(*args, **kwargs)
            plt.tight_layout()
            plt.savefig(filepath)
            plt.close()
        except Exception as e:
            logging.warning(f"Failed to generate plot {filepath}: {e}")
            plt.close()

    def analyze_column(self, col):
        col_dir = os.path.join(self.output_dir, col)
        plots_dir = os.path.join(col_dir, f"{col}_plots")
        os.makedirs(plots_dir, exist_ok=True)

        df_col = self.preprocessed_df.copy()

        # Appends global cluster, score, and embedding assignments to the current dataframe.
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

        is_num = col in self.numeric_cols

        # Generates column profile summary.
        profile = df_col[col].describe().to_frame()
        profile.to_csv(os.path.join(col_dir, f"{col}_profile.csv"))

        # Generates cluster summary.
        cluster_cols = [k for k in self.labels.keys() if self.labels.get(k) is not None]
        if cluster_cols:
            cluster_summary = df_col.groupby(cluster_cols)[col].describe() if is_num else df_col.groupby(cluster_cols)[
                col].value_counts()
            cluster_summary.to_csv(os.path.join(col_dir, f"{col}_cluster_summary.csv"))

        # Generates anomaly summary.
        anomaly_cols = [k for k in ['IsolationForest', 'LOF', 'OneClassSVM'] if k in df_col.columns]
        if anomaly_cols:
            anomaly_summary = df_col.groupby(anomaly_cols)[col].describe() if is_num else df_col.groupby(anomaly_cols)[
                col].value_counts()
            anomaly_summary.to_csv(os.path.join(col_dir, f"{col}_anomaly_summary.csv"))

        # Generates RUL Class summary using pre-existing target columns.
        if 'RUL_class' in df_col.columns:
            rul_summary = df_col.groupby('RUL_class')[col].describe() if is_num else df_col.groupby('RUL_class')[
                col].value_counts()
            rul_summary.to_csv(os.path.join(col_dir, f"{col}_rul_class_summary.csv"))

        # Filters association rules relevant to the current column.
        if self.assoc_rules is not None:
            col_str = str(col)
            mask = self.assoc_rules['antecedents'].apply(lambda x: any(col_str in str(item) for item in x)) | \
                   self.assoc_rules['consequents'].apply(lambda x: any(col_str in str(item) for item in x))
            col_rules = self.assoc_rules[mask]
            col_rules.to_csv(os.path.join(col_dir, f"{col}_association_rules.csv"), index=False)

        # Generates distribution and category plots.
        if is_num:
            self._safe_plot(sns.histplot, os.path.join(plots_dir, 'distribution.png'), data=df_col, x=col, kde=True)
            if 'RUL_class' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'boxplot_rul_class.png'), data=df_col,
                                x='RUL_class', y=col)

            if 'KMeans' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'value_by_kmeans.png'), data=df_col, x='KMeans',
                                y=col)
            if 'GMM' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'value_by_gmm.png'), data=df_col, x='GMM', y=col)
            if 'DBSCAN' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'value_by_dbscan.png'), data=df_col, x='DBSCAN',
                                y=col)
            if 'IsolationForest_score' in df_col.columns:
                self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'anomaly_score_if.png'), data=df_col, x=col,
                                y='IsolationForest_score')

        else:
            self._safe_plot(sns.countplot, os.path.join(plots_dir, 'distribution.png'), data=df_col, x=col)
            if 'KMeans' in df_col.columns:
                self._safe_plot(sns.countplot, os.path.join(plots_dir, 'value_by_kmeans.png'), data=df_col, x='KMeans',
                                hue=col)

        # Generates PCA scatter plots.
        if 'PCA' in self.embeddings:
            hue_arg = col if df_col[col].nunique() < 20 else None
            self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'pca_scatter_col.png'), data=df_col, x='PCA_x',
                            y='PCA_y', hue=hue_arg)
            if 'RUL_class' in df_col.columns:
                self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'pca_scatter_rul.png'), data=df_col, x='PCA_x',
                                y='PCA_y', hue='RUL_class')

        # Generates tSNE scatter plots.
        if 'tSNE' in self.embeddings:
            hue_arg = col if df_col[col].nunique() < 20 else None
            self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'tsne_scatter_col.png'), data=df_col, x='tSNE_x',
                            y='tSNE_y', hue=hue_arg)

        # Generates UMAP scatter plots.
        if 'UMAP' in self.embeddings:
            hue_arg = col if df_col[col].nunique() < 20 else None
            self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'umap_scatter_col.png'), data=df_col, x='UMAP_x',
                            y='UMAP_y', hue=hue_arg)

    def generate_global_outputs(self):
        logging.info("Generating global outputs...")

        # Saves cluster assignments.
        cluster_df = pd.DataFrame(self.labels)
        cluster_df.to_csv(os.path.join(self.output_dir, 'global_cluster_assignments.csv'), index=False)

        # Saves anomaly scores.
        anomaly_df = pd.DataFrame(self.anomaly_scores)
        anomaly_df.to_csv(os.path.join(self.output_dir, 'global_anomaly_scores.csv'), index=False)

        # Saves geometric embeddings.
        embed_dict = {}
        for k, v in self.embeddings.items():
            if v is not None:
                embed_dict[f'{k}_x'] = v[:, 0]
                embed_dict[f'{k}_y'] = v[:, 1]
        pd.DataFrame(embed_dict).to_csv(os.path.join(self.output_dir, 'global_dimensionality_embeddings.csv'),
                                        index=False)

        # Creates global markdown report.
        report_path = os.path.join(self.output_dir, 'global_report.md')
        with open(report_path, 'w') as f:
            f.write("# Global Unsupervised Analysis Report\n\n")
            f.write("## Dataset Overview\n")
            f.write(f"- Number of numerical columns: {len(self.numeric_cols)}\n")
            f.write(f"- Number of categorical columns: {len(self.categorical_cols)}\n")
            f.write(f"- Number of scaled features used: {len(self.scaled_cols)}\n")

            f.write("\n## Clustering Results\n")
            f.write("K-Means, Hierarchical, DBSCAN, and GMM algorithms were applied.\n")

            f.write("\n## Anomaly Detection Results\n")
            f.write("Isolation Forest, LOF, and One-Class SVM applied.\n")

            f.write("\n## Dimensionality Reduction\n")
            f.write(f"PCA, t-SNE applied. UMAP installed: {UMAP_AVAILABLE}\n")

            f.write("\n## Association Rules\n")
            f.write(f"mlxtend installed: {MLXTEND_AVAILABLE}\n")

            f.write("\n## Recommendations\n")
            f.write("Consider extracting top rules for FCA scaling in ToscanaJ based on critical RUL associations.\n")

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)
        self.load_data()
        self.preprocess_data()

        self.run_clustering()
        self.run_anomaly_detection()
        self.run_dimensionality_reduction()
        self.run_association_rules()

        # Selects base columns for individual analysis to avoid duplicating plots for scaled and binned variants.
        cols_to_analyze = self.numeric_cols + self.categorical_cols

        for idx, col in enumerate(cols_to_analyze):
            logging.info(f"Analyzing column {idx + 1}/{len(cols_to_analyze)}: {col}")
            self.analyze_column(col)

        self.generate_global_outputs()
        logging.info("Analysis complete.")


if __name__ == "__main__":
    from pathlib import Path

    # ------------------------------------------------------------
    # Resolve paths relative to this script location
    # ------------------------------------------------------------

    SCRIPT_DIR = Path(__file__).resolve().parent

    INPUT_FILE = SCRIPT_DIR / "Dataset" / "PreProcessedDataset.csv"
    OUTPUT_DIR = SCRIPT_DIR / "Unsupervised_OutputsGEM" / "unsupervised_scaled"

    # ------------------------------------------------------------
    # Run analysis
    # ------------------------------------------------------------

    analyzer = UnsupervisedAnalyzer(
        input_file=str(INPUT_FILE),
        output_dir=str(OUTPUT_DIR)
    )

    analyzer.run()