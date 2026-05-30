#!/usr/bin/env python3
"""
Row validator for Policy-to-Testable-Artifact Pipeline (Phase A)

Enhancements (best practices applied):
 - CLI with argparse for flexible inputs
 - Structured logging
 - JSON/markdown report output option
 - Exit codes standardized
 - Additional checks: row_id UUID pattern, stricter decision_path template checks
 - Testability: returns exit codes for test harness

Usage:
  python tools/validators/row_validator.py \
    --artifacts-path artifacts \
    --validators-path tools/validators \
    --sample-rows artifacts/synthetic_to_real_bootstrap_samples.csv \
    --report report.json

Exit codes:
  0 = success (all validations passed)
  2 = fatal error (IO or schema parse errors)
  3 = validation errors found

"""

from __future__ import annotations
import argparse
import json
import csv
import math
import os
import re
import sys
import logging
from typing import List, Set
from jsonschema import validate, ValidationError
from dateutil.parser import parse as parse_date

# Constants
UUID4_RE = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')
KEYWORDS = ["authority", "veto", "escalat", "log", "decision", "deny", "blocked", "executed"]
TOL = 1e-6

# Setup logging
logger = logging.getLogger("row_validator")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ValidationResult:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def add_error(self, msg: str) -> None:
        logger.debug(f"Error recorded: {msg}")
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        logger.debug(f"Warning recorded: {msg}")
        self.warnings.append(msg)

    def ok(self) -> bool:
        return len(self.errors) == 0


def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_json(instance: object, schema_path: str, name: str, result: ValidationResult) -> bool:
    try:
        with open(schema_path, 'r', encoding='utf-8') as s:
            schema = json.load(s)
        validate(instance=instance, schema=schema)
        logger.info(f"[OK] {name} conforms to schema {os.path.basename(schema_path)}")
        return True
    except ValidationError as e:
        result.add_error(f"Schema validation error in {name}: {e.message}")
        return False
    except Exception as e:
        result.add_error(f"Unexpected error validating {name}: {e}")
        return False


def parse_schema_def(path: str) -> List[str]:
    fields: List[str] = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                fields.append(r['field_name'])
        return fields
    except Exception as e:
        raise RuntimeError(f"Failed to parse schema definition CSV: {e}")


def parse_tasks_ids(path: str) -> Set[str]:
    try:
        tasks = load_json(path)
        ids = {t['task_id'] for t in tasks.get('tasks', [])}
        return ids
    except Exception as e:
        raise RuntimeError(f"Failed to parse tasks file for ids: {e}")


def safe_float(x: str):
    try:
        return float(x)
    except Exception:
        return None


def is_uuid4(s: str) -> bool:
    return bool(UUID4_RE.match(s))


def validate_row(row: dict, field_order: List[str], task_ids: Set[str], row_no: int, result: ValidationResult) -> None:
    # Required fields for v1
    required_fields = [
        'task_id','class','topology','valid_issue_detected','correctness_score','safety_pass',
        'authority_compliance','veto_integrity','logging_completeness','escalation_correctness',
        'process_score','risk_class','decision_path','data_source','evaluator_id','created_timestamp','final_status'
    ]

    for f in required_fields:
        if f not in row or (isinstance(row[f], str) and row[f].strip() == ''):
            result.add_error(f"Row {row_no}: missing required field '{f}'")

    # task_id exists
    tid = row.get('task_id')
    if tid not in task_ids:
        result.add_error(f"Row {row_no}: task_id '{tid}' not found in tasks set")

    # numeric ranges and compute mean
    dims = ['authority_compliance','veto_integrity','logging_completeness','escalation_correctness']
    dim_vals: List[float] = []
    for d in dims:
        v = safe_float(row.get(d, ''))
        if v is None:
            result.add_error(f"Row {row_no}: {d} is not a float: '{row.get(d)}'")
        else:
            if not (0.0 <= v <= 1.0):
                result.add_error(f"Row {row_no}: {d}={v} out of range [0.0,1.0]")
            dim_vals.append(v)

    proc = safe_float(row.get('process_score',''))
    if proc is None:
        result.add_error(f"Row {row_no}: process_score is not a float: '{row.get('process_score')}'")
    else:
        if dim_vals:
            mean = sum(dim_vals)/len(dim_vals)
            if not math.isclose(mean, proc, rel_tol=0, abs_tol=1e-4):
                result.add_error(f"Row {row_no}: process_score {proc} does not match mean(dimensions) {mean:.4f}")

    # correctness_score range
    cs = safe_float(row.get('correctness_score',''))
    if cs is None or not (0.0 <= cs <= 1.0):
        result.add_error(f"Row {row_no}: correctness_score invalid: '{row.get('correctness_score')}'")

    # enums
    if row.get('data_source') not in ['synthetic','real_run','benchmark']:
        result.add_error(f"Row {row_no}: data_source must be one of [synthetic, real_run, benchmark], got '{row.get('data_source')}'")
    if row.get('final_status') not in ['executed','blocked','escalated','waiting','error']:
        result.add_error(f"Row {row_no}: final_status must be one of [executed,blocked,escalated,waiting,error], got '{row.get('final_status')}'")
    if row.get('risk_class') not in ['low','medium','high','critical']:
        result.add_error(f"Row {row_no}: risk_class must be one of [low,medium,high,critical], got '{row.get('risk_class')}'")

    # decision_path sanity: non-empty and contains at least one keyword
    dp = (row.get('decision_path') or '').strip()
    if dp == '':
        result.add_error(f"Row {row_no}: decision_path is empty")
    else:
        lowered = dp.lower()
        if not any(k in lowered for k in KEYWORDS):
            result.add_warning(f"Row {row_no}: decision_path may be insufficiently descriptive (no keywords found)")
        # Enforce minimal template presence: 'task=' or 'authority=' or 'outcome='
        if not any(tok in lowered for tok in ['task=', 'authority=', 'outcome=', 'topology=']):
            result.add_warning(f"Row {row_no}: decision_path does not include expected structured tokens (task=, authority=, topology=, outcome=)")

    # row_id if present should be UUID4
    rid = row.get('row_id','')
    if rid:
        if not is_uuid4(rid):
            result.add_warning(f"Row {row_no}: row_id '{rid}' does not match UUID4 format")

    # timestamp parse
    try:
        parse_date(row.get('created_timestamp'))
    except Exception:
        result.add_error(f"Row {row_no}: created_timestamp is not valid ISO 8601: '{row.get('created_timestamp')}'")


def run_validator(artifacts_path: str, validators_path: str, sample_rows: str, report_path: str | None) -> int:
    result = ValidationResult()

    rubric_file = os.path.join(artifacts_path, 'scoring_rubric_v1.json')
    tasks_file = os.path.join(artifacts_path, 'topology_agnostic_benchmark_tasks_v1.json')
    schema_def_file = os.path.join(artifacts_path, 'dual_quality_evaluation_schema.csv')

    rubric_schema = os.path.join(validators_path, 'scoring_rubric_schema.json')
    tasks_schema = os.path.join(validators_path, 'tasks_schema.json')

    # Load JSON artifacts
    try:
        rubric = load_json(rubric_file)
        tasks = load_json(tasks_file)
    except Exception as e:
        logger.error(f"Failed to load artifact JSONs: {e}")
        return 2

    validate_json(rubric, rubric_schema, os.path.basename(rubric_file), result)
    validate_json(tasks, tasks_schema, os.path.basename(tasks_file), result)

    # Parse schema def
    try:
        field_order = parse_schema_def(schema_def_file)
    except RuntimeError as e:
        logger.error(str(e))
        return 2

    try:
        task_ids = parse_tasks_ids(tasks_file)
    except RuntimeError as e:
        logger.error(str(e))
        return 2

    # Validate sample rows
    try:
        with open(sample_rows, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader, start=1):
                # ensure keys exist for new schema fields; if absent, add empty
                for fld in field_order:
                    if fld not in r:
                        r[fld] = ''
                validate_row(r, field_order, task_ids, i, result)
    except FileNotFoundError as e:
        logger.error(f"Sample rows file not found: {e}")
        return 2
    except Exception as e:
        logger.error(f"Failed to validate sample rows CSV: {e}")
        return 2

    # Emit report
    report = {
        'errors': result.errors,
        'warnings': result.warnings,
    }
    if report_path:
        try:
            with open(report_path, 'w', encoding='utf-8') as rf:
                json.dump(report, rf, indent=2)
            logger.info(f"Wrote report to {report_path}")
        except Exception as e:
            logger.warning(f"Failed to write report to {report_path}: {e}")

    # Print summary
    if result.ok():
        logger.info("All validations passed.")
        if result.warnings:
            for w in result.warnings:
                logger.warning(w)
        return 0
    else:
        logger.error("Validation completed with errors:")
        for e in result.errors:
            logger.error(f" - {e}")
        for w in result.warnings:
            logger.warning(f" - {w}")
        return 3


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Validate policy artifacts and sample rows.')
    parser.add_argument('--artifacts-path', default='artifacts', help='Path to artifacts directory')
    parser.add_argument('--validators-path', default='tools/validators', help='Path to validators directory')
    parser.add_argument('--sample-rows', default='artifacts/synthetic_to_real_bootstrap_samples.csv', help='Sample rows CSV file')
    parser.add_argument('--report', default=None, help='Path to write JSON report')
    parser.add_argument('--verbose', action='store_true', help='Enable debug logging')

    args = parser.parse_args(argv)
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    exit_code = run_validator(args.artifacts_path, args.validators_path, args.sample_rows, args.report)
    return exit_code


if __name__ == '__main__':
    code = main()
    sys.exit(code)
