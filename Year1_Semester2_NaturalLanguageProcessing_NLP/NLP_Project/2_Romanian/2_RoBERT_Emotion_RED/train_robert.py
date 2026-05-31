"""
train_robert.py
===============
Fine-tune ``readerbench/RoBERT-base`` on the REDv2 Romanian Emotion Dataset
for **multi-label emotion classification**.

Task
----
Given a Romanian social-media text, predict which of 7 emotions are expressed:
    Sadness · Surprise · Fear · Anger · Neutral · Trust · Joy

Each emotion is predicted independently (binary), so a single text can carry
multiple emotions simultaneously.  The model head uses BCEWithLogitsLoss
(selected automatically by HuggingFace when ``problem_type="multi_label_classification"``).

Usage
-----
    python train_robert.py

Resumability
------------
If ``checkpoints/robert_red/config.json`` already exists, training is skipped
and the script goes straight to threshold search + test-set evaluation.
Delete the checkpoint directory to force retraining.

Device
------
Automatically prefers Apple MPS → CUDA → CPU.  fp16 is disabled for MPS
compatibility; the model trains in float32.

Outputs
-------
- ``checkpoints/robert_red/``         Best model checkpoint + tokenizer
- ``data/red/preprocessed_red_*.pkl`` Cached preprocessed texts (per split)
- ``results/robert_red_metrics.json`` Per-label F1, aggregate metrics, optimal thresholds
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import (
    classification_report,
    f1_score,
    hamming_loss,
    precision_score,
    recall_score,
)
from torch.utils.data import DataLoader
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
    compute_multilabel_metrics,
)
from dataset_red import (
    AGREED_LABEL_COLS,
    EMOTION_LABELS,
    load_preprocessed,
    load_splits,
    save_preprocessed,
)
from preprocessing_red import preprocess_batch_red

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CONFIG = {
    # Model
    "bert_model_name":         "readerbench/RoBERT-base",
    "max_length":              128,      # REDv2 texts are short (mean 23 words, p95 46)
    "batch_size":              16,
    "eval_batch_size":         32,

    # Training
    "learning_rate":           2e-5,
    "weight_decay":            0.01,
    "num_epochs":              5,
    "warmup_ratio":            0.06,     # ~6 % of steps used for LR warm-up
    "early_stopping_patience": 2,        # stop if val macro-F1 doesn't improve for 2 epochs
    "num_frozen_layers":       4,        # freeze bottom N (of 12) BERT layers

    # Inference
    "threshold_search_steps":  81,       # linspace(0.1, 0.9, 81) per label
    "default_threshold":       0.5,      # used inside compute_metrics during training

    # Misc
    "random_seed":             42,
    "task":                    "classification",

    # Paths
    "checkpoint_dir":          project_root / "checkpoints" / "robert_red",
    "results_dir":             Path(__file__).resolve().parent / "Results",
}


# ---------------------------------------------------------------------------
# Device
# ---------------------------------------------------------------------------

def compute_metrics(eval_pred):
    return compute_multilabel_metrics(eval_pred, default_threshold=CONFIG["default_threshold"])


# ---------------------------------------------------------------------------
# Preprocessing with caching
# ---------------------------------------------------------------------------

def get_preprocessed_texts(
    df_train, df_val, df_test
) -> tuple[
    tuple[list[str], np.ndarray],
    tuple[list[str], np.ndarray],
    tuple[list[str], np.ndarray],
]:
    """Preprocess and cache texts for each split.

    Applies the full ``preprocessing_red`` pipeline (including deduplication)
    and synchronises label arrays with the returned ``kept_indices``.

    Returns:
        Three ``(texts, labels)`` tuples for train, val, test respectively.
        ``labels`` is a float32 NumPy array of shape ``(N, 7)``.
    """
    results = []
    for split_name, df in [("train", df_train), ("val", df_val), ("test", df_test)]:
        raw_labels = df[AGREED_LABEL_COLS].values.astype(np.float32)  # (N, 7)

        cached = load_preprocessed(split_name)
        if cached is not None:
            # Cache stores only deduplicated texts; we must also filter labels.
            # We detect the kept count from cache length and re-run dedup index
            # computation only if a mismatch exists.
            if len(cached) == len(raw_labels):
                # No deduplication occurred (or labels already filtered)
                results.append((cached, raw_labels))
            else:
                # Rare: labels not yet trimmed — recompute kept indices
                print(
                    f"[train_robert] Cache length mismatch for '{split_name}' "
                    f"({len(cached)} texts vs {len(raw_labels)} label rows). "
                    f"Recomputing kept indices…"
                )
                from preprocessing_red import preprocess, remove_duplicates
                cleaned_raw = [preprocess(t) for t in df["text"].tolist()]
                _, kept = remove_duplicates(cleaned_raw)
                results.append((cached, raw_labels[kept]))
        else:
            print(
                f"[train_robert] Preprocessing '{split_name}' "
                f"({len(df):,} texts)…"
            )
            texts, kept = preprocess_batch_red(df["text"].tolist(), verbose=(split_name == "train"))
            save_preprocessed(texts, split_name)
            results.append((texts, raw_labels[kept]))

    return results[0], results[1], results[2]


# ---------------------------------------------------------------------------
# Tokenisation
# ---------------------------------------------------------------------------

def tokenize_split(tokenizer, texts: list[str], max_length: int) -> dict:
    """Tokenise a list of texts without padding (dynamic padding per batch).

    Args:
        tokenizer:  A loaded HuggingFace tokenizer.
        texts:      List of preprocessed text strings.
        max_length: Maximum token count; longer sequences are truncated.

    Returns:
        Dict with ``input_ids`` and ``attention_mask`` as Python lists.
    """
    return tokenizer(
        texts,
        padding=False,
        truncation=True,
        max_length=max_length,
        return_tensors=None,
    )


# ---------------------------------------------------------------------------
# Per-label threshold search on the validation set
# ---------------------------------------------------------------------------

def find_optimal_thresholds(
    model,
    val_dataset: TextClassificationDataset,
    tokenizer,
    device: torch.device,
    config: dict,
) -> np.ndarray:
    """Search for the per-label sigmoid threshold that maximises each label's F1.

    Runs a single inference pass over the validation set, then sweeps
    ``linspace(0.1, 0.9, threshold_search_steps)`` per label independently.

    Args:
        model:       Fine-tuned model (already on ``device``).
        val_dataset: Validation REDDataset instance.
        tokenizer:   Matching tokenizer (for DataCollatorWithPadding).
        device:      Torch device.
        config:      The global CONFIG dict.

    Returns:
        NumPy array of shape ``(7,)`` with the optimal threshold per label.
    """
    print("\n[train_robert] Searching per-label optimal thresholds on validation set…")

    collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")
    loader   = DataLoader(
        val_dataset,
        batch_size=config["eval_batch_size"],
        collate_fn=collator,
        shuffle=False,
    )

    model.eval()
    all_logits: list[np.ndarray] = []
    all_labels: list[np.ndarray] = []

    with torch.no_grad():
        for batch in loader:
            input_ids      = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            token_type_ids = batch.get("token_type_ids")
            if token_type_ids is not None:
                token_type_ids = token_type_ids.to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )
            all_logits.append(outputs.logits.cpu().numpy())
            all_labels.append(batch["labels"].numpy())

    logits_arr = np.concatenate(all_logits, axis=0)   # (N_val, 7)
    labels_arr = np.concatenate(all_labels, axis=0).astype(int)  # (N_val, 7)
    probs_arr  = torch.sigmoid(torch.tensor(logits_arr)).numpy()

    candidates = np.linspace(0.1, 0.9, config["threshold_search_steps"])
    best_thresholds = np.full(len(EMOTION_LABELS), config["default_threshold"])

    for label_idx, emotion in enumerate(EMOTION_LABELS):
        label_true = labels_arr[:, label_idx]
        best_f1, best_t = -1.0, config["default_threshold"]
        for t in candidates:
            preds = (probs_arr[:, label_idx] >= t).astype(int)
            f1 = f1_score(label_true, preds, zero_division=0)
            if f1 > best_f1:
                best_f1, best_t = f1, t
        best_thresholds[label_idx] = best_t
        print(f"  {emotion:<10}  best_t={best_t:.2f}  val_F1={best_f1:.4f}")

    return best_thresholds


# ---------------------------------------------------------------------------
# Test-set evaluation
# ---------------------------------------------------------------------------

def evaluate_on_test(
    model,
    test_dataset: TextClassificationDataset,
    tokenizer,
    device: torch.device,
    thresholds: np.ndarray,
    config: dict,
) -> tuple[dict, np.ndarray, np.ndarray]:
    """Run inference on the test set using per-label thresholds.

    Args:
        model:        Fine-tuned model.
        test_dataset: Test REDDataset instance.
        tokenizer:    Matching tokenizer.
        device:       Torch device.
        thresholds:   Per-label thresholds from ``find_optimal_thresholds``.
        config:       Global CONFIG dict.

    Returns:
        ``(metrics_dict, all_labels, all_preds)``
    """
    collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")
    loader   = DataLoader(
        test_dataset,
        batch_size=config["eval_batch_size"],
        collate_fn=collator,
        shuffle=False,
    )

    model.eval()
    all_logits: list[np.ndarray] = []
    all_labels: list[np.ndarray] = []

    with torch.no_grad():
        for batch in loader:
            input_ids      = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            token_type_ids = batch.get("token_type_ids")
            if token_type_ids is not None:
                token_type_ids = token_type_ids.to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
            )
            all_logits.append(outputs.logits.cpu().numpy())
            all_labels.append(batch["labels"].numpy())

    logits_arr = np.concatenate(all_logits, axis=0)
    labels_arr = np.concatenate(all_labels, axis=0).astype(int)
    probs_arr  = torch.sigmoid(torch.tensor(logits_arr)).numpy()

    # Apply per-label thresholds
    preds_arr = np.zeros_like(probs_arr, dtype=int)
    for i, t in enumerate(thresholds):
        preds_arr[:, i] = (probs_arr[:, i] >= t).astype(int)

    micro = f1_score(labels_arr, preds_arr, average="micro", zero_division=0)
    macro = f1_score(labels_arr, preds_arr, average="macro", zero_division=0)
    hl    = hamming_loss(labels_arr, preds_arr)

    # Per-label metrics
    per_label: dict[str, dict] = {}
    for i, emotion in enumerate(EMOTION_LABELS):
        per_label[emotion] = {
            "precision": float(precision_score(labels_arr[:, i], preds_arr[:, i], zero_division=0)),
            "recall":    float(recall_score(labels_arr[:, i], preds_arr[:, i], zero_division=0)),
            "f1":        float(f1_score(labels_arr[:, i], preds_arr[:, i], zero_division=0)),
            "support":   int(labels_arr[:, i].sum()),
            "threshold": float(thresholds[i]),
        }

    metrics = {
        "micro_f1":    float(micro),
        "macro_f1":    float(macro),
        "hamming_loss": float(hl),
        "thresholds":  {e: float(thresholds[i]) for i, e in enumerate(EMOTION_LABELS)},
        "per_label":   per_label,
    }
    return metrics, labels_arr, preds_arr


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 65)
    print("RoBERT-base Fine-Tuning — REDv2 Multi-Label Emotion Classification")
    print("=" * 65)

    # ── Device & reproducibility ─────────────────────────────────────────
    device = select_hardware_device()
    print(f"Device : {device}")

    seed = CONFIG["random_seed"]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    # ── Paths ────────────────────────────────────────────────────────────
    ckpt_dir    = CONFIG["checkpoint_dir"]
    results_dir = CONFIG["results_dir"]
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    # ── Data ─────────────────────────────────────────────────────────────
    df_train, df_val, df_test = load_splits(task=CONFIG["task"])

    # ── Preprocessing + deduplication ────────────────────────────────────
    (train_texts, train_labels), \
    (val_texts,   val_labels),   \
    (test_texts,  test_labels) = get_preprocessed_texts(df_train, df_val, df_test)

    print(
        f"\n[train_robert] Dataset sizes after preprocessing:"
        f"\n  Train : {len(train_texts):,} samples"
        f"\n  Val   : {len(val_texts):,} samples"
        f"\n  Test  : {len(test_texts):,} samples"
    )

    # ── Tokenizer ────────────────────────────────────────────────────────
    print(f"\n[train_robert] Loading tokenizer: {CONFIG['bert_model_name']}")
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["bert_model_name"])
    collator  = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")

    # ── Check for existing checkpoint ────────────────────────────────────
    has_checkpoint = (ckpt_dir / "config.json").exists()

    if has_checkpoint:
        print(f"\n✅  Checkpoint found at '{ckpt_dir}' — skipping training.")
        model = AutoModelForSequenceClassification.from_pretrained(str(ckpt_dir))
        model.to(device)
    else:
        print("\n[train_robert] No checkpoint found. Tokenising and training…")

        train_enc = tokenize_split(tokenizer, train_texts, CONFIG["max_length"])
        val_enc   = tokenize_split(tokenizer, val_texts,   CONFIG["max_length"])

        train_dataset = TextClassificationDataset(train_enc, train_labels)
        val_dataset   = TextClassificationDataset(val_enc,   val_labels)

        # ── Model ────────────────────────────────────────────────────────
        id2label = {i: e for i, e in enumerate(EMOTION_LABELS)}
        label2id = {e: i for i, e in enumerate(EMOTION_LABELS)}

        model = AutoModelForSequenceClassification.from_pretrained(
            CONFIG["bert_model_name"],
            num_labels=len(EMOTION_LABELS),
            problem_type="multi_label_classification",
            id2label=id2label,
            label2id=label2id,
        )
        model.to(device)

        # ── Layer freezing ────────────────────────────────────────────────
        num_frozen = CONFIG.get("num_frozen_layers", 0)
        if num_frozen > 0:
            print(
                f"[train_robert] Freezing embeddings and first "
                f"{num_frozen} transformer layers…"
            )
            for param in model.bert.embeddings.parameters():
                param.requires_grad = False
            for i in range(min(num_frozen, len(model.bert.encoder.layer))):
                for param in model.bert.encoder.layer[i].parameters():
                    param.requires_grad = False

        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total     = sum(p.numel() for p in model.parameters())
        print(f"[train_robert] Trainable params: {trainable:,} / {total:,}")

        # ── TrainingArguments ─────────────────────────────────────────────
        training_args = TrainingArguments(
            output_dir=str(ckpt_dir),
            num_train_epochs=CONFIG["num_epochs"],
            per_device_train_batch_size=CONFIG["batch_size"],
            per_device_eval_batch_size=CONFIG["eval_batch_size"],
            learning_rate=CONFIG["learning_rate"],
            weight_decay=CONFIG["weight_decay"],
            warmup_ratio=CONFIG["warmup_ratio"],
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="macro_f1",
            greater_is_better=True,
            logging_steps=50,
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
        print(f"\n[train_robert] Training complete in {elapsed / 60:.1f} min.")

        trainer.save_model(str(ckpt_dir))
        tokenizer.save_pretrained(str(ckpt_dir))
        print(f"[train_robert] Best model saved → {ckpt_dir}")

    # ── Per-label threshold search on validation set ─────────────────────
    val_enc     = tokenize_split(tokenizer, val_texts, CONFIG["max_length"])
    val_dataset = TextClassificationDataset(val_enc, val_labels)

    thresholds = find_optimal_thresholds(model, val_dataset, tokenizer, device, CONFIG)

    # ── Test-set evaluation ───────────────────────────────────────────────
    print("\n[train_robert] Evaluating on test set…")

    test_enc     = tokenize_split(tokenizer, test_texts, CONFIG["max_length"])
    test_dataset = TextClassificationDataset(test_enc, test_labels)

    metrics, all_labels, all_preds = evaluate_on_test(
        model, test_dataset, tokenizer, device, thresholds, CONFIG
    )

    # ── Print results ─────────────────────────────────────────────────────
    print("\n── RoBERT-base Test-Set Metrics ──────────────────────────────────")
    print(f"  micro_f1    : {metrics['micro_f1']:.4f}")
    print(f"  macro_f1    : {metrics['macro_f1']:.4f}")
    print(f"  hamming_loss: {metrics['hamming_loss']:.4f}")
    print()
    print("Per-label results:")
    header = f"  {'emotion':<12}  {'thresh':>6}  {'P':>6}  {'R':>6}  {'F1':>6}  {'support':>7}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for emotion, stats in metrics["per_label"].items():
        print(
            f"  {emotion:<12}  {stats['threshold']:>6.2f}  "
            f"{stats['precision']:>6.4f}  {stats['recall']:>6.4f}  "
            f"{stats['f1']:>6.4f}  {stats['support']:>7}"
        )

    # ── Save metrics JSON ─────────────────────────────────────────────────
    out_path = results_dir / "robert_red_metrics.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"\n[train_robert] Metrics saved → {out_path}")


if __name__ == "__main__":
    main()
