import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Access Barriers Analysis Dashboard",
    layout="wide"
)

# --------------------------------------------------
# COUNTY SELECTION
# --------------------------------------------------

selected_county = st.selectbox(
    "County",
    ["Yakima", "Adams", "Benton", "Chelan", "Clark"]
)

# --------------------------------------------------
# COUNTY OVERVIEW
# --------------------------------------------------

st.caption("COUNTY OVERVIEW")

st.subheader(
    f"{selected_county} County Access Snapshot"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Access Score", "--")

with col2:
    st.metric("Transportation Risk", "--")

with col3:
    st.metric("Predicted Civil Filings", "--")

with col4:
    st.metric("Statewide Rank", "--")

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

    st.empty()

with profile_col:

    st.subheader("County Profile")

    st.write("**Community Type**")
    st.write("--")

    st.write("**Urban-Rural Classification**")
    st.write("--")

    st.write("**Population**")
    st.write("--")

    st.write("**Similar Counties**")
    st.write("--")

# --------------------------------------------------
# BARRIER PROFILE
# --------------------------------------------------

st.divider()

st.subheader(
    "Barrier Category Scores"
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

# --------------------------------------------------
# COUNTY COMPARISON
# --------------------------------------------------

st.divider()

st.subheader(
    "Compare With Similar Communities"
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
        "Access Score": [
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

# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.divider()

st.subheader(
    f"Key Insights for {selected_county}"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        "Highest barrier category will appear here."
    )

with c2:
    st.info(
        "Transportation risk insights will appear here."
    )

with c3:
    st.info(
        "Similar county comparisons will appear here."
    )

# --------------------------------------------------
# ABOUT
# --------------------------------------------------

with st.expander("About the Model"):

    st.markdown("""
    ### Project Purpose

    Identify and visualize access barriers across Washington communities.

    ### Data Sources

    ACS demographic and socioeconomic indicators, RUCA classifications, and civil filing data.

    ### Methodology

    Access barrier scores were developed and used as inputs to predictive models examining civil filings and transportation risk.

    ### Intended Use

    Support access-to-justice planning and policy analysis.
    """)
