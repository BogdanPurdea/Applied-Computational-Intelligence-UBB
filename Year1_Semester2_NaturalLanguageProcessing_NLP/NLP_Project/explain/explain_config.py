from pathlib import Path

# All model configurations mapped to their decentralized directories
MODEL_INFO = {
    "bert_romanian": {
        "checkpoint_dir": "checkpoints/bert_romanian",
        "pipeline_dir": "2_Romanian/1_BERT_Sentiment_Articles",
        "dataset_type": "ro_articles",
        "class_names": ["negative", "positive", "neutral"],
        "num_classes": 3,
    },
    "robert_red": {
        "checkpoint_dir": "checkpoints/robert_red",
        "pipeline_dir": "2_Romanian/2_RoBERT_Emotion_RED",
        "dataset_type": "red",
        "class_names": ["sadness", "surprise", "fear", "anger", "neutral", "trust", "joy"],
        "num_classes": 7,
    },
    "robert_conv": {
        "checkpoint_dir": "checkpoints/robert_conv",
        "pipeline_dir": "2_Romanian/3_RoBERT_Conv_Emotion_RED",
        "dataset_type": "red",
        "class_names": ["sadness", "surprise", "fear", "anger", "neutral", "trust", "joy"],
        "num_classes": 7,
    },
    "robert_ensemble": {
        "checkpoint_dir": "checkpoints/robert_ensemble",
        "pipeline_dir": "2_Romanian/4_RoBERT_Ensemble_Emotion_RED",
        "dataset_type": "red",
        "class_names": ["sadness", "surprise", "fear", "anger", "neutral", "trust", "joy"],
        "num_classes": 7,
    },
    "distilbert": {
        "checkpoint_dir": "checkpoints/distilbert",
        "pipeline_dir": "1_English/4_DistilBERT_SA_Practical",
        "dataset_type": "imdb",
        "class_names": ["negative", "positive"],
        "num_classes": 2,
    },
    "sentencebert": {
        "checkpoint_dir": "checkpoints/sentencebert",
        "pipeline_dir": "1_English/5_SentenceBERT_Practical",
        "dataset_type": "imdb",
        "class_names": ["negative", "positive"],
        "num_classes": 2,
    },
}

# The default target model to explain (can be overridden or customized dynamically)
TARGET_MODEL = "robert_red"

info = MODEL_INFO[TARGET_MODEL]
project_root = Path(__file__).resolve().parents[1]

# Shared settings across both LIME and SHAP interpretability scripts
SHARED_CONFIG = {
    "checkpoint_dir": project_root / info["checkpoint_dir"],
    "model_name": TARGET_MODEL,
    "dataset_type": info["dataset_type"],
    "num_examples": 49 if info["num_classes"] == 7 else 50,  # balance class counts
    "random_seed": 42,
    "class_names": info["class_names"],
    "max_length": 256,
}

# LIME-specific parameters
LIME_CONFIG = {
    **SHARED_CONFIG,
    "results_dir": project_root / info["pipeline_dir"] / "Results" / "lime_explanations",
    "num_samples": 500,          # perturbation samples per example
    "num_features": 10,          # top N features (words) to extract
    "batch_size": 32,            # batch size for LIME model calls
}

# SHAP-specific parameters
SHAP_CONFIG = {
    **SHARED_CONFIG,
    "results_dir": project_root / info["pipeline_dir"] / "Results" / "shap_explanations",
    "max_evals": 500,            # max model calls per example for SHAP
    "batch_size": 16,            # batch size inside SHAP's model wrapper
}
