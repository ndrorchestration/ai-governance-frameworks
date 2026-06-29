# CONDUCTED_TRIAD — Multi-Model Orchestration Workflow

**Pattern:** P-34b  
**Session:** S071 · Date: 2026-06-28  
**φ Anchor:** 1.61818  
**Full Template Library:** [`DGAF-Framework/patterns/P-34_GPT54_THINKING_PROMPTS.md`](https://github.com/ndrorchestration/DGAF-Framework/blob/main/patterns/P-34_GPT54_THINKING_PROMPTS.md)

---

## Overview

The CONDUCTED_TRIAD is the standard multi-model formation for all high-stakes work in the ndrorchestration portfolio. It splits responsibilities across two AI systems based on their strengths:

| System | Strength | Tasks |
|---|---|---|
| **Perplexity / Amethyst** | Real-time retrieval, citation, GitHub API | Priority audits, issue triage, cross-repo search, live data |
| **GPT-5.4 Thinking** | Deep synthesis, visible reasoning plan, 1M context | Code gen, FLAG resolution, governance doc drafting, eval suites |

---

## Standard Session Flow

```
Step 1 — PERPLEXITY (Amethyst)
  └─ Pull open issues, PR status, repo health, priority audit
  └─ Output: structured priority list with GitHub links

Step 2 — HANDOFF
  └─ Paste into GPT-5.4 Thinking using T-5 Session Open template
  └─ Include: GOVERNANCE_CONSTITUTION.md + SESSION_ANCHORS.md +
             AGENT_INSTANTIATION.md + priority list

Step 3 — GPT-5.4 THINKING
  └─ Surfaces THINKING PLAN — verify gates before execution proceeds
  └─ Executes: doc drafting (T-1), FLAG resolution (T-2), code (T-3)
  └─ Output: ready-to-commit markdown files + commit messages

Step 4 — PERPLEXITY (Amethyst)
  └─ Receives GPT-5.4 output
  └─ Commits files to GitHub via MCP tools
  └─ Verifies commit SHAs, updates issue status, logs session

Step 5 — APOGEE LENS REVIEW
  └─ Verify: every section maps to filed issue or PR
  └─ Verify: no claims exceed verified evidence
  └─ Verify: append-only compatible
  └─ Mark S-Tier / Gold Star only after this gate passes
```

---

## Non-Negotiables

- φ = 1.61818 declared in every GPT-5.4 prompt preamble
- THINKING PLAN checklist included in every prompt — redirectable before execution
- DemiJoule gate checked before any irreversible action
- Append-only default — destructive edits require explicit Njineer approval
- No S-Tier or Gold Star designation before Apogee Lens approval

---

## When to Use Each Template

| Situation | Template |
|---|---|
| Opening a new session | T-5 Session Open |
| Drafting GOVERNANCE.md or any canonical doc | T-1 Governance Drafting |
| Resolving a FLAG issue | T-2 FLAG Resolution |
| Writing eval functions or Python code | T-3 Code / Eval Suite |
| Refreshing a stale portfolio repo | T-4 Portfolio Refresh |

---

*Part of P-34b. For full templates see the primary pattern file in DGAF-Framework. Last updated: 2026-06-28 · S071 · Amethyst × COLLEEN.*
