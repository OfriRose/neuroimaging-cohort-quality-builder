select site_id, cohort_split, diagnostic_group, feature_name
from {{ ref('feature_coverage') }}
group by site_id, cohort_split, diagnostic_group, feature_name
having count(*) <> 1

