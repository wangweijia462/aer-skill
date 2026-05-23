import matplotlib.pyplot as plt
import pandas as pd

from common import (
    DATA_DIR,
    model_holdout,
    roc_pr_curves,
    save_figure,
)


def main():
    _, _, mlp_test, mlp_metrics = model_holdout(cutoff_year=2021, estimator="mlp")
    _, _, logit_test, logit_metrics = model_holdout(cutoff_year=2021, estimator="logit")

    y_true = mlp_test["BreakRisk4Q"]
    fpr_mlp, tpr_mlp, prec_mlp, rec_mlp = roc_pr_curves(y_true, mlp_test["pred"])
    fpr_logit, tpr_logit, prec_logit, rec_logit = roc_pr_curves(
        logit_test["BreakRisk4Q"], logit_test["pred"]
    )

    pd.DataFrame([mlp_metrics, logit_metrics]).to_csv(
        DATA_DIR / "figure_2_holdout_metrics.csv", index=False
    )

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), constrained_layout=True)

    axes[0].plot(
        fpr_mlp,
        tpr_mlp,
        color="0.10",
        label=f"Neural network, AUC = {mlp_metrics['auc']:.3f}",
    )
    axes[0].plot(
        fpr_logit,
        tpr_logit,
        color="0.55",
        linestyle="--",
        label=f"Logit benchmark, AUC = {logit_metrics['auc']:.3f}",
    )
    axes[0].plot([0, 1], [0, 1], color="0.75", linewidth=0.8)
    axes[0].set_title("A. ROC curve, 2022-2023 holdout", loc="left")
    axes[0].set_xlabel("False positive rate")
    axes[0].set_ylabel("True positive rate")
    axes[0].legend(frameon=False, loc="lower right")

    axes[1].plot(
        rec_mlp,
        prec_mlp,
        color="0.10",
        label=f"Neural network, AP = {mlp_metrics['average_precision']:.3f}",
    )
    axes[1].plot(
        rec_logit,
        prec_logit,
        color="0.55",
        linestyle="--",
        label=f"Logit benchmark, AP = {logit_metrics['average_precision']:.3f}",
    )
    axes[1].axhline(y_true.mean(), color="0.75", linewidth=0.8)
    axes[1].set_title("B. Precision-recall curve", loc="left")
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].legend(frameon=False, loc="lower left")

    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(color="0.90", linewidth=0.6)
        ax.set_axisbelow(True)

    save_figure(fig, "fig2_prediction_curves")


if __name__ == "__main__":
    main()
