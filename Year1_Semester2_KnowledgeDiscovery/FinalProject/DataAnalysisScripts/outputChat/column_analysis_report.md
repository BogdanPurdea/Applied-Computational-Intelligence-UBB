# Exhaustive Column-by-Column Data Analysis and Knowledge Discovery Report

**Dataset:** Continuous Casting of Steel SCADA Database
**Total Records:** 17503
**Numeric Feature Policy:** All numeric modeling and numeric analytics use `*_scaled` columns only.
**Scaled Feature Count:** 53

## Executive Summary and Industrial Discoveries
The pipeline has been refactored to operate on standardized numeric feature properties. This ensures that regression, classification, feature importance, clustering, PCA, and association-rule mining are executed against the scaled feature space instead of raw industrial measurements.

### Top 10 Critical Degradation Indicators
The following indicators should be interpreted through their corresponding `*_scaled` variables and validated against model-derived feature importance and association-rule outputs.
1. **High scaled resistance** indicates abnormal crystallizer mechanical load.
2. **High scaled alloy speed** may accelerate sleeve wear through increased throughput stress.
3. **High scaled water temperature delta** may indicate inefficient thermal extraction.
4. **High scaled impurity index** may increase defect-prone operating conditions.
5. **High scaled crystallizer movement** may increase localized mechanical wear.
6. **Abnormal scaled temperature difference** may expose unstable heat-transfer behavior.
7. **High scaled total cooling consumption** may indicate compensatory cooling regimes.
8. **Low or abnormal scaled primary cooling flow** may accelerate thermal fatigue.
9. **Scaled chemistry indicators such as C, S, P, and Mn** should be monitored for composition-driven degradation.
10. **Latent PCA and KMeans regimes** should be reviewed as operating-state clusters.

## Regression Model Comparison
| Model             |      MAE |     RMSE |           R2 |             MAPE |
|:------------------|---------:|---------:|-------------:|-----------------:|
| SVR               |  13348.4 |  53208.4 |   -0.0460856 |      3.98889e+06 |
| MLP Regressor     |  15932.7 |  54385.6 |   -0.0928862 | 329675           |
| ElasticNet        | 236311   | 258702   |  -23.729     |      1.92946e+08 |
| Ridge             | 240988   | 294575   |  -31.0625    |      2.25458e+08 |
| Lasso             | 241004   | 294609   |  -31.07      |      2.25497e+08 |
| Linear Regression | 241006   | 294614   |  -31.071     |      2.25499e+08 |
| Extra Trees       |  88805.8 | 405697   |  -59.8151    |      7.44372e+06 |
| Gradient Boosting | 122868   | 470525   |  -80.8038    |      6.91126e+07 |
| LightGBM          | 135269   | 509860   |  -95.0528    |      1.41071e+08 |
| KNN Regressor     | 133733   | 575119   | -121.214     |      4.68404e+07 |
| Random Forest     | 117799   | 636404   | -148.649     |      2.87587e+07 |
| XGBoost           | 164078   | 771894   | -219.152     |      6.51855e+07 |
| Decision Tree     | 140718   | 846928   | -264.033     |      1.10153e+06 |

## Classification Model Comparison
| Model                        |   Accuracy |   Precision |   Recall |   F1-score |
|:-----------------------------|-----------:|------------:|---------:|-----------:|
| XGBoost Classifier           |   0.913879 |    0.613905 | 0.490233 |   0.53786  |
| LightGBM Classifier          |   0.916875 |    0.63674  | 0.462334 |   0.521615 |
| Gradient Boosting Classifier |   0.917374 |    0.617049 | 0.447574 |   0.5021   |
| Decision Tree Classifier     |   0.882177 |    0.449661 | 0.434867 |   0.43964  |
| Random Forest Classifier     |   0.916126 |    0.515274 | 0.300716 |   0.325052 |
| KNN Classifier               |   0.895407 |    0.340631 | 0.294615 |   0.305316 |
| Logistic Regression          |   0.910634 |    0.333896 | 0.271471 |   0.275642 |
| Extra Trees Classifier       |   0.914129 |    0.37863  | 0.257595 |   0.253482 |
| SVM Classifier               |   0.914378 |    0.728584 | 0.254244 |   0.247226 |
| MLP Classifier               |   0.912631 |    0.2285   | 0.249659 |   0.238611 |
| Naive Bayes                  |   0.194458 |    0.270423 | 0.291906 |   0.123026 |

## Top 25 Scaled Feature Importances
| Feature                                                           | Original_Feature                                                   |   Importance |
|:------------------------------------------------------------------|:-------------------------------------------------------------------|-------------:|
| resistance_tonn_scaled                                            | resistance, tonn_scaled                                            |   0.434614   |
| month_scaled                                                      | month_scaled                                                       |   0.15949    |
| V_scaled                                                          | V, %_scaled                                                        |   0.134292   |
| day_scaled                                                        | day_scaled                                                         |   0.0559101  |
| grab2_num_scaled                                                  | grab2_num_scaled                                                   |   0.0224959  |
| weekday_scaled                                                    | weekday_scaled                                                     |   0.0218882  |
| cast_in_row_scaled                                                | cast_in_row_scaled                                                 |   0.0175661  |
| N_scaled                                                          | N, %_scaled                                                        |   0.0152399  |
| Mn_scaled                                                         | Mn,%_scaled                                                        |   0.0123141  |
| hour_scaled                                                       | hour_scaled                                                        |   0.0115754  |
| S_scaled                                                          | S, %_scaled                                                        |   0.00970822 |
| Ce_scaled                                                         | Ce, %_scaled                                                       |   0.00894165 |
| Si_scaled                                                         | Si, %_scaled                                                       |   0.00799571 |
| water_consumption_secondary_cooling_zone_num3_liter_minute_scaled | water_consumption_secondary_cooling_zone_num3, liter/minute_scaled |   0.00762803 |
| Cu_scaled                                                         | Cu, %_scaled                                                       |   0.00642449 |
| Cr_scaled                                                         | Cr, %_scaled                                                       |   0.0056436  |
| C_scaled                                                          | C, %_scaled                                                        |   0.00499319 |
| Pb_scaled                                                         | Pb, %_scaled                                                       |   0.00478036 |
| steel_temperature_grab1_Celsius_deg._scaled                       | steel_temperature_grab1, Celsius deg._scaled                       |   0.00393238 |
| Ca_scaled                                                         | Ca, %_scaled                                                       |   0.0039294  |
| water_consumption_secondary_cooling_zone_num2_liter_minute_scaled | water_consumption_secondary_cooling_zone_num2, liter/minute_scaled |   0.00375683 |
| Ni_scaled                                                         | Ni, %_scaled                                                       |   0.00369445 |
| P_scaled                                                          | P, %_scaled                                                        |   0.00355152 |
| Zn_scaled                                                         | Zn, %_scaled                                                       |   0.00347657 |
| As_scaled                                                         | As, %_scaled                                                       |   0.00347193 |

## Individual Column Analysis Reports

# Column: `date`

### 1. Metadata
- **Inferred Data Type:** Temporal
- **Base Feature:** `date`
- **Unique Values:** 86
- **Missing Values:** 0 (0.00%)
- **Examples:** ['8/18/2020', '8/18/2020', '8/18/2020']

### 2. Descriptive Statistics
- **Min Date:** 2020-01-05 00:00:00
- **Max Date:** 2020-08-26 00:00:00
- **Span:** 234 days 00:00:00

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `date` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Mode imputation applied to categorical or temporal attribute where applicable.

### 5. Relationship with RUL

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `steel_type`

### 1. Metadata
- **Inferred Data Type:** Categorical / Identifier-like
- **Base Feature:** `steel_type`
- **Unique Values:** 12
- **Missing Values:** 0 (0.00%)
- **Examples:** ['Arm500', 'Arm500', 'Arm500']

### 2. Descriptive Statistics
- **Top Categories Frequency:**
  - `Arm500`: 79.04%
  - `St4sp`: 7.72%
  - `St3sp`: 4.59%
  - `1015`: 3.04%
  - `25G2S`: 2.41%

![Categories](../plots/steel_type.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `steel_type` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Mode imputation applied to categorical or temporal attribute where applicable.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 21.163611 (p = 2.25e-43)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `workpiece_slice_geometry`

### 1. Metadata
- **Inferred Data Type:** Categorical / Identifier-like
- **Base Feature:** `workpiece_slice_geometry`
- **Unique Values:** 2
- **Missing Values:** 0 (0.00%)
- **Examples:** ['180x180', '180x180', '180x180']

### 2. Descriptive Statistics
- **Top Categories Frequency:**
  - `180x180`: 86.85%
  - `150x150`: 13.15%

![Categories](../plots/workpiece_slice_geometry.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `workpiece_slice_geometry` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Mode imputation applied to categorical or temporal attribute where applicable.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 3.244118 (p = 7.17e-02)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `steel_temperature_grab1, Celsius deg._scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `steel_temperature_grab1, Celsius deg.`
- **Unique Values:** 57
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.051306949, -0.083182345, 0.0124438427370271]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** 0.012444
- **Std Dev:** 1.000029
- **Min / Max:** -49.936301 / 3.199983
- **Skewness / Kurtosis:** -37.951303 / 1593.315830

![Distribution](../plots/steel_temperature_grab1__Celsius_deg._scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `steel_temperature_grab1, Celsius deg._scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 922 (5.27%)
- **Z-Score Outliers Count / %:** 21 (0.12%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.003395 (p = 6.53e-01)
- **Spearman Rank Correlation:** rho = 0.014093 (p = 6.23e-02)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `steel_temperature_grab1, Celsius deg._fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 232246.97 tons
  - `Low`: 207771.75 tons
  - `Medium`: 183023.87 tons
- **FCA Attribute Labels:** `low_steel_temperature_grab1, Celsius deg.`, `medium_steel_temperature_grab1, Celsius deg.`, `high_steel_temperature_grab1, Celsius deg.`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `resistance, tonn_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `resistance, tonn`
- **Unique Values:** 8077
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.0188815582249045, 0.0191795733965967, 0.0194886261672405]

### 2. Descriptive Statistics
- **Mean:** -0.000000
- **Median:** -0.012101
- **Std Dev:** 1.000029
- **Min / Max:** -0.074750 / 93.448316
- **Skewness / Kurtosis:** 93.255842 / 8713.209799

![Distribution](../plots/resistance__tonn_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `resistance, tonn_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 24 (0.14%)
- **Z-Score Outliers Count / %:** 2 (0.01%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.006512 (p = 3.89e-01)
- **Spearman Rank Correlation:** rho = -0.620422 (p = 0.00e+00)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `resistance, tonn_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 72547.71 tons
  - `Low`: 418871.64 tons
  - `Medium`: 126181.00 tons
- **FCA Attribute Labels:** `low_resistance, tonn`, `medium_resistance, tonn`, `high_resistance, tonn`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `swing_frequency, amount/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `swing_frequency, amount/minute`
- **Unique Values:** 12
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.5602784336722145, 0.5602784336722145, 0.5602784336722145]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** 0.560278
- **Std Dev:** 1.000029
- **Min / Max:** -3.645655 / 2.242652
- **Skewness / Kurtosis:** -1.411198 / 0.724114

![Distribution](../plots/swing_frequency__amount_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `swing_frequency, amount/minute_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 12 (0.07%)
- **Z-Score Outliers Count / %:** 6 (0.03%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.016974 (p = 2.47e-02)
- **Spearman Rank Correlation:** rho = 0.035787 (p = 2.18e-06)

### 6. Binned Conceptual Analysis FCA Scaling
- **Mean RUL by quantile bin:**
  - `Low`: 206694.30 tons
  - `Medium`: 2823.71 tons
- **FCA Attribute Labels:** `low_swing_frequency, amount/minute`, `medium_swing_frequency, amount/minute`, `high_swing_frequency, amount/minute`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `crystallizer_movement, mm_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `crystallizer_movement, mm`
- **Unique Values:** 7
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.758268586, -0.758268586, -0.758268586]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** -0.758269
- **Std Dev:** 1.000029
- **Min / Max:** -1.501505 / 1.471441
- **Skewness / Kurtosis:** 0.633290 / -1.493156

![Distribution](../plots/crystallizer_movement__mm_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `crystallizer_movement, mm_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 0 (0.00%)
- **Z-Score Outliers Count / %:** 0 (0.00%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.000755 (p = 9.20e-01)
- **Spearman Rank Correlation:** rho = 0.065845 (p = 2.78e-18)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `crystallizer_movement, mm_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 167765.18 tons
  - `Low`: 201067.91 tons
  - `Medium`: 378181.21 tons
- **FCA Attribute Labels:** `low_crystallizer_movement, mm`, `medium_crystallizer_movement, mm`, `high_crystallizer_movement, mm`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `alloy_speed, meter/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `alloy_speed, meter/minute`
- **Unique Values:** 3
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.361151267, -0.361151267, -0.361151267]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** -0.361151
- **Std Dev:** 1.000029
- **Min / Max:** -3.349913 / 2.627610
- **Skewness / Kurtosis:** 2.095675 / 3.272310

![Distribution](../plots/alloy_speed__meter_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `alloy_speed, meter/minute_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 2215 (12.65%)
- **Z-Score Outliers Count / %:** 50 (0.29%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.018732 (p = 1.32e-02)
- **Spearman Rank Correlation:** rho = -0.017109 (p = 2.36e-02)

### 6. Binned Conceptual Analysis FCA Scaling
- **Mean RUL by quantile bin:**
  - `Low`: 197392.51 tons
  - `Medium`: 266001.38 tons
- **FCA Attribute Labels:** `low_alloy_speed, meter/minute`, `medium_alloy_speed, meter/minute`, `high_alloy_speed, meter/minute`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_consumption, liter/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `water_consumption, liter/minute`
- **Unique Values:** 5
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.3876179112192165, 0.3876179112192165, 0.3876179112192165]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** 0.387618
- **Std Dev:** 1.000029
- **Min / Max:** -12.159575 / 0.387618
- **Skewness / Kurtosis:** -2.691469 / 10.820462

![Distribution](../plots/water_consumption__liter_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_consumption, liter/minute_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 3161 (18.06%)
- **Z-Score Outliers Count / %:** 12 (0.07%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.013534 (p = 7.34e-02)
- **Spearman Rank Correlation:** rho = -0.037131 (p = 8.93e-07)

### 6. Binned Conceptual Analysis FCA Scaling
- **Mean RUL by quantile bin:**
  - `Low`: 205878.95 tons
- **FCA Attribute Labels:** `low_water_consumption, liter/minute`, `medium_water_consumption, liter/minute`, `high_water_consumption, liter/minute`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_temperature_delta, Celsius deg._scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `water_temperature_delta, Celsius deg.`
- **Unique Values:** 4
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.1460011426728458, 0.1460011426728458, 0.1460011426728458]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** 0.146001
- **Std Dev:** 1.000029
- **Min / Max:** -10.048645 / 0.146001
- **Skewness / Kurtosis:** -8.254160 / 73.991269

![Distribution](../plots/water_temperature_delta__Celsius_deg._scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_temperature_delta, Celsius deg._scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 477 (2.73%)
- **Z-Score Outliers Count / %:** 477 (2.73%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.002276 (p = 7.63e-01)
- **Spearman Rank Correlation:** rho = -0.019370 (p = 1.04e-02)

### 6. Binned Conceptual Analysis FCA Scaling
- **Mean RUL by quantile bin:**
  - `Low`: 205878.95 tons
- **FCA Attribute Labels:** `low_water_temperature_delta, Celsius deg.`, `medium_water_temperature_delta, Celsius deg.`, `high_water_temperature_delta, Celsius deg.`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_consumption_secondary_cooling_zone_num1, liter/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `water_consumption_secondary_cooling_zone_num1, liter/minute`
- **Unique Values:** 33
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.2634828607423528, 0.2634828607423528, 0.2634828607423528]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** 0.263483
- **Std Dev:** 1.000029
- **Min / Max:** -7.759238 / 3.071435
- **Skewness / Kurtosis:** -2.135360 / 9.512585

![Distribution](../plots/water_consumption_secondary_cooling_zone_num1__liter_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_consumption_secondary_cooling_zone_num1, liter/minute_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 5040 (28.80%)
- **Z-Score Outliers Count / %:** 298 (1.70%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.032207 (p = 2.03e-05)
- **Spearman Rank Correlation:** rho = -0.059452 (p = 3.49e-15)

### 6. Binned Conceptual Analysis FCA Scaling
- **Mean RUL by quantile bin:**
  - `Low`: 194341.84 tons
  - `Medium`: 292606.63 tons
- **FCA Attribute Labels:** `low_water_consumption_secondary_cooling_zone_num1, liter/minute`, `medium_water_consumption_secondary_cooling_zone_num1, liter/minute`, `high_water_consumption_secondary_cooling_zone_num1, liter/minute`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `C, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `C, %`
- **Unique Values:** 511
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.439567019, -0.296043705, -0.495951178]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** -0.029500
- **Std Dev:** 1.000029
- **Min / Max:** -6.923745 / 5.357750
- **Skewness / Kurtosis:** 0.400391 / 16.789128

![Distribution](../plots/C__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `C, %_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 1311 (7.49%)
- **Z-Score Outliers Count / %:** 619 (3.54%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.023227 (p = 2.12e-03)
- **Spearman Rank Correlation:** rho = 0.055368 (p = 2.30e-13)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `C, %_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 197203.16 tons
  - `Low`: 223491.03 tons
  - `Medium`: 196498.11 tons
- **FCA Attribute Labels:** `low_C, %`, `medium_C, %`, `high_C, %`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `Si, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `Si, %`
- **Unique Values:** 829
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.098357396, -0.156547964, 0.069117897]

### 2. Descriptive Statistics
- **Mean:** -0.000000
- **Median:** -0.067133
- **Std Dev:** 1.000029
- **Min / Max:** -1.165658 / 6.988118
- **Skewness / Kurtosis:** 5.389603 / 30.559607

![Distribution](../plots/Si__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `Si, %_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 435 (2.49%)
- **Z-Score Outliers Count / %:** 421 (2.41%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.026621 (p = 4.28e-04)
- **Spearman Rank Correlation:** rho = 0.052677 (p = 3.09e-12)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `Si, %_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 189296.48 tons
  - `Low`: 237912.75 tons
  - `Medium`: 190372.88 tons
- **FCA Attribute Labels:** `low_Si, %`, `medium_Si, %`, `high_Si, %`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `Mn,%_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `Mn,%`
- **Unique Values:** 1444
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.151868916, -0.178507535, -0.243254179]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** -0.227345
- **Std Dev:** 1.000029
- **Min / Max:** -1.184855 / 3.011097
- **Skewness / Kurtosis:** 1.023908 / 0.298357

![Distribution](../plots/Mn_%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `Mn,%_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 0 (0.00%)
- **Z-Score Outliers Count / %:** 12 (0.07%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.013326 (p = 7.79e-02)
- **Spearman Rank Correlation:** rho = 0.044522 (p = 3.80e-09)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `Mn,%_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 190856.22 tons
  - `Low`: 248313.73 tons
  - `Medium`: 178404.82 tons
- **FCA Attribute Labels:** `low_Mn,%`, `medium_Mn,%`, `high_Mn,%`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `S, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `S, %`
- **Unique Values:** 170
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.758402387, -0.291619374, -1.020967832]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** -0.204098
- **Std Dev:** 1.000029
- **Min / Max:** -1.487751 / 7.468648
- **Skewness / Kurtosis:** 1.197281 / 2.452094

![Distribution](../plots/S__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `S, %_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 293 (1.67%)
- **Z-Score Outliers Count / %:** 173 (0.99%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.002825 (p = 7.09e-01)
- **Spearman Rank Correlation:** rho = 0.014516 (p = 5.48e-02)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `S, %_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 207090.48 tons
  - `Low`: 204788.28 tons
  - `Medium`: 205782.55 tons
- **FCA Attribute Labels:** `low_S, %`, `medium_S, %`, `high_S, %`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `P, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `P, %`
- **Unique Values:** 216
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.491395466, -0.161612876, -0.938957552]

### 2. Descriptive Statistics
- **Mean:** -0.000000
- **Median:** -0.114501
- **Std Dev:** 1.000029
- **Min / Max:** -2.305200 / 5.586027
- **Skewness / Kurtosis:** 0.624288 / 0.632008

![Distribution](../plots/P__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `P, %_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 218 (1.25%)
- **Z-Score Outliers Count / %:** 98 (0.56%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.015811 (p = 3.65e-02)
- **Spearman Rank Correlation:** rho = 0.012221 (p = 1.06e-01)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `P, %_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 233849.73 tons
  - `Low`: 179971.79 tons
  - `Medium`: 204845.51 tons
- **FCA Attribute Labels:** `low_P, %`, `medium_P, %`, `high_P, %`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `temperature_difference_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `temperature_difference`
- **Unique Values:** 24
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.1807509732527328, 1.465756775382133, -0.675919562]

### 2. Descriptive Statistics
- **Mean:** -0.000000
- **Median:** 0.180751
- **Std Dev:** 1.000029
- **Min / Max:** -4.959272 / 6.605780
- **Skewness / Kurtosis:** -0.051898 / 2.250674

![Distribution](../plots/temperature_difference_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `temperature_difference_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 352 (2.01%)
- **Z-Score Outliers Count / %:** 178 (1.02%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.013707 (p = 6.98e-02)
- **Spearman Rank Correlation:** rho = 0.028669 (p = 1.49e-04)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `temperature_difference_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 243012.26 tons
  - `Low`: 190564.42 tons
  - `Medium`: 181178.97 tons
- **FCA Attribute Labels:** `low_temperature_difference`, `medium_temperature_difference`, `high_temperature_difference`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `total_cooling_consumption_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `total_cooling_consumption`
- **Unique Values:** 74
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.3441576310841344, 0.3441576310841344, 0.3441576310841344]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** 0.344158
- **Std Dev:** 1.000029
- **Min / Max:** -13.453103 / 1.429335
- **Skewness / Kurtosis:** -4.741436 / 33.081517

![Distribution](../plots/total_cooling_consumption_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `total_cooling_consumption_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 1906 (10.89%)
- **Z-Score Outliers Count / %:** 313 (1.79%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.011488 (p = 1.29e-01)
- **Spearman Rank Correlation:** rho = -0.065185 (p = 6.01e-18)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `total_cooling_consumption_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 198952.42 tons
  - `Low`: 199902.49 tons
  - `Medium`: 211459.09 tons
- **FCA Attribute Labels:** `low_total_cooling_consumption`, `medium_total_cooling_consumption`, `high_total_cooling_consumption`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `average_cooling_consumption_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `average_cooling_consumption`
- **Unique Values:** 74
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.3441576310841344, 0.3441576310841344, 0.3441576310841344]

### 2. Descriptive Statistics
- **Mean:** 0.000000
- **Median:** 0.344158
- **Std Dev:** 1.000029
- **Min / Max:** -13.453103 / 1.429335
- **Skewness / Kurtosis:** -4.741436 / 33.081517

![Distribution](../plots/average_cooling_consumption_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `average_cooling_consumption_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 1906 (10.89%)
- **Z-Score Outliers Count / %:** 313 (1.79%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.011488 (p = 1.29e-01)
- **Spearman Rank Correlation:** rho = -0.065185 (p = 6.01e-18)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `average_cooling_consumption_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 198952.42 tons
  - `Low`: 199902.49 tons
  - `Medium`: 211459.09 tons
- **FCA Attribute Labels:** `low_average_cooling_consumption`, `medium_average_cooling_consumption`, `high_average_cooling_consumption`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `impurity_index_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric Scaled
- **Base Feature:** `impurity_index`
- **Unique Values:** 473
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.526863342, -0.030721991, -1.053073865]

### 2. Descriptive Statistics
- **Mean:** -0.000000
- **Median:** -0.045757
- **Std Dev:** 1.000029
- **Min / Max:** -2.496394 / 4.870553
- **Skewness / Kurtosis:** 0.480494 / 0.308277

![Distribution](../plots/impurity_index_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `impurity_index_scaled` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Median imputation applied to scaled numeric feature.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 151 (0.86%)
- **Z-Score Outliers Count / %:** 75 (0.43%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.004929 (p = 5.14e-01)
- **Spearman Rank Correlation:** rho = 0.019902 (p = 8.46e-03)

### 6. Binned Conceptual Analysis FCA Scaling
- **Existing FCA Bin Column Used:** `impurity_index_fca_bin`
- **Mean RUL by existing FCA bin:**
  - `High`: 196856.74 tons
  - `Low`: 213561.75 tons
  - `Medium`: 207178.41 tons
- **FCA Attribute Labels:** `low_impurity_index`, `medium_impurity_index`, `high_impurity_index`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `sleeve`

### 1. Metadata
- **Inferred Data Type:** Categorical / Identifier-like
- **Base Feature:** `sleeve`
- **Unique Values:** 86
- **Missing Values:** 0 (0.00%)
- **Examples:** [0, 0, 0]

### 2. Descriptive Statistics
- **Top Categories Frequency:**
  - `30014144`: 4.71%
  - `30014821`: 2.99%
  - `30014808`: 2.81%
  - `30014812`: 2.74%
  - `30014810`: 2.72%

![Categories](../plots/sleeve.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `sleeve` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Mode imputation applied to categorical or temporal attribute where applicable.

### 5. Relationship with RUL

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `num_crystallizer`

### 1. Metadata
- **Inferred Data Type:** Categorical / Identifier-like
- **Base Feature:** `num_crystallizer`
- **Unique Values:** 24
- **Missing Values:** 0 (0.00%)
- **Examples:** [17, 17, 17]

### 2. Descriptive Statistics
- **Top Categories Frequency:**
  - `12`: 9.55%
  - `11`: 8.28%
  - `18`: 7.94%
  - `7`: 7.20%
  - `10`: 6.22%

![Categories](../plots/num_crystallizer.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `num_crystallizer` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Mode imputation applied to categorical or temporal attribute where applicable.

### 5. Relationship with RUL

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `num_stream`

### 1. Metadata
- **Inferred Data Type:** Categorical / Identifier-like
- **Base Feature:** `num_stream`
- **Unique Values:** 6
- **Missing Values:** 0 (0.00%)
- **Examples:** [1, 1, 1]

### 2. Descriptive Statistics
- **Top Categories Frequency:**
  - `3`: 18.67%
  - `6`: 17.61%
  - `5`: 16.40%
  - `2`: 16.13%
  - `4`: 15.93%

![Categories](../plots/num_stream.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `num_stream` is nan tons vs 205878.95 tons when populated.
- **Handling Strategy:** Mode imputation applied to categorical or temporal attribute where applicable.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 214.990073 (p = 2.52e-223)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present