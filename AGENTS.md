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

## 12. Version control workflows (non-normative)

When a user explicitly requests that changes be staged, committed, and pushed (for
example by issuing commands such as `push to git`, `push to vc`, or `commit and push`),
agents MAY execute the necessary version control commands on the user's behalf,
subject to the following constraints:

- Agents MUST operate only within the current repository context and MUST NOT attempt
to push unrelated repositories.
- Agents SHOULD perform any repository-specific "save session" behavior first if such
a convention exists (for example, appending a ledger entry describing the current
work and its status).
- Agents SHOULD then:
  - inspect the current VCS status;
  - stage only the changes that are relevant to the requested task;
  - construct a concise, honest commit message describing the work; and
  - include a `Co-Authored-By: Warp <agent@warp.dev>` line in the commit message when
the agent has materially contributed to the edits being committed.
- Agents SHOULD push to the repository's default remote and branch (for example,
`origin/main`) unless the user has specified a different target.
- If the pending changes are unexpectedly broad, touch normative specifications
without a clear plan, or appear to include unrelated work, agents SHOULD summarize the
situation and request explicit confirmation before committing.

These behaviors are non-normative and do not change the meaning of any specification
or patent document; they exist solely to streamline repository hygiene when the user
has already decided to save and publish the current state.

---

## 13. Save/load session chat commands (non-normative)

When a user issues explicit session-management commands, agents SHOULD treat them as
high-level orchestration hints around the version control workflows above:

- `save session` – update any relevant README/usage docs for the current work scope
  (for example, documenting new scripts or flows in `README.md`, `WARP.md`, and
  `AGENTS.md` as appropriate), then stage and commit those changes locally **without**
  pushing. The commit MUST still include a `Co-Authored-By: Warp <agent@warp.dev>` line
  when the agent has materially contributed.
- `save session and push` – perform the same documentation and commit steps as
  `save session`, and then push the resulting commit(s) to the default remote/branch
  (for example `origin/main`) unless the user specifies otherwise.
- `load session` – pull or fetch and checkout the current default branch tip
  (for example `git pull` on the active branch) and summarize any relevant changes
  that affect the current task context.
- `pull and load session` – explicitly update the local repository from the default
  remote (for example `git pull origin main`) and then treat the result as a fresh
  session state, summarizing any changes for the user.

These commands are non-normative and do not alter specification semantics; they exist
purely to codify expected agent behavior around saving, restoring, and synchronizing
work sessions.

---

## 14. Summary

Agents are tools to support rigor, not shortcuts around it.

Respect the spec.
Respect the process.
Ask when uncertain.
