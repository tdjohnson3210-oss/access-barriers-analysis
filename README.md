# Access Barrier Index Analysis

This repository contains data, code, notebooks, and documentation used to analyze transportation and access barriers using American Community Survey (ACS), RUCA, and civil court filing data.

## Repository Structure

```text
access-barriers-analysis/
├── data_raw/              # Original source datasets
├── data_processed/        # Processed and merged datasets
├── notebooks/            # Jupyter notebooks
├── scripts/              # Data preparation scripts
├── metadata/             # Data dictionaries and documentation
├── docs/                 # Project documentation
└── README.md
```

## Datasets

### Primary Dataset

The primary dataset contains tract-level indicators related to:

- Transportation barriers
- Digital access
- Educational attainment
- Disability status
- Language barriers
- Household vulnerability
- Residential mobility
- Geographic and rurality characteristics

### Secondary Dataset

The secondary dataset contains court activity measures, including:

- New filings
- Self-represented litigant cases
- Interpreter usage
- Incoming and outgoing cases
- Pending caseloads
- Total dispositions

## Loading the Primary Dataset

If the primary dataset has been split into multiple parquet files, load and combine them as follows:

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

## Transportation Barrier Modeling

Two models were developed:

### Model 1: Transportation Relationship Model

- Model Type: Multiple Linear Regression
- Target: Transportation Barrier Score
- Predictors:
  - Digital Score
  - Education Score
  - Language Score
  - Disability Score
  - Household Score
  - Mobility Score

### Model 2: Transportation Risk Classification

- Model Type: Random Forest Classifier
- Target: Transportation Risk Category
- Predictors:
  - Digital Score
  - Education Score
  - Language Score
  - Disability Score
  - Household Score
  - Mobility Score

Transportation risk categories were created using:

```python
pd.qcut(
    transportation_score,
    q=5,
    labels=[
        "Very Low",
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
)
```

## Key Findings

- Transportation barriers are strongly associated with digital, household, and education barriers.
- Transportation barriers rarely occur in isolation.
- Digital barriers were the strongest predictor of transportation risk.
- Transportation risk could be classified with approximately 65% accuracy.
- Transportation appears to be part of broader patterns of structural disadvantage.

## Future Work

Future development may include:

- Transportation risk mapping
- Interactive dashboards
- Additional Models and Tuning
