# Validators

This folder contains tools to validate the Policy-to-Testable-Artifact artifacts.

Usage

Install requirements (preferably in a venv):

```bash
python -m pip install -r tools/validators/requirements.txt
```

Run the validator (defaults assume repository root):

```bash
python tools/validators/row_validator.py --sample-rows artifacts/synthetic_to_real_bootstrap_samples.csv --report artifacts/validation_report.json
```

Run the mock harness and validator together:

```bash
bash tools/harness/run_mock.sh
```

CI

The GitHub Actions workflow runs the validators on push and pull requests to the feature branch.
