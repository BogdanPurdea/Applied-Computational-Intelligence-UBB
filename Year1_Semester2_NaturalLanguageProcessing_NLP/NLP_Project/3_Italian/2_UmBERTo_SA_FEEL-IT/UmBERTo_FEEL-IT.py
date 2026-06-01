import os
import glob
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from lime.lime_text import LimeTextExplainer
import shap

# Version 2 with fix

class ItalianReviewDataset(torch.utils.data.Dataset):
    """
    Custom PyTorch Dataset class for text classification.
    Manages the formatting of text encodings and labels for the training pipeline.
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
    Compares the model outputs against the true labels.
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
    Loads a CSV dataset, maps string sentiments to binary integers, and removes invalid rows.
    Utilizes the python engine to safely skip rows with broken formatting.
    """
    df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')
    df['sentiment'] = df['sentiment'].str.lower().map({'positive': 1, 'negative': 0})
    df = df.dropna(subset=['sentiment'])
    df['sentiment'] = df['sentiment'].astype(int)

    texts = df['text'].tolist()
    labels = df['sentiment'].tolist()
    return texts, labels


def main():
    """
    Executes the training pipeline for a sequence classification model.
    Checks for the latest training checkpoint before initializing a new training phase.
    Splits a preprocessed dataset into train, validation, and test sets.
    Enforces CUDA usage, exports metrics, and generates interpretability plots.
    """
    # Enforces Nvidia CUDA usage for hardware acceleration.
    if not torch.cuda.is_available():
        raise SystemError("CUDA is not available. An Nvidia GPU is required to run this script.")

    device = torch.device("cuda")
    print("Hardware device confirmed: NVIDIA CUDA")

    # Defines directory paths relative to the script location.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(script_dir))

    preprocessed_data_path = os.path.join(
        parent_dir,
        "Datasets",
        "PreProcessed_FEEL-IT_Dataset.csv"
    )
    output_dir = os.path.join(script_dir, "output_umberto_V2")
    training_output_dir = os.path.join(output_dir, "umberto_training_results")

    # Creates the output directory if it does not exist.
    os.makedirs(output_dir, exist_ok=True)

    # Initializes the model identifier using the Italian UmBERTo model.
    model_name = "Musixmatch/umberto-commoncrawl-cased-v1"
    max_length = 512
    batch_size = 16
    epochs = 2

    print("Loading preprocessed dataset...")
    prep_texts, prep_labels = load_and_prepare_data(preprocessed_data_path)

    print("Splitting preprocessed dataset into Training (70%), Validation (15%), and Testing (15%)...")
    # Extracts 70% of the data for training, reserving 30% for temporary holdout.
    train_texts, temp_texts, train_labels, temp_labels = train_test_split(
        prep_texts, prep_labels, test_size=0.30, random_state=42, stratify=prep_labels
    )

    # Divides the temporary 30% holdout equally into validation and test sets.
    val_texts, test_texts, val_labels, test_labels = train_test_split(
        temp_texts, temp_labels, test_size=0.50, random_state=42, stratify=temp_labels
    )

    # Outputs a summary of the exact record counts to the console.
    print("\n========== Dataset Split Summary ==========")
    print(f"Training records (70%): {len(train_texts)}")
    print(f"Validation records (15%): {len(val_texts)}")
    print(f"Testing records (15%): {len(test_texts)}")
    print("===========================================\n")

    # Determines the latest checkpoint path if training has previously occurred.
    saved_model_path = None
    requires_training = True

    if os.path.exists(training_output_dir):
        # Locates all checkpoint sub-folders within the directory using pattern matching.
        checkpoints = glob.glob(os.path.join(training_output_dir, "checkpoint-*"))
        if checkpoints:
            # Sorts the checkpoint folders by number and selects the highest one.
            saved_model_path = max(checkpoints, key=lambda x: int(x.split('-')[-1]))
            requires_training = False

    # Loads the tokenizer. If a saved model exists, loads the tokenizer from the checkpoint.
    if saved_model_path:
        print(f"Loading saved tokenizer from {saved_model_path}...")
        tokenizer = AutoTokenizer.from_pretrained(saved_model_path)
    else:
        print(f"Loading base tokenizer for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)

    print("Tokenizing text data...")
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=max_length)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=max_length)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=max_length)

    train_dataset = ItalianReviewDataset(train_encodings, train_labels)
    val_dataset = ItalianReviewDataset(val_encodings, val_labels)
    test_dataset = ItalianReviewDataset(test_encodings, test_labels)

    # Loads the fine-tuned model from the checkpoint or initializes a base model for training.
    if not requires_training:
        print(f"\nFound existing fine-tuned model at {saved_model_path}.")
        print("Loading model from disk. Skipping training phase...")
        model = AutoModelForSequenceClassification.from_pretrained(saved_model_path)
    else:
        print(f"\nNo checkpoints found in {training_output_dir}.")
        print("Initializing base model for new training phase...")
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    model.to(device)

    training_args = TrainingArguments(
        output_dir=training_output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=2e-5,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        fp16=True,
        dataloader_num_workers=0,
        gradient_accumulation_steps=1,
        logging_steps=200,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    # Executes training only if a valid checkpoint was not found.
    if requires_training:
        print("\n========== Beginning Training ==========")
        trainer.train()
        print("Training complete. Models are saved in checkpoint directories.")

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

    # Exports final test metrics to a CSV file in the output directory.
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
        Calculates prediction probabilities for a given list of input strings.
        Outputs scaled percentages required for LIME explanations.
        Processes inputs in smaller batches to prevent GPU memory exhaustion.
        Formats the output as a combined numpy array.
        """
        if isinstance(text_list, np.ndarray):
            text_list = text_list.tolist()
        elif not isinstance(text_list, list):
            text_list = list(text_list)

        final_model.eval()
        inference_batch_size = 16
        all_scores = []

        for i in range(0, len(text_list), inference_batch_size):
            batch_texts = text_list[i:i + inference_batch_size]
            inputs = tokenizer(batch_texts, truncation=True, padding=True, max_length=max_length, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = final_model(**inputs)
                scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
                all_scores.append(scores.cpu().numpy())

        return np.vstack(all_scores)

    def predict_logits(text_list):
        """
        Calculates raw prediction scores (logits) for a given list of input strings.
        Outputs unscaled values required for stable SHAP explanations.
        Processes inputs in smaller batches to prevent GPU memory exhaustion.
        Formats the output as a combined numpy array.
        """
        if isinstance(text_list, np.ndarray):
            text_list = text_list.tolist()
        elif not isinstance(text_list, list):
            text_list = list(text_list)

        final_model.eval()
        inference_batch_size = 16
        all_logits = []

        for i in range(0, len(text_list), inference_batch_size):
            batch_texts = text_list[i:i + inference_batch_size]
            inputs = tokenizer(batch_texts, truncation=True, padding=True, max_length=max_length, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = final_model(**inputs)
                all_logits.append(outputs.logits.cpu().numpy())

        return np.vstack(all_logits)

    # Initializes the SHAP explainer once outside the processing loop to improve efficiency.
    shap_explainer = shap.Explainer(predict_proba, masker=shap.maskers.Text(tokenizer=tokenizer), output_names=class_names)

    # Extracts up to five review strings from the dataset that have a length of 256 characters or fewer.
    sample_reviews = [text for text in prep_texts if len(text) <= 256][:5]

    lime_explainer = LimeTextExplainer(class_names=class_names)

    for index, review_text in enumerate(sample_reviews):
        print(f"\nProcessing explanation {index + 1} of {len(sample_reviews)}...")
        print(f"Review Text: '{review_text[:100]}...'")

        prediction_scores = predict_proba([review_text])[0]
        predicted_class_index = int(np.argmax(prediction_scores))
        predicted_class_name = class_names[predicted_class_index]

        print(f"Prediction probabilities: negative={prediction_scores[0]:.4f}, positive={prediction_scores[1]:.4f}")
        print(f"Predicted class for explanation: {predicted_class_name}")

        # Counts approximate LIME word features in the full review.
        lime_num_features = len(review_text.split())

        # 1. Generates and Exports Full LIME Explanation Image
        lime_exp = lime_explainer.explain_instance(
            review_text,
            predict_proba,
            num_features=lime_num_features,
            labels=(predicted_class_index,)
        )

        lime_fig = lime_exp.as_pyplot_figure(label=predicted_class_index)
        lime_output_path = os.path.join(output_dir, f"lime_explanation_{index}.png")
        lime_fig.savefig(lime_output_path, bbox_inches='tight')
        plt.close(lime_fig)
        print(f"LIME plot exported to: {lime_output_path}")

        # Exports full interactive LIME HTML
        lime_html_path = os.path.join(output_dir, f"lime_explanation_{index}.html")
        lime_exp.save_to_file(lime_html_path)
        print(f"LIME HTML exported to: {lime_html_path}")

        # 2. Generates and Exports Full SHAP Explanation Image
        shap_values = shap_explainer([review_text])

        shap_feature_count = len(shap_values[0, :, predicted_class_index].values)

        shap.plots.bar(
            shap_values[0, :, predicted_class_index],
            max_display=shap_feature_count,
            show=False
        )

        shap_output_path = os.path.join(output_dir, f"shap_explanation_{index}.png")
        plt.savefig(shap_output_path, bbox_inches='tight')
        plt.close()
        print(f"SHAP plot exported to: {shap_output_path}")

        # Exports full interactive SHAP HTML
        shap_html = shap.plots.text(shap_values[0, :, predicted_class_index], display=False)
        shap_html_path = os.path.join(output_dir, f"shap_explanation_{index}.html")
        with open(shap_html_path, "w", encoding="utf-8") as f:
            f.write(f"<html><head><meta charset='utf-8'><title>SHAP Explanation {index}</title></head><body style='padding: 20px;'>{shap_html}</body></html>")
        print(f"SHAP HTML exported to: {shap_html_path}")

    print("\nProcess finished successfully.")


if __name__ == "__main__":
    main()