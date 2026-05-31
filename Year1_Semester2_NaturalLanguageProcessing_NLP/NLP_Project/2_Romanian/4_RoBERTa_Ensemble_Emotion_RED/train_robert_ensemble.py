"""
train_robert_ensemble.py
========================
Fine-tune a 5-fold ensemble of ``readerbench/RoBERT-base`` on the REDv2 Romanian Emotion Dataset.
Trains each fold for 3 epochs, performs out-of-fold optimal threshold search,
and computes final ensembled test set metrics.

Usage:
    python train_robert_ensemble.py
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
    f1_score,
    hamming_loss,
    precision_score,
    recall_score,
)
from sklearn.model_selection import KFold
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
    "bert_model_name":         "readerbench/RoBERT-base",
    "max_length":              128,
    "batch_size":              16,
    "eval_batch_size":         32,

    # Training
    "learning_rate":           2e-5,
    "weight_decay":            0.01,
    "num_epochs":              3,        # Train 3 epochs per fold to prevent overfitting
    "warmup_ratio":            0.06,
    "early_stopping_patience": 2,
    "num_frozen_layers":       4,

    # Inference
    "threshold_search_steps":  81,
    "default_threshold":       0.5,

    # Misc
    "random_seed":             42,
    "task":                    "classification",

    # Paths
    "checkpoint_dir":          project_root / "checkpoints" / "robert_ensemble",
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
    results = []
    for split_name, df in [("train", df_train), ("val", df_val), ("test", df_test)]:
        raw_labels = df[AGREED_LABEL_COLS].values.astype(np.float32)

        cached = load_preprocessed(split_name)
        if cached is not None:
            if len(cached) == len(raw_labels):
                results.append((cached, raw_labels))
            else:
                print(
                    f"[train_robert_ensemble] Cache length mismatch for '{split_name}' "
                    f"({len(cached)} texts vs {len(raw_labels)} label rows). "
                    f"Recomputing kept indices…"
                )
                from preprocessing_red import preprocess, remove_duplicates
                cleaned_raw = [preprocess(t) for t in df["text"].tolist()]
                _, kept = remove_duplicates(cleaned_raw)
                results.append((cached, raw_labels[kept]))
        else:
            print(
                f"[train_robert_ensemble] Preprocessing '{split_name}' "
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
    return tokenizer(
        texts,
        padding=False,
        truncation=True,
        max_length=max_length,
        return_tensors=None,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 65)
    print("RoBERT-base 5-Fold Ensemble — REDv2 Emotion Classification")
    print("=" * 65)

    device = select_hardware_device()
    print(f"Device : {device}")

    seed = CONFIG["random_seed"]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    ckpt_dir    = CONFIG["checkpoint_dir"]
    results_dir = CONFIG["results_dir"]
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    df_train, df_val, df_test = load_splits(task=CONFIG["task"])

    (train_texts, train_labels), \
    (val_texts,   val_labels),   \
    (test_texts,  test_labels) = get_preprocessed_texts(df_train, df_val, df_test)

    # Combine train and validation splits to form the ensemble pool
    full_texts = train_texts + val_texts
    full_labels = np.concatenate([train_labels, val_labels], axis=0)

    print(
        f"\n[train_robert_ensemble] Combined Dataset Pool: {len(full_texts):,} samples"
        f"\n  Test Split : {len(test_texts):,} samples"
    )

    print(f"\n[train_robert_ensemble] Loading tokenizer: {CONFIG['bert_model_name']}")
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["bert_model_name"])
    collator  = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")

    # 5-fold cross-validation setup
    kf = KFold(n_splits=5, shuffle=True, random_state=seed)
    
    # Store out-of-fold predictions
    oof_probs = np.zeros((len(full_texts), len(EMOTION_LABELS)))
    
    id2label = {i: e for i, e in enumerate(EMOTION_LABELS)}
    label2id = {e: i for i, e in enumerate(EMOTION_LABELS)}

    # Check if all 5 folds already trained
    all_folds_trained = all((ckpt_dir / f"fold_{i}" / "config.json").exists() for i in range(5))

    if all_folds_trained:
        print("\n✅  All 5 folds already trained — skipping training phase.")
    else:
        print("\n[train_robert_ensemble] Training folds...")
        for fold_i, (train_idx, val_idx) in enumerate(kf.split(full_texts)):
            fold_ckpt_dir = ckpt_dir / f"fold_{fold_i}"
            print(f"\n--- Fold {fold_i} ---")
            
            if (fold_ckpt_dir / "config.json").exists():
                print(f"  Fold {fold_i} already trained. Skipping.")
                continue

            fold_train_texts = [full_texts[idx] for idx in train_idx]
            fold_train_labels = full_labels[train_idx]
            fold_val_texts = [full_texts[idx] for idx in val_idx]
            fold_val_labels = full_labels[val_idx]

            fold_train_enc = tokenize_split(tokenizer, fold_train_texts, CONFIG["max_length"])
            fold_val_enc   = tokenize_split(tokenizer, fold_val_texts, CONFIG["max_length"])

            fold_train_dataset = TextClassificationDataset(fold_train_enc, fold_train_labels)
            fold_val_dataset   = TextClassificationDataset(fold_val_enc, fold_val_labels)

            model = AutoModelForSequenceClassification.from_pretrained(
                CONFIG["bert_model_name"],
                num_labels=len(EMOTION_LABELS),
                problem_type="multi_label_classification",
                id2label=id2label,
                label2id=label2id,
            )
            model.to(device)

            # Monkey-patch state_dict to return contiguous tensors (MPS compat)
            original_state_dict = model.state_dict
            def patched_state_dict(*args, **kwargs):
                sd = original_state_dict(*args, **kwargs)
                return {k: v.contiguous() for k, v in sd.items()}
            model.state_dict = patched_state_dict

            # Freezing embeddings + first 4 layers
            num_frozen = CONFIG.get("num_frozen_layers", 0)
            if num_frozen > 0:
                for param in model.bert.embeddings.parameters():
                    param.requires_grad = False
                for i in range(min(num_frozen, len(model.bert.encoder.layer))):
                    for param in model.bert.encoder.layer[i].parameters():
                        param.requires_grad = False

            training_args = TrainingArguments(
                output_dir=str(fold_ckpt_dir),
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
                fp16=False,
                report_to="none",
            )

            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=fold_train_dataset,
                eval_dataset=fold_val_dataset,
                processing_class=tokenizer,
                data_collator=collator,
                compute_metrics=compute_metrics,
                callbacks=[
                    EarlyStoppingCallback(
                        early_stopping_patience=CONFIG["early_stopping_patience"]
                    )
                ],
            )

            trainer.train()
            trainer.save_model(str(fold_ckpt_dir))
            tokenizer.save_pretrained(str(fold_ckpt_dir))
            print(f"  Fold {fold_i} best model saved → {fold_ckpt_dir}")

    # ── Inference: Out-of-Fold Predictions ─────────────────────────────────
    print("\n[train_robert_ensemble] Gathering Out-of-Fold validation predictions…")
    for fold_i, (train_idx, val_idx) in enumerate(kf.split(full_texts)):
        fold_ckpt_dir = ckpt_dir / f"fold_{fold_i}"
        print(f"  Evaluating fold {fold_i} on its validation slice…")
        
        model = AutoModelForSequenceClassification.from_pretrained(str(fold_ckpt_dir))
        model.to(device)
        model.eval()

        fold_val_texts = [full_texts[idx] for idx in val_idx]
        fold_val_labels = full_labels[val_idx]
        fold_val_enc = tokenize_split(tokenizer, fold_val_texts, CONFIG["max_length"])
        fold_val_dataset = TextClassificationDataset(fold_val_enc, fold_val_labels)

        val_loader = DataLoader(
            fold_val_dataset,
            batch_size=CONFIG["eval_batch_size"],
            collate_fn=collator,
            shuffle=False,
        )

        fold_logits = []
        with torch.no_grad():
            for batch in val_loader:
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
                fold_logits.append(outputs.logits.cpu().numpy())

        fold_logits = np.concatenate(fold_logits, axis=0)
        fold_probs = torch.sigmoid(torch.tensor(fold_logits)).numpy()
        oof_probs[val_idx] = fold_probs

    # ── OOF Threshold Search ───────────────────────────────────────────────
    candidates = np.linspace(0.1, 0.9, CONFIG["threshold_search_steps"])
    best_thresholds = np.full(len(EMOTION_LABELS), CONFIG["default_threshold"])

    print("\n[train_robert_ensemble] Searching per-label optimal thresholds on OOF predictions…")
    for label_idx, emotion in enumerate(EMOTION_LABELS):
        label_true = full_labels[:, label_idx]
        best_f1, best_t = -1.0, CONFIG["default_threshold"]
        for t in candidates:
            preds = (oof_probs[:, label_idx] >= t).astype(int)
            f1 = f1_score(label_true, preds, zero_division=0)
            if f1 > best_f1:
                best_f1, best_t = f1, t
        best_thresholds[label_idx] = best_t
        print(f"  {emotion:<10}  best_t={best_t:.2f}  OOF_F1={best_f1:.4f}")

    # ── Test Set Inference: 5-Fold Ensembling ──────────────────────────────
    print("\n[train_robert_ensemble] Ensembling 5 folds on the test set…")
    
    test_enc = tokenize_split(tokenizer, test_texts, CONFIG["max_length"])
    test_dataset = TextClassificationDataset(test_enc, test_labels)
    test_loader = DataLoader(
        test_dataset,
        batch_size=CONFIG["eval_batch_size"],
        collate_fn=collator,
        shuffle=False,
    )

    test_probs_sum = np.zeros((len(test_texts), len(EMOTION_LABELS)))

    for fold_i in range(5):
        fold_ckpt_dir = ckpt_dir / f"fold_{fold_i}"
        print(f"  Inference fold {fold_i}…")
        model = AutoModelForSequenceClassification.from_pretrained(str(fold_ckpt_dir))
        model.to(device)
        model.eval()

        fold_test_logits = []
        with torch.no_grad():
            for batch in test_loader:
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
                fold_test_logits.append(outputs.logits.cpu().numpy())

        fold_test_logits = np.concatenate(fold_test_logits, axis=0)
        fold_test_probs = torch.sigmoid(torch.tensor(fold_test_logits)).numpy()
        test_probs_sum += fold_test_probs

    avg_test_probs = test_probs_sum / 5.0

    # ── Compute test metrics using OOF thresholds ──────────────────────────
    preds_arr = np.zeros_like(avg_test_probs, dtype=int)
    for i, t in enumerate(best_thresholds):
        preds_arr[:, i] = (avg_test_probs[:, i] >= t).astype(int)

    labels_arr = test_labels.astype(int)
    micro = f1_score(labels_arr, preds_arr, average="micro", zero_division=0)
    macro = f1_score(labels_arr, preds_arr, average="macro", zero_division=0)
    hl    = hamming_loss(labels_arr, preds_arr)

    per_label: dict[str, dict] = {}
    for i, emotion in enumerate(EMOTION_LABELS):
        per_label[emotion] = {
            "precision": float(precision_score(labels_arr[:, i], preds_arr[:, i], zero_division=0)),
            "recall":    float(recall_score(labels_arr[:, i], preds_arr[:, i], zero_division=0)),
            "f1":        float(f1_score(labels_arr[:, i], preds_arr[:, i], zero_division=0)),
            "support":   int(labels_arr[:, i].sum()),
            "threshold": float(best_thresholds[i]),
        }

    metrics = {
        "micro_f1":    float(micro),
        "macro_f1":    float(macro),
        "hamming_loss": float(hl),
        "thresholds":  {e: float(best_thresholds[i]) for i, e in enumerate(EMOTION_LABELS)},
        "per_label":   per_label,
    }

    # ── Print results ─────────────────────────────────────────────────────
    print("\n── RoBERT-base 5-Fold Ensemble Test-Set Metrics ──────────────────")
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
    out_path = results_dir / "robert_ensemble_metrics.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"\n[train_robert_ensemble] Metrics saved → {out_path}")


if __name__ == "__main__":
    main()
