import os
import sys
import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModel

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils import (
    set_seed, load_csv, split_dataset, compute_metrics,
    save_metrics, plot_confusion_matrix, build_lime_explainer,
    run_lime_explanations, run_shap_explanations
)

def parse_args():
    parser = argparse.ArgumentParser(description="Train Sentence-BERT + MLP on WELFake dataset")
    default_data_path = os.path.join(parent_dir, "data", "welfake", "WELFake_Dataset.csv")
    default_output_dir = os.path.join(parent_dir, "outputs", "sentencebert_welfake")
    parser.add_argument("--data_path", type=str, default=default_data_path, help="Path to WELFake CSV file")
    parser.add_argument("--output_dir", type=str, default=default_output_dir, help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--learning_rate", type=float, default=1e-3, help="Learning rate for MLP (encoder may have different LR if un-frozen)")
    parser.add_argument("--max_length", type=int, default=128, help="Max token length")
    parser.add_argument("--sample_size", type=int, default=0, help="If >0, use a subset of data for quick testing")
    parser.add_argument("--title_column", type=str, default="title", help="Name of title column in CSV")
    parser.add_argument("--text_column", type=str, default="text", help="Name of text column in CSV")
    parser.add_argument("--label_column", type=str, default="label", help="Name of label column in CSV")
    parser.add_argument("--freeze_encoder", action="store_true", help="Freeze the Sentence-BERT encoder")
    
    parser.add_argument("--run_lime", type=str, default="false", choices=["true", "false"], help="Run LIME explanations")
    parser.add_argument("--run_shap", type=str, default="false", choices=["true", "false"], help="Run SHAP explanations")
    parser.add_argument("--num_explainer_samples", type=int, default=5, help="Number of samples to explain")
    return parser.parse_args()

def load_welfake_data(args):
    if not os.path.exists(args.data_path):
        raise FileNotFoundError(f"Data file not found: {args.data_path}")
    df = pd.read_csv(args.data_path)
    
    # Combine title and text if they exist
    has_title = args.title_column in df.columns
    has_text = args.text_column in df.columns
    
    if not (has_title or has_text):
        raise ValueError(f"Neither '{args.title_column}' nor '{args.text_column}' found in the dataset.")
    if args.label_column not in df.columns:
        raise ValueError(f"Label column '{args.label_column}' not found.")
        
    df[args.label_column] = pd.to_numeric(df[args.label_column], errors='coerce')
    df = df.dropna(subset=[args.label_column])
    df[args.label_column] = df[args.label_column].astype(int)
    
    # Fill NAs in text/title with empty string
    if has_title:
        df[args.title_column] = df[args.title_column].fillna("")
    if has_text:
        df[args.text_column] = df[args.text_column].fillna("")
        
    if has_title and has_text:
        df['combined_text'] = df[args.title_column].astype(str) + " " + df[args.text_column].astype(str)
    elif has_title:
        df['combined_text'] = df[args.title_column].astype(str)
    else:
        df['combined_text'] = df[args.text_column].astype(str)
        
    if args.sample_size and args.sample_size > 0:
        df = df.sample(n=min(args.sample_size, len(df)), random_state=42)
        
    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels = split_dataset(
        df, 'combined_text', args.label_column
    )
    return train_texts, val_texts, test_texts, train_labels, val_labels, test_labels

class SBERTClassifier(nn.Module):
    def __init__(self, model_name, num_classes=2, freeze_encoder=True):
        super(SBERTClassifier, self).__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        
        # Structure allowing unfreezing
        if freeze_encoder:
            for param in self.encoder.parameters():
                param.requires_grad = False
        else:
            for param in self.encoder.parameters():
                param.requires_grad = True
                
        hidden_size = self.encoder.config.hidden_size
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, input_ids, attention_mask):
        # Mean pooling
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        pooled_output = sum_embeddings / sum_mask
        
        logits = self.classifier(pooled_output)
        return logits

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
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

    def __len__(self):
        return len(self.labels)

def train_model(model, train_loader, val_loader, args, device):
    criterion = nn.CrossEntropyLoss()
    # Use different learning rates if encoder is unfrozen
    if args.freeze_encoder:
        optimizer = torch.optim.AdamW(model.classifier.parameters(), lr=args.learning_rate)
    else:
        optimizer = torch.optim.AdamW([
            {'params': model.encoder.parameters(), 'lr': 2e-5},
            {'params': model.classifier.parameters(), 'lr': args.learning_rate}
        ])

    best_val_loss = float('inf')
    
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
            optimizer.step()
            train_loss += loss.item()
            
        train_loss /= len(train_loader)
        
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
        print(f"Epoch {epoch+1}/{args.epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f}")
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), os.path.join(args.output_dir, "best_model.pt"))

def evaluate_model(model, test_loader, device):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].cpu().numpy()
            logits = model(input_ids, attention_mask)
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels)
            
    return np.array(all_labels), np.array(all_preds)

def main():
    args = parse_args()
    set_seed(42)
    os.makedirs(args.output_dir, exist_ok=True)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 1. Load Data
    print("Loading data...")
    train_texts, val_texts, test_texts, train_labels, val_labels, test_labels = load_welfake_data(args)

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

    # 4. Train
    print("Starting training...")
    train_model(model, train_loader, val_loader, args, device)

    # 5. Evaluate
    print("Loading best model for evaluation...")
    model.load_state_dict(torch.load(os.path.join(args.output_dir, "best_model.pt")))
    
    print("Evaluating on test set...")
    y_true, y_pred = evaluate_model(model, test_loader, device)
    
    metrics = compute_metrics(y_true, y_pred, average='binary')
    save_metrics(metrics, args.output_dir, "test_metrics.json")
    print("Test Metrics:", metrics)

    class_names = ['real', 'fake'] # real=0, fake=1
    plot_confusion_matrix(y_true, y_pred, class_names, args.output_dir, "test_confusion_matrix.png")

    # Save tokenizer for inference later
    tokenizer.save_pretrained(args.output_dir)

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
