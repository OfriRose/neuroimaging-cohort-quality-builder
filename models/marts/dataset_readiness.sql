with assignments as (
    select * from {{ ref('cohort_assignment') }}
),

cohort_counts as (
    select
        (select count(*) from {{ ref('stg_abide_participants') }}) as raw_participant_count,
        (select count(*) from {{ ref('base_cohort') }}) as base_cohort_count,
        (select count(*) from {{ ref('cohort_exclusions') }}) as exclusion_rule_count,
        count(*) filter (where cohort_split = 'train') as train_participant_count,
        count(*) filter (where cohort_split = 'evaluation') as evaluation_participant_count,
        count(distinct site_id) filter (where cohort_split = 'train') as train_site_count,
        count(distinct site_id) filter (where cohort_split = 'evaluation') as evaluation_site_count,
        count(*) filter (
            where subject_id is null
               or site_id is null
               or age_at_scan is null
               or sex is null
               or diagnostic_group is null
        ) as required_field_failure_count,
        count(distinct diagnostic_group) filter (where cohort_split = 'train') = 2
            as train_has_both_diagnostic_groups,
        count(distinct diagnostic_group) filter (where cohort_split = 'evaluation') = 2
            as evaluation_has_both_diagnostic_groups
    from assignments
),

split_overlap as (
    select count(*) as site_split_overlap_count
    from (
        select site_id
        from assignments
        group by site_id
        having count(distinct cohort_split) > 1
    ) overlapping_sites
),

coverage_summary as (
    select
        round(avg(coverage_pct), 1) as mean_feature_coverage_pct,
        round(min(coverage_pct), 1) as minimum_feature_coverage_pct
    from {{ ref('feature_coverage') }}
),

behavioral_coverage as (
    select
        5 as behavioral_feature_count,
        count(distinct feature_name) filter (where coverage_pct > 0)
            as behavioral_features_with_evaluation_coverage_count
    from {{ ref('feature_coverage') }}
    where cohort_split = 'evaluation'
      and feature_name in (
          'ados_total',
          'srs_raw_total',
          'scq_total',
          'aq_total',
          'comorbidity'
      )
)

select
    cohort_counts.*,
    split_overlap.site_split_overlap_count,
    coverage_summary.mean_feature_coverage_pct,
    coverage_summary.minimum_feature_coverage_pct,
    behavioral_coverage.behavioral_feature_count,
    behavioral_coverage.behavioral_features_with_evaluation_coverage_count,
    cohort_counts.base_cohort_count > 0
        and cohort_counts.train_participant_count > 0
        and cohort_counts.evaluation_participant_count > 0
        and cohort_counts.required_field_failure_count = 0
        and cohort_counts.train_has_both_diagnostic_groups
        and cohort_counts.evaluation_has_both_diagnostic_groups
        and split_overlap.site_split_overlap_count = 0 as is_structurally_ready,
    behavioral_coverage.behavioral_features_with_evaluation_coverage_count
        = behavioral_coverage.behavioral_feature_count
        as is_ready_for_behavioral_enrichment_analysis
from cohort_counts
cross join split_overlap
cross join coverage_summary
cross join behavioral_coverage
