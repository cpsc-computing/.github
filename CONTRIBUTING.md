# Contributing to Constraint-Projected State Computing (CPSC)

Thank you for your interest in contributing to the CPSC specification repository.

This repository is **spec-first** and **governance-driven**.  
All contributions must follow the rules defined here, in `WARP.md`, and in `AGENTS.md`.

---

## 1. Scope of Contributions

This repository accepts contributions in the following areas:

- Clarifications to existing specifications
- Corrections of errors or inconsistencies
- Improvements to wording, structure, or readability
- Non-normative examples and documentation
- Issue reports and design discussions

This repository does **not** accept:
- speculative features without discussion
- implementations that redefine semantics
- changes that bypass the specification process

---

## 2. Normative vs Non-Normative Content

### Normative Content (Authoritative)

Located under:
- `specification/`

Examples:
- CPSC-Specification.md
- CAS-YAML-Specification.md
- Binary-Format-Specification.md
- Binary-Format-RTL-Mapping.md

Changes to normative content are **high-impact** and require a formal process.

---

### Non-Normative Content (Informational)

Located under:
- `examples/`
- `docs/`
- `fpga/`

Non-normative contributions are welcome but:
- MUST reference the specification
- MUST NOT redefine semantics
- MUST be clearly marked as non-normative

---

## 3. Spec-First Contribution Rule

All changes MUST follow this order:

1. Identify or propose a specification change
2. Discuss and document intent
3. Update the specification (if required)
4. Update examples or documentation
5. Implement tooling or demos (if applicable)

If the specification is ambiguous:
- STOP
- Open a proposal issue
- Clarify the spec
- Then proceed

---

## 4. Spec Change Proposals (Required for Normative Changes)

Any change that affects semantics, behavior, or interpretation of CPSC
**MUST** go through the Spec Change Proposal process.

This includes:
- adding or removing fields
- changing constraint semantics
- altering binary layout or ordering
- modifying determinism or execution rules

See: `SPEC-CHANGE-TEMPLATE.md`

---

## 5. Using GitHub Issues

All design discussions and proposals MUST occur via GitHub Issues.

When opening an issue:
- Use the Spec Change Proposal template when applicable
- Clearly state whether the change is normative or non-normative
- Reference specific sections and files

Pull Requests without an associated issue may be closed.

---

## 6. Agent-Assisted Contributions

Agent-assisted contributions are allowed, but:

- Agents MUST follow `AGENTS.md`
- Agents MUST not introduce new semantics
- Human review is always required
- The specification remains authoritative

---

## 7. Licensing and IP

By contributing:
- You agree that contributions are provided under the existing repository license
- You do not receive commercial rights
- You acknowledge that patent rights are reserved

Do not submit content you do not have the right to contribute.

---

## 8. Review and Acceptance

All contributions are reviewed for:
- correctness
- clarity
- alignment with CPSC principles
- impact on determinism and portability

Maintainers may request revisions or reject contributions.

---

## 9. Summary

CPSC prioritizes:
- correctness over speed
- clarity over cleverness
- specification authority over convenience

Thank you for contributing responsibly.
