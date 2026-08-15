# AI Governance Frameworks

![Status](https://img.shields.io/badge/Status-Experimental-blue?style=flat-square)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)

> **Epistemic status:** Experimental governance/evaluation repository. This project contains mappings, templates, and research artifacts. The presence of a NIST, ISO, IIA, or Paul-Elder reference does not by itself establish certification, compliance, or external endorsement.

## Purpose

This repository explores practical AI-governance mappings and implementation templates, including relationships to NIST AI RMF, ISO/IEC 42001, IIA AI auditing concepts, and critical-thinking methods.

The repository's own artifacts are authoritative for what is implemented. A mapping to an external standard is an interpretive cross-reference unless the referenced standard and the implementation evidence establish more.

## Needle Templates

The `docs/needle-templates/` directory contains workflow-template artifacts intended to map operational tasks to governance controls. Template presence is evidence that the artifact exists; it is not evidence that an external auditor has certified the resulting workflow.

## External-framework boundary

- **NIST AI RMF** — external risk-management framework. This repository may map artifacts to it; such a mapping does not constitute NIST endorsement or compliance certification.
- **ISO/IEC 42001** — external AI management-system standard. Repository artifacts may reference its clauses; certification is a separate organizational and audit process.
- **IIA** — external professional standards/guidance. References should not be represented as IIA approval.
- **Paul-Elder Critical Thinking** — external critical-thinking framework; use of its concepts does not establish formal accreditation.

## Project-local terminology

The repository contains project-local concepts such as the **Index 11 stability gradient** and MAS taxonomy mappings. These should be treated as experimental/project-defined constructs unless a specific mathematical or empirical claim is independently derived and validated.

In particular, metallic-mean constants appearing in an artifact do not, by themselves, establish a mathematically optimal governance architecture or a causal relationship to AI-system stability.

## Validation boundary

Historical badges, certifications, attestation language, benchmark values, or claims such as `100%` risk coverage are not treated as current verified results unless the repository contains the underlying reproducible evidence.

A successful template execution is evidence about that execution; it does not establish organization-wide governance compliance.

## Related ecosystem

This repository may integrate with:

- `DGAF-Framework` — separate governance/evaluation research track
- `ai-prompt-systems-portfolio` — prompt-engineering artifacts
- `Amethyst-Governance-Eval-Stack` — separate evaluation track
- `junior-apogee-app` — separate application/QA track
- `resumeapex-eval` — separate benchmark/evaluation track

Cross-repository references do not establish mutual validation.

## Status

**Active / experimental.**

Before presenting any artifact as certified, compliant, production-ready, or mathematically validated, verify the exact implementation, evidence, external-framework requirements, and current commit.

## License

Apache License 2.0 — see [LICENSE](LICENSE).

## Provenance

Developed by Ndr / Ender Hensel (`ndrorchestration`).
