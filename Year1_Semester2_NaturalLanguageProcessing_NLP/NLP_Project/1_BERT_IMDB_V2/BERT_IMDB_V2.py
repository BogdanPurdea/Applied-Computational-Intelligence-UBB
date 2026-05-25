import os
import gc
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    Executes the 5-fold cross-validation training pipeline for BERT.
    Enforces CUDA usage, exports metrics to a CSV file, and exports LIME/SHAP plots as images.
    """
    # Enforces Nvidia CUDA usage.
    if not torch.cuda.is_available():
        raise SystemError("CUDA is not available. An Nvidia GPU is required to run this optimized script.")
    
    device = torch.device("cuda")
    print("Hardware device confirmed: NVIDIA CUDA")

    # Defines paths relative to the script file.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "IMDB_Dataset.csv")
    output_dir = os.path.join(script_dir, "outputs")
    
    # Creates the outputs folder if it does not exist.
    os.makedirs(output_dir, exist_ok=True)

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
    
    # Stores metrics to export later.
    all_fold_metrics = []

    final_model = None

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
            output_dir=os.path.join(output_dir, f"results_fold_{fold+1}"),
            num_train_epochs=epochs_per_fold,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=2e-5,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            fp16=True, # Mixed precision enabled for Nvidia GPU
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
        
        # Formats the metrics for export.
        formatted_metrics = {
            'Fold': fold + 1,
            'Accuracy': metrics['eval_accuracy'],
            'Precision': metrics['eval_precision'],
            'Recall': metrics['eval_recall'],
            'F1_Score': metrics['eval_f1']
        }
        all_fold_metrics.append(formatted_metrics)
        print(f"Fold {fold + 1} Metrics: {formatted_metrics}")

        if fold == (n_splits - 1):
            final_model = model
        else:
            del model
            del trainer
            torch.cuda.empty_cache()
            gc.collect()

    print("\n========== Cross-Validation Complete ==========")
    
    # Exports metrics to a CSV file in the outputs directory.
    metrics_df = pd.DataFrame(all_fold_metrics)
    metrics_csv_path = os.path.join(output_dir, "fold_metrics.csv")
    metrics_df.to_csv(metrics_csv_path, index=False)
    print(f"Metrics for all folds exported to: {metrics_csv_path}")

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
        # Converts the input into a standard Python list to ensure compatibility with the Hugging Face tokenizer.
        if isinstance(text_list, np.ndarray):
            text_list = text_list.tolist()
        elif not isinstance(text_list, list):
            text_list = list(text_list)

        final_model.eval()
        inputs = tokenizer(text_list, truncation=True, padding=True, max_length=max_length, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = final_model(**inputs)
            scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
        return scores.cpu().numpy()

    sample_review = "This movie had a fantastic script and brilliant acting, but the ending was terrible and slow."
    print(f"Generating explanations for sample review:\n'{sample_review}'")

    # 1. Generate and Export LIME Explanation Image
    print("\nRunning LIME explanation...")
    lime_explainer = LimeTextExplainer(class_names=class_names)
    lime_exp = lime_explainer.explain_instance(sample_review, predict_proba, num_features=6)
    
    lime_fig = lime_exp.as_pyplot_figure()
    lime_output_path = os.path.join(output_dir, "lime_explanation.png")
    lime_fig.savefig(lime_output_path, bbox_inches='tight')
    plt.close(lime_fig)
    print(f"LIME plot exported to: {lime_output_path}")

    # 2. Generate and Export SHAP Explanation Image
    print("\nRunning SHAP explanation...")
    shap_explainer = shap.Explainer(predict_proba, masker=shap.maskers.Text(tokenizer=r"\W+"), output_names=class_names)
    shap_values = shap_explainer([sample_review])
    
    # Generates a bar plot for the positive class (index 1) and saves as image.
    shap.plots.bar(shap_values[0, :, "positive"], show=False)
    shap_output_path = os.path.join(output_dir, "shap_explanation.png")
    plt.savefig(shap_output_path, bbox_inches='tight')
    plt.close()
    print(f"SHAP plot exported to: {shap_output_path}")

    print("\nProcess finished successfully.")

if __name__ == "__main__":
    main()