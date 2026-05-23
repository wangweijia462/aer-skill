from pathlib import Path
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyreadstat
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


warnings.filterwarnings("ignore", category=ConvergenceWarning)

WORKSPACE = Path(__file__).resolve().parents[3]
OUT_DIR = WORKSPACE / "output" / "nn_supply_chain_figures"
FIG_DIR = OUT_DIR / "figures"
DATA_DIR = OUT_DIR / "data"
for directory in (FIG_DIR, DATA_DIR):
    directory.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "Affected",
    "S_FC",
    "Affected_x_S_FC",
    "Climate_CityC",
    "C_Size",
    "C_Lev",
    "C_Inv",
    "C_Ppe",
    "C_Firmage",
    "C_Board",
    "C_Occupy",
    "C_Indep",
    "C_Frequency",
    "C_Duration",
    "year_c",
    "quarter_sin",
    "quarter_cos",
]

FEATURE_LABELS = {
    "Affected": "Climate-finance exposure",
    "S_FC": "Supplier financing constraint",
    "Affected_x_S_FC": "Exposure x supplier constraint",
    "Climate_CityC": "Customer-city climate shock",
    "C_Size": "Customer size",
    "C_Lev": "Customer leverage",
    "C_Inv": "Customer inventory",
    "C_Ppe": "Customer fixed assets",
    "C_Firmage": "Customer age",
    "C_Board": "Board size",
    "C_Occupy": "Shareholder tunneling",
    "C_Indep": "Independent directors",
    "C_Frequency": "Trading frequency",
    "C_Duration": "Relationship duration",
    "year_c": "Calendar year",
    "quarter_sin": "Quarter sine",
    "quarter_cos": "Quarter cosine",
}


def set_aer_style():
    mpl.rcParams.update(
        {
            "figure.figsize": (6.8, 4.2),
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "lines.linewidth": 1.5,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


set_aer_style()


def find_dta(name_tokens):
    candidates = [
        path
        for path in WORKSPACE.rglob("*.dta")
        if all(token in path.name for token in name_tokens)
    ]
    if not candidates:
        raise FileNotFoundError(f"No Stata file matches tokens: {name_tokens}")
    candidates.sort(key=lambda path: (len(path.parts), len(str(path))))
    return candidates[0]


def stata_yq_to_year_quarter(yq_series):
    yq = yq_series.astype(int)
    year = 1960 + (yq // 4)
    quarter = (yq % 4) + 1
    return year, quarter


def load_reorganization_data():
    path = find_dta(["14_", "15_"])
    raw, meta = pyreadstat.read_dta(str(path))
    ter_cols = sorted(
        [column for column in raw.columns if column.startswith("Ter_q_q")],
        key=lambda column: int(column.split("q")[-1]),
    )
    interaction = [
        column
        for column in raw.columns
        if column.startswith("Affected") and column != "Affected"
    ][0]

    data = raw.dropna(subset=ter_cols).copy()
    data["BreakRisk4Q"] = (data[ter_cols].sum(axis=1) > 0).astype(int)
    data["year"], data["quarter"] = stata_yq_to_year_quarter(data["yq"])
    data["year_c"] = data["year"] - data["year"].min()
    data["quarter_sin"] = np.sin(2 * np.pi * data["quarter"] / 4)
    data["quarter_cos"] = np.cos(2 * np.pi * data["quarter"] / 4)
    data["Affected_x_S_FC"] = data[interaction]
    data = data.dropna(subset=FEATURES + ["BreakRisk4Q"]).sort_values(
        ["year", "quarter", "C_ID"]
    )
    data.attrs["source_file"] = str(path)
    data.attrs["ter_cols"] = ter_cols
    data.attrs["interaction_col"] = interaction
    data.attrs["variable_labels"] = dict(zip(meta.column_names, meta.column_labels))
    return data


def make_mlp(seed=42):
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "model",
                MLPClassifier(
                    hidden_layer_sizes=(12, 6),
                    activation="relu",
                    alpha=0.01,
                    learning_rate_init=0.003,
                    max_iter=1500,
                    early_stopping=True,
                    validation_fraction=0.15,
                    n_iter_no_change=30,
                    random_state=seed,
                ),
            ),
        ]
    )


def make_logit():
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, solver="lbfgs")),
        ]
    )


def model_holdout(cutoff_year=2021, estimator="mlp", seed=42):
    data = load_reorganization_data()
    train = data[data["year"] <= cutoff_year]
    test = data[data["year"] > cutoff_year]
    model = make_mlp(seed) if estimator == "mlp" else make_logit()
    model.fit(train[FEATURES], train["BreakRisk4Q"])
    pred = model.predict_proba(test[FEATURES])[:, 1]
    metrics = {
        "estimator": estimator,
        "cutoff_year": cutoff_year,
        "n_train": len(train),
        "n_test": len(test),
        "auc": roc_auc_score(test["BreakRisk4Q"], pred),
        "average_precision": average_precision_score(test["BreakRisk4Q"], pred),
        "brier": brier_score_loss(test["BreakRisk4Q"], pred),
        "observed_rate": test["BreakRisk4Q"].mean(),
        "mean_predicted_rate": pred.mean(),
    }
    result = test.copy()
    result["pred"] = pred
    result["residual"] = result["BreakRisk4Q"] - result["pred"]
    return model, train, result, metrics


def rolling_oos_predictions(start_cutoff=2018, end_cutoff=2022, seed=42):
    data = load_reorganization_data()
    pieces = []
    metrics = []
    for cutoff in range(start_cutoff, end_cutoff + 1):
        train = data[data["year"] <= cutoff]
        test = data[data["year"] == cutoff + 1]
        if len(test) < 50 or train["BreakRisk4Q"].nunique() < 2:
            continue
        if test["BreakRisk4Q"].nunique() < 2:
            continue
        model = make_mlp(seed)
        model.fit(train[FEATURES], train["BreakRisk4Q"])
        pred = model.predict_proba(test[FEATURES])[:, 1]
        part = test.copy()
        part["pred"] = pred
        part["residual"] = part["BreakRisk4Q"] - part["pred"]
        part["train_cutoff"] = cutoff
        pieces.append(part)
        metrics.append(
            {
                "train_cutoff": cutoff,
                "eval_year": cutoff + 1,
                "n_train": len(train),
                "n_test": len(test),
                "auc": roc_auc_score(test["BreakRisk4Q"], pred),
                "brier": brier_score_loss(test["BreakRisk4Q"], pred),
                "observed_rate": test["BreakRisk4Q"].mean(),
                "mean_predicted_rate": pred.mean(),
            }
        )
    return pd.concat(pieces, ignore_index=True), pd.DataFrame(metrics)


def parameter_vector(model):
    mlp = model.named_steps["model"]
    arrays = list(mlp.coefs_) + list(mlp.intercepts_)
    return np.concatenate([array.ravel() for array in arrays])


def normalized_distance(model_a, model_b, reference_model):
    vec_a = parameter_vector(model_a)
    vec_b = parameter_vector(model_b)
    vec_ref = parameter_vector(reference_model)
    return np.linalg.norm(vec_a - vec_b) / max(np.linalg.norm(vec_ref), 1e-12)


def stability_diagnostics(reference_year=2018, last_cutoff=2022, seed=42):
    data = load_reorganization_data()
    reference_train = data[data["year"] <= reference_year]
    reference_model = make_mlp(seed)
    reference_model.fit(reference_train[FEATURES], reference_train["BreakRisk4Q"])

    null_distances = []
    for null_seed in range(seed + 1, seed + 21):
        null_model = make_mlp(null_seed)
        null_model.fit(reference_train[FEATURES], reference_train["BreakRisk4Q"])
        null_distances.append(
            normalized_distance(null_model, reference_model, reference_model)
        )
    threshold = float(np.quantile(null_distances, 0.95))

    rows = []
    for cutoff in range(reference_year, last_cutoff + 1):
        train = data[data["year"] <= cutoff]
        test = data[data["year"] == cutoff + 1]
        if len(test) < 50 or test["BreakRisk4Q"].nunique() < 2:
            continue
        model = make_mlp(seed)
        model.fit(train[FEATURES], train["BreakRisk4Q"])
        pred = model.predict_proba(test[FEATURES])[:, 1]
        rows.append(
            {
                "train_cutoff": cutoff,
                "eval_year": cutoff + 1,
                "n_train": len(train),
                "n_test": len(test),
                "distance_to_reference": normalized_distance(
                    model, reference_model, reference_model
                ),
                "null_q95": threshold,
                "auc": roc_auc_score(test["BreakRisk4Q"], pred),
                "brier": brier_score_loss(test["BreakRisk4Q"], pred),
            }
        )
    null = pd.DataFrame({"distance": null_distances})
    diagnostics = pd.DataFrame(rows)
    return diagnostics, null


def roc_pr_curves(y_true, pred):
    fpr, tpr, _ = roc_curve(y_true, pred)
    precision, recall, _ = precision_recall_curve(y_true, pred)
    return fpr, tpr, precision, recall


def save_figure(fig, stem):
    pdf_path = FIG_DIR / f"{stem}.pdf"
    png_path = FIG_DIR / f"{stem}.png"
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight")
    plt.close(fig)
    return pdf_path, png_path
