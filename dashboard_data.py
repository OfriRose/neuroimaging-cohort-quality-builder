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
