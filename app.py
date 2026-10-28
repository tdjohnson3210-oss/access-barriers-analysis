import streamlit as st
import pandas as pd
import joblib
import requests

from io import BytesIO

st.set_page_config(
    page_title="Access Barriers Analysis Dashboard",
    layout="wide"
)

# GitHub URLs ----
BASE_URL = (
    "https://raw.githubusercontent.com/"
    "tdjohnson3210-oss/access-barriers-analysis/main/models"
)

CIVIL_MODEL_URL = (
    f"{BASE_URL}/civil_filings_model.pkl"
)

CIVIL_FEATURES_URL = (
    f"{BASE_URL}/civil_filings_features.pkl"
)

TRANSPORT_MODEL_URL = (
    f"{BASE_URL}/transportation_risk_model.pkl"
)

TRANSPORT_FEATURES_URL = (
    f"{BASE_URL}/transportation_risk_features.pkl"
)

# Load Models ----
@st.cache_resource
def load_models():

    # Civil Filings
    civil_model = joblib.load(
        BytesIO(
            requests.get(
                CIVIL_MODEL_URL
            ).content
        )
    )

    civil_features = joblib.load(
        BytesIO(
            requests.get(
                CIVIL_FEATURES_URL
            ).content
        )
    )

    # Transportation Risk
    transportation_model = joblib.load(
        BytesIO(
            requests.get(
                TRANSPORT_MODEL_URL
            ).content
        )
    )

    transportation_features = joblib.load(
        BytesIO(
            requests.get(
                TRANSPORT_FEATURES_URL
            ).content
        )
    )

    return (
        civil_model,
        civil_features,
        transportation_model,
        transportation_features
    )

(
    civil_model,
    civil_features,
    transportation_model,
    transportation_features
) = load_models()

# County Selection ----
selected_county = st.selectbox(
    "County",
    [
        "Yakima",
        "Adams",
        "Benton",
        "Chelan",
        "Clark"
    ]
)

# County Overview ----
st.markdown("### COUNTY OVERVIEW")

st.markdown(
    f"""
    ## {selected_county} County Access Snapshot
    """
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="County Access Score",
        value="74 / 100"
    )
    st.caption("Higher scores suggest more barriers")

with col2:
    st.metric(
        label="Statewide Ranking",
        value="#8 of 39"
    )
    st.caption("Ranked from higher to lower barriers")

with col3:
    st.metric(
        label="Risk Classification",
        value="High"
    )
    st.caption("Based on combined access indicators")

with col4:
    st.metric(
        label="Similar Communities",
        value="7"
    )
    st.caption("Counties with comparable patterns")


with map_col:

    st.subheader("Access Barriers Across Washington")

    st.caption(
        "County access scores shown from lower to higher potential barriers"
    )

    map_placeholder = pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": [3, 5, 2, 6, 4]
        }
    )

    st.scatter_chart(
        map_placeholder,
        x="x",
        y="y"
    )
