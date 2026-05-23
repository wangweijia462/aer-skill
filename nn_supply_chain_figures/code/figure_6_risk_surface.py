import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import DATA_DIR, FEATURES, model_holdout, save_figure


def averaged_predictions(model, base, variable, grid, fixed_values=None):
    rows = []
    for value in grid:
        scenario = base.copy()
        scenario[variable] = value
        if fixed_values:
            for key, fixed_value in fixed_values.items():
                scenario[key] = fixed_value
        if "Affected" in scenario.columns and "S_FC" in scenario.columns:
            scenario["Affected_x_S_FC"] = scenario["Affected"] * scenario["S_FC"]
        pred = model.predict_proba(scenario[FEATURES])[:, 1].mean()
        rows.append({"grid_value": value, "predicted_risk": pred, **(fixed_values or {})})
    return pd.DataFrame(rows)


def main():
    model, train, test, _ = model_holdout(cutoff_year=2021, estimator="mlp")
    base = test[FEATURES].copy()

    affected_grid = np.linspace(0, 1, 41)
    sfc_levels = [0.0, 0.5, 1.0]
    affected_curves = pd.concat(
        [
            averaged_predictions(
                model,
                base,
                "Affected",
                affected_grid,
                fixed_values={"S_FC": sfc},
            ).assign(sfc_level=sfc)
            for sfc in sfc_levels
        ],
        ignore_index=True,
    )

    climate_grid = np.linspace(test["Climate_CityC"].min(), test["Climate_CityC"].max(), 41)
    climate_curve = averaged_predictions(model, base, "Climate_CityC", climate_grid)

    affected_curves.to_csv(DATA_DIR / "figure_6_affected_surface.csv", index=False)
    climate_curve.to_csv(DATA_DIR / "figure_6_climate_curve.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), constrained_layout=True)

    styles = {0.0: ("0.15", "-"), 0.5: ("0.40", "--"), 1.0: ("0.65", "-.")}
    for sfc in sfc_levels:
        subset = affected_curves[affected_curves["sfc_level"] == sfc]
        color, linestyle = styles[sfc]
        axes[0].plot(
            subset["grid_value"],
            subset["predicted_risk"],
            color=color,
            linestyle=linestyle,
            label=f"Supplier constraint = {sfc:g}",
        )
    axes[0].set_title("A. Exposure-supplier constraint risk surface", loc="left")
    axes[0].set_xlabel("Climate-finance exposure")
    axes[0].set_ylabel("Predicted disruption risk")
    axes[0].legend(frameon=False, loc="upper right")

    axes[1].plot(
        climate_curve["grid_value"],
        climate_curve["predicted_risk"],
        color="0.15",
    )
    y_min = climate_curve["predicted_risk"].min() - 0.02
    y_max = climate_curve["predicted_risk"].max() + 0.02
    support = np.quantile(test["Climate_CityC"], np.linspace(0.05, 0.95, 19))
    axes[1].plot(support, np.repeat(y_min, len(support)), "|", color="0.45", markersize=7)
    axes[1].set_title("B. Customer-city climate shock", loc="left")
    axes[1].set_xlabel("Climate shock intensity")
    axes[1].set_ylabel("Predicted disruption risk")
    axes[1].set_ylim(y_min - 0.01, y_max)

    for ax in axes:
        ax.grid(axis="y", color="0.90", linewidth=0.6)
        ax.set_axisbelow(True)

    save_figure(fig, "fig6_risk_surface")


if __name__ == "__main__":
    main()
