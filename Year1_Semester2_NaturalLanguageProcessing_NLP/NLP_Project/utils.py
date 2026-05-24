import os
import random
import json
import logging
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
import seaborn as sns
from lime.lime_text import LimeTextExplainer
import shap

def set_seed(seed: int = 42):
    """Sets seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def load_csv(path: str, text_col: str, label_col: str, sample_size: int = None):
    """Loads CSV and handles missing values."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    if text_col not in df.columns or label_col not in df.columns:
        raise ValueError(f"Columns {text_col} and/or {label_col} not found in the dataset.")
    df = df.dropna(subset=[text_col, label_col])
    if sample_size and sample_size > 0:
        df = df.sample(n=min(sample_size, len(df)), random_state=42)
    return df

def split_dataset(df: pd.DataFrame, text_col: str, label_col: str, test_size=0.2, val_size=0.1):
    """Splits dataset into train, val, test."""
    texts = df[text_col].tolist()
    labels = df[label_col].tolist()
    
    # Train + Val / Test split
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=test_size, random_state=42, stratify=labels
    )
    
    # Train / Val split
    val_ratio = val_size / (1.0 - test_size)
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_texts, train_labels, test_size=val_ratio, random_state=42, stratify=train_labels
    )
    
    return train_texts, val_texts, test_texts, train_labels, val_labels, test_labels

def compute_metrics(y_true, y_pred, average='weighted'):
    """Computes standard classification metrics."""
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average=average, zero_division=0)
    return {
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

def save_metrics(metrics: dict, output_dir: str, file_name: str = "metrics.json"):
    """Saves metrics dictionary to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=4)

def plot_confusion_matrix(y_true, y_pred, class_names, output_dir: str, file_name: str = "confusion_matrix.png"):
    """Plots and saves confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, file_name))
    plt.close()

def build_lime_explainer(class_names):
    """Returns a LimeTextExplainer instance."""
    return LimeTextExplainer(class_names=class_names)

def run_lime_explanations(explainer, predict_proba_fn, texts, num_samples, output_dir, file_prefix="lime"):
    """Runs LIME and saves HTML reports."""
    os.makedirs(output_dir, exist_ok=True)
    for i, text in enumerate(texts[:num_samples]):
        # Predict Proba function expected to take a list of strings and return a numpy array of shape (len(list), num_classes)
        try:
            exp = explainer.explain_instance(text, predict_proba_fn, num_features=10)
            exp.save_to_file(os.path.join(output_dir, f"{file_prefix}_{i}.html"))
        except Exception as e:
            print(f"Failed to generate LIME explanation for sample {i}: {e}")

def run_shap_explanations(predict_proba_fn, texts, num_samples, output_dir, file_prefix="shap"):
    """Runs SHAP and saves plots."""
    os.makedirs(output_dir, exist_ok=True)
    try:
        # Create an explainer with the predict probability function
        explainer = shap.Explainer(predict_proba_fn, shap.maskers.Text(tokenizer=r"\W+"))
        # Explain the subset of texts
        shap_values = explainer(texts[:num_samples])
        
        # Plotting the SHAP values (Summary or Waterfall)
        # We will save a summary plot if applicable or just text plots
        # shap.plots.text is interactive, we will try to save a bar plot
        plt.figure()
        shap.plots.bar(shap_values, show=False)
        plt.savefig(os.path.join(output_dir, f"{file_prefix}_bar.png"), bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Failed to generate SHAP explanations: {e}")
