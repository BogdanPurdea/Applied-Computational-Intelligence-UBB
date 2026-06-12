import os
import sys
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
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

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
        self.numeric_cols = []
        self.categorical_cols = []
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
        
        # Identify columns
        for col in self.df.columns:
            if col == self.target_col:
                continue
            if pd.api.types.is_numeric_dtype(self.df[col]):
                if self.df[col].nunique() < 10 and 'num' in col.lower() or 'id' in col.lower():
                    self.categorical_cols.append(col)
                else:
                    self.numeric_cols.append(col)
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]) or 'date' in col.lower() or 'time' in col.lower():
                # Ignore raw dates for clustering
                pass
            else:
                self.categorical_cols.append(col)
                
        logging.info(f"Identified {len(self.numeric_cols)} numeric and {len(self.categorical_cols)} categorical columns.")

    def preprocess_data(self):
        logging.info("Preprocessing data for unsupervised learning...")
        df_clean = self.df.copy()
        
        # Handle target
        if self.target_col in df_clean.columns:
            df_clean = df_clean.dropna(subset=[self.target_col]).copy()
            
        num_imputer = SimpleImputer(strategy='median')
        cat_imputer = SimpleImputer(strategy='most_frequent')
        scaler = StandardScaler()
        
        # Fill NA
        if self.numeric_cols:
            df_clean[self.numeric_cols] = num_imputer.fit_transform(df_clean[self.numeric_cols])
        if self.categorical_cols:
            df_clean[self.categorical_cols] = cat_imputer.fit_transform(df_clean[self.categorical_cols])
            
        # For clustering we need fully numeric matrix
        clustering_data = df_clean[self.numeric_cols].copy()
        
        # Label encode categoricals for simplicity in clustering
        for col in self.categorical_cols:
            le = LabelEncoder()
            clustering_data[col] = le.fit_transform(df_clean[col].astype(str))
            
        self.scaled_data = scaler.fit_transform(clustering_data)
        self.preprocessed_df = df_clean
        logging.info("Preprocessing complete.")

    @safe_execution
    def run_clustering(self):
        logging.info("Running clustering algorithms...")
        
        # KMeans
        logging.info(" - k-Means")
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.labels['KMeans'] = kmeans.fit_predict(self.scaled_data)
        
        # Hierarchical
        logging.info(" - Hierarchical")
        hc = AgglomerativeClustering(n_clusters=3)
        self.labels['Hierarchical'] = hc.fit_predict(self.scaled_data)
        
        # DBSCAN
        logging.info(" - DBSCAN")
        dbscan = DBSCAN(eps=3.0, min_samples=5)
        self.labels['DBSCAN'] = dbscan.fit_predict(self.scaled_data)
        
        # GMM
        logging.info(" - GMM")
        gmm = GaussianMixture(n_components=3, random_state=42)
        self.labels['GMM'] = gmm.fit_predict(self.scaled_data)

    @safe_execution
    def run_anomaly_detection(self):
        logging.info("Running anomaly detection algorithms...")
        
        # Isolation Forest
        logging.info(" - Isolation Forest")
        iso = IsolationForest(contamination=0.05, random_state=42)
        self.labels['IsolationForest'] = iso.fit_predict(self.scaled_data)
        self.anomaly_scores['IsolationForest'] = iso.decision_function(self.scaled_data)
        
        # Local Outlier Factor
        logging.info(" - LOF")
        lof = LocalOutlierFactor(contamination=0.05)
        self.labels['LOF'] = lof.fit_predict(self.scaled_data)
        self.anomaly_scores['LOF'] = lof.negative_outlier_factor_
        
        # One-Class SVM
        logging.info(" - One-Class SVM")
        ocsvm = OneClassSVM(nu=0.05)
        self.labels['OneClassSVM'] = ocsvm.fit_predict(self.scaled_data)
        self.anomaly_scores['OneClassSVM'] = ocsvm.decision_function(self.scaled_data)

    @safe_execution
    def run_dimensionality_reduction(self):
        logging.info("Running dimensionality reduction algorithms...")
        
        # PCA
        logging.info(" - PCA")
        pca = PCA(n_components=2, random_state=42)
        self.embeddings['PCA'] = pca.fit_transform(self.scaled_data)
        
        # t-SNE
        logging.info(" - t-SNE")
        tsne = TSNE(n_components=2, random_state=42)
        self.embeddings['tSNE'] = tsne.fit_transform(self.scaled_data)
        
        # UMAP
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
            logging.warning("mlxtend not installed, skipping association rules.")
            return

        # Prepare dummy DataFrame for FCA/Association rules
        df_bin = pd.DataFrame()
        for col in self.numeric_cols:
            if self.preprocessed_df[col].nunique() > 3:
                try:
                    df_bin[col] = pd.qcut(self.preprocessed_df[col], q=3, labels=['Low', 'Medium', 'High'], duplicates='drop')
                except ValueError:
                    pass
            else:
                df_bin[col] = self.preprocessed_df[col].astype(str)
        
        for col in self.categorical_cols:
            df_bin[col] = self.preprocessed_df[col].astype(str)
            
        if self.target_col in self.preprocessed_df.columns:
            try:
                df_bin[self.target_col] = pd.qcut(self.preprocessed_df[self.target_col], q=3, labels=['Critical', 'Low', 'Healthy'], duplicates='drop')
            except ValueError:
                df_bin[self.target_col] = self.preprocessed_df[self.target_col].astype(str)

        df_dummies = pd.get_dummies(df_bin)
        
        logging.info(" - Apriori / FP-Growth")
        # Run FP-growth for speed if possible, else fallback to apriori
        frequent_itemsets = fpgrowth(df_dummies, min_support=0.15, use_colnames=True, max_len=3)
        if len(frequent_itemsets) > 0:
            self.assoc_rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5, num_itemsets=2)
            # Filter to relevant rules if needed
            self.assoc_rules.to_csv(os.path.join(self.output_dir, 'global_association_rules.csv'), index=False)
        logging.info("Association rules extracted.")

    def _safe_plot(self, plot_func, filepath, *args, **kwargs):
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
        
        # Global assignments to col DF
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
        
        # Profile
        profile = df_col[col].describe().to_frame()
        profile.to_csv(os.path.join(col_dir, f"{col}_profile.csv"))
        
        # Cluster Summary
        cluster_cols = [k for k in self.labels.keys() if self.labels.get(k) is not None]
        if cluster_cols:
            cluster_summary = df_col.groupby(cluster_cols)[col].describe() if is_num else df_col.groupby(cluster_cols)[col].value_counts()
            cluster_summary.to_csv(os.path.join(col_dir, f"{col}_cluster_summary.csv"))
            
        # Anomaly Summary
        anomaly_cols = [k for k in ['IsolationForest', 'LOF', 'OneClassSVM'] if k in df_col.columns]
        if anomaly_cols:
            anomaly_summary = df_col.groupby(anomaly_cols)[col].describe() if is_num else df_col.groupby(anomaly_cols)[col].value_counts()
            anomaly_summary.to_csv(os.path.join(col_dir, f"{col}_anomaly_summary.csv"))

        # RUL Class Summary
        if self.target_col in df_col.columns:
            # Create a categorical RUL
            try:
                df_col['RUL_class'] = pd.qcut(df_col[self.target_col], q=3, labels=['Critical', 'Low', 'Healthy'], duplicates='drop')
            except ValueError:
                df_col['RUL_class'] = df_col[self.target_col]
                
            rul_summary = df_col.groupby('RUL_class')[col].describe() if is_num else df_col.groupby('RUL_class')[col].value_counts()
            rul_summary.to_csv(os.path.join(col_dir, f"{col}_rul_class_summary.csv"))

        # Association Rules for this column
        if self.assoc_rules is not None:
            # find rules where col is in antecedents or consequents
            col_str = str(col)
            mask = self.assoc_rules['antecedents'].apply(lambda x: any(col_str in str(item) for item in x)) | \
                   self.assoc_rules['consequents'].apply(lambda x: any(col_str in str(item) for item in x))
            col_rules = self.assoc_rules[mask]
            col_rules.to_csv(os.path.join(col_dir, f"{col}_association_rules.csv"), index=False)

        # Plots
        if is_num:
            self._safe_plot(sns.histplot, os.path.join(plots_dir, 'distribution.png'), data=df_col, x=col, kde=True)
            if 'RUL_class' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'boxplot_rul_class.png'), data=df_col, x='RUL_class', y=col)
                
            if 'KMeans' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'value_by_kmeans.png'), data=df_col, x='KMeans', y=col)
            if 'GMM' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'value_by_gmm.png'), data=df_col, x='GMM', y=col)
            if 'DBSCAN' in df_col.columns:
                self._safe_plot(sns.boxplot, os.path.join(plots_dir, 'value_by_dbscan.png'), data=df_col, x='DBSCAN', y=col)
            if 'IsolationForest_score' in df_col.columns:
                self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'anomaly_score_if.png'), data=df_col, x=col, y='IsolationForest_score')
                
        else:
            self._safe_plot(sns.countplot, os.path.join(plots_dir, 'distribution.png'), data=df_col, x=col)
            # Add categorical equivalent plots (e.g. countplots split by hue)
            if 'KMeans' in df_col.columns:
                self._safe_plot(sns.countplot, os.path.join(plots_dir, 'value_by_kmeans.png'), data=df_col, x='KMeans', hue=col)
            
        # PCA Scatter
        if 'PCA' in self.embeddings:
            # Colored by col
            hue_arg = col if df_col[col].nunique() < 20 else None
            self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'pca_scatter_col.png'), data=df_col, x='PCA_x', y='PCA_y', hue=hue_arg)
            if 'RUL_class' in df_col.columns:
                self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'pca_scatter_rul.png'), data=df_col, x='PCA_x', y='PCA_y', hue='RUL_class')
                
        # tSNE Scatter
        if 'tSNE' in self.embeddings:
            hue_arg = col if df_col[col].nunique() < 20 else None
            self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'tsne_scatter_col.png'), data=df_col, x='tSNE_x', y='tSNE_y', hue=hue_arg)
            
        # UMAP Scatter
        if 'UMAP' in self.embeddings:
            hue_arg = col if df_col[col].nunique() < 20 else None
            self._safe_plot(sns.scatterplot, os.path.join(plots_dir, 'umap_scatter_col.png'), data=df_col, x='UMAP_x', y='UMAP_y', hue=hue_arg)

    def generate_global_outputs(self):
        logging.info("Generating global outputs...")
        
        # Save cluster assignments
        cluster_df = pd.DataFrame(self.labels)
        cluster_df.to_csv(os.path.join(self.output_dir, 'global_cluster_assignments.csv'), index=False)
        
        # Save anomaly scores
        anomaly_df = pd.DataFrame(self.anomaly_scores)
        anomaly_df.to_csv(os.path.join(self.output_dir, 'global_anomaly_scores.csv'), index=False)
        
        # Save embeddings
        embed_dict = {}
        for k, v in self.embeddings.items():
            if v is not None:
                embed_dict[f'{k}_x'] = v[:, 0]
                embed_dict[f'{k}_y'] = v[:, 1]
        pd.DataFrame(embed_dict).to_csv(os.path.join(self.output_dir, 'global_dimensionality_embeddings.csv'), index=False)
        
        # Create global report
        report_path = os.path.join(self.output_dir, 'global_report.md')
        with open(report_path, 'w') as f:
            f.write("# Global Unsupervised Analysis Report\n\n")
            f.write("## Dataset Overview\n")
            f.write(f"- Number of numerical columns: {len(self.numeric_cols)}\n")
            f.write(f"- Number of categorical columns: {len(self.categorical_cols)}\n")
            
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
        
        cols_to_analyze = [c for c in self.preprocessed_df.columns if c != self.target_col]
        
        for idx, col in enumerate(cols_to_analyze):
            logging.info(f"Analyzing column {idx+1}/{len(cols_to_analyze)}: {col}")
            self.analyze_column(col)
            
        self.generate_global_outputs()
        logging.info("Analysis complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Column-by-column Unsupervised Learning Analysis")
    parser.add_argument('--input', type=str, required=True, help="Input CSV file")
    parser.add_argument('--output', type=str, required=True, help="Output directory for results")
    args = parser.parse_args()

    analyzer = UnsupervisedAnalyzer(args.input, args.output)
    analyzer.run()
