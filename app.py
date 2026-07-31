"""Public, aggregate-only Streamlit entry point."""

import streamlit as st

st.set_page_config(
    page_title="ABIDE cohort quality",
    page_icon=":material/fact_check:",
    layout="wide",
)

page = st.navigation(
    [
        st.Page("app_pages/dataset_readiness.py", title="Dataset Readiness", icon=":material/fact_check:"),
        st.Page("app_pages/coverage_limitations.py", title="Coverage & Limitations", icon=":material/warning:"),
        st.Page("app_pages/site_shift.py", title="Site Shift", icon=":material/compare_arrows:"),
    ],
    position="top",
)
page.run()
