CPSC / CPAC Patent Work Ledger
===============================

This file records high-level steps completed and the next concrete action for Theme-based prior-art and claim-structuring work. It is non-normative and for internal coordination only.

---

Theme A – CPSC paradigm (Constraint-Structured Control Plane)
--------------------------------------------------------------

Completed so far:
- Defined Theme A and drafted proto independent claims (system, method, medium) for a constraint-structured control plane with:
  - explicit constraint structures (graph/lattice/hierarchy),
  - a generalized control plane orchestrating heterogeneous components (ML + non-ML),
  - constraint state tracking and constraint-centric justification artifacts,
  - governance behavior configurable by editing constraint programs without retraining models.
- Refined the Theme A system proto-claim to emphasize:
  - explicit representation of constraints and their relationships,
  - heterogeneous components under a single constraint program,
  - separation of constraint program from model weights/parameters.
- Analyzed one concrete comparator patent (ML-based clinician hazardous behavior + wasting station) and recorded a short prior-art note under `Theme A – recorded prior-art notes (non-normative)` in `patents/README.md`, including:
  - representative claim pattern,
  - overlaps with Theme A (ML-informed risk scoring, closed-loop actuation),
  - gaps relative to Theme A (no generalized constraint plane, no first-class constraint structure, no justification artifacts, no separable constraint program).
- Integrated a concrete proto-cell / epoch-controller hardware fabric embodiment and the CAS-YAML → CPSC Binary → hardware configuration path into the CPSC specification under `docs/specification/`, and updated `docs/public/cpsc-overview.md` to use the proto-cell/epoch fabric as a canonical CPSC hardware example while fixing several stray encoding artifacts in that document.
- Later refined the public CPSC overview text to remove an obsolete reference to "ConvergeCore" while preserving the proto-cell / epoch-controller embodiment as an example linked to the Deterministic Developmental Fabric (DDF), and regenerated the corresponding `docs-pdf/public/cpsc-overview.pdf` artifact.

Next action for Theme A (resume point):
- Identify and analyze a second comparator patent in the safety-controller family, preferably in the automated driving / vehicle or industrial control domain (e.g., a patent titled "Safety controller for automated driving" or similar, found via Google Patents or PFW search).
- Extract its independent claims and compare them against the Theme A checklist (constraint structure, control plane, heterogeneous components, justification artifacts, separable constraint program).
- Add a new short prior-art entry for Theme A in `patents/README.md` summarizing:
  - representative claim pattern for that safety controller,
  - overlaps with Theme A,
  - gaps relative to the CPSC architecture.
- Only adjust the Theme A proto-claims if this second comparator reveals a genuinely new architectural pattern not already captured by the refined Theme A system claim and the clinician hazardous-behavior example.

---

How to use this ledger when resuming work:
- For each Theme (A–G), there should be at most one "Next action" block that represents the current resume point.
- When you resume work on a Theme, read that Theme's "Next action" block, perform the action, then MOVE those bullets into the "Completed so far" list for that Theme and replace the "Next action" block with the *new* concrete next step (or remove it if that Theme is complete).
- Keep this file in sync with non-normative notes in `patents/README.md` and related Theme documentation, but do NOT move Theme content here; this file is for sequencing and coordination, not for substantive patent text.

Session note – USPTO PFW MCP proxy port conflict
------------------------------------------------
- Date: 2026-01-23
- Context: Local testing of `uspto_pfw_mcp` after merging async lifecycle fixes into `master`.
- Observation: MCP server initialized correctly, but HTTP proxy failed to bind on ports 8080 and 8081 with `WinError 10048` ("only one usage of each socket address...") indicating other processes were already holding those ports.
- Status: Treated as an environmental/temporary port conflict; no changes made to server code or default proxy port (kept at 8080). Future sessions should assume the implementation is good and resolve port usage at the OS level if the error recurs.

---

Theme B – CPAC representations / compression
-------------------------------------------

Completed so far:
- (placeholder) Theme B work not yet started in this ledger.

Next action for Theme B (resume point):
- (to be defined once Theme A is complete and initial CPAC prior-art analysis begins).

---

Theme C – Constraint-governed AI (governor / safety policy)
----------------------------------------------------------

Completed so far:
- (placeholder) Theme C work not yet started in this ledger.

Next action for Theme C (resume point):
- (to be defined when we start Theme C prior-art analysis).

---

Theme D – Learned structure-induction & structural classes
---------------------------------------------------------

Completed so far:
- (placeholder) Theme D work not yet started in this ledger.

Next action for Theme D (resume point):
- (to be defined when we start Theme D prior-art analysis).

---

Theme E – Quantum / non-von-Neumann backends
--------------------------------------------

Completed so far:
- (placeholder) Theme E work not yet started in this ledger.

Next action for Theme E (resume point):
- (to be defined when we start Theme E prior-art analysis).

---

Theme F – Cryptographic / PQC governance
----------------------------------------

Completed so far:
- (placeholder) Theme F work not yet started in this ledger.

Next action for Theme F (resume point):
- (to be defined when we start Theme F prior-art analysis).

---

Theme G – Governance & validation harness
-----------------------------------------

Completed so far:
- (placeholder) Theme G work not yet started in this ledger.

Next action for Theme G (resume point):
- (to be defined when we start Theme G prior-art analysis).
