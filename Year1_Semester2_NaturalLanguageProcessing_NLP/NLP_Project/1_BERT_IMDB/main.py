import os
import gc
import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

class IMDBDataset(torch.utils.data.Dataset):
    """
    Custom PyTorch Dataset class for IMDB text classification.
    """
    def __init__(self, encodings, labels):
        """
        Initializes the dataset object with tokenized encodings and integer labels.
        """
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        """
        Retrieves a single data sample and its corresponding label at the specified index.
        Converts the data into PyTorch tensors required for model input.
        """
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        """
        Calculates and returns the total number of samples in the dataset.
        """
        return len(self.labels)

def compute_metrics(eval_pred):
    """
    Calculates accuracy, precision, recall, and F1 score for the model predictions.
    """
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='binary')
    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def load_and_prepare_data(file_path):
    """
    Loads the CSV dataset, maps string sentiments to binary integers, and removes invalid rows.
    """
    df = pd.read_csv(file_path)
    
    # Map 'positive' to 1 and 'negative' to 0
    df['sentiment'] = df['sentiment'].str.lower().map({'positive': 1, 'negative': 0})
    df = df.dropna(subset=['sentiment'])
    df['sentiment'] = df['sentiment'].astype(int)
    
    texts = df['review'].tolist()
    labels = df['sentiment'].tolist()
    
    return texts, labels

def main():
    """
    Executes the 5-fold cross-validation training and evaluation pipeline for BERT.
    """
    # Configuration parameters
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "IMDB_Dataset.csv")
    model_name = "bert-base-uncased"
    max_length = 128  # Truncates text to speed up training; increase to 256 or 512 if hardware permits.
    batch_size = 16   # Optimized for 8GB VRAM (RTX 4060).
    epochs_per_fold = 2 # Reduced epochs per fold to save overall time.
    n_splits = 5

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Hardware device in use: {device}")

    print("Loading dataset...")
    texts, labels = load_and_prepare_data(data_path)
    texts = np.array(texts)
    labels = np.array(labels)

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Initialize 5-Fold Cross Validation
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    fold_metrics = []

    for fold, (train_index, val_index) in enumerate(skf.split(texts, labels)):
        print(f"\n========== Starting Fold {fold + 1} / {n_splits} ==========")
        
        train_texts, val_texts = texts[train_index].tolist(), texts[val_index].tolist()
        train_labels, val_labels = labels[train_index].tolist(), labels[val_index].tolist()

        print("Tokenizing text data...")
        train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=max_length)
        val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=max_length)

        train_dataset = IMDBDataset(train_encodings, train_labels)
        val_dataset = IMDBDataset(val_encodings, val_labels)

        print("Initializing model...")
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
        model.to(device)

        training_args = TrainingArguments(
            output_dir=f"./results_fold_{fold+1}",
            num_train_epochs=epochs_per_fold,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=2e-5,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            fp16=True, # Enables Mixed Precision to drastically speed up training on RTX 4060
            logging_steps=50,
            report_to="none" # Disables third-party logging to keep the console clean
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=compute_metrics
        )

        print("Beginning training...")
        trainer.train()

        print("Evaluating fold...")
        metrics = trainer.evaluate()
        fold_metrics.append(metrics)
        print(f"Fold {fold + 1} Metrics: {metrics}")

        # Memory cleanup between folds to prevent Out Of Memory (OOM) errors
        del model
        del trainer
        del train_dataset
        del val_dataset
        torch.cuda.empty_cache()
        gc.collect()

    print("\n========== Cross-Validation Complete ==========")
    avg_accuracy = sum(m['eval_accuracy'] for m in fold_metrics) / n_splits
    avg_f1 = sum(m['eval_f1'] for m in fold_metrics) / n_splits
    print(f"Average Accuracy across 5 folds: {avg_accuracy:.4f}")
    print(f"Average F1 Score across 5 folds: {avg_f1:.4f}")

if __name__ == "__main__":
    main()