#!/usr/bin/env python3
"""
Row validator for Policy-to-Testable-Artifact Pipeline (Phase A)
Validates:
 - scoring_rubric_v1.json against scoring_rubric_schema.json
 - topology_agnostic_benchmark_tasks_v1.json against tasks_schema.json
 - dual_quality_evaluation_schema.csv (parses expected fields)
 - synthetic_to_real_bootstrap_samples.csv rows: presence, types, enums, process_score computation, task_id reference, decision_path sanity

Exit code 0 on success, non-zero on failure.
"""

import sys
import json
import csv
import math
import os
from jsonschema import validate, ValidationError
from dateutil.parser import parse as parse_date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ARTIFACTS = os.path.join(ROOT, 'artifacts')
VALIDATORS = os.path.join(ROOT, 'tools', 'validators')

RUBRIC_FILE = os.path.join(ARTIFACTS, 'scoring_rubric_v1.json')
TASKS_FILE = os.path.join(ARTIFACTS, 'topology_agnostic_benchmark_tasks_v1.json')
SCHEMA_DEF_FILE = os.path.join(ARTIFACTS, 'dual_quality_evaluation_schema.csv')
SAMPLE_ROWS_FILE = os.path.join(ARTIFACTS, 'synthetic_to_real_bootstrap_samples.csv')

RUBRIC_SCHEMA = os.path.join(VALIDATORS, 'scoring_rubric_schema.json')
TASKS_SCHEMA = os.path.join(VALIDATORS, 'tasks_schema.json')

TOL = 1e-6

KEYWORDS = ["authority", "veto", "escalat", "log", "decision", "deny", "deny", "blocked", "executed"]

errors = []

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_json(instance, schema_path, name):
    try:
        with open(schema_path, 'r', encoding='utf-8') as s:
            schema = json.load(s)
        validate(instance=instance, schema=schema)
        print(f"[OK] {name} conforms to schema {os.path.basename(schema_path)}")
        return True
    except ValidationError as e:
        errors.append(f"Schema validation error in {name}: {e.message}")
        return False
    except Exception as e:
        errors.append(f"Unexpected error validating {name}: {e}")
        return False


def parse_schema_def(path):
    fields = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Expect columns: field_name,data_type,description,category,required,example,validation_rule
            for r in reader:
                fields.append(r['field_name'])
        return fields
    except Exception as e:
        errors.append(f"Failed to parse schema definition CSV: {e}")
        return []


def parse_tasks_ids(path):
    try:
        tasks = load_json(path)
        ids = [t['task_id'] for t in tasks.get('tasks', [])]
        return set(ids)
    except Exception as e:
        errors.append(f"Failed to parse tasks file for ids: {e}")
        return set()


def safe_float(x):
    try:
        return float(x)
    except:
        return None


def validate_row(row, field_order, task_ids, row_no):
    # Check required fields (we'll read required flag from schema def by inspecting header file -- simplified: assume required as per v1 schema)
    required_fields = [
        'task_id','class','topology','valid_issue_detected','correctness_score','safety_pass',
        'authority_compliance','veto_integrity','logging_completeness','escalation_correctness',
        'process_score','risk_class','decision_path','data_source','evaluator_id','created_timestamp','final_status'
    ]
    for f in required_fields:
        if f not in row or row[f] == '':
            errors.append(f"Row {row_no}: missing required field '{f}'")
    # task_id exists
    if row.get('task_id') not in task_ids:
        errors.append(f"Row {row_no}: task_id '{row.get('task_id')}' not found in tasks set")
    # numeric ranges
    dims = ['authority_compliance','veto_integrity','logging_completeness','escalation_correctness']
    dim_vals = []
    for d in dims:
        v = safe_float(row.get(d, ''))
        if v is None:
            errors.append(f"Row {row_no}: {d} is not a float: '{row.get(d)}'")
        else:
            if not (0.0 <= v <= 1.0):
                errors.append(f"Row {row_no}: {d}={v} out of range [0.0,1.0]")
            dim_vals.append(v)
    proc = safe_float(row.get('process_score',''))
    if proc is None:
        errors.append(f"Row {row_no}: process_score is not a float: '{row.get('process_score')}'")
    else:
        if dim_vals:
            mean = sum(dim_vals)/len(dim_vals)
            if not (math.isclose(mean, proc, rel_tol=0, abs_tol=1e-4)):
                errors.append(f"Row {row_no}: process_score {proc} does not match mean(dimensions) {mean:.4f}")
    # correctness_score range
    cs = safe_float(row.get('correctness_score',''))
    if cs is None or not (0.0 <= cs <= 1.0):
        errors.append(f"Row {row_no}: correctness_score invalid: '{row.get('correctness_score')}'")
    # enums
    if row.get('data_source') not in ['synthetic','real_run','benchmark']:
        errors.append(f"Row {row_no}: data_source must be one of [synthetic, real_run, benchmark], got '{row.get('data_source')}'")
    if row.get('final_status') not in ['executed','blocked','escalated','waiting','error']:
        errors.append(f"Row {row_no}: final_status must be one of [executed,blocked,escalated,waiting,error], got '{row.get('final_status')}'")
    if row.get('risk_class') not in ['low','medium','high','critical']:
        errors.append(f"Row {row_no}: risk_class must be one of [low,medium,high,critical], got '{row.get('risk_class')}'")
    # decision_path sanity: non-empty and contains at least one keyword
    dp = row.get('decision_path','') or ''
    if dp.strip() == '':
        errors.append(f"Row {row_no}: decision_path is empty")
    else:
        lowered = dp.lower()
        if not any(k in lowered for k in KEYWORDS):
            errors.append(f"Row {row_no}: decision_path may be insufficiently descriptive (no keywords found)")
    # timestamp parse
    try:
        parse_date(row.get('created_timestamp'))
    except Exception:
        errors.append(f"Row {row_no}: created_timestamp is not valid ISO 8601: '{row.get('created_timestamp')}'")


def main():
    # Validate JSON artifacts
    try:
        rubric = load_json(RUBRIC_FILE)
        tasks = load_json(TASKS_FILE)
    except Exception as e:
        print(f"Failed to load artifact JSONs: {e}")
        sys.exit(2)

    ok1 = validate_json(rubric, RUBRIC_SCHEMA, os.path.basename(RUBRIC_FILE))
    ok2 = validate_json(tasks, TASKS_SCHEMA, os.path.basename(TASKS_FILE))

    # Parse schema def for expected columns
    field_order = parse_schema_def(SCHEMA_DEF_FILE)
    if not field_order:
        print("Failed to parse schema definition; aborting row validation")
        sys.exit(2)

    task_ids = parse_tasks_ids(TASKS_FILE)

    # Validate sample rows
    try:
        with open(SAMPLE_ROWS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # normalize header keys to match schema field_names
            header = reader.fieldnames
            for i, r in enumerate(reader, start=1):
                # ensure keys exist for new schema fields; if absent, add empty
                for fld in field_order:
                    if fld not in r:
                        r[fld] = ''
                validate_row(r, field_order, task_ids, i)
    except Exception as e:
        errors.append(f"Failed to validate sample rows CSV: {e}")

    if errors:
        print("Validation completed with errors:")
        for e in errors:
            print(" - ", e)
        sys.exit(3)
    else:
        print("All validations passed.")
        sys.exit(0)

if __name__ == '__main__':
    main()
