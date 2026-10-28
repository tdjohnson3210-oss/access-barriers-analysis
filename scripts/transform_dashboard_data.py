import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# LOAD DATA ----

# MODEL 1 ----
predictor_cols = [
    "transportation_score",
    "digital_score",
    "education_score",
    "language_score",
    "disability_score",
    "household_score",
    "mobility_score",
    "population",
    "popdensity",
    "primaryruca"
]

X = model_df[predictor_cols]

y = model_df["civil"]

model = LinearRegression()

model.fit(X, y)

model_df["predicted_civil_filings"] = (
    model.predict(X)
)

model_df["filing_difference"] = (
    model_df["civil"]
    - model_df["predicted_civil_filings"]
)


# Filings Rank ----
model_df["civil_rank"] = (
    model_df
    .groupby("year")["civil"]
    .rank(
        ascending=False,
        method="dense"
    )
    .astype(int)
)


# MODEL 2 ----
model_df["transportation_risk"] = pd.qcut(
    model_df["transportation_score"],
    q=5,
    labels=[
        "Very Low",
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]
)

X_transport = model_df[
    [
        "digital_score",
        "education_score",
        "language_score",
        "disability_score",
        "household_score",
        "mobility_score"
    ]
]

y_transport = model_df["transportation_risk"]

rf_model = RandomForestClassifier(
    random_state=42
)

rf_model.fit(
    X_transport,
    y_transport
)


# Access Scores ----
score_cols = [
    "transportation_score",
    "digital_score",
    "education_score",
    "language_score",
    "disability_score",
    "household_score",
    "mobility_score"
]

model_df["access_score"] = (
    model_df[score_cols]
    .mean(axis=1)
)

model_df["access_rank"] = (
    model_df
    .groupby("year")["access_score"]
    .rank(
        ascending=False,
        method="dense"
    )
    .astype(int)
)


# Filtered dataset ----
dashboard_df = (
    model_df
    .rename(
        columns={
            "countyname20": "county",
            "civil": "actual_civil_filings"
        }
    )
)

dashboard_df["state"] = "Washington"

dashboard_df = dashboard_df[
    [
        "state",
        "county",
        "year",
        "actual_civil_filings",
        "predicted_civil_filings",
        "filing_difference",
        "civil_rank",
        "transportation_risk",
        "transportation_score",
        "digital_score",
        "education_score",
        "language_score",
        "disability_score",
        "household_score",
        "mobility_score",
        "access_score",
        "access_rank",
        "population",
        "popdensity",
        "primaryruca"
    ]
]


# Save ----
# dashboard_df.to_parquet(
#    "dashboard_data.parquet",
#    index=False
#)
