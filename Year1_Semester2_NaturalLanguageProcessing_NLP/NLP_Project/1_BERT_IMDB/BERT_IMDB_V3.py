import os
import gc
import glob
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
    Executes the model interpretability pipeline using a pre-trained model.
    Automatically locates the most recent checkpoint folder and generates explanation plots.
    """
    # Enforces Nvidia CUDA usage for hardware acceleration.
    if not torch.cuda.is_available():
        raise SystemError("CUDA is not available. An Nvidia GPU is required to run this script.")
    
    device = torch.device("cuda")
    print("Hardware device confirmed: NVIDIA CUDA")

    # Defines directory paths relative to the script location.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "outputs")
    fold_dir = os.path.join(output_dir, "results_fold_5")
    
    # Verifies that the fold directory exists before proceeding.
    if not os.path.exists(fold_dir):
        raise FileNotFoundError(f"Saved model directory not found at: {fold_dir}")

    # Locates all checkpoint sub-folders within the fold directory using pattern matching.
    checkpoints = glob.glob(os.path.join(fold_dir, "checkpoint-*"))
    if not checkpoints:
        raise FileNotFoundError(f"No checkpoint folders found inside {fold_dir}. The model files may be missing.")
    
    # Sorts the checkpoint folders by number and selects the highest one.
    saved_model_path = max(checkpoints, key=lambda x: int(x.split('-')[-1]))
    print(f"Automatically selected the latest checkpoint: {saved_model_path}")

    model_name = "bert-base-uncased"
    max_length = 128

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print(f"Loading saved model from: {saved_model_path}...")
    final_model = AutoModelForSequenceClassification.from_pretrained(saved_model_path)
    final_model.to(device)

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