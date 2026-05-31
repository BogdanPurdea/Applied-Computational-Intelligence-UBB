"""
train_sbert.py
==============
Fine-tune a SentenceTransformer model (using sequence classification) on the IMDB dataset.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import torch
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
# Add project root and shared/migrated/language-shared to path so we can load modules
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "shared" / "migrated"))
sys.path.insert(0, str(project_root / "1_English" / "shared"))

from train_utils import (
    select_hardware_device,
    TextClassificationDataset,
    compute_classification_metrics as compute_metrics,
)
from dataset_en import load_splits, load_preprocessed, save_preprocessed
from preprocessing_en import preprocess_batch

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CONFIG = {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "max_length": 128,
    "batch_size": 16,
    "epochs": 3,
    "random_seed": 42,
    "train_ratio": 0.70,
    "val_ratio": 0.15,
    "test_ratio": 0.15,
    
    # Paths
    "checkpoint_dir": project_root / "checkpoints" / "sentencebert",
    "output_dir": project_root / "checkpoints" / "sentencebert_training_results",
}



# ---------------------------------------------------------------------------
# Preprocessing Helper with Disk Caching
# ---------------------------------------------------------------------------

def get_preprocessed_texts(df_train, df_val, df_test):
    result = []
    for split_name, df in [("train", df_train), ("val", df_val), ("test", df_test)]:
        cached = load_preprocessed(split_name)
        if cached is not None:
            result.append(cached)
        else:
            print(f"Preprocessing {split_name} ({len(df):,} reviews)…")
            texts = preprocess_batch(df["review"].tolist())
            save_preprocessed(texts, split_name)
            result.append(texts)
    return tuple(result)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 65)
    print("SentenceTransformer Fine-Tuning (Sequence Classification) — IMDB")
    print("=" * 65)

    # ── Device selection ──────────────────────────────────────────────────
    device = select_hardware_device()

    # ── Paths ────────────────────────────────────────────────────────────
    output_dir = CONFIG["output_dir"]
    checkpoint_dir = CONFIG["checkpoint_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # ── Load Data ────────────────────────────────────────────────────────
    print("Loading dataset splits...")
    df_train, df_val, df_test = load_splits(
        seed=CONFIG["random_seed"],
        train_ratio=CONFIG["train_ratio"],
        val_ratio=CONFIG["val_ratio"],
        test_ratio=CONFIG["test_ratio"]
    )

    # Output summary
    print("\n========== Dataset Split Summary ==========")
    print(f"Training records ({int(CONFIG['train_ratio']*100)}%): {len(df_train)}")
    print(f"Validation records ({int(CONFIG['val_ratio']*100)}%): {len(df_val)}")
    print(f"Testing records ({int(CONFIG['test_ratio']*100)}%): {len(df_test)}")
    print("===========================================\n")

    # ── Preprocess ───────────────────────────────────────────────────────
    print("Preprocessing reviews...")
    train_texts, val_texts, _ = get_preprocessed_texts(df_train, df_val, df_test)

    train_labels = df_train["label"].tolist()
    val_labels = df_val["label"].tolist()

    # ── Tokenize ─────────────────────────────────────────────────────────
    model_name = CONFIG["model_name"]
    max_length = CONFIG["max_length"]

    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print("Tokenizing text data...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=max_length)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=max_length)

    train_dataset = TextClassificationDataset(train_encodings, train_labels)
    val_dataset = TextClassificationDataset(val_encodings, val_labels)

    # ── Model Init ───────────────────────────────────────────────────────
    print("Initializing model...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.to(device)

    # ── Training Arguments ───────────────────────────────────────────────
    training_args = TrainingArguments(
        output_dir=str(output_dir / "sentencebert_training_results"),
        num_train_epochs=CONFIG["epochs"],
        per_device_train_batch_size=CONFIG["batch_size"],
        per_device_eval_batch_size=CONFIG["batch_size"],
        learning_rate=2e-5,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        fp16=(device.type == "cuda"),
        dataloader_num_workers=0,
        gradient_accumulation_steps=1,
        logging_steps=100,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    # ── Training ─────────────────────────────────────────────────────────
    print("Beginning training...")
    trainer.train()

    # ── Save ─────────────────────────────────────────────────────────────
    print(f"\nSaving fine-tuned model and tokenizer to {checkpoint_dir}...")
    trainer.save_model(str(checkpoint_dir))
    tokenizer.save_pretrained(str(checkpoint_dir))

    print("\nProcess finished successfully. Model saved.")


if __name__ == "__main__":
    main()
