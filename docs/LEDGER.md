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
- Analyzed a second comparator in the automated-vehicle safety-controller family (US 10,234,871 B2 – distributed safety monitors for automated vehicles) and added a non-normative Theme A prior-art note in `patents/README.md` capturing its representative claim pattern, overlaps (safety monitors gating an automated control loop, ASIL-oriented architecture), and gaps relative to CPSC (no explicit constraint-structured control plane, no generalized constraint program, no constraint-centric state/justification artifacts).
- Integrated a concrete proto-cell / epoch-controller hardware fabric embodiment and the CAS-YAML → CPSC Binary → hardware configuration path into the CPSC specification under `docs/specification/`, and updated `docs/public/cpsc-overview.md` to use the proto-cell/epoch fabric as a canonical CPSC hardware example while fixing several stray encoding artifacts in that document.
- Later refined the public CPSC overview text to remove an obsolete reference to "ConvergeCore" while preserving the proto-cell / epoch-controller embodiment as an example linked to the Deterministic Developmental Fabric (DDF), and regenerated the corresponding `docs-pdf/public/cpsc-overview.pdf` artifact.

Next action for Theme A (resume point):
- Consolidate the Theme A differentiation story across the clinician hazardous-behavior controller and the distributed safety-monitor architecture into a short, internal claim-structuring note (non-normative) that identifies the key architectural axes where CPSC departs from traditional safety controllers (generalized constraint plane, explicit constraint structures, constraint-centric state/justification artifacts, separable constraint program).
- Defer any further Theme A claim edits until that note exists and has been reviewed alongside the current CPSC-CPAC provisional draft.

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
- Run an initial comparator search for CPAC-style structural / degree-of-freedom compression of signals or models (e.g., patents combining compression with explicit structure or constraints), pick one representative comparator, and record a short non-normative Theme B prior-art note in `patents/README.md`.

---

Theme C – Constraint-governed AI (governor / safety policy)
----------------------------------------------------------

Completed so far:
- (placeholder) Theme C work not yet started in this ledger.

Next action for Theme C (resume point):
- Identify one representative "AI safety governor" or "policy engine" patent (e.g., safety envelopes, runtime monitors for ML controllers), summarize its independent-claim pattern, and add a short non-normative Theme C prior-art note in `patents/README.md` focusing on how it does or does not treat constraints as first-class structures.

---

Theme D – Learned structure-induction & structural classes
---------------------------------------------------------

Completed so far:
- (placeholder) Theme D work not yet started in this ledger.

Next action for Theme D (resume point):
- Select one comparator in the "learned relational/graph structure" or "program synthesis / structure induction" family, and record a non-normative Theme D prior-art note in `patents/README.md` emphasizing how learned structure relates (or not) to explicit CPSC structural classes.

---

Theme E – Quantum / non-von-Neumann backends
--------------------------------------------

Completed so far:
- (placeholder) Theme E work not yet started in this ledger.

Next action for Theme E (resume point):
- Identify a representative quantum or non-von-Neumann accelerator/control architecture patent and record a short non-normative Theme E prior-art note in `patents/README.md` focusing on whether it exposes an explicit constraint or state-manifold model vs. hardware-centric pipelines.

---

Theme F – Cryptographic / PQC governance
----------------------------------------

Completed so far:
- (placeholder) Theme F work not yet started in this ledger.

Next action for Theme F (resume point):
- Use the existing `pqc-prior-art-notes.md` themes to pick one comparator for constraint-governed PQC posture/migration, and summarize it in a non-normative Theme F prior-art note in `patents/README.md` (separate from Theme H structural/compression work).

---

Theme G – Governance & validation harness
-----------------------------------------

Completed so far:
- (placeholder) Theme G work not yet started in this ledger.

Next action for Theme G (resume point):
- Define one comparator in the "validation harness / monitoring framework" space (e.g., safety-case or assurance-harness patents) and write a non-normative Theme G prior-art note in `patents/README.md` highlighting differences between ad hoc harnesses and a CPSC-style constraint-projected validation fabric.
