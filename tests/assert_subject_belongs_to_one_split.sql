select subject_id
from {{ ref('cohort_assignment') }}
group by subject_id
having count(distinct cohort_split) <> 1

