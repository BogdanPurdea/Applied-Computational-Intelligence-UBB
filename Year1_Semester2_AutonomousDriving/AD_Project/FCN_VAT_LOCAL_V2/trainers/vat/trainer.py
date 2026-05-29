import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from tqdm import tqdm
import matplotlib.pyplot as plt

def vat_loss(model, x, logits, xi=1e-6, eps=2.5, ip=1):
    d = torch.randn_like(x)
    # L2 norm over the batch
    d_flat = d.view(d.size(0), -1)
    d = d / (1e-12 + torch.norm(d_flat, dim=1).view(-1, 1, 1, 1))
    
    for _ in range(ip):
        d.requires_grad_()
        x_pert = x + xi * d
        logits_pert = model(x_pert)
        
        probs = F.softmax(logits.detach(), dim=1)
        log_probs_pert = F.log_softmax(logits_pert, dim=1)
        # Using batchmean as recommended by PyTorch for KL Div
        kl = F.kl_div(log_probs_pert, probs, reduction='batchmean')
        
        grad = torch.autograd.grad(kl, d)[0]
        grad_flat = grad.view(grad.size(0), -1)
        d = grad / (1e-12 + torch.norm(grad_flat, dim=1).view(-1, 1, 1, 1))
        d = d.detach()
        
    r_vadv = eps * d
    x_vadv = x + r_vadv
    logits_vadv = model(x_vadv)
    
    probs = F.softmax(logits.detach(), dim=1)
    log_probs_vadv = F.log_softmax(logits_vadv, dim=1)
    lds = F.kl_div(log_probs_vadv, probs, reduction='batchmean')
    return lds

def train_vat(model, labeled_loader, unlabeled_loader, test_loader, epochs=15, lr=1e-3, epsilon=2.5, lambda_vat=1.0, ip=1, device="cuda", save_name="vat_best.pth"):
    print("="*50)
    print("  VIRTUAL ADVERSARIAL TRAINING (VAT)")
    print(f"  eps={epsilon}, lambda={lambda_vat}, ip={ip}")
    print("="*50)
    
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()
    
    best_acc = 0.0
    history = {"sup_loss": [], "vat_loss": [], "train_acc": [], "test_acc": []}
    for epoch in range(1, epochs + 1):
        model.train()
        total_sup_loss = 0.0
        total_vat_loss = 0.0
        correct = 0
        total = 0
        
        def cycle(iterable):
            while True:
                for x in iterable:
                    yield x
                    
        labeled_iter = iter(cycle(labeled_loader)) if labeled_loader is not None else None
        
        pbar = tqdm(unlabeled_loader, desc=f"Epoch {epoch}/{epochs}", leave=False, bar_format="{l_bar}{bar:20}{r_bar}")
        for unlab_imgs, _ in pbar:
            unlab_imgs = unlab_imgs.to(device)
            optimizer.zero_grad()
            
            loss_sup = torch.tensor(0.0).to(device)
            if labeled_iter is not None:
                lab_imgs, lab_targets = next(labeled_iter)
                lab_imgs, lab_targets = lab_imgs.to(device), lab_targets.to(device)
                lab_logits = model(lab_imgs)
                loss_sup = criterion(lab_logits, lab_targets)
                correct += (lab_logits.argmax(dim=1) == lab_targets).sum().item()
                total += lab_targets.size(0)
                
            # VAT Loss on unlabeled
            unlab_logits = model(unlab_imgs)
            loss_vat = vat_loss(model, unlab_imgs, unlab_logits, eps=epsilon, ip=ip)
            
            loss = loss_sup + lambda_vat * loss_vat
            loss.backward()
            optimizer.step()
            
            total_sup_loss += loss_sup.item()
            total_vat_loss += loss_vat.item()
            
            pbar.set_postfix({"sup": f"{loss_sup.item():.3f}", "vat": f"{loss_vat.item():.3f}"})
            
        train_acc = correct / total if total > 0 else 0.0
        
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
            
        print(f"Epoch {epoch:2d}/{epochs} | Sup Loss: {total_sup_loss/len(unlabeled_loader):.4f} | VAT Loss: {total_vat_loss/len(unlabeled_loader):.4f} | Train Acc: {train_acc*100:.2f}% | Test Acc: {test_acc*100:.2f}% {tag}")
        
        history["sup_loss"].append(total_sup_loss/len(unlabeled_loader))
        history["vat_loss"].append(total_vat_loss/len(unlabeled_loader))
        history["train_acc"].append(train_acc * 100)
        history["test_acc"].append(test_acc * 100)
        
    print(f"\nVAT Training Complete! Best Test Accuracy: {best_acc*100:.2f}%")
    
    os.makedirs("training_plots", exist_ok=True)
    prefix = save_name.replace(".pth", "")
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs + 1), history["sup_loss"], label="Sup Loss", marker='o')
    plt.plot(range(1, epochs + 1), history["vat_loss"], label="VAT Loss", marker='o')
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
