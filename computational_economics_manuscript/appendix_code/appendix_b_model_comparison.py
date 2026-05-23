"""
Appendix B – Extended model comparison with bootstrap confidence intervals.

Compares MLP(12,6), Logistic Regression, Random Forest, Gradient Boosting,
Ridge-penalised Logit on the 2022-2023 primary holdout.

Requires:
  - Original Stata file (located by common.load_reorganization_data)
  - scikit-learn >= 1.1

Output: computational_economics_manuscript/appendix_data/appendix_b_model_comparison.csv
"""

import pathlib, sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# ── locate common.py ──────────────────────────────────────────────────────────
REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "nn_supply_chain_figures" / "code"))
from common import load_reorganization_data, make_mlp, FEATURES  # noqa: E402

OUT_DIR = REPO / "computational_economics_manuscript" / "appendix_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(0)
N_BOOT = 1000
CUTOFF = 2021


def make_models():
    return {
        "MLP (12,6)": make_mlp(seed=42),
        "Logit (C=1)": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, solver="lbfgs", C=1.0)),
        ]),
        "Logit ridge (C=0.1)": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, solver="lbfgs", C=0.1)),
        ]),
        "Random Forest (100)": Pipeline([
            ("scaler", StandardScaler()),
            ("model", RandomForestClassifier(n_estimators=100, random_state=42,
                                             n_jobs=-1)),
        ]),
        "Gradient Boosting": Pipeline([
            ("model", HistGradientBoostingClassifier(random_state=42,
                                                     max_iter=300,
                                                     early_stopping=True)),
        ]),
    }


def bootstrap_auc(y_true, y_pred, n_boot=N_BOOT, rng=RNG):
    n = len(y_true)
    aucs, aps, briers = [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        yt, yp = y_true[idx], y_pred[idx]
        if len(np.unique(yt)) < 2:
            continue
        aucs.append(roc_auc_score(yt, yp))
        aps.append(average_precision_score(yt, yp))
        briers.append(brier_score_loss(yt, yp))
    return (float(np.percentile(aucs, 2.5)),  float(np.percentile(aucs, 97.5)),
            float(np.percentile(aps, 2.5)),   float(np.percentile(aps, 97.5)),
            float(np.percentile(briers, 2.5)), float(np.percentile(briers, 97.5)))


def main():
    data = load_reorganization_data()
    train = data[data["year"] <= CUTOFF]
    test  = data[data["year"] >  CUTOFF]
    X_train, y_train = train[FEATURES], train["BreakRisk4Q"]
    X_test,  y_test  = test[FEATURES],  test["BreakRisk4Q"]

    rows = []
    for name, model in make_models().items():
        model.fit(X_train, y_train)
        pred = model.predict_proba(X_test)[:, 1]
        auc  = roc_auc_score(y_test, pred)
        ap   = average_precision_score(y_test, pred)
        brier = brier_score_loss(y_test, pred)
        al, ah, prl, prh, bl, bh = bootstrap_auc(np.asarray(y_test), pred)
        rows.append({"model": name,
                     "n_train": len(train), "n_test": len(test),
                     "auc": auc, "auc_lo": al, "auc_hi": ah,
                     "ap": ap, "ap_lo": prl, "ap_hi": prh,
                     "brier": brier, "brier_lo": bl, "brier_hi": bh,
                     "obs_rate": float(y_test.mean())})
        print(f"{name:30s}  AUC={auc:.3f} [{al:.3f},{ah:.3f}]  "
              f"AP={ap:.3f}  Brier={brier:.3f}")

    pd.DataFrame(rows).to_csv(OUT_DIR / "appendix_b_model_comparison.csv", index=False)


if __name__ == "__main__":
    main()
