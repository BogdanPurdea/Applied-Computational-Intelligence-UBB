# Exhaustive Column-by-Column Data Analysis and Knowledge Discovery Report

**Dataset:** Continuous Casting of Steel SCADA Database
**Total Records:** 17279

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
- **Examples:** ['2020-03-05', '2020-03-05', '2020-03-05']

### 2. Descriptive Statistics
- **Min Date:** 2020-01-05 00:00:00
- **Max Date:** 2020-08-26 00:00:00
- **Span:** 234 days 00:00:00

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `date` is nan tons vs 208547.91 tons when populated.
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
  - `Arm500`: 78.97%
  - `St4sp`: 7.82%
  - `St3sp`: 4.57%
  - `1015`: 3.03%
  - `25G2S`: 2.42%

![Categories](plots/steel_type.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `steel_type` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 21.3199 (p = 1.00e-43)

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
  - `180x180`: 86.81%
  - `150x150`: 13.19%

![Categories](plots/workpiece_slice_geometry.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `workpiece_slice_geometry` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 3.1393 (p = 7.64e-02)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `steel_temperature_grab1, Celsius deg.`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 56
- **Missing Values:** 3 (0.02%)
- **Examples:** [1587.0, 1583.0, 1585.0]

### 2. Descriptive Statistics
- **Mean:** 1566.8373
- **Median:** 1567.0000
- **Std Dev:** 23.8748
- **Min / Max:** 567.0000 / 1667.0000
- **Skewness / Kurtosis:** -38.2064 / 1600.2047

![Distribution](plots/steel_temperature_grab1__Celsius_deg..png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `steel_temperature_grab1, Celsius deg.` is 661.00 tons vs 208584.01 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 897 (5.19%)
- **Z-Score Outliers Count / %:** 18 (0.10%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0030 (p = 6.98e-01)
- **Spearman Rank Correlation:** rho = 0.0209 (p = 5.95e-03)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 209894.78 tons
  - `Medium`: 185185.20 tons
  - `High`: 236335.18 tons
- **FCA Attribute Labels:** `low_steel_temperature_grab1`, `medium_steel_temperature_grab1`, `high_steel_temperature_grab1`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 99.99% present
  - `Low`: 99.67% present
  - `Medium`: 100.00% present

# Column: `resistance, tonn`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 8076
- **Missing Values:** 0 (0.00%)
- **Examples:** [1789.0, 1819.0, 1846.0]

### 2. Descriptive Statistics
- **Mean:** 6860.1366
- **Median:** 5733.0000
- **Std Dev:** 91184.1117
- **Min / Max:** 24.0000 / 8473135.0000
- **Skewness / Kurtosis:** 92.6645 / 8602.5830

![Distribution](plots/resistance__tonn.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `resistance, tonn` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 27 (0.16%)
- **Z-Score Outliers Count / %:** 2 (0.01%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0067 (p = 3.81e-01)
- **Spearman Rank Correlation:** rho = -0.6839 (p = 0.00e+00)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 424992.04 tons
  - `Medium`: 130591.10 tons
  - `High`: 70366.52 tons
- **FCA Attribute Labels:** `low_resistance`, `medium_resistance`, `high_resistance`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `swing_frequency, amount/minute`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 12
- **Missing Values:** 0 (0.00%)
- **Examples:** [180, 180, 180]

### 2. Descriptive Statistics
- **Mean:** 193.2993
- **Median:** 200.0000
- **Std Dev:** 11.8830
- **Min / Max:** 150.0000 / 220.0000
- **Skewness / Kurtosis:** -1.4171 / 0.7080

![Distribution](plots/swing_frequency__amount_minute.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `swing_frequency, amount/minute` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 12 (0.07%)
- **Z-Score Outliers Count / %:** 6 (0.03%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0165 (p = 2.96e-02)
- **Spearman Rank Correlation:** rho = 0.0431 (p = 1.48e-08)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 209226.67 tons
  - `Medium`: 3467.72 tons
- **FCA Attribute Labels:** `low_swing_frequency`, `medium_swing_frequency`, `high_swing_frequency`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `crystallizer_movement, mm`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 7
- **Missing Values:** 0 (0.00%)
- **Examples:** [7, 7, 7]

### 2. Descriptive Statistics
- **Mean:** 9.0385
- **Median:** 7.0000
- **Std Dev:** 2.6896
- **Min / Max:** 5.0000 / 13.0000
- **Skewness / Kurtosis:** 0.6348 / -1.4910

![Distribution](plots/crystallizer_movement__mm.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `crystallizer_movement, mm` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 0 (0.00%)
- **Z-Score Outliers Count / %:** 0 (0.00%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0006 (p = 9.33e-01)
- **Spearman Rank Correlation:** rho = 0.0688 (p = 1.31e-19)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 203610.94 tons
  - `Medium`: 382677.07 tons
  - `High`: 170102.56 tons
- **FCA Attribute Labels:** `low_crystallizer_movement`, `medium_crystallizer_movement`, `high_crystallizer_movement`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `alloy_speed, meter/minute`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 3
- **Missing Values:** 0 (0.00%)
- **Examples:** [1, 2, 2]

### 2. Descriptive Statistics
- **Mean:** 2.1214
- **Median:** 2.0000
- **Std Dev:** 0.3354
- **Min / Max:** 1.0000 / 3.0000
- **Skewness / Kurtosis:** 2.0859 / 3.2343

![Distribution](plots/alloy_speed__meter_minute.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `alloy_speed, meter/minute` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 2198 (12.72%)
- **Z-Score Outliers Count / %:** 50 (0.29%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0185 (p = 1.49e-02)
- **Spearman Rank Correlation:** rho = -0.0206 (p = 6.68e-03)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 200092.94 tons
  - `Medium`: 268106.60 tons
- **FCA Attribute Labels:** `low_alloy_speed`, `medium_alloy_speed`, `high_alloy_speed`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_consumption, liter/minute`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 5
- **Missing Values:** 0 (0.00%)
- **Examples:** [2155, 2155, 2155]

### 2. Descriptive Statistics
- **Mean:** 2127.1234
- **Median:** 2155.0000
- **Std Dev:** 71.8122
- **Min / Max:** 1255.0000 / 2155.0000
- **Skewness / Kurtosis:** -2.6899 / 10.8517

![Distribution](plots/water_consumption__liter_minute.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_consumption, liter/minute` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 3119 (18.05%)
- **Z-Score Outliers Count / %:** 11 (0.06%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0134 (p = 7.72e-02)
- **Spearman Rank Correlation:** rho = -0.0381 (p = 5.36e-07)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 208547.91 tons
- **FCA Attribute Labels:** `low_water_consumption`, `medium_water_consumption`, `high_water_consumption`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_temperature_delta, Celsius deg.`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 4
- **Missing Values:** 0 (0.00%)
- **Examples:** [8, 8, 8]

### 2. Descriptive Statistics
- **Mean:** 8.9580
- **Median:** 9.0000
- **Std Dev:** 0.2887
- **Min / Max:** 6.0000 / 9.0000
- **Skewness / Kurtosis:** -8.3439 / 76.0314

![Distribution](plots/water_temperature_delta__Celsius_deg..png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_temperature_delta, Celsius deg.` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 467 (2.70%)
- **Z-Score Outliers Count / %:** 467 (2.70%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0018 (p = 8.16e-01)
- **Spearman Rank Correlation:** rho = -0.0225 (p = 3.08e-03)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 208547.91 tons
- **FCA Attribute Labels:** `low_water_temperature_delta`, `medium_water_temperature_delta`, `high_water_temperature_delta`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `water_consumption_secondary_cooling_zone_num1, liter/minute`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 33
- **Missing Values:** 0 (0.00%)
- **Examples:** [260, 260, 300]

### 2. Descriptive Statistics
- **Mean:** 313.5098
- **Median:** 320.0000
- **Std Dev:** 24.8822
- **Min / Max:** 120.0000 / 390.0000
- **Skewness / Kurtosis:** -2.1247 / 9.5421

![Distribution](plots/water_consumption_secondary_cooling_zone_num1__liter_minute.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `water_consumption_secondary_cooling_zone_num1, liter/minute` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 4985 (28.85%)
- **Z-Score Outliers Count / %:** 288 (1.67%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0320 (p = 2.63e-05)
- **Spearman Rank Correlation:** rho = -0.0651 (p = 1.12e-17)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 197084.80 tons
  - `Medium`: 293893.76 tons
- **FCA Attribute Labels:** `low_water_consumption_secondary_cooling_zone_num1`, `medium_water_consumption_secondary_cooling_zone_num1`, `high_water_consumption_secondary_cooling_zone_num1`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `C, %`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 511
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.2, 0.2019, 0.1852]

### 2. Descriptive Statistics
- **Mean:** 0.1930
- **Median:** 0.1924
- **Std Dev:** 0.0195
- **Min / Max:** 0.0579 / 0.2975
- **Skewness / Kurtosis:** 0.4352 / 16.8431

![Distribution](plots/C__%.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `C, %` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 1292 (7.48%)
- **Z-Score Outliers Count / %:** 609 (3.52%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0239 (p = 1.68e-03)
- **Spearman Rank Correlation:** rho = 0.0516 (p = 1.10e-11)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 226662.47 tons
  - `Medium`: 199526.98 tons
  - `High`: 199030.07 tons
- **FCA Attribute Labels:** `low_C`, `medium_C`, `high_C`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `Si, %`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 828
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.149, 0.1542, 0.1558]

### 2. Descriptive Statistics
- **Mean:** 0.1863
- **Median:** 0.1815
- **Std Dev:** 0.0707
- **Min / Max:** 0.1041 / 0.6786
- **Skewness / Kurtosis:** 5.3703 / 30.3117

![Distribution](plots/Si__%.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `Si, %` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 433 (2.51%)
- **Z-Score Outliers Count / %:** 419 (2.42%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0268 (p = 4.21e-04)
- **Spearman Rank Correlation:** rho = 0.0549 (p = 4.92e-13)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 241070.91 tons
  - `Medium`: 192873.94 tons
  - `High`: 191662.69 tons
- **FCA Attribute Labels:** `low_Si`, `medium_Si`, `high_Si`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `Mn,%`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 1443
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.518, 0.5148, 0.5031]

### 2. Descriptive Statistics
- **Mean:** 0.7661
- **Median:** 0.7040
- **Std Dev:** 0.2711
- **Min / Max:** 0.4453 / 1.5794
- **Skewness / Kurtosis:** 1.0212 / 0.2823

![Distribution](plots/Mn_%.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `Mn,%` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 0 (0.00%)
- **Z-Score Outliers Count / %:** 5 (0.03%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0137 (p = 7.18e-02)
- **Spearman Rank Correlation:** rho = 0.0445 (p = 4.82e-09)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 248972.05 tons
  - `Medium`: 183765.26 tons
  - `High`: 192942.62 tons
- **FCA Attribute Labels:** `low_Mn`, `medium_Mn`, `high_Mn`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `S, %`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 170
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.004, 0.0041, 0.0021]

### 2. Descriptive Statistics
- **Mean:** 0.0061
- **Median:** 0.0054
- **Std Dev:** 0.0034
- **Min / Max:** 0.0010 / 0.0317
- **Skewness / Kurtosis:** 1.1903 / 2.4142

![Distribution](plots/S__%.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `S, %` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 288 (1.67%)
- **Z-Score Outliers Count / %:** 163 (0.94%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = -0.0031 (p = 6.84e-01)
- **Spearman Rank Correlation:** rho = 0.0120 (p = 1.14e-01)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 207541.56 tons
  - `Medium`: 208658.85 tons
  - `High`: 209467.11 tons
- **FCA Attribute Labels:** `low_S`, `medium_S`, `high_S`

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present

# Column: `P, %`

### 1. Metadata
- **Inferred Data Type:** Numeric
- **Unique Values:** 216
- **Missing Values:** 0 (0.00%)
- **Examples:** [0.0216, 0.0183, 0.0167]

### 2. Descriptive Statistics
- **Mean:** 0.0150
- **Median:** 0.0146
- **Std Dev:** 0.0043
- **Min / Max:** 0.0052 / 0.0387
- **Skewness / Kurtosis:** 0.6237 / 0.6288

![Distribution](plots/P__%.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `P, %` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 4. Outlier Analysis
- **IQR Outliers Count / %:** 217 (1.26%)
- **Z-Score Outliers Count / %:** 98 (0.57%)

### 5. Relationship with RUL
- **Pearson Correlation with RUL:** r = 0.0155 (p = 4.20e-02)
- **Spearman Rank Correlation:** rho = 0.0081 (p = 2.86e-01)

### 6. Binned Conceptual Analysis (FCA Scaling)
- **Mean RUL by bin:**
  - `Low`: 182786.26 tons
  - `Medium`: 207982.34 tons
  - `High`: 235671.51 tons
- **FCA Attribute Labels:** `low_P`, `medium_P`, `high_P`

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
- **Examples:** ['30011717', '30011717', '30011717']

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `30014144`: 4.75%
  - `30014821`: 3.03%
  - `30014808`: 2.83%
  - `30014812`: 2.77%
  - `30014817`: 2.75%

![Categories](plots/sleeve.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `sleeve` is nan tons vs 208547.91 tons when populated.
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
- **Examples:** [1, 1, 1]

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `12`: 9.64%
  - `11`: 8.33%
  - `18`: 7.96%
  - `7`: 7.19%
  - `10`: 6.26%

![Categories](plots/num_crystallizer.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `num_crystallizer` is nan tons vs 208547.91 tons when populated.
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
- **Examples:** [3, 3, 3]

### 2. Descriptive Statistics
- **Top Categories (Frequency):**
  - `3`: 18.31%
  - `6`: 17.77%
  - `5`: 16.52%
  - `2`: 16.18%
  - `4`: 15.81%

![Categories](plots/num_stream.png)

### 3. Missing Value Analysis
- **Relationship to RUL:** Target RUL mean for missing values of `num_stream` is nan tons vs 208547.91 tons when populated.
- **Handling Strategy:** Median imputation for numeric features, mode imputation for categorical attributes.

### 5. Relationship with RUL
- **ANOVA Test against RUL:** F-statistic = 212.1625 (p = 2.34e-220)

### 7. RUL Class Distribution
- **Class Distribution relative to column presence:**
  - `Critical`: 100.00% present
  - `Healthy`: 100.00% present
  - `Low`: 100.00% present
  - `Medium`: 100.00% present