import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score

def compute_classification_metrics(y_true, y_pred, y_probs=None, average='weighted', is_multiclass=False):
    """Computes precision, recall, F1, accuracy, and conditionally ROC-AUC."""
    acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average=average, zero_division=0)
    
    metrics = {
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
    
    if is_multiclass:
        # Add macro F1 for multi-class
        _, _, f1_macro, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
        metrics['f1_macro'] = f1_macro
        
        if y_probs is not None:
            try:
                roc_auc = roc_auc_score(y_true, y_probs, multi_class='ovr', average='weighted')
                metrics['roc_auc'] = roc_auc
            except Exception:
                pass
    else:
        if y_probs is not None:
            try:
                roc_auc = roc_auc_score(y_true, y_probs[:, 1])
                metrics['roc_auc'] = roc_auc
            except Exception:
                pass
                
    return metrics
