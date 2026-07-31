"""Load the checked-in, aggregate-only artifacts used by the public dashboard."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

ARTIFACT_DIRECTORY = Path(__file__).resolve().parent / "data" / "dashboard"
REQUIRED_ARTIFACTS = (
    "dataset_readiness.csv",
    "feature_coverage.csv",
    "site_shift.csv",
    "cohort_split_summary.csv",
)

DISPLAY_LABELS = {
    "ados_total": "ADOS total score",
    "aq_total": "AQ total score",
    "comorbidity": "Comorbidity recorded",
    "dsm_iv_code": "DSM-IV code",
    "full_scale_iq": "Full-scale IQ",
    "performance_iq": "Performance IQ",
    "scq_total": "SCQ total score",
    "srs_raw_total": "SRS raw total score",
    "verbal_iq": "Verbal IQ",
    "cohort_split": "Cohort split",
    "feature_name": "Feature",
    "feature_label": "Feature",
    "split_label": "Cohort split",
    "available_count": "Available participants",
    "missing_count": "Missing participants",
    "participant_count": "Participants",
    "coverage_pct": "Coverage (%)",
    "site_label": "Site",
    "mean_age": "Mean age",
    "asd_pct": "ASD proportion (%)",
    "mean_full_scale_iq": "Mean full-scale IQ",
    "train": "Train",
    "evaluation": "Evaluation",
}


def display_label(value: str) -> str:
    """Return the shared public label for a field or categorical value."""
    return DISPLAY_LABELS.get(value, value.replace("_", " ").capitalize())


@st.cache_data
def load_artifact(filename: str) -> pd.DataFrame:
    return pd.read_csv(ARTIFACT_DIRECTORY / filename)


def artifacts_are_available() -> bool:
    return all((ARTIFACT_DIRECTORY / filename).is_file() for filename in REQUIRED_ARTIFACTS)


def show_missing_artifacts_message() -> None:
    st.warning(
        "Aggregate dashboard data is not available. This public dashboard does not connect "
        "to databases or local services. Generate artifacts locally with "
        "`python scripts/export_dashboard_data.py`."
    )


def attribution_footer() -> None:
    st.divider()
    st.caption(
        "ABIDE I / INDI attribution. This educational portfolio dashboard uses aggregate, "
        "de-identified outputs only; it is not a diagnostic or clinical tool. ABIDE/INDI "
        "does not endorse this project. "
        "[Data access](https://fcon_1000.projects.nitrc.org/indi/abide/abide_I.html) · "
        "[CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/)"
    )
