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

st.title(
    "Washington Access Barriers Dashboard"
)

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

year_df = dashboard_df[
    dashboard_df["year"] == selected_year
]

# --------------------------------------------------
# SNAPSHOT
# --------------------------------------------------

st.caption(
    "COUNTY SNAPSHOT"
)

st.subheader(
    f"{selected_county}"
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Civil Filings",
        int(
            county_data["actual_civil_filings"]
        )
    )

with c2:

    st.metric(
        "Transportation Risk",
        county_data["transportation_risk"]
    )

with c3:

    st.metric(
        "Expected Filings",
        round(
            county_data["predicted_civil_filings"]
        )
    )

with c4:

    st.metric(
        "Statewide Rank",
        f"#{int(county_data['civil_rank'])}"
    )

# --------------------------------------------------
# STATEWIDE COMPARISON
# --------------------------------------------------

st.divider()

st.subheader(
    "Transportation Risk Across Washington"
)

comparison_df = (
    year_df
    .sort_values(
        "transportation_score",
        ascending=False
    )
)

fig = px.bar(
    comparison_df,
    x="transportation_score",
    y="county",
    orientation="h",
    color="transportation_risk",
    color_discrete_map={
        "Very Low": "#2ca02c",
        "Low": "#98df8a",
        "Moderate": "#ffbb78",
        "High": "#ff7f0e",
        "Very High": "#d62728"
    },
    hover_data=[
        "actual_civil_filings",
        "civil_rank"
    ],
    height=900
)

fig.update_layout(
    yaxis_title="",
    xaxis_title="Transportation Barrier Score",
    legend_title="Risk Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# COUNTY BARRIER PROFILE
# --------------------------------------------------

st.divider()

st.subheader(
    f"{selected_county} Barrier Profile"
)

barrier_df = pd.DataFrame({
    "Barrier": [
        "Transportation",
        "Digital",
        "Education",
        "Language",
        "Disability",
        "Household",
        "Mobility"
    ],
    "Score": [
        county_data["transportation_score"],
        county_data["digital_score"],
        county_data["education_score"],
        county_data["language_score"],
        county_data["disability_score"],
        county_data["household_score"],
        county_data["mobility_score"]
    ]
})

profile_fig = px.bar(
    barrier_df,
    x="Score",
    y="Barrier",
    orientation="h",
    color="Score",
    color_continuous_scale="RdYlGn_r",
    text_auto=".2f"
)

profile_fig.update_layout(
    height=500,
    yaxis_title="",
    xaxis_title="Barrier Score",
    coloraxis_showscale=False
)

st.plotly_chart(
    profile_fig,
    use_container_width=True
)

# --------------------------------------------------
# COUNTY COMPARISON TABLE
# --------------------------------------------------

st.divider()

st.subheader(
    "County Rankings"
)

ranking_df = (
    year_df[
        [
            "county",
            "transportation_risk",
            "actual_civil_filings",
            "civil_rank"
        ]
    ]
    .sort_values(
        "civil_rank"
    )
)

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True
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

        Linear regression was used to estimate expected civil filing activity. Transportation risk classifications were generated from transportation barrier indicators.

        ### Intended Use

        Support access-to-justice planning, research, and policy analysis across Washington State.
        """
    )
