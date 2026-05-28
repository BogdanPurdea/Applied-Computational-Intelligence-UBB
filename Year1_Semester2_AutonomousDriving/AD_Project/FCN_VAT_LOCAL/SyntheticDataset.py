import os
import glob
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

# Use GTSRB image size
from Model import IMG_SIZE

# Simple normalization to [-1, 1]
MEAN = (0.5, 0.5, 0.5)
STD  = (0.5, 0.5, 0.5)

synthetic_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])

class SyntheticLabeledDataset(Dataset):
    def __init__(self, root_dir="synthetic_dataset/labeled", transform=synthetic_transform):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        # 0 for circles, 1 for moons
        self.class_map = {"circles": 0, "moons": 1}
        
        for cls_name, cls_idx in self.class_map.items():
            cls_dir = os.path.join(self.root_dir, cls_name)
            if os.path.exists(cls_dir):
                paths = glob.glob(os.path.join(cls_dir, "*.png"))
                self.image_paths.extend(paths)
                self.labels.extend([cls_idx] * len(paths))
                
    def __len__(self):
        return len(self.image_paths)
        
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx]


class SyntheticUnlabeledDataset(Dataset):
    def __init__(self, root_dir="synthetic_dataset/unlabeled", transform=synthetic_transform):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        
        if os.path.exists(self.root_dir):
            self.image_paths = glob.glob(os.path.join(self.root_dir, "*.png"))
            
    def __len__(self):
        return len(self.image_paths)
        
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        # Return -1 as label for unlabeled data
        return image, -1


class SyntheticTestDataset(Dataset):
    def __init__(self, root_dir="synthetic_dataset/test", transform=synthetic_transform):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        self.class_map = {"circles": 0, "moons": 1}
        
        for cls_name, cls_idx in self.class_map.items():
            cls_dir = os.path.join(self.root_dir, cls_name)
            if os.path.exists(cls_dir):
                paths = glob.glob(os.path.join(cls_dir, "*.png"))
                self.image_paths.extend(paths)
                self.labels.extend([cls_idx] * len(paths))
                
    def __len__(self):
        return len(self.image_paths)
        
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, self.labels[idx]
