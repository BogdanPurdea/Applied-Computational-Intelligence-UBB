# Technical Guide: Migrated Codebase for Classification & Interpretability

This guide provides a comprehensive overview of the modular and migrated codebase in the project. It describes how datasets are loaded, preprocessed, fine-tuned, and explained using **LIME** and **SHAP** post-hoc interpretability frameworks.

---

## 1. Directory Structure of Shared & Migrated Code

The reusable utilities are centralized under the `NLP_Project/shared/` directory, while task execution scripts are situated in language-specific directories:

```
NLP_Project/
├── shared/
│   └── migrated/
│       ├── dataset_utils.py         # Caching and stratified dataset split helpers
│       ├── preprocessing_base.py    # Core text cleaning regular expressions & functions
│       ├── train_utils.py           # Training metrics, PyTorch dataset wrap, hardware detection
│       ├── explain_utils.py         # Subsampling, custom model loading, and probability wrapper
│       ├── verify_training.py       # Integration sanity check for the training utility pipeline
│       └── verify_explain.py        # Integration sanity check for the explainer wrapper
├── explain/
│   ├── explain_config.py            # Global variables and hyperparameter config for explainers
│   ├── explain_lime.py              # LIME explanation generation batch script
│   └── explain_shap.py              # SHAP explanation generation batch script
```

---

## 2. Data Splitting & Caching (`dataset_utils.py`)

The dataset utility loader [dataset_utils.py](file:///Users/bogdanpurdea/Projects/Applied-Computational-Intelligence-UBB/Year1_Semester2_NaturalLanguageProcessing_NLP/NLP_Project/shared/migrated/dataset_utils.py) manages raw data loading, stratified subset splitting, and serialization caches.

### 2.1. Stratified Train-Val-Test Splitting
To ensure class distributions are preserved identically across all training stages, the pipeline employs `perform_stratified_split`. 
- **Methodology**:
  1. Carves out the test set from the input DataFrame using stratified sampling (preserves target label ratios).
  2. Divides the remaining subset into training and validation splits.
  3. Returns a tuple of three clean, index-reset DataFrames.

```python
def perform_stratified_split(
    df: pd.DataFrame,
    label_col: str,
    seed: int,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Carve out test set
    df_train_val, df_test = train_test_split(
        df, test_size=test_ratio, stratify=df[label_col], random_state=seed
    )
    # Split remainder into train / val
    val_share = val_ratio / (train_ratio + val_ratio)
    df_train, df_val = train_test_split(
        df_train_val, test_size=val_share, stratify=df_train_val[label_col], random_state=seed
    )
    return (
        df_train.reset_index(drop=True),
        df_val.reset_index(drop=True),
        df_test.reset_index(drop=True),
    )
```

### 2.2. Pickling Cache Helpers
Text preprocessing for large corpora (e.g., IMDB or WELFake) can be computationally expensive. The functions `save_pickle_cache` and `load_pickle_cache` serialize preprocessed lists of strings directly to the disk, accelerating subsequent runs.
- `save_pickle_cache(data, path)`: Recursively creates parent directories if needed and dumps the object.
- `load_pickle_cache(path)`: Safely loads the pickled object if it exists; otherwise, returns `None`.

---

## 3. Text Preprocessing Engine

Text preprocessing is divided into a language-agnostic core (`preprocessing_base.py`) and customized language-specific wrappers.

### 3.1. Core Base Cleaner (`preprocessing_base.py`)
Centralized regular expressions and helper functions in [preprocessing_base.py](file:///Users/bogdanpurdea/Projects/Applied-Computational-Intelligence-UBB/Year1_Semester2_NaturalLanguageProcessing_NLP/NLP_Project/shared/migrated/preprocessing_base.py) execute basic text normalization:
* **HTML Stripping**: `HTML_REGEX.sub(" ", text)` deletes tags like `<br />` or `<b>`.
* **URL/Mention Removal**: `URL_REGEX` and `MENTION_REGEX` remove HTTP/WWW links and Twitter-style user mentions (`@\w+`).
* **Emoji Conversion**: `emoji.demojize(text)` converts unicode emojis to string names (e.g., `😊` becomes `smiling face with smiling eyes`) so Transformer tokenizers can parse their semantic meaning.
* **Character Caps**: Caps runs of repeating characters to a maximum of 3 (e.g., `sooooo` becomes `sooo`) to reduce vocabulary noise.
* **Whitespace Compression**: Compresses tabs, newlines, and multi-spaces into a single space.

### 3.2. English Pipeline (`preprocessing_en.py`)
- **Contraction Expansion**: English contractions are expanded to explicit negations (e.g., `don't` $\rightarrow$ `do not`) via `contractions.fix()`. This prevents the model from splitting "not" contextually during tokenization.
- **ASCII Emoticons**: Text emoticons (e.g., `:)`, `<3`, `XD`) are translated to English words (e.g., `happy`, `love`, `laughing`) before emoji demojization.

### 3.3. Romanian Pipelines (`preprocessing_ro.py` / `preprocessing_red.py`)
- **Preservation of Diacritics**: Diacritics (`ș`, `ț`, `ă`, `â`, `î`) are strictly **preserved** rather than stripped, because the Romanian RoBERT model vocabulary supports them natively.
- **Romanian Emoticons**: Text emoticons are translated to Romanian sentiment words (e.g., `:)` $\rightarrow$ `fericit`).
- **Batch Deduplication**: `preprocessing_red.py` performs exact-match deduplication at the batch level and returns the list of retained indices so that multi-label matrices remain synchronized.

---

## 4. Fine-Tuning Infrastructure (`train_utils.py`)

The training utilities in [train_utils.py](file:///Users/bogdanpurdea/Projects/Applied-Computational-Intelligence-UBB/Year1_Semester2_NaturalLanguageProcessing_NLP/NLP_Project/shared/migrated/train_utils.py) provide hardware acceleration, PyTorch dataset compilation, and training evaluation metrics.

### 4.1. Hardware Device Auto-Discovery
The function `select_hardware_device` dynamically assigns execution:
1. **MPS (Metal Performance Shaders)**: Selected on Apple Silicon macOS devices (`torch.backends.mps.is_available()`).
2. **CUDA**: Selected on NVIDIA GPUs.
3. **CPU**: Fallback default.

### 4.2. PyTorch Dataset Wrapper
`TextClassificationDataset` wraps tokenized texts for standard Hugging Face sequence classification. It supports:
- **Single-Label**: Targets stored as `torch.long` indices (Cross-Entropy loss).
- **Multi-Label**: Targets stored as `torch.float` arrays representing multi-hot classes (BCEWithLogitsLoss).

### 4.3. Metrics Computation
* **`compute_classification_metrics`**: Computes macro-F1 and accuracy for multiclass classification, or binary precision, recall, F1, and accuracy for binary datasets.
* **`compute_multilabel_metrics`**: Computes micro-F1, macro-F1, and Hamming Loss. The logits are mapped via sigmoid, and active classes are thresholded at `0.5`:
  $$\text{probs} = \frac{1}{1 + e^{-\text{logits}}}$$

---

## 5. Explainability Framework (`explain_utils.py`)

The explainability utilities in [explain_utils.py](file:///Users/bogdanpurdea/Projects/Applied-Computational-Intelligence-UBB/Year1_Semester2_NaturalLanguageProcessing_NLP/NLP_Project/shared/migrated/explain_utils.py) align and load model configurations for comparison under LIME and SHAP.

### 5.1. Class-Balanced Sampling
To ensure direct, unbiased comparisons between the explainers, `select_balanced_eval_subset` extracts the exact same balanced evaluation subset from the test split across classes:
```python
def select_balanced_eval_subset(
    texts: list[str],
    labels: list[int],
    n: int,
    seed: int,
    num_classes: int = 2,
) -> tuple[list[str], list[int], list[int]]:
    rng = np.random.default_rng(seed)
    samples_per_class = n // num_classes
    chosen_lists = []
    for c in range(num_classes):
        class_idx = np.where(np.array(labels) == c)[0]
        chosen_c = rng.choice(class_idx, size=samples_per_class, replace=False)
        chosen_lists.append(chosen_c)
    chosen = np.sort(np.concatenate(chosen_lists))
    return [texts[i] for i in chosen], [labels[i] for i in chosen], chosen.tolist()
```

### 5.2. Explainability Model Loader
`load_explainability_model` manages three distinct model architectures:
1. **Custom Convolutional Classifier (`robert_conv`)**: Instantiates the custom model structure `BertWithConvForSequenceClassification` and loads state dict weights.
2. **K-Fold Ensembles (`robert_ensemble`)**: Loads a list of 5 fine-tuned BERT models representing individual fold checkpoints to compute ensemble predictions.
3. **Standard Models**: Loads sequence classifiers via `AutoModelForSequenceClassification.from_pretrained()`.

### 5.3. Model-Agnostic Probability Wrapper (`predict_fn`)
Both LIME and SHAP require a probability function that maps raw text strings to floating-point probabilities. `make_predict_fn` abstracts this for all models:
* Batches inputs to fit in GPU memory.
* Uses the appropriate tokenizer to convert texts to model input tensors.
* Activates `torch.no_grad()` to freeze gradients during attribution.
* **Loss Alignment**: Applies **sigmoid** activation for multilabel models (REDv2) or **softmax** activation for single-label classifiers:
  $$\text{Probability (Multilabel)} = \sigma(\text{logits}) \quad \Big| \quad \text{Probability (Single-label)} = \text{softmax}(\text{logits})$$
* Averages predictions across the list of models if evaluating an ensemble fold.

---

## 6. Explainer Run Scripts

Once configuration variables are set in `explain_config.py`, LIME and SHAP can be run via their respective scripts:

### 6.1. LIME Explainer (`explain_lime.py`)
1. Instantiates `LimeTextExplainer` using class names.
2. Loops through the balanced evaluation text examples.
3. Calls `explainer.explain_instance(...)` which perturbs words randomly, fits a local linear surrogate model on the outputs, and extracts the top coefficients.
4. Saves interactive visual HTML files (`example_{idx:03d}.html`) and compiles a metadata summary `lime_summary.json`.
5. Outputs the aggregated top features (sorted by average absolute weight) to `lime_top_words.json`.

### 6.2. SHAP Explainer (`explain_shap.py`)
1. Instantiates `shap.maskers.Text(tokenizer=r"\W+")` to define word-level feature boundaries.
2. Prepares a `shap.Explainer` wrapper pointing to `predict_fn` and the masker.
3. Evaluates the text sample to calculate Shapley values across token coalitions.
4. Saves raw attribution weights as NumPy arrays (`shap_values_{idx:03d}.npy`) for comparative plotting in the notebook viewer.
5. Saves aggregated token metadata to `shap_summary.json` and `shap_top_tokens.json`.

---

## 7. Pipeline Verification Scripts

To ensure no code regressions occur during migration, verification scripts are provided:
- **`verify_training.py`**: Runs a quick training sanity check using a tiny synthetic dataset.
- **`verify_explain.py`**: Tests the `predict_fn` wrapper and verifies that LIME and SHAP can produce valid attributions on the loaded models.
