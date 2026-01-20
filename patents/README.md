# Patents – CPSC / CPAC

This directory contains **legal disclosure documents** related to patent protection
for the Constraint-Projected State Computing (CPSC) paradigm and its applications,
including Constraint-Projected Adaptive Compression (CPAC).

⚠️ **IMPORTANT**
- Documents in this directory are **not specifications**
- They are **not normative**
- They must **not** be treated as implementation requirements
- Specifications live under `docs/specification/`

Patent documents exist solely to:
- establish priority dates,
- disclose inventions for patent protection,
- support future non-provisional and continuation filings.

---

## Current Filings

### CPSC-CPAC-Provisional-2026-01

**Status:** DRAFT (pre-filing)  
**Jurisdiction:** United States  
**Type:** Provisional Utility Patent Application  

**Title:**  
Constraint-Projected State Computing Systems and Applications

**Scope (High-Level):**
- CPSC as a new computing paradigm
- CPAC as a structural compression and enforcement layer
- Semantic system specification and deterministic lowering into constraint architectures
- Deterministic constraint projection
- Hardware and software embodiments
- Security, control, AI governance, and mission-critical systems
- Validation-only recursion-stability

**Planned Filing Artifacts:**
- Markdown source: `CPSC-CPAC-Provisional-2026-01.md`
- Filed PDF: `CPSC-CPAC-Provisional-2026-01.pdf`
- Filing receipt (USPTO): to be added post-filing

**Post-Filing Metadata (TO BE FILLED):**
- USPTO Application No.: `63/XXX,XXX`
- Filing Date: `2026-01-XX`
- Entity Status: `[Micro | Small]`
- PDF SHA-256 Hash: `<hash>`
- Git Commit SHA: `<commit>`

Once filed, the Markdown and PDF corresponding to this provisional
MUST be treated as **immutable**.

---

## Versioning and Immutability Policy

- Filed patent documents are **frozen**
- No edits after filing
- Corrections or extensions require:
  - a new provisional, or
  - a non-provisional / continuation filing

New ideas discovered after filing must be recorded in:
- a new provisional document, or
- internal notes awaiting future filings

---

## Relationship to Repository License

The repository license governs:
- source code
- specifications
- documentation

The license does **not** grant patent rights.

Patent rights are governed solely by filed patent applications
and any issued patents.

---

## Internal Use Only

This directory is intended for:
- IP tracking
- internal planning
- legal coordination

It should remain **private** unless and until disclosure is required.

---

## MCP-Backed Prior Art and Background Tools

For non-normative background research, contributors MAY use external MCP servers
backed by USPTO data, such as the `patent_mcp_server` used in this repository's
MCP configuration examples.

These tools are intended to support:
- prior-art searches,
- background and landscape review,
- identification of potentially relevant patents and publications for citation.

They MUST NOT be treated as authoritative or complete. Any search results should
be validated against official USPTO search tools or commercial equivalents, and
legal conclusions MUST be made by a qualified practitioner.

See `WARP.md` §14 for setup details and JSON configuration examples.
