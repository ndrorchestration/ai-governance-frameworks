import subprocess
import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
VALIDATOR = os.path.join(ROOT, 'tools', 'validators', 'row_validator.py')
SAMPLE = os.path.join(ROOT, 'artifacts', 'synthetic_to_real_bootstrap_samples.csv')


def test_row_validator_runs():
    # Run validator; expect exit code 0 (pass) on current synthetic sample file
    proc = subprocess.run([sys.executable, VALIDATOR, '--sample-rows', SAMPLE], cwd=ROOT)
    assert proc.returncode == 0, f"Validator failed with exit code {proc.returncode}"
