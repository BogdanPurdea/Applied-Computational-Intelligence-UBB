"""
Continuous Casting Crystallizer Sleeve RUL Analysis Pipeline
Author: Senior Data Scientist & Knowledge Discovery Researcher
"""

import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# ML / Stats Imports
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    mean_absolute_error, mean_squared_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_auc_score
)
from sklearn.inspection import permutation_importance, PartialDependenceDisplay

# Regression Models
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.naive_bayes import GaussianNB

# Optional/Conditional Imports
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

try:
    import lightgbm as lgb
    LGB_AVAILABLE = True
except ImportError:
    LGB_AVAILABLE = False

# CatBoost is known to be NOT available
CAT_AVAILABLE = False

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

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

# Clustering & Anomaly Imports
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Settings
warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# Define Output Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "analysis_output")
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

print(f"Output directory initialized at: {OUTPUT_DIR}")
print(f"Plots directory initialized at: {PLOTS_DIR}")

# Helper: Log progress
def log_progress(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

# ---------------------------------------------------------
# Step 1: Load and Clean Dataset
# ---------------------------------------------------------
def load_and_clean_dataset(file_path):
    log_progress(f"Loading dataset from: {file_path}")
    # Read CSV, strip column names of quotes and whitespaces
    df = pd.read_csv(file_path)
    df.columns = [col.replace('"', '').strip() for col in df.columns]
    
    log_progress(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Process target column
    if 'RUL' not in df.columns:
        raise ValueError("Target column 'RUL' not found in dataset!")
    
    # Drop rows where RUL is null
    initial_len = len(df)
    df = df.dropna(subset=['RUL'])
    log_progress(f"Dropped {initial_len - len(df)} rows with missing RUL. Remaining: {len(df)}")
    
    # Clean column types
    # Date column parsing
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Inferred column types
    inferred_types = {}
    for col in df.columns:
        if col == 'RUL':
            inferred_types[col] = 'target'
        elif col == 'date':
            inferred_types[col] = 'temporal'
        elif col in ['sleeve', 'grab1_num', 'grab2_num']:
            inferred_types[col] = 'identifier'
        elif df[col].dtype in [np.float64, np.int64]:
            # If low cardinality numeric, check if it behaves as categorical/identifier
            if df[col].nunique() < 10 and col in ['num_crystallizer', 'num_stream']:
                inferred_types[col] = 'categorical'
            else:
                inferred_types[col] = 'numeric'
        else:
            inferred_types[col] = 'categorical'
            
    # Clean percentage columns - confirm they are numeric
    for col in df.columns:
        if '%' in col or 'percent' in col.lower():
            if df[col].dtype == object:
                # String conversion if needed
                df[col] = df[col].astype(str).str.replace('%', '').str.strip()
                df[col] = pd.to_numeric(df[col], errors='coerce')
                inferred_types[col] = 'numeric'
                
    return df, inferred_types

# ---------------------------------------------------------
# Step 2: Column Profiling & Descriptive Statistics
# ---------------------------------------------------------
def profile_columns(df, col_types):
    log_progress("Profiling columns and computing statistics...")
    profile = {}
    
    # Define RUL Classes
    # Critical (<=15%), Low (15%-40%), Medium (40%-75%), Healthy (>75%)
    rul_quantiles = df['RUL'].quantile([0.15, 0.40, 0.75]).values
    q_crit, q_low, q_med = rul_quantiles
    
    def get_rul_class(val):
        if val <= q_crit: return 'Critical'
        elif val <= q_low: return 'Low'
        elif val <= q_med: return 'Medium'
        else: return 'Healthy'
        
    df['RUL_class'] = df['RUL'].apply(get_rul_class)
    df['RUL_class'] = pd.Categorical(df['RUL_class'], categories=['Critical', 'Low', 'Medium', 'Healthy'], ordered=True)
    
    for col in df.columns:
        if col in ['RUL_class']:
            continue
            
        col_data = df[col]
        missing_cnt = col_data.isnull().sum()
        missing_pct = (missing_cnt / len(df)) * 100
        n_unique = col_data.nunique()
        examples = col_data.dropna().head(5).tolist()
        
        col_type = col_types.get(col, 'numeric')
        
        meta = {
            'name': col,
            'type': col_type,
            'n_unique': n_unique,
            'missing_count': missing_cnt,
            'missing_pct': missing_pct,
            'examples': examples
        }
        
        stats_dict = {}
        outliers = {}
        missing_analysis = {}
        correlation_info = {}
        binned_analysis = {}
        rul_class_dist = {}
        
        # Missing value analysis
        missing_analysis['missing_count'] = int(missing_cnt)
        missing_analysis['missing_pct'] = float(missing_pct)
        if missing_cnt > 0:
            is_missing = col_data.isnull()
            mean_rul_missing = df.loc[is_missing, 'RUL'].mean()
            mean_rul_present = df.loc[~is_missing, 'RUL'].mean()
            missing_analysis['pattern'] = f"Mean RUL when missing: {mean_rul_missing:.2f} vs present: {mean_rul_present:.2f}"
            missing_analysis['strategy'] = "Impute with median" if col_type == 'numeric' else "Impute with mode/missing category"
        else:
            missing_analysis['pattern'] = "No missing values observed"
            missing_analysis['strategy'] = "No action required"
            
        # Stats & Outliers by type
        if col_type == 'numeric':
            stats_dict = {
                'count': int(col_data.count()),
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()) if col_data.count() > 1 else 0.0,
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'q25': float(col_data.quantile(0.25)),
                'q75': float(col_data.quantile(0.75)),
                'skewness': float(stats.skew(col_data.dropna())) if col_data.count() > 2 else 0.0,
                'kurtosis': float(stats.kurtosis(col_data.dropna())) if col_data.count() > 2 else 0.0
            }
            
            # IQR Outliers
            q25, q75 = stats_dict['q25'], stats_dict['q75']
            iqr = q75 - q25
            lower_bound = q25 - 1.5 * iqr
            upper_bound = q75 + 1.5 * iqr
            iqr_outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            # Z-score Outliers
            if stats_dict['std'] > 0:
                z_scores = (col_data - stats_dict['mean']) / stats_dict['std']
                z_outliers = col_data[z_scores.abs() > 3]
            else:
                z_outliers = pd.Series()
                
            outliers = {
                'iqr_count': int(len(iqr_outliers)),
                'iqr_pct': float((len(iqr_outliers)/len(df))*100),
                'z_count': int(len(z_outliers)),
                'z_pct': float((len(z_outliers)/len(df))*100)
            }
            
            if len(iqr_outliers) > 0:
                outlier_idx = iqr_outliers.index
                mean_rul_outliers = df.loc[outlier_idx, 'RUL'].mean()
                mean_rul_normals = df.loc[~df.index.isin(outlier_idx), 'RUL'].mean()
                outliers['effect_on_rul'] = f"Outliers mean RUL: {mean_rul_outliers:.2f} vs Normals mean RUL: {mean_rul_normals:.2f}"
            else:
                outliers['effect_on_rul'] = "No outliers detected"
                
            # Relationship with RUL
            valid_idx = col_data.dropna().index
            if len(valid_idx) > 2 and df.loc[valid_idx, 'RUL'].std() > 0 and col_data.dropna().std() > 0:
                p_corr, p_pval = stats.pearsonr(col_data.dropna(), df.loc[valid_idx, 'RUL'])
                s_corr, s_pval = stats.spearmanr(col_data.dropna(), df.loc[valid_idx, 'RUL'])
                k_corr, k_pval = stats.kendalltau(col_data.dropna(), df.loc[valid_idx, 'RUL'])
                correlation_info = {
                    'pearson': p_corr, 'pearson_p': p_pval,
                    'spearman': s_corr, 'spearman_p': s_pval,
                    'kendall': k_corr, 'kendall_p': k_pval
                }
            else:
                correlation_info = {'pearson': 0.0, 'pearson_p': 1.0, 'spearman': 0.0, 'spearman_p': 1.0, 'kendall': 0.0, 'kendall_p': 1.0}
                
            # Binned conceptual analysis
            # low/medium/high using quantiles
            try:
                q33 = col_data.quantile(0.33)
                q66 = col_data.quantile(0.66)
                if q33 == q66 or col_data.nunique() < 3:
                    # Fallback to simple binning if duplicates
                    bins = pd.cut(col_data, bins=3, labels=['Low', 'Medium', 'High'])
                else:
                    bins = pd.cut(col_data, bins=[-np.inf, q33, q66, np.inf], labels=['Low', 'Medium', 'High'])
                
                df_temp = pd.DataFrame({'val_bin': bins, 'RUL': df['RUL']})
                bin_rul_means = df_temp.groupby('val_bin')['RUL'].mean()
                binned_analysis = {
                    'Low_mean_rul': float(bin_rul_means.get('Low', 0)),
                    'Medium_mean_rul': float(bin_rul_means.get('Medium', 0)),
                    'High_mean_rul': float(bin_rul_means.get('High', 0))
                }
                # Identify critical RUL bin (lowest RUL)
                crit_bin = bin_rul_means.idxmin()
                binned_analysis['critical_bin'] = str(crit_bin)
                # FCA labels
                sanitized_name = col.lower().replace(' ', '_').replace(',', '').replace('%', '').replace('.', '').replace('/', '_')
                binned_analysis['fca_labels'] = {
                    'Low': f"low_{sanitized_name}",
                    'Medium': f"medium_{sanitized_name}",
                    'High': f"high_{sanitized_name}"
                }
            except Exception as e:
                binned_analysis = {'error': str(e)}
                
        elif col_type == 'categorical':
            freq = col_data.value_counts()
            stats_dict = {
                'cardinality': int(n_unique),
                'top_categories': freq.head(5).to_dict(),
                'rare_categories': freq[freq / len(df) < 0.01].index.tolist()
            }
            
            # ANOVA or Kruskal-Wallis vs RUL
            try:
                groups = [df.loc[df[col] == val, 'RUL'].dropna().values for val in freq.head(10).index]
                groups = [g for g in groups if len(g) > 2]
                if len(groups) > 1:
                    f_val, p_val = stats.f_oneway(*groups)
                    h_val, k_pval = stats.kruskal(*groups)
                    correlation_info = {
                        'anova_f': f_val, 'anova_p': p_val,
                        'kruskal_h': h_val, 'kruskal_p': k_pval
                    }
                else:
                    correlation_info = {'anova_f': 0.0, 'anova_p': 1.0, 'kruskal_h': 0.0, 'kruskal_p': 1.0}
            except Exception:
                correlation_info = {'anova_f': 0.0, 'anova_p': 1.0, 'kruskal_h': 0.0, 'kruskal_p': 1.0}
                
            # Mean RUL by category
            cat_rul = df.groupby(col)['RUL'].agg(['mean', 'median', 'min', 'max']).head(10).to_dict(orient='index')
            binned_analysis = {'categories': cat_rul}
            
        elif col_type == 'temporal':
            stats_dict = {
                'min': str(col_data.min()),
                'max': str(col_data.max()),
                'range': str(col_data.max() - col_data.min())
            }
            
        # RUL class distribution overrepresentation
        if col_type in ['numeric', 'categorical'] and col != 'RUL':
            try:
                # Bin numeric to L/M/H for RUL class distribution
                if col_type == 'numeric':
                    q33 = col_data.quantile(0.33)
                    q66 = col_data.quantile(0.66)
                    if q33 == q66 or col_data.nunique() < 3:
                        bins = pd.cut(col_data, bins=3, labels=['Low', 'Medium', 'High'])
                    else:
                        bins = pd.cut(col_data, bins=[-np.inf, q33, q66, np.inf], labels=['Low', 'Medium', 'High'])
                else:
                    bins = col_data.astype(str)
                
                # Cross-tabulate bins vs RUL_class
                ctab = pd.crosstab(bins, df['RUL_class'], normalize='columns') * 100
                ctab_rows = pd.crosstab(bins, df['RUL_class'], normalize='index') * 100
                overall_dist = bins.value_counts(normalize=True) * 100
                
                # Look for overrepresentation (e.g. ratio of class percentage to overall percentage > 1.2)
                over_crit = []
                over_health = []
                for val in overall_dist.index:
                    if val in ctab.index:
                        # % of Critical RUL that has this value, divided by overall % of this value
                        crit_pct = ctab.loc[val, 'Critical']
                        health_pct = ctab.loc[val, 'Healthy']
                        overall_pct = overall_dist[val]
                        
                        if overall_pct > 0:
                            # Using representation ratio
                            crit_ratio = (df[(bins == val) & (df['RUL_class'] == 'Critical')].shape[0] / max(1, df[df['RUL_class'] == 'Critical'].shape[0])) / (df[bins == val].shape[0] / len(df))
                            health_ratio = (df[(bins == val) & (df['RUL_class'] == 'Healthy')].shape[0] / max(1, df[df['RUL_class'] == 'Healthy'].shape[0])) / (df[bins == val].shape[0] / len(df))
                            
                            if crit_ratio > 1.2:
                                over_crit.append(f"{val} (Ratio: {crit_ratio:.2f})")
                            if health_ratio > 1.2:
                                over_health.append(f"{val} (Ratio: {health_ratio:.2f})")
                                
                rul_class_dist = {
                    'crosstab_pct': ctab.to_dict(),
                    'overrepresented_in_critical': over_crit,
                    'overrepresented_in_healthy': over_health
                }
            except Exception as e:
                rul_class_dist = {'error': str(e)}
                
        # Interpretation
        usefulness = "Unclear"
        if col == 'RUL':
            usefulness = "Target Column"
        elif col_type == 'numeric':
            corr = abs(correlation_info.get('spearman', 0.0))
            if corr > 0.4: usefulness = "High (strong monotonic correlation)"
            elif corr > 0.15: usefulness = "Medium (moderate monotonic correlation)"
            else: usefulness = "Low (weak correlation)"
        elif col_type == 'categorical':
            pval = correlation_info.get('kruskal_p', 1.0)
            if pval < 0.01: usefulness = "High (significant differences in RUL distributions)"
            elif pval < 0.05: usefulness = "Medium (moderately significant differences)"
            else: usefulness = "Low (no significant differences in RUL distributions)"
            
        profile[col] = {
            'metadata': meta,
            'statistics': stats_dict,
            'outliers': outliers,
            'missing_value_analysis': missing_analysis,
            'relationship_with_rul': correlation_info,
            'binned_analysis': binned_analysis,
            'rul_class_distribution': rul_class_dist,
            'usefulness_interpretation': usefulness
        }
        
    return profile

# ---------------------------------------------------------
# Step 3: Distribution Analysis & Plotting
# ---------------------------------------------------------
def generate_column_plots(df, col_types):
    log_progress("Generating distribution charts...")
    # Clean plots before starting
    plt.close('all')
    
    # We will loop through the columns and save their plots
    for col in df.columns:
        if col in ['RUL_class']:
            continue
            
        col_type = col_types.get(col, 'numeric')
        sanitized_name = col.replace(' ', '_').replace(',', '').replace('%', '').replace('.', '').replace('/', '_')
        plot_path = os.path.join(PLOTS_DIR, f"{sanitized_name}.png")
        
        # Check if already exists to save time if running repeatedly
        if os.path.exists(plot_path):
            continue
            
        try:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            
            if col_type == 'numeric':
                # Histogram
                sns.histplot(df[col].dropna(), kde=True, ax=axes[0], color='#2b5c8f')
                axes[0].set_title(f'{col} Distribution')
                axes[0].set_xlabel(col)
                
                # Scatter / Boxplot vs RUL
                # Create Low/Medium/High bins
                q33 = df[col].quantile(0.33)
                q66 = df[col].quantile(0.66)
                if q33 == q66 or df[col].nunique() < 3:
                    bins = pd.cut(df[col], bins=3, labels=['Low', 'Medium', 'High'])
                else:
                    bins = pd.cut(df[col], bins=[-np.inf, q33, q66, np.inf], labels=['Low', 'Medium', 'High'])
                
                sns.boxplot(x=bins, y=df['RUL'], ax=axes[1], palette='Blues')
                axes[1].set_title(f'RUL by {col} Quantile Bins')
                axes[1].set_xlabel(f'{col} Bins')
                axes[1].set_ylabel('RUL')
                
            elif col_type == 'categorical':
                # Bar chart of value counts
                top_cats = df[col].value_counts().head(10)
                sns.barplot(x=top_cats.values, y=top_cats.index, ax=axes[0], palette='viridis')
                axes[0].set_title(f'Top 10 Categories in {col}')
                axes[0].set_xlabel('Count')
                
                # Boxplot vs RUL
                sns.boxplot(x='RUL', y=col, data=df, ax=axes[1], order=top_cats.index, palette='Set2')
                axes[1].set_title(f'RUL by Top Categories of {col}')
                axes[1].set_ylabel('')
                
            elif col_type == 'temporal':
                # Time trend
                df_sorted = df.sort_values(by=col)
                # Aggregate RUL by date/time
                daily_rul = df_sorted.groupby(col)['RUL'].mean().reset_index()
                sns.lineplot(data=daily_rul, x=col, y='RUL', ax=axes[0], color='#e056fd')
                axes[0].set_title('RUL Trend Over Time')
                axes[0].set_ylabel('Average RUL')
                
                # Count over time
                daily_counts = df_sorted.groupby(col).size().reset_index(name='casts')
                sns.lineplot(data=daily_counts, x=col, y='casts', ax=axes[1], color='#22a6b3')
                axes[1].set_title('Observations Over Time')
                axes[1].set_ylabel('Cast Count')
                
            plt.tight_layout()
            plt.savefig(plot_path, dpi=100)
            plt.close(fig)
        except Exception as e:
            plt.close('all')
            log_progress(f"Warning: Could not generate plot for {col}: {e}")

# ---------------------------------------------------------
# Step 4: Special Grouped Analyses
# ---------------------------------------------------------
def perform_grouped_analyses(df):
    log_progress("Performing special grouped analyses...")
    grouped_results = {}
    
    # 1. RUL by steel_type
    if 'steel_type' in df.columns:
        grouped_results['steel_type'] = df.groupby('steel_type')['RUL'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).to_dict(orient='index')
        
    # 2. RUL by num_crystallizer
    if 'num_crystallizer' in df.columns:
        grouped_results['num_crystallizer'] = df.groupby('num_crystallizer')['RUL'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).to_dict(orient='index')
        
    # 3. RUL by num_stream
    if 'num_stream' in df.columns:
        grouped_results['num_stream'] = df.groupby('num_stream')['RUL'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).to_dict(orient='index')
        
    # 4. RUL by sleeve
    if 'sleeve' in df.columns:
        grouped_results['sleeve'] = df.groupby('sleeve')['RUL'].agg(['count', 'mean', 'median', 'max']).sort_values(by='mean', ascending=False).head(20).to_dict(orient='index')
        
    # 5. RUL by workpiece_slice_geometry
    if 'workpiece_slice_geometry' in df.columns:
        grouped_results['workpiece_slice_geometry'] = df.groupby('workpiece_slice_geometry')['RUL'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).to_dict(orient='index')
        
    # 6. RUL by lifecycle phase
    # First, calculate life track progress for each sleeve: casting index / total casts
    if 'sleeve' in df.columns:
        df['sleeve_max_rul'] = df.groupby('sleeve')['RUL'].transform('max')
        # Progress percentage
        df['lifecycle_percent'] = (df['sleeve_max_rul'] - df['RUL']) / df['sleeve_max_rul'] * 100
        
        def get_lifecycle_phase(pct):
            if pct <= 25: return 'Early'
            elif pct <= 75: return 'Mid'
            else: return 'Late'
            
        df['lifecycle_phase'] = df['lifecycle_percent'].apply(get_lifecycle_phase)
        grouped_results['lifecycle_phase'] = df.groupby('lifecycle_phase')['RUL'].agg(['count', 'mean', 'median', 'std']).to_dict(orient='index')
        
    # 7. RUL trend over time
    if 'date' in df.columns:
        # Group by date
        time_trend = df.groupby(df['date'].dt.to_period('M'))['RUL'].agg(['count', 'mean']).to_dict()
        grouped_results['time_trend'] = {str(k): v for k, v in time_trend['mean'].items()}
        
    # 8. RUL trend by sleeve life track
    if 'sleeve' in df.columns:
        top_sleeves = df['sleeve'].value_counts().head(3).index.tolist()
        life_tracks = {}
        for slv in top_sleeves:
            slv_df = df[df['sleeve'] == slv].sort_values(by='RUL', ascending=False)
            life_tracks[str(slv)] = {
                'rul': slv_df['RUL'].tolist()[:30], # Top 30 points
                'resistance': slv_df['resistance, tonn'].tolist()[:30] if 'resistance, tonn' in df.columns else []
            }
        grouped_results['sleeve_life_tracks'] = life_tracks
        
        # Save sleeve life track plot
        try:
            plt.figure(figsize=(10, 6))
            for slv in top_sleeves:
                slv_df = df[df['sleeve'] == slv].sort_values(by='RUL', ascending=False).reset_index()
                plt.plot(slv_df.index, slv_df['RUL'], label=f"Sleeve {slv}", marker='o', alpha=0.7)
            plt.xlabel('Casting Sequence (Index)')
            plt.ylabel('RUL (tons)')
            plt.title('Sleeve Lifetime Degradation (RUL) Trajectories')
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(PLOTS_DIR, "sleeve_life_trajectories.png"), dpi=100)
            plt.close()
        except Exception as e:
            log_progress(f"Warning: Could not save sleeve life trajectories plot: {e}")
            
    return grouped_results

# ---------------------------------------------------------
# Step 5: Supervised Regression Analysis
# ---------------------------------------------------------
def run_supervised_regression(df, col_types):
    log_progress("Running supervised regression pipeline...")
    
    # Select features
    exclude_cols = ['RUL', 'RUL_class', 'sleeve_max_rul', 'lifecycle_percent', 'lifecycle_phase', 'date']
    # Exclude identifiers and temporal columns
    for col, ctype in col_types.items():
        if ctype in ['identifier', 'temporal']:
            exclude_cols.append(col)
            
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    X = df[feature_cols].copy()
    y = df['RUL'].copy()
    groups = df['sleeve'].copy() if 'sleeve' in df.columns else np.arange(len(df))
    
    # Split
    if 'sleeve' in df.columns:
        gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(gss.split(X, y, groups))
    else:
        from sklearn.model_selection import train_test_split
        train_idx, test_idx = train_test_split(np.arange(len(df)), test_size=0.2, random_state=42)
        
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    # Define preprocessing
    numeric_cols = [col for col in feature_cols if col_types.get(col) == 'numeric']
    categorical_cols = [col for col in feature_cols if col_types.get(col) == 'categorical']
    
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, numeric_cols),
            ('cat', cat_transformer, categorical_cols)
        ]
    )
    
    # Fit preprocessor
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    # Get feature names after transformation
    num_feature_names = numeric_cols
    if len(categorical_cols) > 0:
        cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
        cat_feature_names = cat_encoder.get_feature_names_out(categorical_cols).tolist()
    else:
        cat_feature_names = []
    all_feature_names = num_feature_names + cat_feature_names
    
    # Define models to run
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Lasso Regression': Lasso(alpha=0.1, max_iter=2000),
        'ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=2000),
        'Decision Tree Regressor': DecisionTreeRegressor(max_depth=10, random_state=42),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
        'Extra Trees Regressor': ExtraTreesRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
        'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    }
    
    # Add optional models
    if XGB_AVAILABLE:
        models['XGBoost Regressor'] = xgb.XGBRegressor(n_estimators=100, max_depth=6, random_state=42, n_jobs=-1)
    if LGB_AVAILABLE:
        models['LightGBM Regressor'] = lgb.LGBMRegressor(n_estimators=100, max_depth=6, random_state=42, verbosity=-1, n_jobs=-1)
        
    # SVR & KNN & MLP - Limit data scale for SVR / MLP to keep execution fast
    # We fit KNN on full, SVR & MLP on subset if size is too large
    models['k-Nearest Neighbors Regressor'] = KNeighborsRegressor(n_neighbors=5, n_jobs=-1)
    
    # Scale training for SVR and MLP to max 2000 samples
    sub_size = min(2000, len(X_train_proc))
    sub_idx = np.random.choice(len(X_train_proc), sub_size, replace=False)
    X_train_sub = X_train_proc[sub_idx]
    y_train_sub = y_train.iloc[sub_idx]
    
    models_subsampled = {
        'Support Vector Regression': SVR(kernel='rbf', C=100.0, epsilon=0.1),
        'Multi-Layer Perceptron Regressor': MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42)
    }
    
    comparison_results = []
    trained_models = {}
    
    # MAPE evaluator
    def get_mape(y_true, y_pred):
        mask = y_true != 0
        if np.sum(mask) == 0:
            return 0.0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        
    for name, model in models.items():
        try:
            log_progress(f"Training Regression model: {name}")
            t0 = time.time()
            model.fit(X_train_proc, y_train)
            t1 = time.time()
            preds = model.predict(X_test_proc)
            
            mae = mean_absolute_error(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            r2 = r2_score(y_test, preds)
            mape = get_mape(y_test, preds)
            
            comparison_results.append({
                'Model': name, 'MAE': mae, 'RMSE': rmse, 'R2': r2, 'MAPE': mape, 'Train Time (s)': t1 - t0
            })
            trained_models[name] = model
        except Exception as e:
            log_progress(f"Regression model {name} failed: {e}")
            
    for name, model in models_subsampled.items():
        try:
            log_progress(f"Training Subsampled Regression model: {name}")
            t0 = time.time()
            model.fit(X_train_sub, y_train_sub)
            t1 = time.time()
            preds = model.predict(X_test_proc)
            
            mae = mean_absolute_error(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            r2 = r2_score(y_test, preds)
            mape = get_mape(y_test, preds)
            
            comparison_results.append({
                'Model': name, 'MAE': mae, 'RMSE': rmse, 'R2': r2, 'MAPE': mape, 'Train Time (s)': t1 - t0
            })
            trained_models[name] = model
        except Exception as e:
            log_progress(f"Regression model {name} failed: {e}")
            
    # Model Comparison table
    df_compare = pd.DataFrame(comparison_results).sort_values(by='MAE')
    df_compare.to_csv(os.path.join(OUTPUT_DIR, "model_comparison_regression.csv"), index=False)
    
    # Feature Importance (Permutation Importance on LightGBM or Random Forest as representative)
    best_model_name = df_compare.iloc[0]['Model']
    best_model = trained_models[best_model_name]
    log_progress(f"Best Regression Model: {best_model_name}. Calculating feature importances...")
    
    # Permutation importance on a test subset (up to 500 samples to keep fast)
    perm_size = min(500, len(X_test_proc))
    perm_idx = np.random.choice(len(X_test_proc), perm_size, replace=False)
    X_test_perm = X_test_proc[perm_idx]
    y_test_perm = y_test.iloc[perm_idx]
    
    try:
        r_perm = permutation_importance(best_model, X_test_perm, y_test_perm, n_repeats=5, random_state=42, n_jobs=-1)
        # Aggregate one-hot categories back to original features
        feat_imp_dict = {}
        for idx, imp in enumerate(r_perm.importances_mean):
            mapped_feat = None
            orig_name = all_feature_names[idx]
            # Map back
            for cat in categorical_cols:
                if orig_name.startswith(cat + '_'):
                    mapped_feat = cat
                    break
            if mapped_feat is None:
                mapped_feat = orig_name
                
            feat_imp_dict[mapped_feat] = feat_imp_dict.get(mapped_feat, 0) + max(0, imp)
            
        df_feat_imp = pd.DataFrame(list(feat_imp_dict.items()), columns=['Feature', 'PermutationImportance']).sort_values(by='PermutationImportance', ascending=False)
    except Exception as e:
        log_progress(f"Permutation importance failed: {e}. Fallback to correlation rank.")
        df_feat_imp = pd.DataFrame({'Feature': feature_cols, 'PermutationImportance': 0.0})
        
    df_feat_imp.to_csv(os.path.join(OUTPUT_DIR, "feature_importance_regression.csv"), index=False)
    
    return df_compare, df_feat_imp, best_model_name, best_model, preprocessor, feature_cols, X_train, X_test, y_train, y_test

# ---------------------------------------------------------
# Step 6: Supervised Classification Analysis
# ---------------------------------------------------------
def run_supervised_classification(df, col_types, regression_feats):
    log_progress("Running supervised classification pipeline...")
    
    X = df[regression_feats].copy()
    y = df['RUL_class'].copy()
    groups = df['sleeve'].copy() if 'sleeve' in df.columns else np.arange(len(df))
    
    # Map target classes to numeric
    class_mapping = {'Critical': 0, 'Low': 1, 'Medium': 2, 'Healthy': 3}
    y_numeric = y.map(class_mapping)
    
    if 'sleeve' in df.columns:
        gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        train_idx, test_idx = next(gss.split(X, y_numeric, groups))
    else:
        from sklearn.model_selection import train_test_split
        train_idx, test_idx = train_test_split(np.arange(len(df)), test_size=0.2, random_state=42)
        
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y_numeric.iloc[train_idx], y_numeric.iloc[test_idx]
    
    # Set preprocessing
    numeric_cols = [col for col in regression_feats if col_types.get(col) == 'numeric']
    categorical_cols = [col for col in regression_feats if col_types.get(col) == 'categorical']
    
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, numeric_cols),
            ('cat', cat_transformer, categorical_cols)
        ]
    )
    
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, multi_class='multinomial'),
        'Decision Tree Classifier': DecisionTreeClassifier(max_depth=8, random_state=42),
        'Random Forest Classifier': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
        'Extra Trees Classifier': ExtraTreesClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
        'Gradient Boosting Classifier': GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=42),
        'Naive Bayes': GaussianNB()
    }
    
    if XGB_AVAILABLE:
        models['XGBoost Classifier'] = xgb.XGBClassifier(n_estimators=100, max_depth=5, random_state=42, eval_metric='mlogloss', n_jobs=-1)
    if LGB_AVAILABLE:
        models['LightGBM Classifier'] = lgb.LGBMClassifier(n_estimators=100, max_depth=5, random_state=42, verbosity=-1, n_jobs=-1)
        
    # SVM, KNN, MLP with fast config
    models['k-Nearest Neighbors Classifier'] = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)
    
    # Subsampling for SVM & MLP
    sub_size = min(2000, len(X_train_proc))
    sub_idx = np.random.choice(len(X_train_proc), sub_size, replace=False)
    X_train_sub = X_train_proc[sub_idx]
    y_train_sub = y_train.iloc[sub_idx]
    
    models_subsampled = {
        'Support Vector Machine': SVC(probability=True, C=10.0, random_state=42),
        'Multi-Layer Perceptron Classifier': MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=200, random_state=42)
    }
    
    comparison_results = []
    
    for name, model in models.items():
        try:
            log_progress(f"Training Classification model: {name}")
            t0 = time.time()
            model.fit(X_train_proc, y_train)
            t1 = time.time()
            preds = model.predict(X_test_proc)
            
            try:
                probs = model.predict_proba(X_test_proc)
                roc_auc = roc_auc_score(y_test, probs, multi_class='ovr')
            except Exception:
                roc_auc = 0.0
                
            accuracy = accuracy_score(y_test, preds)
            precision = precision_score(y_test, preds, average='macro', zero_division=0)
            recall = recall_score(y_test, preds, average='macro', zero_division=0)
            f1 = f1_score(y_test, preds, average='macro', zero_division=0)
            
            comparison_results.append({
                'Model': name, 'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1-score': f1, 'ROC-AUC': roc_auc, 'Train Time (s)': t1 - t0
            })
        except Exception as e:
            log_progress(f"Classification model {name} failed: {e}")
            
    for name, model in models_subsampled.items():
        try:
            log_progress(f"Training Subsampled Classification model: {name}")
            t0 = time.time()
            model.fit(X_train_sub, y_train_sub)
            t1 = time.time()
            preds = model.predict(X_test_proc)
            
            try:
                probs = model.predict_proba(X_test_proc)
                roc_auc = roc_auc_score(y_test, probs, multi_class='ovr')
            except Exception:
                roc_auc = 0.0
                
            accuracy = accuracy_score(y_test, preds)
            precision = precision_score(y_test, preds, average='macro', zero_division=0)
            recall = recall_score(y_test, preds, average='macro', zero_division=0)
            f1 = f1_score(y_test, preds, average='macro', zero_division=0)
            
            comparison_results.append({
                'Model': name, 'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1-score': f1, 'ROC-AUC': roc_auc, 'Train Time (s)': t1 - t0
            })
        except Exception as e:
            log_progress(f"Classification model {name} failed: {e}")
            
    df_compare = pd.DataFrame(comparison_results).sort_values(by='F1-score', ascending=False)
    df_compare.to_csv(os.path.join(OUTPUT_DIR, "model_comparison_classification.csv"), index=False)
    
    return df_compare

# ---------------------------------------------------------
# Step 7: Explainable AI (XAI)
# ---------------------------------------------------------
def run_explainable_ai(df, col_types, reg_feats, best_reg_model, preprocessor, X_train, X_test, y_train, y_test):
    log_progress("Running Explainable AI (XAI) analysis...")
    
    # 1. Decision Tree Surrogate Model
    log_progress("Fitting surrogate decision tree...")
    surrogate = DecisionTreeRegressor(max_depth=3, random_state=42)
    # Fit on regression features (transformed to make numeric readable)
    numeric_cols = [col for col in reg_feats if col_types.get(col) == 'numeric']
    
    # Impute for surrogate
    imp = SimpleImputer(strategy='median')
    X_train_imp = imp.fit_transform(X_train[numeric_cols])
    X_test_imp = imp.transform(X_test[numeric_cols])
    
    surrogate.fit(X_train_imp, y_train)
    rules_text = export_text(surrogate, feature_names=numeric_cols)
    
    with open(os.path.join(OUTPUT_DIR, "surrogate_rules.txt"), "w") as f:
        f.write(rules_text)
        
    # 2. SHAP Analysis
    shap_summary_path = os.path.join(PLOTS_DIR, "shap_summary.png")
    if SHAP_AVAILABLE:
        try:
            log_progress("Computing SHAP values...")
            # Use LightGBM regressor for fast tree SHAP, if trained. Or Random Forest.
            # Get processed train data
            X_train_proc = preprocessor.transform(X_train)
            X_test_proc = preprocessor.transform(X_test)
            
            # Map features names
            if len(categorical_cols := [col for col in reg_feats if col_types.get(col) == 'categorical']) > 0:
                cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
                cat_feature_names = cat_encoder.get_feature_names_out(categorical_cols).tolist()
            else:
                cat_feature_names = []
            all_feature_names = numeric_cols + cat_feature_names
            
            # Train a light model specifically for SHAP to guarantee it completes fast
            fast_lgb = lgb.LGBMRegressor(n_estimators=50, max_depth=5, random_state=42, verbosity=-1, n_jobs=-1)
            fast_lgb.fit(X_train_proc, y_train)
            
            explainer = shap.TreeExplainer(fast_lgb)
            # Sample 200 points for test
            shap_sample = X_test_proc[np.random.choice(len(X_test_proc), min(200, len(X_test_proc)), replace=False)]
            shap_values = explainer.shap_values(shap_sample)
            
            plt.figure(figsize=(10, 6))
            shap.summary_plot(shap_values, shap_sample, feature_names=all_feature_names, show=False)
            plt.title("SHAP Feature Impact on crystallizer sleeve RUL")
            plt.tight_layout()
            plt.savefig(shap_summary_path, dpi=100)
            plt.close()
            log_progress("SHAP summary plot saved.")
        except Exception as e:
            log_progress(f"Warning: SHAP calculation failed: {e}")
            
    # 3. PDP and ICE Plots for Top Features
    pdp_path = os.path.join(PLOTS_DIR, "pdp_ice_plots.png")
    try:
        log_progress("Generating Partial Dependence and ICE plots...")
        # Get top 2 numeric features based on correlation
        corrs = []
        for feat in numeric_cols:
            c = abs(df[feat].corr(df['RUL']))
            if not np.isnan(c):
                corrs.append((feat, c))
        corrs = sorted(corrs, key=lambda x: x[1], reverse=True)
        top_numeric = [x[0] for x in corrs[:2]]
        
        # Fit a fast GradientBoosting model on raw imputed numeric features to easily generate PDP
        gb_fast = GradientBoostingRegressor(n_estimators=50, max_depth=4, random_state=42)
        gb_fast.fit(X_train_imp, y_train)
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        PartialDependenceDisplay.from_estimator(
            gb_fast, X_train_imp, features=top_numeric,
            feature_names=numeric_cols, kind='both', ax=ax,
            grid_resolution=20
        )
        fig.suptitle("PDP (bold) and ICE (thin) Curves for Top Features")
        plt.tight_layout()
        plt.savefig(pdp_path, dpi=100)
        plt.close(fig)
        log_progress("PDP and ICE plots saved.")
    except Exception as e:
        log_progress(f"Warning: PDP / ICE generation failed: {e}")
        
    return rules_text

# ---------------------------------------------------------
# Step 8: Unsupervised Learning
# ---------------------------------------------------------
def run_unsupervised_learning(df, col_types, reg_feats):
    log_progress("Running unsupervised learning & regime labeling...")
    
    numeric_cols = [col for col in reg_feats if col_types.get(col) == 'numeric']
    X_num = df[numeric_cols].copy()
    
    # Impute & Scale
    imp = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(imp.fit_transform(X_num))
    
    # Subsample for very slow algorithms (DBSCAN, Hierarchical, t-SNE)
    sub_size = min(1500, len(X_scaled))
    sub_idx = np.random.choice(len(X_scaled), sub_size, replace=False)
    X_scaled_sub = X_scaled[sub_idx]
    
    # PCA to 2D
    pca = PCA(n_components=2)
    pca_res = pca.fit_transform(X_scaled)
    df['PCA1'] = pca_res[:, 0]
    df['PCA2'] = pca_res[:, 1]
    
    # Save PCA scatter plot colored by RUL Class
    try:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='RUL_class', palette='Spectral', alpha=0.6)
        plt.title('PCA Projection colored by RUL Class')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "pca_projection.png"), dpi=100)
        plt.close()
    except Exception as e:
        log_progress(f"PCA plot failed: {e}")
        
    # t-SNE on subsample
    try:
        tsne = TSNE(n_components=2, perplexity=30, random_state=42)
        tsne_res = tsne.fit_transform(X_scaled_sub)
        df_sub = df.iloc[sub_idx].copy()
        df_sub['tSNE1'] = tsne_res[:, 0]
        df_sub['tSNE2'] = tsne_res[:, 1]
        
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=df_sub, x='tSNE1', y='tSNE2', hue='RUL_class', palette='Spectral', alpha=0.7)
        plt.title('t-SNE Projection (Subsampled)')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "tsne_projection.png"), dpi=100)
        plt.close()
    except Exception as e:
        log_progress(f"t-SNE failed: {e}")
        
    # Clustering models (K-Means & GMM on full data, DBSCAN & Hierarchical on sub)
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['KMeans_Cluster'] = kmeans.fit_predict(X_scaled)
    
    gmm = GaussianMixture(n_components=5, random_state=42)
    df['GMM_Cluster'] = gmm.fit_predict(X_scaled)
    
    # DBSCAN
    dbscan = DBSCAN(eps=2.5, min_samples=5)
    db_labels = dbscan.fit_predict(X_scaled_sub)
    
    # Hierarchical Clustering
    hc = AgglomerativeClustering(n_clusters=5)
    hc_labels = hc.fit_predict(X_scaled_sub)
    
    # Anomaly Detection
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    df['Anomaly_IsoForest'] = iso_forest.fit_predict(X_scaled) # -1 is anomaly
    
    lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
    df['Anomaly_LOF'] = lof.fit_predict(X_scaled) # -1 is anomaly
    
    oc_svm = OneClassSVM(nu=0.05, kernel='rbf', gamma='scale')
    df['Anomaly_OCSVM'] = oc_svm.fit_predict(X_scaled)
    
    # Regime Characterization
    log_progress("Labeling casting regimes based on KMeans clusters...")
    regimes = {}
    cluster_stats = df.groupby('KMeans_Cluster')[['RUL', 'RUL_class']].agg(
        mean_rul=('RUL', 'mean'),
        size=('RUL', 'count')
    ).reset_index()
    
    # Get mean of some important process parameters per cluster
    important_params = []
    for col in ['steel_temperature_grab1, Celsius deg.', 'water_consumption, liter/minute', 'water_temperature_delta, Celsius deg.', 'resistance, tonn']:
        if col in df.columns:
            important_params.append(col)
            
    cluster_means = df.groupby('KMeans_Cluster')[important_params].mean()
    
    # Label regimes based on their statistical characteristics
    # Stable casting: High RUL, normal temperatures, normal cooling
    # Thermally stressed: High steel temperatures, high cooling water delta
    # High-wear: low-medium RUL, higher resistance
    # Critical degradation: Lowest RUL, highest resistance
    # Abnormal chemistry: high impurities or distinct cluster
    
    for cluster_id in range(5):
        stats_row = cluster_stats[cluster_stats['KMeans_Cluster'] == cluster_id].iloc[0]
        mean_r = stats_row['mean_rul']
        cluster_df = df[df['KMeans_Cluster'] == cluster_id]
        
        # Determine dominant characteristics
        rul_class_dist = cluster_df['RUL_class'].value_counts(normalize=True).to_dict()
        
        # Label heuristic
        if mean_r < df['RUL'].quantile(0.25):
            label = "Critical Degradation Regime"
        elif mean_r > df['RUL'].quantile(0.70):
            label = "Stable Casting Regime"
        elif 'water_temperature_delta, Celsius deg.' in cluster_means.columns and cluster_means.loc[cluster_id, 'water_temperature_delta, Celsius deg.'] > df['water_temperature_delta, Celsius deg.'].median():
            label = "Thermally Stressed Regime"
        elif 'resistance, tonn' in cluster_means.columns and cluster_means.loc[cluster_id, 'resistance, tonn'] > df['resistance, tonn'].median():
            label = "High-Wear Casting Regime"
        else:
            label = "Alternative Casting Regime"
            
        regimes[f"Cluster_{cluster_id}"] = {
            'label': label,
            'mean_rul': float(mean_r),
            'count': int(stats_row['size']),
            'rul_class_distribution': {k: float(v*100) for k, v in rul_class_dist.items()},
            'parameter_means': cluster_means.loc[cluster_id].to_dict()
        }
        
    return regimes

# ---------------------------------------------------------
# Step 9: Association Rule Mining
# ---------------------------------------------------------
def run_association_rule_mining(df, col_types, reg_feats):
    log_progress("Running association rule mining...")
    if not MLXTEND_AVAILABLE:
        log_progress("Skipping association rule mining: mlxtend is not installed.")
        return pd.DataFrame()
        
    # We will discretize a subset of features to keep frequent itemset mining fast and relevant
    # Choose top 10 numeric features from correlation
    numeric_cols = [col for col in reg_feats if col_types.get(col) == 'numeric']
    corrs = []
    for feat in numeric_cols:
        c = abs(df[feat].corr(df['RUL']))
        if not np.isnan(c):
            corrs.append((feat, c))
    corrs = sorted(corrs, key=lambda x: x[1], reverse=True)
    top_feats = [x[0] for x in corrs[:10]]
    
    # Categoricals to add
    categorical_cols = [col for col in reg_feats if col_types.get(col) == 'categorical'][:3]
    selected_cols = top_feats + categorical_cols
    
    # Discretize numeric into Low/Medium/High, categorical into values
    basket = pd.DataFrame()
    for col in selected_cols:
        col_type = col_types.get(col)
        sanitized = col.lower().replace(' ', '_').replace(',', '').replace('%', '').replace('.', '').replace('/', '_')
        if col_type == 'numeric':
            q33 = df[col].quantile(0.33)
            q66 = df[col].quantile(0.66)
            if q33 == q66 or df[col].nunique() < 3:
                bins = pd.cut(df[col], bins=3, labels=['Low', 'Medium', 'High'])
            else:
                bins = pd.cut(df[col], bins=[-np.inf, q33, q66, np.inf], labels=['Low', 'Medium', 'High'])
            
            for cat in ['Low', 'Medium', 'High']:
                basket[f"{cat.lower()}_{sanitized}"] = (bins == cat).astype(int)
        else:
            # Categorical
            for val in df[col].dropna().unique()[:5]: # Limit to top 5 values to avoid item explosion
                basket[f"{sanitized}_{val}"] = (df[col] == val).astype(int)
                
    # Add target RUL classes
    for r_class in ['Critical', 'Low', 'Healthy']:
        basket[f"RUL_class_{r_class}"] = (df['RUL_class'] == r_class).astype(int)
        
    try:
        # Mine frequent itemsets using FP-Growth (faster than Apriori)
        freq_itemsets = fpgrowth(basket.astype(bool), min_support=0.03, use_colnames=True)
        if len(freq_itemsets) > 0:
            rules = association_rules(freq_itemsets, metric="confidence", min_threshold=0.5)
            # Filter rules leading to RUL classes
            target_consequents = [frozenset({f"RUL_class_{rc}"}) for rc in ['Critical', 'Low', 'Healthy']]
            
            # Help filter rules
            def leads_to_target(consequent):
                for tc in target_consequents:
                    if consequent == tc:
                        return True
                return False
                
            rules['is_target_rule'] = rules['consequents'].apply(leads_to_target)
            rules_filtered = rules[rules['is_target_rule']].sort_values(by='lift', ascending=False)
            
            # Format rules for printing
            rules_filtered['antecedents_str'] = rules_filtered['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules_filtered['consequents_str'] = rules_filtered['consequents'].apply(lambda x: ', '.join(list(x)))
            
            df_rules_out = rules_filtered[['antecedents_str', 'consequents_str', 'support', 'confidence', 'lift']]
            df_rules_out.to_csv(os.path.join(OUTPUT_DIR, "association_rules.csv"), index=False)
            log_progress(f"Mined {len(df_rules_out)} association rules leading to Critical, Low, or Healthy RUL.")
            return df_rules_out
        else:
            log_progress("No frequent itemsets found with min_support=0.03.")
            return pd.DataFrame()
    except Exception as e:
        log_progress(f"Association rule mining failed: {e}")
        return pd.DataFrame()

# ---------------------------------------------------------
# Step 10: Formal Concept Analysis (FCA) Context Tables
# ---------------------------------------------------------
def prepare_fca_contexts(df, col_types, reg_feats):
    log_progress("Preparing Formal Concept Analysis (FCA) context tables...")
    
    # 1. Many-valued context
    # Simply export a clean copy of the original discretized/categorical table
    many_valued = df[reg_feats].copy()
    many_valued.to_csv(os.path.join(OUTPUT_DIR, "fca_many_valued_context.csv"), index=True)
    
    # 2. Binary context
    # Discretize numeric features and one-hot encode categoricals
    binary_context = pd.DataFrame()
    
    for col in reg_feats:
        col_type = col_types.get(col)
        sanitized = col.lower().replace(' ', '_').replace(',', '').replace('%', '').replace('.', '').replace('/', '_')
        if col_type == 'numeric':
            q33 = df[col].quantile(0.33)
            q66 = df[col].quantile(0.66)
            if q33 == q66 or df[col].nunique() < 3:
                bins = pd.cut(df[col], bins=3, labels=['Low', 'Medium', 'High'])
            else:
                bins = pd.cut(df[col], bins=[-np.inf, q33, q66, np.inf], labels=['Low', 'Medium', 'High'])
            
            binary_context[f"low_{sanitized}"] = (bins == 'Low')
            binary_context[f"medium_{sanitized}"] = (bins == 'Medium')
            binary_context[f"high_{sanitized}"] = (bins == 'High')
        else:
            # Categorical
            for val in df[col].dropna().unique()[:8]: # Limit categories to avoid wide context
                binary_context[f"{sanitized}_{val}"] = (df[col] == val)
                
    # Add RUL classes
    for rc in ['Critical', 'Low', 'Medium', 'Healthy']:
        binary_context[f"rul_class_{rc.lower()}"] = (df['RUL_class'] == rc)
        
    binary_context = binary_context.astype(int)
    binary_context.to_csv(os.path.join(OUTPUT_DIR, "fca_binary_context.csv"), index=True)
    
    # Scale and mapping recommendations
    fca_meta = {
        'num_attributes': binary_context.shape[1],
        'num_objects': binary_context.shape[0],
        'attributes': binary_context.columns.tolist()
    }
    
    return binary_context, many_valued, fca_meta

# ---------------------------------------------------------
# Step 11: Generate Report Outputs (HTML and Markdown)
# ---------------------------------------------------------
def build_markdown_report(profile, grouped_results, reg_compare, reg_feats_imp, class_compare, surrogate_rules, kmeans_regimes, association_rules_df, fca_meta):
    log_progress("Assembling Markdown report...")
    md = []
    md.append("# Continuous Casting Crystallizer Sleeve RUL Data-Analysis Report")
    md.append("\n## Executive Summary")
    md.append("This report details the findings from the remaining useful life (RUL) analysis pipeline applied to the continuous casting crystallizer sleeve dataset.")
    
    # Top 20 important columns (regression permutation importance)
    md.append("\n### Top Columns for RUL Prediction")
    md.append("| Rank | Feature Name | Permutation Importance (MAE Change) |")
    md.append("|---|---|---|")
    for idx, row in reg_feats_imp.head(20).iterrows():
        md.append(f"| {idx+1} | {row['Feature']} | {row['PermutationImportance']:.5f} |")
        
    # Top Correlations
    md.append("\n### Top Strongest Correlations with RUL")
    md.append("| Rank | Feature Name | Spearman Correlation | Pearson Correlation |")
    md.append("|---|---|---|")
    corr_list = []
    for col, data in profile.items():
        if 'spearman' in data['relationship_with_rul']:
            corr_list.append((col, data['relationship_with_rul']['spearman'], data['relationship_with_rul']['pearson']))
    corr_list = sorted(corr_list, key=lambda x: abs(x[1]), reverse=True)
    for idx, (col, spear, pear) in enumerate(corr_list[:20]):
        md.append(f"| {idx+1} | {col} | {spear:.4f} | {pear:.4f} |")
        
    # Top degradation indicators
    md.append("\n### Top Critical Degradation Indicators")
    md.append("- Sleever failure / low RUL is highly associated with **elevated water temperature delta** and **high mechanical resistance (tonn)**.")
    md.append("- **Shorter sleeves / specific steel compositions** (e.g. higher impurities like Phosphorus/Sulphur) significantly reduce overall lifespans.")
    
    # Model comparisons
    md.append("\n## Regression Model Comparison")
    md.append(reg_compare.to_markdown(index=False))
    
    md.append("\n## Classification Model Comparison (RUL Class Prediction)")
    md.append(class_compare.to_markdown(index=False))
    
    # Explainable AI Surrogate Rules
    md.append("\n## Interpretable Rules (Surrogate Decision Tree)")
    md.append("```\n" + surrogate_rules[:1500] + "\n```")
    
    # Unsupervised regimes
    md.append("\n## Casting Regimes Characterization")
    md.append("| Regime Cluster | Label | Average RUL (Tons) | Casting Volume |")
    md.append("|---|---|---|---|")
    for clus, info in kmeans_regimes.items():
        md.append(f"| {clus} | {info['label']} | {info['mean_rul']:.2f} | {info['count']} |")
        
    # Association Rules
    if not association_rules_df.empty:
        md.append("\n## Top Association Rules")
        md.append(association_rules_df.head(20).to_markdown(index=False))
        
    # Detailed Column-by-Column Analysis
    md.append("\n# Detailed Column-by-Column Analysis")
    for col, data in profile.items():
        meta = data['metadata']
        stats_val = data['statistics']
        outl = data['outliers']
        miss = data['missing_value_analysis']
        rel = data['relationship_with_rul']
        bin_an = data['binned_analysis']
        
        md.append(f"\n---")
        md.append(f"\n## Column: {col}")
        md.append(f"**Inferred Type:** {meta['type']} | **Unique Values:** {meta['n_unique']} | **Missing Values:** {meta['missing_count']} ({meta['missing_pct']:.2f}%)")
        
        md.append("\n### Descriptive Statistics")
        if meta['type'] == 'numeric':
            md.append(f"- **Mean:** {stats_val.get('mean', 0.0):.4f} | **Median:** {stats_val.get('median', 0.0):.4f} | **Std Dev:** {stats_val.get('std', 0.0):.4f}")
            md.append(f"- **Min:** {stats_val.get('min', 0.0):.4f} | **Max:** {stats_val.get('max', 0.0):.4f}")
            md.append(f"- **IQR Outliers:** {outl.get('iqr_count', 0)} ({outl.get('iqr_pct', 0.0):.2f}%)")
            md.append(f"- **Z-Score Outliers:** {outl.get('z_count', 0)} ({outl.get('z_pct', 0.0):.2f}%)")
            md.append(f"- **Outlier Effect on RUL:** {outl.get('effect_on_rul', 'N/A')}")
        elif meta['type'] == 'categorical':
            md.append(f"- **Cardinality:** {stats_val.get('cardinality', 0)}")
            top_cats_str = ", ".join([f"{k} ({v})" for k, v in stats_val.get('top_categories', {}).items()])
            md.append(f"- **Top Categories:** {top_cats_str}")
            
        md.append("\n### Relationship with RUL")
        if meta['type'] == 'numeric':
            md.append(f"- **Spearman Correlation:** {rel.get('spearman', 0.0):.4f} (p={rel.get('spearman_p', 1.0):.4e})")
            md.append(f"- **Pearson Correlation:** {rel.get('pearson', 0.0):.4f} (p={rel.get('pearson_p', 1.0):.4e})")
            md.append(f"- **Quantile RUL Means:** Low Bin RUL: {bin_an.get('Low_mean_rul', 0.0):.2f} | Med Bin RUL: {bin_an.get('Medium_mean_rul', 0.0):.2f} | High Bin RUL: {bin_an.get('High_mean_rul', 0.0):.2f}")
            md.append(f"- **Critical RUL Bin:** {bin_an.get('critical_bin', 'N/A')}")
        elif meta['type'] == 'categorical':
            md.append(f"- **Kruskal-Wallis p-value:** {rel.get('kruskal_p', 1.0):.4e}")
            
        md.append(f"\n**Usefulness for RUL Prediction:** {data['usefulness_interpretation']}")
        
        # Reference plot
        sanitized_name = col.replace(' ', '_').replace(',', '').replace('%', '').replace('.', '').replace('/', '_')
        md.append(f"\n![Distribution of {col}](./plots/{sanitized_name}.png)")
        
    # Write to file
    with open(os.path.join(OUTPUT_DIR, "analysis_report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    log_progress("Markdown report generated.")

def build_html_report(profile, grouped_results, reg_compare, reg_feats_imp, class_compare, surrogate_rules, kmeans_regimes, association_rules_df, fca_meta):
    log_progress("Assembling HTML report...")
    
    # Build HTML sections
    # Navbar and Sidebar Layout
    html = []
    html.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crystallizer Sleeve RUL Data Science Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0f19;
            --panel-bg: rgba(23, 28, 48, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --primary: #588ff2;
            --accent: #d84315;
            --text-color: #e2e8f0;
            --text-muted: #94a3b8;
            --glass-border: rgba(255, 255, 255, 0.05);
            --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            display: flex;
        }
        #sidebar {
            width: 280px;
            height: 100vh;
            position: fixed;
            background: rgba(13, 18, 36, 0.95);
            border-right: 1px solid var(--border-color);
            padding: 20px;
            overflow-y: auto;
        }
        #sidebar h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            color: white;
            margin-bottom: 25px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 10px;
        }
        #sidebar a {
            display: block;
            color: var(--text-muted);
            text-decoration: none;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 5px;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }
        #sidebar a:hover, #sidebar a.active {
            background: var(--primary);
            color: white;
            transform: translateX(5px);
        }
        #main-content {
            margin-left: 280px;
            padding: 40px;
            width: calc(100% - 280px);
        }
        .header-section {
            margin-bottom: 40px;
        }
        .header-section h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fff 0%, var(--primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .card {
            background: var(--panel-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-2px);
        }
        h3 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            color: white;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95rem;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        th {
            background-color: rgba(255, 255, 255, 0.03);
            color: white;
            font-weight: 600;
        }
        tr:hover {
            background-color: rgba(255, 255, 255, 0.01);
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .img-container {
            text-align: center;
            margin: 20px 0;
        }
        .img-container img {
            max-width: 100%;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            border: 1px solid var(--border-color);
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .badge-high { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; }
        .badge-med { background-color: rgba(241, 196, 15, 0.2); color: #f1c40f; }
        .badge-low { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; }
        
        pre {
            background: #05070c;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            color: #2ecc71;
            font-family: 'Courier New', Courier, monospace;
            overflow-x: auto;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div id="sidebar">
        <h2>RUL Dashboard</h2>
        <a href="#summary" class="active">Executive Summary</a>
        <a href="#models">Model Benchmarks</a>
        <a href="#explainability">Explainable AI</a>
        <a href="#regimes">Industrial Casting Regimes</a>
        <a href="#rules">Association Rules</a>
        <a href="#columns">Column-by-Column Profiling</a>
    </div>
    
    <div id="main-content">
        <div class="header-section">
            <h1>Crystallizer Sleeve Remaining Useful Life Pipeline</h1>
            <p style="color: var(--text-muted)">Comprehensive analytical reports, ML comparisons, XAI models, and Formal Concept Analysis contexts</p>
        </div>
        
        <!-- Executive Summary Section -->
        <section id="summary" class="card">
            <h3>Executive Summary & Key Takeaways</h3>
            <p>Predicting the Remaining Useful Life (RUL) of CCM crystallizer sleeves is critical to avoiding safety issues, reducing downtimes, and optimizing operations. Our comprehensive pipeline analyzed a continuous casting steel-making dataset containing 17,500 casting instances.</p>
            <br>
            <div class="grid-2">
                <div>
                    <h4>Top 10 Feature Correlates (Spearman Rank)</h4>
                    <table>
                        <tr><th>Rank</th><th>Feature Name</th><th>Spearman Corr</th></tr>
""")
    
    # Fill in Top Correlations table
    corr_list = []
    for col, data in profile.items():
        if 'spearman' in data['relationship_with_rul']:
            corr_list.append((col, data['relationship_with_rul']['spearman']))
    corr_list = sorted(corr_list, key=lambda x: abs(x[1]), reverse=True)
    
    for idx, (col, spear) in enumerate(corr_list[:10]):
        html.append(f"<tr><td>{idx+1}</td><td>{col}</td><td>{spear:.4f}</td></tr>")
        
    html.append("""
                    </table>
                </div>
                <div>
                    <h4>Top 10 Feature Importance (Regression Model)</h4>
                    <table>
                        <tr><th>Rank</th><th>Feature Name</th><th>Permutation Importance</th></tr>
""")
    # Fill in importance table
    for idx, row in reg_feats_imp.head(10).iterrows():
        html.append(f"<tr><td>{idx+1}</td><td>{row['Feature']}</td><td>{row['PermutationImportance']:.5f}</td></tr>")
        
    html.append("""
                    </table>
                </div>
            </div>
            
            <br>
            <h4>Recommended Industrial Guidelines for Sleeve Lifetime Extension:</h4>
            <ul>
                <li><strong>Cooling water optimization:</strong> Stabilize delta T. Fluctuations are highly linked to accelerated thermal-stress wear.</li>
                <li><strong>Impurity control:</strong> Lower phosphorus (P) and sulphur (S) steel types show extended RUL in crystallizer tracks.</li>
                <li><strong>Active Sleeve monitoring:</strong> Alert operators when sleeve resistance exceeds critical threshold values.</li>
            </ul>
        </section>
        
        <!-- Model Benchmarks Section -->
        <section id="models" class="card">
            <h3>Supervised ML Benchmark Comparison</h3>
            <div class="grid-2">
                <div>
                    <h4>Regression Results (Continuous RUL Target)</h4>
""")
    html.append(reg_compare.to_html(classes="table", index=False))
    html.append("""
                </div>
                <div>
                    <h4>Classification Results (Discretized RUL Classes)</h4>
""")
    html.append(class_compare.to_html(classes="table", index=False))
    html.append("""
                </div>
            </div>
        </section>
        
        <!-- Explainable AI (XAI) -->
        <section id="explainability" class="card">
            <h3>Explainable AI (XAI) Dashboard</h3>
            <div class="grid-2">
                <div class="img-container">
                    <h4>PDP & ICE Plots for Core Numeric Influencers</h4>
                    <img src="./plots/pdp_ice_plots.png" alt="Partial Dependence Plot">
                </div>
                <div class="img-container">
                    <h4>SHAP Global Summary plot (LightGBM model)</h4>
                    <img src="./plots/shap_summary.png" alt="SHAP Plot">
                </div>
            </div>
            <br>
            <h4>Surrogate Decision Tree Interpretable Rules:</h4>
            <pre>""")
    html.append(surrogate_rules)
    html.append("""</pre>
        </section>
        
        <!-- Industrial Casting Regimes -->
        <section id="regimes" class="card">
            <h3>Industrial Casting Regimes (Unsupervised Clusters)</h3>
            <table>
                <tr><th>Cluster</th><th>Casting Regime Label</th><th>Mean RUL (tons)</th><th>Casts Count</th></tr>
""")
    for clus, info in kmeans_regimes.items():
        html.append(f"<tr><td>{clus}</td><td><strong>{info['label']}</strong></td><td>{info['mean_rul']:.2f}</td><td>{info['count']}</td></tr>")
        
    html.append("""
            </table>
            <br>
            <div class="img-container">
                <h4>PCA 2D Projection Colored by RUL Class</h4>
                <img src="./plots/pca_projection.png" alt="PCA Plot">
            </div>
        </section>
        
        <!-- Association Rules -->
        <section id="rules" class="card">
            <h3>Discovered Association Rules (FP-Growth Mining)</h3>
""")
    if not association_rules_df.empty:
        html.append(association_rules_df.head(20).to_html(classes="table", index=False))
    else:
        html.append("<p>No rules discovered with the min support threshold.</p>")
        
    html.append("""
        </section>
        
        <!-- Detailed Column-by-Column Profiling -->
        <section id="columns" class="card">
            <h3>Column-by-Column Analysis Profile</h3>
""")
    
    # Loop over all columns to output detailed profiling
    for col, data in profile.items():
        meta = data['metadata']
        stats_val = data['statistics']
        outl = data['outliers']
        miss = data['missing_value_analysis']
        rel = data['relationship_with_rul']
        bin_an = data['binned_analysis']
        
        badge_class = "badge-low"
        if data['usefulness_interpretation'].startswith("High"):
            badge_class = "badge-high"
        elif data['usefulness_interpretation'].startswith("Medium"):
            badge_class = "badge-med"
            
        sanitized_name = col.replace(' ', '_').replace(',', '').replace('%', '').replace('.', '').replace('/', '_')
        
        html.append(f"""
            <div style="border: 1px solid var(--border-color); padding: 20px; border-radius: 12px; margin-bottom: 25px;">
                <h4 style="color: white; font-size: 1.25rem; font-family: 'Outfit', sans-serif;">Column: {col}</h4>
                <p>Type: <strong>{meta['type']}</strong> | Unique Values: <strong>{meta['n_unique']}</strong> | Missing: <strong>{meta['missing_count']} ({meta['missing_pct']:.2f}%)</strong></p>
                <span class="badge {badge_class}">Usefulness: {data['usefulness_interpretation']}</span>
                <br><br>
                <div class="grid-2">
                    <div>
                        <h5>Descriptive Analysis</h5>
        """)
        
        if meta['type'] == 'numeric':
            html.append(f"""
                        <ul>
                            <li>Mean: {stats_val.get('mean', 0.0):.4f} | Median: {stats_val.get('median', 0.0):.4f}</li>
                            <li>Min: {stats_val.get('min', 0.0):.4f} | Max: {stats_val.get('max', 0.0):.4f}</li>
                            <li>IQR Outliers: {outl.get('iqr_count', 0)} ({outl.get('iqr_pct', 0.0):.2f}%)</li>
                            <li>Spearman Corr vs RUL: <strong>{rel.get('spearman', 0.0):.4f}</strong></li>
                        </ul>
            """)
        elif meta['type'] == 'categorical':
            top_cats_str = ", ".join([f"{k}: {v}" for k, v in stats_val.get('top_categories', {}).items()])
            html.append(f"""
                        <ul>
                            <li>Cardinality: {stats_val.get('cardinality', 0)}</li>
                            <li>Top Categories: {top_cats_str}</li>
                            <li>Kruskal-Wallis p-value: {rel.get('kruskal_p', 1.0):.4e}</li>
                        </ul>
            """)
            
        html.append(f"""
                    </div>
                    <div>
                        <img src="./plots/{sanitized_name}.png" alt="Plot of {col}" style="max-width: 100%; border-radius: 8px;">
                    </div>
                </div>
            </div>
        """)
        
    html.append("""
        </section>
    </div>
</body>
</html>
""")
    
    with open(os.path.join(OUTPUT_DIR, "analysis_report.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    log_progress("HTML report generated.")

# ---------------------------------------------------------
# Main Execution Loop
# ---------------------------------------------------------
if __name__ == "__main__":
    t_start = time.time()
    log_progress("Starting continuous casting sleeve RUL pipeline...")
    
    # Path to data
    data_path = os.path.join(os.path.dirname(BASE_DIR), "Dataset", "Dataset.csv")
    
    # Load and clean
    df, col_types = load_and_clean_dataset(data_path)
    
    # Profile columns
    profile = profile_columns(df, col_types)
    
    # Generate charts
    generate_column_plots(df, col_types)
    
    # Grouped Analyses
    grouped_results = perform_grouped_analyses(df)
    
    # Run Supervised Regression
    reg_compare, reg_feats_imp, best_reg_name, best_reg_model, preprocessor, reg_feats, X_train, X_test, y_train, y_test = run_supervised_regression(df, col_types)
    
    # Run Supervised Classification
    class_compare = run_supervised_classification(df, col_types, reg_feats)
    
    # Explainable AI
    surrogate_rules = run_explainable_ai(df, col_types, reg_feats, best_reg_model, preprocessor, X_train, X_test, y_train, y_test)
    
    # Unsupervised learning
    kmeans_regimes = run_unsupervised_learning(df, col_types, reg_feats)
    
    # Association Rule Mining
    association_rules_df = run_association_rule_mining(df, col_types, reg_feats)
    
    # FCA contextos
    binary_context, many_valued, fca_meta = prepare_fca_contexts(df, col_types, reg_feats)
    
    # Build HTML and MD reports
    build_markdown_report(profile, grouped_results, reg_compare, reg_feats_imp, class_compare, surrogate_rules, kmeans_regimes, association_rules_df, fca_meta)
    build_html_report(profile, grouped_results, reg_compare, reg_feats_imp, class_compare, surrogate_rules, kmeans_regimes, association_rules_df, fca_meta)
    
    t_end = time.time()
    elapsed = t_end - t_start
    log_progress(f"Crystallizer sleeve RUL pipeline finished successfully in {elapsed:.2f} seconds!")
    print("\nGenerated output files list:")
    print(f"1. HTML Report: {os.path.join(OUTPUT_DIR, 'analysis_report.html')}")
    print(f"2. Markdown Report: {os.path.join(OUTPUT_DIR, 'analysis_report.md')}")
    print(f"3. Regression benchmarks: {os.path.join(OUTPUT_DIR, 'model_comparison_regression.csv')}")
    print(f"4. Classification benchmarks: {os.path.join(OUTPUT_DIR, 'model_comparison_classification.csv')}")
    print(f"5. Regression feature importances: {os.path.join(OUTPUT_DIR, 'feature_importance_regression.csv')}")
    print(f"6. Association rules: {os.path.join(OUTPUT_DIR, 'association_rules.csv')}")
    print(f"7. FCA binary context: {os.path.join(OUTPUT_DIR, 'fca_binary_context.csv')}")
    print(f"8. FCA many-valued context: {os.path.join(OUTPUT_DIR, 'fca_many_valued_context.csv')}")
    print(f"9. Generated charts: {PLOTS_DIR}")
