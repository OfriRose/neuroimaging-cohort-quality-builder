with raw_participants as (
    select * from {{ ref('stg_abide_participants') }}
),
base_cohort as (
    select * from {{ ref('base_cohort') }}
),
exclusions as (
    select * from {{ ref('cohort_exclusions') }}
),
assignments as (
    select * from {{ ref('cohort_assignment') }}
)

select 'participant_count' as metric, null::text as split, 'raw' as category, count(*) as count
from raw_participants
union all
select 'participant_count', null::text, 'base_cohort', count(*)
from base_cohort
union all
select 'exclusion_reason', null::text, exclusion_reason, count(*)
from exclusions
group by exclusion_reason
union all
select 'split_count', cohort_split, 'all', count(*)
from assignments
group by cohort_split
union all
select 'diagnostic_group', cohort_split, diagnostic_group, count(*)
from assignments
group by cohort_split, diagnostic_group
union all
select 'site', cohort_split, site_id, count(*)
from assignments
group by cohort_split, site_id
order by metric, split, category

