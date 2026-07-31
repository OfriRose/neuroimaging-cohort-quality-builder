# Neuroimaging Cohort Quality Builder

A reproducible analytics-engineering pipeline that turns real ABIDE I phenotypic
metadata into a tested, analysis-ready participant staging table. It demonstrates
explicit data contracts, missing-value normalization, multi-site quality checks,
and profiling for cohort design—without downloading images, diagnosing autism, or
making clinical claims.

## What it delivers

- PostgreSQL 16 in Docker Compose and a pinned `dbt-postgres` environment
- An immutable raw CSV loaded as a dbt seed
- `stg_abide_participants`, retaining every raw record while mapping coded fields
- Transparent eligibility flags, exclusions, and an auditable 1,111-person cohort
- Site-held-out assignment: 944 training and 167 evaluation participants
- Feature coverage, site-shift, and structural dataset-readiness audits
- dbt tests for identity, eligibility, and split isolation
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

The age-range source audit is warning-level: the out-of-range record remains in
staging and is documented in cohort exclusions rather than breaking the build.

## Dashboard

After `dbt build`, run the three-page, read-only dashboard:

```bash
streamlit run dashboard/app.py
```

> Screenshot placeholder: Dataset Readiness page with cohort counts and readiness flags.
