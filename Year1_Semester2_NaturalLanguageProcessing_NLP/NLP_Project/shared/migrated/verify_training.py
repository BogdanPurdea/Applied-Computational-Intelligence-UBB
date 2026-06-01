#!/usr/bin/env python3
"""
verify_training.py
==================
Verify that all training (fine-tuning) pipelines compile and run successfully.
It runs a minimal dry-run (1 epoch, batch size 2, 10 samples) for each script
and saves checkpoints and metrics to a temporary directory.

Nothing is written to the real project directories:
- Checkpoints and metrics are redirected to a temporary directory.
- Preprocessed-text pickle caches are fully suppressed (no disk writes).
"""

from __future__ import annotations

import sys
import tempfile
import traceback
from pathlib import Path

# Add project root and module directories to sys.path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent

# Set up paths for utilities and shared loaders
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(project_root / "shared" / "migrated") not in sys.path:
    sys.path.insert(0, str(project_root / "shared" / "migrated"))
if str(project_root / "1_English" / "shared") not in sys.path:
    sys.path.insert(0, str(project_root / "1_English" / "shared"))
if str(project_root / "2_Romanian" / "shared") not in sys.path:
    sys.path.insert(0, str(project_root / "2_Romanian" / "shared"))

# Add each training pipeline directory to path to import them directly
sys.path.insert(0, str(project_root / "1_English" / "4_DistilBERT_SA_Practical"))
sys.path.insert(0, str(project_root / "1_English" / "5_DistilBERT_SA_Practical"))
sys.path.insert(0, str(project_root / "1_English" / "6_SentenceBERT_Practical"))
sys.path.insert(0, str(project_root / "2_Romanian" / "1_BERT_Sentiment_Articles"))
sys.path.insert(0, str(project_root / "2_Romanian" / "2_RoBERT_Emotion_RED"))
sys.path.insert(0, str(project_root / "2_Romanian" / "3_RoBERT_Conv_Emotion_RED"))
sys.path.insert(0, str(project_root / "2_Romanian" / "4_RoBERT_Ensemble_Emotion_RED"))

print("=" * 70)
print("Training Pipeline Verification Script (Dry-Run)")
print("=" * 70)

# ---------------------------------------------------------------------------
# Nuclear backstop: suppress ALL pickle writes at the lowest level
# ---------------------------------------------------------------------------
# dataset_utils.save_pickle_cache is called by every save_preprocessed
# implementation. Neutralising it here prevents any pickle reaching disk
# regardless of how the higher-level function was imported.
import dataset_utils
_real_save_pickle = dataset_utils.save_pickle_cache
dataset_utils.save_pickle_cache = lambda data, path: None
print("[setup] dataset_utils.save_pickle_cache → suppressed (no-op).")

# ---------------------------------------------------------------------------
# Setup Dataset Mocks (to run training instantly with a tiny data subset)
# ---------------------------------------------------------------------------
print("\n[setup] Injecting dataset mocks...")

import dataset_ro
import dataset_red
import dataset_en

_noop_save = lambda *args, **kwargs: None
_noop_load = lambda *args, **kwargs: None

# We will load a tiny subset (10 samples) and bypass loading cached preprocessed pickles
orig_splits_imdb = dataset_en.load_splits
dataset_en.load_splits = lambda *args, **kwargs: tuple(
    df.head(10).reset_index(drop=True) for df in orig_splits_imdb(*args, **kwargs)
)
dataset_en.load_preprocessed = _noop_load
dataset_en.save_preprocessed = _noop_save

orig_splits_ro = dataset_ro.load_splits
dataset_ro.load_splits = lambda *args, **kwargs: tuple(
    df.head(10).reset_index(drop=True) for df in orig_splits_ro(*args, **kwargs)
)
dataset_ro.load_preprocessed = _noop_load
dataset_ro.save_preprocessed = _noop_save

orig_splits_red = dataset_red.load_splits
dataset_red.load_splits = lambda *args, **kwargs: tuple(
    df.head(10).reset_index(drop=True) for df in orig_splits_red(*args, **kwargs)
)
dataset_red.load_preprocessed = _noop_load
dataset_red.save_preprocessed = _noop_save

print("✅ Dataset mocks set up successfully.")

# ---------------------------------------------------------------------------
# Import training modules
# ---------------------------------------------------------------------------
print("\n[setup] Importing training scripts...")
import train_bert as t_bert
import train_distilbert as t_distil
import train_robert as t_robert
import train_robert_conv as t_conv
import train_robert_ensemble as t_ens
import train_sbert as t_sbert
print("✅ All training scripts imported successfully.")

# Patch save_preprocessed in each training module's own namespace.
# Training scripts do `from dataset_xx import save_preprocessed` which binds
# the function locally — patching the dataset module attribute above is NOT
# enough.  We must also overwrite the reference inside each train module.
for _mod in (t_bert, t_distil, t_robert, t_conv, t_ens, t_sbert):
    if hasattr(_mod, "save_preprocessed"):
        _mod.save_preprocessed = _noop_save
print("[setup] Patched save_preprocessed in all training module namespaces.")


# ---------------------------------------------------------------------------
# Execute Verification
# ---------------------------------------------------------------------------
def run_verification():
    failures = []
    
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        print(f"\n📂 Using temporary output directory: {temp_dir}\n")
        
        # 1. train_bert
        print("─" * 60)
        print("1/6 verifying: train_bert.py")
        print("─" * 60)
        try:
            t_bert.CONFIG["num_epochs"] = 1
            t_bert.CONFIG["batch_size"] = 2
            t_bert.CONFIG["eval_batch_size"] = 2
            t_bert.CONFIG["checkpoint_dir"] = temp_dir / "bert_romanian"
            t_bert.CONFIG["results_dir"] = temp_dir / "results"
            t_bert.main()
            print("\n✅ train_bert pipeline completed successfully!\n")
        except Exception as e:
            print(f"\n❌ train_bert failed:\n{traceback.format_exc()}")
            failures.append(("train_bert.py", str(e)))

        # 2. train_distilbert
        print("─" * 60)
        print("2/6 verifying: train_distilbert.py")
        print("─" * 60)
        try:
            t_distil.CONFIG["num_epochs"] = 1
            t_distil.CONFIG["batch_size"] = 2
            t_distil.CONFIG["eval_batch_size"] = 2
            t_distil.CONFIG["checkpoint_dir"] = temp_dir / "distilbert"
            t_distil.CONFIG["results_dir"] = temp_dir / "results"
            t_distil.main()
            print("\n✅ train_distilbert pipeline completed successfully!\n")
        except Exception as e:
            print(f"\n❌ train_distilbert failed:\n{traceback.format_exc()}")
            failures.append(("train_distilbert.py", str(e)))

        # 3. train_robert
        print("─" * 60)
        print("3/6 verifying: train_robert.py")
        print("─" * 60)
        try:
            t_robert.CONFIG["num_epochs"] = 1
            t_robert.CONFIG["batch_size"] = 2
            t_robert.CONFIG["eval_batch_size"] = 2
            t_robert.CONFIG["checkpoint_dir"] = temp_dir / "robert_red"
            t_robert.CONFIG["results_dir"] = temp_dir / "results"
            t_robert.main()
            print("\n✅ train_robert pipeline completed successfully!\n")
        except Exception as e:
            print(f"\n❌ train_robert failed:\n{traceback.format_exc()}")
            failures.append(("train_robert.py", str(e)))

        # 4. train_robert_conv
        print("─" * 60)
        print("4/6 verifying: train_robert_conv.py")
        print("─" * 60)
        try:
            t_conv.CONFIG["num_epochs"] = 1
            t_conv.CONFIG["batch_size"] = 2
            t_conv.CONFIG["eval_batch_size"] = 2
            t_conv.CONFIG["checkpoint_dir"] = temp_dir / "robert_conv"
            t_conv.CONFIG["results_dir"] = temp_dir / "results"
            t_conv.main()
            print("\n✅ train_robert_conv pipeline completed successfully!\n")
        except Exception as e:
            print(f"\n❌ train_robert_conv failed:\n{traceback.format_exc()}")
            failures.append(("train_robert_conv.py", str(e)))

        # 5. train_robert_ensemble
        print("─" * 60)
        print("5/6 verifying: train_robert_ensemble.py")
        print("─" * 60)
        try:
            t_ens.CONFIG["num_epochs"] = 1
            t_ens.CONFIG["batch_size"] = 2
            t_ens.CONFIG["eval_batch_size"] = 2
            t_ens.CONFIG["checkpoint_dir"] = temp_dir / "robert_ensemble"
            t_ens.CONFIG["results_dir"] = temp_dir / "results"
            t_ens.main()
            print("\n✅ train_robert_ensemble pipeline completed successfully!\n")
        except Exception as e:
            print(f"\n❌ train_robert_ensemble failed:\n{traceback.format_exc()}")
            failures.append(("train_robert_ensemble.py", str(e)))

        # 6. train_sbert
        print("─" * 60)
        print("6/6 verifying: train_sbert.py")
        print("─" * 60)
        try:
            t_sbert.CONFIG["epochs"] = 1
            t_sbert.CONFIG["batch_size"] = 2
            t_sbert.CONFIG["checkpoint_dir"] = temp_dir / "sentencebert"
            t_sbert.CONFIG["output_dir"] = temp_dir / "output_PreProcessed"
            t_sbert.main()
            print("\n✅ train_sbert pipeline completed successfully!\n")
        except Exception as e:
            print(f"\n❌ train_sbert failed:\n{traceback.format_exc()}")
            failures.append(("train_sbert.py", str(e)))

    print("=" * 70)
    if failures:
        print("❌ SOME PIPELINES FAILED VERIFICATION:")
        for name, err in failures:
            print(f"  - {name}: {err}")
        sys.exit(1)
    else:
        print("🎉 ALL TRAINING PIPELINES FUNCTIONED CORRECTLY!")
        sys.exit(0)

if __name__ == "__main__":
    run_verification()
