"""
Appendix E – MLP architecture sensitivity.

Trains five MLP architectures on the 2022-2023 primary holdout and computes:
  - Holdout AUC, AP, Brier
  - Normalized parameter distance from (12,6) reference model

Requires the original Stata file.
Output: computational_economics_manuscript/appendix_data/appendix_e_architecture.csv
"""

import pathlib, sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "nn_supply_chain_figures" / "code"))
from common import (load_reorganization_data, FEATURES,     # noqa: E402
                    parameter_vector, normalized_distance)

OUT_DIR = REPO / "computational_economics_manuscript" / "appendix_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CUTOFF = 2021

ARCHITECTURES = {
    "(8,)":      (8,),
    "(12,6)":    (12, 6),   # baseline
    "(16,8)":    (16, 8),
    "(32,16)":   (32, 16),
    "(64,32)":   (64, 32),
}


def make_mlp_arch(hidden, seed=42):
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", MLPClassifier(
            hidden_layer_sizes=hidden,
            activation="relu",
            alpha=0.01,
            learning_rate_init=0.003,
            max_iter=1500,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=30,
            random_state=seed,
        )),
    ])


def main():
    data = load_reorganization_data()
    train = data[data["year"] <= CUTOFF]
    test  = data[data["year"] >  CUTOFF]
    X_train, y_train = train[FEATURES], train["BreakRisk4Q"]
    X_test,  y_test  = test[FEATURES],  test["BreakRisk4Q"]

    # fit baseline (12,6) as reference for distance calculations
    baseline = make_mlp_arch((12, 6))
    baseline.fit(X_train, y_train)

    rows = []
    for name, hidden in ARCHITECTURES.items():
        model = make_mlp_arch(hidden)
        model.fit(X_train, y_train)
        pred  = model.predict_proba(X_test)[:, 1]
        n_params = sum(w.size for w in model.named_steps["model"].coefs_) + \
                   sum(b.size for b in model.named_steps["model"].intercepts_)
        dist = normalized_distance(model, baseline, baseline)
        rows.append({
            "architecture": name,
            "n_params": n_params,
            "auc":    roc_auc_score(y_test, pred),
            "ap":     average_precision_score(y_test, pred),
            "brier":  brier_score_loss(y_test, pred),
            "param_dist_from_baseline": dist,
        })
        print(f"{name:10s}  params={n_params:4d}  AUC={rows[-1]['auc']:.3f}  "
              f"dist={dist:.3f}")

    pd.DataFrame(rows).to_csv(OUT_DIR / "appendix_e_architecture.csv", index=False)


if __name__ == "__main__":
    main()
