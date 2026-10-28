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

def classify_ruca(ruca):

    if pd.isna(ruca):
        return "Unknown"

    elif ruca <= 3:
        return "Metropolitan"

    elif ruca <= 6:
        return "Micropolitan"

    else:
        return "Rural"


def describe_transportation_risk(risk):

    descriptions = {
        "Very Low": "Relatively few transportation-related access barriers",
        "Low": "Below-average transportation-related access barriers",
        "Moderate": "Moderate transportation-related access barriers",
        "High": "Elevated transportation-related access barriers",
        "Very High": "Substantially elevated transportation-related access barriers"
    }

    return descriptions.get(risk, "Unknown")


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

dashboard_df["community_type"] = (
    dashboard_df["primaryruca_actual"]
    .apply(classify_ruca)
)

dashboard_df["transportation_risk_description"] = (
    dashboard_df["transportation_risk"]
    .apply(describe_transportation_risk)
)

# Create user-friendly 0-100 barrier scores

for col in score_cols:

    dashboard_df[f"{col}_display"] = (
        dashboard_df[col]
        .rank(pct=True)
        .mul(100)
        .round(0)
        .astype(int)
    )

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
        "transportation_risk_description",

        "access_score",
        "access_rank",

        "community_type",

        "population_actual",
        "popdensity_actual",
        "primaryruca_actual",

        "transportation_score_display",
        "digital_score_display",
        "education_score_display",
        "language_score_display",
        "disability_score_display",
        "household_score_display",
        "mobility_score_display",

        # Keep originals for future analysis
        "transportation_score",
        "digital_score",
        "education_score",
        "language_score",
        "disability_score",
        "household_score",
        "mobility_score"
    ]
]


# Save ----
