with participants as (
    select * from {{ ref('int_participant_quality') }}
)

select subject_id, site_id, 'missing subject_id' as exclusion_reason
from participants
where not has_subject_id

union all

select subject_id, site_id, 'duplicate subject_id' as exclusion_reason
from participants
where has_subject_id and not has_unique_subject_id

union all

select subject_id, site_id, 'missing site_id' as exclusion_reason
from participants
where not has_site_id

union all

select subject_id, site_id, 'age_at_scan outside 7-64' as exclusion_reason
from participants
where not coalesce(has_plausible_age, false)

union all

select subject_id, site_id, 'sex code not in (1, 2)' as exclusion_reason
from participants
where not coalesce(has_valid_sex, false)

union all

select subject_id, site_id, 'diagnostic group code not in (1, 2)' as exclusion_reason
from participants
where not coalesce(has_valid_diagnostic_group, false)

