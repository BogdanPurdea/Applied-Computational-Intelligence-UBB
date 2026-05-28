import torch
import numpy as np
from sklearn.metrics import classification_report
from torch.utils.data import DataLoader

from Model import FCN
from SyntheticDataset import SyntheticTestDataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CKPT_PATH = "./synthetic_best.pth"

def test_synthetic():
    print("="*40)
    print("  EVALUATING SYNTHETIC MODEL")
    print("="*40)

    print(f"Loading best model from {CKPT_PATH}...")
    model = FCN(num_classes=2).to(DEVICE)
    try:
        model.load_state_dict(torch.load(CKPT_PATH, map_location=DEVICE, weights_only=False))
    except Exception as e:
        print(f"Failed to load checkpoint: {e}")
        return
        
    model.eval()
    
    test_ds = SyntheticTestDataset()
    test_loader = DataLoader(test_ds, batch_size=64, shuffle=False)
    
    all_preds = []
    all_labels = []
    
    print("Evaluating on Synthetic Test Dataset...")
    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs = imgs.to(DEVICE)
            logits = model(imgs)
            preds = logits.argmax(dim=1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
            
    test_accuracy = (np.array(all_preds) == np.array(all_labels)).mean()
    
    print("\n" + "=" * 30)
    print(f"TEST RESULTS")
    print("=" * 30)
    print(f"Accuracy:     {test_accuracy * 100:.2f}%")
    print("=" * 30)
    
    print("\nClassification Report (0: circles, 1: moons):")
    print(classification_report(all_labels, all_preds, digits=4))

if __name__ == '__main__':
    test_synthetic()
