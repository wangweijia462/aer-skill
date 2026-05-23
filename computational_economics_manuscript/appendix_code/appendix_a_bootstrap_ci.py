"""
Appendix A – Bootstrap confidence intervals for rolling-window AUC and AP.

Input:  nn_supply_chain_figures/data/figure_3_rolling_predictions.csv
        nn_supply_chain_figures/data/figure_2_holdout_metrics.csv
Output: computational_economics_manuscript/appendix_data/appendix_a_bootstrap_ci.csv

This script runs on the already-saved rolling predictions; it does NOT
require the original .dta file.
"""

import pathlib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

REPO = pathlib.Path(__file__).resolve().parents[2]
ROLLING_CSV = REPO / "nn_supply_chain_figures" / "data" / "figure_3_rolling_predictions.csv"
HOLDOUT_CSV = REPO / "nn_supply_chain_figures" / "data" / "figure_2_holdout_metrics.csv"
OUT_DIR = REPO / "computational_economics_manuscript" / "appendix_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(seed=0)
N_BOOT = 1000


def bootstrap_metrics(y_true, y_pred, n_boot=N_BOOT, rng=RNG):
    """Return dict of point estimates and 95 % bootstrap CIs."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
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

    auc_pt = roc_auc_score(y_true, y_pred)
    ap_pt = average_precision_score(y_true, y_pred)
    brier_pt = brier_score_loss(y_true, y_pred)
    return {
        "n": n,
        "auc": auc_pt,
        "auc_lo": float(np.percentile(aucs, 2.5)),
        "auc_hi": float(np.percentile(aucs, 97.5)),
        "ap": ap_pt,
        "ap_lo": float(np.percentile(aps, 2.5)),
        "ap_hi": float(np.percentile(aps, 97.5)),
        "brier": brier_pt,
        "brier_lo": float(np.percentile(briers, 2.5)),
        "brier_hi": float(np.percentile(briers, 97.5)),
        "obs_rate": float(y_true.mean()),
    }


def main():
    df = pd.read_csv(ROLLING_CSV)

    rows = []
    for cutoff in sorted(df["train_cutoff"].unique()):
        sub = df[df["train_cutoff"] == cutoff].copy()
        eval_year = int(sub["year"].iloc[0])
        m = bootstrap_metrics(sub["BreakRisk4Q"], sub["pred"])
        rows.append({"window": f"{int(cutoff)}->{eval_year}", "train_cutoff": int(cutoff),
                     "eval_year": eval_year, **m})

    # Combined rolling holdout (2022 + 2023) as approximation for main holdout CI
    holdout_sub = df[df["year"].isin([2022, 2023])].copy()
    if len(holdout_sub) > 0 and len(holdout_sub["BreakRisk4Q"].unique()) > 1:
        m = bootstrap_metrics(holdout_sub["BreakRisk4Q"], holdout_sub["pred"])
        rows.append({"window": "rolling 2022+2023 (approx. holdout)", "train_cutoff": None,
                     "eval_year": None, **m})

    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "appendix_a_bootstrap_ci.csv", index=False)
    print(out[["window", "n", "auc", "auc_lo", "auc_hi",
               "ap", "ap_lo", "ap_hi", "brier", "brier_lo", "brier_hi"]].to_string(index=False))


if __name__ == "__main__":
    main()
