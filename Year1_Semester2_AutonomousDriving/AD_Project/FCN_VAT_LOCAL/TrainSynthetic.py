import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from tqdm import tqdm

from Model import FCN
from SyntheticDataset import SyntheticLabeledDataset, SyntheticUnlabeledDataset, SyntheticTestDataset

# CONFIG
BATCH_SIZE = 32
EPOCHS = 15
LR = 1e-3
WEIGHT_DECAY = 1e-4
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CKPT_PATH = "./synthetic_best.pth"
PSEUDO_LABEL_THRESHOLD = 0.95
UNLABELED_WEIGHT = 1.0

def train_synthetic():
    print("="*50)
    print("  SEMI-SUPERVISED TRAINING ON SYNTHETIC DATA")
    print("="*50)

    print("\n[1/3] Loading Datasets...")
    labeled_ds = SyntheticLabeledDataset()
    unlabeled_ds = SyntheticUnlabeledDataset()
    test_ds = SyntheticTestDataset()
    
    labeled_loader = DataLoader(labeled_ds, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
    unlabeled_loader = DataLoader(unlabeled_ds, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False)
    
    print(f"  Labeled samples:   {len(labeled_ds)}")
    print(f"  Unlabeled samples: {len(unlabeled_ds)}")
    print(f"  Test samples:      {len(test_ds)}")

    print("\n[2/3] Initializing Model...")
    # 2 classes: circles (0) and moons (1)
    model = FCN(num_classes=2).to(DEVICE)
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    criterion = nn.CrossEntropyLoss()
    
    print("\n[3/3] Starting Training Loop...")
    best_acc = 0.0
    
    for epoch in range(1, EPOCHS + 1):
        model.train()
        total_loss = 0.0
        labeled_correct = 0
        labeled_total = 0
        pseudo_labels_used = 0
        
        # Cycle through labeled data since unlabeled dataset is much larger
        def cycle(iterable):
            while True:
                for x in iterable:
                    yield x
                    
        labeled_iter = iter(cycle(labeled_loader))
        
        pbar = tqdm(unlabeled_loader, desc=f"Epoch {epoch}/{EPOCHS}", leave=False, bar_format="{l_bar}{bar:20}{r_bar}")
        for unlab_imgs, _ in pbar:
            lab_imgs, lab_targets = next(labeled_iter)
            
            lab_imgs = lab_imgs.to(DEVICE)
            lab_targets = lab_targets.to(DEVICE)
            unlab_imgs = unlab_imgs.to(DEVICE)
            
            optimizer.zero_grad()
            
            # Supervised Loss on Labeled Data
            lab_logits = model(lab_imgs)
            loss_sup = criterion(lab_logits, lab_targets)
            
            # Unsupervised Loss (Pseudo-Labeling) on Unlabeled Data
            unlab_logits = model(unlab_imgs)
            probs = F.softmax(unlab_logits, dim=1)
            max_probs, pseudo_targets = torch.max(probs, dim=1)
            
            # Only use high-confidence predictions as targets
            mask = max_probs >= PSEUDO_LABEL_THRESHOLD
            loss_unsup = 0.0
            if mask.sum() > 0:
                loss_unsup = criterion(unlab_logits[mask], pseudo_targets[mask])
                pseudo_labels_used += mask.sum().item()
                
            loss = loss_sup + UNLABELED_WEIGHT * loss_unsup
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            labeled_correct += (lab_logits.argmax(dim=1) == lab_targets).sum().item()
            labeled_total += lab_targets.size(0)
            
            pbar.set_postfix({"loss": f"{loss.item():.4f}", "pseudo": pseudo_labels_used})
            
        # Evaluation at the end of epoch
        model.eval()
        test_correct = 0
        test_total = 0
        with torch.no_grad():
            for imgs, targets in test_loader:
                imgs, targets = imgs.to(DEVICE), targets.to(DEVICE)
                logits = model(imgs)
                test_correct += (logits.argmax(dim=1) == targets).sum().item()
                test_total += targets.size(0)
                
        test_acc = test_correct / test_total
        train_acc = labeled_correct / labeled_total
        
        tag = ""
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), CKPT_PATH)
            tag = " *Saved Best*"
            
        print(f"Epoch {epoch:2d}/{EPOCHS} | Train Acc: {train_acc*100:.2f}% | Test Acc: {test_acc*100:.2f}% | Pseudo Lbls: {pseudo_labels_used} {tag}")

    print(f"\nTraining Complete! Best Test Accuracy: {best_acc*100:.2f}%")

if __name__ == "__main__":
    train_synthetic()
