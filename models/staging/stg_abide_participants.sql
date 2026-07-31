with source as (
    select * from {{ ref('Phenotypic_V1_0b') }}
),

normalized as (
    select
        nullif(nullif(trim(cast(sub_id as text)), ''), '-9999') as subject_id,
        nullif(nullif(trim(cast(site_id as text)), ''), '-9999') as site_id,
        nullif(nullif(trim(cast(age_at_scan as text)), ''), '-9999')::numeric as age_at_scan,
        nullif(nullif(trim(cast(sex as text)), ''), '-9999')::integer as sex_code,
        nullif(nullif(trim(cast(dx_group as text)), ''), '-9999')::integer as diagnostic_group_code,
        nullif(nullif(trim(cast(dsm_iv_tr as text)), ''), '-9999')::integer as dsm_iv_code,
        nullif(nullif(trim(cast(fiq as text)), ''), '-9999')::numeric as full_scale_iq,
        nullif(nullif(trim(cast(viq as text)), ''), '-9999')::numeric as verbal_iq,
        nullif(nullif(trim(cast(piq as text)), ''), '-9999')::numeric as performance_iq,
        nullif(nullif(trim(cast(adi_r_social_total_a as text)), ''), '-9999')::numeric as adi_r_social_total,
        nullif(nullif(trim(cast(adi_r_verbal_total_bv as text)), ''), '-9999')::numeric as adi_r_verbal_total,
        nullif(nullif(trim(cast(adi_rrb_total_c as text)), ''), '-9999')::numeric as adi_r_restricted_repetitive_behavior_total,
        nullif(nullif(trim(cast(adi_r_onset_total_d as text)), ''), '-9999')::numeric as adi_r_onset_total,
        nullif(nullif(trim(cast(ados_total as text)), ''), '-9999')::numeric as ados_total,
        nullif(nullif(trim(cast(ados_comm as text)), ''), '-9999')::numeric as ados_communication,
        nullif(nullif(trim(cast(ados_social as text)), ''), '-9999')::numeric as ados_social,
        nullif(nullif(trim(cast(srs_raw_total as text)), ''), '-9999')::numeric as srs_raw_total,
        nullif(nullif(trim(cast(scq_total as text)), ''), '-9999')::numeric as scq_total,
        nullif(nullif(trim(cast(aq_total as text)), ''), '-9999')::numeric as aq_total,
        nullif(nullif(trim(cast(comorbidity as text)), ''), '-9999') as comorbidity
    from source
)

select
    subject_id,
    site_id,
    age_at_scan,
    sex_code,
    case sex_code
        when 1 then 'male'
        when 2 then 'female'
        else null
    end as sex,
    diagnostic_group_code,
    case diagnostic_group_code
        when 1 then 'autism spectrum disorder'
        when 2 then 'typically developing control'
        else null
    end as diagnostic_group,
    dsm_iv_code,
    full_scale_iq,
    verbal_iq,
    performance_iq,
    adi_r_social_total,
    adi_r_verbal_total,
    adi_r_restricted_repetitive_behavior_total,
    adi_r_onset_total,
    ados_total,
    ados_communication,
    ados_social,
    srs_raw_total,
    scq_total,
    aq_total,
    comorbidity
from normalized

