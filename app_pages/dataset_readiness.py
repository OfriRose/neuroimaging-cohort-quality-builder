import streamlit as st

from dashboard_data import (
    artifacts_are_available,
    attribution_footer,
    load_artifact,
    show_missing_artifacts_message,
)

st.title("Dataset readiness")
st.caption("Aggregate-only public demonstration of cohort quality controls.")

if not artifacts_are_available():
    show_missing_artifacts_message()
else:
    readiness = load_artifact("dataset_readiness.csv").iloc[0]
    structural, behavioral = st.columns(2)
    structural.metric(
        "Structurally ready",
        "Yes" if readiness["is_structurally_ready"] else "No",
        border=True,
    )
    behavioral.metric(
        "Ready for behavioral enrichment analysis",
        "Yes" if readiness["is_ready_for_behavioral_enrichment_analysis"] else "No",
        border=True,
    )

    with st.container(horizontal=True):
        st.metric("Eligible cohort", f'{readiness["base_cohort_count"]:,}', border=True)
        st.metric("Train", f'{readiness["train_participant_count"]:,}', border=True)
        st.metric("Evaluation", f'{readiness["evaluation_participant_count"]:,}', border=True)
        st.metric(
            "Sites",
            f'{readiness["train_site_count"]} train / {readiness["evaluation_site_count"]} evaluation',
            border=True,
        )

    st.info(
        "Structural readiness applies to the complete required-field cohort and its "
        "site-held-out split. Behavioral-enrichment readiness is stricter: it also requires "
        "usable held-out coverage for behavioral fields."
    )
    st.caption(f'Exclusions: {readiness["exclusions_display"]}')

attribution_footer()
