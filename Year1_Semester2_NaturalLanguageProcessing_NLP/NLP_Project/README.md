# NLP Experimentation Framework

An academic-grade, modular framework for performing Transformer-based NLP experiments, including model fine-tuning, automated evaluations, and cross-model performance comparisons.

## Architecture & Structure

```
nlp_transformer_classification/
├── 1_IMDB/
│   ├── mainBERTIMDB.py                 # Fine-tunes BERT for Sentiment Analysis
│   ├── mainSentenceBERTIMDB.py         # Trains Sentence-BERT + MLP for Sentiment Analysis
│   └── comparison_imdb.py              # Aggregates metrics & plots ROC comparison
├── 2_FAKENEWS/
│   ├── mainBERTFakeNews.py             # Fine-tunes BERT for Fake News Detection
│   ├── mainSentenceBERTFakeNews.py     # Trains Sentence-BERT + MLP for Fake News Detection
│   └── comparison_fakenews.py          # Aggregates metrics & plots ROC comparison
├── 3_ROMANIAN_EMOTION/
│   └── mainRoBERTaRED.py               # Fine-tunes Romanian RoBERTa for multi-class emotion
├── shared/                             # Reusable framework utilities
│   ├── utils.py                        # Logging, JSON saving, and deterministic seeding
│   ├── dataset_utils.py                # CSV loading and Scikit-learn stratified splitting
│   ├── visualization.py                # Confusion matrices, ROC curves, training histories
│   ├── metrics.py                      # Accuracy, F1, Recall, Precision, ROC-AUC
│   ├── model_utils.py                  # Sentence-BERT classifier wrapper and device detection
│   └── explainability.py               # Native LIME and SHAP integration
├── data/
├── outputs/                            # Model checkpoints, metrics, and interpretability reports
└── comparison_results/                 # Final CSV tables and comparative PNG charts
```

## Setup & Requirements

### Hardware Recommendations
- **GPU**: NVIDIA GPU with CUDA strongly recommended. Models use `torch.cuda` automatically.
- **Memory**: Minimum 8GB VRAM (12GB+ recommended for unfrozen Sentence-BERT and full BERT).

### Installation
Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Datasets

Ensure datasets are downloaded and placed in the `data/` directory or specify paths via CLI.
1. **IMDB Movie Reviews**: https://www.kaggle.com/datasets/rehanliaqat17/imbd-dataset
2. **WELFake Dataset**: https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification
3. **Romanian Emotion Dataset**: Your local `.csv` file.

## Execution

Scripts support modular CLI configuration. Use `--help` on any script for details.

### 1. IMDB Experimentation
Train models:
```bash
python 1_IMDB/mainBERTIMDB.py --epochs 3 --run_lime true
python 1_IMDB/mainSentenceBERTIMDB.py --epochs 5 --freeze_encoder
```
Compare models:
```bash
python 1_IMDB/comparison_imdb.py
```

### 2. Fake News Experimentation
Train models:
```bash
python 2_FAKENEWS/mainBERTFakeNews.py --epochs 3
python 2_FAKENEWS/mainSentenceBERTFakeNews.py --epochs 5
```
Compare models:
```bash
python 2_FAKENEWS/comparison_fakenews.py
```

### 3. Romanian Emotion Classification
Train multi-class RoBERTa:
```bash
python 3_ROMANIAN_EMOTION/mainRoBERTaRED.py --epochs 3
```

## Interpretability (Explainable AI)

To run **LIME** (Local Interpretable Model-agnostic Explanations) and **SHAP** (SHapley Additive exPlanations), add the following flags:
```bash
--run_lime true --run_shap true --num_explainer_samples 5
```
Because XAI over transformers is extremely computationally expensive, it is restricted to a small number of samples by default. HTML and PNG plots will be exported to `outputs/<model>/lime/` and `outputs/<model>/shap/`.

## Output Artifacts

Upon completion, each model generates:
- Full model checkpoint & tokenizer in `outputs/<model>/`
- `metrics.json` tracking training time, inference time, GPU peak memory, and accuracy metrics.
- `test_probs.npy` and `test_labels.npy` used for aggregation.
- Standalone ROC curves and Confusion Matrix PNGs.

The `comparison_*.py` scripts will aggregate these into `comparison_results/`, exporting `_model_comparison.csv` tables and unified ROC visualization plots suitable for academic presentation.
