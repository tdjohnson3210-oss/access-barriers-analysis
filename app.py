import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Washington Access Barriers Dashboard",
    layout="wide"
)

# --------------------------------------------------
# STYLING
# --------------------------------------------------

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
# HELPER FUNCTIONS
# --------------------------------------------------

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

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

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

# --------------------------------------------------
# COUNTY SNAPSHOT
# --------------------------------------------------

st.caption(
    "COUNTY SNAPSHOT"
)

st.subheader(
    selected_county
)

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "Civil Filings",
        f"{int(county_data['actual_civil_filings']):,}"
    )

with m2:

    st.metric(
        "Transportation Risk",
        county_data["transportation_risk"]
    )

with m3:

    st.metric(
        "Expected Filings",
        f"{round(county_data['predicted_civil_filings']):,}"
    )

with m4:

    st.metric(
        "Statewide Rank",
        f"#{int(county_data['civil_rank'])}"
    )

# --------------------------------------------------
# BARRIER CATEGORY CLASSIFICATIONS
# --------------------------------------------------

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

# --------------------------------------------------
# KEY FINDING
# --------------------------------------------------

st.info(
    f"{selected_county} is classified as "
    f"{county_data['transportation_risk']} transportation risk and ranks "
    f"#{int(county_data['civil_rank'])} statewide for civil filings. "
    f"The strongest access barrier category is "
    f"{highest_barrier.lower()}."
)

# --------------------------------------------------
# STATEWIDE COMPARISON
# --------------------------------------------------

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

# --------------------------------------------------
# COUNTY DETAILS
# --------------------------------------------------

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
                county_data["transportation_risk"
