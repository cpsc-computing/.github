# CPSC / CPAC / CGAD Embodiments — Overview

This document is the **live index of embodiments** for Constraint-Projected State Computing (CPSC),
Constraint-Projected Adaptive Compression (CPAC), and CPSC-Governed Agentic Development (CGAD).
It is public and will be updated as new embodiments are added to the provisional and related docs.

---

## 1. Embodiment Index (Definitive List)

Each entry is a single-sentence summary used as the canonical reference for that embodiment.
The first five are the current flagship CGAD embodiments.

1. **CGAD-1: General Agentic Governance Layer**
   - Treats agents (human or AI) as untrusted proposal generators whose actions are accepted only if a CPSC projection can reconcile them with an explicit constraint model over system state.

2. **CGAD-2: DDF / Hardware Fabric Governance**
   - Applies CGAD and CPSC to a constraint fabric (e.g., proto-cell + epoch controller) so that bitstream rebuilds, board syncs, and on-board runs are allowed only when regression, phase, and configuration constraints are satisfied.

3. **CGAD-3: cpsc-python / CPAC Spec-First Development**
   - Governs compression and benchmarking work in cpsc-python by requiring spec references, plans, green tests, benchmark runs, and ledger updates before non-trivial changes or pushes are accepted under CPSC projection.

4. **CGAD-4: Smart Control Plane for Realms and Resources**
   - Models datacenter or heterogeneous compute realms as constrained state and uses CPSC to accept or reject scheduling, migration, and allocation proposals under explicit governance and safety rules.

5. **CGAD-5: CPAC Front-End for NN and RL Models**
   - Uses a CPAC/CPSC front-end to project raw data into a constrained degree-of-freedom space, so neural or RL components operate only on structurally valid states separated from policy and safety constraints.

6. **E-11.1: Constraint Optimization and Satisfiability**
   - Encodes optimization and satisfiability problems as constraints and uses projection to evolve assignments deterministically toward valid or improved solutions.

7. **E-11.2: Configuration, Planning, and Scheduling**
   - Represents configurations and schedules as constrained state where degrees of freedom correspond to choices and projection enforces all hard constraints.

8. **E-11.3: Policy and Authorization Enforcement**
   - Treats access control as a constrained state space in which requests, policies, and resource state are projected to either a policy-compliant grant or a deterministic denial.

9. **E-11.4: Real-Time Control and Safety Envelopes**
   - Projects actuator commands into constraint-defined safety envelopes so that only commands consistent with declared bounds and invariants are emitted.

10. **E-11.5: Autonomous and Robotic Systems**
    - Interprets candidate actions from planners or learned controllers as proposals that must project into safety- and dynamics-constrained state spaces before execution.

11. **E-11.6: AI and Learned-System Governance**
    - Governs outputs of neural networks and language models by projecting them into constraint-defined state spaces encoding policy, safety, or structural rules.

12. **E-11.7: Hardware-Based Resource and Security Governance**
    - Implements governance and security policies directly in hardware by encoding scheduling, power, memory, and access rules as constraints evaluated by a CPSC fabric.

13. **E-11.8: Telemetry, Logging, and Replay**
    - Uses projection to validate, reconstruct, and replay telemetry and logs deterministically, enabling corruption detection and forensic analysis.

14. **E-11.9: Embedded and Low-Power Systems**
    - Provides deterministic, explainable computation for embedded and low-power devices without relying on neural inference by treating all behavior as constrained state projection.

15. **E-11.10: CPAC Core Compression Pipeline**
    - Decomposes compression into CPSC-based degree-of-freedom extraction followed by prediction and entropy coding, ensuring structure is enforced before any coding.

16. **E-11.11: Quantum and Non-Von-Neumann Backends**
    - Treats quantum, neuromorphic, analog, and in-memory compute devices as execution backends for a shared CPSC constraint architecture that defines correctness independently of hardware.

17. **E-11.12: Learned Predictors for CPAC**
    - Uses learned predictors operating in the structured degree-of-freedom space to improve compression while keeping correctness defined solely by CPSC projection.

18. **E-11.13: Constraint-Projected PQC Execution**
    - Executes post-quantum cryptographic algorithms by viewing cryptographic state as constrained variables and determining validity via projection instead of instruction-level control flow.

19. **E-11.13a: PQC Cryptographic State and Verification**
    - Represents PQC keys, signatures, and ciphertexts as cryptographic degrees of freedom and reconstructs all derived structure deterministically through projection.

20. **E-11.13b: PQC + CPAC Cryptographic State Handling**
    - Combines CPSC-based PQC execution with CPAC to serialize only cryptographic degrees of freedom and reconstruct full state deterministically on use.

21. **E-11.13c: Cryptographic Governance and Formal Verification**
    - Uses constraint models as machine-readable specifications for cryptographic systems and validates implementations by checking that execution corresponds to projection under those models.

22. **E-11.13d: PQC Communication and Key-Management**
    - Applies constraint-projected cryptographic models to channels, storage, and identity, governing hybrid and PQC-only states in a unified constrained space.

23. **E-11.14: Learned Structure-Induction (Neural-Assisted CPSC)**
    - Adds an optional learned stage that proposes structure or candidate states, which are then validated or rejected by CPSC projection.

24. **E-11.15: Quantum Resource Governance and Scheduling**
    - Treats classical and quantum resources as realms in a constrained governance fabric that deterministically enforces allocation and policy rules.

25. **E-11.16: Quantum-Aware Validation and Regression Harness**
    - Uses a CPSC constraint architecture as a reference semantics for validating and regressing quantum and probabilistic backends.

26. **E-11.17: Quantum-Safe Migration and Dual-Stack Governance**
    - Governs migration from classical to PQC cryptography by encoding both legacy and PQC states and policies in a unified constraint model.

27. **E-11.18: Hybrid Quantum–Classical CPAC**
    - Maintains a single CPAC semantics while allowing both classical and quantum predictors beneath the same constraint-defined compression model.

28. **E-13.x: CGAD for General Agentic Systems (Section 13)**
    - Elevates constraints and projection above agents, tools, and workflows so that all agent actions are treated as proposed state transitions validated by CPSC.

> When a new embodiment is introduced in the provisional or related specs, it
> MUST be added to this index with a unique identifier (e.g., `E-11.x` or
> `CGAD-n`) and a one-sentence summary.

---

## 2. Flagship CGAD Embodiments (Top 5)

### 2.1 CGAD-1: General Agentic Governance Layer

Traditional agentic systems treat prompts and policies as soft guidance while
letting agents mutate state directly, which leads to long-session drift,
implicit authority, and hard-to-replay outcomes. CGAD-1 inverts this pattern by
making all agent actions **proposed state transitions** in a shared model:
conversations and tools suggest next states, but only CPSC’s projection into a
constraint-defined valid region decides whether those transitions become real.
This makes governance declarative and deterministic—authority lives in
constraints over state, not in opaque orchestration logic—so that identical
inputs and proposals always yield identical accept/reject decisions.

### 2.2 CGAD-2: DDF / Hardware Fabric Governance

Complex FPGA/SoC flows often rely on tribal rules like "never deploy on red
regression" or "always rerun Vivado import after touching the BD," which are
hard to enforce consistently across tools and sessions. In CGAD-2, the DDF
hardware environment is modeled as constrained state—phase, regression status,
bitstream build mode, BD/RTL touch flags, and deploy/sync intents—and
CPSC enforces that any proposed action (rebuild, sync, run on hardware) can
only proceed if projection finds a valid configuration. This turns informal
safety culture into a mathematically enforced gate: hardware runs simply cannot
occur in states that violate regression, phase, or configuration constraints
without first updating the constraint model itself.

### 2.3 CGAD-3: cpsc-python / CPAC Spec-First Development

Spec-heavy compression work often aspires to be "requirements-first" but drifts
in practice as experiments, code, and benchmarks evolve faster than ledgers and
requirements. CGAD-3 encodes cpsc-python’s governance—spec references, planning
requirements, regression gates, wrapper-only execution, benchmark obligations,
and ledger updates—as an explicit CAS model, and treats session behavior as a
candidate assignment to that model. CPSC projection then decides whether a
non-trivial change or push is allowed: if any obligation is missing (no
referenced requirement, no plan, red tests, missing benchmarks, or stale
ledgers), the proposed transition is rejected, making spec-first discipline
structural rather than aspirational.

### 2.4 CGAD-4: Smart Control Plane for Realms and Resources

Datacenters and heterogeneous compute fabrics tend to accumulate independent
schedulers, policy engines, and hand-tuned scripts, each enforcing its own
rules and creating emergent, hard-to-explain behavior. CGAD-4 replaces this
with a **constraint-governed control plane** in which realms, resources,
workloads, SLAs, and governance policies are explicit variables in a CPSC
constraint architecture, and all scheduling or migration decisions are
proposals projected into that architecture. If a proposed assignment violates
isolation, error-budget, or policy constraints, projection simply fails, so the
control plane becomes a deterministic, auditable map from proposals to
constraint-satisfying resource states.

### 2.5 CGAD-5: CPAC Front-End for NN and RL Models

Neural networks and RL agents are often trained directly on raw or loosely
structured inputs, forcing them to learn both **structure** and **policy** in a
single, opaque model that silently internalizes quirks and bugs in upstream
systems. In CGAD-5, a CPAC/CPSC front-end first projects raw data into a
constraint-defined degree-of-freedom space—e.g., validated records, normalized
state, and enforced invariants—and only then exposes this structured state to
NN/RL models. CPSC remains the sole authority on which states are admissible,
while learned components act purely as proposal mechanisms within that space,
so safety and policy guarantees live in the constraint model, not in whatever
network happened to be trained last.

---

## 3. Other Application Embodiments (Section 11)

This section summarizes the non-exhaustive application embodiments from
Section 11 of the provisional.

### 3.1 E-11.1: Constraint Optimization and Satisfiability

Optimization and SAT problems are expressed as constraint systems over
variables, and CPSC projection evolves candidate assignments deterministically
until they either satisfy all constraints or fail under declared bounds.
Unlike ad-hoc solver loops, projection is part of the core execution model,
with determinism and convergence behavior specified explicitly.

### 3.2 E-11.2: Configuration, Planning, and Scheduling

Configurations, plans, and schedules are modeled as state with explicit degrees
of freedom and constraints representing resources, dependencies, and policies.
Given a proposed configuration or schedule, CPSC projects it into the valid
region or reports failure, making planning a matter of state projection rather
than imperative conflict resolution.

### 3.3 E-11.3: Policy and Authorization Enforcement

Access control decisions are derived from requests, policies, and resource
state encoded as constraints; projection determines whether any valid state
exists in which the request is allowed. This yields deterministic, auditable
policy enforcement where correctness is expressed declaratively, not scattered
across conditional branches.

### 3.4 E-11.4: Real-Time Control and Safety Envelopes

In control systems, desired actuator commands are proposed based on feedback
and targets, but CPSC projects these proposals into constraint-defined safety
envelopes (e.g., rate, position, or energy limits). The final output is always
consistent with declared safety bounds, independent of controller heuristics or
implementation details.

### 3.5 E-11.5: Autonomous and Robotic Systems

Candidate trajectories or actions from planners and learned policies are
interpreted as proposed states or sequences that must satisfy dynamic,
kinematic, and safety constraints. CPSC acts as a safety and policy layer that
accepts or rejects these proposals based solely on constraint satisfaction,
separating motion feasibility and safety from the particulars of the planner.

### 3.6 E-11.6: AI and Learned-System Governance

Outputs from learned models (including large language models) are mapped into
structured state spaces where policy, safety, or structural rules are
specified. CPSC projection then enforces those rules—e.g., ensuring that
allocations, recommendations, or decisions respect constraints—without
requiring the model itself to be trusted or interpretable.

### 3.7 E-11.7: Hardware-Based Resource and Security Governance

Security and resource policies are realized as constraints in hardware, with
CPSC fabrics evaluating admissibility of accesses, allocations, or transitions
at line rate. This allows critical enforcement (e.g., memory or power budgets,
privilege boundaries) to be implemented in deterministic hardware rather than
in software that may be bypassed.

### 3.8 E-11.8: Telemetry, Logging, and Replay

Telemetry frames and logs are treated as partially observed state, and CPSC
projection reconstructs a minimal, constraint-consistent representation while
flagging inconsistencies. This enables deterministic replay and analysis, where
any corruption or tampering manifests as projection failure or structural
anomalies.

### 3.9 E-11.9: Embedded and Low-Power Systems

CPSC supports embedded and low-power designs by replacing complex control logic
with constraint projection on a compact state representation, avoiding heavy
neural inference or deep stacks of imperative code. Determinism, explainability,
and bounded resource use are first-class design targets.

### 3.10 E-11.10: CPAC Core Compression Pipeline

CPAC uses CPSC as its front-end: raw data are injected into a
constraint-architected state, projected to a minimal degree-of-freedom vector,
optionally predicted, and then entropy-coded. This separates semantic
structure (captured by constraints and DoFs) from statistical modeling and
coding, making the transform both deterministic and explainable.

### 3.11 E-11.11: Quantum and Non-Von-Neumann Backends

A single semantic system specification and constraint architecture define the
problem, while quantum, neuromorphic, analog, or other non-Von-Neumann
backends act as proposal or computation engines underneath. CPSC provides a
stable intent layer above these backends, so hardware can be swapped or
combined without changing the semantics of correctness.

### 3.12 E-11.12: Learned Predictors for CPAC

Learned predictors operate only in the DoF space produced by CPAC’s
constraint projection, outputting predicted DoFs or distributions used by
entropy coders. Correctness and losslessness remain defined entirely by CPSC;
learned components influence efficiency, not validity.

### 3.13 E-11.13: Constraint-Projected PQC Execution and Variants

Post-quantum cryptographic algorithms are expressed as constrained
cryptographic state, with signatures, ciphertexts, and keys represented as
DoFs and all other structure reconstructed via projection. Multiple variants
cover pure execution, CPAC-coupled state handling, governance and formal
verification, and full communication/key-management stacks; in all cases,
validity is determined by satisfying cryptographic constraints, not by
branch-heavy procedural code.

### 3.14 E-11.14: Learned Structure-Induction (Neural-Assisted CPSC)

Optional learned models propose structure (e.g., record boundaries, latent
fields, or candidate assignments) from raw input, but CPSC projection remains
sole arbiter of validity. This allows learned components to assist parsing and
modeling while preserving deterministic, constraint-based correctness.

### 3.15 E-11.15: Quantum Resource Governance and Scheduling

Quantum and classical resources are modeled as realms with capacities,
policies, and error budgets, and CPSC enforces that any proposed workload
assignment or schedule satisfies governance constraints before execution.
This yields explainable, policy-compliant resource management in hybrid
quantum-classical environments.

### 3.16 E-11.16: Quantum-Aware Validation and Regression Harness

A shared constraint architecture defines acceptable outputs for
quantum-targeted problems, and CPSC projection is used to validate candidate
solutions from quantum or approximate backends. This provides a deterministic
regression and drift-detection harness across quantum providers, compilers,
and hardware generations.

### 3.17 E-11.17: Quantum-Safe Migration and Dual-Stack Governance

Legacy and post-quantum cryptographic states and policies are represented in a
single constraint model, and CPSC projection determines whether proposed
migration steps (e.g., key rotations, mode changes, downgrades) are compliant.
Migration plans and runtime configurations are accepted only if they project
into states that satisfy declared quantum-safe policies.

### 3.18 E-11.18: Hybrid Quantum–Classical CPAC

The CPAC pipeline is kept semantics-stable while allowing classical, quantum,
or hybrid predictors beneath it: all predictors propose DoFs or distributions
that are then projected by CPSC. Compressed bitstreams remain defined solely in
terms of constraint architectures and DoFs, independent of predictor type.

---

## 4. CGAD-Section 13 Embodiments

Section 13 of the provisional (CGAD) refines the general AI governance
embodiment into multiple architectural patterns. CGAD-1 through CGAD-5 above
are the current flagship instances; future CGAD-specific embodiments (for
example, additional repository profiles or domain-specific agent workflows)
SHOULD extend the `CGAD-n` numbering here and include both a one-sentence index
entry (Section 1) and a brief narrative summary in this section.
