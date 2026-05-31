"""
train_bert.py
=============
Fine-tune ``dumitrescustefan/bert-base-romanian-cased-v1`` on the Romanian articles dataset.

This script is designed to be run from the command line as a standalone
process — not inside a Jupyter notebook.

Usage
-----
    python train_bert.py

Resumability
------------
If ``checkpoints/bert_romanian/config.json`` already exists, training is skipped
and the script goes straight to test-set evaluation. Delete the checkpoint
directory to force retraining.

Device
------
Automatically uses Apple MPS (Metal Performance Shaders) on Apple Silicon,
falling back to CUDA if available, then CPU. No fp16 is used — MPS operates
in float32 natively and manages precision internally.

Outputs
-------
- ``checkpoints/bert_romanian/``      Best model checkpoint + tokenizer
- ``data/preprocessed_ro_*.pkl`` Cached preprocessed texts (speeds up re-runs)
- ``results/bert_romanian_metrics.json`` Accuracy, precision, recall, F1 on test set
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from torch.utils.data import DataLoader, Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)
# Add project root and shared/migrated/language-shared to path so we can load modules
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "shared" / "migrated"))
sys.path.insert(0, str(project_root / "2_Romanian" / "shared"))

from train_utils import (
    select_hardware_device,
    TextClassificationDataset,
    compute_classification_metrics as compute_metrics,
)
from dataset_ro import load_splits, load_preprocessed, save_preprocessed
from preprocessing_ro import preprocess_batch

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CONFIG = {
    # Model
    "bert_model_name": "dumitrescustefan/bert-base-romanian-cased-v1",
    "max_length": 256,                # max tokens; sequences longer than this are truncated
    "batch_size": 16,
    "eval_batch_size": 32,

    # Training
    "learning_rate": 2e-5,
    "weight_decay": 0.01,
    "num_epochs": 5,
    "warmup_ratio": 0.06,             # ~6% of total steps used for LR warm-up
    "early_stopping_patience": 2,     # stop if val-F1 doesn't improve for 2 epochs
    "num_frozen_layers": 4,           # Freeze bottom N (out of 12) BERT layers to prevent overfitting
    "random_seed": 42,

    # Dataset splits
    "train_ratio": 0.70,
    "val_ratio": 0.15,
    "test_ratio": 0.15,

    # Paths
    "checkpoint_dir": project_root / "checkpoints" / "bert_romanian",
    "results_dir": Path(__file__).resolve().parent / "Results",
}




# ---------------------------------------------------------------------------
# Preprocessing with caching
# ---------------------------------------------------------------------------

def get_preprocessed_texts(
    df_train, df_val, df_test
) -> tuple[list[str], list[str], list[str]]:
    """Return preprocessed texts for each split, using disk cache if available.

    Preprocessing is CPU-bound and takes less than a minute. The
    results are pickled to ``data/preprocessed_{split}.pkl`` so subsequent
    runs skip it entirely.
    """
    result = []
    for split_name, df in [("train", df_train), ("val", df_val), ("test", df_test)]:
        cached = load_preprocessed(split_name)
        if cached is not None:
            result.append(cached)
        else:
            print(f"[train_bert] Preprocessing {split_name} set ({len(df):,} articles)…")
            texts = preprocess_batch(df["article"].tolist())
            save_preprocessed(texts, split_name)
            result.append(texts)
    return tuple(result)


# ---------------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------------

def tokenize_split(tokenizer, texts: list[str], max_length: int) -> dict:
    """Tokenize a list of texts.

    Uses ``truncation=True`` but does NOT pad here — padding is handled
    dynamically per-batch by ``DataCollatorWithPadding``, which is far more
    memory-efficient than padding all sequences to ``max_length`` upfront.

    Args:
        tokenizer:  A loaded HuggingFace tokenizer.
        texts:      List of preprocessed text strings.
        max_length: Maximum number of tokens; longer sequences are truncated.

    Returns:
        Dict with ``input_ids`` and ``attention_mask`` as Python lists.
    """
    return tokenizer(
        texts,
        padding=False,          # dynamic padding handled by DataCollatorWithPadding
        truncation=True,
        max_length=max_length,
        return_tensors=None,    # plain lists; RomanianArticlesDataset wraps them in tensors
    )


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate_on_test(model, test_dataset, tokenizer, device, config) -> dict:
    """Run inference on the test set and return a metrics dict.

    Uses a plain PyTorch DataLoader rather than the HF Trainer so that we
    can run evaluation independently of a training run.

    Returns:
        Dict with keys: accuracy, precision, recall, f1.
    """
    collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")
    loader = DataLoader(
        test_dataset,
        batch_size=config["eval_batch_size"],
        collate_fn=collator,
    )

    model.eval()
    all_preds, all_labels = [], []

    with torch.no_grad():
        for batch in loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            token_type_ids = batch.get("token_type_ids")
            if token_type_ids is not None:
                token_type_ids = token_type_ids.to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )
            preds = torch.argmax(outputs.logits, dim=-1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(batch["labels"].numpy())

    metrics = {
        "accuracy": float(accuracy_score(all_labels, all_preds)),
        "precision": float(precision_score(all_labels, all_preds, average="macro")),
        "recall": float(recall_score(all_labels, all_preds, average="macro")),
        "f1": float(f1_score(all_labels, all_preds, average="macro")),
    }
    return metrics, all_labels, all_preds


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 65)
    print("BERT Fine-Tuning — Romanian BERT on Romanian Articles")
    print("=" * 65)

    # ── Device ──────────────────────────────────────────────────────────
    device = select_hardware_device()
    print(f"Device : {device}")

    # ── Reproducibility ──────────────────────────────────────────────────
    import random
    seed = CONFIG["random_seed"]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    # ── Paths ────────────────────────────────────────────────────────────
    ckpt_dir = CONFIG["checkpoint_dir"]
    results_dir = CONFIG["results_dir"]
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    # ── Data ─────────────────────────────────────────────────────────────
    df_train, df_val, df_test = load_splits(
        seed=seed,
        train_ratio=CONFIG["train_ratio"],
        val_ratio=CONFIG["val_ratio"],
        test_ratio=CONFIG["test_ratio"],
    )
    train_labels = df_train["label"].tolist()
    val_labels = df_val["label"].tolist()
    test_labels = df_test["label"].tolist()

    # ── Preprocessing ────────────────────────────────────────────────────
    train_texts, val_texts, test_texts = get_preprocessed_texts(df_train, df_val, df_test)

    # ── Tokenizer ────────────────────────────────────────────────────────
    print(f"\n[train_bert] Loading tokenizer: {CONFIG['bert_model_name']}")
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["bert_model_name"])
    collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")

    # ── Check for existing checkpoint ────────────────────────────────────
    has_checkpoint = any(ckpt_dir.glob("config.json"))

    if has_checkpoint:
        print(f"\n✅ Checkpoint found at '{ckpt_dir}' — skipping training.")
        model = AutoModelForSequenceClassification.from_pretrained(str(ckpt_dir))
        model.to(device)
    else:
        print("\n[train_bert] No checkpoint found. Tokenizing and training…")

        train_enc = tokenize_split(tokenizer, train_texts, CONFIG["max_length"])
        val_enc = tokenize_split(tokenizer, val_texts, CONFIG["max_length"])
        test_enc = tokenize_split(tokenizer, test_texts, CONFIG["max_length"])

        train_dataset = TextClassificationDataset(train_enc, train_labels)
        val_dataset = TextClassificationDataset(val_enc, val_labels)
        test_dataset = TextClassificationDataset(test_enc, test_labels)

        print(f"  Train : {len(train_dataset):,} samples")
        print(f"  Val   : {len(val_dataset):,} samples")
        print(f"  Test  : {len(test_dataset):,} samples")

        # Instantiate model
        model = AutoModelForSequenceClassification.from_pretrained(
            CONFIG["bert_model_name"],
            num_labels=3,
            id2label={0: "negative", 1: "positive", 2: "neutral"},
            label2id={"negative": 0, "positive": 1, "neutral": 2},
        )
        model.to(device)

        # Freeze the bottom layers to prevent overfitting
        num_frozen = CONFIG.get("num_frozen_layers", 0)
        if num_frozen > 0:
            print(f"[train_bert] Freezing embeddings and first {num_frozen} transformer layers…")
            for param in model.bert.embeddings.parameters():
                param.requires_grad = False
            for i in range(min(num_frozen, len(model.bert.encoder.layer))):
                for param in model.bert.encoder.layer[i].parameters():
                    param.requires_grad = False

        # Training arguments
        # Note: fp16 is disabled — MPS uses float32; bf16 is not set to keep
        # compatibility across MPS, CUDA, and CPU without extra flags.
        training_args = TrainingArguments(
            output_dir=str(ckpt_dir),
            num_train_epochs=CONFIG["num_epochs"],
            per_device_train_batch_size=CONFIG["batch_size"],
            per_device_eval_batch_size=CONFIG["eval_batch_size"],
            learning_rate=CONFIG["learning_rate"],
            weight_decay=CONFIG["weight_decay"],
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            greater_is_better=True,
            logging_steps=100,
            seed=seed,
            fp16=False,       # MPS does not support fp16 via Trainer
            report_to="none",
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            processing_class=tokenizer,
            data_collator=collator,
            compute_metrics=compute_metrics,
            callbacks=[
                EarlyStoppingCallback(
                    early_stopping_patience=CONFIG["early_stopping_patience"]
                )
            ],
        )

        t0 = time.time()
        trainer.train()
        elapsed = time.time() - t0
        print(f"\n[train_bert] Training complete in {elapsed / 60:.1f} min.")

        # Persist best model + tokenizer for later use by evaluate / explain scripts
        trainer.save_model(str(ckpt_dir))
        tokenizer.save_pretrained(str(ckpt_dir))
        print(f"[train_bert] Best model saved → {ckpt_dir}")

    # ── Test-set evaluation ──────────────────────────────────────────────
    print("\n[train_bert] Evaluating on test set…")

    # Tokenize test set (needed whether we trained or loaded from checkpoint)
    test_enc = tokenize_split(tokenizer, test_texts, CONFIG["max_length"])
    test_dataset = TextClassificationDataset(test_enc, test_labels)

    metrics, all_labels, all_preds = evaluate_on_test(
        model, test_dataset, tokenizer, device, CONFIG
    )

    print("\n── BERT Test-Set Metrics ─────────────────────────────────")
    for k, v in metrics.items():
        print(f"  {k:<12}: {v:.4f}")
    print()
    print(classification_report(all_labels, all_preds, target_names=["negative", "positive", "neutral"]))

    # ── Save metrics to JSON ─────────────────────────────────────────────
    out_path = results_dir / "bert_romanian_metrics.json"
    with open(out_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[train_bert] Metrics saved → {out_path}")


if __name__ == "__main__":
    main()
