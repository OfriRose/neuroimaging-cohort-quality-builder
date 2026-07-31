select *
from {{ ref('dataset_readiness') }}
where not is_structurally_ready
