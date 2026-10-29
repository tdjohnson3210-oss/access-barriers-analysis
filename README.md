# Access Barriers Analysis Dashboard

This repository contains the data, models, code, and documentation used to examine access-to-justice barriers across Washington State communities. The project combines demographic, socioeconomic, transportation, and court activity indicators to generate county-level access barrier assessments, transportation risk classifications, and projected civil filing estimates.

https://access-barriers-analysis-2mwwrmwezsizgdy9mcs5u6.streamlit.app/

## Dashboard

The project includes an interactive Streamlit dashboard that allows users to:

- Explore county-level transportation risk classifications
- Compare counties across Washington State
- Review projected civil filing estimates
- Examine access barrier profiles
- Analyze population, density, and rurality characteristics

### Application Files

```text
app.py                     # Streamlit dashboard
requirements.txt           # Application dependencies
data_processed/
└── dashboard_data.parquet # Dashboard dataset
```

## Repository Structure

```text
access-barriers-analysis/

├── app.py
├── requirements.txt

├── data_raw/
│   └── Source datasets

├── data_processed/
│   ├── dashboard_data.parquet
│   └── Processed modeling datasets

├── notebooks/
│   └── Data preparation, analysis, and modeling notebooks

├── scripts/
│   └── Data processing scripts

├── metadata/
│   └── Data dictionaries and supporting documentation

├── docs/
│   └── Project documentation

└── README.md
```

## Data Sources

The project incorporates data from:

- American Community Survey (ACS)
- Rural-Urban Commuting Area (RUCA) classifications
- Washington State civil court filing data

These sources were used to develop county-level measures of:

- Transportation barriers
- Digital access
- Educational attainment
- Disability status
- Language barriers
- Household vulnerability
- Residential mobility
- Population and rurality characteristics

## Models

### Civil Filings Model

**Model Type:** Multiple Linear Regression

**Purpose:** Estimate expected civil filing activity using access barrier indicators, population characteristics, and rurality measures.

**Performance:**

- R² = 0.945
- MAE = 371
- RMSE = 562

### Transportation Risk Model

**Model Type:** Random Forest Classification

**Purpose:** Classify county-level transportation risk using access barrier indicators.

**Performance:**

- Accuracy = 75%

## Key Findings

- Population and rurality were strong predictors of civil filing activity.
- Transportation barriers were associated with other access barriers but were not independently significant after controlling for demographic and geographic factors.
- Transportation risk classifications could be predicted with approximately 75% accuracy.
- Access barriers tend to occur as interconnected challenges rather than isolated conditions.

## Running the Dashboard

Install required packages:

```bash
pip install -r requirements.txt
```

Launch the dashboard:

```bash
streamlit run app.py
```
