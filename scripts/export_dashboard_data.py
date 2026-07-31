"""Export privacy-reviewed aggregate dbt marts for the public dashboard."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIRECTORY = PROJECT_ROOT / "data" / "dashboard"
MART_SCHEMA = "analytics_marts"
LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}

EXPORTS = {
    "dataset_readiness.csv": f"""
        select
            is_structurally_ready,
            is_ready_for_behavioral_enrichment_analysis,
            raw_participant_count,
            base_cohort_count,
            train_participant_count,
            evaluation_participant_count,
            train_site_count,
            evaluation_site_count,
            case
                when exclusion_rule_count < 10 then 'Suppressed (<10)'
                else exclusion_rule_count::text
            end as exclusions_display
        from {MART_SCHEMA}.dataset_readiness
    """,
    "feature_coverage.csv": f"""
        select
            cohort_split,
            feature_name,
            sum(available_count)::integer as available_count,
            sum(missing_count)::integer as missing_count,
            sum(participant_count)::integer as participant_count,
            round(100.0 * sum(available_count) / sum(participant_count), 1) as coverage_pct
        from {MART_SCHEMA}.feature_coverage
        group by cohort_split, feature_name
        having sum(participant_count) >= 10
        order by feature_name, cohort_split
    """,
    "site_shift.csv": f"""
        select
            'train'::text as cohort_split,
            'Training aggregate'::text as site_label,
            count(*)::integer as participant_count,
            round(avg(age_at_scan), 2) as mean_age,
            round(100.0 * avg((diagnostic_group = 'autism spectrum disorder')::integer), 1) as asd_pct,
            round(avg(full_scale_iq), 2) as mean_full_scale_iq
        from {MART_SCHEMA}.cohort_assignment
        where cohort_split = 'train'

        union all

        select
            cohort_split,
            site_id as site_label,
            participant_count,
            mean_age,
            asd_pct,
            mean_full_scale_iq
        from {MART_SCHEMA}.site_shift
        where cohort_split = 'evaluation'
          and participant_count >= 10
        order by cohort_split, site_label
    """,
    "cohort_split_summary.csv": f"""
        select
            cohort_split,
            diagnostic_group,
            count(*)::integer as participant_count,
            count(distinct site_id)::integer as site_count
        from {MART_SCHEMA}.cohort_assignment
        group by cohort_split, diagnostic_group
        having count(*) >= 10
        order by cohort_split, diagnostic_group
    """,
}


def connect_to_local_postgres():
    """Connect only to an explicitly local PostgreSQL instance."""
    host = os.getenv("POSTGRES_HOST", "localhost")
    if host not in LOCAL_HOSTS:
        raise ValueError("Dashboard exports may only connect to local PostgreSQL.")

    return psycopg2.connect(
        host=host,
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "abide"),
        user=os.getenv("POSTGRES_USER", "abide"),
        password=os.getenv("POSTGRES_PASSWORD", "abide_dev_password"),
        application_name="abide_dashboard_export",
        options="-c default_transaction_read_only=on",
    )


def export_csv(cursor: RealDictCursor, output_path: Path, query: str) -> None:
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        raise ValueError(f"Query returned no rows for {output_path.name}.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with connect_to_local_postgres() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            for filename, query in EXPORTS.items():
                export_csv(cursor, OUTPUT_DIRECTORY / filename, query)

    print(f"Exported {len(EXPORTS)} aggregate dashboard files to {OUTPUT_DIRECTORY}.")


if __name__ == "__main__":
    main()
