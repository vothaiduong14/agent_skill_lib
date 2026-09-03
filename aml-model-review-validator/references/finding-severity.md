# Finding Severity Framework

Severity is based on risk, not wording.

## Critical
A weakness creates an immediate or pervasive risk that the AML control cannot be relied upon for its intended use, for example:
- material implementation defect causing broad false negatives,
- severe data omission affecting high-risk populations,
- proven leakage invalidating performance evidence for a production ML model,
- control is materially different from approved methodology,
- model is not capable of its stated AML objective and no effective compensating control exists.

Typical conclusion: not fit for intended use or immediate restriction required.

## High
A material weakness could significantly impair risk coverage, reliability, or governance:
- substantial untested below-the-line risk,
- important data lineage/reconciliation failure,
- major OOT degradation with no understood cause,
- material segment blind spot,
- weak label design causing materially overstated performance,
- threshold governance inconsistent with stated risk appetite.

Typical conclusion: conditional use with time-bound remediation, or restriction depending on impact.

## Moderate
A meaningful weakness that does not currently invalidate the model but reduces confidence or control effectiveness:
- incomplete monitoring,
- limited sensitivity analysis,
- incomplete explainability,
- weak change documentation,
- non-material inconsistencies,
- insufficient secondary benchmark testing.

## Low
A control enhancement or documentation weakness with limited current risk.

## Observation / Enhancement
A non-deficiency improvement opportunity.

## Severity factors
Assess:
1. breadth of affected population,
2. high-risk customer/product/geography exposure,
3. false-negative potential,
4. downstream decision impact,
5. duration,
6. detectability,
7. compensating controls,
8. reversibility,
9. regulatory reliance,
10. recurrence / governance weakness.

Do not assign severity solely from the number of affected records.
