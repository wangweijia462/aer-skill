"""
Appendix D – Alternative forecast horizons (q+1 through q+4).

Constructs BreakRiskHQ = 1{sum_{h=1}^{H} Ter_q_qh > 0} for H in {1,2,3,4}
and reports MLP + Logit holdout AUC, AP, Brier for each horizon.

Requires the original Stata file.
Output: computational_economics_manuscript/appendix_data/appendix_d_horizons.csv
"""

import pathlib, sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "nn_supply_chain_figures" / "code"))
from common import load_reorganization_data, make_mlp, make_logit, FEATURES  # noqa: E402

OUT_DIR = REPO / "computational_economics_manuscript" / "appendix_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CUTOFF = 2021


def build_target(data, n_quarters):
    ter_cols = data.attrs["ter_cols"][:n_quarters]
    return (data[ter_cols].sum(axis=1) > 0).astype(int)


def main():
    data = load_reorganization_data()
    train_full = data[data["year"] <= CUTOFF]
    test_full  = data[data["year"] >  CUTOFF]

    rows = []
    for H in [1, 2, 3, 4]:
        y_train = build_target(train_full, H)
        y_test  = build_target(test_full, H)
        obs_rate = float(y_test.mean())
        if y_train.nunique() < 2 or y_test.nunique() < 2:
            print(f"H={H}: insufficient class diversity, skipping")
            continue
        for est, make_fn in [("mlp", make_mlp), ("logit", make_logit)]:
            model = make_fn()
            model.fit(train_full[FEATURES], y_train)
            pred = model.predict_proba(test_full[FEATURES])[:, 1]
            rows.append({
                "horizon_quarters": H,
                "estimator": est,
                "n_train": len(train_full),
                "n_test":  len(test_full),
                "obs_rate": obs_rate,
                "auc":   roc_auc_score(y_test, pred),
                "ap":    average_precision_score(y_test, pred),
                "brier": brier_score_loss(y_test, pred),
            })
            print(f"H={H}  {est:5s}  obs_rate={obs_rate:.3f}  "
                  f"AUC={rows[-1]['auc']:.3f}")

    pd.DataFrame(rows).to_csv(OUT_DIR / "appendix_d_horizons.csv", index=False)


if __name__ == "__main__":
    main()
