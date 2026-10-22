# Access Barrier and Civil Fillings Analysis

This repository contains data, code, notebooks, and documentation used to examine transportation barriers, access-to-justice challenges, and civil court participation using American Community Survey (ACS), RUCA, and Washington civil court filing data.

## Repository Structure

```text
access-barriers-analysis/
├── data_raw/              # Original source datasets
├── data_processed/        # Processed and merged datasets
├── notebooks/             # Jupyter notebooks
├── scripts/               # Data preparation scripts
├── metadata/              # Data dictionaries and documentation
├── docs/                  # Project documentation
└── README.md
```

## Datasets

### Primary Dataset

The primary dataset contains indicators related to:

- Transportation barriers
- Digital access
- Educational attainment
- Disability status
- Language barriers
- Household vulnerability
- Residential mobility
- Population and rurality characteristics

### Secondary Dataset

The secondary dataset contains county-level court activity measures, including:

- Civil filings
- Self-represented litigant cases
- Interpreter usage
- Incoming and outgoing cases
- Pending caseloads
- Total dispositions

## Loading the Primary Dataset

```python
import pandas as pd

base_url = (
    "https://raw.githubusercontent.com/"
    "tdjohnson3210-oss/access-barriers-analysis/main/data_processed"
)

dfs = []

for i in range(9):
    dfs.append(
        pd.read_parquet(
            f"{base_url}/df_primary_part_{i}.parquet"
        )
    )

df_primary = pd.concat(
    dfs,
    ignore_index=True
)

print(df_primary.shape)
```

## Loading the Secondary Dataset

```python
import pandas as pd

url = (
    "https://raw.githubusercontent.com/"
    "tdjohnson3210-oss/access-barriers-analysis/main"
)

df_secondary = pd.read_parquet(
    f"{url}/data_processed/df_secondary.parquet"
)

print(df_secondary.shape)
```

## Modeling Approach

### Model 1: Civil Filings Regression

**Model Type:** Multiple Linear Regression

**Target Variable**
- Civil Filings

**Predictors**
- Transportation Score
- Digital Score
- Education Score
- Language Score
- Disability Score
- Household Score
- Mobility Score
- Population
- Population Density
- RUCA

**Key Results**
- R² = 0.945
- MAE = 371
- RMSE = 562
- Population and rurality were significant predictors of civil filings.
- Transportation barriers were not a statistically significant independent predictor after controlling for other variables.

---

### Model 2: Transportation Risk Classification

**Model Type:** Random Forest Classification

**Target Variable**
- Transportation Risk Category

**Predictors**
- Digital Score
- Education Score
- Language Score
- Disability Score
- Household Score
- Mobility Score

**Key Results**
- Accuracy = 75%
- Digital barriers were the strongest predictor of transportation risk.
- Education, household, and mobility barriers also contributed substantially to classification performance.
- Most classification errors occurred between neighboring transportation risk categories.

## Key Findings

- Transportation barriers were strongly associated with digital and educational barriers.
- Transportation barriers did not independently predict civil filings after controlling for geographic and demographic factors.
- Population and rurality were the strongest predictors of filing activity.
- Transportation risk could be classified with 75% accuracy using other access-related barriers.
- Transportation disadvantage appears to be part of a broader pattern of access-related challenges rather than an isolated barrier.
