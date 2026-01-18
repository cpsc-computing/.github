# WARP Workflow Rules
## Constraint-Projected State Computing (CPSC)

This file defines the **authoritative workflow, rules, and expectations**
for all human and AI-assisted work in this repository.

All contributors, including automated agents, MUST follow this document.

---

## 1. Purpose

The purpose of this repository is to maintain **authoritative specifications**
for Constraint-Projected State Computing (CPSC) and its related formats,
interfaces, and reference guidance.

This repository is **spec-first**, not implementation-first.

The specification is the source of truth.

---

## 2. Spec-First Rule (Non-Negotiable)

All work MUST follow this order:

1. Specification
2. Validation
3. Examples
4. Implementations
5. Tooling

No implementation, demo, or example may:
- contradict the specification
- extend semantics beyond the specification
- redefine behavior not specified in the spec

If ambiguity is discovered:
- STOP
- Propose a spec clarification
- Update the spec
- Then proceed

---

## 3. Normative vs Non-Normative Content

The repository distinguishes content types:

### Normative (Authoritative)
Located under:
- `specification/`

Includes:
- CPSC-Specification.md
- CAS-YAML-Specification.md
- Binary-Format-Specification.md
- Binary-Format-RTL-Mapping.md

Normative content:
- MUST be precise
- MUST be deterministic
- MUST avoid implementation bias
- MUST use RFC-style “MUST / SHOULD / MAY” language

### Non-Normative (Informational / Examples)
Located under:
- `examples/`
- `docs/`
- `fpga/`

Non-normative content:
- MUST reference the spec
- MUST NOT redefine semantics
- MAY be illustrative or incomplete

---

## 4. Change Control

All changes to normative documents MUST:

1. Clearly state intent
2. Identify affected sections
3. Preserve backward compatibility where possible
4. Explicitly document breaking changes
5. Increment document version if semantics change

Large changes SHOULD be discussed before implementation.

---

## 5. Agent Usage Policy

Automated agents are permitted and encouraged,
but they MUST operate under strict constraints.

All agents MUST:
- Follow the spec-first rule
- Treat specifications as authoritative
- Avoid inventing semantics
- Avoid filling gaps with assumptions
- Ask for clarification when ambiguity exists

Agents MUST NOT:
- Introduce new concepts without spec changes
- Rewrite specs for convenience
- Optimize away declared constraints
- Merge normative and non-normative content

---

## 6. Planning Requirements for Agents

All non-trivial agent work MUST begin with a **plan**.

A valid plan:
- Enumerates tasks
- Identifies affected documents
- States assumptions
- Declares intended outputs

Plans MUST be reviewed before execution for:
- scope
- correctness
- alignment with repository goals

---

## 7. Agent Task Lists

Agents SHOULD use explicit task lists for complex work.

Task lists SHOULD:
- Break work into atomic steps
- Reference specific files
- Distinguish between draft and final outputs

Completed tasks MUST be marked clearly.

---

## 8. Agent Profiles and Permissions

Agent capabilities MUST be scoped using profiles.

Profiles SHOULD restrict:
- write access to normative specs
- ability to introduce new concepts
- authority to resolve ambiguities

Default agent posture:
- Conservative
- Spec-respecting
- Minimal inference

---

## 9. Licensing Awareness

All contributors and agents MUST respect:

- The CPSC Research & Evaluation License
- Explicit non-commercial restrictions
- Reserved patent rights

Agents MUST NOT:
- Suggest relicensing
- Imply open-source status
- Remove or weaken license notices

---

## 10. Conflict Resolution

If conflicts arise between:
- examples and spec → spec wins
- implementation and spec → spec wins
- agent output and spec → spec wins

When in doubt:
- Pause
- Escalate
- Clarify in the spec

---

## 11. Reference

Agent behavior and workflow guidelines are further defined in:

- `AGENTS.md`

---

## 12. Summary

This repository prioritizes:
- correctness over speed
- clarity over convenience
- authority over novelty

The specification is law.
