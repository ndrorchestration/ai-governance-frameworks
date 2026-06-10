# Needle Templates — NIST AI RMF & ISO 42001 Implementation Artifacts

> **Status: ⭐ GOLD STAR CERTIFIED** — All templates verified, P-30 passed, COLLEEN 1-1-1-1 cleared.  
> **Partner Directory:** [needle.app/partners-directory/ndr-ai-orchestration](https://needle.app/partners-directory/ndr-ai-orchestration)

This directory contains one file per Needle.app workflow template, each mapping
the template to its specific NIST AI RMF controls and ISO 42001 clauses.

These templates are the **runnable implementation layer** of formal AI governance
obligations. They are cross-referenced to the DGAF NDR Pattern Registry and
ratified via the Apogee Attestation Gate (P-30).

## Templates

| ID | Template | NIST AI RMF | ISO 42001 | File | Run |
|---|---|---|---|---|---|
| NT-01 | Evaluate LLM Output Quality | GOVERN 1.7, MEASURE 2.5 | §8.4 | [NT-01.md](NT-01.md) | [needle.app →](https://needle.app/workflow-templates/evaluate-ai-output-quality) |
| NT-02 | Generate Grounded KB Answers | MANAGE 2.2 | §8.4 | [NT-02.md](NT-02.md) | [needle.app →](https://needle.app/workflow-templates/generate-grounded-knowledge-base-answers) |
| NT-03 | KB Answer With Quality Check | MEASURE 2.9 | §9.1 | [NT-03.md](NT-03.md) | [needle.app →](https://needle.app/workflow-templates/kb-answer-with-quality-check) |
| NT-04 | Define AI Governance Specification | GOVERN 1.7 | §6.1, §9.1 | [NT-04.md](NT-04.md) | [needle.app →](https://needle.app/workflow-templates/implement-governance-multi-agent-orchestration) |

## Governance Traceability

- **NDR Pattern Registry:** [DGAF-Framework/docs/needle/TEMPLATE_REGISTRY.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/needle/TEMPLATE_REGISTRY.md)
- **Machine-readable cross-reference:** [DGAF-Framework/docs/ndr_patterns_unified.json](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/ndr_patterns_unified.json)
- **Apogee attestation records:** [ai-prompt-systems-portfolio/docs/qa/](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/tree/main/docs/qa)
- **Attestation gate:** NDR P-30 (Apogee Attestation Gate) — PASS, composite avg 0.958
