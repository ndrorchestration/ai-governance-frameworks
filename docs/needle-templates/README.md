# Needle Templates — NIST AI RMF & ISO 42001 Implementation Artifacts

This directory contains one file per Needle.app workflow template, each mapping
the template to its specific NIST AI RMF controls and ISO 42001 clauses.

These templates are the **runnable implementation layer** of formal AI governance
obligations. They are cross-referenced to the DGAF NDR Pattern Registry and
ratified via the Apogee Attestation Gate (P-30).

## Templates

| ID | Template | NIST AI RMF | ISO 42001 | File |
|---|---|---|---|---|
| NT-01 | Evaluate LLM Output Quality | GOVERN 1.7, MEASURE 2.5 | §8.4 | [NT-01.md](NT-01.md) |
| NT-02 | Generate Grounded KB Answers | MANAGE 2.2 | §8.4 | [NT-02.md](NT-02.md) |
| NT-03 | KB Answer With Quality Check | MEASURE 2.9 | §9.1 | [NT-03.md](NT-03.md) |
| NT-04 | Define AI Governance Specification | GOVERN 1.7 | §6.1, §9.1 | [NT-04.md](NT-04.md) |

## Governance Traceability

- **NDR Pattern Registry:** [DGAF-Framework/docs/needle/TEMPLATE_REGISTRY.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/needle/TEMPLATE_REGISTRY.md)
- **Machine-readable cross-reference:** [DGAF-Framework/docs/ndr_patterns_unified.json](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/ndr_patterns_unified.json)
- **Attestation gate:** NDR P-30 (Apogee Attestation Gate)
