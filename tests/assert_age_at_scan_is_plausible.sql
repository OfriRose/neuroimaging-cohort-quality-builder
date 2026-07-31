{{ config(severity='warn') }}

-- Audit only: out-of-range records remain in staging and are excluded downstream.
select subject_id, age_at_scan
from {{ ref('stg_abide_participants') }}
where age_at_scan is null
   or age_at_scan < 7
   or age_at_scan > 64
