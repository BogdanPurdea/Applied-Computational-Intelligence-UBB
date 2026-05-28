import os
import time
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from DatasetPreProcessing import train_loader, val_loader
from Model import FCN

# =============================================================================
# CONFIG
# =============================================================================
EPOCHS      = 150
LR          = 1e-3
WEIGHT_DECAY = 1e-4

CKPT_PATH    = "./gtsrb_fcn_best.pth"
HISTORY_PATH = "./training_history.json"
PLOT_PATH    = "./training_curves.png"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =============================================================================
# HELPERS
# =============================================================================
def accuracy(logits, targets):
    return (logits.argmax(dim=1) == targets).float().mean().item()

from tqdm import tqdm

def train_one_epoch(model, loader, criterion, optimizer):
    model.train()
    total_loss = total_acc = 0.0
    pbar = tqdm(loader, desc="  Train", leave=False, bar_format="{l_bar}{bar:20}{r_bar}")
    for imgs, labels in pbar:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        logits = model(imgs)
        loss   = criterion(logits, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item()
        total_acc  += accuracy(logits, labels)
    return total_loss / len(loader), total_acc / len(loader)

@torch.no_grad()
def evaluate(model, loader, criterion):
    model.eval()
    total_loss = total_acc = 0.0
    pbar = tqdm(loader, desc="  Val  ", leave=False, bar_format="{l_bar}{bar:20}{r_bar}")
    for imgs, labels in pbar:
        imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
        logits      = model(imgs)
        total_loss += criterion(logits, labels).item()
        total_acc  += accuracy(logits, labels)
    return total_loss / len(loader), total_acc / len(loader)

def train_model():
    print("\n[1/3]  Building model ...")
    model = FCN().to(DEVICE)
    total_p = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Trainable params : {total_p:,}")
    print(f"  Device           : {DEVICE}")

    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=LR * 1e-2)

    print("\n[2/3]  Training ...\n")
    print(f"  {'Ep':>3} | {'Tr Loss':>9} {'Tr Acc%':>8} | {'Vl Loss':>9} {'Vl Acc%':>8} | {'LR':>9} | {'Time':>6} |")
    print("  " + "-" * 72)

    best_val_acc = 0.0
    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    for epoch in range(1, EPOCHS + 1):
        t0 = time.time()

        tr_l, tr_a = train_one_epoch(model, train_loader, criterion, optimizer)
        vl_l, vl_a = evaluate(model, val_loader, criterion)
        scheduler.step()

        history["train_loss"].append(tr_l)
        history["train_acc"].append(tr_a)
        history["val_loss"].append(vl_l)
        history["val_acc"].append(vl_a)

        cur_lr  = scheduler.get_last_lr()[0]
        elapsed = time.time() - t0

        tag = ""
        if vl_a > best_val_acc:
            best_val_acc = vl_a
            torch.save({
                "epoch": epoch,
                "model_state": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "val_acc": vl_a,
                "history": history,
            }, CKPT_PATH)
            tag = "  * saved"

        print(
            f"  {epoch:>3} | {tr_l:>9.4f} {tr_a * 100:>7.2f}% | "
            f"{vl_l:>9.4f} {vl_a * 100:>7.2f}% | "
            f"{cur_lr:>9.2e} | {elapsed:>5.1f}s |{tag}"
        )

    print("  " + "-" * 72)
    print(f"\n  Best val acc   : {best_val_acc * 100:.2f}%")
    print(f"  Checkpoint     -> {CKPT_PATH}")

    # =============================================================================
    # SAVE & PLOT
    # =============================================================================
    print("\n[3/3] Saving history and plotting...")
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
    print(f"\n  History saved  -> {HISTORY_PATH}")

    epochs_list = range(1, len(history["train_loss"]) + 1)
    best_e  = history["val_acc"].index(max(history["val_acc"])) + 1
    best_va = max(history["val_acc"]) * 100

    fig = plt.figure(figsize=(14, 5))
    fig.suptitle("GTSRB FCN - Training History", fontsize=14, fontweight="bold", y=1.02)
    gs  = gridspec.GridSpec(1, 2, figure=fig, wspace=0.32)

    ax1 = fig.add_subplot(gs[0])
    ax1.plot(epochs_list, history["train_loss"], "o-",  color="#2196F3", lw=2, ms=3, label="Train Loss")
    ax1.plot(epochs_list, history["val_loss"],   "s--", color="#FF5722", lw=2, ms=3, label="Val Loss")
    ax1.axvline(best_e, color="#9E9E9E", ls=":", lw=1.4, label=f"Best epoch ({best_e})")
    ax1.set_title("Loss per Epoch")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    ax2 = fig.add_subplot(gs[1])
    ax2.plot(epochs_list, [a * 100 for a in history["train_acc"]], "o-",  color="#2196F3", lw=2, ms=3, label="Train Acc")
    ax2.plot(epochs_list, [a * 100 for a in history["val_acc"]],   "s--", color="#FF5722", lw=2, ms=3, label="Val Acc")
    ax2.axvline(best_e, color="#9E9E9E", ls=":", lw=1.4, label=f"Best epoch ({best_e})")
    ax2.axhline(best_va, color="#4CAF50", ls="--", lw=1.2, label=f"Best val {best_va:.2f}%")
    ax2.set_title("Accuracy per Epoch")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy (%)")
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150, bbox_inches="tight")
    print(f"  Plot saved     -> {PLOT_PATH}")
    print("\n  All done.")

if __name__ == '__main__':
    train_model()