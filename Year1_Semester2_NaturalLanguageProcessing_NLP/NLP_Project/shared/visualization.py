import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import pandas as pd
import numpy as np

def plot_confusion_matrix(y_true, y_pred, class_names, output_dir: str, file_name: str = "confusion_matrix.png"):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, file_name), bbox_inches='tight')
    plt.close()

def plot_roc_curve(y_true, y_probs, output_dir: str, file_name: str = "roc_curve.png", class_names=None):
    plt.figure(figsize=(8, 6))
    if len(y_probs.shape) == 1 or y_probs.shape[1] == 2:
        # Binary
        probs = y_probs if len(y_probs.shape) == 1 else y_probs[:, 1]
        fpr, tpr, _ = roc_curve(y_true, probs)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    else:
        # Multi-class OvR
        from sklearn.preprocessing import label_binarize
        y_true_bin = label_binarize(y_true, classes=range(y_probs.shape[1]))
        for i in range(y_probs.shape[1]):
            fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_probs[:, i])
            roc_auc = auc(fpr, tpr)
            label_name = class_names[i] if class_names else f'Class {i}'
            plt.plot(fpr, tpr, lw=2, label=f'{label_name} (area = {roc_auc:.2f})')
            
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, file_name), bbox_inches='tight')
    plt.close()

def plot_training_history(train_losses, val_losses, output_dir: str, file_name: str = "training_history.png"):
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training History')
    plt.legend()
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, file_name), bbox_inches='tight')
    plt.close()

def plot_model_comparison(comparison_df: pd.DataFrame, metrics: list, output_dir: str, file_name: str = "metric_barplots.png"):
    df_melted = comparison_df.melt(id_vars=['Model'], value_vars=metrics, var_name='Metric', value_name='Score')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df_melted, x='Metric', y='Score', hue='Model')
    plt.title('Model Comparison')
    plt.ylim(0, 1.05)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, file_name), bbox_inches='tight')
    plt.close()
