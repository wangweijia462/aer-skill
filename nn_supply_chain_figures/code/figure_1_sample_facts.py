import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd

from common import DATA_DIR, load_reorganization_data, save_figure


def main():
    data = load_reorganization_data()
    annual = (
        data.groupby("year")
        .agg(
            observations=("BreakRisk4Q", "size"),
            break_risk=("BreakRisk4Q", "mean"),
            affected=("Affected", "mean"),
            climate_city=("Climate_CityC", "mean"),
        )
        .reset_index()
    )
    annual.to_csv(DATA_DIR / "figure_1_sample_facts.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), constrained_layout=True)

    colors = ["0.35" if n >= 50 else "0.78" for n in annual["observations"]]
    axes[0].bar(
        annual["year"],
        annual["break_risk"],
        width=0.75,
        color=colors,
        edgecolor="0.15",
        linewidth=0.5,
    )
    axes[0].set_title("A. Realized four-quarter disruption risk", loc="left")
    axes[0].set_ylabel("Share of customer-quarters")
    axes[0].set_xlabel("Base year")
    axes[0].set_ylim(0, max(0.85, annual["break_risk"].max() * 1.15))
    axes[0].set_xticks(annual["year"][::2])
    axes[0].legend(
        handles=[
            Patch(facecolor="0.35", edgecolor="0.15", label="N >= 50"),
            Patch(facecolor="0.78", edgecolor="0.15", label="N < 50"),
        ],
        frameon=False,
        loc="upper right",
    )

    axes[1].plot(
        annual["year"],
        annual["climate_city"],
        color="0.10",
        marker="o",
        markersize=3,
        label="Customer-city climate shock",
    )
    axes[1].plot(
        annual["year"],
        annual["affected"],
        color="0.55",
        linestyle="--",
        marker="s",
        markersize=3,
        label="Climate-finance exposure",
    )
    axes[1].set_title("B. Climate exposure in the prediction sample", loc="left")
    axes[1].set_ylabel("Sample mean")
    axes[1].set_xlabel("Base year")
    axes[1].set_xticks(annual["year"][::2])
    axes[1].legend(frameon=False, loc="upper right")

    for ax in axes:
        ax.grid(axis="y", color="0.88", linewidth=0.6)
        ax.set_axisbelow(True)

    save_figure(fig, "fig1_sample_facts")


if __name__ == "__main__":
    main()
