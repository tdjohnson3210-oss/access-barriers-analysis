import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Access Barriers Analysis Dashboard",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    url = (
        "https://raw.githubusercontent.com/"
        "tdjohnson3210-oss/access-barriers-analysis/main/"
        "data_processed/dashboard_data.parquet"
    )

    return pd.read_parquet(url)

dashboard_df = load_data()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

selected_year = st.selectbox(
    "Year",
    sorted(
        dashboard_df["year"].unique()
    ),
    index=len(
        dashboard_df["year"].unique()) - 1
)

selected_county = st.selectbox(
    "County",
    sorted(
        dashboard_df[
            dashboard_df["year"] == selected_year
        ]["county"].unique()
    )
)

county_data = dashboard_df[
    (dashboard_df["county"] == selected_county)
    &
    (dashboard_df["year"] == selected_year)
].iloc[0]

# --------------------------------------------------
# COUNTY OVERVIEW
# --------------------------------------------------

st.caption("COUNTY OVERVIEW")

st.subheader(
    f"{selected_county} County Access Snapshot"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Civil Filings",
        int(
            county_data["actual_civil_filings"]
        )
    )

with col2:
    st.metric(
        "Transportation Risk",
        county_data["transportation_risk"]
    )

with col3:
    st.metric(
        "Expected Filings",
        round(
            county_data["predicted_civil_filings"]
        )
    )

with col4:
    st.metric(
        "Statewide Rank",
        f"#{int(county_data['civil_rank'])}"
    )

# --------------------------------------------------
# MAP + BARRIER PROFILE
# --------------------------------------------------

st.divider()

map_col, barrier_col = st.columns([4, 1])

with map_col:

    st.subheader(
        "Access Barriers Across Washington"
    )

    st.info(
        "Washington county choropleth map coming soon."
    )

with barrier_col:

    st.subheader(
        "Barrier Profile"
    )

    st.metric(
        "Transportation",
        round(
            county_data["transportation_score"],
            2
        )
    )

    st.metric(
        "Digital",
        round(
            county_data["digital_score"],
            2
        )
    )

    st.metric(
        "Education",
        round(
            county_data["education_score"],
            2
        )
    )

    st.metric(
        "Language",
        round(
            county_data["language_score"],
            2
        )
    )

    st.metric(
        "Disability",
        round(
            county_data["disability_score"],
            2
        )
    )

    st.metric(
        "Household",
        round(
            county_data["household_score"],
            2
        )
    )

    st.metric(
        "Mobility",
        round(
            county_data["mobility_score"],
            2
        )
    )

# --------------------------------------------------
# ABOUT
# --------------------------------------------------

with st.expander(
    "About the Model"
):

    st.markdown(
        """
        ### Project Purpose

        Identify and visualize access barriers across Washington communities.

        ### Data Sources

        ACS demographic and socioeconomic indicators,
        RUCA classifications, and civil filing data.

        ### Methodology

        Barrier scores were developed for transportation,
        digital access, education, language, disability,
        household, and mobility factors.

        Linear regression was used to estimate expected
        civil filings, while transportation risk categories
        were created from transportation barrier indicators.

        ### Intended Use

        Support access-to-justice planning,
        policy analysis, and community research.
        """
    )
