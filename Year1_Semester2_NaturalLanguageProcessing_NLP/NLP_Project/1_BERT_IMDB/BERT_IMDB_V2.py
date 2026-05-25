import os
import gc
import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from lime.lime_text import LimeTextExplainer
import shap

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
    df['sentiment'] = df['sentiment'].str.lower().map({'positive': 1, 'negative': 0})
    df = df.dropna(subset=['sentiment'])
    df['sentiment'] = df['sentiment'].astype(int)
    
    texts = df['review'].tolist()
    labels = df['sentiment'].tolist()
    return texts, labels

def main():
    """
    Executes the 5-fold cross-validation training pipeline for BERT and performs
    interpretability analysis using LIME and SHAP frameworks.
    """
    # Verify hardware configuration
    if torch.backends.mps.is_available():
        device = "mps"
        print(f"Hardware device confirmed: Apple Silicon ({device})")
    elif torch.cuda.is_available():
        device = "cuda"
        print(f"Hardware device confirmed: NVIDIA ({device})")
    else:
        device = "cpu"
        print("WARNING: GPU not detected. Falling back to CPU. Training will be slow.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "IMDB_Dataset.csv")
    
    model_name = "bert-base-uncased"
    max_length = 128
    batch_size = 16
    epochs_per_fold = 2
    n_splits = 5

    print("Loading dataset...")
    texts, labels = load_and_prepare_data(data_path)
    texts = np.array(texts)
    labels = np.array(labels)

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    fold_metrics = []

    # Reference variables to store the final fold items for demonstration purposes
    final_model = None
    final_trainer = None

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
            output_dir=os.path.join(script_dir, f"results_fold_{fold+1}"),
            num_train_epochs=epochs_per_fold,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=2e-5,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            fp16=(device == "cuda"), # Enable mixed precision training only for NVIDIA CUDA devices
            dataloader_num_workers=0,
            gradient_accumulation_steps=2,
            logging_steps=50,
            report_to="none"
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

        # Retain references to the final model to execute explainability functions
        if fold == (n_splits - 1):
            final_model = model
            final_trainer = trainer
        else:
            del model
            del trainer
            torch.cuda.empty_cache()
            gc.collect()

    print("\n========== Cross-Validation Complete ==========")
    avg_accuracy = sum(m['eval_accuracy'] for m in fold_metrics) / n_splits
    print(f"Average Accuracy across 5 folds: {avg_accuracy:.4f}")

    # ==========================================
    # Model Interpretability Section (LIME & SHAP)
    # ==========================================
    print("\n========== Initializing Model Interpretability ==========")
    
    class_names = ['negative', 'positive']
    
    def predict_proba(text_list):
        """
        Prediction function formatted specifically for LIME and SHAP APIs.
        Accepts a list of strings and outputs a numpy array of confidence scores.
        """
        final_model.eval()
        inputs = tokenizer(text_list, truncation=True, padding=True, max_length=max_length, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = final_model(**inputs)
            scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
        return scores.cpu().numpy()

    # Define a sample review text to use for explanations
    sample_review = "This movie had a fantastic script and brilliant acting, but the ending was terrible and slow."
    print(f"Generating explanations for sample review:\n'{sample_review}'")

    # 1. Generate LIME Explanation
    print("\nRunning LIME explanation...")
    lime_explainer = LimeTextExplainer(class_names=class_names)
    lime_exp = lime_explainer.explain_instance(sample_review, predict_proba, num_features=6)
    
    lime_output_path = os.path.join(script_dir, "lime_explanation.html")
    lime_exp.save_to_file(lime_output_path)
    print(f"LIME analysis complete. Results saved to: {lime_output_path}")

    # 2. Generate SHAP Explanation
    print("\nRunning SHAP explanation...")
    # Uses a text explainer with the defined prediction function and token pattern
    shap_explainer = shap.Explainer(predict_proba, masker=shap.maskers.Text(tokenizer=r"\W+"), output_names=class_names)
    shap_values = shap_explainer([sample_review])
    
    # Extract structural prediction values for class 1 (positive sentiment)
    print("SHAP Base Value (Expected Average Output):", shap_values.base_values[0][1])
    print("SHAP Word Contribution Values:\n", list(zip(shap_values.data[0], shap_values.values[0][:, 1])))

    print("\nProcess finished successfully.")

if __name__ == "__main__":
    main()