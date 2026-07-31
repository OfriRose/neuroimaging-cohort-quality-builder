import streamlit as st

from dashboard_data import (
    artifacts_are_available,
    attribution_footer,
    display_label,
    load_artifact,
    show_missing_artifacts_message,
)

st.title("Site shift")
st.caption("Aggregate comparison of the training cohort with held-out UM_1 and PITT sites.")

if not artifacts_are_available():
    show_missing_artifacts_message()
else:
    sites = load_artifact("site_shift.csv")
    train = sites.loc[sites["cohort_split"] == "train"].iloc[0]
    evaluation_sites = sites.loc[sites["cohort_split"] == "evaluation"]

    for column, (_, site) in zip(st.columns(len(evaluation_sites)), evaluation_sites.iterrows()):
        with column.container(border=True):
            st.subheader(site["site_label"])
            st.metric("Participants", f'{site["participant_count"]:,}')
            st.metric("Mean age vs train", f'{site["mean_age"] - train["mean_age"]:+.2f} years')
            st.metric("ASD proportion vs train", f'{site["asd_pct"] - train["asd_pct"]:+.1f} pp')
            st.metric("Mean FIQ vs train", f'{site["mean_full_scale_iq"] - train["mean_full_scale_iq"]:+.2f}')

    sites_display = sites.copy()
    sites_display["cohort_split"] = sites_display["cohort_split"].map(display_label)
    sites_display = sites_display.rename(columns=display_label)
    st.dataframe(
        sites_display,
        hide_index=True,
        column_config={
            "Mean age": st.column_config.NumberColumn("Mean age", format="%.2f"),
            "ASD proportion (%)": st.column_config.NumberColumn(
                "ASD proportion (%)", format="%.1f%%"
            ),
            "Mean full-scale IQ": st.column_config.NumberColumn(
                "Mean full-scale IQ", format="%.2f"
            ),
        },
    )
    st.warning("These are descriptive site-level differences, not causal or clinical conclusions.")

attribution_footer()
