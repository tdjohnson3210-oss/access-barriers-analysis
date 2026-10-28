import streamlit as st

st.set_page_config(
    page_title="Access Barriers Analysis Dashboard",
    layout="wide"
)

st.title("Access Barriers Analysis Dashboard")

st.write(
    "Explore where communities may experience barriers to court access and identify opportunities for more equitable services."
)

st.selectbox(
    "County",
    ["Yakima"]
)

st.selectbox(
    "Year",
    [2025]
)

st.button("Analyze County")
