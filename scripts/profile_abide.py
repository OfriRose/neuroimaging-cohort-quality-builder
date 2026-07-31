"""Profile the raw ABIDE I phenotypic CSV using the project's missing-value rules."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

REQUIRED_FIELDS = ("SUB_ID", "SITE_ID", "AGE_AT_SCAN", "SEX", "DX_GROUP")
OPTIONAL_FIELDS = (
    "DSM_IV_TR", "FIQ", "VIQ", "PIQ", "ADOS_TOTAL", "SRS_RAW_TOTAL",
    "SCQ_TOTAL", "AQ_TOTAL", "COMORBIDITY",
)
MISSING_SENTINELS = {"", "-9999"}
DX_LABELS = {"1": "autism spectrum disorder", "2": "typically developing control"}


def is_missing(value: str | None) -> bool:
    return value is None or value.strip() in MISSING_SENTINELS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path", nargs="?", type=Path,
        default=Path("data/raw/Phenotypic_V1_0b.csv"),
    )
    args = parser.parse_args()

    with args.csv_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    required_columns = set(REQUIRED_FIELDS) | set(OPTIONAL_FIELDS)
    absent = required_columns - set(rows[0] if rows else ())
    if absent:
        raise ValueError(f"CSV is missing expected columns: {sorted(absent)}")

    subject_ids = {row["SUB_ID"].strip() for row in rows if not is_missing(row["SUB_ID"])}
    sites = {row["SITE_ID"].strip() for row in rows if not is_missing(row["SITE_ID"])}

    print(f"row_count: {len(rows)}")
    print(f"unique_participants: {len(subject_ids)}")
    print(f"unique_sites: {len(sites)}")
    print("\nmissing_required:")
    for field in REQUIRED_FIELDS:
        count = sum(is_missing(row[field]) for row in rows)
        print(f"  {field}: {count} ({count / len(rows):.1%})")

    print("\nmissing_optional_enrichment:")
    for field in OPTIONAL_FIELDS:
        count = sum(is_missing(row[field]) for row in rows)
        print(f"  {field}: {count} ({count / len(rows):.1%})")

    distribution = Counter(
        (row["SITE_ID"].strip(), DX_LABELS.get(row["DX_GROUP"].strip(), row["DX_GROUP"].strip() or "missing"))
        for row in rows
    )
    print("\ndiagnostic_group_by_site:")
    print("  site_id,diagnostic_group,row_count")
    for (site, group), count in sorted(distribution.items()):
        print(f"  {site},{group},{count}")


if __name__ == "__main__":
    main()

