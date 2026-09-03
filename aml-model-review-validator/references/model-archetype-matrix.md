# Model Archetype Validation Matrix

Use this file after classifying the model.

## A. Transaction Monitoring Rule / Scenario

Primary questions:
- What red flag / typology / behavioural risk is the scenario intended to identify?
- Is the logical construct reasonably capable of detecting it?
- Is the population complete?
- Are the threshold and lookback window justified?
- What risk sits below the threshold?
- How much overlap exists with other scenarios?

Core tests:
- rule logic reperformance,
- population reconciliation,
- threshold sensitivity,
- below-the-line sampling,
- known-case backtest,
- historical alert yield,
- alert-to-case / SAR/SMR conversion,
- overlap analysis,
- alert concentration by segment/product,
- change in output over time,
- typology mapping.

Red flags:
- threshold chosen only to match analyst capacity,
- no below-the-line testing,
- no evidence for lookback window,
- exclusion list not governed,
- scenario fires mainly on one low-risk segment,
- typology mapping exists only at a generic label level,
- duplicated alerts across scenarios.

## B. Supervised AML Detection / Alert Prioritisation

Primary questions:
- What is the label and how reliable is it?
- Does the sample preserve point-in-time integrity?
- Does the model add value over a baseline?
- Is performance stable OOT?
- Does ranking suppress meaningful risk?
- Are investigators given usable explanations?

Core tests:
- target/label review,
- leakage tests,
- temporal split review,
- feature review,
- baseline comparison,
- PR-AUC,
- precision/recall,
- lift,
- precision@K / recall@K,
- capacity curve,
- temporal OOT,
- segment results,
- calibration if applicable,
- drift,
- SHAP/reason-code testing,
- ablation/sensitivity,
- production parity.

Red flags:
- random split on temporally dependent observations,
- SAR features constructed after the investigation date,
- "non-SAR" treated as confirmed negative,
- class weighting/oversampling applied before train-test split,
- evaluation only on resampled data,
- ROC-AUC/Gini used as sole evidence,
- feature importance without business/typology rationale,
- no analysis of suppressed alerts.

## C. Unsupervised / Anomaly / Clustering

Primary questions:
- What makes an anomaly financially-crime-relevant?
- Are clusters stable and interpretable?
- Does the model find risk not already captured?
- Is expert review sufficiently independent?

Core tests:
- preprocessing/scaling,
- stability across seeds/time,
- hyperparameter sensitivity,
- cluster/anomaly size,
- enrichment against independent risk indicators,
- investigator sampling,
- novel-case analysis,
- overlap with existing controls,
- feature contribution,
- concentration,
- production reproducibility.

Red flags:
- anomaly score equated with suspiciousness,
- no expert validation,
- no stability testing,
- outputs dominated by data errors,
- clusters defined by trivial size/volume effects,
- tuning based on desired alert volume only.

## D. Customer Risk Rating / Entity Risk Scoring

Primary questions:
- Does the methodology appropriately reflect customer ML/TF risk?
- Are factors, weights, thresholds, overrides, and missing-data rules justified?
- Are higher-risk attributes treated coherently?
- Are ratings stable but responsive to meaningful change?

Core tests:
- factor mapping to risk assessment,
- weight review,
- monotonicity/reasonableness,
- rating distribution,
- migration,
- sensitivity,
- missing/default handling,
- override frequency,
- override direction,
- concentration,
- retrospective outcome enrichment,
- benchmark comparison,
- implementation reperformance.

Red flags:
- material risk factors omitted without compensating control,
- weights lack rationale,
- missing values default to low risk,
- overrides systematically reduce risk,
- high-risk factor can paradoxically lower total risk,
- risk tiers driven by one factor unintentionally.

## E. Segmentation / Peer Grouping

Primary questions:
- Is segmentation behaviourally meaningful?
- Are groups sufficiently homogeneous and stable?
- Does segmentation improve detection without creating blind spots?

Core tests:
- feature selection,
- scaling,
- sample size,
- stability,
- within/between-group dispersion,
- business interpretability,
- migration,
- edge cases,
- threshold interaction,
- downstream performance by segment.

## F. Screening / Fuzzy Matching / Entity Resolution

Primary questions:
- Can the engine detect relevant variants with acceptable false negatives?
- Are languages, aliases, transliteration and identifiers handled correctly?
- Are threshold and suppression rules governed?

Core tests:
- curated positive test corpus,
- aliases,
- reordered tokens,
- misspellings,
- transliteration,
- non-Latin scripts,
- initials,
- dates of birth,
- identifiers,
- common names,
- threshold sensitivity,
- false-positive burden,
- list ingestion and update latency,
- whitelist/suppression.

## G. Hybrid Monitoring

Break the system into components and validate:
- component soundness,
- interfaces,
- dependency logic,
- combination/ensemble logic,
- suppression/override,
- cumulative risk coverage,
- end-to-end outcomes.

Never validate only the final score while ignoring upstream rules/features or downstream suppression.
