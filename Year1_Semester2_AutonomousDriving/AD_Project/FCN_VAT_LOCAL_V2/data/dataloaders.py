import os
import torch
from torch.utils.data import DataLoader, random_split, Dataset, ConcatDataset
from torchvision import datasets, transforms
from PIL import Image

def get_dataloaders(dataset_name, batch_size, labeled_ratio, num_workers=0):
    if dataset_name.lower() == "gtsrb":
        return get_gtsrb_dataloaders(batch_size, labeled_ratio, num_workers)
    elif dataset_name.lower() == "synthetic":
        return get_synthetic_dataloaders(batch_size, labeled_ratio, num_workers)
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")

def get_gtsrb_dataloaders(batch_size, labeled_ratio, num_workers):
    IMG_SIZE = 48
    GTSRB_MEAN = (0.3337, 0.3064, 0.3171)
    GTSRB_STD  = (0.2672, 0.2564, 0.2629)
    # Local path for GTSRB dataset
    DATA_ROOT = "./gtsrb_dataset"
    
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
    
    full_train = datasets.GTSRB(root=DATA_ROOT, split="train", transform=train_transform, download=True)
    test_dataset = datasets.GTSRB(root=DATA_ROOT, split="test", transform=val_test_transform, download=True)
    
    total_len = len(full_train)
    labeled_len = int(total_len * labeled_ratio)
    unlabeled_len = total_len - labeled_len
    
    if labeled_len == total_len:
        labeled_dataset = full_train
        unlabeled_dataset = None
    elif labeled_len == 0:
        labeled_dataset = None
        unlabeled_dataset = full_train
    else:
        labeled_dataset, unlabeled_dataset = random_split(
            full_train, [labeled_len, unlabeled_len], generator=torch.Generator().manual_seed(42)
        )
    
    labeled_loader = DataLoader(labeled_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, drop_last=True) if labeled_dataset else None
    unlabeled_loader = DataLoader(unlabeled_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, drop_last=True) if unlabeled_dataset else None
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    num_classes = 43
    return labeled_loader, unlabeled_loader, test_loader, num_classes


class SyntheticDataset(Dataset):
    def __init__(self, root_dir, transform=None, is_unlabeled=False):
        self.root_dir = root_dir
        self.transform = transform
        self.is_unlabeled = is_unlabeled
        self.image_files = []
        self.labels = []
        
        # Class mapping
        self.class_to_idx = {"circles": 0, "moons": 1}
        
        if is_unlabeled:
            # Unlabeled files are directly in root_dir
            if os.path.exists(root_dir):
                for f in os.listdir(root_dir):
                    if f.endswith('.png'):
                        self.image_files.append(os.path.join(root_dir, f))
                        # Try to extract pseudo-label from filename, since they have names like "unlabeled_circles_0000.png"
                        if "circles" in f:
                            self.labels.append(self.class_to_idx["circles"])
                        elif "moons" in f:
                            self.labels.append(self.class_to_idx["moons"])
                        else:
                            self.labels.append(-1)
        else:
            # Labeled/test files are in subfolders
            if os.path.exists(root_dir):
                for class_name in self.class_to_idx.keys():
                    class_dir = os.path.join(root_dir, class_name)
                    if os.path.exists(class_dir):
                        for f in os.listdir(class_dir):
                            if f.endswith('.png'):
                                self.image_files.append(os.path.join(class_dir, f))
                                self.labels.append(self.class_to_idx[class_name])
                                
    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

def get_synthetic_dataloaders(batch_size, labeled_ratio, num_workers):
    IMG_SIZE = 48
    BASE_DIR = "synthetic_dataset"
    
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    labeled_dataset = SyntheticDataset(os.path.join(BASE_DIR, "labeled"), transform=transform)
    unlabeled_dataset = SyntheticDataset(os.path.join(BASE_DIR, "unlabeled"), transform=transform, is_unlabeled=True)
    test_dataset = SyntheticDataset(os.path.join(BASE_DIR, "test"), transform=transform)
    
    if labeled_ratio == 1.0:
        labeled_dataset = ConcatDataset([labeled_dataset, unlabeled_dataset])
        unlabeled_dataset = None
    
    labeled_loader = DataLoader(labeled_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, drop_last=True) if len(labeled_dataset) > 0 else None
    
    if unlabeled_dataset and len(unlabeled_dataset) > 0 and labeled_ratio < 1.0:
        unlabeled_loader = DataLoader(unlabeled_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers, drop_last=True)
    else:
        unlabeled_loader = None
        
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    num_classes = 2
    return labeled_loader, unlabeled_loader, test_loader, num_classes
