import altair as alt
import streamlit as st

from dashboard_data import (
    artifacts_are_available,
    attribution_footer,
    display_label,
    load_artifact,
    show_missing_artifacts_message,
)

st.header("Coverage & limitations")
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
        with column.container(border=True):
            st.metric(display_label(feature["feature_name"]), "0.0%")
            st.badge("0% in evaluation", color="red")

    coverage_display = coverage.assign(
        feature_label=coverage["feature_name"].map(display_label),
        split_label=coverage["cohort_split"].map(display_label),
    )
    chart = (
        alt.Chart(coverage_display)
        .mark_bar()
        .encode(
            x=alt.X("feature_label:N", title="Feature", sort=None),
            xOffset=alt.XOffset("split_label:N", title="Cohort split"),
            y=alt.Y("coverage_pct:Q", title="Coverage (%)", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color("split_label:N", title="Cohort split"),
            tooltip=[
                alt.Tooltip("feature_label:N", title="Feature"),
                alt.Tooltip("split_label:N", title="Cohort split"),
                alt.Tooltip("coverage_pct:Q", title="Coverage", format=".1f"),
            ],
        )
    )
    st.altair_chart(chart, width="stretch")

    coverage_table = coverage_display[
        [
            "split_label",
            "feature_label",
            "available_count",
            "missing_count",
            "participant_count",
            "coverage_pct",
        ]
    ].rename(columns=display_label)
    st.dataframe(
        coverage_table,
        hide_index=True,
        column_config={
            "Coverage (%)": st.column_config.NumberColumn("Coverage (%)", format="%.1f%%")
        },
    )

attribution_footer()
