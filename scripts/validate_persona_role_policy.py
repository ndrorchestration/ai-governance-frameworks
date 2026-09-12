#!/usr/bin/env python3
"""Fail closed when current governance surfaces depend on named-agent authority."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"PERSONA_ROLE_POLICY_FAIL: {message}")


def main() -> int:
    index = read("docs/index.md")
    require("role.governance-orchestrator" in index, "docs index lacks governance role")
    require("role.continuity-archive-coordinator" in index, "docs index lacks continuity role")
    require("**Governance:** Agent" not in index, "docs index still grants governance to a persona")

    triad = read("orchestration/CONDUCTED_TRIAD_WORKFLOW.md")
    require("Research/retrieval lane" in triad, "triad lacks functional retrieval lane")
    require("Evidence verification review" in triad, "triad lacks functional evidence review")
    require("PERPLEXITY (Amethyst)" not in triad, "triad still keys execution to Amethyst persona")
    require("APOGEE LENS REVIEW" not in triad, "triad still keys review to Apogee persona")
    require("DemiJoule gate checked" not in triad, "triad still keys irreversible-action gate to persona")

    gate = read("docs/structural-alignment/index-11-governance-gate.md")
    require("Persona/role authority boundary" in gate, "Index-11 lacks authority boundary")
    require("role.evidence-verification-reviewer" in gate, "Index-11 lacks evidenced evaluation role mapping")
    require("UNRESOLVED" in gate, "Index-11 does not preserve conflicting mappings as unresolved")
    require("COLLEEN activates" not in gate, "Index-11 still grants persona gate authority")
    require("COLLEEN sign-off" not in gate, "Index-11 still grants persona sign-off authority")

    snapshot = read("ECOSYSTEM_STATE.md")
    require("Snapshot-era role labels" in snapshot, "historical snapshot boundary must remain explicit")

    print("PERSONA_ROLE_POLICY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
