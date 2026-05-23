# Neural Network Stability and Climate-Induced Supply Chain Disruption Risk

Replication archive for the *Computational Economics* submission.

## Repository Structure

```
aer-skill/
├── computational_economics_manuscript/
│   ├── manuscript.tex          # Main LaTeX manuscript
│   ├── references.bib          # BibTeX references
│   ├── appendix_code/          # Replication scripts (A–E)
│   └── appendix_data/          # Output CSV files from scripts
├── nn_supply_chain_figures/
│   ├── code/
│   │   ├── common.py           # Shared data loading and utilities
│   │   └── *.py                # Figure generation scripts
│   ├── data/                   # Input CSV files (pre-computed from .dta)
│   └── figures/                # Output PDF figures
└── requirements.txt
```

## Data Requirements

The replication scripts require the original Stata data file from
[original2024climate]. Place the `.dta` file at the path specified in
`nn_supply_chain_figures/code/common.py` (the `DATA_PATH` variable near the
top of that file).

The `appendix_data/` directory already contains the output of Appendix A
(`appendix_a_bootstrap_ci.csv`), which is computed from pre-saved rolling
predictions and does not require the `.dta` file.

## Installation

```bash
pip install -r requirements.txt
```

## Reproducing All Results

After placing the `.dta` file at the correct path, run the five replication
scripts in sequence from the repository root:

```bash
python computational_economics_manuscript/appendix_code/appendix_a_bootstrap_ci.py
python computational_economics_manuscript/appendix_code/appendix_b_model_comparison.py
python computational_economics_manuscript/appendix_code/appendix_c_ablation.py
python computational_economics_manuscript/appendix_code/appendix_d_horizons.py
python computational_economics_manuscript/appendix_code/appendix_e_architecture.py
```

Each script writes output to `computational_economics_manuscript/appendix_data/`.

## Random Seeds

| Component | Seed |
|---|---|
| Main MLP (primary holdout and rolling) | 42 |
| Stability null distribution | 43–62 |
| Bootstrap resampling (Appendix A) | 0 |
| Architecture sensitivity (Appendix E) | 42 |

## Figures

Figures are pre-generated and stored in `nn_supply_chain_figures/figures/`.
To regenerate figures, run the scripts in `nn_supply_chain_figures/code/`.

## Compiling the Manuscript

The manuscript uses `\graphicspath{{../nn_supply_chain_figures/figures/}}`.
Compile from the `computational_economics_manuscript/` directory:

```bash
cd computational_economics_manuscript
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

## Key Results (for verification)

| Configuration | Horizon | AUC |
|---|---|---|
| MLP (12,6) | 4 quarters | 0.536 |
| Logistic regression | 4 quarters | 0.544 |
| MLP (12,6) | 1 quarter | 0.668 |
| MLP (12,6) | 2 quarters | 0.656 |
| Stability max distance | — | 0.490 |
| Stability null threshold | — | 1.534 |
