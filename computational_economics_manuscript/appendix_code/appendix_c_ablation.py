"""
Appendix C – Feature-group ablation on 2022-2023 holdout.

Trains MLP and Logit on subsets of features (climate, finance, supply-chain,
governance) and the full set; reports AUC, AP, Brier.

Requires the original Stata file.
Output: computational_economics_manuscript/appendix_data/appendix_c_ablation.csv
"""

import pathlib, sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "nn_supply_chain_figures" / "code"))
from common import load_reorganization_data, make_mlp, make_logit  # noqa: E402

OUT_DIR = REPO / "computational_economics_manuscript" / "appendix_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CUTOFF = 2021

FEATURE_GROUPS = {
    "Climate only":       ["Affected", "Climate_CityC", "Affected_x_S_FC"],
    "Supply chain only":  ["S_FC", "C_Duration"],
    "Finance only":       ["C_Size", "C_Lev", "C_Inv", "C_Ppe", "C_Firmage"],
    "Governance only":    ["C_Board", "C_Indep", "C_Occupy", "C_Frequency"],
    "Climate + Finance":  ["Affected", "Climate_CityC", "Affected_x_S_FC",
                           "C_Size", "C_Lev", "C_Inv", "C_Ppe", "C_Firmage"],
    "All features":       ["Affected", "S_FC", "Affected_x_S_FC", "Climate_CityC",
                           "C_Size", "C_Lev", "C_Inv", "C_Ppe", "C_Firmage",
                           "C_Board", "C_Occupy", "C_Indep", "C_Frequency",
                           "C_Duration", "year_c", "quarter_sin", "quarter_cos"],
}


def run_one(X_train, y_train, X_test, y_test, estimator="mlp"):
    model = make_mlp() if estimator == "mlp" else make_logit()
    model.fit(X_train, y_train)
    pred = model.predict_proba(X_test)[:, 1]
    return {
        "auc":   roc_auc_score(y_test, pred),
        "ap":    average_precision_score(y_test, pred),
        "brier": brier_score_loss(y_test, pred),
    }


def main():
    data = load_reorganization_data()
    train = data[data["year"] <= CUTOFF]
    test  = data[data["year"] >  CUTOFF]
    y_train, y_test = train["BreakRisk4Q"], test["BreakRisk4Q"]

    rows = []
    for group_name, feats in FEATURE_GROUPS.items():
        for est in ("mlp", "logit"):
            m = run_one(train[feats], y_train, test[feats], y_test, est)
            rows.append({"feature_group": group_name, "n_features": len(feats),
                         "estimator": est, **m})
            print(f"{group_name:25s}  {est:5s}  AUC={m['auc']:.3f}  AP={m['ap']:.3f}")

    pd.DataFrame(rows).to_csv(OUT_DIR / "appendix_c_ablation.csv", index=False)


if __name__ == "__main__":
    main()
