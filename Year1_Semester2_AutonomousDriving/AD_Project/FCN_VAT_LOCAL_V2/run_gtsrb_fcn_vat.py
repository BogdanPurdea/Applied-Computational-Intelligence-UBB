import torch
from data.dataloaders import get_dataloaders
from models.FCN.fcn import FCN
from trainers.vat.trainer import train_vat

# ==========================================
# HYPERPARAMETERS
# ==========================================
DATASET = "gtsrb"
LABELED_RATIO = 0.1  # Semi-supervised: keep only 10% of labels
EPOCHS = 15
BATCH_SIZE = 32
LR = 1e-3

# VAT Specific Hyperparameters
EPSILON = 2.5
LAMBDA_VAT = 1.0
IP = 1
SAVE_NAME = "run_gtsrb_fcn_vat.pth"
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
    model = FCN(num_classes=num_classes).to(device)

    # 3. Trainer
    train_vat(
        model=model,
        labeled_loader=labeled_loader,
        unlabeled_loader=unlabeled_loader,
        test_loader=test_loader,
        epochs=EPOCHS,
        lr=LR,
        epsilon=EPSILON,
        lambda_vat=LAMBDA_VAT,
        ip=IP,
        device=device,
        save_name=SAVE_NAME
    )

if __name__ == "__main__":
    main()
