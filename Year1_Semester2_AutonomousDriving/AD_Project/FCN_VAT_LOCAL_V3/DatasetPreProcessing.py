# =============================================================================
# GTSRB FCN — Step 2: Data Preparation
# =============================================================================

import os
import platform
import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

def prepare_data_pipeline():
    """
    Creates target directories, downloads the GTSRB dataset, applies transformations,
    and initializes data loaders for training, validation, and testing.
    Returns dataset and dataloader objects for subsequent processing steps.
    """
    # ─── CONFIG ───────────────────────────────────────────────────────────────────
    IMG_SIZE   = 48
    BATCH_SIZE = 128
    VAL_SPLIT  = 0.15
    DATA_ROOT  = "/data/gtsrb-german-traffic-sign"

    # Sets worker count based on operating system to prevent multiprocessing errors.
    if platform.system() == "Windows":
        NUM_WORKERS = 0
    else:
        NUM_WORKERS = 4

    # Creates target directory structure. Requires elevated permissions on some systems.
    os.makedirs(DATA_ROOT, exist_ok=True)

    # ─── GTSRB-SPECIFIC NORMALIZATION STATS ──────────────────────────────────────
    # Defines pre-computed per-channel mean and standard deviation.
    GTSRB_MEAN = (0.3337, 0.3064, 0.3171)
    GTSRB_STD  = (0.2672, 0.2564, 0.2629)

    # ─── TRANSFORMS ───────────────────────────────────────────────────────────────
    # Defines transformations for training data to reduce overfitting.
    train_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),

        # Applies geometric augmentations.
        transforms.RandomRotation(degrees=15),
        transforms.RandomAffine(
            degrees=0,
            translate=(0.1, 0.1),
            scale=(0.9, 1.1),
        ),
        transforms.RandomHorizontalFlip(p=0.1),

        # Applies photometric augmentations.
        transforms.ColorJitter(
            brightness=0.4,
            contrast=0.4,
            saturation=0.3,
            hue=0.05,
        ),

        # Converts image to floating-point tensor in range 0 to 1.
        transforms.ToTensor(),
        # Normalizes tensor channels.
        transforms.Normalize(GTSRB_MEAN, GTSRB_STD),
    ])

    # Defines transformations for validation and test data.
    val_test_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(GTSRB_MEAN, GTSRB_STD),
    ])

    # ─── DATASETS ─────────────────────────────────────────────────────────────────
    # Prints status message to standard output.
    print("Loading datasets ...")

    # Instantiates the training dataset with augmentations.
    full_train_aug = datasets.GTSRB(
        root=DATA_ROOT, split="train",
        transform=train_transform,
        download=True,
    )
    # Instantiates the training dataset without augmentations for validation.
    full_train_clean = datasets.GTSRB(
        root=DATA_ROOT, split="train",
        transform=val_test_transform,
        download=False,
    )
    # Instantiates the test dataset.
    test_dataset = datasets.GTSRB(
        root=DATA_ROOT, split="test",
        transform=val_test_transform,
        download=True,
    )

    # ─── TRAIN / VAL SPLIT ────────────────────────────────────────────────────────
    # Calculates dataset split proportions.
    n_total = len(full_train_aug)
    n_val   = int(n_total * VAL_SPLIT)
    n_train = n_total - n_val

    # Initializes random number generator with a fixed seed.
    generator = torch.Generator().manual_seed(42)

    # Splits datasets using identical random seeds to ensure matching indices.
    train_dataset, _ = random_split(
        full_train_aug, [n_train, n_val], generator=generator
    )
    _, val_dataset = random_split(
        full_train_clean, [n_train, n_val],
        generator=torch.Generator().manual_seed(42)
    )

    # ─── DATALOADERS ──────────────────────────────────────────────────────────────
    # Initializes dataloader for training data.
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=True,
        drop_last=True,
    )
    # Initializes dataloader for validation data.
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True,
    )
    # Initializes dataloader for test data.
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True,
    )

    return train_dataset, val_dataset, test_dataset, train_loader, val_loader, test_loader


if __name__ == "__main__":
    # Executes the data pipeline method.
    train_ds, val_ds, test_ds, train_ld, val_ld, test_ld = prepare_data_pipeline()

    # Prints verification metrics to standard output.
    print(f"\n{'─'*45}")
    print(f"  Train samples  : {len(train_ds):>7,}")
    print(f"  Val   samples  : {len(val_ds):>7,}")
    print(f"  Test  samples  : {len(test_ds):>7,}")
    print(f"  Train batches  : {len(train_ld):>7,}")
    print(f"  Val   batches  : {len(val_ld):>7,}")
    print(f"  Test  batches  : {len(test_ld):>7,}")
    print(f"{'─'*45}")

    # Extracts a single batch to verify tensor shapes and parameters.
    imgs, labels = next(iter(train_ld))
    print(f"\n  Batch image tensor : {tuple(imgs.shape)}")
    print(f"  Batch label tensor : {tuple(labels.shape)}")
    print(f"  Pixel range        : [{imgs.min():.3f},  {imgs.max():.3f}]")
    print(f"  Unique classes     : {labels.unique().numel()}")
    print(f"\n✓ Data pipeline ready.")