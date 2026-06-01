"""
explain_utils.py
================
Shared utilities for model explainability with LIME and SHAP.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def select_balanced_eval_subset(
    texts: list[str],
    labels: list[int],
    n: int,
    seed: int,
    num_classes: int = 2,
) -> tuple[list[str], list[int], list[int]]:
    """Select balanced examples from the test set across all classes.

    Returns:
        Tuple of (selected_texts, selected_labels, original_indices).
    """
    rng = np.random.default_rng(seed)
    samples_per_class = n // num_classes

    chosen_lists = []
    for c in range(num_classes):
        class_idx = np.where(np.array(labels) == c)[0]
        chosen_c = rng.choice(class_idx, size=samples_per_class, replace=False)
        chosen_lists.append(chosen_c)

    chosen = np.sort(np.concatenate(chosen_lists))
    sel_texts = [texts[i] for i in chosen]
    sel_labels = [labels[i] for i in chosen]
    return sel_texts, sel_labels, chosen.tolist()

def load_explainability_model(model_name: str, ckpt_dir: Path | str, device: torch.device):
    """Load the target model(s) and tokenizer for explainability.

    Supports custom convolutional layers, fold ensembles, or standard sequence classifiers.
    """
    ckpt_dir = Path(ckpt_dir)
    if model_name == "robert_conv":
        safe_path = ckpt_dir / "model.safetensors"
        bin_path = ckpt_dir / "pytorch_model.bin"
        assert safe_path.exists() or bin_path.exists(), (
            f"No weights found at {ckpt_dir}. Ensure robert_conv is trained."
        )
        
        tokenizer = AutoTokenizer.from_pretrained(str(ckpt_dir))
        # Add path for dataset_red and train_robert_conv
        project_root = Path(__file__).resolve().parents[2]
        import sys
        robert_conv_dir = str(project_root / "2_Romanian" / "3_RoBERT_Conv_Emotion_RED")
        ro_shared_dir = str(project_root / "2_Romanian" / "shared")
        if robert_conv_dir not in sys.path:
            sys.path.insert(0, robert_conv_dir)
        if ro_shared_dir not in sys.path:
            sys.path.insert(0, ro_shared_dir)
            
        from train_robert_conv import BertWithConvForSequenceClassification
        from dataset_red import EMOTION_LABELS
        id2label = {idx: e for idx, e in enumerate(EMOTION_LABELS)}
        label2id = {e: idx for idx, e in enumerate(EMOTION_LABELS)}
        
        model = BertWithConvForSequenceClassification(
            "readerbench/RoBERT-base",
            num_labels=len(EMOTION_LABELS),
            id2label=id2label,
            label2id=label2id,
        )
        if safe_path.exists():
            import safetensors.torch
            state_dict = safetensors.torch.load_file(str(safe_path), device="cpu")
        else:
            state_dict = torch.load(bin_path, map_location="cpu")
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
        
    elif model_name == "robert_ensemble":
        for fold_i in range(5):
            fold_config = ckpt_dir / f"fold_{fold_i}" / "config.json"
            assert fold_config.exists(), (
                f"Missing fold checkpoint at {fold_config.parent}. Ensure robert_ensemble is trained."
            )
            
        tokenizer = AutoTokenizer.from_pretrained(str(ckpt_dir / "fold_0"))
        
        model = []
        for fold_i in range(5):
            m = AutoModelForSequenceClassification.from_pretrained(str(ckpt_dir / f"fold_{fold_i}"))
            m.to(device)
            m.eval()
            model.append(m)
            
    else:
        assert (ckpt_dir / "config.json").exists(), (
            f"No checkpoint found at {ckpt_dir}. Ensure target model is trained first."
        )
        tokenizer = AutoTokenizer.from_pretrained(str(ckpt_dir))
        model = AutoModelForSequenceClassification.from_pretrained(str(ckpt_dir))
        model.to(device)
        model.eval()
        
    return model, tokenizer

def make_predict_fn(model, tokenizer, device, max_length, batch_size, dataset_type="imdb"):
    """Return a callable that maps a list of text strings to class probabilities.

    Supports custom convolutional layers, fold ensembles, or standard sequence classifiers.
    """
    def predict(texts: list[str]) -> np.ndarray:
        # Convert to list of python strings to support numpy string types passed by SHAP
        texts = [str(t) for t in texts]
        is_ensemble = isinstance(model, list)
        all_probs = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            enc = tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=max_length,
                return_tensors="pt",
            )
            enc = {k: v.to(device) for k, v in enc.items()}
            with torch.no_grad():
                if is_ensemble:
                    batch_probs = None
                    for m in model:
                        logits = m(**enc).logits
                        if dataset_type == "red":
                            probs = torch.sigmoid(logits).cpu().numpy()
                        else:
                            probs = torch.softmax(logits, dim=-1).cpu().numpy()
                        if batch_probs is None:
                            batch_probs = probs
                        else:
                            batch_probs += probs
                    batch_probs /= len(model)
                else:
                    logits = model(**enc).logits
                    if dataset_type == "red":
                        batch_probs = torch.sigmoid(logits).cpu().numpy()
                    else:
                        batch_probs = torch.softmax(logits, dim=-1).cpu().numpy()
            all_probs.append(batch_probs)
        return np.vstack(all_probs)

    return predict
