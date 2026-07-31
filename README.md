# Neuroimaging Cohort Quality Builder

A reproducible analytics-engineering pipeline that turns real ABIDE I phenotypic
metadata into a tested, analysis-ready participant staging table. It demonstrates
explicit data contracts, missing-value normalization, multi-site quality checks,
and profiling for cohort design—without downloading images, diagnosing autism, or
making clinical claims.

## What Phase 1 delivers

- PostgreSQL 16 in Docker Compose and a pinned `dbt-postgres` environment
- An immutable raw CSV loaded as a dbt seed
- `stg_abide_participants`, retaining every raw record while mapping coded fields
- dbt tests for identity, required fields, categorical validity, and ages 7–64
- A dependency-free profile of missingness and diagnosis distribution by site

The governing data contract and site-held-out evaluation design are documented in
[`docs/cohort_spec.md`](docs/cohort_spec.md). Raw data under `data/raw/` is never
modified by the pipeline.

## Run locally

```bash
cp .env.example .env
cp profiles.yml.example profiles.yml
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d
dbt seed
dbt build
python scripts/profile_abide.py
```

`dbt build` intentionally reports source quality violations rather than silently
filtering them. Cohort inclusion logic belongs in a later downstream model.



123654789-+

+-*/
