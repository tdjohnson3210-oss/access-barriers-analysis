import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Washington Access Barriers Dashboard",
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
# HELPER FUNCTION
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

    else:
        return "Very High"

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
        "actual_civil_filings": True,
        "civil_rank": True,
        "population_actual": ":,.0f",
        "popdensity_actual": ":,.1f",
        "Barrier Category": True,
        "transportation_score": False
    },
    height=700
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
# COUNTY DETAILS
# --------------------------------------------------

st.divider()

left_col, right_col = st.columns(2)

with left_col:

    st.subheader(
        "County Characteristics"
    )

    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Population",
                "Population Density",
                "Transportation Risk",
                "Civil Filing Rank"
            ],
            "Value": [
                f"{int(county_data['population_actual']):,}",
                f"{county_data['popdensity_actual']:.1f}",
                county_data["transportation_risk"],
                f"#{int(county_data['civil_rank'])}"
            ]
        }
    )

    st.dataframe(
        summary_df,
        hide_index=True,
        use_container_width=True
    )

with right_col:

    st.subheader(
        "Barrier Categories"
    )

    barrier_df = pd.DataFrame(
        {
            "Barrier": [
                "Transportation",
                "Digital",
                "Education",
                "Language",
                "Disability",
                "Household",
                "Mobility"
            ],
            "Category": [
                classify_score(
                    county_data["transportation_score"]
                ),
                classify_score(
                    county_data["digital_score"]
                ),
                classify_score(
                    county_data["education_score"]
                ),
                classify_score(
                    county_data["language_score"]
                ),
                classify_score(
                    county_data["disability_score"]
                ),
                classify_score(
                    county_data["household_score"]
                ),
                classify_score(
                    county_data["mobility_score"]
                )
            ]
        }
    )

    st.dataframe(
        barrier_df,
        hide_index=True,
        use_container_width=True
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
