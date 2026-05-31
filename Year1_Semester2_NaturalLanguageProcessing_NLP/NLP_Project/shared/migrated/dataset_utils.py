"""
dataset_utils.py
================
Shared data splitting and pickle caching helpers for the dataset loaders.
"""

from __future__ import annotations

import pickle
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

def perform_stratified_split(
    df: pd.DataFrame,
    label_col: str,
    seed: int,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Perform a stratified split of a DataFrame into train, val, and test splits.

    Args:
        df: Input DataFrame.
        label_col: Name of the column to stratify on.
        seed: Random seed for reproducibility.
        train_ratio: Ratio for the train split.
        val_ratio: Ratio for the val split.
        test_ratio: Ratio for the test split.

    Returns:
        A tuple of (df_train, df_val, df_test).
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, (
        "train_ratio + val_ratio + test_ratio must sum to 1.0"
    )

    # Step 1: carve out test set
    df_train_val, df_test = train_test_split(
        df,
        test_size=test_ratio,
        stratify=df[label_col],
        random_state=seed,
    )

    # Step 2: split remainder into train / val
    val_share = val_ratio / (train_ratio + val_ratio)
    df_train, df_val = train_test_split(
        df_train_val,
        test_size=val_share,
        stratify=df_train_val[label_col],
        random_state=seed,
    )

    return (
        df_train.reset_index(drop=True),
        df_val.reset_index(drop=True),
        df_test.reset_index(drop=True),
    )

def save_pickle_cache(data: any, path: Path) -> Path:
    """Pickle data to the specified path, creating directories if needed.

    Args:
        data: Python object to cache.
        path: Path to the target pickle file.

    Returns:
        The path to the saved file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(data, f)
    return path

def load_pickle_cache(path: Path) -> any | None:
    """Load data from a cached pickle file.

    Args:
        path: Path to the pickle file.

    Returns:
        The loaded object if the file exists, otherwise None.
    """
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return pickle.load(f)
