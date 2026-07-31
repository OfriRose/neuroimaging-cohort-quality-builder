-- Staging normalizes values but must not filter or duplicate source records.
select
    (select count(*) from {{ ref('Phenotypic_V1_0b') }}) as source_row_count,
    (select count(*) from {{ ref('stg_abide_participants') }}) as staging_row_count
where (select count(*) from {{ ref('Phenotypic_V1_0b') }})
   <> (select count(*) from {{ ref('stg_abide_participants') }})
