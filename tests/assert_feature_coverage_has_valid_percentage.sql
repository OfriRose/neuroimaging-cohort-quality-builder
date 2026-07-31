select site_id, cohort_split, diagnostic_group, feature_name, coverage_pct
from {{ ref('feature_coverage') }}
where coverage_pct < 0 or coverage_pct > 100

