select *
from {{ ref('int_participant_quality') }}
where is_base_cohort_eligible

