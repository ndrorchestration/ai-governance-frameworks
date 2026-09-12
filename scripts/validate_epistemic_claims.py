#!/usr/bin/env python3
"""Fail closed on known unsupported current-facing Index-11 governance claims."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"EPISTEMIC_CLAIM_FAIL: {message}")


def main() -> int:
    structural = read("docs/structural-alignment/structural-alignment-agentic-architectures.md")
    gate = read("docs/structural-alignment/index-11-governance-gate.md")

    for forbidden in ("S-TIER", "Peer-reviewed", "production-grade governance model"):
        require(forbidden not in structural, f"unsupported current claim remains: {forbidden}")

    require("experimental hypothesis" in structural.lower(), "structural mapping is not explicitly experimental")
    require("not independently peer-reviewed" in structural.lower(), "peer-review boundary is missing")

    require("pP = 1/(2 sin(π/11))" in gate, "canonical Platinum Mean definition is missing")
    require("1.774732842" in gate, "canonical Platinum Mean value is missing")
    require("2·sin(π/11) ≈ 0.541196" not in gate, "reciprocal quantity is still mislabeled as Platinum Mean")
    require("does not establish" in gate, "mathematical identity is not bounded from behavioral validity")
    require("experimental threshold" in gate.lower(), "heuristic threshold is not explicitly experimental")

    print("EPISTEMIC_CLAIM_HYGIENE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
