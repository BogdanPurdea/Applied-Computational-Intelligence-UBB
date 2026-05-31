"""
dataset_ro.py
=============
Load and cache the Romanian categorized web articles dataset.

Columns: article (str), sentiment (str: "positive"/"negative"/"neutral"), label (int: 1/0/2)
Split  : 70 % train / 15 % val / 15 % test (stratified on label)
"""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd

# Add project root to path so we can do imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "shared" / "migrated"))
from dataset_utils import perform_stratified_split, save_pickle_cache, load_pickle_cache

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DATA_DIR = project_root / "Datasets" / "migrated" / "ro_article_reviews"
CSV_PATH = DATA_DIR / "ro_articles.csv"

# Default split ratios (must sum to 1.0)
DEFAULT_TRAIN_RATIO = 0.70
DEFAULT_VAL_RATIO = 0.15
DEFAULT_TEST_RATIO = 0.15
DEFAULT_SEED = 42


# ---------------------------------------------------------------------------
# Split loader
# ---------------------------------------------------------------------------

def load_splits(
    seed: int = DEFAULT_SEED,
    train_ratio: float = DEFAULT_TRAIN_RATIO,
    val_ratio: float = DEFAULT_VAL_RATIO,
    test_ratio: float = DEFAULT_TEST_RATIO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the full Romanian dataset and return stratified train/val/test splits."""
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Romanian dataset CSV not found at '{CSV_PATH}'. Run rebuild_dataset.py first.")

    df = pd.read_csv(CSV_PATH)

    df_train, df_val, df_test = perform_stratified_split(
        df, "label", seed, train_ratio, val_ratio, test_ratio
    )

    print(
        f"[dataset_ro] Splits — "
        f"train: {len(df_train):,}  "
        f"val: {len(df_val):,}  "
        f"test: {len(df_test):,}"
    )
    return df_train, df_val, df_test


# ---------------------------------------------------------------------------
# Preprocessed text cache helpers
# ---------------------------------------------------------------------------

def save_preprocessed(texts: list[str], split: str) -> Path:
    """Pickle a list of preprocessed texts to ``data/preprocessed_ro_{split}.pkl``."""
    path = DATA_DIR / f"preprocessed_ro_{split}.pkl"
    save_pickle_cache(texts, path)
    print(f"[dataset_ro] Saved preprocessed {split} texts → {path}")
    return path


def load_preprocessed(split: str) -> list[str] | None:
    """Load cached preprocessed texts, or return None if cache is missing."""
    path = DATA_DIR / f"preprocessed_ro_{split}.pkl"
    texts = load_pickle_cache(path)
    if texts is not None:
        print(f"[dataset_ro] Loaded preprocessed {split} texts from cache ({len(texts):,} items)")
    return texts


# ---------------------------------------------------------------------------
# CLI entry point — run as: python dataset_ro.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Romanian Dataset Setup")
    print("=" * 60)
    df_train, df_val, df_test = load_splits()
    print("\nClass distribution in each split:")
    for name, df in [("train", df_train), ("val", df_val), ("test", df_test)]:
        counts = df["label"].value_counts().rename({0: "negative", 1: "positive", 2: "neutral"})
        print(f"  {name:5s}: {counts.to_dict()}")
    print("\nDone. data/ro_article_reviews/ro_articles.csv is ready for use by training scripts.")
