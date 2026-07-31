"""Reject unsafe or insufficiently aggregated public dashboard artifacts."""

from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIRECTORY = PROJECT_ROOT / "data" / "dashboard"

EXPECTED_COLUMNS = {
    "dataset_readiness.csv": [
        "is_structurally_ready",
        "is_ready_for_behavioral_enrichment_analysis",
        "raw_participant_count",
        "base_cohort_count",
        "train_participant_count",
        "evaluation_participant_count",
        "train_site_count",
        "evaluation_site_count",
        "exclusions_display",
    ],
    "feature_coverage.csv": [
        "cohort_split",
        "feature_name",
        "available_count",
        "missing_count",
        "participant_count",
        "coverage_pct",
    ],
    "site_shift.csv": [
        "cohort_split",
        "site_label",
        "participant_count",
        "mean_age",
        "asd_pct",
        "mean_full_scale_iq",
    ],
    "cohort_split_summary.csv": [
        "cohort_split",
        "diagnostic_group",
        "participant_count",
        "site_count",
    ],
}

MAXIMUM_ROWS = {
    "dataset_readiness.csv": 1,
    "feature_coverage.csv": 18,
    "site_shift.csv": 3,
    "cohort_split_summary.csv": 4,
}
IDENTIFIER_COLUMNS = {"subject_id", "sub_id", "participant_id", "patient_id", "record_id"}


def validate_file(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as artifact_file:
        reader = csv.DictReader(artifact_file)
        columns = reader.fieldnames or []
        rows = list(reader)

    if columns != EXPECTED_COLUMNS[path.name]:
        raise ValueError(f"Unexpected columns in {path.name}: {columns}")
    if IDENTIFIER_COLUMNS.intersection(column.lower() for column in columns):
        raise ValueError(f"Participant identifier column found in {path.name}.")
    if not rows or len(rows) > MAXIMUM_ROWS[path.name]:
        raise ValueError(f"Unexpected grain or row count in {path.name}: {len(rows)}")
    if "participant_count" in columns:
        for row in rows:
            if int(row["participant_count"]) < 10:
                raise ValueError(f"Small participant group found in {path.name}: {row}")


def main() -> None:
    found = {path.name for path in ARTIFACT_DIRECTORY.glob("*.csv")}
    expected = set(EXPECTED_COLUMNS)
    if found != expected:
        raise ValueError(f"Expected {sorted(expected)}, found {sorted(found)}")

    for filename in sorted(EXPECTED_COLUMNS):
        validate_file(ARTIFACT_DIRECTORY / filename)

    print("Dashboard artifacts passed privacy and aggregation validation.")


if __name__ == "__main__":
    main()
