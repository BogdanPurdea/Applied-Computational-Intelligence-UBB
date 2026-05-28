import torch
import torch.nn as nn
import numpy as np
from sklearn.metrics import classification_report

from Model import FCN
from DatasetPreProcessing import test_loader
from ModelTraining import CKPT_PATH, DEVICE

def test_model():
    print(f"Loading best model from {CKPT_PATH}...")
    model = FCN().to(DEVICE)
    
    try:
        checkpoint = torch.load(CKPT_PATH, map_location=DEVICE, weights_only=False)
        model.load_state_dict(checkpoint['model_state'])
    except Exception as e:
        print(f"Failed to load checkpoint: {e}")
        return
        
    model.eval()
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    all_preds = []
    all_labels = []
    test_loss = 0.0

    print("Evaluating on Test Dataset...")
    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            logits = model(imgs)
            loss = criterion(logits, labels)

            test_loss += loss.item()
            preds = logits.argmax(dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    avg_test_loss = test_loss / len(test_loader)
    test_accuracy = (np.array(all_preds) == np.array(all_labels)).mean()

    print("\n" + "=" * 30)
    print(f"TEST RESULTS")
    print("=" * 30)
    print(f"Average Loss: {avg_test_loss:.4f}")
    print(f"Accuracy:     {test_accuracy * 100:.2f}%")
    print("=" * 30)

    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds, digits=4))

if __name__ == '__main__':
    test_model()