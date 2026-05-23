# Cover Letter — Submission to *Computational Economics*

---

**[Date]**

Editorial Office  
*Computational Economics*  
Springer Nature

---

Dear Editors,

We are pleased to submit our manuscript, **"Neural Network Stability and
Climate-Induced Supply Chain Disruption Risk: Evidence from Chinese Listed
Firms,"** for consideration for publication in *Computational Economics*.

## Summary of the Paper

This paper applies neural network methodology and a formal model-stability
diagnostic framework to the prediction of climate-induced supply chain
disruption risk using a panel of 4,188 customer-quarter observations from
Chinese A-share listed firms (2011–2023).

The prediction target is a four-quarter forward-looking binary indicator
(*BreakRisk4Q*) that captures whether a customer firm terminates at least one
major supplier relationship within the next twelve months.  We train a
two-hidden-layer multilayer perceptron (MLP) classifier on 17 firm-level,
relationship-level, and climate features, and evaluate its performance against
a logistic regression benchmark using a temporal holdout design.

Our central empirical contributions are:

1. **Honest reporting of predictive performance.** The MLP achieves holdout
   AUC of 0.536 across the 2022–2023 test period, comparable to logistic
   regression (AUC = 0.544), reflecting strong heterogeneity in supply-chain
   disruption outcomes that static observable variables cannot fully capture.
   Rolling one-year-ahead evaluations confirm that modest but positive
   discriminative power (AUC 0.516–0.578) is a structural feature of the
   prediction environment.

2. **Formal model-stability certification.** Adapting the normalized
   parameter-distance framework to this domain, we show that successive MLP
   parameter vectors remain consistently below the 95th-percentile null
   threshold generated from same-sample random-seed perturbations (maximum
   observed distance 0.49 vs.\ threshold 1.53 across five rolling windows).
   This structural stability can be certified independently of predictive
   accuracy, providing a necessary condition for reliable deployment.

3. **Economically interpretable results.** Permutation importance analysis
   identifies customer size, seasonal timing, and customer age as dominant
   predictors, with climate-finance exposure contributing a modest but
   positive signal.  Risk-surface analysis uncovers a nonlinear interaction
   between climate-finance exposure and supplier financing constraints,
   with qualitatively different risk profiles at high and low constraint
   levels that linear models cannot represent.

## Fit with *Computational Economics*

We believe this paper is well suited to *Computational Economics* for the
following reasons.

- **Computational method as the core contribution.** The paper proposes and
  validates a computationally grounded evaluation protocol (parameter-distance
  stability diagnostics, rolling out-of-sample design, permutation importance,
  risk-surface visualization) that is general enough to be applied to other
  machine-learning applications in economics and finance.

- **Neural network modeling in an economic context.** The paper demonstrates
  how neural network architectures can be deployed for forward-looking economic
  risk assessment, with explicit attention to the properties required for
  operational reliability: stability, calibration, and interpretability.

- **Honest treatment of model limitations.** Rather than overstating
  predictive performance, we frame limited accuracy as an informative finding
  about the data-generating process, and we show how stability diagnostics
  provide meaningful information even when accuracy is modest.  This
  calibrated approach to machine-learning evaluation is particularly relevant
  for the growing literature on computational methods in economic risk
  assessment.

- **Reproducibility.** All figures and statistics are generated from a Python
  codebase applied to the Stata replication data of the underlying supply-chain
  study; no simulated outcome data are used.

## Relation to Existing Literature

The paper builds on and extends three literatures.  It applies the neural
network stability framework of [stability reference] to a supply-chain climate
risk setting, complementing the machine-learning asset-pricing work of Gu,
Kelly, and Xiu (2020, *Review of Financial Studies*).  It connects to the
supply-chain disruption literature (Carvalho et al., 2021, *Quarterly Journal
of Economics*; Hendricks and Singhal, 2005, *Production and Operations
Management*) by providing a prediction-oriented counterpart to the causal
identification work.  And it contributes to the climate-finance literature
(Battiston et al., 2017, *Nature Climate Change*; Giglio, Kelly, and Stroebel,
2021, *Annual Review of Financial Economics*) by linking climate-finance
exposure to firm-level supply-chain outcomes in an emerging market.

## Declarations

The manuscript has not been previously published, is not currently under
review elsewhere, and all authors approve submission to *Computational
Economics*.  The data and code used in the study are available from the
authors upon reasonable request.

We hope you will find this contribution of interest to the readers of
*Computational Economics*.  We look forward to receiving your decision.

Sincerely,

[Author Names]  
[Affiliation]  
[Email]  
[Date]
