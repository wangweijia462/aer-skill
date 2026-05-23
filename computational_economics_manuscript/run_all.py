"""
run_all.py – reproduce all appendix tables in sequence.

Place the original Stata data file at the path specified in
appendix_code/common.py before running this script.

Usage:
    python computational_economics_manuscript/run_all.py
"""

import subprocess
import sys
import pathlib

REPO = pathlib.Path(__file__).resolve().parent
CODE = REPO / "appendix_code"

scripts = [
    CODE / "appendix_a_bootstrap_ci.py",
    CODE / "appendix_b_model_comparison.py",
    CODE / "appendix_c_ablation.py",
    CODE / "appendix_d_horizons.py",
    CODE / "appendix_e_architecture.py",
]

for script in scripts:
    print(f"\n{'='*60}")
    print(f"Running {script.name}")
    print('='*60)
    result = subprocess.run([sys.executable, str(script)], check=False)
    if result.returncode != 0:
        print(f"ERROR: {script.name} exited with code {result.returncode}")
        sys.exit(result.returncode)

print("\nAll scripts completed. Results written to appendix_data/")
print("\nKey values to verify:")
print("  appendix_b: MLP AUC = 0.536, Logit AUC = 0.544")
print("  appendix_d: H=1 MLP AUC = 0.668, H=2 MLP AUC = 0.656")
print("  appendix_e: AUC range = 0.529--0.557")
