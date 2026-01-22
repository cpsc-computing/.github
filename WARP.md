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
- `docs/specification/`

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

## 13. Patent and IP Documents

Patent-related materials for CPSC / CPAC live under `docs/patents/` and are **legal disclosure and planning documents**, not specifications.

Key files:
- `docs/patents/README.md` – overview of patent materials, status, and immutability policy
- `docs/patents/CPSC-CPAC-Provisional-2026-01.md` – draft provisional utility patent application text (pre-filing); once filed, the Markdown and corresponding PDF become immutable
- `docs/patents/executive-summary.md` – high-level business and technical summary of the CPSC / CPAC IP
- `docs/patents/internal-ip-playbook.md` – internal patent strategy, licensing narratives, claim structure, and continuation planning
- `docs/patents/non-provisional-outline.md` – structured outline for the anchor non-provisional patent filing

These documents:
- are **non-normative** and MUST NOT be treated as specifications or implementation requirements
- do **not** override or redefine semantics in `docs/specification/`
- exist to record inventions, support filings, and guide licensing and continuation strategy
- do **not** grant patent rights beyond what is established in actual filed applications and issued patents

This directory is intended for internal IP tracking and planning and should remain private unless disclosure is explicitly required.

## 14. External Patent Tools and MCP Servers

When performing prior-art searches, patent landscape reviews, or PTAB decision analysis, contributors and agents MAY use external services and MCP servers as non-normative inputs.

Supported examples are:

- The USPTO Patent MCP server (`patent_mcp_server`, from riemannzeta), which exposes PPUBS full-text search, ODP, PatentsView, PTAB, Office Action, citation, and litigation tools via a single MCP endpoint; and
- USPTO-backed MCP servers from John Walkoe, which expose programmatic access to PTAB, Patent File Wrapper, Final Petition Decisions, and Enriched Citation APIs via MCP:

  - `uspto_ptab_mcp` – PTAB Open Data v3 (IPR/PGR/CBM proceedings, appeals, decisions)
  - `uspto_pfw_mcp` – Patent File Wrapper (prosecution documents, office actions)
  - `uspto_fpd_mcp` – Final Petition Decisions
  - `uspto_enriched_citation_mcp` – Enriched Citation API v3

To install and update these servers on a development machine, use:

- `scripts/setup-ptab-mcp-for-warp.ps1` – clones or updates the four upstream USPTO MCP repositories under `$env:USERPROFILE` and invokes each repository's `deploy/windows_setup.ps1` (when not run with `-SkipSetup`). Those upstream scripts install dependencies, prompt for USPTO/Mistral API keys, store them securely via Windows DPAPI, and can optionally configure Claude/Warp MCP integration.

Workflow rules for these tools:
- Results from MCP servers and external patent tools are **informational only** and MUST NOT be treated as normative specifications.
- Any conclusions or text derived from such tools MUST be reviewed and, where appropriate, restated in human-authored, spec-aligned language.
- Specifications under `docs/specification/` remain the sole source of normative technical behavior, regardless of external legal or search tools.

### 14.1 Warp MCP JSON configuration examples (Warp / Claude Code)

Warp discovers MCP servers via JSON configuration. For manual configuration of these USPTO MCP servers, use entries of the following form (paths may be adjusted as needed):

**Patent MCP server (`patent_mcp_server` from riemannzeta, PPUBS/ODP/PatentsView/Office Actions/Litigation):**

```json
{
  "patents": {
    "command": "uv",
    "args": [
      "--directory",
      "C:/Users/trist/patent_mcp_server",
      "run",
      "patent-mcp-server"
    ]
  }
}
```

**PTAB MCP (`uspto_ptab_mcp`):**

```json
{
  "uspto_ptab": {
    "command": "uv",
    "args": [
      "--directory",
      "C:/Users/trist/uspto_ptab_mcp",
      "run",
      "ptab-mcp"
    ]
  }
}
```

**Patent File Wrapper MCP (`uspto_pfw_mcp`):**

```json
{
  "uspto_pfw": {
    "command": "uv",
    "args": [
      "--directory",
      "C:/Users/trist/uspto_pfw_mcp",
      "run",
      "patent-filewrapper-mcp"
    ]
  }
}
```

**Final Petition Decisions MCP (`uspto_fpd_mcp`):**

```json
{
  "uspto_fpd": {
    "command": "uv",
    "args": [
      "--directory",
      "C:/Users/trist/uspto_fpd_mcp",
      "run",
      "fpd-mcp"
    ]
  }
}
```
***Enriched Citations MCP (`uspto_enriched_citation_mcp`):**

```json
{
  "uspto_enriched_citations": {
    "command": "uv",
    "args": [
      "--directory",
      "C:/Users/trist/uspto_enriched_citation_mcp",
      "run",
      "uspto-enriched-citation-mcp"
    ]
  }
}
```

### 14.2 PPUBS behavior and reliability notes

The `patents` MCP server (`patent_mcp_server`) depends on the USPTO Patent Public Search (PPUBS) API for search functionality. In practice:

- "by-number" and "by-GUID" lookups (for example, `ppubs_get_patent_by_number` and `ppubs_get_full_document`) currently succeed and can return full text and metadata for known documents (e.g., US 10,000,000).
- Search-style endpoints (for example, `ppubs_search_patents` and `ppubs_search_applications`) may intermittently or persistently return HTTP 500 `INTERNAL_SERVER_ERROR` with an `"Unable to Process"` developer message even for simple queries.

When running prior-art protocols that rely on PPUBS via MCP, treat 500 errors from these search endpoints as an upstream service issue rather than a wiring/config problem, and fall back to PatentsView or the USPTO v3 MCP servers (PTAB, PFW, FPD, Enriched Citations) where possible.

### 14.3 Division of labor: patent_mcp_server vs John Walkoe MCPs

For practical work:

- Use `patent_mcp_server` (the `patents` MCP server) primarily for:
  - PPUBS full-text search and by-number access (when PPUBS is behaving),
  - PatentsView/PatentSearch text and entity search (once the MCP glue is updated),
  - One-stop access to ODP, PTAB, office actions, litigation, and citations when you are comfortable with some fragility.
- Use the John Walkoe MCP servers (`uspto_ptab_mcp`, `uspto_pfw_mcp`, `uspto_fpd_mcp`, `uspto_enriched_citation_mcp`) as the **canonical, task-focused interfaces** for:
  - PTAB trials/appeals (progressive-disclosure search tiers, document workflows),
  - File wrapper / prosecution history (minimal/balanced searches, document-code filtered access to CLM/NOA/CTFR/CTNF/892/IDS/etc.),
  - Final Petition Decisions,
  - Enriched office-action citations and citation neighborhoods.

Agents should therefore prefer the John Walkoe MCPs for structured PTAB/prosecution/citation workflows (Theme A–G prior-art protocols) and treat `patent_mcp_server` as a complementary source for PPUBS front-door search and PatentsView-based landscape work, rather than as a replacement for the specialized v3 MCPs.
```

On Windows, `C:/Users/trist` corresponds to `$env:USERPROFILE` for this machine. If your MCP client does not expand environment variables inside JSON strings, keep absolute paths as in the examples above.

Additional fields such as `env` MAY be supplied following Warp MCP documentation if you choose to use the "traditional" (plain-text env) configuration instead of the secure DPAPI storage used by the upstream installers.

### 14.2 Persisting USPTO_API_KEY in PowerShell

On Windows, contributors who wish to use USPTO-backed MCP servers SHOULD set the USPTO API key as a persistent user-level environment variable rather than hardcoding it in this repository.

From a PowerShell prompt, run (substituting your actual key):

```powershell
[System.Environment]::SetEnvironmentVariable(
  "USPTO_API_KEY",
  "<YOUR_USPTO_API_KEY>",
  "User"
)
```

After running this command, restart Warp or open a new PowerShell session. The key will then be available as `$env:USPTO_API_KEY` for MCP clients and tools. Secrets MUST NOT be committed to this repository in any form.

### 14.3 Standard patent research chat commands

To keep patent research reproducible and auditable, contributors and agents SHOULD use a small set of standard natural-language commands when interacting with MCP-backed USPTO tools. These commands are **non-normative orchestration hints**; they do not change the meaning of any specification or patent document.

Recognized patterns include:

- `prior-art protocol: start Themes A–G (PTAB+PFW+CitA only)`
  - Re-reads the non-normative prior-art search protocol under `docs/patents/`.
  - Runs the PTAB/File-Wrapper/Enriched-Citation portions of the protocol for CPSC/CPAC Themes A–G using `uspto_ptab`, `uspto_pfw`, and `uspto_enriched_citations` MCP servers (trial decisions, prosecution history, and citation data).
  - Proposes a Run ID and captures run metadata (date, spec/non-provisional version if available, coverage, and conclusion summary) in the chat transcript and, if a ledger file such as `LEDGER.md` exists, in that file.
  - Clearly marks the run as **USPTO-PTAB/PFW/CitA-only** and notes any tools that are not yet configured (for example, commercial full-text search APIs).

- `prior-art protocol: status (USPTO MCP)`
  - Summarizes prior-art and background work completed so far for Themes A–G, based on the protocol and any existing ledger entries in `docs/patents/` and/or `LEDGER.md`.
  - Highlights which USPTO MCP servers (PTAB, PFW, FPD, Enriched Citations) were used in each run and what changes would warrant a rerun.

- `prior-art protocol: rerun since <reason> (USPTO MCP)`
  - Treats the request as a new protocol run with an explicit trigger (for example, “claims refactored”, “new PTAB decisions identified”, “CPSC spec v0.4 released”).
  - Re-runs the appropriate subsets of the protocol against the currently configured USPTO MCP servers and records a new run entry.

These commands are intended to:

- keep prior-art work clearly separated from normative specifications,
- ensure that searches are repeatable and tied to specific versions of the CPSC/CPAC text,
- make it obvious which USPTO MCP data sources (PTAB, PFW, FPD, Enriched Citations) were used in any given run.

Agents MUST continue to treat all MCP tool output as **informational only** and MUST NOT treat any search result as changing the semantics of `docs/specification/` documents.

### 14.4 Version-control and session chat commands

For convenience and reproducibility, contributors MAY use natural-language commands to
request that agents stage, commit, and push changes to version control. These commands
are **non-normative orchestration hints** but DO authorize agents to run VCS commands
for the current repository when explicitly requested.

Recognized patterns include (examples, not a closed list):

- `push to git`
- `push to vc`
- `commit and push`
- `stage, commit, and push`

When a version-control command is issued (for example `push to git`), agents SHOULD:

1. Perform any repository-appropriate "save session" behavior for the current scope, if
   a convention or ledger file (for example `LEDGER.md` or an embedded ledger section in
   `docs/patents/`) exists.
2. Run `git status` (or the appropriate VCS status command) to determine which files
   have changed.
3. Stage the relevant changes (for example using `git add`), avoiding unintentional
   inclusion of generated artifacts unless explicitly requested.
4. Propose or infer a concise commit message based on the work performed in this
   session, ensuring that each commit message includes a `Co-Authored-By: Warp <agent@warp.dev>`
   line when the agent has made material edits.
5. Push the commit to the default remote and branch for this repository (for example,
   `origin/main`) unless the user has specified a different target.

If the scope of staged changes is unexpectedly large or appears to include unrelated
work, agents SHOULD pause, summarize the pending changes, and ask the user for
confirmation before committing and pushing.

In addition, when users issue explicit session-management commands, agents SHOULD
behave as follows (non-normative orchestration hints):

- `save session` – ensure any new tools or workflows used in the current session are
  reflected in the appropriate docs (for example `README.md`, `WARP.md`, `AGENTS.md`),
  then stage and commit the relevant changes locally, but do **not** push.
- `save session and push` – perform the `save session` steps and then push the
  resulting commits to the repository's default remote/branch (for example
  `origin/main`) unless the user has specified an alternative.
- `load session` – refresh local context from the current branch tip as needed
  (for example by running `git pull` or `git fetch` + `git merge` according to the
  repository's norms) and summarize relevant changes for the user.
- `pull and load session` – explicitly pull from the default remote/branch and then
  treat the updated state as the basis for subsequent work in the current chat.

### 14.5 Starting local USPTO MCP servers from PowerShell

For local testing or manual invocation outside of Warp's built-in MCP management,
contributors MAY start individual USPTO MCP servers directly from a PowerShell prompt
using `uv` once `scripts/setup-ptab-mcp-for-warp.ps1` (and each upstream
`deploy/windows_setup.ps1`) has been run. For example:

```powershell
uv --directory "$env:USERPROFILE\uspto_ptab_mcp" run ptab-mcp
uv --directory "$env:USERPROFILE\uspto_pfw_mcp" run patent-filewrapper-mcp
uv --directory "$env:USERPROFILE\uspto_fpd_mcp" run fpd-mcp
uv --directory "$env:USERPROFILE\uspto_enriched_citation_mcp" run uspto-enriched-citation-mcp
```

These commands assume the upstream repositories have been cloned into the default
locations under `$env:USERPROFILE` and that `uv` is installed and on `PATH`. API keys
are typically stored securely via DPAPI by the upstream installers; if you choose to
use plain-text environment variables instead, secrets MUST NOT be committed to this
repository.
