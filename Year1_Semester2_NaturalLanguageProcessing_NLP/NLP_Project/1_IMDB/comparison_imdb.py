import os
import sys
import argparse
import pandas as pd
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from shared.utils import load_json
from shared.visualization import plot_model_comparison

def parse_args():
    parser = argparse.ArgumentParser(description="Compare IMDB models")
    parser.add_argument("--bert_dir", type=str, default=os.path.join(parent_dir, "outputs", "BERT_IMDB"))
    parser.add_argument("--sbert_dir", type=str, default=os.path.join(parent_dir, "outputs", "SentenceBERT_IMDB"))
    parser.add_argument("--output_dir", type=str, default=os.path.join(parent_dir, "comparison_results"))
    return parser.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    
    bert_metrics_path = os.path.join(args.bert_dir, "metrics.json")
    sbert_metrics_path = os.path.join(args.sbert_dir, "metrics.json")
    
    if not os.path.exists(bert_metrics_path) or not os.path.exists(sbert_metrics_path):
        print("Error: Both models must be trained before running comparison.")
        return
        
    bert_metrics = load_json(bert_metrics_path)
    sbert_metrics = load_json(sbert_metrics_path)
    
    # Create comparison CSV
    df = pd.DataFrame([
        {"Model": "BERT", **bert_metrics},
        {"Model": "Sentence-BERT", **sbert_metrics}
    ])
    
    csv_path = os.path.join(args.output_dir, "imdb_model_comparison.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved comparison to {csv_path}")
    
    # Generate barplots
    metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1']
    if 'roc_auc' in df.columns:
        metrics_to_plot.append('roc_auc')
        
    plot_model_comparison(df, metrics_to_plot, args.output_dir, "imdb_metric_barplots.png")
    
    # Plot combined ROC Curve if probabilities exist
    bert_probs_file = os.path.join(args.bert_dir, "test_probs.npy")
    sbert_probs_file = os.path.join(args.sbert_dir, "test_probs.npy")
    labels_file = os.path.join(args.bert_dir, "test_labels.npy")
    
    if os.path.exists(bert_probs_file) and os.path.exists(sbert_probs_file) and os.path.exists(labels_file):
        from sklearn.metrics import roc_curve, auc
        import matplotlib.pyplot as plt
        
        y_true = np.load(labels_file)
        bert_probs = np.load(bert_probs_file)[:, 1] if np.load(bert_probs_file).shape[1] == 2 else np.load(bert_probs_file)
        sbert_probs = np.load(sbert_probs_file)[:, 1] if np.load(sbert_probs_file).shape[1] == 2 else np.load(sbert_probs_file)
        
        plt.figure(figsize=(8, 6))
        
        # BERT ROC
        fpr, tpr, _ = roc_curve(y_true, bert_probs)
        plt.plot(fpr, tpr, lw=2, label=f'BERT (area = {auc(fpr, tpr):.2f})')
        
        # SBERT ROC
        fpr, tpr, _ = roc_curve(y_true, sbert_probs)
        plt.plot(fpr, tpr, lw=2, label=f'Sentence-BERT (area = {auc(fpr, tpr):.2f})')
        
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('IMDB ROC Comparison')
        plt.legend(loc="lower right")
        plt.savefig(os.path.join(args.output_dir, "imdb_roc_curves.png"), bbox_inches='tight')
        plt.close()
        print("Saved combined ROC curve.")

if __name__ == "__main__":
    main()
