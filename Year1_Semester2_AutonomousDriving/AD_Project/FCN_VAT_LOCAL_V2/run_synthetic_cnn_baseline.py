import torch
from data.dataloaders import get_dataloaders
from models.CNN.cnn import CNN
from trainers.baseline.trainer import train_baseline

# ==========================================
# HYPERPARAMETERS
# ==========================================
DATASET = "synthetic"
LABELED_RATIO = 1.0  # 1.0 means fully supervised (use all labels)
EPOCHS = 15
BATCH_SIZE = 32
LR = 1e-3
SAVE_NAME = "run_synthetic_cnn_baseline.pth"
# ==========================================

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 1. Dataloaders
    labeled_loader, unlabeled_loader, test_loader, num_classes = get_dataloaders(
        dataset_name=DATASET,
        batch_size=BATCH_SIZE,
        labeled_ratio=LABELED_RATIO,
        num_workers=0
    )

    # 2. Model
    model = CNN(num_classes=num_classes).to(device)

    # 3. Trainer
    train_baseline(
        model=model,
        labeled_loader=labeled_loader,
        test_loader=test_loader,
        epochs=EPOCHS,
        lr=LR,
        device=device,
        save_name=SAVE_NAME
    )

if __name__ == "__main__":
    main()
