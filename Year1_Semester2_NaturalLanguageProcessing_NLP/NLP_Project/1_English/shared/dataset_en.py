"""
dataset.py
==========
Download, extract, and cache the IMDB 50k Movie Reviews dataset.

This module is the single source of truth for dataset access across all
training and evaluation scripts. It handles the quirk where kagglehub
returns a ZIP-compressed file with a .csv extension.

Usage
-----
    # One-time extraction (idempotent):
    from dataset import download_and_extract, load_splits
    download_and_extract()

    # In any training script:
    df_train, df_val, df_test = load_splits()

Dataset
-------
Source : https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews
Rows   : 50,000  (25,000 positive / 25,000 negative — perfectly balanced)
Columns: review (str), sentiment (str: "positive"/"negative"), label (int: 1/0)
Split  : 70 % train / 15 % val / 15 % test  (stratified on label)
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import kagglehub
import pandas as pd

# Add project root and shared/migrated to path so we can do imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "shared" / "migrated"))
from dataset_utils import perform_stratified_split, save_pickle_cache, load_pickle_cache

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DATA_DIR = project_root / "Datasets" / "migrated" / "imdb_movie_reviews"
CSV_PATH = DATA_DIR / "imdb.csv"

DATASET_SLUG = "lakshmi25npathi/imdb-dataset-of-50k-movie-reviews"

# Default split ratios (must sum to 1.0)
DEFAULT_TRAIN_RATIO = 0.70
DEFAULT_VAL_RATIO = 0.15
DEFAULT_TEST_RATIO = 0.15
DEFAULT_SEED = 42


# ---------------------------------------------------------------------------
# Download & extraction
# ---------------------------------------------------------------------------

def download_and_extract(force: bool = False) -> Path:
    """Download the IMDB dataset via kagglehub and save as a plain UTF-8 CSV.

    kagglehub caches downloads locally, so network I/O only happens once.
    The raw file returned is a ZIP archive with a .csv extension; this
    function transparently extracts the inner CSV and saves it to
    ``data/imdb.csv`` with a ``label`` column (1 = positive, 0 = negative).

    Args:
        force: Re-download and overwrite even if ``data/imdb.csv`` exists.

    Returns:
        Path to the saved CSV file.
    """
    if CSV_PATH.exists() and not force:
        print(f"[dataset] Already cached → {CSV_PATH}  ({_row_count(CSV_PATH):,} rows)")
        return CSV_PATH

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("[dataset] Downloading via kagglehub (cached after first run)…")
    raw_dir = Path(kagglehub.dataset_download(DATASET_SLUG))
    print(f"[dataset] kagglehub path: {raw_dir}")

    # Locate the (possibly ZIP-wrapped) CSV
    csv_files = list(raw_dir.glob("*.csv"))
    assert csv_files, f"No .csv file found under {raw_dir}"
    raw_csv = csv_files[0]

    # Read — handle both plain CSV and ZIP-wrapped CSV
    if zipfile.is_zipfile(raw_csv):
        print(f"[dataset] Extracting inner CSV from ZIP: {raw_csv.name}")
        with zipfile.ZipFile(raw_csv) as zf:
            inner_name = next(n for n in zf.namelist() if n.endswith(".csv"))
            with zf.open(inner_name) as f:
                df = pd.read_csv(f)
    else:
        df = pd.read_csv(raw_csv)

    # Validate expected columns
    assert "review" in df.columns and "sentiment" in df.columns, (
        f"Expected columns 'review' and 'sentiment', got: {list(df.columns)}"
    )

    # Add integer label column  (1 = positive, 0 = negative)
    df["label"] = (df["sentiment"].str.lower() == "positive").astype(int)

    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"[dataset] Saved {len(df):,} rows → {CSV_PATH}")
    return CSV_PATH


# ---------------------------------------------------------------------------
# Split loader
# ---------------------------------------------------------------------------

def load_splits(
    seed: int = DEFAULT_SEED,
    train_ratio: float = DEFAULT_TRAIN_RATIO,
    val_ratio: float = DEFAULT_VAL_RATIO,
    test_ratio: float = DEFAULT_TEST_RATIO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the full IMDB dataset and return stratified train/val/test splits.

    Automatically calls :func:`download_and_extract` if the cached CSV does
    not yet exist.

    The split is **stratified on the label column** to ensure each split has
    the same positive/negative ratio as the full dataset (50 / 50).

    Args:
        seed:        Random seed for reproducibility.
        train_ratio: Fraction of data used for training.
        val_ratio:   Fraction used for validation.
        test_ratio:  Fraction used for testing.

    Returns:
        Tuple of ``(df_train, df_val, df_test)`` DataFrames, each with
        columns ``review``, ``sentiment``, ``label``.

    Raises:
        AssertionError: If ratios do not sum to approximately 1.0.
    """
    if not CSV_PATH.exists():
        download_and_extract()

    df = pd.read_csv(CSV_PATH)

    df_train, df_val, df_test = perform_stratified_split(
        df, "label", seed, train_ratio, val_ratio, test_ratio
    )

    print(
        f"[dataset] Splits — "
        f"train: {len(df_train):,}  "
        f"val: {len(df_val):,}  "
        f"test: {len(df_test):,}"
    )
    return df_train, df_val, df_test


# ---------------------------------------------------------------------------
# Preprocessed text cache helpers
# ---------------------------------------------------------------------------

def save_preprocessed(texts: list[str], split: str) -> Path:
    """Pickle a list of preprocessed texts to ``data/preprocessed_{split}.pkl``.

    Avoids re-running the CPU-intensive preprocessing pipeline on every run.

    Args:
        texts: List of cleaned text strings.
        split: One of ``"train"``, ``"val"``, ``"test"``.

    Returns:
        Path to the saved pickle file.
    """
    path = DATA_DIR / f"preprocessed_{split}.pkl"
    save_pickle_cache(texts, path)
    print(f"[dataset] Saved preprocessed {split} texts → {path}")
    return path


def load_preprocessed(split: str) -> list[str] | None:
    """Load cached preprocessed texts, or return None if cache is missing.

    Args:
        split: One of ``"train"``, ``"val"``, ``"test"``.

    Returns:
        List of cleaned text strings, or ``None`` if not yet cached.
    """
    path = DATA_DIR / f"preprocessed_{split}.pkl"
    texts = load_pickle_cache(path)
    if texts is not None:
        print(f"[dataset] Loaded preprocessed {split} texts from cache ({len(texts):,} items)")
    return texts


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _row_count(path: Path) -> int:
    """Count rows in a CSV file without loading all columns into memory."""
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f) - 1  # subtract header


# ---------------------------------------------------------------------------
# CLI entry point — run as: python dataset.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("IMDB Dataset Setup")
    print("=" * 60)
    download_and_extract()
    df_train, df_val, df_test = load_splits()
    print("\nClass distribution in each split:")
    for name, df in [("train", df_train), ("val", df_val), ("test", df_test)]:
        counts = df["label"].value_counts().rename({0: "negative", 1: "positive"})
        print(f"  {name:5s}: {counts.to_dict()}")
    print("\nDone. data/imdb_movie_reviews/imdb.csv is ready for use by training scripts.")
