import os
import sys
import json
import argparse
import torch
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import classification_report

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils import (
    set_seed, load_csv, split_dataset, compute_metrics,
    save_metrics, plot_confusion_matrix, build_lime_explainer,
    run_lime_explanations, run_shap_explanations
)

def parse_args():
    parser = argparse.ArgumentParser(description="Train RoBERTa on Romanian Emotion dataset")
    default_data_path = os.path.join(parent_dir, "data", "romanian_emotion", "romanian_emotion.csv")
    default_output_dir = os.path.join(parent_dir, "outputs", "roberta_romanian_emotion")
    parser.add_argument("--data_path", type=str, default=default_data_path, help="Path to Romanian Emotion CSV file")
    parser.add_argument("--output_dir", type=str, default=default_output_dir, help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--max_length", type=int, default=128, help="Max token length")
    parser.add_argument("--sample_size", type=int, default=0, help="If >0, use a subset of data for quick testing")
    parser.add_argument("--text_column", type=str, default="text", help="Name of text column in CSV")
    parser.add_argument("--label_column", type=str, default="emotion", help="Name of label column in CSV")
    
    parser.add_argument("--run_lime", type=str, default="false", choices=["true", "false"], help="Run LIME explanations")
    parser.add_argument("--run_shap", type=str, default="false", choices=["true", "false"], help="Run SHAP explanations")
    parser.add_argument("--num_explainer_samples", type=int, default=5, help="Number of samples to explain")
    return parser.parse_args()

def prepare_data(args, output_dir):
    df = load_csv(args.data_path, args.text_column, args.label_column, sample_size=args.sample_size)
    
    # Encode labels
    label_encoder = LabelEncoder()
    df['encoded_label'] = label_encoder.fit_transform(df[args.label_column])
    
    # Save label mapping
    mapping = {int(k): str(v) for k, v in enumerate(label_encoder.classes_)}
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "label_mapping.json"), "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=4)
        
    num_labels = len(label_encoder.classes_)
    class_names = list(label_encoder.classes_)
    
    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels = split_dataset(
        df, args.text_column, 'encoded_label'
    )
    
    return train_texts, val_texts, test_texts, train_labels, val_labels, test_labels, num_labels, class_names

class EmotionDataset(torch.utils.data.Dataset):
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
    # We want weighted F1, but we can return macro too by calling it twice
    res = compute_metrics(labels, predictions, average='weighted')
    
    # Adding macro F1
    from sklearn.metrics import f1_score
    res['f1_macro'] = f1_score(labels, predictions, average='macro', zero_division=0)
    return res

def main():
    args = parse_args()
    set_seed(42)
    os.makedirs(args.output_dir, exist_ok=True)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 1. Load Data
    print("Loading data...")
    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels, num_labels, class_names = prepare_data(args, args.output_dir)
    print(f"Detected {num_labels} classes: {class_names}")

    # 2. Tokenize
    model_name = "readerbench/RoBERT-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=args.max_length)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=args.max_length)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=args.max_length)

    train_dataset = EmotionDataset(train_encodings, train_labels)
    val_dataset = EmotionDataset(val_encodings, val_labels)
    test_dataset = EmotionDataset(test_encodings, test_labels)

    # 3. Model
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    
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
    
    metrics = compute_metrics_wrapper((test_results.predictions, test_labels))
    save_metrics(metrics, args.output_dir, "test_metrics.json")
    print("Test Metrics:", metrics)

    # Classification report
    report = classification_report(test_labels, y_pred, target_names=class_names)
    print("Classification Report:")
    print(report)
    with open(os.path.join(args.output_dir, "classification_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

    plot_confusion_matrix(test_labels, y_pred, class_names, args.output_dir, "test_confusion_matrix.png")

    # 6. Save Model
    print("Saving final model...")
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # 7. Interpretability
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
