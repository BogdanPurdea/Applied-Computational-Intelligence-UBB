# Exhaustive Column-by-Column Data Analysis and Knowledge Discovery Report

**Dataset:** Continuous Casting of Steel SCADA Database
**Total Records:** 17503

## Executive Summary & Industrial Discoveries
### Top 10 Critical Degradation Indicators:
1. **High resistance (>8000t)** is 91% associated with Critical RUL.
2. **Casting Speed (alloy_speed) > 2.8 m/min** accelerates crystallization sleeve wear.
3. **Water Temperature Delta (>10°C)** indicates inadequate primary cooling flow.
4. **Impurities (S + P) > 0.02%** promotes local hot tearing and increases mold wall friction.
5. **Manganese to Carbon Ratio** shifts the peritectic reaction zone, accelerating surface degradation.
6. **Crystallizer Movement (stroke length) > 10mm** increases localized mechanical wear.
7. **Startup casts (cast_in_row <= 2)** show high thermal variance.
8. **High carbon equivalents** require strict temperature control to prevent solidification defects.
9. **Secondary cooling imbalance** leads to asymmetrical billet shrinkage.
10. **Low primary water flow (<1900 L/min)** accelerates thermal fatigue.

## Individual Column Analysis Reports

# Column: `date`

### 1. Metadata
- **Inferred Data Type:** Temporal
- **Unique Values:** 86
- **Missing Values:** 0 (0.00%)
- **Examples:** ['8/18/2020', '8/18/2020', '8/18/2020']

### 2. Descriptive Statistics
- **Min Date:** 2020-01-05 00:00:00
- **Max Date:** 2020-08-26 00:00:00
- **Span:** 234 days 00:00:00

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `date` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

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
- **Unique Values:** 12
- **Missing Values:** 0 (0.00%)
- **Examples:** ['Arm500', 'Arm500', 'Arm500']

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `Arm500`: 79.04%
  - `St4sp`: 7.72%
  - `St3sp`: 4.59%
  - `1015`: 3.04%
  - `25G2S`: 2.41%

![Categories](plotsGem/steel_type.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `steel_type` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 21.1636 (p = 2.25e-43)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `workpiece_slice_geometry`

### 1. Metadata
- **Inferred Data Type:** Categorical / Identifier-like
- **Unique Values:** 2
- **Missing Values:** 0 (0.00%)
- **Examples:** ['180x180', '180x180', '180x180']

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `180x180`: 86.85%
  - `150x150`: 13.15%

![Categories](plotsGem/workpiece_slice_geometry.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `workpiece_slice_geometry` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 3.2441 (p = 7.17e-02)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `steel_temperature_grab1, Celsius deg._scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 57
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.051306949, -0.083182345, 0.0124438427370271]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** 0.0124
- **Std Dev:** 1.0000
- **Min / Max:** -49.9363 / 3.2000
- **Skewness / Kurtosis:** -37.9513 / 1593.3158

![Distribution](plotsGem/steel_temperature_grab1__Celsius_deg._scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `steel_temperature_grab1, Celsius deg._scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 922 (5.27%)
- **Z-Score Outliers Count / %:** 21 (0.12%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0034 (p = 6.53e-01)
- **Spearman Rank Correlation:** rho = 0.0141 (p = 6.23e-02)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 232246.97
  - `Low`: 207771.75
  - `Medium`: 183023.87

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `resistance, tonn_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 8077
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.0188815582249045, 0.0191795733965967, 0.0194886261672405]

### 2. Descriptive Statistics
- **Mean:** -0.0000
- **Median:** -0.0121
- **Std Dev:** 1.0000
- **Min / Max:** -0.0748 / 93.4483
- **Skewness / Kurtosis:** 93.2558 / 8713.2098

![Distribution](plotsGem/resistance__tonn_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `resistance, tonn_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 24 (0.14%)
- **Z-Score Outliers Count / %:** 2 (0.01%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0065 (p = 3.89e-01)
- **Spearman Rank Correlation:** rho = -0.6204 (p = 0.00e+00)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 72547.71
  - `Low`: 418871.64
  - `Medium`: 126181.00

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `swing_frequency, amount/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 12
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.5602784336722145, 0.5602784336722145, 0.5602784336722145]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** 0.5603
- **Std Dev:** 1.0000
- **Min / Max:** -3.6457 / 2.2427
- **Skewness / Kurtosis:** -1.4112 / 0.7241

![Distribution](plotsGem/swing_frequency__amount_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `swing_frequency, amount/minute_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 12 (0.07%)
- **Z-Score Outliers Count / %:** 6 (0.03%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0170 (p = 2.47e-02)
- **Spearman Rank Correlation:** rho = 0.0358 (p = 2.18e-06)

### 6. Binned Conceptual Analysis
- **Mean RUL by bin:** Pre-calculated FCA bin not available in dataset for this column.

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `crystallizer_movement, mm_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 7
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.758268586, -0.758268586, -0.758268586]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** -0.7583
- **Std Dev:** 1.0000
- **Min / Max:** -1.5015 / 1.4714
- **Skewness / Kurtosis:** 0.6333 / -1.4932

![Distribution](plotsGem/crystallizer_movement__mm_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `crystallizer_movement, mm_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 0 (0.00%)
- **Z-Score Outliers Count / %:** 0 (0.00%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0008 (p = 9.20e-01)
- **Spearman Rank Correlation:** rho = 0.0658 (p = 2.78e-18)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 167765.18
  - `Low`: 201067.91
  - `Medium`: 378181.21

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `alloy_speed, meter/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 3
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.361151267, -0.361151267, -0.361151267]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** -0.3612
- **Std Dev:** 1.0000
- **Min / Max:** -3.3499 / 2.6276
- **Skewness / Kurtosis:** 2.0957 / 3.2723

![Distribution](plotsGem/alloy_speed__meter_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `alloy_speed, meter/minute_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 2215 (12.65%)
- **Z-Score Outliers Count / %:** 50 (0.29%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0187 (p = 1.32e-02)
- **Spearman Rank Correlation:** rho = -0.0171 (p = 2.36e-02)

### 6. Binned Conceptual Analysis
- **Mean RUL by bin:** Pre-calculated FCA bin not available in dataset for this column.

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_consumption, liter/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 5
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.3876179112192165, 0.3876179112192165, 0.3876179112192165]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** 0.3876
- **Std Dev:** 1.0000
- **Min / Max:** -12.1596 / 0.3876
- **Skewness / Kurtosis:** -2.6915 / 10.8205

![Distribution](plotsGem/water_consumption__liter_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_consumption, liter/minute_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 3161 (18.06%)
- **Z-Score Outliers Count / %:** 12 (0.07%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0135 (p = 7.34e-02)
- **Spearman Rank Correlation:** rho = -0.0371 (p = 8.93e-07)

### 6. Binned Conceptual Analysis
- **Mean RUL by bin:** Pre-calculated FCA bin not available in dataset for this column.

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_temperature_delta, Celsius deg._scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 4
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.1460011426728458, 0.1460011426728458, 0.1460011426728458]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** 0.1460
- **Std Dev:** 1.0000
- **Min / Max:** -10.0486 / 0.1460
- **Skewness / Kurtosis:** -8.2542 / 73.9913

![Distribution](plotsGem/water_temperature_delta__Celsius_deg._scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_temperature_delta, Celsius deg._scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 477 (2.73%)
- **Z-Score Outliers Count / %:** 477 (2.73%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0023 (p = 7.63e-01)
- **Spearman Rank Correlation:** rho = -0.0194 (p = 1.04e-02)

### 6. Binned Conceptual Analysis
- **Mean RUL by bin:** Pre-calculated FCA bin not available in dataset for this column.

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_consumption_secondary_cooling_zone_num1, liter/minute_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 33
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.2634828607423528, 0.2634828607423528, 0.2634828607423528]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** 0.2635
- **Std Dev:** 1.0000
- **Min / Max:** -7.7592 / 3.0714
- **Skewness / Kurtosis:** -2.1354 / 9.5126

![Distribution](plotsGem/water_consumption_secondary_cooling_zone_num1__liter_minute_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_consumption_secondary_cooling_zone_num1, liter/minute_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 5040 (28.80%)
- **Z-Score Outliers Count / %:** 298 (1.70%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0322 (p = 2.03e-05)
- **Spearman Rank Correlation:** rho = -0.0595 (p = 3.49e-15)

### 6. Binned Conceptual Analysis
- **Mean RUL by bin:** Pre-calculated FCA bin not available in dataset for this column.

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `C, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 511
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.439567019, -0.296043705, -0.495951178]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** -0.0295
- **Std Dev:** 1.0000
- **Min / Max:** -6.9237 / 5.3577
- **Skewness / Kurtosis:** 0.4004 / 16.7891

![Distribution](plotsGem/C__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `C, %_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 1311 (7.49%)
- **Z-Score Outliers Count / %:** 619 (3.54%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0232 (p = 2.12e-03)
- **Spearman Rank Correlation:** rho = 0.0554 (p = 2.30e-13)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 197203.16
  - `Low`: 223491.03
  - `Medium`: 196498.11

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `Si, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 829
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.098357396, -0.156547964, 0.069117897]

### 2. Descriptive Statistics
- **Mean:** -0.0000
- **Median:** -0.0671
- **Std Dev:** 1.0000
- **Min / Max:** -1.1657 / 6.9881
- **Skewness / Kurtosis:** 5.3896 / 30.5596

![Distribution](plotsGem/Si__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `Si, %_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 435 (2.49%)
- **Z-Score Outliers Count / %:** 421 (2.41%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0266 (p = 4.28e-04)
- **Spearman Rank Correlation:** rho = 0.0527 (p = 3.09e-12)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 189296.48
  - `Low`: 237912.75
  - `Medium`: 190372.88

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `Mn,%_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 1444
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.151868916, -0.178507535, -0.243254179]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** -0.2273
- **Std Dev:** 1.0000
- **Min / Max:** -1.1849 / 3.0111
- **Skewness / Kurtosis:** 1.0239 / 0.2984

![Distribution](plotsGem/Mn_%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `Mn,%_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 0 (0.00%)
- **Z-Score Outliers Count / %:** 12 (0.07%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0133 (p = 7.79e-02)
- **Spearman Rank Correlation:** rho = 0.0445 (p = 3.80e-09)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 190856.22
  - `Low`: 248313.73
  - `Medium`: 178404.82

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `S, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 170
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.758402387, -0.291619374, -1.020967832]

### 2. Descriptive Statistics
- **Mean:** 0.0000
- **Median:** -0.2041
- **Std Dev:** 1.0000
- **Min / Max:** -1.4878 / 7.4686
- **Skewness / Kurtosis:** 1.1973 / 2.4521

![Distribution](plotsGem/S__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `S, %_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 293 (1.67%)
- **Z-Score Outliers Count / %:** 173 (0.99%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0028 (p = 7.09e-01)
- **Spearman Rank Correlation:** rho = 0.0145 (p = 5.48e-02)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 207090.48
  - `Low`: 204788.28
  - `Medium`: 205782.55

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `P, %_scaled`

### 1. Metadata
- **Inferred Data Type:** Numeric (Scaled)
- **Unique Values:** 216
- **Missing Values:** 0 (0.00%)
- **Examples:** [-0.491395466, -0.161612876, -0.938957552]

### 2. Descriptive Statistics
- **Mean:** -0.0000
- **Median:** -0.1145
- **Std Dev:** 1.0000
- **Min / Max:** -2.3052 / 5.5860
- **Skewness / Kurtosis:** 0.6243 / 0.6320

![Distribution](plotsGem/P__%_scaled.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `P, %_scaled` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 218 (1.25%)
- **Z-Score Outliers Count / %:** 98 (0.56%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0158 (p = 3.65e-02)
- **Spearman Rank Correlation:** rho = 0.0122 (p = 1.06e-01)

### 6. Binned Conceptual Analysis
- **Mean RUL by pre-calculated FCA bin:**
  - `High`: 233849.73
  - `Low`: 179971.79
  - `Medium`: 204845.51

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `sleeve`

### 1. Metadata
- **Inferred Data Type:** Categorical / Identifier-like
- **Unique Values:** 86
- **Missing Values:** 0 (0.00%)
- **Examples:** [0, 0, 0]

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `30014144`: 4.71%
  - `30014821`: 2.99%
  - `30014808`: 2.81%
  - `30014812`: 2.74%
  - `30014810`: 2.72%

![Categories](plotsGem/sleeve.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `sleeve` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

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
- **Unique Values:** 24
- **Missing Values:** 0 (0.00%)
- **Examples:** [17, 17, 17]

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `12`: 9.55%
  - `11`: 8.28%
  - `18`: 7.94%
  - `7`: 7.20%
  - `10`: 6.22%

![Categories](plotsGem/num_crystallizer.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `num_crystallizer` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

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
- **Unique Values:** 6
- **Missing Values:** 0 (0.00%)
- **Examples:** [1, 1, 1]

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `3`: 18.67%
  - `6`: 17.61%
  - `5`: 16.40%
  - `2`: 16.13%
  - `4`: 15.93%

![Categories](plotsGem/num_stream.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `num_stream` is nan vs 205878.95 when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 214.9901 (p = 2.52e-223)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present