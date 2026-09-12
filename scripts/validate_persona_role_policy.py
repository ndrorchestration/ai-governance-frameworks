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

    xref = read("patterns/P-34b_GPT54_THINKING_PROMPTS_XREF.md")
    require("Current functional interpretation" in xref, "P-34b cross-list lacks current functional interpretation")
    require("role.governance-orchestrator" in xref, "P-34b cross-list lacks governance coordination role")
    require("role.evidence-verification-reviewer" in xref, "P-34b cross-list lacks evidence review role")
    require("role.constraint-qa-auditor" in xref, "P-34b cross-list lacks constraint review role")
    require("Historical cross-listing snapshot" in xref, "P-34b cross-list does not preserve dated persona content as historical provenance")
    require("does not modify the primary DGAF pattern" in xref, "P-34b local projection does not bound DGAF authority")

    snapshot = read("ECOSYSTEM_STATE.md")
    require("Snapshot-era role labels" in snapshot, "historical snapshot boundary must remain explicit")

    print("PERSONA_ROLE_POLICY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
