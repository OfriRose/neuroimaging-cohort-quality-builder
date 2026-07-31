select subject_id
from {{ ref('base_cohort') }}
where not is_base_cohort_eligible

