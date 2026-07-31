# ABIDE Cohort Specification v0.1

## Goal
Build a reproducible, quality-controlled cohort from multi-site autism
neuroimaging metadata for downstream research or model evaluation.
This project does not diagnose autism and does not train a clinical model.

## Required fields
- SUB_ID
- SITE_ID
- AGE_AT_SCAN
- SEX
- DX_GROUP

## Optional enrichment fields
- DSM_IV_TR
- FIQ, VIQ, PIQ
- ADOS, SRS, SCQ, AQ, COMORBIDITY

## Missing-data rule
Treat blank values and -9999 as missing.

## Initial inclusion criteria
- Unique, non-null SUB_ID
- Non-null SITE_ID
- Age between 7 and 64
- SEX in {1, 2}
- DX_GROUP in {1, 2}

## Cohort strategy
- Keep all eligible participants in the base cohort.
- Do not exclude participants for missing IQ or behavioural scores.
- Report coverage of optional measures by site and diagnostic group.
- Reserve entire sites for evaluation to measure site shift.