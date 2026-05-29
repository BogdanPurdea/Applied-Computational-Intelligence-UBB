import sys
import os
import torch
import importlib
from data.dataloaders import get_dataloaders

def main():
    if len(sys.argv) < 7:
        print("Usage: _gui_runner.py <module_name> <epochs> <batch_size> <lr> <dataset> <mode>")
        sys.exit(1)

    module_name = sys.argv[1]
    epochs = int(sys.argv[2])
    batch_size = int(sys.argv[3])
    lr = float(sys.argv[4])
    dataset = sys.argv[5]
    mode = sys.argv[6]

    # Dynamically import the requested script
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        print(f"Error importing task '{module_name}': {e}")
        sys.exit(1)

    # Monkeypatch hyperparameters into the module before running its logic
    mod.EPOCHS = epochs
    mod.BATCH_SIZE = batch_size
    mod.LR = lr
    mod.DATASET = dataset

    if mode == "train":
        print(f"Executing {module_name}.main() in TRAIN mode with:")
        print(f"  Dataset: {dataset}")
        print(f"  Epochs: {epochs}")
        print(f"  Batch Size: {batch_size}")
        print(f"  LR: {lr}")
        # Run the train entry point
        mod.main()
        
    elif mode == "test":
        print(f"Executing test evaluation for {module_name}")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        
        # Determine the labeled ratio used by the module (usually 1.0 or 0.1)
        labeled_ratio = getattr(mod, "LABELED_RATIO", 1.0)
        
        print(f"Loading test dataloaders for '{dataset}'...")
        _, _, test_loader, num_classes = get_dataloaders(
            dataset_name=dataset,
            batch_size=batch_size,
            labeled_ratio=labeled_ratio,
            num_workers=0
        )
        
        # Load the architecture
        model = None
        if "cnn" in module_name.lower():
            from models.CNN.cnn import CNN
            model = CNN(num_classes=num_classes).to(device)
        elif "fcn" in module_name.lower():
            from models.FCN.fcn import FCN
            model = FCN(num_classes=num_classes).to(device)
        else:
            print(f"Could not determine model architecture (CNN/FCN) from {module_name}")
            sys.exit(1)
            
        save_name = getattr(mod, "SAVE_NAME", f"{module_name}.pth")
        checkpoint_path = os.path.join("checkpoints", save_name)
        
        if not os.path.exists(checkpoint_path):
            print(f"Error: Checkpoint not found at '{checkpoint_path}'")
            print("Please run the 'train' task first to generate the checkpoint.")
            sys.exit(1)
            
        print(f"Loading weights from {checkpoint_path}...")
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        model.eval()
        
        print("Starting evaluation...")
        correct = 0
        total = 0
        
        with torch.no_grad():
            for imgs, targets in test_loader:
                imgs, targets = imgs.to(device), targets.to(device)
                logits = model(imgs)
                
                # Check if it's FCN returning spatial maps
                if len(logits.shape) > 2:
                    # e.g., (batch, classes, H, W)
                    logits = logits.mean(dim=[2, 3])
                    
                correct += (logits.argmax(dim=1) == targets).sum().item()
                total += targets.size(0)
                
        acc = correct / total * 100
        print(f"\nFinal Test Accuracy: {acc:.2f}% ({correct}/{total})")

if __name__ == "__main__":
    main()
