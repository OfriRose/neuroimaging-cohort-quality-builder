"""Read-only Streamlit dashboard for the dbt cohort-quality marts."""

from __future__ import annotations

import os
from decimal import Decimal
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

MART_SCHEMA = os.getenv("DBT_MART_SCHEMA", "analytics_marts")
PAGES = ("Dataset Readiness", "Coverage & Limitations", "Site Shift")


@st.cache_resource
def database_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "abide"),
        user=os.getenv("POSTGRES_USER", "abide"),
        password=os.getenv("POSTGRES_PASSWORD", "abide_dev_password"),
        application_name="abide_quality_dashboard",
        options="-c default_transaction_read_only=on",
    )


@st.cache_data(ttl=60)
def query(sql: str) -> list[dict[str, Any]]:
    with database_connection().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql)
        return [
            {key: float(value) if isinstance(value, Decimal) else value for key, value in row.items()}
            for row in cursor.fetchall()
        ]


def readiness_page() -> None:
    readiness = query(f"SELECT * FROM {MART_SCHEMA}.dataset_readiness")[0]

    st.header("Dataset Readiness")
    st.caption("Two readiness questions, separated to avoid overstating what the data supports.")
    structural, behavioral = st.columns(2)
    if readiness["is_structurally_ready"]:
        structural.success("Structurally ready")
    else:
        structural.error("Not structurally ready")
    if readiness["is_ready_for_behavioral_enrichment_analysis"]:
        behavioral.success("Behavioral enrichment ready")
    else:
        behavioral.error("Not ready for behavioral enrichment analysis")

    raw, cohort, train, evaluation = st.columns(4)
    raw.metric("Raw participants", readiness["raw_participant_count"])
    cohort.metric("Eligible cohort", readiness["base_cohort_count"])
    train.metric("Train", readiness["train_participant_count"])
    evaluation.metric("Evaluation", readiness["evaluation_participant_count"])

    st.info(
        "The cohort is structurally ready: required fields pass, both diagnostic groups "
        "occur in both splits, and sites do not cross splits. Behavioral enrichment is "
        "not evaluation-ready because only 1 of 5 selected behavioral fields has any "
        "held-out coverage."
    )


def coverage_page() -> None:
    coverage = query(f"""
        SELECT
            cohort_split,
            feature_name,
            SUM(available_count) AS available_count,
            SUM(participant_count) AS participant_count,
            ROUND(100.0 * SUM(available_count) / SUM(participant_count), 1) AS coverage_pct
        FROM {MART_SCHEMA}.feature_coverage
        GROUP BY cohort_split, feature_name
        ORDER BY feature_name, cohort_split
    """)

    st.header("Coverage & Limitations")
    st.caption("Optional-field availability; these measures do not determine base-cohort eligibility.")
    st.error("Held-out evaluation coverage is 0% for SRS, SCQ, AQ, and comorbidity.")

    zero_features = ["srs_raw_total", "scq_total", "aq_total", "comorbidity"]
    columns = st.columns(4)
    for column, feature in zip(columns, zero_features):
        column.metric(feature.replace("_", " ").upper(), "0.0%", "Evaluation")

    st.bar_chart(coverage, x="feature_name", y="coverage_pct", color="cohort_split")
    st.dataframe(coverage, hide_index=True, width="stretch")
    st.warning(
        "Behavioral analyses using the zero-coverage fields cannot be assessed on the "
        "held-out sites. This is a dataset limitation, not a value to impute away."
    )


def site_shift_page() -> None:
    sites = query(f"""
        SELECT *
        FROM {MART_SCHEMA}.site_shift
        ORDER BY cohort_split, participant_count DESC, site_id
    """)
    evaluation_sites = [row for row in sites if row["cohort_split"] == "evaluation"]

    st.header("Site Shift")
    st.caption("Descriptive differences from the full training aggregate; no causal or clinical inference.")
    for site, column in zip(evaluation_sites, st.columns(len(evaluation_sites))):
        column.subheader(site["site_id"])
        column.metric("Participants", site["participant_count"])
        column.metric("Mean-age difference", f'{site["age_difference_from_train"]:+.2f} years')
        column.metric("ASD share difference", f'{site["asd_pct_point_difference_from_train"]:+.1f} pp')
        column.metric("Mean FIQ difference", f'{site["full_scale_iq_difference_from_train"]:+.2f}')

    st.dataframe(sites, hide_index=True, width="stretch")


st.set_page_config(page_title="ABIDE Cohort Quality", page_icon="✓", layout="wide")
st.title("ABIDE I Cohort Quality")
st.caption("Auditable cohort construction and limitations—no imaging or predictive modeling.")
selected_page = st.sidebar.radio("Page", PAGES)

try:
    if selected_page == "Dataset Readiness":
        readiness_page()
    elif selected_page == "Coverage & Limitations":
        coverage_page()
    else:
        site_shift_page()
except psycopg2.Error:
    st.error("Could not read the dbt marts. Start PostgreSQL and run `dbt build` first.")
    st.stop()
