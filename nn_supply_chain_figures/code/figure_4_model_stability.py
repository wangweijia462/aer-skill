import matplotlib.pyplot as plt

from common import DATA_DIR, save_figure, stability_diagnostics


def main():
    diagnostics, null = stability_diagnostics(reference_year=2018, last_cutoff=2022)
    diagnostics.to_csv(DATA_DIR / "figure_4_stability_diagnostics.csv", index=False)
    null.to_csv(DATA_DIR / "figure_4_same_sample_null_distances.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), constrained_layout=True)

    axes[0].plot(
        diagnostics["train_cutoff"],
        diagnostics["distance_to_reference"],
        color="0.10",
        marker="o",
        markersize=4,
    )
    axes[0].axhline(
        diagnostics["null_q95"].iloc[0],
        color="0.55",
        linestyle="--",
        label="Same-sample seed distance, 95th pct.",
    )
    axes[0].set_title("A. Normalized parameter distance", loc="left")
    axes[0].set_xlabel("Training sample through")
    axes[0].set_ylabel("Distance from 2018 reference model")
    axes[0].legend(frameon=False, loc="lower right")

    axes[1].bar(
        diagnostics["eval_year"],
        diagnostics["auc"],
        color="0.35",
        edgecolor="0.15",
        linewidth=0.5,
        width=0.7,
    )
    axes[1].axhline(0.5, color="0.65", linestyle="--", linewidth=0.8)
    axes[1].set_title("B. One-year-ahead AUC by evaluation year", loc="left")
    axes[1].set_xlabel("Evaluation year")
    axes[1].set_ylabel("AUC")
    axes[1].set_ylim(0.45, max(0.62, diagnostics["auc"].max() + 0.03))

    for ax in axes:
        ax.grid(axis="y", color="0.90", linewidth=0.6)
        ax.set_axisbelow(True)

    save_figure(fig, "fig4_model_stability")


if __name__ == "__main__":
    main()
