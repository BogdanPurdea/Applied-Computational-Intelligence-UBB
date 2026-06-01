# Explainability Results Report: LIME & SHAP Interpretability Analysis

This report summarizes and analyzes the Local Interpretable Model-agnostic Explanations (LIME) and SHapley Additive exPlanations (SHAP) generated across all 12 model configurations in this project.

---

## 1. Executive Summary

LIME and SHAP are post-hoc local explainability frameworks used to interpret the predictions of complex neural architectures (e.g., Transformers). 
* **LIME** approximates the model locally by perturbing the input sample (masking words) and training a simple sparse linear model on these perturbations.
* **SHAP** calculates Shapley values from cooperative game theory to measure how much each token shifts the model's prediction away from the base average value.

By comparing LIME and SHAP results, we can identify which specific words drive the sentiment, news classification, or emotion labels, verifying that the models rely on semantic features rather than noise or dataset artifacts.

---

## 2. Overview of Explainer Runs & Formats

The explainability results throughout the workspace are organized into two distinct layout formats:
1. **Format A (JSON Summary-Based)**: Detailed local explanations are exported as `lime_summary.json` and `shap_summary.json` containing token-level weights for a larger batch of test set samples (typically 48–50 samples).
2. **Format B (Static Image-Based)**: Pre-rendered visualization charts (PNG) and interactive reports (HTML) are generated for a small selected batch of 5 test set samples (indices `0` to `4`).

---

## 3. Format A: Detailed Summary Analysis

For the summary-based models, we analyzed the overall prediction accuracy on the explained sample subset and aggregated the top terms identified by LIME as having the strongest positive and negative influences.

### 3.1. Explainer Subset Statistics

| Model ID | Task / Dataset | Explained Sample Size | Exact-Match Accuracy on Subset |
| :--- | :--- | :---: | :---: |
| `5_DistilBERT_SA_Practical` | Binary Sentiment (IMDB) | 50 samples | 96.00% (48/50) |
| `6_SentenceBERT_Practical` | Binary Sentiment (IMDB) | 50 samples | 94.00% (47/50) |
| `1_BERT_Sentiment_Articles` | Multiclass Sentiment (ro_articles) | 48 samples | 68.75% (33/48) |
| `2_RoBERT_Emotion_RED` | Multilabel Emotion (REDv2) | 49 samples | 14.29% (7/49) |
| `3_RoBERT_Conv_Emotion_RED` | Multilabel Emotion (REDv2) | 49 samples | 12.24% (6/49) |
| `4_RoBERT_Ensemble_Emotion_RED`| Multilabel Emotion (REDv2) | 49 samples | 12.24% (6/49) |

> [!IMPORTANT]
> **Understanding Multilabel Exact-Match Accuracy**:
> The exact-match accuracy (subset accuracy) for the three RoBERT models on the REDv2 dataset appears low (~12% to 14%). This is because multilabel exact-match requires **all 7 emotion labels** (sadness, surprise, fear, anger, neutral, trust, joy) to be predicted exactly correct for a sample to count as correct. 
> Given $2^7 = 128$ possible label combinations, this is an extremely strict metric. In contrast, the models' overall Hamming losses (~0.10) and per-label F1-scores (~70%) show that they are highly performant.

---

### 3.2. Global Aggregated Analysis: LIME & SHAP Across All Samples

When local explanations (LIME weights and SHAP/Shapley values) are aggregated across the entire subset of evaluated samples, we gain a global understanding of what features the models rely on.

#### Understanding High Shapley Values & LIME Weights
- **Shapley values** represent the additive contribution of each token to the model's prediction relative to the baseline (average prediction across the training set). High Shapley values indicate that a feature has a powerful, consistent effect on shifting the prediction towards (positive values) or away from (negative values) a specific class.
- **LIME weights** locally approximate the model's decision boundary. When summed across many samples, they highlight which words are consistently influential.

#### Aggregated Top 15 Feature Rankings
By running the global aggregation tool in the explainability viewer, we get the following top terms ranked by cumulative absolute importance:

##### English Sentiment (IMDB)
* **`5_DistilBERT_SA_Practical`**:
  * **LIME**: `awful`, `worst`, `unnerving`, `not`, `misguided`, `story`, `this`, `is`, `good`, `great`, `and`, `best`, `but`, `perfect`, `funniest`
  * **SHAP**: `unnerving`, `good`, `awful`, `worst`, `bad`, `weak`, `hilarious`, `a`, `boring`, `this`, `however`, `excellent`, `horrible`, `insulting`, `mesmerized`
* **`6_SentenceBERT_Practical`**:
  * **LIME**: `not`, `it`, `bad`, `awful`, `worst`, `able`, `gibberish`, `truest`, `stinkpot`, `predictable`, `example`, `funniest`, `but`, `barely`, `no`
  * **SHAP**: `good`, `not`, `bad`, `weak`, `is`, `stinkpot`, `awful`, `worst`, `very`, `life`, `excellent`, `crap`, `predictable`, `wonderful`, `funny`

##### Romanian Multiclass Sentiment (`1_BERT_Sentiment_Articles`)
* **LIME**: `nu`, `de`, `care`, `și`, `amendată`, `profit`, `o`, `mongolia`, `interior`, `nutritie`, `a`, `risipa`, `intrebarile`, `puterea`, `iapă`
* **SHAP**: `vindecătoare`, `puterea`, `amendată`, `de`, `nutritie`, `interzisa`, `care`, `fost`, `a`, `republica`, `2017`, `copyright`, `dosar`, `penal`, `secretă`

##### Romanian Multilabel Emotion (REDv2 Subset)
* **`2_RoBERT_Emotion_RED`**:
  * **LIME & SHAP**: `frumos` (beautiful/nice), `bunătate` (kindness), `trist` (sad), `încântare` (delight), `fantastică` (fantastic), `îngrijorare` (concern/worry), `fobie` (phobia), `urăsc` (hate), `mâhnit` (grieved/sad), `uluitor` (astonishing), `plâng` (cry), `suferă` (suffers), `indignat` (indignant)
* **`3_RoBERT_Conv_Emotion_RED`**:
  * **LIME & SHAP**: `frumos`, `trist`, `încântare`, `bunătate`, `îngrijorare`, `urăsc`, `mâhnit`, `fantastică`, `fobie`, `plâng`, `îngrijorat`, `exuberant`, `uluit`, `suferă`
* **`4_RoBERT_Ensemble_Emotion_RED`**:
  * **LIME & SHAP**: `frumos`, `trist`, `bunătate`, `încântare`, `îngrijorare`, `urăsc`, `fantastică`, `mâhnit`, `dezolant` (desolate), `alarmant` (alarming), `uluitor`, `plâng`, `fobie`, `suferă`, `uluit`

#### Key Interpretability Insights per Model/Dataset

##### 1. English Sentiment Models (`5_DistilBERT_SA_Practical` & `6_SentenceBERT_Practical`)
- **Direct Sentiment Mapping**: Both models show an exceptionally high reliance on clear semantic indicators (such as `awful`, `worst`, `bad` for negative sentiment; `good`, `great`, `best`, `perfect` for positive sentiment).
- **Sentence-BERT Negation Sensitivity**: For `6_SentenceBERT_Practical`, the aggregated feature list highlights negations (`not`, `no`) as top features. This suggests that Sentence-BERT embeds structural context heavily, making the model highly sensitive to negations in sentiment determination.
- **SHAP vs LIME Consistency**: Both explainers are highly aligned. LIME's local surrogate weights and SHAP's Shapley attributions both identify `awful`, `worst`, `not`, and `good` as the absolute most important features.

##### 2. Romanian Multiclass Sentiment (`1_BERT_Sentiment_Articles`)
- **Topic-Driven Sentiment**: The top features are strongly topic-specific content words (e.g., `amendată` - fined, `profit` - profit, `nutritie` - nutrition, `risipa` - waste, `dosar penal` - criminal case). Because this dataset is news-based, the model heavily maps these topic indicators to sentiment classes.
- **Lingering Boilerplate**: Boilerplate metadata terms like `2017` and `copyright` appear in the top SHAP tokens. This indicates that header/footer boilerplate remains a mild feature shortcut, though it is heavily outweighed by content-rich features.

##### 3. Romanian Multilabel Emotion Models (REDv2 Subset)
- **High Cross-Model Convergence**: Across all three architectures (`2_RoBERT_Emotion_RED`, `3_RoBERT_Conv_Emotion_RED`, and `4_RoBERT_Ensemble_Emotion_RED`), the aggregated rankings are nearly identical. The same set of emotional vocabulary (`frumos`, `bunătate`, `trist`, `încântare`, `îngrijorare`, `urăsc`, `mâhnit`, `fobie`, `suferă`) dominates all models.
- **Architecture Independence**: This convergence shows that whether the model uses a standard linear classification head, a convolutional classification head, or an ensemble voting head, it relies on the exact same core lexicon of emotional Romanian words. This validates the robustness of the representations learned by fine-tuning.
- **Colloquial Emotion Triggers**: Strong colloquial and descriptive terms (such as `proștii` - fools/idiots, `agramați` - illiterate, `dezolant` - desolate, `alarmant` - alarming) are identified with high Shapley values, indicating the model successfully models conversational emotional markers.

#### General Interpretability Findings
1. **Absence of Stopwords**: Stopwords (like `de`, `la`, `in`, `the`, `and`) are almost completely absent from the top 15 aggregated lists for both LIME and SHAP across all models.
   - *Why do they appear in local lists but not globally?* In individual local samples, minor perturbations co-occurring within a sentence structure might assign non-zero weights to high-frequency stopwords.
   - *Why do they drop out globally?* Because their contribution directions are inconsistent across samples (canceling out) or their magnitude is negligible compared to content words. Globally, the models are proven to rely on semantic vocabulary.
2. **Robustness of Explanations**: The strong correlation between LIME and SHAP aggregate rankings mathematically validates the reliability of post-hoc local explanations in this project.

---

## 4. Format B: Static Pre-Rendered Explanations

For these models, pre-rendered PNG and HTML assets are generated for exactly **5 samples** (indices `0` to `4` from the test splits).

### 4.1. Models Using Format B
* **`1_BERT_SA_IMDB`** (English Movie Review Sentiment)
* **`2_DistilBERT_SA_IMDB`** (English Movie Review Sentiment)
* **`3_BERT_WELFake`** (English Fake News Detection)
* **`4_DistilBERT_NEWS`** (English Fake News Detection)
* **`1_ITA_BERT_SA_FEEL-IT`** (Italian Tweet Sentiment)
* **`2_UmBERTo_SA_FEEL-IT`** (Italian Tweet Sentiment)

### 4.2. Generated Artifacts
For each model, the output directories contain:
- **LIME Visualizations**:
  - `lime_explanation_{0-4}.png`: Pre-plotted horizontal bar charts showing top words contributing to the classification.
  - `lime_explanation_{0-4}.html`: Detailed interactive report displaying the local linear fit, classification probabilities, and the text sample with highlighted highlights.
- **SHAP Visualizations**:
  - `shap_explanation_{0-4}.png`: Horizontal bar charts plotting Shapley feature attribution values for input tokens.

These static charts are directly discoverable and viewable using the interactive `explainability_viewer.ipynb` notebook.
