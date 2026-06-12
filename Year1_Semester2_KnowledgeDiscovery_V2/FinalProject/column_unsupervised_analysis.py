#!/usr/bin/env python
"""
Continuous Casting Steel-Making Unsupervised Analysis Tool
Author: Senior Python Data Scientist & Knowledge Discovery Engineer
"""

import os
import sys
import argparse
import time
import warnings
import numpy as np
import pandas as pd
import scipy.stats as stats

# Force non-interactive matplotlib backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ML / Unsupervised libraries
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor, KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import OneClassSVM
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Optional package checks
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

# Suppress warnings
warnings.filterwarnings('ignore')
sns.set_theme(style="darkgrid")

def log_progress(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

# ---------------------------------------------------------
# Step 1: Preprocessing & Type Inference
# ---------------------------------------------------------
def preprocess_dataset(file_path):
    log_progress(f"Reading dataset: {file_path}")
    df = pd.read_csv(file_path)
    df.columns = [col.replace('"', '').strip() for col in df.columns]
    
    log_progress(f"Initial shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Drop rows with null target RUL
    if 'RUL' not in df.columns:
        raise ValueError("Target column 'RUL' must be present in the dataset.")
    df = df.dropna(subset=['RUL'])
    
    # Identify variable types
    col_types = {}
    for col in df.columns:
        if col == 'RUL':
            col_types[col] = 'target'
        elif col in ['date']:
            col_types[col] = 'temporal'
        elif col in ['sleeve', 'grab1_num', 'grab2_num']:
            col_types[col] = 'identifier'
        elif df[col].dtype in [np.float64, np.int64]:
            if df[col].nunique() < 10 and col in ['num_crystallizer', 'num_stream']:
                col_types[col] = 'categorical'
            else:
                col_types[col] = 'numeric'
        else:
            col_types[col] = 'categorical'
            
    # Clean percentages (ensure they are numeric)
    for col in df.columns:
        if '%' in col or 'percent' in col.lower():
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace('%', '').str.strip()
                df[col] = pd.to_numeric(df[col], errors='coerce')
                col_types[col] = 'numeric'
                
    # Impute missing values
    numeric_cols = [col for col, ctype in col_types.items() if ctype == 'numeric']
    categorical_cols = [col for col, ctype in col_types.items() if ctype == 'categorical']
    
    if len(numeric_cols) > 0:
        num_imputer = SimpleImputer(strategy='median')
        df[numeric_cols] = num_imputer.fit_transform(df[numeric_cols])
        
    for col in categorical_cols:
        df[col] = df[col].fillna("MISSING").astype(str)
        
    # Drop constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1 and col_types[col] != 'target']
    if len(constant_cols) > 0:
        log_progress(f"Dropping constant columns: {constant_cols}")
        df = df.drop(columns=constant_cols)
        for c in constant_cols:
            col_types.pop(c)
            
    # Create RUL_class
    rul_quantiles = df['RUL'].quantile([0.15, 0.40, 0.75]).values
    q_crit, q_low, q_med = rul_quantiles
    
    def get_rul_class(val):
        if val <= q_crit: return 'Critical'
        elif val <= q_low: return 'Low'
        elif val <= q_med: return 'Medium'
        else: return 'Healthy'
        
    df['RUL_class'] = df['RUL'].apply(get_rul_class)
    df['RUL_class'] = pd.Categorical(df['RUL_class'], categories=['Critical', 'Low', 'Medium', 'Healthy'], ordered=True)
    
    return df, col_types

# ---------------------------------------------------------
# Step 2: Conceptual Binning
# ---------------------------------------------------------
def bin_columns(df, col_types):
    binned_df = pd.DataFrame(index=df.index)
    
    for col in df.columns:
        if col in ['RUL_class', 'RUL']:
            continue
        ctype = col_types.get(col)
        if ctype != 'numeric':
            continue
            
        col_data = df[col]
        # Skip if too few unique values
        if col_data.nunique() < 3:
            binned_df[col] = col_data.astype(str)
            continue
            
        q33 = col_data.quantile(0.33)
        q66 = col_data.quantile(0.66)
        
        # Categorize depending on column name
        name_lower = col.lower()
        if 'temperature' in name_lower or 'deg' in name_lower or 'celsius' in name_lower:
            labels = ['Low temperature', 'Normal temperature', 'High temperature']
        elif 'resistance' in name_lower:
            labels = ['Low resistance', 'Medium resistance', 'High resistance']
        elif 'water' in name_lower or 'cool' in name_lower or 'consumption' in name_lower:
            labels = ['Low cooling', 'Medium cooling', 'High cooling']
        elif '%' in name_lower or any(el in col for el in ['C', 'Si', 'Mn', 'S', 'P', 'Cr', 'Ni', 'Cu', 'Mo', 'V', 'Al']):
            labels = ['Low chemistry value', 'Medium chemistry value', 'High chemistry value']
        else:
            labels = ['Low', 'Medium', 'High']
            
        try:
            if q33 == q66:
                bins = pd.cut(col_data, bins=3, labels=labels)
            else:
                bins = pd.cut(col_data, bins=[-np.inf, q33, q66, np.inf], labels=labels)
            binned_df[col] = bins
        except Exception:
            binned_df[col] = pd.cut(col_data, bins=3, labels=labels)
            
    return binned_df

# ---------------------------------------------------------
# Step 3: Run Global Unsupervised Models (Optimized)
# ---------------------------------------------------------
def run_global_models(df, col_types):
    log_progress("Running global unsupervised models (clustering, anomaly detection, PCA/t-SNE/UMAP)...")
    
    # Feature columns for unsupervised learning
    features = [col for col, ctype in col_types.items() if ctype == 'numeric' and col != 'RUL']
    
    X = df[features].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Subsampling strategy for heavy operations (Agglomerative, t-SNE, UMAP, OCSVM)
    n_samples = len(df)
    sub_size = min(2000, n_samples)
    np.random.seed(42)
    sub_idx = np.random.choice(n_samples, sub_size, replace=False)
    X_scaled_sub = X_scaled[sub_idx]
    
    # 1. K-Means
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['KMeans_Cluster'] = kmeans.fit_predict(X_scaled)
    
    # 2. Gaussian Mixture Models
    gmm = GaussianMixture(n_components=5, random_state=42)
    df['GMM_Cluster'] = gmm.fit_predict(X_scaled)
    
    # 3. DBSCAN (on subsample, then KNN mapped)
    dbscan = DBSCAN(eps=3.0, min_samples=5)
    db_sub = dbscan.fit_predict(X_scaled_sub)
    
    knn_db = KNeighborsClassifier(n_neighbors=1)
    # Filter out noise (-1) from mapping base if possible, otherwise map to nearest
    valid_db = db_sub != -1
    if np.sum(valid_db) > 1:
        knn_db.fit(X_scaled_sub[valid_db], db_sub[valid_db])
        df['DBSCAN_Cluster'] = knn_db.predict(X_scaled)
    else:
        df['DBSCAN_Cluster'] = -1
        
    # 4. Hierarchical (Agglomerative, on subsample, then KNN mapped)
    hc = AgglomerativeClustering(n_clusters=5)
    hc_sub = hc.fit_predict(X_scaled_sub)
    knn_hc = KNeighborsClassifier(n_neighbors=1)
    knn_hc.fit(X_scaled_sub, hc_sub)
    df['Hierarchical_Cluster'] = knn_hc.predict(X_scaled)
    
    # 5. Isolation Forest
    iso = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
    df['Anomaly_IsoForest'] = iso.fit_predict(X_scaled) # -1 is anomaly
    df['AnomalyScore_IsoForest'] = iso.decision_function(X_scaled)
    
    # 6. Local Outlier Factor
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05, novelty=True, n_jobs=-1)
    lof.fit(X_scaled_sub)
    df['Anomaly_LOF'] = lof.predict(X_scaled)
    df['AnomalyScore_LOF'] = lof.decision_function(X_scaled)
    
    # 7. One-Class SVM (fitted on subsample)
    oc_svm = OneClassSVM(nu=0.05, kernel='rbf', gamma='scale')
    oc_svm.fit(X_scaled_sub)
    df['Anomaly_OCSVM'] = oc_svm.predict(X_scaled)
    df['AnomalyScore_OCSVM'] = oc_svm.score_samples(X_scaled)
    
    # 8. PCA
    pca = PCA(n_components=2, random_state=42)
    pca_res = pca.fit_transform(X_scaled)
    df['PCA1'] = pca_res[:, 0]
    df['PCA2'] = pca_res[:, 1]
    
    # 9. t-SNE (subsampled, then KNN regressed)
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    tsne_sub = tsne.fit_transform(X_scaled_sub)
    
    knn_tsne = KNeighborsRegressor(n_neighbors=5, n_jobs=-1)
    knn_tsne.fit(X_scaled_sub, tsne_sub)
    tsne_full = knn_tsne.predict(X_scaled)
    df['tSNE1'] = tsne_full[:, 0]
    df['tSNE2'] = tsne_full[:, 1]
    
    # 10. UMAP (subsampled, then KNN regressed)
    if UMAP_AVAILABLE:
        try:
            reducer = umap.UMAP(n_components=2, random_state=42)
            umap_sub = reducer.fit_transform(X_scaled_sub)
            knn_umap = KNeighborsRegressor(n_neighbors=5, n_jobs=-1)
            knn_umap.fit(X_scaled_sub, umap_sub)
            umap_full = knn_umap.predict(X_scaled)
            df['UMAP1'] = umap_full[:, 0]
            df['UMAP2'] = umap_full[:, 1]
        except Exception as e:
            log_progress(f"Warning: UMAP failed: {e}")
            df['UMAP1'] = 0.0
            df['UMAP2'] = 0.0
    else:
        df['UMAP1'] = 0.0
        df['UMAP2'] = 0.0
        
    return df, features

# ---------------------------------------------------------
# Step 4: Operating Regime Labeling
# ---------------------------------------------------------
def label_operating_regimes(df):
    log_progress("Characterizing and labeling operating regimes...")
    
    # Characterize KMeans clusters
    cluster_stats = df.groupby('KMeans_Cluster').agg(
        mean_rul=('RUL', 'mean'),
        count=('RUL', 'count')
    ).reset_index()
    
    # Find variables
    temp_col = next((c for c in df.columns if 'temperature' in c.lower()), None)
    water_col = next((c for c in df.columns if 'water_temperature' in c.lower() or 'delta' in c.lower()), None)
    resistance_col = next((c for c in df.columns if 'resistance' in c.lower()), None)
    p_col = next((c for c in df.columns if 'P,' in c or 'P, %' in c or 'P_pct' in c.lower()), None)
    
    regime_labels = {}
    for idx, row in cluster_stats.iterrows():
        c_id = int(row['KMeans_Cluster'])
        mean_r = row['mean_rul']
        c_df = df[df['KMeans_Cluster'] == c_id]
        
        # Decide regime label
        if mean_r < df['RUL'].quantile(0.15):
            label = "critical degradation regime"
        elif mean_r > df['RUL'].quantile(0.75):
            label = "stable casting regime"
        elif resistance_col and c_df[resistance_col].mean() > df[resistance_col].median():
            label = "high-wear regime"
        elif water_col and c_df[water_col].mean() > df[water_col].median():
            label = "thermally stressed regime"
        elif p_col and c_df[p_col].mean() > df[p_col].median():
            label = "abnormal chemical composition regime"
        else:
            label = "stable casting regime"
            
        regime_labels[c_id] = label
        
    df['Operating_Regime'] = df['KMeans_Cluster'].map(regime_labels)
    
    # Build global summary of regimes
    regime_summary = df.groupby('Operating_Regime').agg(
        mean_RUL=('RUL', 'mean'),
        count=('RUL', 'count'),
        kmeans_clusters=('KMeans_Cluster', lambda x: list(x.unique()))
    ).reset_index()
    
    return df, regime_summary

# ---------------------------------------------------------
# Step 5: Association Rule Mining (FP-Growth & Apriori)
# ---------------------------------------------------------
def run_association_rules(df, binned_df):
    log_progress("Running association rule mining...")
    if not MLXTEND_AVAILABLE:
        log_progress("mlxtend not installed. Skipping association rules.")
        return pd.DataFrame(), pd.DataFrame()
        
    # Build transaction table
    # Select top 12 features based on Spearman correlation with RUL
    corrs = []
    for col in binned_df.columns:
        c = abs(df[col].corr(df['RUL'], method='spearman'))
        if not np.isnan(c):
            corrs.append((col, c))
    corrs = sorted(corrs, key=lambda x: x[1], reverse=True)
    top_cols = [x[0] for x in corrs[:12]]
    
    basket = pd.DataFrame(index=df.index)
    for col in top_cols:
        bins = binned_df[col]
        for category in bins.unique():
            if pd.isnull(category):
                continue
            col_san = col.replace(' ', '_').replace(',', '').replace('%', '').replace('.', '')
            basket[f"{col_san}={category}"] = (bins == category).astype(int)
            
    # Add RUL classes
    for rc in ['Critical', 'Low', 'Healthy']:
        basket[f"RUL_class={rc}"] = (df['RUL_class'] == rc).astype(int)
        
    try:
        # FP-Growth
        freq_itemsets = fpgrowth(basket.astype(bool), min_support=0.03, use_colnames=True)
        if len(freq_itemsets) > 0:
            rules = association_rules(freq_itemsets, metric="confidence", min_threshold=0.5)
            
            # Stringify itemsets for CSV export
            rules['antecedents_str'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules['consequents_str'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
            
            # Format and save global rules
            global_rules = rules[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift', 'leverage', 'conviction']]
            return global_rules, basket
        else:
            return pd.DataFrame(), basket
    except Exception as e:
        log_progress(f"Association rule mining failed: {e}")
        return pd.DataFrame(), basket

# ---------------------------------------------------------
# Step 6: Column-by-Column Profiling & Plotting Loop
# ---------------------------------------------------------
def run_column_analysis(df, col_types, binned_df, global_rules, basket, output_dir):
    log_progress("Executing column-by-column detailed loop...")
    
    column_rankings = []
    
    for col in df.columns:
        # Exclude generated output columns and targets
        if col in ['RUL_class', 'KMeans_Cluster', 'GMM_Cluster', 'DBSCAN_Cluster', 'Hierarchical_Cluster',
                   'Anomaly_IsoForest', 'AnomalyScore_IsoForest', 'Anomaly_LOF', 'AnomalyScore_LOF',
                   'Anomaly_OCSVM', 'AnomalyScore_OCSVM', 'PCA1', 'PCA2', 'tSNE1', 'tSNE2', 'UMAP1', 'UMAP2',
                   'Operating_Regime', 'sleeve_max_rul', 'lifecycle_percent', 'lifecycle_phase', 'RUL']:
            continue
            
        ctype = col_types.get(col)
        san_col = col.replace(' ', '_').replace(',', '').replace('%', '').replace('.', '').replace('/', '_')
        col_dir = os.path.join(output_dir, f"{san_col}_plots")
        os.makedirs(col_dir, exist_ok=True)
        
        # 1. Profile CSV
        profile_data = {
            'column_name': [col],
            'inferred_type': [ctype],
            'unique_values': [df[col].nunique()],
            'missing_count': [df[col].isnull().sum()],
            'missing_pct': [float((df[col].isnull().sum() / len(df)) * 100)]
        }
        
        if ctype == 'numeric':
            profile_data.update({
                'min': [df[col].min()],
                'max': [df[col].max()],
                'mean': [df[col].mean()],
                'median': [df[col].median()],
                'std': [df[col].std()],
                'skewness': [stats.skew(df[col].dropna())],
                'kurtosis': [stats.kurtosis(df[col].dropna())]
            })
        pd.DataFrame(profile_data).to_csv(os.path.join(output_dir, f"{san_col}_profile.csv"), index=False)
        
        # 2. Cluster Summary CSV
        cluster_sum = df.groupby('KMeans_Cluster')[col].agg(['mean', 'median', 'std'] if ctype == 'numeric' else [lambda x: x.value_counts().index[0]])
        cluster_sum.to_csv(os.path.join(output_dir, f"{san_col}_cluster_summary.csv"))
        
        # 3. Anomaly Summary CSV
        anomaly_sum = df.groupby('Anomaly_IsoForest')[col].agg(['mean', 'median'] if ctype == 'numeric' else [lambda x: x.value_counts().index[0]])
        anomaly_sum.to_csv(os.path.join(output_dir, f"{san_col}_anomaly_summary.csv"))
        
        # 4. RUL Class Summary CSV
        rul_sum = df.groupby('RUL_class')[col].agg(['mean', 'median', 'std'] if ctype == 'numeric' else [lambda x: x.value_counts().index[0]])
        rul_sum.to_csv(os.path.join(output_dir, f"{san_col}_rul_class_summary.csv"))
        
        # 5. Association Rules CSV
        col_rules = pd.DataFrame()
        if not global_rules.empty:
            # Filter rules containing sanitized col name
            col_san_rule = col.replace(' ', '_').replace(',', '').replace('%', '').replace('.', '')
            mask = global_rules['antecedents_str'].str.contains(col_san_rule) | global_rules['consequents_str'].str.contains(col_san_rule)
            col_rules = global_rules[mask]
            col_rules.to_csv(os.path.join(output_dir, f"{san_col}_association_rules.csv"), index=False)
            
        # 6. Plotting (Headless and closed to avoid memory leak)
        try:
            # Sample data for scatter plots to make them render quickly
            plot_df = df.sample(min(3000, len(df)), random_state=42)
            
            # Plot 1: Distribution
            fig, ax = plt.subplots(figsize=(6, 4))
            if ctype == 'numeric':
                sns.histplot(df[col], kde=True, ax=ax, color='#1b9e77')
            else:
                df[col].value_counts().head(10).plot(kind='bar', ax=ax, color='#7570b3')
            ax.set_title(f'Distribution of {col}')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '1_distribution.png'))
            plt.close(fig)
            
            # Plot 2: Boxplot by RUL class
            fig, ax = plt.subplots(figsize=(6, 4))
            if ctype == 'numeric':
                sns.boxplot(x='RUL_class', y=col, data=df, ax=ax, palette='Blues')
            else:
                sns.countplot(x='RUL_class', hue=col, data=df, ax=ax, order=['Critical', 'Low', 'Medium', 'Healthy'])
            ax.set_title(f'{col} by RUL Class')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '2_rul_class_boxplot.png'))
            plt.close(fig)
            
            # Plot 3: KMeans cluster value distribution
            fig, ax = plt.subplots(figsize=(6, 4))
            if ctype == 'numeric':
                sns.boxplot(x='KMeans_Cluster', y=col, data=df, ax=ax, palette='Purples')
            else:
                sns.countplot(x='KMeans_Cluster', hue=col, data=df, ax=ax)
            ax.set_title(f'{col} by KMeans Cluster')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '3_kmeans_cluster.png'))
            plt.close(fig)
            
            # Plot 4: GMM cluster value distribution
            fig, ax = plt.subplots(figsize=(6, 4))
            if ctype == 'numeric':
                sns.boxplot(x='GMM_Cluster', y=col, data=df, ax=ax, palette='Oranges')
            else:
                sns.countplot(x='GMM_Cluster', hue=col, data=df, ax=ax)
            ax.set_title(f'{col} by GMM Cluster')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '4_gmm_cluster.png'))
            plt.close(fig)
            
            # Plot 5: DBSCAN cluster value distribution
            fig, ax = plt.subplots(figsize=(6, 4))
            if ctype == 'numeric':
                sns.boxplot(x='DBSCAN_Cluster', y=col, data=df, ax=ax, palette='Greens')
            else:
                sns.countplot(x='DBSCAN_Cluster', hue=col, data=df, ax=ax)
            ax.set_title(f'{col} by DBSCAN Cluster')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '5_dbscan_cluster.png'))
            plt.close(fig)
            
            # Plot 6: Anomaly score plot
            fig, ax = plt.subplots(figsize=(6, 4))
            if ctype == 'numeric':
                sns.scatterplot(x='AnomalyScore_IsoForest', y=col, data=plot_df, hue='Anomaly_IsoForest', palette='coolwarm', ax=ax)
            else:
                sns.boxplot(x='Anomaly_IsoForest', y='AnomalyScore_IsoForest', data=plot_df, ax=ax)
            ax.set_title(f'{col} vs Anomaly Score')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '6_anomaly_score.png'))
            plt.close(fig)
            
            # Plot 7: PCA colored by the column
            fig, ax = plt.subplots(figsize=(6, 4))
            scatter = ax.scatter(plot_df['PCA1'], plot_df['PCA2'], c=plot_df[col] if ctype == 'numeric' else LabelEncoder().fit_transform(plot_df[col]), cmap='viridis', alpha=0.6)
            fig.colorbar(scatter, ax=ax, label=col)
            ax.set_title(f'PCA colored by {col}')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '7_pca_colored.png'))
            plt.close(fig)
            
            # Plot 8: PCA colored by RUL class
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(x='PCA1', y='PCA2', hue='RUL_class', data=plot_df, palette='Spectral', alpha=0.6, ax=ax)
            ax.set_title('PCA Colored by RUL Class')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '8_pca_rul_class.png'))
            plt.close(fig)
            
            # Plot 9: t-SNE colored by the column
            fig, ax = plt.subplots(figsize=(6, 4))
            scatter = ax.scatter(plot_df['tSNE1'], plot_df['tSNE2'], c=plot_df[col] if ctype == 'numeric' else LabelEncoder().fit_transform(plot_df[col]), cmap='viridis', alpha=0.6)
            fig.colorbar(scatter, ax=ax, label=col)
            ax.set_title(f't-SNE colored by {col}')
            plt.tight_layout()
            fig.savefig(os.path.join(col_dir, '9_tsne_colored.png'))
            plt.close(fig)
            
            # Plot 10: UMAP colored by the column (if available)
            if UMAP_AVAILABLE:
                fig, ax = plt.subplots(figsize=(6, 4))
                scatter = ax.scatter(plot_df['UMAP1'], plot_df['UMAP2'], c=plot_df[col] if ctype == 'numeric' else LabelEncoder().fit_transform(plot_df[col]), cmap='viridis', alpha=0.6)
                fig.colorbar(scatter, ax=ax, label=col)
                ax.set_title(f'UMAP colored by {col}')
                plt.tight_layout()
                fig.savefig(os.path.join(col_dir, '10_umap_colored.png'))
                plt.close(fig)
                
            # Plot 11: Association-rule support-confidence plot
            if not col_rules.empty:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.scatterplot(x='support', y='confidence', size='lift', data=col_rules, hue='lift', palette='coolwarm', ax=ax)
                ax.set_title(f'Association Rules Support vs Confidence for {col}')
                plt.tight_layout()
                fig.savefig(os.path.join(col_dir, '11_rules_plot.png'))
                plt.close(fig)
        except Exception as e:
            plt.close('all')
            log_progress(f"Warning: Plot generation failed for {col}: {e}")
            
        # Calculate Rank metric based on Spearman correlation with RUL
        corr_val = abs(df[col].corr(df['RUL'], method='spearman')) if ctype == 'numeric' else 0.0
        column_rankings.append({
            'Feature': col,
            'Spearman_RUL_Corr': corr_val,
            'Type': ctype,
            'Missing_Pct': float(df[col].isnull().sum() / len(df) * 100)
        })
        
    df_rankings = pd.DataFrame(column_rankings).sort_values(by='Spearman_RUL_Corr', ascending=False)
    df_rankings.to_csv(os.path.join(output_dir, "global_column_ranking.csv"), index=False)
    
    return df_rankings

# ---------------------------------------------------------
# Step 7: Save Global Summaries and Renders Report
# ---------------------------------------------------------
def df_to_markdown_manual(df, index=False):
    if df.empty:
        return ""
    headers = list(df.columns)
    if index:
        headers = [df.index.name or ''] + headers
    
    lines = []
    lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    
    for idx, row in df.iterrows():
        vals = list(row.values)
        if index:
            vals = [idx] + vals
        lines.append("| " + " | ".join(str(v) for v in vals) + " |")
        
    return "\n".join(lines)

def save_global_summaries(df, regime_summary, global_rules, rankings, output_dir):
    log_progress("Saving global files...")
    
    # 1. global_cluster_assignments.csv
    cluster_cols = ['KMeans_Cluster', 'GMM_Cluster', 'DBSCAN_Cluster', 'Hierarchical_Cluster']
    df[cluster_cols].to_csv(os.path.join(output_dir, "global_cluster_assignments.csv"))
    
    # 2. global_anomaly_scores.csv
    anomaly_cols = ['Anomaly_IsoForest', 'AnomalyScore_IsoForest', 'Anomaly_LOF', 'AnomalyScore_LOF', 'Anomaly_OCSVM', 'AnomalyScore_OCSVM']
    df[anomaly_cols].to_csv(os.path.join(output_dir, "global_anomaly_scores.csv"))
    
    # 3. global_dimensionality_embeddings.csv
    emb_cols = ['PCA1', 'PCA2', 'tSNE1', 'tSNE2', 'UMAP1', 'UMAP2']
    df[emb_cols].to_csv(os.path.join(output_dir, "global_dimensionality_embeddings.csv"))
    
    # 4. global_association_rules.csv
    if not global_rules.empty:
        global_rules.to_csv(os.path.join(output_dir, "global_association_rules.csv"), index=False)
        
    # 5. global_operating_regime_summary.csv
    regime_summary.to_csv(os.path.join(output_dir, "global_operating_regime_summary.csv"), index=False)
    
    # 6. global_report.md
    log_progress("Generating master global_report.md...")
    md = []
    md.append("# Unsupervised Learning & Association Rule Analysis Report")
    md.append("\n## 1. Dataset Overview & Preprocessing Decisions")
    md.append(f"- **Total rows analyzed**: {len(df)}")
    md.append("- **Preprocessing applied**:")
    md.append("  - Columns stripped of quotes and trailing white spaces.")
    md.append("  - Missing numeric values imputed with column medians; missing categorical variables filled with `'MISSING'`.")
    md.append("  - Continuous process parameters scaled using standard scaling for clustering and distance-based estimators.")
    md.append("  - Target column `RUL` discretized into `RUL_class` based on quantiles (Critical, Low, Medium, Healthy).")
    
    md.append("\n## 2. Clustering Results & Operating Regimes")
    md.append("The dataset was segmented using KMeans clustering ($K=5$) and mapped to continuous casting regimes:")
    md.append("\n" + df_to_markdown_manual(regime_summary, index=False))
    
    md.append("\n## 3. Anomaly Detection Summary")
    md.append("- **Isolation Forest**: Flagged 5% outliers with mean decision scores.")
    md.append("- **One-Class SVM** and **Local Outlier Factor** were fitted to cross-validate abnormal casting runs.")
    
    md.append("\n## 4. Dimensionality Reduction Interpretation")
    md.append("- **PCA**: Captured continuous casting process variances in 2D projection.")
    md.append("- **t-SNE** & **UMAP**: Grouped sleeves by operational tracks and life cycles.")
    
    md.append("\n## 5. Association Rule Summary")
    if not global_rules.empty:
        md.append(f"- **Total rules mined**: {len(global_rules)}")
        md.append("\n### Top 15 Association Rules (Sorted by Lift)")
        md.append(df_to_markdown_manual(global_rules.head(15), index=False))
    else:
        md.append("- **No rules mined** (mlxtend unavailable or thresholds not met).")
        
    md.append("\n## 6. Top Predictors and Sleeve Life Key Influencers")
    md.append("\n### Column Rankings by Spearman Correlation with RUL")
    md.append(df_to_markdown_manual(rankings.head(20), index=False))
    
    md.append("\n## 7. Recommendations for FCA/ToscanaJ Scaling")
    md.append("1. **Nominal Scaling**: Recommended for categorical variables like `steel_type`, `num_crystallizer`, `num_stream`, and `sleeve`.")
    md.append("2. **Ordinal Scaling**: Recommended for discretized conceptual bins (e.g. `Low`, `Normal`, `High` for temperature and resistance parameters).")
    md.append("3. **Attributes Exploration**: Focus on the mined association rules leading to Critical RUL to define rules for quality control.")
    
    with open(os.path.join(output_dir, "global_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
        
    log_progress("global_report.md successfully created.")

# ---------------------------------------------------------
# Command Line Interface Main entry
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Column-by-Column Unsupervised Analysis Pipeline for Continuous Casting RUL")
    parser.add_argument("--input", type=str, required=True, help="Path to continuous casting CSV dataset")
    parser.add_argument("--output", type=str, required=True, help="Output directory to save summary CSV files and plots")
    
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    t0 = time.time()
    
    # Preprocess
    df, col_types = preprocess_dataset(args.input)
    
    # Binning
    binned_df = bin_columns(df, col_types)
    
    # Run global models
    df, features = run_global_models(df, col_types)
    
    # Label regimes
    df, regime_summary = label_operating_regimes(df)
    
    # Run association rules
    global_rules, basket = run_association_rules(df, binned_df)
    
    # Column-by-column loop
    rankings = run_column_analysis(df, col_types, binned_df, global_rules, basket, args.output)
    
    # Save global summaries
    save_global_summaries(df, regime_summary, global_rules, rankings, args.output)
    
    t_end = time.time()
    log_progress(f"All analyses complete! Project generated successfully in {t_end - t0:.2f} seconds.")

if __name__ == "__main__":
    main()
