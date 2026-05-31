#!/usr/bin/env python3
"""
verify_explain.py
=================
Verify that all explainability pipelines (both LIME and SHAP) compile and execute successfully.
It runs a minimal dry-run (1 example per class, tiny perturbation/eval samples) for each model
and saves the output files to a temporary directory without modifying/overwriting the existing results.
"""

from __future__ import annotations

import sys
import tempfile
import traceback
import importlib
from pathlib import Path

# Add project root and module directories to sys.path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(project_root / "shared" / "migrated") not in sys.path:
    sys.path.insert(0, str(project_root / "shared" / "migrated"))
if str(project_root / "1_English" / "shared") not in sys.path:
    sys.path.insert(0, str(project_root / "1_English" / "shared"))
if str(project_root / "2_Romanian" / "shared") not in sys.path:
    sys.path.insert(0, str(project_root / "2_Romanian" / "shared"))
if str(project_root / "explain") not in sys.path:
    sys.path.insert(0, str(project_root / "explain"))

print("=" * 70)
print("Explainability Pipeline Verification Script (Dry-Run)")
print("=" * 70)

# Determine checkpoints directory
checkpoint_base_dir = project_root / "checkpoints"
if not checkpoint_base_dir.exists():
    alt_base_dir = Path("/Users/bogdanpurdea/Projects/NLP/Practical_Project/checkpoints")
    if alt_base_dir.exists():
        checkpoint_base_dir = alt_base_dir
        print(f"[setup] Using alternative checkpoints path: {checkpoint_base_dir}")
    else:
        print(f"❌ Error: Checkpoints base directory not found locally or at alternative path!")
        sys.exit(1)
else:
    print(f"[setup] Using local checkpoints path: {checkpoint_base_dir}")

# Set up dataset mocks to use a tiny subset of 10 items and force preprocessing on-the-fly
import dataset_en
import dataset_ro
import dataset_red

orig_splits_imdb = dataset_en.load_splits
dataset_en.load_splits = lambda *args, **kwargs: tuple(
    df.head(10).reset_index(drop=True) for df in orig_splits_imdb(*args, **kwargs)
)
dataset_en.load_preprocessed = lambda *args, **kwargs: None
dataset_en.save_preprocessed = lambda *args, **kwargs: None

orig_splits_ro = dataset_ro.load_splits
dataset_ro.load_splits = lambda *args, **kwargs: tuple(
    df.head(10).reset_index(drop=True) for df in orig_splits_ro(*args, **kwargs)
)
dataset_ro.load_preprocessed = lambda *args, **kwargs: None
dataset_ro.save_preprocessed = lambda *args, **kwargs: None

orig_splits_red = dataset_red.load_splits
dataset_red.load_splits = lambda *args, **kwargs: tuple(
    df.head(10).reset_index(drop=True) for df in orig_splits_red(*args, **kwargs)
)
dataset_red.load_preprocessed = lambda *args, **kwargs: None
dataset_red.save_preprocessed = lambda *args, **kwargs: None

# Monkey-patch explain_utils to bypass class balancing logic during verification
# to avoid missing class errors in the tiny 10-item dataset subsets.
import explain_utils
explain_utils.select_balanced_eval_subset = lambda texts, labels, n, seed, num_classes: (
    texts[:n],
    labels[:n],
    list(range(min(n, len(texts))))
)

# List of models to verify
MODELS_TO_VERIFY = [
    "distilbert",
    "sentencebert",
    "bert_romanian",
    "robert_red",
    "robert_conv",
    "robert_ensemble"
]

import explain_config
import explain_lime
import explain_shap

def verify_model(model_name: str, temp_dir: Path) -> tuple[bool, bool]:
    lime_ok = False
    shap_ok = False
    
    print("\n" + "─" * 60)
    print(f"Verifying Model: {model_name}")
    print("─" * 60)
    
    info = explain_config.MODEL_INFO[model_name]
    checkpoint_dir = checkpoint_base_dir / Path(info["checkpoint_dir"]).name
    
    if not checkpoint_dir.exists():
        print(f"⚠️ Checkpoint directory for {model_name} not found at {checkpoint_dir}. Skipping.")
        return False, False
        
    temp_lime_dir = temp_dir / model_name / "lime_explanations"
    temp_shap_dir = temp_dir / model_name / "shap_explanations"
    temp_lime_dir.mkdir(parents=True, exist_ok=True)
    temp_shap_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Patch explain_config module dictionary in place
    explain_config.TARGET_MODEL = model_name
    explain_config.info = info
    
    # Mutate SHARED_CONFIG
    explain_config.SHARED_CONFIG.clear()
    explain_config.SHARED_CONFIG.update({
        "checkpoint_dir": checkpoint_dir,
        "model_name": model_name,
        "dataset_type": info["dataset_type"],
        "num_examples": info["num_classes"],  # 1 example per class
        "random_seed": 42,
        "class_names": info["class_names"],
        "max_length": 128,  # Truncate for speed
    })
    
    # Mutate LIME_CONFIG
    explain_config.LIME_CONFIG.clear()
    explain_config.LIME_CONFIG.update({
        **explain_config.SHARED_CONFIG,
        "results_dir": temp_lime_dir,
        "num_samples": 5,          # Tiny perturbation count for verification speed
        "num_features": 5,
        "batch_size": 16,
    })
    
    # Mutate SHAP_CONFIG
    explain_config.SHAP_CONFIG.clear()
    explain_config.SHAP_CONFIG.update({
        **explain_config.SHARED_CONFIG,
        "results_dir": temp_shap_dir,
        "max_evals": 5,            # Tiny evaluation count for verification speed
        "batch_size": 8,
    })
    
    # 2. Reload modules to apply updated configuration and perform correct imports
    try:
        importlib.reload(explain_lime)
        importlib.reload(explain_shap)
    except Exception as e:
        print(f"❌ Error reloading explain modules for {model_name}: {e}")
        traceback.print_exc()
        return False, False
        
    # 3. Execute LIME
    print(f"\n[lime] Running LIME dry-run...")
    try:
        explain_lime.main()
        # Verify LIME outputs
        if (temp_lime_dir / "lime_summary.json").exists() and (temp_lime_dir / "lime_top_words.json").exists():
            print("✅ LIME dry-run completed successfully.")
            lime_ok = True
        else:
            print("❌ LIME dry-run finished but output files are missing.")
    except Exception as e:
        print(f"❌ LIME dry-run failed with error: {e}")
        traceback.print_exc()
        
    # 4. Execute SHAP
    print(f"\n[shap] Running SHAP dry-run...")
    try:
        explain_shap.main()
        # Verify SHAP outputs
        if (temp_shap_dir / "shap_summary.json").exists() and (temp_shap_dir / "shap_top_tokens.json").exists():
            print("✅ SHAP dry-run completed successfully.")
            shap_ok = True
        else:
            print("❌ SHAP dry-run finished but output files are missing.")
    except Exception as e:
        print(f"❌ SHAP dry-run failed with error: {e}")
        traceback.print_exc()
        
    return lime_ok, shap_ok

def main():
    failures = []
    
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        print(f"📂 Verification outputs will be saved to temporary directory: {temp_dir}\n")
        
        for model in MODELS_TO_VERIFY:
            lime_ok, shap_ok = verify_model(model, temp_dir)
            if not lime_ok or not shap_ok:
                failures.append((model, lime_ok, shap_ok))
                
        print("\n" + "=" * 70)
        print("VERIFICATION SUMMARY")
        print("=" * 70)
        if not failures:
            print("🎉 ALL EXPLAIN SCRIPTS FUNCTIONED CORRECTLY (LIME & SHAP)!")
            sys.exit(0)
        else:
            print("❌ The following models failed explainability verification:")
            for model, lime, shap in failures:
                print(f"  - {model}: LIME={'✅' if lime else '❌'}, SHAP={'✅' if shap else '❌'}")
            sys.exit(1)

if __name__ == "__main__":
    main()
