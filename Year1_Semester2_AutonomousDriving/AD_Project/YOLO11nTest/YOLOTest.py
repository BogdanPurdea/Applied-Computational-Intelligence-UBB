# ============================================================
# GTSRB Transfer Learning Baseline: Pretrained YOLO11 Nano
# Local Windows-safe implementation
# ============================================================

import sys
import os
import random
import platform

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm

import kagglehub

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, Subset

import torchvision.transforms as T
from ultralytics import YOLO

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

# ============================================================
# Configuration
# ============================================================

SEED = 42
NUM_CLASSES = 43
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15
LR = 1e-4
VAL_RATIO = 0.15
WEIGHT_DECAY = 1e-4

BEST_MODEL_PATH = "best_yolo11n_gtsrb.pth"
HISTORY_CSV_PATH = "training_history_yolo11n_gtsrb.csv"


# ============================================================
# Reproducibility
# ============================================================

def set_seed(seed: int = 42):
    """
    Establishes random seed values across computational libraries to guarantee reproducible execution. 
    Configures hardware backends for deterministic processing.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = False


# ============================================================
# Dataset
# ============================================================

class GTSRBDataset(Dataset):
    """
    Defines a data structure for loading the German Traffic Sign Recognition Benchmark image collection.
    """
    def __init__(self, dataframe, root_dir, transform=None):
        """
        Initializes the dataset object using tabular data, root directory paths, and transformation parameters.
        """
        self.df = dataframe.reset_index(drop=True)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        """
        Calculates and returns the total item count within the dataset.
        """
        return len(self.df)

    def __getitem__(self, idx):
        """
        Retrieves a specific image and its associated classification label from the file system based on a numeric index. 
        Applies predefined image transformations prior to returning the data.
        """
        row = self.df.iloc[idx]

        img_path = os.path.join(self.root_dir, row["Path"])
        label = int(row["ClassId"])

        image = Image.open(img_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, label


# ============================================================
# Model Modification
# ============================================================

def create_yolo_classifier(num_classes):
    """
    Instantiates a pre-trained YOLO11 nano classification model. 
    Modifies the final linear layer to align with the target number of output classes.
    Returns the modified PyTorch network.
    """
    # Load the base nano model specifically built for classification
    yolo_base = YOLO("yolo11n-cls.pt")
    pytorch_model = yolo_base.model

    # Locate and replace the final linear classification layer
    for name, module in pytorch_model.named_modules():
        if isinstance(module, nn.Linear):
            in_features = module.in_features
            
            parent_path = name.rsplit('.', 1)[0]
            child_name = name.rsplit('.', 1)[1]
            
            parent_module = pytorch_model.get_submodule(parent_path)
            setattr(parent_module, child_name, nn.Linear(in_features, num_classes))
            
    return pytorch_model


# ============================================================
# Training / Evaluation
# ============================================================

def train_one_epoch(model, loader, criterion, optimizer, device):
    """
    Executes one complete training iteration over the training dataset. 
    Computes loss values, performs gradient backpropagation, and updates model parameters. 
    Returns the calculated average loss and accuracy metrics.
    """
    model.train()

    total_loss = 0.0
    all_preds = []
    all_labels = []

    for images, labels in tqdm(loader, desc="Training", leave=False):
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)

        logits = model(images)
        
        # Extracts the primary prediction tensor if the model output is packaged as a tuple or list.
        if isinstance(logits, tuple) or isinstance(logits, list):
            logits = logits[0]

        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)

        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.detach().cpu().numpy())
        all_labels.extend(labels.detach().cpu().numpy())

    avg_loss = total_loss / len(loader.dataset)
    acc = accuracy_score(all_labels, all_preds)

    return avg_loss, acc


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    """
    Assesses model performance on a specified dataset without performing gradient calculations or weight updates. 
    Calculates statistical metrics including loss, accuracy, precision, recall, and f1-score. 
    Returns a dictionary containing these performance statistics.
    """
    model.eval()

    total_loss = 0.0
    all_preds = []
    all_labels = []

    for images, labels in tqdm(loader, desc="Evaluating", leave=False):
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        logits = model(images)
        
        # Extracts the primary prediction tensor if the model output is packaged as a tuple or list.
        if isinstance(logits, tuple) or isinstance(logits, list):
            logits = logits[0]

        loss = criterion(logits, labels)

        total_loss += loss.item() * images.size(0)

        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(loader.dataset)
    acc = accuracy_score(all_labels, all_preds)

    precision, recall, f1, _ = precision_recall_fscore_support(
        all_labels,
        all_preds,
        average="macro",
        zero_division=0
    )

    return {
        "loss": avg_loss,
        "accuracy": acc,
        "precision_macro": precision,
        "recall_macro": recall,
        "f1_macro": f1,
        "labels": all_labels,
        "preds": all_preds
    }


# ============================================================
# Plotting
# ============================================================

def plot_confusion_matrix(labels, preds):
    """
    Generates and saves a visual matrix graphic comparing true dataset labels against predicted model outputs.
    """
    cm = confusion_matrix(labels, preds)

    plt.figure(figsize=(14, 12))
    plt.imshow(cm)
    plt.title("Confusion Matrix - YOLO11n on GTSRB")
    plt.xlabel("Predicted Class")
    plt.ylabel("True Class")
    plt.colorbar()
    plt.tight_layout()
    plt.savefig("confusion_matrix_yolo11n_gtsrb.png", dpi=200)
    plt.show()


def plot_training_curves(history_df):
    """
    Generates and saves line graphs that display changes in accuracy and loss metrics across training epochs.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(history_df["epoch"], history_df["train_accuracy"], label="Train Accuracy")
    plt.plot(history_df["epoch"], history_df["val_accuracy"], label="Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("accuracy_curve.png", dpi=200)
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(history_df["epoch"], history_df["train_loss"], label="Train Loss")
    plt.plot(history_df["epoch"], history_df["val_loss"], label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training vs Validation Loss")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("loss_curve.png", dpi=200)
    plt.show()


# ============================================================
# Main pipeline
# ============================================================

def main():
    """
    Controls the primary execution sequence of the application. 
    Manages data acquisition, model initialization, training loops, and final evaluation procedures.
    """
    set_seed(SEED)

    print(sys.executable)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("=" * 70)
    print("GTSRB Transfer Learning Baseline: YOLO11-Nano")
    print("=" * 70)
    print("Device:", device)
    print("OS:", platform.platform())

    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
        print("CUDA version:", torch.version.cuda)
    else:
        print("WARNING: CUDA is not available. Training will run on CPU.")

    print("=" * 70)

    # -----------------------------
    # Download GTSRB
    # -----------------------------
    path = kagglehub.dataset_download(
        "meowmeowmeowmeowmeow/gtsrb-german-traffic-sign"
    )
    print("Dataset path:", path)

    # -----------------------------
    # Locate metadata
    # -----------------------------
    train_csv = os.path.join(path, "Train.csv")
    test_csv = os.path.join(path, "Test.csv")

    train_df = pd.read_csv(train_csv)
    test_df = pd.read_csv(test_csv)

    print(train_df.head())
    print(test_df.head())
    print("Train size:", len(train_df))
    print("Test size:", len(test_df))
    print("Classes:", train_df["ClassId"].nunique())

    # -----------------------------
    # Transforms
    # -----------------------------
    # Standard ImageNet values often used for general transfer learning
    imagenet_mean = [0.485, 0.456, 0.406]
    imagenet_std = [0.229, 0.224, 0.225]

    train_transform = T.Compose([
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.RandomRotation(10),
        T.RandomAffine(
            degrees=0,
            translate=(0.05, 0.05),
            scale=(0.90, 1.10)
        ),
        T.ColorJitter(
            brightness=0.25,
            contrast=0.25,
            saturation=0.25
        ),
        T.ToTensor(),
        T.Normalize(mean=imagenet_mean, std=imagenet_std)
    ])

    eval_transform = T.Compose([
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.ToTensor(),
        T.Normalize(mean=imagenet_mean, std=imagenet_std)
    ])

    # -----------------------------
    # Stratified train/validation split
    # -----------------------------
    indices = np.arange(len(train_df))
    labels = train_df["ClassId"].values

    train_indices, val_indices = train_test_split(
        indices,
        test_size=VAL_RATIO,
        random_state=SEED,
        stratify=labels
    )

    train_base_dataset = GTSRBDataset(train_df, path, transform=train_transform)
    val_base_dataset = GTSRBDataset(train_df, path, transform=eval_transform)
    test_dataset = GTSRBDataset(test_df, path, transform=eval_transform)

    train_dataset = Subset(train_base_dataset, train_indices)
    val_dataset = Subset(val_base_dataset, val_indices)

    num_workers = 0
    pin_memory = torch.cuda.is_available()

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory
    )

    print("\nSplit summary:")
    print("Train:", len(train_dataset))
    print("Validation:", len(val_dataset))
    print("Test:", len(test_dataset))

    # -----------------------------
    # Model Setup
    # -----------------------------
    model = create_yolo_classifier(NUM_CLASSES)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.AdamW(
        model.parameters(),
        lr=LR,
        weight_decay=WEIGHT_DECAY
    )

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=2
    )

    # -----------------------------
    # Training loop
    # -----------------------------
    history = []
    best_val_acc = 0.0

    for epoch in range(1, EPOCHS + 1):
        print(f"\nEpoch {epoch}/{EPOCHS}")

        train_loss, train_acc = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device
        )

        val_metrics = evaluate(
            model,
            val_loader,
            criterion,
            device
        )

        scheduler.step(val_metrics["accuracy"])

        current_lr = optimizer.param_groups[0]["lr"]

        row = {
            "epoch": epoch,
            "learning_rate": current_lr,
            "train_loss": train_loss,
            "train_accuracy": train_acc,
            "val_loss": val_metrics["loss"],
            "val_accuracy": val_metrics["accuracy"],
            "val_precision_macro": val_metrics["precision_macro"],
            "val_recall_macro": val_metrics["recall_macro"],
            "val_f1_macro": val_metrics["f1_macro"]
        }

        history.append(row)

        print(
            f"LR: {current_lr:.2e} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Train Acc: {train_acc:.4f} | "
            f"Val Loss: {val_metrics['loss']:.4f} | "
            f"Val Acc: {val_metrics['accuracy']:.4f} | "
            f"Val F1: {val_metrics['f1_macro']:.4f}"
        )

        if val_metrics["accuracy"] > best_val_acc:
            best_val_acc = val_metrics["accuracy"]
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "best_val_accuracy": best_val_acc,
                    "epoch": epoch
                },
                BEST_MODEL_PATH
            )
            print(f"Saved best model: {BEST_MODEL_PATH}")

    # -----------------------------
    # Save history
    # -----------------------------
    history_df = pd.DataFrame(history)
    history_df.to_csv(HISTORY_CSV_PATH, index=False)

    print("\nTraining complete.")
    print("Best validation accuracy:", best_val_acc)
    print("History saved to:", HISTORY_CSV_PATH)

    # -----------------------------
    # Load best model
    # -----------------------------
    checkpoint = torch.load(BEST_MODEL_PATH, map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])

    # -----------------------------
    # Final test evaluation
    # -----------------------------
    test_metrics = evaluate(
        model,
        test_loader,
        criterion,
        device
    )

    print("\n==============================")
    print("FINAL TEST METRICS")
    print("==============================")
    print(f"Test Loss:       {test_metrics['loss']:.4f}")
    print(f"Accuracy:        {test_metrics['accuracy']:.4f}")
    print(f"Macro Precision: {test_metrics['precision_macro']:.4f}")
    print(f"Macro Recall:    {test_metrics['recall_macro']:.4f}")
    print(f"Macro F1-score:  {test_metrics['f1_macro']:.4f}")

    report = classification_report(
        test_metrics["labels"],
        test_metrics["preds"],
        digits=4,
        zero_division=0
    )

    print("\nClassification Report:")
    print(report)

    with open("classification_report_yolo11n_gtsrb.txt", "w", encoding="utf-8") as f:
        f.write(report)

    # -----------------------------
    # Plots
    # -----------------------------
    plot_confusion_matrix(
        test_metrics["labels"],
        test_metrics["preds"]
    )

    plot_training_curves(history_df)

    print("\nGenerated files:")
    print("-", BEST_MODEL_PATH)
    print("-", HISTORY_CSV_PATH)
    print("- classification_report_yolo11n_gtsrb.txt")
    print("- confusion_matrix_yolo11n_gtsrb.png")
    print("- accuracy_curve.png")
    print("- loss_curve.png")


# ============================================================
# Windows multiprocessing guard
# ============================================================

if __name__ == "__main__":
    main()