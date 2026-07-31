-- The cohort specification defines the plausible/inclusion range as 7 through 64.
select subject_id, age_at_scan
from {{ ref('stg_abide_participants') }}
where age_at_scan is null
   or age_at_scan < 7
   or age_at_scan > 64

