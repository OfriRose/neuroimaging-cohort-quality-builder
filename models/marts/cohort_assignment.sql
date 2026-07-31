select
    *,
    case
        when site_id in ('UM_1', 'PITT') then 'evaluation'
        else 'train'
    end as cohort_split
from {{ ref('base_cohort') }}

