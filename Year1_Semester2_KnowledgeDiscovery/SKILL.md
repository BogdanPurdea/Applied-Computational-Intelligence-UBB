---
name: fca-steel-project
description: Executes the Continuous Casting of Steel FCA/KD/Data Mining project step by step and outputs each numbered step as a separate Markdown file.
---

# FCA Steel Project Agent

## Objective

Execute the project using the files available in the current workspace.

Dataset: Continuous Casting of Steel.

Produce one Markdown file per project step:

- step_2_data_mining.md
- step_3_toscanaj_scales.md
- step_4_attribute_exploration.md
- step_5_triadic_analysis.md
- step_6_temporal_concept_analysis.md
- step_7_fca_application_report.md

## Mandatory Workflow

Before doing work:

1. Inspect the current folder.
2. Identify dataset files.
3. Identify schema, columns, missing values, data types, and target variables if any.
4. Create an execution plan in `project_plan.md`.
5. Do not delete files.
6. Do not overwrite source data.
7. Store generated outputs under `./output/`.

## Step 2: Data Mining and First Layer of Knowledge

Perform as many relevant analyses as possible:

- Data profiling
- Missing value analysis
- Correlation analysis
- PCA
- Clustering:
  - K-Means
  - Hierarchical clustering
  - DBSCAN if applicable
- Classification or supervised modeling if labels exist:
  - LDA
  - Decision Tree
  - Random Forest
  - Logistic Regression if applicable
- FCA-style binarization / conceptual scaling
- Association rules if applicable
- Outlier analysis

Output:

`output/step_2_data_mining.md`

Include:

- Methods used
- Why each method was selected
- Parameters
- Results
- Tables
- Interpretation
- Extracted knowledge

## Step 3: ToscanaJ System

Build a many-valued context from the dataset or Step 2 results.

Design creative conceptual scales, for example:

- Temperature stability scale
- Casting speed scale
- Defect risk scale
- Process regime scale
- Chemical composition scale
- Operational quality scale
- Cluster membership scale
- PCA profile scale

Output:

`output/step_3_toscanaj_scales.md`

Include:

- Many-valued context description
- Scales built
- Rationale for each scale
- ToscanaJ compatibility notes
- Knowledge extracted from scale combinations
- Mention Java legacy requirement for ToscanaJ

## Step 4: Attribute Exploration

Choose a meaningful attribute set related to steel casting, quality control, manufacturing, or computer science.

Perform simulated expert attribute exploration if no human expert is available.

Output:

`output/step_4_attribute_exploration.md`

Include:

- Attribute set
- Implications
- Accepted/rejected implications
- Counterexamples
- Final knowledge base
- Lessons learned

## Step 5: Triadic Knowledge Discovery

Create or derive a triadic context:

Objects × Attributes × Conditions

Example:

- Objects: casting batches / samples
- Attributes: process or quality properties
- Conditions: time periods, clusters, regimes, or quality classes

Output:

`output/step_5_triadic_analysis.md`

Include:

- Triadic context definition
- Triadic concepts or patterns
- Interpretation
- Knowledge discovered

## Step 6: Temporal Concept Analysis

Create a temporal interpretation of the dataset if timestamps exist.

If no timestamp exists, derive temporal stages from row order, batch sequence, or process phases.

Output:

`output/step_6_temporal_concept_analysis.md`

Include:

- Temporal objects
- Conceptual states
- Life tracks
- State transitions
- Stability/change observations
- Interpretation

## Step 7: FCA Application Report

Write a report about one real-life FCA application related to:

- Industrial quality control
- Manufacturing analytics
- Process optimization
- Defect diagnosis
- Knowledge discovery

Output:

`output/step_7_fca_application_report.md`

Include:

- Application domain
- Data/context
- FCA method
- Benefits
- Limitations
- Relevance to Continuous Casting of Steel

## Execution Rules

Allowed commands:

- mkdir
- ls / dir
- pwd / cd
- cat / type
- head / tail
- cp / copy
- mv / move inside workspace only
- python
- python3
- pip only with approval
- git status
- git diff

Restricted commands:

- rm
- rmdir
- del
- erase
- git reset --hard
- git clean
- sudo
- runas
- chmod
- chown
- format
- diskpart
- shutdown
- reboot

Do not delete anything.

Do not modify source dataset files.

Ask before installing packages.

Prefer Python scripts under `./scripts/`.

Generate reproducible analysis code.

Every Markdown file must be detailed enough for academic submission.