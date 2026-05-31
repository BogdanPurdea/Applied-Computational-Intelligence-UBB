"""
train_utils.py
==============
Shared utilities and dataset definitions for training transformer models.
"""

from __future__ import annotations

import numpy as np
import torch
from torch.utils.data import Dataset
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    hamming_loss,
    precision_score,
    recall_score,
)

def select_hardware_device(verbose: bool = True) -> torch.device:
    """Return the best available torch device for this machine."""
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        name = "Apple Silicon MPS"
    elif torch.cuda.is_available():
        device = torch.device("cuda")
        name = "NVIDIA CUDA"
    else:
        device = torch.device("cpu")
        name = "CPU (Note: Training will be slow)"
    
    if verbose:
        print(f"Hardware device confirmed: {name}")
    return device

class TextClassificationDataset(Dataset):
    """Wraps tokenized text encodings for sequence classification in PyTorch/Hugging Face.

    Supports both single-label and multi-label classifications.
    """
    def __init__(self, encodings: dict, labels: list[int] | np.ndarray) -> None:
        self.encodings = encodings
        if isinstance(labels, np.ndarray):
            self.labels = labels.astype(np.float32)
        else:
            self.labels = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> dict:
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if isinstance(self.labels, np.ndarray):
            item["labels"] = torch.tensor(self.labels[idx], dtype=torch.float)
        else:
            item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

def compute_classification_metrics(eval_pred) -> dict[str, float]:
    """Compute standard single-label classification metrics (accuracy, F1, precision, recall).
    
    Supports both binary and multi-class classification.
    """
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, preds)
    
    num_classes = logits.shape[-1]
    if num_classes > 2:
        # Multi-class
        f1 = f1_score(labels, preds, average="macro", zero_division=0)
        return {"accuracy": float(acc), "f1": float(f1)}
    else:
        # Binary
        precision = precision_score(labels, preds, average="binary", zero_division=0)
        recall = recall_score(labels, preds, average="binary", zero_division=0)
        f1 = f1_score(labels, preds, average="binary", zero_division=0)
        return {
            "accuracy": float(acc),
            "f1": float(f1),
            "precision": float(precision),
            "recall": float(recall),
        }

def compute_multilabel_metrics(eval_pred, default_threshold: float = 0.5) -> dict[str, float]:
    """Compute multi-label metrics (micro-F1, macro-F1, hamming loss) using a threshold."""
    logits, labels = eval_pred
    probs = 1.0 / (1.0 + np.exp(-logits))
    preds = (probs >= default_threshold).astype(int)
    labels_int = labels.astype(int)

    micro = f1_score(labels_int, preds, average="micro", zero_division=0)
    macro = f1_score(labels_int, preds, average="macro", zero_division=0)
    hl = hamming_loss(labels_int, preds)
    return {
        "micro_f1": float(micro),
        "macro_f1": float(macro),
        "hamming": float(hl),
    }
