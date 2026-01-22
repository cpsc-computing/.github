# Constraint-Projected State Computing (CPSC)

Constraint-Projected State Computing (CPSC) is a declarative computing model in which
computation is performed by projecting system state onto explicit constraints,
rather than executing ordered instructions.

CPSC provides a foundation for deterministic, constraint-driven systems across
software, compression, control systems, and hardware (FPGA / ASIC).

---

## What This Organization Hosts

This organization contains:

- The **CPSC technical specification**
- Declarative constraint models (CAS-YAML)
- Reference documentation and examples
- Licensing and governance materials
- Future reference implementations

The specification is the primary source of truth.

---

## Why CPSC Exists

Many real-world systems are governed by strong rules:
- physical limits
- protocol invariants
- safety constraints
- structural relationships

Traditional instruction-based computing handles these indirectly,
often resulting in complex control logic, tuning, and fragile edge cases.

CPSC makes **constraints the primary abstraction**.

---

## Core Concepts

- **State** — the full configuration of a system
- **Constraints** — rules defining valid states
- **Projection** — resolving state into validity
- **Degrees of Freedom** — minimal independent information
- **Constraint Fabric** — parallel enforcement of rules

---

## Applications

CPSC is applicable to:

- Semantic and structure-aware compression
- Streaming and edge data reduction
- Power electronics and control systems
- Deterministic AI inference pipelines
- FPGA and ASIC acceleration
- Secure state reconstruction
- Protocol enforcement and validation

---

## Status

CPSC is currently in the **specification and early reference phase**.

The specification is released for research and evaluation.
Reference implementations will follow.

---

## Patent and prior-art research

This organization maintains a separate `docs/patents/` directory for non-normative patent and IP materials related to Constraint-Projected State Computing (CPSC) and Constraint-Projected Adaptive Compression (CPAC).

- Documents under `docs/patents/` are **legal disclosure and planning artifacts**, not specifications.
- A non-normative **prior-art search protocol** for CPSC/CPAC Themes A and B (paradigm-level computing model and DoF-based compression) is maintained there, together with a simple ledger structure for recording what has been searched and when.
- Contributors using Warp and the local `patent_mcp_server` MCP backend MAY follow this protocol to run reproducible prior-art and landscape searches using USPTO-backed APIs (PPUBS, PatentSearch/PatentsView), but results remain informational only.
- Standard chat commands beginning with `prior-art protocol:` (documented in `WARP.md` and `AGENTS.md`) provide a repeatable way to ask agents to execute or summarize these searches; they do **not** change the meaning of any specification.

### Patent draft rendering helpers

For local draft PDFs of the CPSC/CPAC provisional (including Mermaid figures),
this repository provides:

- A Python wrapper script: `.github/scripts/render_markdown_to_pdf.py`
- PowerShell helpers: `.github/scripts/setup-provisional-render-env.ps1` and
  `.github/scripts/render-provisional-pdf.ps1`

These are convenience tools around the `md2pdf` CLI from the `md2pdf-mermaid`
package and use a headless Chromium engine to render Markdown (with Mermaid
blocks) to PDF. They do not change the legal status or semantics of any
document; they only control local formatting for review.

### USPTO / PatentSearch API keys and environment variables

To use the MCP-backed patent tools with live USPTO data, contributors MUST obtain and configure API keys outside this repository:

1. **USPTO Open Data Portal API key (`USPTO_API_KEY`)**
   - Create or sign in to a MyUSPTO account at `https://my.uspto.gov/`.
   - Visit the USPTO Open Data Portal at `https://data.uspto.gov/home`.
   - Use the key management page at `https://data.uspto.gov/myodp/key-reveal` to generate or reveal your Open Data Portal API key.
   - Store the key as a user-level environment variable so it is available as `$env:USPTO_API_KEY` (for example, using the PowerShell instructions in `WARP.md` §14.2), or in a local `.env` file consumed by `patent_mcp_server`.

2. **PatentsView / PatentSearch API key (`PATENTSVIEW_API_KEY`)**
   - Request a PatentsView PatentSearch API key via the official support portal at `https://patentsview-support.atlassian.net/servicedesk/customer/portal/1/group/1/create/18`.
   - General PatentsView information is available at `https://patentsview.org/home`.
   - Once issued, store the key so it is available to tools as `$env:PATENTSVIEW_API_KEY` (for example, as a user-level environment variable or in a local `.env` file that `patent_mcp_server` reads).

3. **Security and repository hygiene**
   - API keys MUST NOT be committed to this repository in any form (no checked-in `.env` files, scripts, or JSON containing secrets).
   - MCP configuration examples in `WARP.md` and related scripts are designed to read keys from the environment (`USPTO_API_KEY`, `PATENTSVIEW_API_KEY`) rather than from tracked files.

All patent-related work must respect the repository’s licensing and IP reservations. Patent rights are governed solely by filed applications and issued patents, not by this repository or any MCP-backed tooling.

---

## Licensing

The CPSC specification and related documents are released under the
**CPSC Research & Evaluation License**.

- Non-commercial research, evaluation, and educational use is permitted
- Commercial use requires a separate license

For a plain-language explanation, see `LEGAL-FAQ.md`.

---

## Getting Started

1. Read `docs/specification/CPSC-Specification.md`
2. Review CAS-YAML examples under `docs/specification/`
3. Consult `docs/LEGAL-FAQ.md` for licensing guidance

---

## Contact

For research questions, discussion, or licensing inquiries,
contact BitConcepts, LLC.
