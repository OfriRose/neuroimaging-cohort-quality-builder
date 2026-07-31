# Feature coverage, site shift, and dataset readiness

Phase 3 evaluates whether the constructed cohort is structurally usable and makes
site heterogeneity visible. These reports are descriptive quality audits, not
clinical comparisons or evidence that site effects have been corrected.

## Feature coverage

`feature_coverage` reports availability for DSM-IV code, three IQ measures, ADOS,
SRS, SCQ, AQ, and comorbidity by site, split, and diagnostic group. Coverage is
not an eligibility rule because these fields are optional in the cohort contract.

## Site shift

`site_shift` reports participant count, age, sex mix, diagnostic-group mix, and
full-scale IQ coverage/mean for each site. Difference columns compare each site
with the complete training aggregate. They identify where review is warranted;
they are not hypothesis tests and should not be interpreted causally.

## Readiness definition

`is_structurally_ready` is `true`: the base cohort is non-empty, both site-held-out
splits are non-empty, required fields are complete, both diagnostic groups occur
in each split, and no site crosses splits.

`is_ready_for_behavioral_enrichment_analysis` is `false`. This stricter flag
requires non-zero held-out evaluation coverage for ADOS, SRS, SCQ, AQ, and
comorbidity. Only ADOS meets that requirement; evaluation coverage is zero for
the other four. Structural cohort comparisons remain possible, but claims based
on those behavioral enrichment fields cannot be evaluated on the held-out sites.
