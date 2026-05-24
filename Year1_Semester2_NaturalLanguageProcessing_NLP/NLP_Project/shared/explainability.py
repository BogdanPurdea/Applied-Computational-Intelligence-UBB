import os
import matplotlib.pyplot as plt
from lime.lime_text import LimeTextExplainer
import shap

def run_lime_explanations(predict_proba_fn, texts, class_names, num_samples, output_dir, file_prefix="lime"):
    os.makedirs(output_dir, exist_ok=True)
    explainer = LimeTextExplainer(class_names=class_names)
    for i, text in enumerate(texts[:num_samples]):
        try:
            exp = explainer.explain_instance(text, predict_proba_fn, num_features=10)
            exp.save_to_file(os.path.join(output_dir, f"{file_prefix}_{i}.html"))
        except Exception as e:
            print(f"Failed to generate LIME explanation for sample {i}: {e}")

def run_shap_explanations(predict_proba_fn, texts, num_samples, output_dir, file_prefix="shap"):
    os.makedirs(output_dir, exist_ok=True)
    try:
        explainer = shap.Explainer(predict_proba_fn, shap.maskers.Text(tokenizer=r"\W+"))
        shap_values = explainer(texts[:num_samples])
        
        plt.figure()
        shap.plots.bar(shap_values, show=False)
        plt.savefig(os.path.join(output_dir, f"{file_prefix}_bar.png"), bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Failed to generate SHAP explanations: {e}")
