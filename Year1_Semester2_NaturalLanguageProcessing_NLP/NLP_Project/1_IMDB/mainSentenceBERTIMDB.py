import os
import sys
import time
import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import numpy as np
from transformers import AutoTokenizer

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from shared.utils import setup_logging, set_seed, save_json
from shared.dataset_utils import load_csv, split_dataset
from shared.metrics import compute_classification_metrics
from shared.visualization import plot_confusion_matrix, plot_roc_curve, plot_training_history
from shared.explainability import run_lime_explanations, run_shap_explanations
from shared.model_utils import get_device, SBERTClassifier

def parse_args():
    parser = argparse.ArgumentParser(description="Train Sentence-BERT on IMDB dataset")
    parser.add_argument("--data_path", type=str, default=os.path.join(parent_dir, "data", "imdb", "IMDB_Dataset.csv"))
    parser.add_argument("--output_dir", type=str, default=os.path.join(parent_dir, "outputs", "SentenceBERT_IMDB"))
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--learning_rate", type=float, default=1e-3)
    parser.add_argument("--max_length", type=int, default=128)
    parser.add_argument("--sample_size", type=int, default=0)
    parser.add_argument("--run_lime", type=str, default="false", choices=["true", "false"])
    parser.add_argument("--run_shap", type=str, default="false", choices=["true", "false"])
    parser.add_argument("--num_explainer_samples", type=int, default=5)
    parser.add_argument("--freeze_encoder", action="store_true")
    return parser.parse_args()

class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        encoding = self.tokenizer(
            text, add_special_tokens=True, max_length=self.max_length,
            padding='max_length', truncation=True, return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

    def __len__(self):
        return len(self.labels)

def train_model(model, train_loader, val_loader, args, device, logger):
    criterion = nn.CrossEntropyLoss()
    if args.freeze_encoder:
        optimizer = torch.optim.AdamW(model.classifier.parameters(), lr=args.learning_rate)
    else:
        optimizer = torch.optim.AdamW([
            {'params': model.encoder.parameters(), 'lr': 2e-5},
            {'params': model.classifier.parameters(), 'lr': args.learning_rate}
        ])
        
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=1, factor=0.5)
    
    best_val_loss = float('inf')
    early_stopping_patience = 2
    epochs_no_improve = 0
    
    train_losses = []
    val_losses = []

    for epoch in range(args.epochs):
        model.train()
        train_loss = 0
        for batch in train_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            optimizer.zero_grad()
            logits = model(input_ids, attention_mask)
            loss = criterion(logits, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
            
        train_loss /= len(train_loader)
        train_losses.append(train_loss)
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                logits = model(input_ids, attention_mask)
                loss = criterion(logits, labels)
                val_loss += loss.item()
                
        val_loss /= len(val_loader)
        val_losses.append(val_loss)
        scheduler.step(val_loss)
        
        logger.info(f"Epoch {epoch+1}/{args.epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f}")
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_no_improve = 0
            torch.save(model.state_dict(), os.path.join(args.output_dir, "best_model.pt"))
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= early_stopping_patience:
                logger.info("Early stopping triggered!")
                break
                
    return train_losses, val_losses

def evaluate_model(model, test_loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    all_probs = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].cpu().numpy()
            logits = model(input_ids, attention_mask)
            probs = torch.nn.functional.softmax(logits, dim=-1).cpu().numpy()
            preds = np.argmax(probs, axis=1)
            
            all_preds.extend(preds)
            all_labels.extend(labels)
            all_probs.extend(probs)
            
    return np.array(all_labels), np.array(all_preds), np.array(all_probs)

def main():
    args = parse_args()
    set_seed(42)
    logger = setup_logging(args.output_dir)
    device = get_device()
    logger.info(f"Using device: {device}")

    # 1. Load Data
    logger.info("Loading IMDB Data...")
    df, text_col = load_csv(args.data_path, text_col="review", label_col="sentiment", sample_size=args.sample_size)
    if df['sentiment'].dtype == object or df['sentiment'].dtype == str:
        df['sentiment'] = df['sentiment'].str.lower().map({'positive': 1, 'negative': 0})
        df = df.dropna(subset=['sentiment'])
        df['sentiment'] = df['sentiment'].astype(int)

    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels = split_dataset(df, text_col, 'sentiment')

    # 2. Tokenize & Dataloaders
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    train_dataset = TextDataset(train_texts, train_labels, tokenizer, args.max_length)
    val_dataset = TextDataset(val_texts, val_labels, tokenizer, args.max_length)
    test_dataset = TextDataset(test_texts, test_labels, tokenizer, args.max_length)
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size)

    # 3. Model
    model = SBERTClassifier(model_name, num_classes=2, freeze_encoder=args.freeze_encoder)
    model.to(device)

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

    # 4. Train
    logger.info("Starting training...")
    start_time = time.time()
    train_losses, val_losses = train_model(model, train_loader, val_loader, args, device, logger)
    train_time = time.time() - start_time
    mem_usage = torch.cuda.max_memory_allocated() / (1024 ** 2) if torch.cuda.is_available() else 0

    plot_training_history(train_losses, val_losses, args.output_dir)

    # 5. Evaluate
    logger.info("Loading best model for evaluation...")
    model.load_state_dict(torch.load(os.path.join(args.output_dir, "best_model.pt")))
    
    logger.info("Evaluating on test set...")
    inf_start = time.time()
    y_true, y_pred, y_probs = evaluate_model(model, test_loader, device)
    inf_time = time.time() - inf_start
    
    np.save(os.path.join(args.output_dir, "test_probs.npy"), y_probs)
    np.save(os.path.join(args.output_dir, "test_labels.npy"), y_true)

    metrics = compute_classification_metrics(y_true, y_pred, y_probs=y_probs, average='binary')
    metrics['train_time_sec'] = train_time
    metrics['inference_time_sec'] = inf_time
    metrics['peak_memory_mb'] = mem_usage
    
    save_json(metrics, os.path.join(args.output_dir, "metrics.json"))
    logger.info(f"Test Metrics: {metrics}")

    class_names = ['negative', 'positive']
    plot_confusion_matrix(y_true, y_pred, class_names, args.output_dir)
    plot_roc_curve(y_true, y_probs, args.output_dir, class_names=class_names)

    # Save tokenizer
    tokenizer.save_pretrained(args.output_dir)
    
    from sklearn.metrics import classification_report
    report = classification_report(y_true, y_pred, target_names=class_names)
    with open(os.path.join(args.output_dir, "classification_report.txt"), "w", encoding="utf-8") as f:
        f.write(report)

    # 6. Interpretability
    def predict_proba(texts):
        model.eval()
        all_probs = []
        for i in range(0, len(texts), args.batch_size):
            batch_texts = texts[i:i+args.batch_size]
            encodings = tokenizer(
                batch_texts, truncation=True, padding=True, 
                max_length=args.max_length, return_tensors="pt"
            ).to(device)
            with torch.no_grad():
                logits = model(encodings['input_ids'], encodings['attention_mask'])
                probs = torch.nn.functional.softmax(logits, dim=-1)
                all_probs.extend(probs.cpu().numpy())
        return np.array(all_probs)

    if args.run_lime == "true":
        logger.info("Running LIME explanations...")
        run_lime_explanations(predict_proba, test_texts, class_names, args.num_explainer_samples, os.path.join(args.output_dir, "lime"))

    if args.run_shap == "true":
        logger.info("Running SHAP explanations...")
        run_shap_explanations(predict_proba, test_texts, args.num_explainer_samples, os.path.join(args.output_dir, "shap"))

if __name__ == "__main__":
    main()
