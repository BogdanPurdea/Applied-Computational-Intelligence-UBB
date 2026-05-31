"""
train_robert_conv.py
====================
Fine-tune ``readerbench/RoBERT-base`` augmented with a 1D Convolutional layer
placed before attention layers on the REDv2 Romanian Emotion Dataset
for **multi-label emotion classification**.

Usage
-----
    python train_robert_conv.py
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import (
    f1_score,
    hamming_loss,
    precision_score,
    recall_score,
)
from torch.utils.data import DataLoader
from transformers import (
    AutoModel,
    AutoConfig,
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
from transformers.modeling_outputs import SequenceClassifierOutput

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
    "checkpoint_dir":          project_root / "checkpoints" / "robert_conv",
    "results_dir":             Path(__file__).resolve().parent / "Results",
}


# ---------------------------------------------------------------------------
# Custom Model Wrapper
# ---------------------------------------------------------------------------

class BertWithConvForSequenceClassification(nn.Module):
    def __init__(self, model_name, num_labels, kernel_size=3, id2label=None, label2id=None):
        super().__init__()
        self.config = AutoConfig.from_pretrained(model_name)
        self.config.num_labels = num_labels
        self.config.id2label = id2label
        self.config.label2id = label2id
        
        self.bert = AutoModel.from_pretrained(model_name, config=self.config)
        hidden_size = self.config.hidden_size
        
        # 1D Conv layer placed after encoder attention blocks
        self.conv = nn.Conv1d(
            in_channels=hidden_size,
            out_channels=hidden_size,
            kernel_size=kernel_size,
            padding=kernel_size // 2
        )
        self.layer_norm = nn.LayerNorm(hidden_size, eps=self.config.layer_norm_eps)
        self.dropout = nn.Dropout(self.config.hidden_dropout_prob)
        self.classifier = nn.Linear(hidden_size, num_labels)
        self.loss_fct = nn.BCEWithLogitsLoss()

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        labels=None,
        **kwargs
    ):
        # 1. Pass through standard BERT layers
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            return_dict=True
        )
        sequence_output = outputs.last_hidden_state
        
        # 2. Apply Conv1D after attention blocks
        x = sequence_output.transpose(1, 2)
        x = self.conv(x)
        x = x.transpose(1, 2)
        x = self.layer_norm(x)
        x = self.dropout(x)
        
        # 3. Pool the [CLS] representation (token 0)
        pooled_output = x[:, 0, :]
        pooled_output = self.dropout(pooled_output)
        
        # 4. Logits
        logits = self.classifier(pooled_output)
        
        # 5. Loss calculation
        loss = None
        if labels is not None:
            loss = self.loss_fct(logits, labels)
            
        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions
        )

    def state_dict(self, *args, **kwargs):
        sd = super().state_dict(*args, **kwargs)
        return {k: v.contiguous() for k, v in sd.items()}


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
                    f"[train_robert_conv] Cache length mismatch for '{split_name}' "
                    f"({len(cached)} texts vs {len(raw_labels)} label rows). "
                    f"Recomputing kept indices…"
                )
                from preprocessing_red import preprocess, remove_duplicates
                cleaned_raw = [preprocess(t) for t in df["text"].tolist()]
                _, kept = remove_duplicates(cleaned_raw)
                results.append((cached, raw_labels[kept]))
        else:
            print(
                f"[train_robert_conv] Preprocessing '{split_name}' "
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
# Per-label threshold search on the validation set
# ---------------------------------------------------------------------------

def find_optimal_thresholds(
    model,
    val_dataset: TextClassificationDataset,
    tokenizer,
    device: torch.device,
    config: dict,
) -> np.ndarray:
    print("\n[train_robert_conv] Searching per-label optimal thresholds on validation set…")

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

    logits_arr = np.concatenate(all_logits, axis=0)
    labels_arr = np.concatenate(all_labels, axis=0).astype(int)
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

    preds_arr = np.zeros_like(probs_arr, dtype=int)
    for i, t in enumerate(thresholds):
        preds_arr[:, i] = (probs_arr[:, i] >= t).astype(int)

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
    print("RoBERT-base 1D-Conv Fine-Tuning — REDv2 Emotion Classification")
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

    print(
        f"\n[train_robert_conv] Dataset sizes after preprocessing:"
        f"\n  Train : {len(train_texts):,} samples"
        f"\n  Val   : {len(val_texts):,} samples"
        f"\n  Test  : {len(test_texts):,} samples"
    )

    print(f"\n[train_robert_conv] Loading tokenizer: {CONFIG['bert_model_name']}")
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["bert_model_name"])
    collator  = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="pt")

    safe_path = ckpt_dir / "model.safetensors"
    bin_path = ckpt_dir / "pytorch_model.bin"
    has_checkpoint = safe_path.exists() or bin_path.exists()

    id2label = {i: e for i, e in enumerate(EMOTION_LABELS)}
    label2id = {e: i for i, e in enumerate(EMOTION_LABELS)}

    if has_checkpoint:
        print(f"\n✅  Checkpoint found at '{ckpt_dir}' — skipping training.")
        model = BertWithConvForSequenceClassification(
            CONFIG["bert_model_name"],
            num_labels=len(EMOTION_LABELS),
            id2label=id2label,
            label2id=label2id,
        )
        if safe_path.exists():
            import safetensors.torch
            state_dict = safetensors.torch.load_file(str(safe_path), device="cpu")
        else:
            state_dict = torch.load(bin_path, map_location="cpu")
        model.load_state_dict(state_dict)
        model.to(device)
    else:
        print("\n[train_robert_conv] No checkpoint found. Tokenising and training…")

        train_enc = tokenize_split(tokenizer, train_texts, CONFIG["max_length"])
        val_enc   = tokenize_split(tokenizer, val_texts,   CONFIG["max_length"])

        train_dataset = TextClassificationDataset(train_enc, train_labels)
        val_dataset   = TextClassificationDataset(val_enc,   val_labels)

        # ── Model instantiation ───────────────────────────────────────────
        model = BertWithConvForSequenceClassification(
            CONFIG["bert_model_name"],
            num_labels=len(EMOTION_LABELS),
            id2label=id2label,
            label2id=label2id,
        )
        model.to(device)

        # ── Layer freezing ────────────────────────────────────────────────
        num_frozen = CONFIG.get("num_frozen_layers", 0)
        if num_frozen > 0:
            print(
                f"[train_robert_conv] Freezing embeddings and first "
                f"{num_frozen} transformer layers…"
            )
            for param in model.bert.embeddings.parameters():
                param.requires_grad = False
            for i in range(min(num_frozen, len(model.bert.encoder.layer))):
                for param in model.bert.encoder.layer[i].parameters():
                    param.requires_grad = False

        trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total     = sum(p.numel() for p in model.parameters())
        print(f"[train_robert_conv] Trainable params: {trainable:,} / {total:,}")

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
            fp16=False,
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
        print(f"\n[train_robert_conv] Training complete in {elapsed / 60:.1f} min.")

        trainer.save_model(str(ckpt_dir))
        tokenizer.save_pretrained(str(ckpt_dir))
        print(f"[train_robert_conv] Best model saved → {ckpt_dir}")

    # ── Per-label threshold search on validation set ─────────────────────
    val_enc     = tokenize_split(tokenizer, val_texts, CONFIG["max_length"])
    val_dataset = TextClassificationDataset(val_enc, val_labels)

    thresholds = find_optimal_thresholds(model, val_dataset, tokenizer, device, CONFIG)

    # ── Test-set evaluation ───────────────────────────────────────────────
    print("\n[train_robert_conv] Evaluating on test set…")

    test_enc     = tokenize_split(tokenizer, test_texts, CONFIG["max_length"])
    test_dataset = TextClassificationDataset(test_enc, test_labels)

    metrics, all_labels, all_preds = evaluate_on_test(
        model, test_dataset, tokenizer, device, thresholds, CONFIG
    )

    # ── Print results ─────────────────────────────────────────────────────
    print("\n── RoBERT-base 1D-Conv Test-Set Metrics ──────────────────────────")
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
    out_path = results_dir / "robert_conv_metrics.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"\n[train_robert_conv] Metrics saved → {out_path}")


if __name__ == "__main__":
    main()
