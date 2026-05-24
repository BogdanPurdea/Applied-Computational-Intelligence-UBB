import os
import pandas as pd
from sklearn.model_selection import train_test_split

def load_csv(path: str, text_col: str, label_col: str, sample_size: int = None, text_col_2: str = None):
    """Loads CSV and handles missing values. Can combine two text columns if text_col_2 is provided."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
        
    df = pd.read_csv(path)
    
    if text_col not in df.columns:
        raise ValueError(f"Text column '{text_col}' not found.")
    if label_col not in df.columns:
        raise ValueError(f"Label column '{label_col}' not found.")
        
    # Drop rows where label is missing
    df = df.dropna(subset=[label_col])
    
    if text_col_2 and text_col_2 in df.columns:
        df[text_col] = df[text_col].fillna("")
        df[text_col_2] = df[text_col_2].fillna("")
        df['combined_text'] = df[text_col].astype(str) + " " + df[text_col_2].astype(str)
        text_col = 'combined_text'
    else:
        df = df.dropna(subset=[text_col])
        
    if sample_size and sample_size > 0:
        df = df.sample(n=min(sample_size, len(df)), random_state=42)
        
    return df, text_col

def split_dataset(df: pd.DataFrame, text_col: str, label_col: str, test_size=0.2, val_size=0.1):
    """Splits dataset into train, val, test."""
    texts = df[text_col].tolist()
    labels = df[label_col].tolist()
    
    # Train + Val / Test split
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        texts, labels, test_size=test_size, random_state=42, stratify=labels
    )
    
    # Train / Val split
    val_ratio = val_size / (1.0 - test_size)
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_texts, train_labels, test_size=val_ratio, random_state=42, stratify=train_labels
    )
    
    return train_texts, val_texts, test_texts, train_labels, val_labels, test_labels
