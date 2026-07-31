with site_statistics as (
    select
        site_id,
        cohort_split,
        count(*) as participant_count,
        round(avg(age_at_scan), 2) as mean_age,
        round(stddev_samp(age_at_scan), 2) as age_stddev,
        round(100.0 * avg((sex = 'female')::integer), 1) as female_pct,
        round(100.0 * avg((diagnostic_group = 'autism spectrum disorder')::integer), 1) as asd_pct,
        round(100.0 * avg((full_scale_iq is not null)::integer), 1) as full_scale_iq_coverage_pct,
        round(avg(full_scale_iq), 2) as mean_full_scale_iq
    from {{ ref('cohort_assignment') }}
    group by site_id, cohort_split
),

train_benchmark as (
    select
        avg(age_at_scan) as mean_age,
        100.0 * avg((sex = 'female')::integer) as female_pct,
        100.0 * avg((diagnostic_group = 'autism spectrum disorder')::integer) as asd_pct,
        avg(full_scale_iq) as mean_full_scale_iq
    from {{ ref('cohort_assignment') }}
    where cohort_split = 'train'
)

select
    site_statistics.*,
    round(site_statistics.mean_age - train_benchmark.mean_age, 2) as age_difference_from_train,
    round(site_statistics.female_pct - train_benchmark.female_pct, 1) as female_pct_point_difference_from_train,
    round(site_statistics.asd_pct - train_benchmark.asd_pct, 1) as asd_pct_point_difference_from_train,
    round(site_statistics.mean_full_scale_iq - train_benchmark.mean_full_scale_iq, 2) as full_scale_iq_difference_from_train
from site_statistics
cross join train_benchmark

