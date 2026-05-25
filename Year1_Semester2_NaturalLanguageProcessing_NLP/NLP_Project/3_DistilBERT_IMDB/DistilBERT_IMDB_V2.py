import os
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
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
    Executes the training pipeline for a DistilBERT model using a 70/15/15 data split.
    Enforces CUDA usage, exports metrics to a CSV file, and exports LIME/SHAP plots as images.
    """
    # Enforces Nvidia CUDA usage for hardware acceleration.
    if not torch.cuda.is_available():
        raise SystemError("CUDA is not available. An Nvidia GPU is required to run this script.")
    
    device = torch.device("cuda")
    print("Hardware device confirmed: NVIDIA CUDA")

    # Defines directory paths relative to the script location.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "IMDB_Dataset.csv")
    output_dir = os.path.join(script_dir, "outputs")
    
    # Creates the outputs folder if it does not exist.
    os.makedirs(output_dir, exist_ok=True)

    # Initializes the DistilBERT model identifier and training parameters.
    model_name = "distilbert-base-uncased"
    max_length = 128
    batch_size = 16
    epochs = 2

    print("Loading dataset...")
    texts, labels = load_and_prepare_data(data_path)

    print("Splitting dataset into 70% Train, 15% Validation, and 15% Test...")
    # First split isolates 70% of the data for training, leaving 30% for validation and testing.
    train_texts, temp_texts, train_labels, temp_labels = train_test_split(
        texts, labels, test_size=0.30, random_state=42, stratify=labels
    )
    
    # Second split divides the remaining 30% equally into validation and test sets (15% each).
    val_texts, test_texts, val_labels, test_labels = train_test_split(
        temp_texts, temp_labels, test_size=0.50, random_state=42, stratify=temp_labels
    )

    print(f"Loading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print("Tokenizing text data...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=max_length)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=max_length)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=max_length)

    train_dataset = IMDBDataset(train_encodings, train_labels)
    val_dataset = IMDBDataset(val_encodings, val_labels)
    test_dataset = IMDBDataset(test_encodings, test_labels)

    print("Initializing model...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.to(device)

    training_args = TrainingArguments(
        output_dir=os.path.join(output_dir, "distilbert_training_results"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=2e-5,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        fp16=True, 
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

    print("\n========== Evaluating on Test Set ==========")
    # Evaluates the finalized model on the untouched test dataset.
    test_results = trainer.predict(test_dataset)
    metrics = test_results.metrics
    
    formatted_metrics = {
        'Accuracy': metrics['test_accuracy'],
        'Precision': metrics['test_precision'],
        'Recall': metrics['test_recall'],
        'F1_Score': metrics['test_f1']
    }
    print(f"Final Test Metrics: {formatted_metrics}")

    # Exports final test metrics to a CSV file in the outputs directory.
    metrics_df = pd.DataFrame([formatted_metrics])
    metrics_csv_path = os.path.join(output_dir, "test_metrics.csv")
    metrics_df.to_csv(metrics_csv_path, index=False)
    print(f"Test metrics exported to: {metrics_csv_path}")

    # Retains the trained model in memory for the interpretability phase.
    final_model = model

    # ==========================================
    # Model Interpretability Section (LIME & SHAP)
    # ==========================================
    print("\n========== Initializing Model Interpretability ==========")
    
    class_names = ['negative', 'positive']
    
    def predict_proba(text_list):
        """
        Calculates prediction confidence scores for a given list of input strings.
        Formats the output as a numpy array to ensure compatibility with LIME and SHAP APIs.
        """
        # Converts the input into a standard list to prevent tokenizer errors.
        if isinstance(text_list, np.ndarray):
            text_list = text_list.tolist()
        elif not isinstance(text_list, list):
            text_list = list(text_list)

        final_model.eval()
        inputs = tokenizer(text_list, truncation=True, padding=True, max_length=max_length, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = final_model(**inputs)
            # Applies the softmax mathematical function to convert raw scores into percentages.
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
    # The masker defines how text is broken apart for the SHAP analysis.
    shap_explainer = shap.Explainer(predict_proba, masker=shap.maskers.Text(tokenizer=r"\W+"), output_names=class_names)
    shap_values = shap_explainer([sample_review])
    
    # Generates a bar plot for the positive class and saves it as an image file.
    shap.plots.bar(shap_values[0, :, "positive"], show=False)
    shap_output_path = os.path.join(output_dir, "shap_explanation.png")
    plt.savefig(shap_output_path, bbox_inches='tight')
    plt.close()
    print(f"SHAP plot exported to: {shap_output_path}")

    print("\nProcess finished successfully.")

if __name__ == "__main__":
    main()