import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Access Barriers Analysis Dashboard",
    layout="wide"
)

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
st.caption("COUNTY OVERVIEW")

st.subheader(
    f"{selected_county} County Access Snapshot"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("County Access Score", "--")
    st.caption("Higher scores suggest more barriers")

with col2:
    st.metric("Statewide Ranking", "--")
    st.caption("Ranked from higher to lower barriers")

with col3:
    st.metric("Risk Classification", "--")
    st.caption("Based on combined access indicators")

with col4:
    st.metric("Similar Communities", "--")
    st.caption("Counties with comparable patterns")

# Map and Profile ----
st.divider()

map_col, profile_col = st.columns([3, 1])

with map_col:

    st.caption("COUNTY MAP")

    st.subheader(
        "Access Barriers Across Washington"
    )

    st.caption(
        "County access scores shown from lower to higher potential barriers"
    )

    st.info(
        "Interactive Washington county map coming soon."
    )

    st.container(height=250)

with profile_col:

    st.subheader("County Profile")

    st.metric(
        "Access Classification",
        "--"
    )

    st.markdown("**Regional Classification**")
    st.write("--")

    st.markdown("**Community Type**")
    st.write("--")

    st.markdown("**Statewide Comparison**")
    st.write("--")

# County Comparison ----
st.divider()

st.caption("COUNTY COMPARISON")

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
        "Score": [79, 74, 67, 65, 64]
    }
)

st.bar_chart(
    comparison_df.set_index("County")
)

# Community Context ----
st.divider()

st.caption("COMMUNITY CONTEXT")

st.subheader(
    "Factors Associated With Access Barriers"
)

factor1, factor2, factor3, factor4, factor5 = st.columns(5)

factor_titles = [
    "Transportation Availability",
    "Geographic Isolation",
    "Rural Accessibility",
    "Service Proximity",
    "Community Characteristics"
]

factor_descriptions = [
    "Access to public transit and reliable transportation.",
    "Travel distance and natural geographic constraints.",
    "Ability to reach services from rural communities.",
    "Distance to courthouses and legal assistance.",
    "Local conditions that affect service access."
]

for col, title, description in zip(
    [factor1, factor2, factor3, factor4, factor5],
    factor_titles,
    factor_descriptions
):
    with col:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(description)

# Key Insights ----
st.divider()

st.caption("DECISION SUPPORT")

st.subheader(
    f"Key Insights for {selected_county} County"
)

insight_col1, insight_col2, insight_col3 = st.columns(3)

insights = [
    "This county exhibits higher access barriers than the statewide average.",
    "Transportation and geographic factors appear to contribute to the county profile.",
    "Comparable counties demonstrate similar accessibility patterns and may provide useful planning comparisons."
]

for col, insight in zip(
    [insight_col1, insight_col2, insight_col3],
    insights
):
    with col:
        with st.container(border=True):
            st.write(insight)

# About the Model ----
with st.expander(
    "About the Model",
    expanded=False
):

    st.markdown(
        """
        ### Project Purpose

        Placeholder

        ### Data Sources

        Placeholder

        ### Methodology

        Placeholder

        ### Model Limitations

        Placeholder

        ### Intended Use

        Placeholder
        """
    )
