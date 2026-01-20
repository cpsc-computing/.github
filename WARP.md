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

## 13. Patent and IP Documents

Patent-related materials for CPSC / CPAC live under `patents/` and are **legal disclosure and planning documents**, not specifications.

Key files:
- `patents/README.md` – overview of patent materials, status, and immutability policy
- `patents/CPSC-CPAC-Provisional-2026-01.md` – draft provisional utility patent application text (pre-filing); once filed, the Markdown and corresponding PDF become immutable
- `patents/executive-summary.md` – high-level business and technical summary of the CPSC / CPAC IP
- `patents/internal-ip-playbook.md` – internal patent strategy, licensing narratives, claim structure, and continuation planning
- `patents/non-provisional-outline.md` – structured outline for the anchor non-provisional patent filing

These documents:
- are **non-normative** and MUST NOT be treated as specifications or implementation requirements
- do **not** override or redefine semantics in `specification/`
- exist to record inventions, support filings, and guide licensing and continuation strategy
- do **not** grant patent rights beyond what is established in actual filed applications and issued patents

This directory is intended for internal IP tracking and planning and should remain private unless disclosure is explicitly required.

## 14. External Patent Tools and MCP Servers

When performing prior-art searches, patent landscape reviews, or PTAB decision analysis, contributors and agents MAY use external services and MCP servers as non-normative inputs.

A supported example is the USPTO-backed patent MCP server (`patent_mcp_server`), which exposes programmatic access to patent and PTAB-related information via MCP.

To install and update this server on a development machine, use:

- `scripts/setup-ptab-mcp-for-warp.ps1` – clones or updates the upstream `patent_mcp_server` repository and runs `uv sync` so it can be launched locally by Warp or other MCP clients.

Workflow rules for these tools:
- Results from MCP servers and external patent tools are **informational only** and MUST NOT be treated as normative specifications.
- Any conclusions or text derived from such tools MUST be reviewed and, where appropriate, restated in human-authored, spec-aligned language.
- Specifications under `specification/` remain the sole source of normative technical behavior, regardless of external legal or search tools.

### 14.1 Warp MCP JSON configuration example

Warp discovers MCP servers via JSON configuration. Two common patterns for configuring
the local patent MCP server are:

**Option A – Pass the repo path via `--directory`:**

```json
{
  "mcpServers": {
    "patents": {
      "command": "uv",
      "args": [
        "--directory",
        "%USERPROFILE%/patent_mcp_server",
        "run",
        "patent-mcp-server"
      ]
    }
  }
}
```

**Option B – Use `working_directory` and keep `args` minimal:**

```json
{
  "mcpServers": {
    "patents": {
      "command": "uv",
      "args": [
        "run",
        "patent-mcp-server"
      ],
      "working_directory": "%USERPROFILE%/patent_mcp_server"
    }
  }
}
```

On Windows, `%USERPROFILE%` refers to the current user's home directory (for example,
`C:\\Users\\trist`). If your MCP client (including Warp) does not expand environment
variables inside JSON strings, replace `%USERPROFILE%/patent_mcp_server` with the
full absolute path to your clone instead.

The `command`, `args`, and `working_directory` values MUST be adjusted if the repository
lives in a different subdirectory or if you prefer to launch it through a wrapper
script. Additional fields such as `env` MAY be supplied following Warp MCP documentation
if you want Warp to inject environment variables like `USPTO_API_KEY` at launch time.

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

To keep patent research reproducible and auditable, contributors and agents SHOULD use a small set of standard natural-language commands when interacting with MCP-backed patent tools. These commands are **non-normative orchestration hints**; they do not change the meaning of any specification or patent document.

Recognized patterns include:

- `prior-art protocol: start Themes A+B (PPUBS only)`
  - Re-reads the non-normative prior-art search protocol under `patents/`.
  - Runs the **PPUBS-only** portions of the protocol for CPSC/CPAC Themes A and B using the `patents` MCP server (granted patents and published applications).
  - Proposes a Run ID and captures run metadata (date, spec version if available, coverage, and conclusion summary) in the chat transcript and, if a ledger file such as `LEDGER.md` exists, in that file.
  - Clearly marks the run as **PPUBS-only** and notes any tools that are not yet configured (for example, PatentSearch/PatentsView APIs).

- `prior-art protocol: extend with PatentSearch`
  - Once PatentSearch/PatentsView credentials (for example `PATENTSVIEW_API_KEY`) are correctly configured for the `patents` MCP server, runs or extends the protocol using PatentSearch text filters, CPC-based sweeps, and citation tools.
  - Records a new run (or an extension of a previous run) with explicit coverage flags (PPUBS abstracts, PPUBS full text, PatentSearch text, CPC sweeps, citations) and a short conclusion summary.

- `prior-art protocol: status`
  - Summarizes prior-art work completed so far for Themes A and B, based on the protocol and any existing ledger entries in `patents/` and/or `LEDGER.md`.
  - Highlights which portions of the protocol have been run, which tools were available at the time (PPUBS vs PatentSearch), and what changes would warrant a re-run.

- `prior-art protocol: rerun since <reason>`
  - Treats the request as a new protocol run with an explicit trigger (for example, “claims refactored”, “PatentSearch key added”, “CPSC spec v0.4 released”).
  - Re-runs the appropriate subsets of the protocol and records a new run entry.

These commands are intended to:

- keep prior-art work clearly separated from normative specifications,
- ensure that searches are repeatable and tied to specific versions of the CPSC/CPAC text,
- make it obvious which data sources (PPUBS vs PatentSearch/PatentsView) were used in any given run.

Agents MUST continue to treat all MCP tool output as **informational only** and MUST NOT treat any search result as changing the semantics of `specification/` documents.
