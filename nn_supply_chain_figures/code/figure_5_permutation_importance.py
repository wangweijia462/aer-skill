import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import permutation_importance

from common import (
    DATA_DIR,
    FEATURE_LABELS,
    FEATURES,
    model_holdout,
    save_figure,
)


def main():
    model, _, test, metrics = model_holdout(cutoff_year=2021, estimator="mlp")
    result = permutation_importance(
        model,
        test[FEATURES],
        test["BreakRisk4Q"],
        scoring="roc_auc",
        n_repeats=50,
        random_state=42,
    )
    importance = pd.DataFrame(
        {
            "feature": FEATURES,
            "label": [FEATURE_LABELS.get(feature, feature) for feature in FEATURES],
            "mean_auc_loss": result.importances_mean,
            "sd_auc_loss": result.importances_std,
            "holdout_auc": metrics["auc"],
        }
    ).sort_values("mean_auc_loss", ascending=False)
    importance.to_csv(DATA_DIR / "figure_5_permutation_importance.csv", index=False)
    plot_data = importance.head(10).sort_values("mean_auc_loss")

    fig, ax = plt.subplots(figsize=(5.6, 3.6), constrained_layout=True)
    ax.barh(
        plot_data["label"],
        plot_data["mean_auc_loss"],
        xerr=1.96 * plot_data["sd_auc_loss"],
        color="0.35",
        edgecolor="0.15",
        linewidth=0.5,
        error_kw={"ecolor": "0.10", "linewidth": 0.8, "capsize": 2},
    )
    ax.axvline(0, color="0.65", linewidth=0.8)
    ax.set_title("Permutation importance in the 2022-2023 holdout", loc="left")
    ax.set_xlabel("Decrease in AUC when permuted")
    ax.grid(axis="x", color="0.90", linewidth=0.6)
    ax.set_axisbelow(True)

    save_figure(fig, "fig5_permutation_importance")


if __name__ == "__main__":
    main()
