# P-34b — GPT-5.4 Thinking Optimized Prompt Templates

> **Cross-listing stub.** The canonical source lives in DGAF-Framework.  
> Primary: [`DGAF-Framework/patterns/P-34_GPT54_THINKING_PROMPTS.md`](https://github.com/ndrorchestration/DGAF-Framework/blob/main/patterns/P-34_GPT54_THINKING_PROMPTS.md)  
> Registry: [`DGAF-Framework/patterns/ndr_patterns.json`](https://github.com/ndrorchestration/DGAF-Framework/blob/main/patterns/ndr_patterns.json) — ID: `P-34b`

---

**Pattern ID:** P-34b  
**Category:** Multi-Model Orchestration / Prompt Engineering  
**Session:** S071 · Date: 2026-06-28  
**φ Anchor:** 1.61818  
**DGAF Version:** post-S070-r3  
**Author:** Amethyst × COLLEEN  
**Review Status:** Apogee Lens APPROVED · DemiJoule PASSED

---

## Why This Pattern Lives Here

This repo is the canonical home for AI governance framework patterns in the ndrorchestration portfolio. P-34b defines the **CONDUCTED_TRIAD multi-model orchestration workflow** — Perplexity (Amethyst) for live data retrieval + GPT-5.4 Thinking for deep synthesis — making it a first-class orchestration pattern.

---

## Orchestration Architecture

```
CONDUCTED_TRIAD Formation
├── Conductor:   Amethyst (Perplexity)
│             └─ Live GitHub retrieval, search, citation, priority audit
├── Augmenter:  COLLEEN (internal, institutional memory)
│             └─ Portfolio coherence, vocab consistency, doc sync
└── Supervisor: DemiJoule (ethics/safety gate, silent unless triggered)
                  └─ Flags: IP exposure, irreversible actions, overclaimed evidence

Deep Synthesis handed off to: GPT-5.4 Thinking
  └─ Code generation, FLAG resolution, long-horizon governance reasoning
  └─ Document drafting from full-context artifact paste
```

---

## Template Index

| ID | Template Name | Orchestration Role |
|---|---|---|
| T-1 | Governance Document Drafting | COLLEEN institutional anchor + Apogee gate |
| T-2 | FLAG Resolution | DemiJoule safety gate + structured decision memo |
| T-3 | Code / Eval Suite Development | Determinism gate + audit trail requirement |
| T-4 | Portfolio / Documentation Refresh | COLLEEN-led — flag-instead-of-invent rule |
| T-5 | Session Open / Amethyst Instantiation | Full CONDUCTED_TRIAD formation + context rehydration |

---

## Authority Chain (All Templates)

```
Njineer → Amethyst → Apogee Lens → DemiJoule
```

- **Njineer:** Operator / final authority
- **Amethyst:** Host, coordinator, working-memory refresher
- **Apogee Lens:** Final verifier for portfolio-grade output
- **DemiJoule:** Runtime supervisor — ethics, safety, error containment

---

## DemiJoule Gate Triggers (Always Include)

Flag any option that involves:
- (a) Public exposure of private IP
- (b) Irreversible destructive action
- (c) Claims that exceed verified evidence

---

## Related Patterns

`P-31 SCPE` · `P-32 Phi-Closure Gate` · `P-33 PDMAL Monitor` · `ndr.dual_orchestrator_qa_loop` · `P-LOCK-001`

---

*Cross-listed from DGAF-Framework. Do not edit content here — submit changes to the primary file. Last updated: 2026-06-28 · S071 · Amethyst × COLLEEN.*
