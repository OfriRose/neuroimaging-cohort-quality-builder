select count(*) as row_count
from {{ ref('dataset_readiness') }}
having count(*) <> 1

