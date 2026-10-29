import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Washington Access Barriers Dashboard",
    layout="wide"
)

# KPI styling
st.markdown("""
<style>

[data-testid="stMetric"] {
    background-color: #111827;
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# Load data

@st.cache_data
def load_data():

    url = (
        "https://raw.githubusercontent.com/"
        "tdjohnson3210-oss/access-barriers-analysis/main/"
        "data_processed/dashboard_data.parquet"
    )

    return pd.read_parquet(url)

dashboard_df = load_data()

# Scoring

def classify_score(score):

    if score <= -1:
        return "Very Low"

    elif score <= -0.25:
        return "Low"

    elif score <= 0.25:
        return "Moderate"

    elif score <= 1:
        return "High"

    return "Very High"


score_order = {
    "Very Low": 1,
    "Low": 2,
    "Moderate": 3,
    "High": 4,
    "Very High": 5
}

# Filters

st.title(
    "Washington Access Barriers Dashboard"
)

filter_col1, filter_col2 = st.columns(2)

with filter_col1:

    selected_year = st.selectbox(
        "Year",
        sorted(
            dashboard_df["year"].unique()
        ),
        index=len(
            dashboard_df["year"].unique()
        ) - 1
    )

with filter_col2:

    selected_county = st.selectbox(
        "County",
        sorted(
            dashboard_df[
                dashboard_df["year"] == selected_year
            ]["county"].unique()
        )
    )

year_df = dashboard_df[
    dashboard_df["year"] == selected_year
].copy()

county_data = year_df[
    year_df["county"] == selected_county
].iloc[0]

# County snapshot

st.caption(
    "COUNTY SNAPSHOT"
)

st.subheader(
    selected_county
)

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Actual Civil Filings",
        f"{int(county_data['actual_civil_filings']):,}"
    )

with m2:

    st.metric(
        "Transportation Risk",
        county_data["transportation_risk"]
    )

with m3:

    st.metric(
        "Projected Civil Filings",
        f"{round(county_data['predicted_civil_filings']):,}",
        help="Expected civil filings based on the county's barrier profile."
    )

with m4:

    st.metric(
        "Statewide Rank",
        f"#{int(county_data['civil_rank'])}"
    )

# Barrier categories

barrier_profile = {
    "Transportation": classify_score(
        county_data["transportation_score"]
    ),
    "Digital": classify_score(
        county_data["digital_score"]
    ),
    "Education": classify_score(
        county_data["education_score"]
    ),
    "Language": classify_score(
        county_data["language_score"]
    ),
    "Disability": classify_score(
        county_data["disability_score"]
    ),
    "Household": classify_score(
        county_data["household_score"]
    ),
    "Mobility": classify_score(
        county_data["mobility_score"]
    )
}

highest_barrier = max(
    barrier_profile,
    key=lambda x: score_order[
        barrier_profile[x]
    ]
)

# Key findings bar

st.info(
    f"{selected_county} is classified as "
    f"{county_data['transportation_risk']} transportation risk and ranks "
    f"#{int(county_data['civil_rank'])} statewide for civil filings. "
    f"The strongest access barrier category is "
    f"{highest_barrier.lower()}."
)

# Statewide comparisons

st.divider()

st.subheader(
    "Washington Transportation Risk"
)

comparison_df = (
    year_df
    .sort_values(
        "transportation_score",
        ascending=False
    )
)

comparison_df["Barrier Category"] = (
    comparison_df["transportation_score"]
    .apply(classify_score)
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
    hover_data={
        "actual_civil_filings": ":,.0f",
        "population_actual": ":,.0f",
        "popdensity_actual": ":,.1f",
        "civil_rank": True,
        "transportation_risk": True,
        "Barrier Category": True,
        "transportation_score": False
    },
    height=700
)

fig.add_vline(
    x=county_data["transportation_score"],
    line_width=3,
    line_dash="dash",
    line_color="white"
)

fig.update_layout(
    yaxis_title="",
    xaxis_title="Relative Transportation Risk",
    legend_title="Risk Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# County details

st.divider()

left_col, right_col = st.columns(2)

with left_col:

    st.subheader(
        "County Context"
    )

    context_df = pd.DataFrame(
        {
            "Metric": [
                "Population",
                "Population Density",
                "Rurality",
                "Transportation Risk",
                "Civil Filing Rank"
            ],
            "Value": [
                f"{int(county_data['population_actual']):,}",
                f"{county_data['popdensity_actual']:.1f} people/sq mi",
                county_data.get(
                    "community_type",
                    "Unavailable"
                ),
                county_data["transportation_risk"],
                f"#{int(county_data['civil_rank'])}"
            ]
        }
    )

    st.dataframe(
        context_df,
        hide_index=True,
        use_container_width=True
    )

with right_col:

    st.subheader(
        "Access Barrier Profile"
    )

    profile_df = pd.DataFrame(
        {
            "Barrier": list(
                barrier_profile.keys()
            ),
            "Assessment": list(
                barrier_profile.values()
            )
        }
    )

    st.dataframe(
        profile_df,
        hide_index=True,
        use_container_width=True
    )

# About

with st.expander(
    "About the Model"
):

    st.markdown(
        """
        ### Project Purpose

        Identify access barriers across Washington county communities.

        ### Data Sources

        ACS demographic and socioeconomic indicators, RUCA classifications, and civil filing data.

        ### Methodology

        Access barrier measures were developed across transportation, digital access, education, language, disability, household, and mobility domains using county-level demographic and socioeconomic indicators.

        For dashboard reporting, barrier measures are translated into relative assessment categories ranging from Very Low to Very High. These categories provide an interpretable representation of how each county compares with other Washington counties across barrier dimensions.

        Linear regression was used to estimate expected civil filing activity. Transportation risk classifications were generated from transportation-related indicators and are presented as relative risk categories to support interpretation and comparison.

        ### Intended Use

        Support access-to-justice planning further related analysis across Washington State.
        """
    )
