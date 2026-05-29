import os
import time
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pandas as pd
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# =============================================================================
# HYPERPARAMETERS & CONFIGURATION
# =============================================================================

# Paths
DATA_ROOT = "./data/gtsrb-german-traffic-sign"
TRAIN_CSV = os.path.join(DATA_ROOT, "Train.csv")
TEST_CSV = os.path.join(DATA_ROOT, "Test.csv")
OUTPUT_DIR = "./output"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
CKPT_PATH = os.path.join(OUTPUT_DIR, "gtsrb_fcn_vat_best.pth")
HISTORY_PATH = os.path.join(OUTPUT_DIR, "training_history.json")

# Creates output directories if they do not exist.
os.makedirs(PLOTS_DIR, exist_ok=True)

# Dataset Parameters
IMG_SIZE = 48
IN_FEATURES = 3 * IMG_SIZE * IMG_SIZE  # 6912
NUM_CLASSES = 43
VAL_SPLIT = 0.15  # 15% of the data goes to testing/validation

# Training Parameters
BATCH_SIZE = 128
EPOCHS = 50
LR = 1e-3
WEIGHT_DECAY = 1e-4
NUM_WORKERS = 0
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model Parameters
DROPOUT_P = 0.4
LABEL_SMOOTHING = 0.1

# VAT Parameters
VAT_XI = 1e-6  # Small constant to scale the initial random noise
VAT_EPSILON = 2.5  # The magnitude of the final adversarial perturbation
VAT_ALPHA = 1.0  # Weight of the VAT loss in the total loss
VAT_ITERATIONS = 1  # Number of steps to find the worst-case perturbation

# Normalization Statistics (GTSRB specific)
GTSRB_MEAN = (0.3337, 0.3064, 0.3171)
GTSRB_STD = (0.2672, 0.2564, 0.2629)


# =============================================================================
# DATA PREPARATION
# =============================================================================

class GTSRBCSVDataset(Dataset):
    """
    Loads images based on a CSV file containing paths and labels.
    Provides a standardized way to read GTSRB avoiding folder duplication.
    """

    def __init__(self, csv_path: str, root_dir: str, transform=None):
        """
        Initializes the dataset reading from the specified CSV.
        """
        self.df = pd.read_csv(csv_path)
        self.root = root_dir
        self.transform = transform

    def __len__(self) -> int:
        """
        Returns the total number of samples in the dataset.
        """
        return len(self.df)

    def __getitem__(self, idx: int) -> tuple:
        """
        Fetches the image and label at the specified index.
        """
        row = self.df.iloc[idx]
        img_path = os.path.join(self.root, row["Path"])
        image = Image.open(img_path).convert("RGB")
        label = int(row["ClassId"])

        if self.transform:
            image = self.transform(image)

        return image, label


# Image Transforms
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomRotation(degrees=15),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
    transforms.RandomHorizontalFlip(p=0.1),
    transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.3, hue=0.05),
    transforms.ToTensor(),
    transforms.Normalize(GTSRB_MEAN, GTSRB_STD),
])

val_test_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(GTSRB_MEAN, GTSRB_STD),
])


# =============================================================================
# MODEL ARCHITECTURE
# =============================================================================

class ProjectionBlock(nn.Module):
    """
    Reduces the dimension of the input features while utilizing a skip connection.
    """

    def __init__(self, in_f: int, out_f: int, dropout: float):
        """
        Initializes the layers for the main path and the dimension-reducing skip connection.
        """
        super().__init__()
        self.main = nn.Sequential(
            nn.Linear(in_f, out_f, bias=False),
            nn.BatchNorm1d(out_f),
            nn.GELU(),
            nn.Dropout(p=dropout),
        )
        self.skip = nn.Linear(in_f, out_f, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Executes the forward pass by adding the main path and skip path outputs.
        """
        return self.main(x) + self.skip(x)


class ResidualFCBlock(nn.Module):
    """
    Refines features without changing their dimensions using a direct skip connection.
    """

    def __init__(self, features: int, dropout: float):
        """
        Initializes the sequential processing layers and final activation function.
        """
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(features, features, bias=False),
            nn.BatchNorm1d(features),
            nn.GELU(),
            nn.Dropout(p=dropout),
            nn.Linear(features, features, bias=False),
            nn.BatchNorm1d(features),
        )
        self.act = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Executes the forward pass by adding the original input to the processed output.
        """
        return self.act(x + self.net(x))


class FCN(nn.Module):
    """
    A Fully Connected Network for classifying images flattened into 1D arrays.
    """

    def __init__(self, in_features: int = IN_FEATURES, num_classes: int = NUM_CLASSES, dropout: float = DROPOUT_P):
        """
        Initializes the sequence of projection and residual blocks, plus the final classifier.
        """
        super().__init__()
        self.flatten = nn.Flatten()

        self.proj1 = ProjectionBlock(in_features, 1024, dropout=dropout)
        self.proj2 = ProjectionBlock(1024, 512, dropout=dropout * 0.80)

        self.res1 = ResidualFCBlock(512, dropout=dropout * 0.60)
        self.res2 = ResidualFCBlock(512, dropout=dropout * 0.60)

        self.proj3 = ProjectionBlock(512, 256, dropout=dropout * 0.50)

        self.classifier = nn.Linear(256, num_classes)
        self._init_weights()

    def _init_weights(self) -> None:
        """
        Applies Kaiming Normal initialization to linear layers and resets batch normalization layers.
        """
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Transforms a batch of 2D images into classification scores.
        """
        x = self.flatten(x)
        x = self.proj1(x)
        x = self.proj2(x)
        x = self.res1(x)
        x = self.res2(x)
        x = self.proj3(x)
        return self.classifier(x)


# =============================================================================
# VIRTUAL ADVERSARIAL TRAINING (VAT)
# =============================================================================

def normalize_tensor(tensor: torch.Tensor) -> torch.Tensor:
    """
    Normalizes a tensor by dividing it by its L2 norm to ensure a consistent scale.
    """
    norm = torch.norm(tensor.view(tensor.size(0), -1), p=2, dim=1)
    norm = norm.view(-1, 1, 1, 1).clamp(min=1e-8)
    return tensor / norm


def compute_vat_loss(model: nn.Module, x: torch.Tensor, original_logits: torch.Tensor) -> torch.Tensor:
    """
    Calculates the penalty for the model changing its prediction when the image is slightly perturbed.
    """
    # Generates random noise and normalizes it.
    d = torch.randn_like(x).to(DEVICE)
    d = normalize_tensor(d)

    # Detaches original logits to prevent updates during the noise search.
    original_probs = F.softmax(original_logits.detach(), dim=1)

    # Finds the worst-case direction that maximizes divergence.
    for _ in range(VAT_ITERATIONS):
        d.requires_grad_()
        x_perturbed = x + VAT_XI * d
        logits_perturbed = model(x_perturbed)
        probs_perturbed = F.log_softmax(logits_perturbed, dim=1)

        # Calculates divergence between clean prediction and perturbed prediction.
        adv_distance = F.kl_div(probs_perturbed, original_probs, reduction="batchmean")
        adv_distance.backward()

        # Extracts the gradient to isolate the maximal error direction.
        d_grad = d.grad
        d = normalize_tensor(d_grad).detach()
        model.zero_grad()

    # Applies the final scaled perturbation.
    r_adv = VAT_EPSILON * d
    x_adv = x + r_adv

    # Calculates the final VAT loss.
    logits_adv = model(x_adv)
    probs_adv = F.log_softmax(logits_adv, dim=1)
    vat_loss = F.kl_div(probs_adv, original_probs, reduction="batchmean")

    return vat_loss


# =============================================================================
# TRAINING AND EVALUATION HELPERS
# =============================================================================

def calculate_accuracy(logits: torch.Tensor, targets: torch.Tensor) -> float:
    """
    Calculates the percentage of correctly classified images in a batch.
    """
    return (logits.argmax(dim=1) == targets).float().mean().item()


def train_one_epoch(model: nn.Module, loader: DataLoader, criterion: nn.Module, optimizer: optim.Optimizer) -> tuple:
    """
    Processes one full pass through the training data, applying both supervised and VAT losses.
    """
    model.train()
    total_loss = 0.0
    total_acc = 0.0

    for imgs, labels in loader:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()

        logits = model(imgs)
        supervised_loss = criterion(logits, labels)

        vat_loss = compute_vat_loss(model, imgs, logits)

        loss = supervised_loss + (VAT_ALPHA * vat_loss)

        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        total_loss += loss.item()
        total_acc += calculate_accuracy(logits, labels)

    return total_loss / len(loader), total_acc / len(loader)


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module) -> tuple:
    """
    Calculates the model's loss and accuracy on a provided evaluation dataset.
    """
    model.eval()
    total_loss = 0.0
    total_acc = 0.0

    for imgs, labels in loader:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
        logits = model(imgs)
        total_loss += criterion(logits, labels).item()
        total_acc += calculate_accuracy(logits, labels)

    return total_loss / len(loader), total_acc / len(loader)


def plot_training_curves(history: dict, filepath: str) -> None:
    """
    Generates and saves visual graphs of the training and validation progress.
    """
    epochs_range = range(1, len(history["train_loss"]) + 1)
    best_epoch = history["val_acc"].index(max(history["val_acc"])) + 1
    best_val_acc = max(history["val_acc"]) * 100

    fig = plt.figure(figsize=(14, 5))
    fig.suptitle("FCN VAT - Training History", fontsize=14, fontweight="bold")
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.32)

    # Plots Loss.
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(epochs_range, history["train_loss"], "o-", color="#2196F3", lw=2, ms=3, label="Train Loss")
    ax1.plot(epochs_range, history["val_loss"], "s--", color="#FF5722", lw=2, ms=3, label="Val Loss")
    ax1.axvline(best_epoch, color="#9E9E9E", ls=":", lw=1.4, label=f"Best epoch ({best_epoch})")
    ax1.set_title("Total Loss per Epoch")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    # Plots Accuracy.
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(epochs_range, [a * 100 for a in history["train_acc"]], "o-", color="#2196F3", lw=2, ms=3,
             label="Train Acc")
    ax2.plot(epochs_range, [a * 100 for a in history["val_acc"]], "s--", color="#FF5722", lw=2, ms=3, label="Val Acc")
    ax2.axvline(best_epoch, color="#9E9E9E", ls=":", lw=1.4, label=f"Best epoch ({best_epoch})")
    ax2.axhline(best_val_acc, color="#4CAF50", ls="--", lw=1.2, label=f"Best val {best_val_acc:.2f}%")
    ax2.set_title("Accuracy per Epoch")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy (%)")
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_test_results(test_loss: float, test_acc: float, filepath: str) -> None:
    """
    Creates a summary graphic displaying the final performance metrics on the test set.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.axis("off")
    ax.text(0.5, 0.7, "Final Test Set Evaluation", fontsize=16, fontweight="bold", ha="center")
    ax.text(0.5, 0.4, f"Loss: {test_loss:.4f}", fontsize=14, ha="center")
    ax.text(0.5, 0.2, f"Accuracy: {test_acc * 100:.2f}%", fontsize=14, ha="center")
    plt.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# MAIN SCRIPT
# =============================================================================

if __name__ == "__main__":
    print("Initializing Datasets...")

    # Reads full training data.
    full_train_df = pd.read_csv(TRAIN_CSV)

    # Shuffles and splits into 85% Train / 15% Validation.
    full_train_df = full_train_df.sample(frac=1, random_state=42).reset_index(drop=True)
    val_size = int(len(full_train_df) * VAL_SPLIT)

    # Saves the splits to temporary CSVs to reuse the GTSRBCSVDataset class logic.
    train_split_csv = os.path.join(OUTPUT_DIR, "temp_train_split.csv")
    val_split_csv = os.path.join(OUTPUT_DIR, "temp_val_split.csv")
    full_train_df.iloc[:-val_size].to_csv(train_split_csv, index=False)
    full_train_df.iloc[-val_size:].to_csv(val_split_csv, index=False)

    train_ds = GTSRBCSVDataset(csv_path=train_split_csv, root_dir=DATA_ROOT, transform=train_transform)
    val_ds = GTSRBCSVDataset(csv_path=val_split_csv, root_dir=DATA_ROOT, transform=val_test_transform)
    test_ds = GTSRBCSVDataset(csv_path=TEST_CSV, root_dir=DATA_ROOT, transform=val_test_transform)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS, pin_memory=True,
                              drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=True)

    print(f"Data Prepared. Train: {len(train_ds)} | Validation: {len(val_ds)} | Test: {len(test_ds)}")

    print(f"Building FCN Model on {DEVICE}...")
    model = FCN().to(DEVICE)
    criterion = nn.CrossEntropyLoss(label_smoothing=LABEL_SMOOTHING)
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=LR * 1e-2)

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}
    best_val_acc = 0.0

    print("Starting VAT Semi-Supervised Training...")
    print(f"{'Ep':>3} | {'Tr Loss':>9} {'Tr Acc%':>8} | {'Vl Loss':>9} {'Vl Acc%':>8} | {'LR':>9} | {'Time':>6} |")
    print("-" * 72)

    # Iterates over each epoch in the total epoch count.
    for epoch in range(1, EPOCHS + 1):
        t0 = time.time()

        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        # Iterates over each batch within the current epoch.
        for step, (inputs, targets) in enumerate(train_loader, 1):
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)

            optimizer.zero_grad()

            # Computes the supervised forward pass and base loss.
            outputs = model(inputs)
            supervised_loss = criterion(outputs, targets)

            # Computes the semi-supervised Virtual Adversarial Training loss.
            vat_loss = compute_vat_loss(model, inputs, outputs)

            # Combines the supervised and VAT losses.
            loss = supervised_loss + (VAT_ALPHA * vat_loss)

            loss.backward()

            # Clips gradients to a maximum norm to prevent exploding gradients.
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

            # Prints the current step progress.
            print(f"\rEpoch {epoch:>3} | Step {step:>4}/{len(train_loader)} | Loss: {loss.item():>7.4f}", end="",
                  flush=True)

        # Calculates final epoch metrics.
        tr_l = running_loss / total
        tr_a = correct / total

        # Clears the step tracking line completely before printing the final epoch summary.
        print("\r" + " " * 80 + "\r", end="", flush=True)

        vl_l, vl_a = evaluate(model, val_loader, criterion)
        scheduler.step()

        history["train_loss"].append(tr_l)
        history["train_acc"].append(tr_a)
        history["val_loss"].append(vl_l)
        history["val_acc"].append(vl_a)

        cur_lr = scheduler.get_last_lr()[0]
        elapsed = time.time() - t0

        tag = ""
        if vl_a > best_val_acc:
            best_val_acc = vl_a
            torch.save({
                "epoch": epoch,
                "model_state": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "val_acc": vl_a,
                "history": history,
            }, CKPT_PATH)
            tag = " * saved"

        print(
            f"{epoch:>3} | {tr_l:>9.4f} {tr_a * 100:>7.2f}% | "
            f"{vl_l:>9.4f} {vl_a * 100:>7.2f}% | "
            f"{cur_lr:>9.2e} | {elapsed:>5.1f}s |{tag}"
        )

    print("-" * 72)
    print(f"Training Complete. Best Validation Accuracy: {best_val_acc * 100:.2f}%")

    # Saves history and generates training plot.
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
    plot_training_curves(history, os.path.join(PLOTS_DIR, "training_curves.png"))

    # Loads best weights for final test evaluation.
    print(f"Loading best checkpoint from {CKPT_PATH} for final testing...")
    ckpt = torch.load(CKPT_PATH, map_location=DEVICE)
    model.load_state_dict(ckpt["model_state"])

    test_loss, test_acc = evaluate(model, test_loader, criterion)
    plot_test_results(test_loss, test_acc, os.path.join(PLOTS_DIR, "test_results.png"))

    print("\nFinal Test Metrics:")
    print(f"Test Loss     : {test_loss:.4f}")
    print(f"Test Accuracy : {test_acc * 100:.2f}%")
    print(f"Plots saved to: {PLOTS_DIR}")