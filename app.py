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
    st.metric("Access Score", "--")
    st.caption("Composite score across barrier categories")

with col2:
    st.metric("Transportation Risk", "--")
    st.caption("Predicted transportation risk level")

with col3:
    st.metric("Predicted Civil Filings", "--")
    st.caption("Model-estimated civil filing activity")

with col4:
    st.metric("Statewide Rank", "--")
    st.caption("Relative access barrier ranking")

# Map and Profile ----
st.divider()

map_col, profile_col = st.columns([3, 1])

with map_col:

    st.caption("STATEWIDE MAP")

    st.subheader(
        "Access Barriers Across Washington"
    )

    st.caption(
        "Counties shaded by overall access score."
    )

    st.info(
        "Interactive Washington county map coming soon."
    )

    st.container(height=300)

with profile_col:

    st.subheader("County Profile")

    st.markdown("**Community Type**")
    st.write("--")

    st.markdown("**Urban-Rural Classification**")
    st.write("--")

    st.markdown("**Population**")
    st.write("--")

    st.markdown("**Similar Counties**")
    st.write("--")

# Barrier Profile ----
st.divider()

st.caption("BARRIER PROFILE")

st.subheader(
    "Barrier Category Breakdown"
)

barrier_cols = st.columns(7)

barriers = [
    "Transportation",
    "Digital",
    "Education",
    "Language",
    "Disability",
    "Household",
    "Mobility"
]

for col, barrier in zip(barrier_cols, barriers):

    with col:

        st.metric(
            barrier,
            "--"
        )

# County Comparison ----
st.divider()

st.caption("COUNTY COMPARISON")

st.subheader(
    "Compare With Similar Communities"
)

st.caption(
    "Comparison of access scores among counties within the same cluster group."
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
        "Access Score": [79, 74, 67, 65, 64]
    }
)

st.bar_chart(
    comparison_df.set_index("County")
)

# Decision Support ----
st.divider()

st.caption("DECISION SUPPORT")

st.subheader(
    f"Key Insights for {selected_county} County"
)

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:

    with st.container(border=True):

        st.write(
            "Highest barrier category will be identified automatically."
        )

with insight_col2:

    with st.container(border=True):

        st.write(
            "Statewide ranking and transportation risk insights will appear here."
        )

with insight_col3:

    with st.container(border=True):

        st.write(
            "Cluster-based comparison counties and planning considerations will appear here."
        )

# About the Model ----
with st.expander(
    "About the Model",
    expanded=False
):

    st.markdown(
        """
        ### Project Purpose

        Identify and visualize access barriers across Washington communities.

        ### Data Sources

        American Community Survey (ACS), RUCA classifications, and Washington civil filing data.

        ### Methodology

        Barrier scores were developed for transportation, digital access, education, language, disability, household, and mobility factors. Predictive models were then used to estimate civil filing activity and transportation risk.

        ### Model Limitations

        Results identify patterns and associations and should not be interpreted as causal findings.

        ### Intended Use

        Support planning, research, and access-to-justice initiatives.
        """
    )
