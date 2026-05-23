import importlib


FIGURE_MODULES = [
    "figure_1_sample_facts",
    "figure_2_prediction_curves",
    "figure_3_calibration_residuals",
    "figure_4_model_stability",
    "figure_5_permutation_importance",
    "figure_6_risk_surface",
]


def main():
    for module_name in FIGURE_MODULES:
        module = importlib.import_module(module_name)
        module.main()


if __name__ == "__main__":
    main()
