-- Run with: dbt show --inline "$(cat analyses/profile_abide.sql)"
with participants as (
    select * from {{ ref('stg_abide_participants') }}
)
select
    site_id,
    diagnostic_group,
    count(*) as participant_records
from participants
group by 1, 2
order by 1, 2

