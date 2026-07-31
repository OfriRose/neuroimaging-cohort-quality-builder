select
    'dataset_readiness' as report,
    null::text as site_id,
    null::text as cohort_split,
    null::text as feature_name,
    concat(
        'structural=', is_structurally_ready,
        '; behavioral_enrichment=', is_ready_for_behavioral_enrichment_analysis
    ) as result
from {{ ref('dataset_readiness') }}

union all

select
    'evaluation_site_shift',
    site_id,
    cohort_split,
    null::text,
    concat(
        'n=', participant_count,
        '; age_delta=', age_difference_from_train,
        '; asd_pct_point_delta=', asd_pct_point_difference_from_train,
        '; fiq_delta=', full_scale_iq_difference_from_train
    )
from {{ ref('site_shift') }}
where cohort_split = 'evaluation'

union all

select
    'feature_coverage',
    null::text,
    cohort_split,
    feature_name,
    round(sum(available_count) * 100.0 / sum(participant_count), 1)::text
from {{ ref('feature_coverage') }}
group by cohort_split, feature_name
