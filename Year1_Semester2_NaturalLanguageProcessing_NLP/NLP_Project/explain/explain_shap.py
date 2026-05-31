"""
Generate SHAP (SHapley Additive exPlanations) for sentiment predictions
made by the fine-tuned target model.

What SHAP does
--------------
SHAP assigns each token a Shapley value — a theoretically grounded measure
(from cooperative game theory) of how much that token contributed to the
model's prediction relative to a baseline. Unlike LIME, SHAP values are
consistent and locally accurate by construction.

This script uses ``shap.Explainer`` with the ``transformers`` pipeline
interface, which uses ``shap.PartitionExplainer`` internally (Shapley
values computed by partitioning the input).

Usage
-----
    python explain_shap.py

Prerequisites
-------------
- The checkpoint directory must contain a trained target model checkpoint.
  Ensure the target model is trained first.
- ``data/imdb.csv`` must exist.

Outputs
-------
- ``results/shap_explanations/shap_values_{i:03d}.npy``  Per-example SHAP arrays
- ``results/shap_explanations/shap_summary.json``         Per-example metadata
- ``results/shap_explanations/shap_top_tokens.json``      Aggregated top tokens

Notes
-----
- The same 50 balanced examples used by ``explain_lime.py`` are reused here
  for direct comparison between the two methods.
- SHAP with transformer pipelines can be slow (~30 s–2 min per example).
  Total runtime: ~30–90 min depending on hardware.
"""

from __future__ import annotations

import json
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np
import shap
import torch
# Add project root and module directories to path so we can do absolute imports
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "shared" / "migrated"))
sys.path.insert(0, str(project_root / "2_Romanian" / "shared"))
sys.path.insert(0, str(project_root / "1_English" / "shared"))

from train_utils import select_hardware_device
from explain_utils import (
    select_balanced_eval_subset,
    load_explainability_model,
    make_predict_fn,
)


warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Configuration & Dynamic Imports
# ---------------------------------------------------------------------------

from explain_config import SHAP_CONFIG as CONFIG

dataset_type = CONFIG.get("dataset_type", "imdb")
if dataset_type == "red":
    from dataset_red import load_splits, load_preprocessed, save_preprocessed
    from preprocessing_red import preprocess_batch_red as preprocess_batch
elif dataset_type == "ro_articles":
    from dataset_ro import load_splits, load_preprocessed, save_preprocessed
    from preprocessing_ro import preprocess_batch
else:
    from dataset_en import load_splits, load_preprocessed, save_preprocessed
    from preprocessing_en import preprocess_batch





# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 65)
    print(f"SHAP Explanations — Fine-tuned {CONFIG['model_name']} on {CONFIG.get('dataset_type', 'imdb').upper()}")
    print("=" * 65)

    device = select_hardware_device()
    print(f"Device : {device}")

    # ── Paths ────────────────────────────────────────────────────────────
    ckpt_dir = CONFIG["checkpoint_dir"]
    out_dir = CONFIG["results_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Load model & tokenizer ───────────────────────────────────────────
    print(f"\n[shap] Loading model from {ckpt_dir}…")
    
    model_name = CONFIG["model_name"]
    dataset_type = CONFIG.get("dataset_type", "imdb")
    model, tokenizer = load_explainability_model(model_name, ckpt_dir, device)

    # ── Build prediction function ─────────────────────────────────────────
    predict_fn = make_predict_fn(
        model, tokenizer, device, CONFIG["max_length"], CONFIG["batch_size"], dataset_type
    )

    # ── Load test data ────────────────────────────────────────────────────

    if dataset_type == "red":
        from dataset_red import EMOTION_LABELS
        _, _, df_test = load_splits(task="classification")
        # Filter to single-label texts for explanation compatibility
        agreed_cols = [f"agreed_label_{e}" for e in EMOTION_LABELS]
        df_test = df_test[df_test["num_emotions"] == 1].reset_index(drop=True)
        # Map back to a single integer label index
        df_test["label"] = df_test[agreed_cols].values.argmax(axis=1)
        text_col = "text"
    else:
        _, _, df_test = load_splits(seed=CONFIG["random_seed"])
        text_col = "article" if dataset_type == "ro_articles" else "review"

    label_col = "label"
    test_labels = df_test[label_col].tolist()

    test_texts = load_preprocessed("test")
    if test_texts is None:
        print("[shap] Preprocessing test set…")
        result = preprocess_batch(df_test[text_col].tolist())
        # preprocess_batch_red returns (texts, kept_indices) for deduplication;
        # other preprocess_batch functions return just a list of strings.
        if dataset_type == "red" and isinstance(result, tuple):
            test_texts, kept_indices = result
            test_labels = [test_labels[i] for i in kept_indices]
        else:
            test_texts = result
        save_preprocessed(test_texts, "test")

    # ── Select balanced examples ──────────────────────────────────────────
    num_classes = len(CONFIG["class_names"])
    sel_texts, sel_labels, sel_indices = select_balanced_eval_subset(
        test_texts, test_labels, CONFIG["num_examples"], CONFIG["random_seed"], num_classes
    )
    class_counts = {name: sum(l == idx for l in sel_labels) for idx, name in enumerate(CONFIG["class_names"])}
    print(f"\n[shap] Selected {len(sel_texts)} examples: {class_counts}")

    # shap.Explainer auto-selects PartitionExplainer for custom predict functions.
    masker = shap.maskers.Text(tokenizer=r"\W+")   # word-level masking
    explainer = shap.Explainer(
        predict_fn,
        masker=masker,
        output_names=CONFIG["class_names"],
    )

    # ── Generate explanations ─────────────────────────────────────────────
    summary = []
    token_importance: dict[str, list[float]] = defaultdict(list)

    for i, (text, label) in enumerate(zip(sel_texts, sel_labels)):
        print(f"[shap] Example {i+1:02d}/{len(sel_texts)}  "
              f"(true: {CONFIG['class_names'][label]}) …", end=" ", flush=True)

        # shap_values shape: (1, num_tokens, num_classes)
        shap_values = explainer(
            [text],
            max_evals=CONFIG["max_evals"],
            batch_size=CONFIG["batch_size"],
        )

        # Extract values for the predicted class
        tokens = shap_values.data[0]              # list of token strings

        # Predicted class from predict function output
        pred_probs = predict_fn([text])[0]
        pred_class = int(np.argmax(pred_probs))

        values_pred = shap_values.values[0, :, pred_class]

        # Save SHAP values as numpy array for later plotting in notebook
        npy_path = out_dir / f"shap_values_{i:03d}.npy"
        np.save(str(npy_path), values_pred)

        # Aggregate token importances
        for tok, val in zip(tokens, values_pred):
            token_importance[tok].append(float(val))

        # Per-example metadata
        top_tokens = sorted(
            zip(tokens, values_pred.tolist()),
            key=lambda x: abs(x[1]),
            reverse=True,
        )[:10]

        summary.append({
            "example_idx": int(sel_indices[i]),
            "true_label": CONFIG["class_names"][label],
            "predicted_label": CONFIG["class_names"][pred_class],
            "correct": pred_class == label,
            "top_tokens": [(t, float(v)) for t, v in top_tokens],
            "npy_file": npy_path.name,
        })
        correct_marker = "✓" if pred_class == label else "✗"
        print(f"pred={CONFIG['class_names'][pred_class]} {correct_marker}")

    # ── Aggregated top tokens ─────────────────────────────────────────────
    agg_tokens = {
        tok: float(np.mean(np.abs(vals)))
        for tok, vals in token_importance.items()
        if len(vals) >= 2      # only tokens appearing in multiple examples
    }
    top_tokens_sorted = sorted(agg_tokens.items(), key=lambda x: x[1], reverse=True)[:50]

    # ── Save JSON outputs ─────────────────────────────────────────────────
    summary_path = out_dir / "shap_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    top_tokens_path = out_dir / "shap_top_tokens.json"
    with open(top_tokens_path, "w") as f:
        json.dump(top_tokens_sorted, f, indent=2)

    correct = sum(e["correct"] for e in summary)
    print(f"\n[shap] Accuracy on explained examples: {correct}/{len(summary)}")
    print(f"[shap] SHAP arrays → {out_dir}/shap_values_*.npy")
    print(f"[shap] Summary     → {summary_path}")
    print(f"[shap] Top tokens  → {top_tokens_path}")


if __name__ == "__main__":
    main()
