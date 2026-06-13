import os
import sys
import argparse
import logging
import traceback
from functools import wraps

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
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
    from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
    MLXTEND_AVAILABLE = True
except ImportError:
    MLXTEND_AVAILABLE = False


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def safe_execution(func):
    """Decorator to safely execute algorithms and return None on failure."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.warning(f"Error in {func.__name__}: {e}")
            logging.debug(traceback.format_exc())
            return None
    return wrapper


class UnsupervisedAnalyzer:
    """
    Column-by-column unsupervised analysis for engineered/scaled datasets.

    Model execution is intentionally restricted to engineered properties:
      - *_scaled columns for numeric process variables
      - *_encoded columns for encoded categorical/time properties
      - *_fca_bin columns and RUL_class for association-rule mining

    Raw production columns are excluded from clustering/anomaly/embedding matrices.
    """

    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.df = None
        self.preprocessed_df = None

        self.target_col = "RUL"
        self.target_class_col = "RUL_class"

        self.scaled_cols = []
        self.encoded_cols = []
        self.fca_bin_cols = []

        self.model_feature_cols = []
        self.association_cols = []
        self.analysis_cols = []

        self.scaled_data = None

        self.labels = {}
        self.embeddings = {}
        self.anomaly_scores = {}
        self.assoc_rules = None

    def load_data(self):
        logging.info(f"Loading data from {self.input_file}")
        self.df = pd.read_csv(self.input_file)

        # Engineered numeric features
        self.scaled_cols = [
            col for col in self.df.columns
            if col.endswith("_scaled") and pd.api.types.is_numeric_dtype(self.df[col])
        ]

        # Engineered encoded categorical/time features
        self.encoded_cols = [
            col for col in self.df.columns
            if col.endswith("_encoded") and pd.api.types.is_numeric_dtype(self.df[col])
        ]

        # FCA-ready binned features
        self.fca_bin_cols = [
            col for col in self.df.columns
            if col.endswith("_fca_bin")
        ]

        if self.target_class_col in self.df.columns:
            self.association_cols = self.fca_bin_cols + [self.target_class_col]
        else:
            self.association_cols = self.fca_bin_cols

        # Model features: use transformed properties only.
        # Raw numeric process columns are deliberately excluded.
        self.model_feature_cols = self.scaled_cols + self.encoded_cols

        # Column-level analysis is focused on transformed/scaled/FCA properties.
        self.analysis_cols = (
            self.scaled_cols
            + self.encoded_cols
            + self.fca_bin_cols
        )

        if self.target_class_col in self.df.columns:
            self.analysis_cols.append(self.target_class_col)

        # Keep order but remove duplicates.
        self.analysis_cols = list(dict.fromkeys(self.analysis_cols))

        logging.info(f"Identified {len(self.scaled_cols)} *_scaled numeric columns.")
        logging.info(f"Identified {len(self.encoded_cols)} *_encoded columns.")
        logging.info(f"Identified {len(self.fca_bin_cols)} *_fca_bin columns.")
        logging.info(f"Using {len(self.model_feature_cols)} engineered columns for ML execution.")

        if not self.model_feature_cols:
            raise ValueError(
                "No engineered model columns found. Expected columns ending in '_scaled' "
                "and optionally '_encoded'."
            )

    def preprocess_data(self):
        logging.info("Preprocessing engineered/scaled data for unsupervised learning...")

        df_clean = self.df.copy()

        # Keep only rows with target if RUL exists.
        # This preserves compatibility with downstream RUL_class summaries.
        if self.target_col in df_clean.columns:
            df_clean = df_clean.dropna(subset=[self.target_col]).copy()

        # Coerce model feature columns to numeric.
        for col in self.model_feature_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

        num_imputer = SimpleImputer(strategy="median")
        clustering_data = df_clean[self.model_feature_cols].copy()
        clustering_data[:] = num_imputer.fit_transform(clustering_data)

        # The *_scaled columns are already scaled, but *_encoded columns may not be.
        # Re-standardizing the engineered matrix keeps algorithms numerically stable
        # without using raw source columns.
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(clustering_data)

        self.preprocessed_df = df_clean.reset_index(drop=True)

        logging.info(f"Preprocessing complete. Matrix shape: {self.scaled_data.shape}")

    @safe_execution
    def run_clustering(self):
        logging.info("Running clustering algorithms on engineered/scaled matrix...")

        n_samples = self.scaled_data.shape[0]

        if n_samples < 3:
            logging.warning("Not enough rows for clustering.")
            return

        n_clusters = min(3, n_samples)

        logging.info(" - k-Means")
        kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init=10
        )
        self.labels["KMeans"] = kmeans.fit_predict(self.scaled_data)

        logging.info(" - Hierarchical")
        hc = AgglomerativeClustering(n_clusters=n_clusters)
        self.labels["Hierarchical"] = hc.fit_predict(self.scaled_data)

        logging.info(" - DBSCAN")
        dbscan = DBSCAN(eps=3.0, min_samples=min(5, n_samples))
        self.labels["DBSCAN"] = dbscan.fit_predict(self.scaled_data)

        logging.info(" - GMM")
        gmm = GaussianMixture(
            n_components=n_clusters,
            random_state=42
        )
        self.labels["GMM"] = gmm.fit_predict(self.scaled_data)

    @safe_execution
    def run_anomaly_detection(self):
        logging.info("Running anomaly detection algorithms on engineered/scaled matrix...")

        n_samples = self.scaled_data.shape[0]

        if n_samples < 5:
            logging.warning("Not enough rows for anomaly detection.")
            return

        contamination = min(0.05, max(1.0 / n_samples, 0.01))

        logging.info(" - Isolation Forest")
        iso = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        self.labels["IsolationForest"] = iso.fit_predict(self.scaled_data)
        self.anomaly_scores["IsolationForest"] = iso.decision_function(self.scaled_data)

        logging.info(" - LOF")
        lof_neighbors = min(20, max(2, n_samples - 1))
        lof = LocalOutlierFactor(
            n_neighbors=lof_neighbors,
            contamination=contamination
        )
        self.labels["LOF"] = lof.fit_predict(self.scaled_data)
        self.anomaly_scores["LOF"] = lof.negative_outlier_factor_

        logging.info(" - One-Class SVM")
        ocsvm = OneClassSVM(nu=contamination)
        self.labels["OneClassSVM"] = ocsvm.fit_predict(self.scaled_data)
        self.anomaly_scores["OneClassSVM"] = ocsvm.decision_function(self.scaled_data)

    @safe_execution
    def run_dimensionality_reduction(self):
        logging.info("Running dimensionality reduction on engineered/scaled matrix...")

        n_samples = self.scaled_data.shape[0]
        n_features = self.scaled_data.shape[1]

        if n_samples < 3 or n_features < 1:
            logging.warning("Not enough data for dimensionality reduction.")
            return

        logging.info(" - PCA")
        pca_components = min(2, n_samples, n_features)
        pca = PCA(n_components=pca_components, random_state=42)
        pca_result = pca.fit_transform(self.scaled_data)

        if pca_components == 1:
            pca_result = np.column_stack([pca_result[:, 0], np.zeros(n_samples)])

        self.embeddings["PCA"] = pca_result

        logging.info(" - t-SNE")
        perplexity = min(30, max(2, (n_samples - 1) // 3))

        if n_samples > perplexity:
            tsne = TSNE(
                n_components=2,
                random_state=42,
                perplexity=perplexity,
                init="pca",
                learning_rate="auto"
            )
            self.embeddings["tSNE"] = tsne.fit_transform(self.scaled_data)
        else:
            logging.warning(" - t-SNE skipped because sample count is too small.")

        if UMAP_AVAILABLE:
            logging.info(" - UMAP")
            reducer = umap.UMAP(
                n_components=2,
                random_state=42,
                n_neighbors=min(15, max(2, n_samples - 1))
            )
            self.embeddings["UMAP"] = reducer.fit_transform(self.scaled_data)
        else:
            logging.info(" - UMAP skipped because package is not installed.")

    @safe_execution
    def run_association_rules(self):
        logging.info("Running association rules extraction on *_fca_bin properties...")

        if not MLXTEND_AVAILABLE:
            logging.warning("mlxtend not installed, skipping association rules.")
            return

        if not self.association_cols:
            logging.warning("No *_fca_bin or RUL_class columns found. Skipping association rules.")
            return

        df_bin = self.preprocessed_df[self.association_cols].copy()

        for col in df_bin.columns:
            df_bin[col] = df_bin[col].astype(str).fillna("Missing")

        df_dummies = pd.get_dummies(df_bin, prefix_sep="=")

        if df_dummies.empty:
            logging.warning("Association-rule dummy matrix is empty.")
            return

        logging.info(" - FP-Growth")
        frequent_itemsets = fpgrowth(
            df_dummies,
            min_support=0.15,
            use_colnames=True,
            max_len=3
        )

        if frequent_itemsets.empty:
            logging.info("No frequent itemsets found with min_support=0.15.")
            return

        try:
            rules = association_rules(
                frequent_itemsets,
                metric="confidence",
                min_threshold=0.5
            )
        except TypeError:
            # Compatibility fallback for different mlxtend versions.
            rules = association_rules(
                frequent_itemsets,
                metric="confidence",
                min_threshold=0.5
            )

        if rules.empty:
            logging.info("No association rules generated.")
            return

        self.assoc_rules = rules.sort_values(
            by=["lift", "confidence", "support"],
            ascending=False
        )

        output_path = os.path.join(self.output_dir, "global_association_rules.csv")
        self.assoc_rules.to_csv(output_path, index=False)

        logging.info(f"Association rules extracted: {len(self.assoc_rules)}")

    def _safe_plot(self, plot_func, filepath, *args, **kwargs):
        try:
            plt.figure(figsize=(10, 6))
            plot_func(*args, **kwargs)
            plt.tight_layout()
            plt.savefig(filepath, dpi=150)
            plt.close()
        except Exception as e:
            logging.warning(f"Failed to generate plot {filepath}: {e}")
            plt.close()

    def _build_augmented_df(self):
        df_aug = self.preprocessed_df.copy()

        for name, values in self.labels.items():
            if values is not None and len(values) == len(df_aug):
                df_aug[name] = values

        for name, values in self.anomaly_scores.items():
            if values is not None and len(values) == len(df_aug):
                df_aug[f"{name}_score"] = values

        for name, values in self.embeddings.items():
            if values is not None and len(values) == len(df_aug):
                df_aug[f"{name}_x"] = values[:, 0]
                df_aug[f"{name}_y"] = values[:, 1]

        return df_aug

    def analyze_column(self, col):
        safe_col_name = (
            str(col)
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            .replace("*", "_")
            .replace("?", "_")
            .replace('"', "_")
            .replace("<", "_")
            .replace(">", "_")
            .replace("|", "_")
        )

        col_dir = os.path.join(self.output_dir, safe_col_name)
        plots_dir = os.path.join(col_dir, f"{safe_col_name}_plots")
        os.makedirs(plots_dir, exist_ok=True)

        df_col = self._build_augmented_df()

        if col not in df_col.columns:
            logging.warning(f"Column not found in preprocessed dataframe: {col}")
            return

        is_num = pd.api.types.is_numeric_dtype(df_col[col])

        # Profile
        try:
            if is_num:
                profile = df_col[col].describe().to_frame()
            else:
                profile = df_col[col].astype(str).describe().to_frame()

            profile.to_csv(os.path.join(col_dir, f"{safe_col_name}_profile.csv"))
        except Exception as e:
            logging.warning(f"Failed profile for {col}: {e}")

        # Cluster summary
        cluster_cols = [
            name for name in ["KMeans", "Hierarchical", "DBSCAN", "GMM"]
            if name in df_col.columns
        ]

        if cluster_cols:
            try:
                for cluster_col in cluster_cols:
                    if is_num:
                        summary = df_col.groupby(cluster_col)[col].describe()
                    else:
                        summary = df_col.groupby(cluster_col)[col].value_counts(dropna=False)

                    summary.to_csv(
                        os.path.join(
                            col_dir,
                            f"{safe_col_name}_cluster_summary_by_{cluster_col}.csv"
                        )
                    )
            except Exception as e:
                logging.warning(f"Failed cluster summary for {col}: {e}")

        # Anomaly summary
        anomaly_label_cols = [
            name for name in ["IsolationForest", "LOF", "OneClassSVM"]
            if name in df_col.columns
        ]

        if anomaly_label_cols:
            try:
                for anomaly_col in anomaly_label_cols:
                    if is_num:
                        summary = df_col.groupby(anomaly_col)[col].describe()
                    else:
                        summary = df_col.groupby(anomaly_col)[col].value_counts(dropna=False)

                    summary.to_csv(
                        os.path.join(
                            col_dir,
                            f"{safe_col_name}_anomaly_summary_by_{anomaly_col}.csv"
                        )
                    )
            except Exception as e:
                logging.warning(f"Failed anomaly summary for {col}: {e}")

        # RUL class summary
        if self.target_class_col in df_col.columns and col != self.target_class_col:
            try:
                if is_num:
                    rul_summary = df_col.groupby(self.target_class_col)[col].describe()
                else:
                    rul_summary = df_col.groupby(self.target_class_col)[col].value_counts(dropna=False)

                rul_summary.to_csv(
                    os.path.join(col_dir, f"{safe_col_name}_rul_class_summary.csv")
                )
            except Exception as e:
                logging.warning(f"Failed RUL_class summary for {col}: {e}")

        # Association rules for this column
        if self.assoc_rules is not None:
            try:
                col_str = str(col).replace("_fca_bin", "")

                mask = (
                    self.assoc_rules["antecedents"].apply(
                        lambda items: any(col_str in str(item) for item in items)
                    )
                    |
                    self.assoc_rules["consequents"].apply(
                        lambda items: any(col_str in str(item) for item in items)
                    )
                )

                col_rules = self.assoc_rules[mask]

                if not col_rules.empty:
                    col_rules.to_csv(
                        os.path.join(col_dir, f"{safe_col_name}_association_rules.csv"),
                        index=False
                    )
            except Exception as e:
                logging.warning(f"Failed association-rule filtering for {col}: {e}")

        # Plots
        if is_num:
            self._safe_plot(
                sns.histplot,
                os.path.join(plots_dir, "distribution.png"),
                data=df_col,
                x=col,
                kde=True
            )

            if self.target_class_col in df_col.columns and col != self.target_class_col:
                self._safe_plot(
                    sns.boxplot,
                    os.path.join(plots_dir, "boxplot_rul_class.png"),
                    data=df_col,
                    x=self.target_class_col,
                    y=col
                )

            for cluster_col in ["KMeans", "Hierarchical", "DBSCAN", "GMM"]:
                if cluster_col in df_col.columns:
                    self._safe_plot(
                        sns.boxplot,
                        os.path.join(plots_dir, f"value_by_{cluster_col}.png"),
                        data=df_col,
                        x=cluster_col,
                        y=col
                    )

            for score_col in [
                "IsolationForest_score",
                "LOF_score",
                "OneClassSVM_score"
            ]:
                if score_col in df_col.columns:
                    self._safe_plot(
                        sns.scatterplot,
                        os.path.join(plots_dir, f"{score_col}_scatter.png"),
                        data=df_col,
                        x=col,
                        y=score_col
                    )
        else:
            self._safe_plot(
                sns.countplot,
                os.path.join(plots_dir, "distribution.png"),
                data=df_col,
                x=col,
                order=df_col[col].astype(str).value_counts().index[:30]
            )

            for cluster_col in ["KMeans", "Hierarchical", "DBSCAN", "GMM"]:
                if cluster_col in df_col.columns:
                    self._safe_plot(
                        sns.countplot,
                        os.path.join(plots_dir, f"value_by_{cluster_col}.png"),
                        data=df_col,
                        x=cluster_col,
                        hue=col
                    )

        # Embedding scatterplots
        for embedding_name in ["PCA", "tSNE", "UMAP"]:
            x_col = f"{embedding_name}_x"
            y_col = f"{embedding_name}_y"

            if x_col in df_col.columns and y_col in df_col.columns:
                hue_arg = None

                try:
                    if df_col[col].nunique(dropna=False) <= 20:
                        hue_arg = col
                except Exception:
                    hue_arg = None

                self._safe_plot(
                    sns.scatterplot,
                    os.path.join(plots_dir, f"{embedding_name.lower()}_scatter_col.png"),
                    data=df_col,
                    x=x_col,
                    y=y_col,
                    hue=hue_arg
                )

                if self.target_class_col in df_col.columns:
                    self._safe_plot(
                        sns.scatterplot,
                        os.path.join(plots_dir, f"{embedding_name.lower()}_scatter_rul_class.png"),
                        data=df_col,
                        x=x_col,
                        y=y_col,
                        hue=self.target_class_col
                    )

    def generate_global_outputs(self):
        logging.info("Generating global outputs...")

        # Save feature manifest
        manifest = pd.DataFrame({
            "feature": (
                self.scaled_cols
                + self.encoded_cols
                + self.fca_bin_cols
                + ([self.target_class_col] if self.target_class_col in self.preprocessed_df.columns else [])
            ),
            "feature_group": (
                ["scaled"] * len(self.scaled_cols)
                + ["encoded"] * len(self.encoded_cols)
                + ["fca_bin"] * len(self.fca_bin_cols)
                + (
                    ["target_class"]
                    if self.target_class_col in self.preprocessed_df.columns
                    else []
                )
            )
        })

        manifest.to_csv(
            os.path.join(self.output_dir, "global_engineered_feature_manifest.csv"),
            index=False
        )

        # Save cluster assignments
        if self.labels:
            cluster_df = pd.DataFrame(self.labels)
            cluster_df.to_csv(
                os.path.join(self.output_dir, "global_cluster_assignments.csv"),
                index=False
            )

        # Save anomaly scores
        if self.anomaly_scores:
            anomaly_df = pd.DataFrame(self.anomaly_scores)
            anomaly_df.to_csv(
                os.path.join(self.output_dir, "global_anomaly_scores.csv"),
                index=False
            )

        # Save embeddings
        embed_dict = {}

        for name, values in self.embeddings.items():
            if values is not None:
                embed_dict[f"{name}_x"] = values[:, 0]
                embed_dict[f"{name}_y"] = values[:, 1]

        if embed_dict:
            pd.DataFrame(embed_dict).to_csv(
                os.path.join(self.output_dir, "global_dimensionality_embeddings.csv"),
                index=False
            )

        # Save augmented output
        augmented_df = self._build_augmented_df()
        augmented_df.to_csv(
            os.path.join(self.output_dir, "global_augmented_engineered_dataset.csv"),
            index=False
        )

        # Create global report
        report_path = os.path.join(self.output_dir, "global_report.md")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Global Unsupervised Analysis Report\n\n")

            f.write("## Execution Scope\n")
            f.write("This analysis was executed on engineered/scaled dataset properties only.\n\n")
            f.write("Raw process measurements were not used directly in the ML matrix.\n\n")

            f.write("## Feature Groups\n")
            f.write(f"- `*_scaled` numeric features: {len(self.scaled_cols)}\n")
            f.write(f"- `*_encoded` features: {len(self.encoded_cols)}\n")
            f.write(f"- `*_fca_bin` association-rule features: {len(self.fca_bin_cols)}\n")
            f.write(f"- Model matrix columns: {len(self.model_feature_cols)}\n")
            f.write(f"- Association-rule columns: {len(self.association_cols)}\n\n")

            f.write("## Clustering Results\n")
            f.write("K-Means, Hierarchical Clustering, DBSCAN, and Gaussian Mixture Models were applied where feasible.\n\n")

            f.write("## Anomaly Detection Results\n")
            f.write("Isolation Forest, Local Outlier Factor, and One-Class SVM were applied where feasible.\n\n")

            f.write("## Dimensionality Reduction\n")
            f.write(f"PCA and t-SNE were attempted. UMAP installed: {UMAP_AVAILABLE}\n\n")

            f.write("## Association Rules\n")
            f.write(f"mlxtend installed: {MLXTEND_AVAILABLE}\n")
            f.write("Association rules were generated from `*_fca_bin` columns and `RUL_class` where available.\n\n")

            f.write("## Output Files\n")
            f.write("- `global_engineered_feature_manifest.csv`\n")
            f.write("- `global_cluster_assignments.csv`\n")
            f.write("- `global_anomaly_scores.csv`\n")
            f.write("- `global_dimensionality_embeddings.csv`\n")
            f.write("- `global_augmented_engineered_dataset.csv`\n")
            f.write("- `global_association_rules.csv`, if rules were generated\n\n")

            f.write("## Recommendation\n")
            f.write(
                "Use the generated `*_association_rules.csv` files to identify FCA-relevant "
                "rules associated with `RUL_class`, especially `Critical` and `Low` classes.\n"
            )

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)

        self.load_data()
        self.preprocess_data()

        self.run_clustering()
        self.run_anomaly_detection()
        self.run_dimensionality_reduction()
        self.run_association_rules()

        if not self.analysis_cols:
            logging.warning("No engineered columns available for column-by-column analysis.")
        else:
            for idx, col in enumerate(self.analysis_cols):
                logging.info(f"Analyzing engineered column {idx + 1}/{len(self.analysis_cols)}: {col}")
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
    OUTPUT_DIR = SCRIPT_DIR / "outputsGPT" / "unsupervised_scaled"

    # ------------------------------------------------------------
    # Run analysis
    # ------------------------------------------------------------

    analyzer = UnsupervisedAnalyzer(
        input_file=str(INPUT_FILE),
        output_dir=str(OUTPUT_DIR)
    )

    analyzer.run()