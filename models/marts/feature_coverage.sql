with participants as (
    select * from {{ ref('cohort_assignment') }}
),

coverage as (
    select
        participants.site_id,
        participants.cohort_split,
        participants.diagnostic_group,
        features.feature_name,
        features.is_available
    from participants
    cross join lateral (
        values
            ('dsm_iv_code', dsm_iv_code is not null),
            ('full_scale_iq', full_scale_iq is not null),
            ('verbal_iq', verbal_iq is not null),
            ('performance_iq', performance_iq is not null),
            ('ados_total', ados_total is not null),
            ('srs_raw_total', srs_raw_total is not null),
            ('scq_total', scq_total is not null),
            ('aq_total', aq_total is not null),
            ('comorbidity', comorbidity is not null)
    ) as features(feature_name, is_available)
)

select
    site_id,
    cohort_split,
    diagnostic_group,
    feature_name,
    count(*) as participant_count,
    sum(is_available::integer) as available_count,
    count(*) - sum(is_available::integer) as missing_count,
    round(100.0 * sum(is_available::integer) / count(*), 1) as coverage_pct
from coverage
group by site_id, cohort_split, diagnostic_group, feature_name

