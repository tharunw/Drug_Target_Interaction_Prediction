# Drug--Target Interaction Prediction

## Project Overview

This project develops an end-to-end machine-learning workflow for
predicting drug--target binding affinity using experimentally measured
ChEMBL activity data, molecular descriptors, Morgan molecular
fingerprints, and protein sequence-derived features.

The main scientific question is whether richer protein sequence
representations improve generalization to previously unseen protein
targets.

## Objectives

-   Acquire and clean experimentally measured drug--target activity
    data.
-   Generate RDKit molecular descriptors and Morgan fingerprints.
-   Extract protein sequence-derived features.
-   Add 400 dipeptide composition features.
-   Train Random Forest regression models for pChEMBL prediction.
-   Evaluate random, drug-grouped, and protein-grouped performance.
-   Compare baseline and enhanced representations.
-   Analyse feature importance and prediction errors.

## Dataset

The final integrated dataset contains:

-   **18,745 drug--protein observations**
-   **122 unique compounds with molecular descriptors**
-   **11 protein targets**
-   Experimentally measured **pChEMBL** values
-   No missing values in the final integrated feature matrix

The prediction target is `pchembl_value`.

## Feature Engineering

### Molecular descriptors

RDKit descriptors include molecular weight, LogP, TPSA, HBD, HBA,
rotatable bonds, ring count, and fraction sp3.

### Morgan fingerprints

Each compound is represented using **256 Morgan fingerprint features**.

### Protein features

The original protein representation contains **24 sequence-derived
features**, including sequence length, amino-acid composition,
hydrophobic fraction, charged fraction, and aromatic fraction.

The enhanced representation adds all **400 possible dipeptide
composition features**:

``` text
24 original protein features
+ 400 dipeptide features
= 424 protein features
```

### Final enhanced representation

``` text
256 Morgan features
+ 24 original protein features
+ 400 dipeptide features
= 680 ML features
```

Final matrix:

``` text
X = (18745, 680)
y = (18745,)
```

## Machine Learning

A **Random Forest Regressor** was used as the primary regression model.

Three evaluation strategies were used:

1.  **Random split** --- conventional 80:20 train/test evaluation.
2.  **Drug-grouped evaluation** --- prevents the same molecule from
    appearing in both training and test sets. Observed drug overlap was
    **0**.
3.  **Protein-grouped five-fold cross-validation** --- prevents the same
    protein target from appearing in both training and test folds and is
    the main evaluation for unseen-target generalization.

# Results

## Baseline model

### Random split

  Metric         Result
  -------- ------------
  MAE        **0.5375**
  RMSE       **0.7258**
  R²         **0.7049**

### Drug-grouped

  Metric         Result
  -------- ------------
  MAE        **0.5448**
  RMSE       **0.7300**
  R²         **0.7134**

### Protein-grouped

  Metric             Result
  ----------- -------------
  Mean MAE       **1.2168**
  Mean RMSE      **1.4770**
  Mean R²       **-0.2249**

## Enhanced model

### Random split

  Metric         Result
  -------- ------------
  MAE        **0.5429**
  RMSE       **0.7355**
  R²         **0.6970**

### Protein-grouped five-fold CV

  Metric             Result
  ----------- -------------
  Mean MAE       **1.2005**
  Mean RMSE      **1.4552**
  Mean R²       **-0.1763**
  R² Std         **0.2413**

### Fold-level enhanced results

    Fold      MAE     RMSE        R²
  ------ -------- -------- ---------
       1   1.1492   1.3917   -0.4213
       2   1.2561   1.5173    0.0238
       3   1.0541   1.2963   -0.0408
       4   1.1382   1.3873    0.0133
       5   1.4048   1.6834   -0.4565

## Baseline vs Enhanced

  Evaluation          Baseline R²   Enhanced R²
  ----------------- ------------- -------------
  Random split             0.7049        0.6970
  Drug-grouped             0.7134           ---
  Protein-grouped         -0.2249   **-0.1763**

Protein-grouped R² improvement:

``` text
-0.1763 - (-0.2249) = +0.0486
```

## Key Findings

-   Random-split performance was strong, with R² around **0.70**.
-   Performance dropped substantially when protein targets were held
    out.
-   Morgan fingerprints were the dominant feature group in the enhanced
    Random Forest analysis.
-   Adding 400 dipeptide features produced a **modest improvement** in
    unseen-protein R² from **-0.2249 to -0.1763**.
-   The enhanced model still has negative R² for unseen proteins, so
    generalization remains challenging.
-   Random-split R² decreased slightly from **0.7049 to 0.6970** after
    enhancement.

## Interpretation

The results indicate that molecular structure contains substantial
predictive information, while generalization to unseen protein targets
is much harder. Dipeptide composition adds useful local sequence
information, but sequence composition alone does not capture all
determinants of drug--protein binding.

Possible missing factors include protein structure, binding-site
characteristics, interaction geometry, assay variation, and limited
target diversity.

## Limitations

-   Only **11 protein targets** are represented, limiting unseen-target
    learning.
-   Sequence features do not directly encode three-dimensional
    structure.
-   Experimental measurements may vary across assays and conditions.
-   Random Forest does not explicitly model protein--ligand interaction
    geometry.
-   Negative protein-grouped R² indicates limited generalization to
    unseen targets.

## Future Improvements

-   Increase the number and diversity of protein targets.
-   Add protein structural and binding-site features.
-   Explore protein language-model embeddings.
-   Explore molecular graph neural networks.
-   Compare additional regression algorithms.
-   Perform hyperparameter optimization.
-   Perform external validation on independent datasets.
-   Improve experimental assay normalization.

## Visualizations

Saved figures include:

-   pChEMBL distribution
-   Feature correlations
-   Baseline actual vs predicted
-   Baseline residuals
-   Enhanced actual vs predicted
-   Enhanced residuals
-   Enhanced residuals vs predictions
-   Enhanced feature importance
-   Feature-group importance
-   Protein-grouped CV
-   Baseline vs enhanced comparison

They are stored in `results/figures/`.

## Project Structure

``` text
Drug_Target_Interaction_Prediction/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_data_cleaning_and_labeling.ipynb
│   ├── 03_molecular_and_protein_features.ipynb
│   ├── 04_exploratory_data_analysis.ipynb
│   └── 05_ML_With_All_Visualizations.ipynb
│
├── results/
│   ├── figures/
│   └── tables/
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── molecular_features.py
│   ├── protein_features.py
│   └── model_utils.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Important Outputs

Processed datasets are stored in `data/processed/`.

Final ML result tables are stored in `results/tables/`:

``` text
final_model_comparison.csv
enhanced_protein_cv_results.csv
baseline_protein_cv_results.csv
enhanced_feature_importance.csv
model_results_summary.csv
```

## Source Code

The `src/` directory contains reusable functions for data processing,
RDKit molecular descriptors, Morgan fingerprints, protein sequence
features, dipeptide features, Random Forest training, regression
evaluation, and feature importance.

## Technologies

-   Python
-   Pandas
-   NumPy
-   RDKit
-   Scikit-learn
-   Matplotlib
-   ChEMBL
-   Jupyter Notebook
-   VS Code
-   Git / GitHub

## Installation

``` bash
git clone <your-github-repository-url>
cd Drug_Target_Interaction_Prediction
pip install -r requirements.txt
```

## Running the Project

Run the notebooks in this order:

``` text
01_data_acquisition.ipynb
02_data_cleaning_and_labeling.ipynb
03_molecular_and_protein_features.ipynb
04_exploratory_data_analysis.ipynb
05_ML_With_All_Visualizations.ipynb
```

## Conclusion

This project demonstrates an end-to-end computational workflow for
drug--target binding-affinity prediction using chemical structure and
protein sequence information.

The baseline model performed well under conventional random splitting
but generalized poorly to unseen protein targets. Adding 400 dipeptide
features modestly improved protein-grouped R² from **-0.2249 to
-0.1763**, while random-split performance decreased slightly.

The results highlight an important challenge in computational drug
discovery: strong performance on randomly split datasets does not
necessarily imply reliable generalization to previously unseen
biological targets.
