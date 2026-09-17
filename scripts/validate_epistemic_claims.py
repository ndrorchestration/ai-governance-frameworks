#!/usr/bin/env python3
"""Fail closed on known unsupported current-facing Index-11 governance claims."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"EPISTEMIC_CLAIM_FAIL: {message}")


def main() -> int:
    structural = read("docs/structural-alignment/structural-alignment-agentic-architectures.md")
    gate = read("docs/structural-alignment/index-11-governance-gate.md")
    contributing = read("CONTRIBUTING.md")

    for forbidden in ("S-TIER", "Peer-reviewed"):
        require(forbidden not in structural, f"unsupported current claim remains: {forbidden}")

    affirmative_production_claim = re.search(
        r"(?<!not a )(?<!not an )\bproduction-grade governance model\b",
        structural,
        flags=re.IGNORECASE,
    )
    require(
        affirmative_production_claim is None,
        "unsupported affirmative production-grade governance claim remains",
    )

    require("experimental hypothesis" in structural.lower(), "structural mapping is not explicitly experimental")
    require("not independently peer-reviewed" in structural.lower(), "peer-review boundary is missing")

    require("pP = 1/(2 sin(π/11))" in gate, "canonical Platinum Mean definition is missing")
    require("1.774732842" in gate, "canonical Platinum Mean value is missing")
    require("2·sin(π/11) ≈ 0.541196" not in gate, "reciprocal quantity is still mislabeled as Platinum Mean")
    require("does not establish" in gate, "mathematical identity is not bounded from behavioral validity")
    require("experimental threshold" in gate.lower(), "heuristic threshold is not explicitly experimental")

    require(
        "DGAF (Dynamic Governance Assurance Framework)" not in contributing,
        "CONTRIBUTING still presents obsolete DGAF expansion as current",
    )
    require(
        "DGAF (Dynamic Governance Agentic Formation)" in contributing,
        "CONTRIBUTING does not use canonical current DGAF expansion",
    )
    require(
        "21% constraint compliance improvement" not in contributing,
        "unsupported 21% constraint-compliance performance claim remains current-facing",
    )
    require(
        "**Framework lineage:** Dynamic Governance Assurance Framework (DGAF)" not in gate,
        "Index-11 gate still presents obsolete DGAF expansion as current framework lineage",
    )
    require(
        "Dynamic Governance Assurance Framework" not in gate or "historical" in gate.lower(),
        "obsolete DGAF expansion is not explicitly historical if retained",
    )

    print("EPISTEMIC_CLAIM_HYGIENE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
