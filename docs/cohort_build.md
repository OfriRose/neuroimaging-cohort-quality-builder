# Cohort construction

Phase 2 separates source preservation from cohort eligibility. Raw and staging
retain all 1,112 records. `int_participant_quality` exposes each inclusion rule as
a boolean; `base_cohort` applies the rules; and `cohort_exclusions` records every
failed rule. Optional IQ and behavioural measures do not affect eligibility.

## Site-held-out assignment

`UM_1` and `PITT` are reserved for evaluation. They were selected before any
modeling because they provide two independent sites, a useful evaluation size
(167 of 1,111 eligible participants, 15.0%), and near-balanced diagnostic groups
(85 ASD and 82 controls). All other sites are assigned to training. Participants
are never randomly split within a site.

## Phase 2 result

- Raw/staging: 1,112 participants
- Base cohort: 1,111 participants
- Excluded: subject `51078` from NYU, because age at scan is 6.47 and therefore
  outside the specified 7–64 range
- Training: 944 participants across 18 sites
- Evaluation: 167 participants across 2 sites

These counts describe cohort construction only and carry no clinical interpretation.

