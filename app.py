import streamlit as st
import pandas as pd
import plotly.express as px

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
# COUNTY PROFILE
# --------------------------------------------------

st.divider()

left_col, right_col = st.columns([3, 1])

with left_col:

    st.subheader(
        "County Comparison"
    )

    comparison_df = (
        dashboard_df[
            dashboard_df["year"] == selected_year
        ]
        .sort_values(
            "actual_civil_filings",
            ascending=True
        )
    )

    fig = px.bar(
        comparison_df,
        x="actual_civil_filings",
        y="county",
        orientation="h",
        height=1000
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right_col:

    st.subheader(
        "County Profile"
    )

    st.write("**Community Type**")
    st.write(
        county_data["community_type"]
    )

    st.write("**Population**")
    st.write(
        f"{county_data['population_actual']:,.0f}"
    )

    st.write("**Population Density**")
    st.write(
        f"{county_data['popdensity_actual']:,.1f}"
    )

    st.write("**RUCA Score**")
    st.write(
        round(
            county_data["primaryruca_actual"],
            1
        )
    )

# --------------------------------------------------
# BARRIER SCORES
# --------------------------------------------------

st.divider()

st.subheader(
    "Barrier Scores (0-100)"
)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

with col1:
    st.metric(
        "Transportation",
        county_data[
            "transportation_score_display"
        ]
    )

with col2:
    st.metric(
        "Digital",
        county_data[
            "digital_score_display"
        ]
    )

with col3:
    st.metric(
        "Education",
        county_data[
            "education_score_display"
        ]
    )

with col4:
    st.metric(
        "Language",
        county_data[
            "language_score_display"
        ]
    )

with col5:
    st.metric(
        "Disability",
        county_data[
            "disability_score_display"
        ]
    )

with col6:
    st.metric(
        "Household",
        county_data[
            "household_score_display"
        ]
    )

with col7:
    st.metric(
        "Mobility",
        county_data[
            "mobility_score_display"
        ]
    )

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader(
    f"Key Insights for {selected_county}"
)

score_cols = [
    "transportation_score_display",
    "digital_score_display",
    "education_score_display",
    "language_score_display",
    "disability_score_display",
    "household_score_display",
    "mobility_score_display"
]

highest_barrier = (
    county_data[score_cols]
    .idxmax()
    .replace(
        "_score_display",
        ""
    )
    .replace(
        "_",
        " "
    )
    .title()
)

c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        f"Highest barrier category: {highest_barrier}"
    )

with c2:
    st.info(
        county_data[
            "transportation_risk_description"
        ]
    )

with c3:
    st.info(
        f"County ranks #{int(county_data['civil_rank'])} statewide."
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

        Barrier scores were developed for transportation, digital access, education, language, disability, household, and mobility factors.

        Linear regression was used to estimate expected civil filings, while transportation risk categories were created from transportation barrier indicators.

        ### Intended Use

        Support access-to-justice planning, policy analysis, and community research.
        """
    )
