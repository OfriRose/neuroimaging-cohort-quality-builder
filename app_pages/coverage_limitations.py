import streamlit as st

from dashboard_data import (
    artifacts_are_available,
    attribution_footer,
    load_artifact,
    show_missing_artifacts_message,
)

st.title("Coverage & limitations")
st.caption("Feature availability by cohort split. All values are aggregate counts or percentages.")

if not artifacts_are_available():
    show_missing_artifacts_message()
else:
    coverage = load_artifact("feature_coverage.csv")
    st.error(
        "Held-out evaluation coverage is 0% for SRS, SCQ, AQ, and comorbidity. "
        "Behavioral-enrichment analyses are not supported for the held-out cohort."
    )
    zero_coverage = coverage[
        (coverage["cohort_split"] == "evaluation")
        & coverage["feature_name"].isin(["srs_raw_total", "scq_total", "aq_total", "comorbidity"])
    ]
    for column, (_, feature) in zip(st.columns(4), zero_coverage.iterrows()):
        column.metric(
            feature["feature_name"].replace("_", " ").upper(),
            "0.0%",
            "Evaluation",
            border=True,
        )

    st.bar_chart(coverage, x="feature_name", y="coverage_pct", color="cohort_split")
    st.dataframe(
        coverage,
        hide_index=True,
        column_config={"coverage_pct": st.column_config.NumberColumn("Coverage", format="%.1f%%")},
    )

attribution_footer()
