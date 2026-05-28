# =============================================================================
# GTSRB FCN — Step 2: Data Preparation
# =============================================================================

import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

# ─── CONFIG ───────────────────────────────────────────────────────────────────
from Model import IMG_SIZE

BATCH_SIZE = 128
VAL_SPLIT  = 0.15        # 15% of train → validation
DATA_ROOT  = "./data"    # dataset downloaded here automatically
NUM_WORKERS = 0          # 0 on Windows to prevent multiprocess errors

# ─── GTSRB-SPECIFIC NORMALIZATION STATS ──────────────────────────────────────
# Pre-computed per-channel mean/std for GTSRB (NOT ImageNet stats)
GTSRB_MEAN = (0.3337, 0.3064, 0.3171)
GTSRB_STD  = (0.2672, 0.2564, 0.2629)

# ─── TRANSFORMS ───────────────────────────────────────────────────────────────
# Train: heavy augmentation to fight overfitting on small sign images
# Val / Test: only resize + normalize — no randomness, reproducible evaluation

train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),

    # Geometric augmentations
    transforms.RandomRotation(degrees=15),             # signs can be slightly tilted
    transforms.RandomAffine(
        degrees=0,
        translate=(0.1, 0.1),                          # small position jitter
        scale=(0.9, 1.1),                              # slight zoom in/out
    ),
    transforms.RandomHorizontalFlip(p=0.1),            # low prob — most signs are asymmetric

    # Photometric augmentations
    transforms.ColorJitter(
        brightness=0.4,                                # real-world lighting varies a lot
        contrast=0.4,
        saturation=0.3,
        hue=0.05,
    ),

    transforms.ToTensor(),                             # PIL → float32 tensor [0, 1]
    transforms.Normalize(GTSRB_MEAN, GTSRB_STD),      # zero-center per channel
])

val_test_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(GTSRB_MEAN, GTSRB_STD),
])

# ─── DATASETS ─────────────────────────────────────────────────────────────────
# torchvision downloads GTSRB automatically on first run (~300 MB)

print("Loading datasets …")

full_train_aug = datasets.GTSRB(
    root=DATA_ROOT, split="train",
    transform=train_transform,
    download=True,
)
full_train_clean = datasets.GTSRB(
    root=DATA_ROOT, split="train",
    transform=val_test_transform,
    download=False,                                    # already downloaded above
)
test_dataset = datasets.GTSRB(
    root=DATA_ROOT, split="test",
    transform=val_test_transform,
    download=True,
)

# ─── TRAIN / VAL SPLIT ────────────────────────────────────────────────────────
# Both splits use the same random seed so indices are identical.
# train_dataset  → augmented transform  (for training)
# val_dataset    → clean transform      (for unbiased evaluation)

n_total = len(full_train_aug)
n_val   = int(n_total * VAL_SPLIT)
n_train = n_total - n_val

generator = torch.Generator().manual_seed(42)         # reproducible split

train_dataset, _ = random_split(
    full_train_aug, [n_train, n_val], generator=generator
)
_, val_dataset = random_split(
    full_train_clean, [n_train, n_val],
    generator=torch.Generator().manual_seed(42)        # same seed → same indices
)

# ─── DATALOADERS ──────────────────────────────────────────────────────────────
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,                                      # shuffle every epoch
    num_workers=NUM_WORKERS,
    pin_memory=False,                                  # avoid Windows hang
    drop_last=True,                                    # avoid single-sample batches (breaks BN)
)
val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=False,
)
test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=False,
)

# ─── SANITY CHECK ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'─'*45}")
    print(f"  Train samples  : {len(train_dataset):>7,}")
    print(f"  Val   samples  : {len(val_dataset):>7,}")
    print(f"  Test  samples  : {len(test_dataset):>7,}")
    print(f"  Batch size     : {BATCH_SIZE:>7}")
    print(f"  Train batches  : {len(train_loader):>7,}")
    print(f"  Val   batches  : {len(val_loader):>7,}")
    print(f"  Test  batches  : {len(test_loader):>7,}")
    print(f"{'─'*45}")

    # Check one batch shape
    imgs, labels = next(iter(train_loader))
    print(f"\n  Batch image tensor : {tuple(imgs.shape)}")
    print(f"  Batch label tensor : {tuple(labels.shape)}")
    print(f"  Pixel range        : [{imgs.min():.3f},  {imgs.max():.3f}]")
    print(f"  Unique classes in batch: {labels.unique().numel()}")
    print(f"\n✓ Data pipeline ready.")