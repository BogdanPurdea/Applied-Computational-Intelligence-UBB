import os
import sys
import time
import argparse
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, EarlyStoppingCallback
import datasets

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from shared.utils import setup_logging, set_seed, save_json
from shared.dataset_utils import load_csv, split_dataset
from shared.metrics import compute_classification_metrics
from shared.visualization import plot_confusion_matrix, plot_roc_curve, plot_training_history
from shared.explainability import run_lime_explanations, run_shap_explanations
from shared.model_utils import get_device

def parse_args():
    parser = argparse.ArgumentParser(description="Train BERT on IMDB dataset")
    parser.add_argument("--data_path", type=str, default=os.path.join(parent_dir, "data", "IMDB_Dataset.csv"))
    parser.add_argument("--output_dir", type=str, default=os.path.join(parent_dir, "outputs", "BERT_IMDB"))
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    parser.add_argument("--max_length", type=int, default=128)
    parser.add_argument("--sample_size", type=int, default=0)
    parser.add_argument("--run_lime", type=str, default="false", choices=["true", "false"])
    parser.add_argument("--run_shap", type=str, default="false", choices=["true", "false"])
    parser.add_argument("--num_explainer_samples", type=int, default=5)
    return parser.parse_args()

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
    probs = torch.nn.functional.softmax(torch.tensor(logits), dim=-1).numpy()
    return compute_classification_metrics(labels, predictions, y_probs=probs, average='binary')

def main():
    args = parse_args()
    set_seed(42)
    logger = setup_logging(args.output_dir)
    device = get_device()
    logger.info(f"Using device: {device}")

    # Load data
    logger.info("Loading IMDB Data...")
    df, text_col = load_csv(args.data_path, text_col="review", label_col="sentiment", sample_size=args.sample_size)
    if df['sentiment'].dtype == object or df['sentiment'].dtype == str:
        df['sentiment'] = df['sentiment'].str.lower().map({'positive': 1, 'negative': 0})
        df = df.dropna(subset=['sentiment'])
        df['sentiment'] = df['sentiment'].astype(int)

    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels = split_dataset(df, text_col, 'sentiment')

    # Tokenize
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=args.max_length)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=args.max_length)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=args.max_length)

    train_dataset = SimpleDataset(train_encodings, train_labels)
    val_dataset = SimpleDataset(val_encodings, val_labels)
    test_dataset = SimpleDataset(test_encodings, test_labels)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    training_args = TrainingArguments(
        output_dir=os.path.join(args.output_dir, "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_dir=os.path.join(args.output_dir, "logs"),
        logging_steps=10,
        seed=42,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics_wrapper,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    logger.info("Starting Training...")
    start_time = time.time()
    train_result = trainer.train()
    train_time = time.time() - start_time

    mem_usage = torch.cuda.max_memory_allocated() / (1024 ** 2) if torch.cuda.is_available() else 0

    # Extract training history
    log_history = trainer.state.log_history
    train_losses = [x['loss'] for x in log_history if 'loss' in x]
    val_losses = [x['eval_loss'] for x in log_history if 'eval_loss' in x]
    plot_training_history(train_losses, val_losses, args.output_dir)

    # Evaluate
    logger.info("Evaluating...")
    inf_start = time.time()
    test_results = trainer.predict(test_dataset)
    inf_time = time.time() - inf_start

    y_pred = np.argmax(test_results.predictions, axis=1)
    y_probs = torch.nn.functional.softmax(torch.tensor(test_results.predictions), dim=-1).numpy()
    
    # Save raw probs and labels for comparison script
    np.save(os.path.join(args.output_dir, "test_probs.npy"), y_probs)
    np.save(os.path.join(args.output_dir, "test_labels.npy"), test_labels)

    metrics = compute_classification_metrics(test_labels, y_pred, y_probs=y_probs, average='binary')
    metrics['train_time_sec'] = train_time
    metrics['inference_time_sec'] = inf_time
    metrics['peak_memory_mb'] = mem_usage
    
    save_json(metrics, os.path.join(args.output_dir, "metrics.json"))
    logger.info(f"Metrics: {metrics}")

    class_names = ['negative', 'positive']
    plot_confusion_matrix(test_labels, y_pred, class_names, args.output_dir)
    plot_roc_curve(test_labels, y_probs, args.output_dir, class_names=class_names)

    # Classification Report
    from sklearn.metrics import classification_report
    report = classification_report(test_labels, y_pred, target_names=class_names)
    with open(os.path.join(args.output_dir, "classification_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

    # Save Model
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # Explainability
    def predict_proba(texts):
        encodings = tokenizer(texts, truncation=True, padding=True, max_length=args.max_length, return_tensors="pt").to(device)
        model.to(device)
        model.eval()
        with torch.no_grad():
            outputs = model(**encodings)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return probs.cpu().numpy()

    if args.run_lime == "true":
        logger.info("Running LIME...")
        run_lime_explanations(predict_proba, test_texts, class_names, args.num_explainer_samples, os.path.join(args.output_dir, "lime"))

    if args.run_shap == "true":
        logger.info("Running SHAP...")
        run_shap_explanations(predict_proba, test_texts, args.num_explainer_samples, os.path.join(args.output_dir, "shap"))

if __name__ == "__main__":
    main()
