"""
explain_lime.py
===============
Generate LIME (Local Interpretable Model-agnostic Explanations) for
sentiment predictions made by the fine-tuned target model.

What LIME does
--------------
LIME perturbs each input text (masking random words) and fits a locally
linear surrogate model around the neighbourhood of that input. The
surrogate's coefficients indicate which words most contributed to the
model's prediction for that specific example.

Usage
-----
    python explain_lime.py

Prerequisites
-------------
- The checkpoint directory must contain a trained target model checkpoint.
  Ensure the target model is trained first.
- ``data/imdb.csv`` must exist (run ``dataset.py``).

Outputs
-------
- ``results/lime_explanations/example_{i:03d}.html``  (50 HTML reports)
- ``results/lime_explanations/lime_top_words.json``   Aggregated top words
- ``results/lime_explanations/lime_summary.json``     Per-example metadata

Notes
-----
- 50 examples are selected: 25 positive, 25 negative (balanced).
- Each explanation calls the model ~100–500 times (LIME's perturbation
  budget). Total runtime is ~10–30 min depending on hardware.
- The same 50 examples are used by ``explain_shap.py`` for direct
  comparison.
"""

from __future__ import annotations

import json
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
from lime.lime_text import LimeTextExplainer
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

from explain_config import LIME_CONFIG as CONFIG

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
    print(f"LIME Explanations — Fine-tuned {CONFIG['model_name']} on {CONFIG.get('dataset_type', 'imdb').upper()}")
    print("=" * 65)

    device = select_hardware_device()
    print(f"Device : {device}")

    # ── Paths ────────────────────────────────────────────────────────────
    ckpt_dir = CONFIG["checkpoint_dir"]
    out_dir = CONFIG["results_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Load model & tokenizer ───────────────────────────────────────────
    print(f"\n[lime] Loading model from {ckpt_dir}…")
    
    model_name = CONFIG["model_name"]
    model, tokenizer = load_explainability_model(model_name, ckpt_dir, device)

    # ── Load test data ───────────────────────────────────────────────────
    dataset_type = CONFIG.get("dataset_type", "imdb")

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
        print("[lime] Preprocessing test set…")
        result = preprocess_batch(df_test[text_col].tolist())
        # preprocess_batch_red returns (texts, kept_indices) for deduplication;
        # other preprocess_batch functions return just a list of strings.
        if dataset_type == "red" and isinstance(result, tuple):
            test_texts, kept_indices = result
            test_labels = [test_labels[i] for i in kept_indices]
        else:
            test_texts = result
        save_preprocessed(test_texts, "test")

    # ── Select balanced examples ─────────────────────────────────────────
    num_classes = len(CONFIG["class_names"])
    sel_texts, sel_labels, sel_indices = select_balanced_eval_subset(
        test_texts, test_labels, CONFIG["num_examples"], CONFIG["random_seed"], num_classes
    )
    class_counts = {name: sum(l == idx for l in sel_labels) for idx, name in enumerate(CONFIG["class_names"])}
    print(f"\n[lime] Selected {len(sel_texts)} examples: {class_counts}")

    # ── Build LIME explainer & predict function ───────────────────────────
    predict_fn = make_predict_fn(
        model, tokenizer, device, CONFIG["max_length"], CONFIG["batch_size"], dataset_type
    )
    explainer = LimeTextExplainer(class_names=CONFIG["class_names"])

    # ── Generate explanations ────────────────────────────────────────────
    summary = []
    word_importance: dict[str, list[float]] = defaultdict(list)

    for i, (text, label) in enumerate(zip(sel_texts, sel_labels)):
        print(f"[lime] Example {i+1:02d}/{len(sel_texts)}  "
              f"(true: {CONFIG['class_names'][label]}) …", end=" ", flush=True)

        pred_probs = predict_fn([text])[0]
        pred_class = int(np.argmax(pred_probs))

        exp = explainer.explain_instance(
            text,
            predict_fn,
            num_features=CONFIG["num_features"],
            num_samples=CONFIG["num_samples"],
            labels=[pred_class],
        )

        # Save HTML report
        html_path = out_dir / f"example_{i:03d}.html"
        exp.save_to_file(str(html_path))

        # Collect word-level feature importances
        features = exp.as_list(label=pred_class)  # [(word, weight), ...]
        for word, weight in features:
            word_importance[word].append(weight)

        # Per-example metadata
        summary.append({
            "example_idx": int(sel_indices[i]),
            "true_label": CONFIG["class_names"][label],
            "predicted_label": CONFIG["class_names"][pred_class],
            "correct": pred_class == label,
            "top_words": [(w, float(wt)) for w, wt in features],
            "html_file": html_path.name,
        })
        correct_marker = "✓" if pred_class == label else "✗"
        print(f"pred={CONFIG['class_names'][pred_class]} {correct_marker}")

    # ── Aggregate top words ───────────────────────────────────────────────
    # Mean absolute importance across all examples a word appeared in
    top_words = {
        word: float(np.mean(np.abs(weights)))
        for word, weights in word_importance.items()
    }
    top_words_sorted = sorted(top_words.items(), key=lambda x: x[1], reverse=True)[:50]

    # ── Save JSON outputs ─────────────────────────────────────────────────
    summary_path = out_dir / "lime_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    top_words_path = out_dir / "lime_top_words.json"
    with open(top_words_path, "w") as f:
        json.dump(top_words_sorted, f, indent=2)

    correct = sum(e["correct"] for e in summary)
    print(f"\n[lime] Accuracy on explained examples: {correct}/{len(summary)}")
    print(f"[lime] HTML reports → {out_dir}/")
    print(f"[lime] Summary      → {summary_path}")
    print(f"[lime] Top words    → {top_words_path}")


if __name__ == "__main__":
    main()
