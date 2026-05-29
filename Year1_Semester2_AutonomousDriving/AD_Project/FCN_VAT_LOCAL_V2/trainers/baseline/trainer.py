import os
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
import matplotlib.pyplot as plt

def train_baseline(model, labeled_loader, test_loader, epochs=15, lr=1e-3, device="cuda", save_name="baseline_best.pth"):
    print("="*50)
    print("  SUPERVISED BASELINE TRAINING")
    print("="*50)
    
    if labeled_loader is None:
        raise ValueError("Baseline training requires a labeled dataset!")

    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()
    
    best_acc = 0.0
    history = {"train_loss": [], "train_acc": [], "test_acc": []}
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(labeled_loader, desc=f"Epoch {epoch}/{epochs}", leave=False, bar_format="{l_bar}{bar:20}{r_bar}")
        for imgs, targets in pbar:
            imgs, targets = imgs.to(device), targets.to(device)
            
            optimizer.zero_grad()
            logits = model(imgs)
            loss = criterion(logits, targets)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            correct += (logits.argmax(dim=1) == targets).sum().item()
            total += targets.size(0)
            
            pbar.set_postfix({"loss": f"{loss.item():.4f}"})
            
        train_acc = correct / total
        
        # Test evaluation
        model.eval()
        test_correct = 0
        test_total = 0
        with torch.no_grad():
            for imgs, targets in test_loader:
                imgs, targets = imgs.to(device), targets.to(device)
                logits = model(imgs)
                test_correct += (logits.argmax(dim=1) == targets).sum().item()
                test_total += targets.size(0)
                
        test_acc = test_correct / test_total
        
        tag = ""
        if test_acc > best_acc:
            best_acc = test_acc
            tag = " *Best*"
            os.makedirs("checkpoints", exist_ok=True)
            torch.save(model.state_dict(), f"checkpoints/{save_name}")
            
        print(f"Epoch {epoch:2d}/{epochs} | Train Loss: {total_loss/len(labeled_loader):.4f} | Train Acc: {train_acc*100:.2f}% | Test Acc: {test_acc*100:.2f}% {tag}")
        
        history["train_loss"].append(total_loss/len(labeled_loader))
        history["train_acc"].append(train_acc * 100)
        history["test_acc"].append(test_acc * 100)
        
    print(f"\nBaseline Training Complete! Best Test Accuracy: {best_acc*100:.2f}%")
    
    os.makedirs("training_plots", exist_ok=True)
    prefix = save_name.replace(".pth", "")
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs + 1), history["train_loss"], label="Train Loss", marker='o')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title(f"{prefix} - Loss")
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs + 1), history["train_acc"], label="Train Acc", marker='o')
    plt.plot(range(1, epochs + 1), history["test_acc"], label="Test Acc", marker='o')
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy (%)")
    plt.title(f"{prefix} - Accuracy")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join("training_plots", f"{prefix}_plots.png"))
    plt.close()
    
    return best_acc
