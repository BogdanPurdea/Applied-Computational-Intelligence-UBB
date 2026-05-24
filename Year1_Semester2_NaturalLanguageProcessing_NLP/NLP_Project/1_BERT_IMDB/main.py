import os
import sys
import argparse
import torch
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import datasets

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils import (
    set_seed, load_csv, split_dataset, compute_metrics,
    save_metrics, plot_confusion_matrix, build_lime_explainer,
    run_lime_explanations, run_shap_explanations
)

def parse_args():
    parser = argparse.ArgumentParser(description="Train BERT on IMDB dataset")
    default_data_path = os.path.join(current_dir, "IMDB_Dataset.csv")
    default_output_dir = os.path.join(current_dir, "outputs", "bert_imdb")
    parser.add_argument("--data_path", type=str, default=default_data_path, help="Path to IMDB CSV file")
    parser.add_argument("--output_dir", type=str, default=default_output_dir, help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--max_length", type=int, default=128, help="Max token length")
    parser.add_argument("--sample_size", type=int, default=0, help="If >0, use a subset of data for quick testing")
    parser.add_argument("--text_column", type=str, default="review", help="Name of text column in CSV")
    parser.add_argument("--label_column", type=str, default="sentiment", help="Name of label column in CSV")
    
    parser.add_argument("--run_lime", type=str, default="false", choices=["true", "false"], help="Run LIME explanations")
    parser.add_argument("--run_shap", type=str, default="false", choices=["true", "false"], help="Run SHAP explanations")
    parser.add_argument("--num_explainer_samples", type=int, default=5, help="Number of samples to explain")
    return parser.parse_args()

def prepare_data(args):
    df = load_csv(args.data_path, args.text_column, args.label_column, sample_size=args.sample_size)
    
    # Map sentiment
    if df[args.label_column].dtype == object or df[args.label_column].dtype == str:
        # Assuming typical IMDB: positive -> 1, negative -> 0
        df[args.label_column] = df[args.label_column].str.lower().map({'positive': 1, 'negative': 0})
        # Drop rows where mapping failed
        df = df.dropna(subset=[args.label_column])
        df[args.label_column] = df[args.label_column].astype(int)

    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels = split_dataset(
        df, args.text_column, args.label_column
    )
    return train_texts, val_texts, test_texts, train_labels, val_labels, test_labels

class SimpleDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def compute_metrics_wrapper(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return compute_metrics(labels, predictions, average='binary')

def main():
    args = parse_args()
    set_seed(42)
    os.makedirs(args.output_dir, exist_ok=True)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 1. Load Data
    print("Loading data...")
    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels = prepare_data(args)

    # 2. Tokenize
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=args.max_length)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=args.max_length)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=args.max_length)

    train_dataset = SimpleDataset(train_encodings, train_labels)
    val_dataset = SimpleDataset(val_encodings, val_labels)
    test_dataset = SimpleDataset(test_encodings, test_labels)

    # 3. Model
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # 4. Train
    training_args = TrainingArguments(
        output_dir=os.path.join(args.output_dir, "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir=os.path.join(args.output_dir, "logs"),
        logging_steps=10,
        seed=42
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics_wrapper
    )

    print("Starting training...")
    trainer.train()

    # 5. Evaluate
    print("Evaluating on test set...")
    test_results = trainer.predict(test_dataset)
    y_pred = np.argmax(test_results.predictions, axis=1)
    
    metrics = compute_metrics(test_labels, y_pred, average='binary')
    save_metrics(metrics, args.output_dir, "test_metrics.json")
    print("Test Metrics:", metrics)

    class_names = ['negative', 'positive']
    plot_confusion_matrix(test_labels, y_pred, class_names, args.output_dir, "test_confusion_matrix.png")

    # 6. Save Model
    print("Saving final model...")
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # 7. Interpretability
    # Create a prediction wrapper that takes a list of strings and returns probability array
    def predict_proba(texts):
        encodings = tokenizer(texts, truncation=True, padding=True, max_length=args.max_length, return_tensors="pt").to(device)
        model.to(device)
        model.eval()
        with torch.no_grad():
            outputs = model(**encodings)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return probs.cpu().numpy()

    if args.run_lime == "true":
        print("Running LIME explanations...")
        lime_explainer = build_lime_explainer(class_names)
        run_lime_explanations(
            lime_explainer, predict_proba, test_texts, 
            num_samples=args.num_explainer_samples, 
            output_dir=os.path.join(args.output_dir, "lime_explanations")
        )

    if args.run_shap == "true":
        print("Running SHAP explanations...")
        run_shap_explanations(
            predict_proba, test_texts, 
            num_samples=args.num_explainer_samples, 
            output_dir=os.path.join(args.output_dir, "shap_explanations")
        )

    print("Done!")

if __name__ == "__main__":
    main()
