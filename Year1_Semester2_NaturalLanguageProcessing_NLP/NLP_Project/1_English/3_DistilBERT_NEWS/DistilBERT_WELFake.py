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


class WELFakeDataset(torch.utils.data.Dataset):
    """
    Custom PyTorch Dataset class for IMDB text classification.
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


def load_and_prepare_data(file_path, sample_size=10000, random_state=42):
    """
    Loads the preprocessed WELFake dataset and optionally reduces it to a
    stratified sample while preserving the 0/1 label distribution.
    Expected columns: text, label, sentiment.
    """
    df = pd.read_csv(file_path, encoding="utf-8", low_memory=False)

    required_columns = {"text", "label"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Found columns: {df.columns.tolist()}"
        )

    df = df.dropna(subset=["text", "label"])

    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df[df["label"].isin([0, 1])]
    df["label"] = df["label"].astype(int)

    if sample_size is not None and len(df) > sample_size:
        df, _ = train_test_split(
            df,
            train_size=sample_size,
            random_state=random_state,
            stratify=df["label"]
        )

    df = df.reset_index(drop=True)

    print("\n========== Sampled Dataset Summary ==========")
    print(f"Total records used: {len(df)}")
    print(df["label"].value_counts().sort_index())
    print("============================================\n")

    texts = df["text"].astype(str).tolist()
    labels = df["label"].tolist()

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
        "PreProcessed_WELFake_Dataset.csv"
    )

    output_dir = os.path.join(script_dir, "output_WELFake")
    training_output_dir = os.path.join(output_dir, "distilbert_training_results")

    # Creates the output directory if it does not exist.
    os.makedirs(output_dir, exist_ok=True)

    # Initializes the model identifier and training parameters.
    model_name = "distilbert-base-uncased"
    max_length = 512   # 128/256/512, Process more of the input
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

    train_dataset = WELFakeDataset(train_encodings, train_labels)
    val_dataset = WELFakeDataset(val_encodings, val_labels)
    test_dataset = WELFakeDataset(test_encodings, test_labels)

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
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        fp16=True,
        dataloader_num_workers=0,
        gradient_accumulation_steps=2,
        logging_steps=100,
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
    shap_explainer = shap.Explainer(predict_logits, masker=shap.maskers.Text(tokenizer=tokenizer), output_names=class_names)

    # Extracts up to five review strings from the dataset that have a length of 256 characters or fewer.
    sample_reviews = [text for text in prep_texts if len(text) <= 256][:5]

    lime_explainer = LimeTextExplainer(class_names=class_names)

    for index, review_text in enumerate(sample_reviews):
        print(f"\nProcessing explanation {index + 1} of {len(sample_reviews)}...")
        print(f"Review Text: '{review_text[:100]}...'")

        # Counts approximate LIME word features in the full review.
        lime_num_features = len(review_text.split())

        # 1. Generates and Exports Full LIME Explanation Image
        lime_exp = lime_explainer.explain_instance(
            review_text,
            predict_proba,
            num_features=lime_num_features
        )

        lime_fig = lime_exp.as_pyplot_figure()
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

        shap_feature_count = len(shap_values[0, :, 1].values)

        shap.plots.bar(
            shap_values[0, :, 1],
            max_display=shap_feature_count,
            show=False
        )

        shap_output_path = os.path.join(output_dir, f"shap_explanation_{index}.png")
        plt.savefig(shap_output_path, bbox_inches='tight')
        plt.close()
        print(f"SHAP plot exported to: {shap_output_path}")

    print("\nProcess finished successfully.")


if __name__ == "__main__":
    main()