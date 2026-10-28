import streamlit as st
import pandas as pd
import joblib
import requests

from io import BytesIO

st.set_page_config(
    page_title="Access Barriers Analysis Dashboard",
    layout="wide"
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
