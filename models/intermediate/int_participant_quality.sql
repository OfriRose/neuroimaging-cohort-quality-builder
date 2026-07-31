with participants as (
    select
        *,
        count(*) over (partition by subject_id) = 1 as has_unique_subject_id
    from {{ ref('stg_abide_participants') }}
),

quality_flags as (
    select
        *,
        subject_id is not null as has_subject_id,
        site_id is not null as has_site_id,
        coalesce(age_at_scan between 7 and 64, false) as has_plausible_age,
        coalesce(sex_code in (1, 2), false) as has_valid_sex,
        coalesce(diagnostic_group_code in (1, 2), false) as has_valid_diagnostic_group
    from participants
)

select
    *,
    has_subject_id
        and has_unique_subject_id
        and has_site_id
        and has_plausible_age
        and has_valid_sex
        and has_valid_diagnostic_group as is_base_cohort_eligible
from quality_flags
