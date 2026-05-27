# Transformer NLP Classification Project

This project implements three distinct transformer-based classification models using PyTorch and HuggingFace Transformers.

## Structure

```
NLP_Project/
│
├── 1_BERT_SA_IMDB/
│   ├── BERT_IMDB.py                   # BERT model training and evaluation script
│   ├── PreProcessingDataset.py        # Dataset preprocessing utility
│   ├── IMDB_Dataset.csv               # Raw IMDB dataset
│   ├── PreProcessed_IMDB_Dataset.csv  # Preprocessed IMDB dataset
│   ├── test_metrics.csv               # Exported final test metrics
│   └── Results/                       # Generated LIME and SHAP visual explanations
│
├── 2_DistilBERT_SA_IMDB/
│   ├── DistilBERT_IMDB.py             # DistilBERT model training and evaluation script
│   ├── test_metrics.csv               # Exported final test metrics
│   └── Results/                       # Generated LIME and SHAP visual explanations
│
├── 3_UmBERTo_SA_FEEL-IT/
│   ├── UmBERTo_FEEL-IT.py             # UmBERTo model training and evaluation script
│   └── feel_it_dataset.csv            # FEEL-IT dataset for sentiment classification
│
├── utils.py                           # Shared utilities for explainability, metrics, and data processing
└── README.md                          # Project documentation
```

## Setup & Requirements

### Hardware Requirements
- **GPU Required**: Training/evaluating transformer models on CPU is exceedingly slow. A CUDA-compatible GPU is required by the scripts (NVIDIA CUDA validation is enforced);
- Memory: Minimum 8GB VRAM is advised.

### Datasets
- **IMDB Dataset**: Placed inside the respective project directories (`1_BERT_SA_IMDB/IMDB_Dataset.csv`);
- **FEEL-IT Dataset**: Placed inside the `3_UmBERTo_SA_FEEL-IT/` directory. The FEEL-IT dataset is widely used for Italian sentiment and emotion classification [@bianchi2021feel].

## Running the Models

Run the scripts directly from the root directory or from their respective folders.

### 1. IMDB Sentiment (BERT)
```bash
python 1_BERT_SA_IMDB/BERT_IMDB.py
```

### 2. IMDB Sentiment (DistilBERT)
```bash
python 2_DistilBERT_SA_IMDB/DistilBERT_IMDB.py
```

### 3. Italian Sentiment Classification (UmBERTo)
```bash
python 3_UmBERTo_SA_FEEL-IT/UmBERTo_FEEL-IT.py
```

## LIME and SHAP Explainability

Interpretability methods (LIME and SHAP) are automatically run at the end of the training/evaluation scripts on a selection of samples.
- **LIME** outputs interactive HTML files and corresponding visualization plots (PNG format) highlighting word importance;
- **SHAP** outputs bar plot visualizations representing feature attributions.

All visual explanations are exported to the `Results/` directory inside each model's folder.

## Artifacts Generated

After running, check the respective `Results/` folder (e.g. `1_BERT_SA_IMDB/Results/` or `2_DistilBERT_SA_IMDB/Results/`) for:
- `lime_explanation_*.html`;
- `lime_explanation_*.png`;
- `shap_explanation_*.png`;
- `test_metrics.csv` (exported to the model's root directory);

## Known Limitations
- CUDA GPU execution is strictly enforced; running on CPU-only machines will throw a system error;
- LIME and SHAP explainer runs can be compute-intensive and may take some time depending on the GPU/CPU setup.

@inproceedings{bianchi2021feel,
  title     = {FEEL-IT: Emotion and Sentiment Classification for the Italian Language},
  author    = {Bianchi, Federico and Nozza, Debora and Hovy, Dirk},
  booktitle = {Proceedings of the 11th Workshop on Computational Approaches to Subjectivity, Sentiment and Social Media Analysis},
  year      = {2021},
  publisher = {Association for Computational Linguistics},
  url       = {https://github.com/MilaNLProc/feel-it}
}