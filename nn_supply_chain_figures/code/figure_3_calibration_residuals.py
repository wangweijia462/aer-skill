import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import DATA_DIR, rolling_oos_predictions, save_figure


def autocorrelation(values, max_lag):
    x = np.asarray(values, dtype=float)
    x = x - x.mean()
    denom = np.dot(x, x)
    if denom == 0:
        return np.zeros(max_lag)
    return np.array([np.dot(x[lag:], x[:-lag]) / denom for lag in range(1, max_lag + 1)])


def main():
    predictions, metrics = rolling_oos_predictions(start_cutoff=2018, end_cutoff=2022)
    predictions.to_csv(DATA_DIR / "figure_3_rolling_predictions.csv", index=False)
    metrics.to_csv(DATA_DIR / "figure_3_rolling_metrics.csv", index=False)

    deciles = pd.qcut(predictions["pred"], 10, duplicates="drop")
    calibration = (
        predictions.assign(decile=deciles)
        .groupby("decile", observed=True)
        .agg(
            mean_pred=("pred", "mean"),
            observed=("BreakRisk4Q", "mean"),
            n=("BreakRisk4Q", "size"),
        )
        .reset_index(drop=True)
    )
    calibration.to_csv(DATA_DIR / "figure_3_calibration_bins.csv", index=False)

    quarterly = (
        predictions.groupby("yq")
        .agg(residual=("residual", "mean"), n=("residual", "size"))
        .reset_index()
        .sort_values("yq")
    )
    max_lag = min(8, len(quarterly) - 2)
    acf = autocorrelation(quarterly["residual"], max_lag)
    acf_data = pd.DataFrame({"lag": np.arange(1, max_lag + 1), "acf": acf})
    acf_data.to_csv(DATA_DIR / "figure_3_residual_acf.csv", index=False)
    band = 1.96 / np.sqrt(len(quarterly))

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), constrained_layout=True)

    axes[0].plot([0, 1], [0, 1], color="0.75", linewidth=0.8)
    axes[0].scatter(
        calibration["mean_pred"],
        calibration["observed"],
        s=20 + 2 * np.sqrt(calibration["n"]),
        color="0.15",
        edgecolor="white",
        linewidth=0.5,
        zorder=3,
    )
    axes[0].set_title("A. Calibration, rolling out-of-sample predictions", loc="left")
    axes[0].set_xlabel("Mean predicted risk")
    axes[0].set_ylabel("Observed disruption rate")
    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)

    axes[1].axhspan(-band, band, color="0.90", zorder=0)
    axes[1].axhline(0, color="0.35", linewidth=0.8)
    axes[1].vlines(acf_data["lag"], 0, acf_data["acf"], color="0.25", linewidth=1.2)
    axes[1].scatter(acf_data["lag"], acf_data["acf"], color="0.15", s=18, zorder=3)
    axes[1].set_title("B. Autocorrelation of quarterly mean residuals", loc="left")
    axes[1].set_xlabel("Lag in quarters")
    axes[1].set_ylabel("Autocorrelation")
    axes[1].set_xticks(acf_data["lag"])
    axes[1].set_ylim(-1, 1)

    for ax in axes:
        ax.grid(color="0.90", linewidth=0.6)
        ax.set_axisbelow(True)

    save_figure(fig, "fig3_calibration_residuals")


if __name__ == "__main__":
    main()
