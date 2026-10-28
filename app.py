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
        dashboard_df["year"].unique()
    ) - 1
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
        "Actual Civil Filings",
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
        "Expected Civil Filings",
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
# MAP + PROFILE
# --------------------------------------------------

st.divider()

map_col, profile_col = st.columns([3, 1])

with map_col:

    st.subheader(
        "Access Barriers Across Washington"
    )

    st.info(
        "Interactive county map coming soon."
    )

with profile_col:

    st.subheader(
        "County Profile"
    )

    st.write(
        "**Transportation Risk**"
    )

    st.write(
        county_data["transportation_risk"]
    )

    st.write(
        "**Population**"
    )

    st.write(
        f"{int(county_data['population']):,}"
    )

    st.write(
        "**Population Density**"
    )

    st.write(
        round(
            county_data["popdensity"],
            2
        )
    )

    st.write(
        "**Primary RUCA**"
    )

    st.write(
        county_data["primaryruca"]
    )

# --------------------------------------------------
# BARRIER PROFILE
# --------------------------------------------------

st.divider()

st.subheader(
    "Barrier Category Scores"
)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.metric(
        "Transportation",
        round(
            county_data["transportation_score"],
            2
        )
    )

with col2:
    st.metric(
        "Digital",
        round(
            county_data["digital_score"],
            2
        )
    )

with col3:
    st.metric(
        "Education",
        round(
            county_data["education_score"],
            2
        )
    )

with col4:
    st.metric(
        "Language",
        round(
            county_data["language_score"],
            2
        )
    )

with col5:
    st.metric(
        "Disability",
        round(
            county_data["disability_score"],
            2
        )
    )

with col6:
    st.metric(
        "Household",
        round(
            county_data["household_score"],
            2
        )
    )

with col7:
    st.metric(
        "Mobility",
        round(
            county_data["mobility_score"],
            2
        )
    )

# --------------------------------------------------
# COUNTY COMPARISON
# --------------------------------------------------

st.divider()

st.subheader(
    "Civil Filings Comparison"
)

comparison_df = (
    dashboard_df[
        dashboard_df["year"] == selected_year
    ]
    .sort_values(
        "actual_civil_filings",
        ascending=False
    )
    .head(10)
)

st.bar_chart(
    comparison_df.set_index(
        "county"
    )["actual_civil_filings"]
)

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader(
    f"Key Insights for {selected_county}"
)

score_cols = [
    "transportation_score",
    "digital_score",
    "education_score",
    "language_score",
    "disability_score",
    "household_score",
    "mobility_score"
]

highest_barrier = (
    county_data[score_cols]
    .idxmax()
    .replace("_score", "")
    .replace("_", " ")
    .title()
)

c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        f"Highest barrier category: {highest_barrier}"
    )

with c2:
    st.info(
        f"Transportation risk is classified as {county_data['transportation_risk']}."
    )

with c3:
    st.info(
        f"County ranks #{int(county_data['civil_rank'])} statewide for civil filings in {selected_year}."
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

        ACS demographic and socioeconomic indicators, RUCA classifications, and civil filing data.

        ### Methodology

        Barrier scores were developed for transportation, digital access, education, language, disability, household, and mobility factors. A linear regression model was used to estimate expected civil filing activity, while a transportation risk model classified county-year observations into transportation risk groups.

        ### Intended Use

        Support access-to-justice planning, research, and policy analysis.
        """
    )
