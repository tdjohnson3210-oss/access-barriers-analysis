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

# Uncomment when URLs are confirmed working ----
# (
#     civil_model,
#     civil_features,
#     transportation_model,
#     transportation_features
# ) = load_models()

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
        value="--"
    )
    st.caption("Higher scores suggest more barriers")

with col2:
    st.metric(
        label="Statewide Ranking",
        value="--"
    )
    st.caption("Ranked from higher to lower barriers")

with col3:
    st.metric(
        label="Risk Classification",
        value="--"
    )
    st.caption("Based on combined access indicators")

with col4:
    st.metric(
        label="Similar Communities",
        value="--"
    )
    st.caption("Counties with comparable patterns")

# Map and Profile ----
map_col, profile_col = st.columns([2, 1])

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

with profile_col:

    st.subheader("County Profile")

    st.markdown(
        f"### {selected_county} County"
    )

    st.metric(
        label="Access Classification",
        value="--"
    )

    st.divider()

    st.markdown("**Regional Classification**")
    st.write("--")

    st.markdown("**Community Type**")
    st.write("--")

    st.markdown("**Statewide Comparison**")
    st.write("--")

    st.divider()

    st.info(
        """
        County-specific characteristics and
        interpretation will appear here.
        """
    )


# County Comparison ----
st.markdown("### COUNTY COMPARISON")

st.subheader(
    "Compare With Similar Communities"
)

st.caption(
    "Access scores for counties with similar geographic and community characteristics"
)

comparison_df = pd.DataFrame(
    {
        "County": [
            "Adams",
            selected_county,
            "Franklin",
            "Grant",
            "Douglas"
        ],
        "Score": [
            79,
            74,
            67,
            65,
            64
        ]
    }
)

st.bar_chart(
    comparison_df.set_index("County")
)


# Community Context ----
st.markdown("### COMMUNITY CONTEXT")

st.subheader(
    "Factors Associated With Access Barriers"
)

st.caption(
    "Conditions that may shape how easily residents can reach and use court services."
)

factor1, factor2, factor3, factor4, factor5 = st.columns(5)

with factor1:
    st.info(
        """
        **Transportation Availability**

        Access to public transit and
        reliable transportation.
        """
    )

with factor2:
    st.info(
        """
        **Geographic Isolation**

        Travel distance and natural
        geographic constraints.
        """
    )

with factor3:
    st.info(
        """
        **Rural Accessibility**

        Ability to reach services from
        rural communities.
        """
    )

with factor4:
    st.info(
        """
        **Service Proximity**

        Distance to courthouses and
        legal assistance.
        """
    )

with factor5:
    st.info(
        """
        **Community Characteristics**

        Local conditions that affect
        service access.
        """
    )


# Key Insights ----
st.markdown("### DECISION SUPPORT")

st.subheader(
    f"Key Insights for {selected_county} County"
)

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.success(
        """
        This county exhibits higher
        access barriers than the
        statewide average.
        """
    )

with insight_col2:
    st.success(
        """
        Transportation and geographic
        factors appear to contribute
        to the county profile.
        """
    )

with insight_col3:
    st.success(
        """
        Comparable counties demonstrate
        similar accessibility patterns
        and may provide useful
        planning comparisons.
        """
    )


# About the Model ----
with st.expander(
    "About the Model",
    expanded=False
):

    st.markdown(
        """
        ### Project Purpose

        This dashboard is designed to support
        exploration of potential access-to-justice
        barriers across Washington State communities.

        ### Data Sources

        Placeholder

        ### Methodology

        Placeholder

        ### Model Limitations

        Placeholder

        ### Intended Use

        This tool is intended to support research,
        planning, and discussion. Results should not
        be interpreted as definitive measures of
        individual community needs.
        """
    )
