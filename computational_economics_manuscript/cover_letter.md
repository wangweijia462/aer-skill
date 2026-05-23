# Cover Letter — Submission to *Computational Economics*

---

Wang Weijia  
School of Economics and Finance  
Xi'an Jiaotong University  
18522704823@163.com

**[Date]**

Editorial Office  
*Computational Economics*  
Springer Nature

---

Dear Editors,

I am pleased to submit the manuscript titled **"Neural Network Stability and
Horizon-Dependent Prediction of Climate-Induced Supply Chain Risk: Evidence
from Chinese Listed Firms"** for consideration in *Computational Economics*.

## Summary

This paper studies whether neural networks can reliably predict climate-induced
supply-chain disruption risk among Chinese listed firms. Using a 4,188
customer-quarter panel from mandatory disclosures of Chinese A-share firms
(2011–2023), I apply a neural-network stability diagnostic framework and
document three principal findings.

1. **Horizon-dependent predictability.** A two-hidden-layer MLP achieves AUC
   0.668 for one-quarter disruption and 0.656 for two-quarter disruption, but
   only 0.536 for the four-quarter target. The AUC decline reflects a
   progressive loss of feature informativeness as managerial adaptation and
   supplier substitution erode the predictive content of observable variables—
   not instability in the network's learned parameters.

2. **Structural stability.** Normalized Frobenius parameter distances remain
   consistently below the 95th-percentile null threshold (maximum distance
   0.490 vs. threshold 1.534), certifying structural stability independently
   of predictive accuracy. The model converges to a consistent representation
   of the prediction problem even as training data grow.

3. **Feature informativeness is the binding constraint.** Model comparison
   (5 classifiers), feature-group ablation, and architecture sensitivity tests
   jointly show that no alternative configuration materially exceeds AUC 0.544
   for the four-quarter target. The bottleneck is the observable feature set,
   not model capacity.

## Fit with *Computational Economics*

The paper directly addresses the journal's scope in three ways:

- It applies machine-learning methods (neural networks, permutation importance,
  risk-surface visualization) to an economically important prediction problem.
- It proposes and validates a computationally grounded stability diagnostic
  that is general enough to apply to other economic forecasting settings.
- It provides a calibrated, honest treatment of model limitations, showing
  how stability diagnostics remain informative when predictive accuracy is
  modest—a pattern likely common in economic risk prediction tasks with
  unmeasured relationship-specific determinants.

## Declarations

The manuscript has not been previously published and is not currently under
review elsewhere. All data and code used in the study are included in the
replication package. No funds, grants, or other support were received during
the preparation of this manuscript. The author has no competing interests to
disclose.

I look forward to receiving your decision.

Sincerely,

Wang Weijia  
School of Economics and Finance  
Xi'an Jiaotong University  
18522704823@163.com
