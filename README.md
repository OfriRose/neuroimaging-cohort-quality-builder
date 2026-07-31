# Neuroimaging Cohort Quality Builder

An analytics-engineering portfolio project that turns local ABIDE I phenotypic
metadata into a tested cohort, quantifies coverage and site shift, and publishes
only aggregate, de-identified dashboard outputs. It does not process images,
diagnose autism, or make clinical claims.

[View the live dashboard](https://neuroimaging-cohort.streamlit.app/)

```text
Local ABIDE I data → PostgreSQL + dbt marts → checked-in aggregate CSVs → public Streamlit dashboard
```

The public dashboard exposes no raw ABIDE files, participant records, identifiers,
or participant-level derived artifacts. Its three pages explain cohort readiness,
coverage limitations, and held-out site shift. See [DATA_ATTRIBUTION.md](DATA_ATTRIBUTION.md)
for attribution and responsible-use information.

## Local refresh

Register with ABIDE/NITRC, obtain access, and place the source files locally in
`data/raw/`. They are intentionally not included in this repository.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-local.txt
cp profiles.yml.example profiles.yml
docker compose up -d --wait
dbt build --profiles-dir .
python scripts/export_dashboard_data.py
streamlit run app.py
```

> Screenshot placeholder: public Dataset Readiness page showing aggregate cohort and split counts.
