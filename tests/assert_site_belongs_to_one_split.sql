select site_id
from {{ ref('cohort_assignment') }}
group by site_id
having count(distinct cohort_split) <> 1

