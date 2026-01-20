# Agent Usage and Governance
## CPSC Specification Repository

This document defines how automated agents are used,
configured, and governed within this repository.

It complements `WARP.md` and is binding for all agent activity.

---

## 1. Role of Agents

Agents are assistants, not authors.

Their role is to:
- help draft content
- improve clarity
- check consistency
- propose changes

Final authority always rests with the human maintainer.

---

## 2. Allowed Agent Activities

Agents MAY:
- Draft specification text for review
- Reformat or clarify existing material
- Identify inconsistencies or ambiguities
- Propose alternative wording
- Generate examples explicitly marked as non-normative
- Use external tooling such as MCP servers (for example, USPTO PTAB search) to gather non-normative background information for patent and prior-art review

Agents MUST:
- Preserve existing semantics
- Reference authoritative specs
- Treat external tool output as informational, not normative
- Flag uncertainty explicitly

---

## 3. Prohibited Agent Activities

Agents MUST NOT:
- Introduce new semantics without approval
- Infer missing rules
- Optimize or simplify constraints
- Alter licensing language
- Merge speculative ideas into normative text

---

## 4. Planning Requirement

For any task involving:
- multiple files
- normative specifications
- architectural changes

Agents MUST produce a plan before acting.

Plans MUST include:
- objective
- files affected
- assumptions
- risks

---

## 5. Task Lists

Agents SHOULD use task lists when:
- modifying specifications
- adding new documents
- refactoring content

Task lists SHOULD be explicit and reviewable.

---

## 6. Profiles and Permissions

Agents SHOULD be configured using profiles such as:

- **Spec Drafter**
  - May draft but not finalize specs
- **Reviewer**
  - May analyze and comment
- **Example Generator**
  - Restricted to non-normative folders
- **Implementation Assistant**
  - May not modify specs

Profiles SHOULD restrict write access accordingly.

---

## 7. Determinism and Conservatism

Agents MUST prefer:
- conservative interpretations
- explicit wording
- minimal changes

If ambiguity exists:
- agents MUST stop and ask

---

## 8. Attribution and Transparency

Agent-generated content SHOULD be:
- reviewed
- edited
- attributed where appropriate

This repository values transparency in how content is produced.

---

## 9. Enforcement

Violations of this document may result in:
- reverted changes
- restricted agent access
- workflow updates

---

## 10. Relationship to WARP.md

`WARP.md` defines repository-wide workflow rules.
This document defines **agent-specific behavior**.

Both documents are authoritative.

---

## 11. Patent research workflows (non-normative)

When assisting with patent research, prior-art searches, or landscape analysis, agents MUST:

- Treat all documents under `patents/` as **non-normative legal and planning material**, not specifications.
- Treat all MCP-backed patent tools (including the `patents` MCP server and any PPUBS or PatentSearch/PatentsView endpoints) as **informational**.
- Avoid making legal conclusions or altering normative specifications based on tool output.

When a user issues a chat command beginning with `prior-art protocol:` (see `WARP.md` §14.3), agents SHOULD:

1. Re-read the current non-normative prior-art protocol text under `patents/`.
2. Identify which parts of the protocol are executable given currently configured tools (for example, PPUBS-only if PatentSearch is not yet configured).
3. Run the relevant portions using the `patents` MCP server, staying within the protocol’s scope.
4. Propose a Run ID and capture run metadata (date, trigger, coverage, and conclusion summary) in the chat.
5. If a ledger file such as `LEDGER.md` or a protocol-embedded ledger section exists, append a concise, machine-searchable run entry there, respecting any existing structure.

Recognized non-normative command patterns include (examples, not a closed list):

- `prior-art protocol: start Themes A+B (PPUBS only)`
- `prior-art protocol: extend with PatentSearch`
- `prior-art protocol: status`
- `prior-art protocol: rerun since <reason>`

Agents MUST make clear in their responses which portions of the protocol were executed, which data sources were used (PPUBS vs PatentSearch/PatentsView), and what changes would require a re-run.

---

## 12. Summary

Agents are tools to support rigor, not shortcuts around it.

Respect the spec.
Respect the process.
Ask when uncertain.
