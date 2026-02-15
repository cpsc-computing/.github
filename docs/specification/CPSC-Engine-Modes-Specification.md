# CPSC Engine Modes Specification
## Iterative and Cellular Projection Engines with DLIF Streaming

**Version:** 1.0  
**Status:** Draft Specification  
**Scope:** Defines two projection engine modes for CPSC with software and hardware embodiment architectures, including the DLIF streaming format for cellular engines.

---

## 1. Introduction

### 1.1 Purpose

This specification defines two projection engine modes for CPSC (Constraint-Projected State Computing):

1. **Iterative Engine** — Global constraint evaluation with numerical iteration
2. **Cellular Engine** — Local rule evaluation with neighbor-based self-organization via DLIF streaming

Both engines satisfy the core CPSC invariants:
- Deterministic convergence under declared bounds
- Explicit state representation
- No hidden execution semantics
- Reproducible results given identical inputs

### 1.2 Document Structure

Each engine mode is specified in two embodiments:

- **Software Embodiment** — Implementation in general-purpose programming languages (Python, Rust, C++)
- **Hardware Embodiment** — Implementation in RTL for FPGA/ASIC synthesis (VHDL, Verilog, SystemVerilog)

### 1.3 Normative References

This specification depends on and must remain consistent with:

| Document                            | Scope                   | Key Interfaces                                               |
| ----------------------------------- | ----------------------- | ------------------------------------------------------------ |
| `CPSC-Specification.md`             | Core CPSC model         | §5 Projection, §6 Determinism, §7 DoF, §12 Hardware Guidance |
| `CAS-YAML-Specification.md`         | Constraint model format | §7 State, §8 Constraints, §10 Projection Config              |
| `Binary-Format-Specification.md`    | DSIF binary format      | §3 Structure, §7 DoF Vector, §9 Streaming Properties         |
| `Binary-Format-RTL-Mapping.md`      | Hardware signal mapping | §6 DoF Mapping, §8 Constraint Fabric Interface               |
| `CPSC-Implementation-Governance.md` | Development practices   | §2 Spec-First Workflow, §3 Determinism                       |
| `CAS-Example-Synthetic-Log.yaml`    | Reference CAS model     | 4-variable telemetry example                                 |
### 1.4 Specification Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    CPSC-Specification.md                        │
│                    (Core computation model)                      │
└─────────────────────────────┬───────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌─────────────────────┐
│ CAS-YAML-     │   │ Binary-Format-  │   │ THIS DOCUMENT       │
│ Specification │   │ Specification   │   │ Engine-Modes-Spec   │
│ (Model def)   │   │ (DSIF format)   │   │ (Engine behavior)   │
└───────┬───────┘   └────────┬────────┘   └──────────┬──────────┘
        │                    │                       │
        │                    │            ┌─────────┴─────────┐
        │                    │            │                   │
        ▼                    ▼            ▼                   ▼
┌───────────────┐   ┌─────────────────┐  ┌─────────┐   ┌───────────┐
│ CAS-Example-  │   │ Binary-Format-  │  │ DLIF    │   │ Cellular  │
│ Synthetic-Log │   │ RTL-Mapping     │  │ Format  │   │ Engine    │
│ (Example)     │   │ (HW signals)    │  │ (§10)   │   │ (§4)      │
└───────────────┘   └─────────────────┘  └─────────┘   └───────────┘
```
---

## 2. Common Definitions

### 2.1 State Model

Per CPSC-Specification.md §3, both engines operate on a **state** defined by a CAS-YAML model:

```
S = { v₁, v₂, …, vₙ }
```
Each variable has (per CAS-YAML-Specification.md §7.2):
- **name**: Unique identifier
- **type**: Numeric type (int, float, fixed-point)
- **domain**: Valid value range or discrete set
- **derived**: Boolean indicating if computed from constraints

### 2.2 Degrees of Freedom (DoF)

Per CPSC-Specification.md §7, the **DoF vector** contains values for all free variables:

```
DoF = [v_free₁, v_free₂, …, v_freeₖ]
```
The DoF vector is encoded in DSIF per Binary-Format-Specification.md §7:
- Order defined by CAS-YAML `degrees_of_freedom.free` list
- Width defined by `execution.precision_bits`
- Numeric interpretation defined by `execution.numeric_mode`

### 2.3 Projection Result

Both engines return a common result structure:

```
ProjectionResult:
  success: bool              # True if converged to valid state
  state: StateVector | None  # Final variable values (None if failed)
  iterations: int            # Iterations (Iterative) or cycles (Cellular)
  max_violation: float       # Largest constraint violation at termination
  details: dict              # Engine-specific diagnostics
  reason: str | None         # Failure description if success=False
```
### 2.4 Engine Selection

Engine mode is determined by:

1. **CAS-YAML `projection.method`** (per CAS-YAML-Specification.md §10):
   - `iterative`, `bounded_relaxation`, `newton`, `gradient` → Iterative Engine
   - `cellular`, `local_rules`, `self_organizing` → Cellular Engine

2. **Runtime override** via API parameter or hardware configuration register

3. **Default**: Iterative Engine (backward compatible with existing implementations)

### 2.5 Determinism Requirements

Per CPSC-Specification.md §6 and CPSC-Implementation-Governance.md §3:

- Given identical CAS model, DoF values, and configuration, engines MUST produce identical results
- Numeric modes and precision MUST be explicit (no hidden defaults)
- Convergence criteria MUST be declared and enforced
- Non-deterministic behavior MUST be eliminated or reported as an error

---

## 3. Iterative Engine

### 3.1 Overview

The Iterative Engine performs **global constraint evaluation** with **numerical iteration** to converge on a valid state. All constraints are evaluated each iteration, and corrections are computed to minimize constraint violations.

**Characteristics:**
- Global view of all constraints per iteration
- Gradient-based or Newton-style correction
- Well-suited for continuous arithmetic constraints
- Convergence via error minimization

**Implements:** CPSC-Specification.md §5 (Projection) via iterative refinement

---

### 3.2 Software Embodiment

#### 3.2.1 Architecture

```
┌─────────────────────────────────────────────────────┐
│                  IterativeEngine                     │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────────────────┐     │
│  │ StateVector │───▶│  ConstraintEvaluator    │     │
│  │  (mutable)  │    │  - evaluate_all()       │     │
│  └─────────────┘    │  - compute_violations() │     │
│        ▲            └───────────┬─────────────┘     │
│        │                        │                   │
│        │            ┌───────────▼─────────────┐     │
│        │            │   CorrectionComputer    │     │
│        │            │   - gradient_step()     │     │
│        │            │   - newton_step()       │     │
│        │            └───────────┬─────────────┘     │
│        │                        │                   │
│        └────────────────────────┘                   │
│                   (apply corrections)               │
├─────────────────────────────────────────────────────┤
│  ConvergenceChecker                                 │
│  - max_iterations: from CAS projection config       │
│  - epsilon: from CAS projection.convergence_epsilon │
└─────────────────────────────────────────────────────┘
```
#### 3.2.2 Data Structures

```python
@dataclass
class StateVector:
    """Mutable mapping of variable names to values."""
    values: dict[str, float]
    
    def __getitem__(self, name: str) -> float: ...
    def __setitem__(self, name: str, value: float): ...
    def copy(self) -> 'StateVector': ...

@dataclass
class ConstraintViolation:
    """Result of evaluating a single constraint."""
    constraint_id: str          # From CAS-YAML constraint.id
    lhs_value: float
    rhs_value: float
    violation: float            # abs(lhs - rhs)
    gradient: dict[str, float]  # ∂violation/∂var for each free variable

@dataclass  
class IterationResult:
    """Diagnostics from one iteration."""
    iteration: int
    max_violation: float
    corrections_applied: dict[str, float]
    converged: bool
```
#### 3.2.3 Algorithm

```python
class IterativeEngine:
    """
    Iterative projection engine using global constraint evaluation.
    
    Configuration sourced from CAS-YAML projection section per
    CAS-YAML-Specification.md §10.
    """
    
    def __init__(
        self,
        max_iterations: int = 100,        # From projection.max_iterations
        convergence_epsilon: float = 1e-6, # From projection.convergence_epsilon
        step_size: float = 0.5,
        method: Literal['gradient', 'newton'] = 'gradient'
    ): ...
    
    def solve(self, model: CasModel, dof_values: Sequence[float]) -> ProjectionResult:
        """
        Project DoF values onto constraint manifold.
        
        Per CPSC-Specification.md §5:
        1. Evaluate all constraints
        2. Identify violations
        3. Apply bounded corrections
        4. Iterate until convergence or declared limits
        """
        # 1. Initialize state from DoF (per CPSC-Spec §7)
        state = self._initialize_state(model, dof_values)
        
        # 2. Iteration loop
        for iteration in range(self.max_iterations):
            # 2a. Evaluate all constraints (per CPSC-Spec §4)
            violations = self._evaluate_constraints(model, state)
            
            # 2b. Check convergence
            max_violation = max(v.violation for v in violations)
            if max_violation <= self.convergence_epsilon:
                return ProjectionResult(success=True, state=state, 
                                        iterations=iteration+1,
                                        max_violation=max_violation)
            
            # 2c. Compute corrections (bounded per CPSC-Spec §6)
            corrections = self._compute_corrections(violations, method=self.method)
            
            # 2d. Apply corrections to free variables only
            self._apply_corrections(state, corrections, model.free_variables)
            
            # 2e. Recompute derived variables from definitions
            self._evaluate_definitions(model, state)
        
        # 3. Failed to converge - report per CPSC-Spec §6
        return ProjectionResult(
            success=False, state=state, 
            iterations=self.max_iterations,
            max_violation=max_violation,
            reason=f"NO_CONVERGENCE: max_violation={max_violation:.2e}"
        )
    
    def _initialize_state(self, model: CasModel, dof_values: Sequence[float]) -> StateVector:
        """
        Initialize state from DoF values.
        
        DoF ordering per CAS-YAML-Specification.md §9.2:
        Variables listed in degrees_of_freedom.free define the order.
        """
        if len(dof_values) != len(model.free_variables):
            raise ValueError(f"DoF count mismatch: expected {len(model.free_variables)}")
        
        state = StateVector(values={})
        for name, value in zip(model.free_variables, dof_values):
            state[name] = float(value)
        
        # Initialize derived variables to zero (will be computed)
        for var in model.variables:
            if var.derived and var.name not in state.values:
                state[var.name] = 0.0
        
        return state
```
#### 3.2.4 DSIF Integration

Per Binary-Format-Specification.md §10 (Reconstruction Algorithm):

```python
def solve_from_dsif(self, blob: bytes, model: CasModel) -> ProjectionResult:
    """
    Reconstruct state from DSIF binary blob.
    
    Implements Binary-Format-Specification.md §10:
    1. Parse header
    2. Validate format version
    3. Read model metadata
    4. Load CAS-YAML model (provided)
    5. Inject degree-of-freedom values
    6. Apply residuals (if present)
    7. Run CPSC projection
    8. Emit valid state
    """
    # Decode DSIF per Binary-Format-Specification.md
    decoded = decode_dsif(blob, model)
    
    # Apply residuals before projection if present
    dof_values = decoded.dof_values
    if decoded.residual_values:
        dof_values = self._apply_residuals(dof_values, decoded.residual_values)
    
    # Run projection
    return self.solve(model, dof_values)
```
#### 3.2.5 Thread Safety

- `StateVector` instances are NOT thread-safe; each thread must use its own copy
- `IterativeEngine` instances are stateless and thread-safe
- `CasModel` instances are immutable and thread-safe

---

### 3.3 Hardware Embodiment

#### 3.3.1 Architecture

Per Binary-Format-RTL-Mapping.md §8 (Constraint Fabric Interface):

```
                    ┌─────────────────────────────────────┐
                    │      Iterative Projection Core      │
                    ├─────────────────────────────────────┤
  dof_in[N-1:0] ───▶│  ┌─────────────────────────────┐   │
                    │  │     DoF Register File       │   │──▶ dof_regs[]
                    │  │     (N × PRECISION bits)    │   │    (to fabric)
                    │  └──────────┬──────────────────┘   │
                    │             │                       │
                    │  ┌──────────▼──────────────────┐   │
                    │  │   Constraint Evaluation     │   │
                    │  │   Units (CEU) × M           │   │
                    │  │   - Parallel evaluation     │   │
                    │  │   - Fixed-point arithmetic  │   │
                    │  └──────────┬──────────────────┘   │
                    │             │ violation[M-1:0]     │
                    │  ┌──────────▼──────────────────┐   │
                    │  │   Correction Accumulator    │   │
                    │  │   - Gradient computation    │   │
                    │  │   - Step scaling            │   │
                    │  └──────────┬──────────────────┘   │
                    │             │ correction[N-1:0]    │
                    │  ┌──────────▼──────────────────┐   │
                    │  │   State Update Logic        │   │
                    │  │   - Saturation arithmetic   │   │
                    │  │   - Write-back to DoF regs  │   │
                    │  └─────────────────────────────┘   │
                    │                                     │
  clk ─────────────▶│  ┌─────────────────────────────┐   │
  rst_n ───────────▶│  │   Iteration Controller      │   │──▶ done
  start ───────────▶│  │   - FSM: IDLE→EVAL→CORR→UPD │   │──▶ converged
  max_iter[7:0] ───▶│  │   - Convergence check       │   │──▶ iteration[7:0]
  epsilon[P-1:0] ──▶│  └─────────────────────────────┘   │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
                              state_out[N×P-1:0]
```
#### 3.3.2 Signal Definitions

Per Binary-Format-RTL-Mapping.md §3-§6:

**Input Ports:**

| Signal           | Width | Description                  | RTL Mapping Reference      |
| ---------------- | ----- | ---------------------------- | -------------------------- |
| `clk`            | 1     | System clock                 | —                          |
| `rst_n`          | 1     | Active-low synchronous reset | —                          |
| `start`          | 1     | Begin projection (pulse)     | —                          |
| `dof_in`         | N×P   | Initial DoF values, packed   | §6.1 dof_regs[]            |
| `max_iter`       | 8     | Maximum iteration count      | From CAS projection config |
| `epsilon`        | P     | Convergence threshold        | From CAS projection config |
| `precision_bits` | 16    | Numeric precision            | §4 meta.precision_bits     |
| `numeric_mode`   | 8     | Fixed/floating mode          | §3.1 hdr_numeric_mode      |
**Output Ports:**

| Signal          | Width | Description                      | RTL Mapping Reference |
| --------------- | ----- | -------------------------------- | --------------------- |
| `done`          | 1     | Projection complete (pulse)      | —                     |
| `converged`     | 1     | 1=success, 0=max_iter reached    | §8 state_valid        |
| `iteration`     | 8     | Final iteration count            | —                     |
| `state_out`     | N×P   | Projected state values           | §8 state_regs[]       |
| `max_violation` | P     | Largest violation at termination | —                     |
#### 3.3.3 FSM States

Per Binary-Format-RTL-Mapping.md §9:

```
         ┌──────┐
    ─────│ IDLE │◀─────────────────────┐
   start └──┬───┘                      │
            │                          │
            ▼                          │
       ┌────────┐                      │
       │  LOAD  │  Load DoF into regs  │
       └───┬────┘                      │
           │                           │
           ▼                           │
       ┌────────┐◀──────┐              │
       │  EVAL  │       │              │
       └───┬────┘       │              │
           │            │ not converged│
           ▼            │ && iter<max  │
       ┌────────┐       │              │
       │ CHECK  │───────┘              │
       └───┬────┘                      │
           │ converged || iter>=max    │
           ▼                           │
       ┌────────┐                      │
       │  DONE  │──────────────────────┘
       └────────┘
```
#### 3.3.4 Timing

| Phase  | Cycles    | Description                                           |
| ------ | --------- | ----------------------------------------------------- |
| LOAD   | 1         | Latch DoF inputs into register file                   |
| EVAL   | ceil(M/P) | Evaluate M constraints with P parallel CEUs           |
| CHECK  | 1         | Compare max_violation to epsilon, compute corrections |
| UPDATE | 1         | Apply corrections to DoF registers                    |
**Total per iteration:** `2 + ceil(M/P)` cycles

---

## 4. Cellular Engine

### 4.1 Overview

The Cellular Engine performs **local rule evaluation** with **neighbor-based state exchange** to achieve self-organization. This implements the "constraint fabric" pattern from CPSC-Specification.md §12:

> "One non-limiting class of hardware embodiments realizes the constraint fabric as a regular array or graph of proto-cells under control of a global epoch controller. In such embodiments, each proto-cell holds local configuration and state, exchanges signals with neighboring proto-cells, and applies fixed local update rules, while an epoch controller orchestrates globally synchronized epochs with commit-only state updates."

**Characteristics:**
- Local computation with neighbor communication only
- Emergent global behavior from simple local rules
- Configuration and data streamed via DLIF format (§10)
- Convergence via pattern stabilization

---

### 4.2 Software Embodiment

#### 4.2.1 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      CellularEngine                           │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    DLIF Decoder                          │ │
│  │  - Parses element stream                                 │ │
│  │  - Routes CONFIG elements to cells                       │ │
│  │  - Routes DATA elements through grid                     │ │
│  └──────────────────────────┬──────────────────────────────┘ │
│                             │                                 │
│  ┌──────────────────────────▼──────────────────────────────┐ │
│  │                        Grid                              │ │
│  │  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐          │ │
│  │  │Cell₀ │◀──▶│Cell₁ │◀──▶│Cell₂ │◀──▶│Cell₃ │          │ │
│  │  └──────┘    └──────┘    └──────┘    └──────┘          │ │
│  │      ▲                                    ▲              │ │
│  │   virtual                              virtual           │ │
│  │   boundary                             boundary          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                                │
│  ┌───────────────────────────▼─────────────────────────────┐ │
│  │                   CycleController                        │ │
│  │  - Orchestrates OBSERVE → COMPUTE → APPLY phases        │ │
│  │  - Detects convergence (stability window)               │ │
│  │  - Enforces max_cycles bound                            │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                                │
│  ┌───────────────────────────▼─────────────────────────────┐ │
│  │                      LocalRule                           │ │
│  │  - Evaluates next state from current + neighbors        │ │
│  │  - Stateless, pure function (determinism per CPSC §6)   │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```
#### 4.2.2 Data Structures

```python
# Cell type constants (2-bit encoding, RTL compatible)
CELL_INACTIVE: int = 0  # "00"
CELL_ACTIVE: int = 1    # "01"
# Reserved: 2 ("10"), 3 ("11")

@dataclass(frozen=True)
class CellState:
    """
    Immutable snapshot of cell state.
    
    Matches RTL cell state register layout for hardware compatibility.
    """
    cell_type: int      # 2 bits: INACTIVE=0, ACTIVE=1
    cell_param: int     # PARAM_WIDTH bits: configuration from DoF
    fitness: int        # FITNESS_WIDTH bits: local quality accumulator

class Cell:
    """
    Mutable cell with double-buffered state for atomic updates.
    
    Implements CPSC-Specification.md §12 proto-cell semantics:
    - Holds local configuration and state
    - Exchanges signals with neighbors
    - Applies fixed local update rules
    """
    
    def __init__(self, index: int, param: int = 0):
        self.index = index
        self._current = CellState(cell_type=CELL_INACTIVE, cell_param=param, fitness=0)
        self._next = self._current
        self._left_neighbor: CellState | None = None
        self._right_neighbor: CellState | None = None
    
    @property
    def state(self) -> CellState:
        """Current committed state (read-only view)."""
        return self._current
    
    def observe(self, left: CellState | None, right: CellState | None) -> None:
        """
        OBSERVE phase: Cache neighbor states.
        
        Per CPSC §12: "exchanges signals with neighboring proto-cells"
        No writes to current state permitted during this phase.
        """
        self._left_neighbor = left
        self._right_neighbor = right
    
    def compute(self, rule: 'LocalRule') -> None:
        """
        COMPUTE phase: Evaluate local rule, store in next buffer.
        
        Per CPSC §12: "applies fixed local update rules"
        Result stored in buffer, not yet committed.
        """
        self._next = rule.evaluate(self._current, self._left_neighbor, self._right_neighbor)
    
    def apply(self) -> None:
        """
        APPLY phase: Commit next state to current.
        
        Per CPSC §12: "commit-only state updates"
        This is the only point where state changes become visible.
        """
        self._current = self._next

class Grid1D:
    """
    One-dimensional chain of cells with configurable boundaries.
    
    Per CPSC-Specification.md §12: "regular array or graph of proto-cells"
    """
    
    def __init__(self, n_cells: int, params: list[int], boundary: str = 'active_left'):
        """
        Args:
            n_cells: Number of cells in chain
            params: Initial cell_param for each cell (from DoF vector)
            boundary: Boundary condition mode:
                - 'active_left': Left boundary = ACTIVE, right = INACTIVE
                  (reference behavior per DDF ARCHITECTURE.md §4.4)
                - 'inactive': Both boundaries see virtual INACTIVE
                - 'wrap': Periodic boundary (cell 0 neighbors cell N-1)
        """
        if len(params) != n_cells:
            raise ValueError(f"params length {len(params)} != n_cells {n_cells}")
        
        self.cells = [Cell(index=i, param=params[i]) for i in range(n_cells)]
        self.boundary = boundary
        self._n_cells = n_cells
    
    def observe(self) -> None:
        """OBSERVE phase for all cells. Order-independent (parallelizable)."""
        for i, cell in enumerate(self.cells):
            left = self._get_left_neighbor(i)
            right = self._get_right_neighbor(i)
            cell.observe(left, right)
    
    def compute(self, rule: 'LocalRule') -> None:
        """COMPUTE phase for all cells. Order-independent (parallelizable)."""
        for cell in self.cells:
            cell.compute(rule)
    
    def apply(self) -> None:
        """
        APPLY phase for all cells.
        
        Per CPSC §12: All cells commit simultaneously ("globally synchronized epochs").
        """
        for cell in self.cells:
            cell.apply()
    
    def get_types(self) -> list[int]:
        """Return cell_type for all cells (for convergence checking)."""
        return [cell.state.cell_type for cell in self.cells]
    
    def get_fitness(self) -> list[int]:
        """Return fitness for all cells."""
        return [cell.state.fitness for cell in self.cells]
    
    def configure_from_dlif(self, stream: 'DlifStream') -> None:
        """Configure grid from DLIF element stream. See §10."""
        for element in stream:
            if element.type == DLIF_CONFIG_PARAM:
                cell_index = element.cell_index
                if 0 <= cell_index < self._n_cells:
                    self.cells[cell_index]._current = CellState(
                        cell_type=CELL_INACTIVE,
                        cell_param=element.value,
                        fitness=0
                    )
    
    def _get_left_neighbor(self, index: int) -> CellState | None:
        if index == 0:
            if self.boundary == 'active_left':
                return CellState(cell_type=CELL_ACTIVE, cell_param=0, fitness=0)
            elif self.boundary == 'wrap':
                return self.cells[-1].state
            else:  # 'inactive'
                return CellState(cell_type=CELL_INACTIVE, cell_param=0, fitness=0)
        return self.cells[index - 1].state
    
    def _get_right_neighbor(self, index: int) -> CellState | None:
        if index == self._n_cells - 1:
            if self.boundary == 'wrap':
                return self.cells[0].state
            else:  # 'active_left' or 'inactive'
                return CellState(cell_type=CELL_INACTIVE, cell_param=0, fitness=0)
        return self.cells[index + 1].state

class CycleController:
    """
    Orchestrates grid cycles and detects convergence.
    
    Per CPSC §12: "epoch controller orchestrates globally synchronized epochs"
    """
    
    def __init__(self, max_cycles: int = 32, stability_window: int = 4):
        """
        Args:
            max_cycles: Maximum cycles before termination (from projection.max_iterations)
            stability_window: Consecutive stable cycles required for convergence
        """
        self.max_cycles = max_cycles
        self.stability_window = stability_window
        self._cycle = 0
        self._stable_count = 0
        self._last_types: list[int] | None = None
    
    @property
    def cycle(self) -> int:
        """Current cycle count."""
        return self._cycle
    
    @property
    def converged(self) -> bool:
        """True if pattern has been stable for stability_window cycles."""
        return self._stable_count >= self.stability_window
    
    def step(self, grid: Grid1D) -> bool:
        """
        Check convergence after a cycle. Returns True if should continue.
        
        Convergence: cell types unchanged for stability_window consecutive cycles.
        """
        current_types = grid.get_types()
        
        if current_types == self._last_types:
            self._stable_count += 1
        else:
            self._stable_count = 0
        
        self._last_types = current_types.copy()
        self._cycle += 1
        
        return not self.converged and self._cycle < self.max_cycles
```
#### 4.2.3 Local Rules

```python
class LocalRule(Protocol):
    """
    Protocol for local rule implementations.
    
    Rules MUST be:
    - Stateless (determinism per CPSC §6)
    - Pure functions (no side effects)
    - Consistent across software/hardware embodiments
    """
    
    def evaluate(
        self, 
        current: CellState, 
        left: CellState | None, 
        right: CellState | None
    ) -> CellState:
        """Compute next state from current state and neighbor states."""
        ...

class PropagationRule:
    """
    Propagate ACTIVE state within max_distance of an active neighbor.
    
    Reference behavior per DDF ARCHITECTURE.md §4.4:
    
    "If at least one neighbor is CELL_TYPE_ACTIVE and the local parameter is
    strictly less than MAX_ACTIVE_DISTANCE, the cell is biased toward
    CELL_TYPE_ACTIVE and may increase its fitness up to a bounded maximum.
    Otherwise, the cell is biased toward CELL_TYPE_INACTIVE and its fitness
    decays deterministically toward zero."
    
    Expected attractor for 4-cell reference scenario:
    [ACTIVE, ACTIVE, INACTIVE, INACTIVE]
    """
    
    def __init__(self, max_distance: int = 2, max_fitness: int = 255):
        self.max_distance = max_distance
        self.max_fitness = max_fitness
    
    def evaluate(
        self, 
        current: CellState, 
        left: CellState | None, 
        right: CellState | None
    ) -> CellState:
        # Check if either neighbor is ACTIVE
        neighbor_active = (
            (left is not None and left.cell_type == CELL_ACTIVE) or
            (right is not None and right.cell_type == CELL_ACTIVE)
        )
        
        # Check if within propagation distance
        within_distance = current.cell_param < self.max_distance
        
        if neighbor_active and within_distance:
            # Become/stay ACTIVE, increment fitness (clamped)
            new_type = CELL_ACTIVE
            new_fitness = min(current.fitness + 1, self.max_fitness)
        else:
            # Become/stay INACTIVE, decay fitness (clamped)
            new_type = CELL_INACTIVE
            new_fitness = max(current.fitness - 1, 0)
        
        return CellState(
            cell_type=new_type,
            cell_param=current.cell_param,  # Param is configuration, immutable
            fitness=new_fitness
        )
```
#### 4.2.4 Engine Implementation

```python
class CellularEngine:
    """
    Cellular projection engine using local rules and self-organization.
    
    Implements CPSC-Specification.md §12 constraint fabric pattern in software.
    """
    
    def __init__(
        self,
        max_cycles: int = 32,
        stability_window: int = 4,
        max_propagation: int = 2,
        boundary: str = 'active_left'
    ):
        self.max_cycles = max_cycles
        self.stability_window = stability_window
        self.rule = PropagationRule(max_distance=max_propagation)
        self.boundary = boundary
    
    def solve(self, model: CasModel, dof_values: Sequence[float]) -> ProjectionResult:
        """
        Project DoF values via cellular self-organization.
        
        Process:
        1. Configure grid from DoF values
        2. Run cycles: OBSERVE → COMPUTE → APPLY
        3. Detect convergence or reach max_cycles
        4. Extract final state from cell types
        """
        # 1. Configure grid from DoF
        n_cells = len(dof_values)
        params = [int(v) for v in dof_values]
        grid = Grid1D(n_cells=n_cells, params=params, boundary=self.boundary)
        
        # 2. Create cycle controller
        controller = CycleController(
            max_cycles=self.max_cycles,
            stability_window=self.stability_window
        )
        
        # 3. Run cycles until convergence or max
        while True:
            grid.observe()              # Phase 1: Read neighbor states
            grid.compute(self.rule)     # Phase 2: Evaluate local rules
            grid.apply()                # Phase 3: Commit atomically
            
            if not controller.step(grid):
                break
        
        # 4. Build result
        final_types = grid.get_types()
        final_fitness = grid.get_fitness()
        state = self._build_state_vector(model, final_types, grid)
        
        return ProjectionResult(
            success=controller.converged,
            state=state,
            iterations=controller.cycle,
            max_violation=0.0 if controller.converged else float('inf'),
            details={
                'final_types': final_types,
                'final_fitness': final_fitness,
                'stable_cycles': controller._stable_count
            },
            reason=None if controller.converged else 'MAX_CYCLES_REACHED'
        )
    
    def solve_from_dlif(self, stream: 'DlifStream', model: CasModel) -> ProjectionResult:
        """
        Project from DLIF stream via cellular self-organization.
        
        See §10 for DLIF format specification.
        """
        # Parse header to determine grid size
        header = stream.read_header()
        n_cells = header.element_count
        
        # Create grid
        grid = Grid1D(n_cells=n_cells, params=[0]*n_cells, boundary=self.boundary)
        
        # Stream configuration elements into grid
        grid.configure_from_dlif(stream)
        
        # Run cycles (same as solve())
        controller = CycleController(self.max_cycles, self.stability_window)
        while True:
            grid.observe()
            grid.compute(self.rule)
            grid.apply()
            if not controller.step(grid):
                break
        
        # Build result
        return self._build_result(grid, controller, model)
    
    def _build_state_vector(self, model: CasModel, types: list[int], grid: Grid1D) -> StateVector:
        """Map cell types back to CAS model variables."""
        state = StateVector(values={})
        for i, var_name in enumerate(model.free_variables):
            if i < len(types):
                state[var_name] = float(types[i])
        return state
```
#### 4.2.5 Thread Safety

- `CellState` is immutable (`frozen=True`) and thread-safe
- `Cell` instances are NOT thread-safe; exclusive access required during cycles
- `Grid1D` is NOT thread-safe during cycle execution
- `LocalRule` implementations MUST be stateless and thread-safe
- `CellularEngine` instances are stateless and thread-safe

---

### 4.3 Hardware Embodiment

#### 4.3.1 Architecture

Per CPSC-Specification.md §12 and Binary-Format-RTL-Mapping.md §8:

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                 Cellular Projection Core                 │
                    ├─────────────────────────────────────────────────────────┤
                    │                                                          │
                    │  ┌────────────────────────────────────────────────────┐ │
  s_axis_dlif_*────▶│  │              DLIF Stream Decoder                   │ │
                    │  │  - Parses DLIF header and elements                 │ │
                    │  │  - Routes CONFIG to cell param registers           │ │
                    │  │  - Signals ready for cycle execution               │ │
                    │  └──────────────────────┬─────────────────────────────┘ │
                    │                         │ cell_param[N-1:0]             │
                    │  ┌──────────────────────▼─────────────────────────────┐ │
                    │  │              Cell Array (N cells)                   │ │
                    │  │                                                     │ │
                    │  │  ┌──────┐   ┌──────┐   ┌──────┐       ┌──────┐    │ │
                    │  │  │Cell₀ │◀─▶│Cell₁ │◀─▶│Cell₂ │ ...  │CellN₋₁│    │ │
                    │  │  └──┬───┘   └──┬───┘   └──┬───┘       └──┬───┘    │ │
                    │  │     │          │          │              │         │ │
                    │  │     ▼          ▼          ▼              ▼         │ │
                    │  │  type[0]    type[1]    type[2]       type[N-1]    │ │
                    │  └────────────────────────────────────────────────────┘ │
                    │           │                                    │        │
      boundary_l───▶│           │    neighbor_bus (directly wired)   │        │
      boundary_r───▶│           ▼                                    ▼        │
                    │  ┌────────────────────────────────────────────────────┐ │
                    │  │              Neighbor Router                        │ │
                    │  │  - cell[i].right_in ← cell[i+1].type_out           │ │
                    │  │  - cell[i].left_in  ← cell[i-1].type_out           │ │
                    │  │  - Boundary injection at edges                     │ │
                    │  └────────────────────────────────────────────────────┘ │
                    │                                                          │
  clk ─────────────▶│  ┌────────────────────────────────────────────────────┐ │
  rst_n ───────────▶│  │              Cycle Controller                       │ │
  start ───────────▶│  │  FSM: IDLE → LOAD → OBSERVE → COMPUTE → APPLY →    │ │──▶ done
  max_cycles[7:0]──▶│  │       (loop)                              → DONE   │ │──▶ converged
  stab_window[3:0]─▶│  │  Phase strobes: ph_observe, ph_compute, ph_apply   │ │──▶ cycle[7:0]
                    │  └────────────────────────────────────────────────────┘ │
                    │                                                          │
                    │  ┌────────────────────────────────────────────────────┐ │
                    │  │              Stability Detector                     │ │
                    │  │  - Shadow register of previous cycle types         │ │
                    │  │  - Comparator: types_current == types_previous     │ │
                    │  │  - Stability counter with window threshold         │ │
                    │  └────────────────────────────────────────────────────┘ │
                    └──────────────────────────────────────────┬──────────────┘
                                                               │
                                                               ▼
                                                   types_out[N×2-1:0]
                                                   fitness_out[N×F-1:0]
```
#### 4.3.2 Signal Definitions

**Input Ports:**

| Signal               | Width | Description                      | Source      |
| -------------------- | ----- | -------------------------------- | ----------- |
| `clk`                | 1     | System clock                     | —           |
| `rst_n`              | 1     | Active-low synchronous reset     | —           |
| `start`              | 1     | Begin projection (pulse)         | Control     |
| `s_axis_dlif_tdata`  | 32    | DLIF stream data                 | AXI4-Stream |
| `s_axis_dlif_tvalid` | 1     | DLIF data valid                  | AXI4-Stream |
| `s_axis_dlif_tlast`  | 1     | DLIF end of stream               | AXI4-Stream |
| `max_cycles`         | 8     | Maximum cycle count              | CAS config  |
| `stab_window`        | 4     | Stability window for convergence | CAS config  |
| `boundary_l`         | 2     | Left virtual neighbor type       | Config      |
| `boundary_r`         | 2     | Right virtual neighbor type      | Config      |
| `max_distance`       | 8     | Propagation distance threshold   | CAS config  |
**Output Ports:**

| Signal               | Width | Description                            |
| -------------------- | ----- | -------------------------------------- |
| `s_axis_dlif_tready` | 1     | Ready to accept DLIF data              |
| `done`               | 1     | Projection complete (pulse)            |
| `converged`          | 1     | 1=pattern stable, 0=max_cycles reached |
| `cycle`              | 8     | Final cycle count                      |
| `types_out`          | N×2   | Cell types, packed (2 bits per cell)   |
| `fitness_out`        | N×F   | Cell fitness values, packed            |
#### 4.3.3 Cell RTL Module

```vhdl
-------------------------------------------------------------------------------
-- cell.vhd
-- Cellular Engine - Single cell with double-buffered state
--
-- Implements CPSC-Specification.md §12 proto-cell semantics:
-- - Local configuration and state registers
-- - Neighbor signal exchange
-- - Fixed local update rules
-- - Commit-only state updates
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity cell is
  generic (
    PARAM_WIDTH   : positive := 8;   -- Cell parameter bit width
    FITNESS_WIDTH : positive := 8;   -- Fitness accumulator bit width
    MAX_DISTANCE  : positive := 2    -- Propagation distance threshold
  );
  port (
    clk           : in  std_logic;
    rst_n         : in  std_logic;
    
    -- Phase strobes from cycle controller (directly from FSM)
    ph_observe    : in  std_logic;   -- Latch neighbor states
    ph_compute    : in  std_logic;   -- Evaluate local rule (active during OBSERVE)
    ph_apply      : in  std_logic;   -- Commit next state
    
    -- Configuration (loaded from DLIF, static during cycles)
    cell_param    : in  std_logic_vector(PARAM_WIDTH-1 downto 0);
    
    -- Neighbor inputs (directly wired from adjacent cells)
    neighbor_l    : in  std_logic_vector(1 downto 0);  -- Left neighbor type
    neighbor_r    : in  std_logic_vector(1 downto 0);  -- Right neighbor type
    
    -- Current state output (directly wired to adjacent cells)
    cell_type     : out std_logic_vector(1 downto 0);
    cell_fitness  : out std_logic_vector(FITNESS_WIDTH-1 downto 0)
  );
end entity;

architecture rtl of cell is
  -- Type encoding (matches software constants)
  constant TYPE_INACTIVE : std_logic_vector(1 downto 0) := "00";
  constant TYPE_ACTIVE   : std_logic_vector(1 downto 0) := "01";
  
  -- Double-buffered state registers
  signal type_reg      : std_logic_vector(1 downto 0) := TYPE_INACTIVE;
  signal type_next     : std_logic_vector(1 downto 0);
  signal fitness_reg   : unsigned(FITNESS_WIDTH-1 downto 0) := (others => '0');
  signal fitness_next  : unsigned(FITNESS_WIDTH-1 downto 0);
  
  -- Latched neighbor state (captured during OBSERVE phase)
  signal neighbor_l_q  : std_logic_vector(1 downto 0) := TYPE_INACTIVE;
  signal neighbor_r_q  : std_logic_vector(1 downto 0) := TYPE_INACTIVE;
  
begin

  -- Output current committed state (directly drives neighbor inputs)
  cell_type    <= type_reg;
  cell_fitness <= std_logic_vector(fitness_reg);
  
  -----------------------------------------------------------------------------
  -- OBSERVE phase: Latch neighbor states
  -- Per CPSC §12: "exchanges signals with neighboring proto-cells"
  -----------------------------------------------------------------------------
  process(clk)
  begin
    if rising_edge(clk) then
      if rst_n = '0' then
        neighbor_l_q <= TYPE_INACTIVE;
        neighbor_r_q <= TYPE_INACTIVE;
      elsif ph_observe = '1' then
        neighbor_l_q <= neighbor_l;
        neighbor_r_q <= neighbor_r;
      end if;
    end if;
  end process;
  
  -----------------------------------------------------------------------------
  -- COMPUTE phase: Combinational local rule evaluation
  -- Per CPSC §12: "applies fixed local update rules"
  --
  -- Implements PropagationRule (DDF ARCHITECTURE.md §4.4):
  -- - If neighbor ACTIVE and param < MAX_DISTANCE → ACTIVE, fitness++
  -- - Otherwise → INACTIVE, fitness--
  -----------------------------------------------------------------------------
  process(type_reg, fitness_reg, neighbor_l_q, neighbor_r_q, cell_param)
    variable neighbor_active : boolean;
    variable within_distance : boolean;
  begin
    -- Check neighbor states
    neighbor_active := (neighbor_l_q = TYPE_ACTIVE) or (neighbor_r_q = TYPE_ACTIVE);
    
    -- Check propagation distance
    within_distance := unsigned(cell_param) < to_unsigned(MAX_DISTANCE, PARAM_WIDTH);
    
    -- Apply local rule
    if neighbor_active and within_distance then
      -- Become/stay ACTIVE
      type_next <= TYPE_ACTIVE;
      -- Increment fitness (saturating)
      if fitness_reg < (2**FITNESS_WIDTH - 1) then
        fitness_next <= fitness_reg + 1;
      else
        fitness_next <= fitness_reg;
      end if;
    else
      -- Become/stay INACTIVE
      type_next <= TYPE_INACTIVE;
      -- Decrement fitness (saturating at zero)
      if fitness_reg > 0 then
        fitness_next <= fitness_reg - 1;
      else
        fitness_next <= fitness_reg;
      end if;
    end if;
  end process;
  
  -----------------------------------------------------------------------------
  -- APPLY phase: Commit next state
  -- Per CPSC §12: "commit-only state updates"
  -----------------------------------------------------------------------------
  process(clk)
  begin
    if rising_edge(clk) then
      if rst_n = '0' then
        type_reg    <= TYPE_INACTIVE;
        fitness_reg <= (others => '0');
      elsif ph_apply = '1' then
        type_reg    <= type_next;
        fitness_reg <= fitness_next;
      end if;
    end if;
  end process;

end architecture;
```
#### 4.3.4 Cycle Controller FSM

```
              ┌──────┐
         ─────│ IDLE │◀────────────────────────────────────┐
        start └──┬───┘                                     │
                 │                                         │
                 ▼                                         │
            ┌─────────┐                                    │
            │  LOAD   │  Accept DLIF stream, load params   │
            └────┬────┘  (wait for s_axis_dlif_tlast)      │
                 │                                         │
                 ▼                                         │
            ┌─────────┐◀──────────────────┐                │
            │ OBSERVE │  ph_observe='1'   │                │
            └────┬────┘                   │                │
                 │                        │ !converged     │
                 ▼                        │ && cycle<max   │
            ┌─────────┐                   │                │
            │  APPLY  │  ph_apply='1'     │                │
            └────┬────┘                   │                │
                 │                        │                │
                 ▼                        │                │
            ┌─────────┐                   │                │
            │  CHECK  │───────────────────┘                │
            └────┬────┘  (stability comparison)            │
                 │                                         │
                 │ converged || cycle>=max                 │
                 ▼                                         │
            ┌─────────┐                                    │
            │  DONE   │────────────────────────────────────┘
            └─────────┘  done='1'
```
Note: COMPUTE is combinational and happens between OBSERVE and APPLY within the same cycle.

#### 4.3.5 Timing

| Phase     | Clock Cycles | Description                                         |
| --------- | ------------ | --------------------------------------------------- |
| LOAD      | Variable     | Stream DLIF elements until `tlast`                  |
| OBSERVE   | 1            | All cells latch neighbor states                     |
| (COMPUTE) | 0            | Combinational, concurrent with OBSERVE→APPLY        |
| APPLY     | 1            | All cells commit next state                         |
| CHECK     | 1            | Compare types to previous, update stability counter |
**Cycles per epoch:** 3 clock cycles (OBSERVE + APPLY + CHECK)

**Example:** N=4 cells, converges at cycle 3, stability_window=4:
- LOAD: ~10 clocks (4 config elements)
- Cycles: 7 cycles × 3 clocks = 21 clocks (need 3+4=7 cycles for stability)
- DONE: 1 clock
- **Total:** ~32 clock cycles

#### 4.3.6 Resource Estimates

Per-cell resources:

| Component    | FFs     | LUTs    | Description             |
| ------------ | ------- | ------- | ----------------------- |
| type_reg     | 2       | 0       | Current type            |
| type_next    | 2       | 4       | Next type (combo logic) |
| fitness_reg  | 8       | 0       | Fitness accumulator     |
| fitness_next | 0       | 8       | Fitness update logic    |
| neighbor_l_q | 2       | 0       | Latched left neighbor   |
| neighbor_r_q | 2       | 0       | Latched right neighbor  |
| **Per cell** | **~16** | **~12** |                         |
**Array totals:**

| Configuration | Cells | Total FFs | Total LUTs |
| ------------- | ----- | --------- | ---------- |
| N=4           | 4     | ~64       | ~48        |
| N=16          | 16    | ~256      | ~192       |
| N=64          | 64    | ~1024     | ~768       |
| N=256         | 256   | ~4096     | ~3072      |
Controller overhead: ~100 FFs, ~150 LUTs (FSM, stability counter, comparator)

---

## 5. Engine Comparison

| Aspect                    | Iterative Engine         | Cellular Engine              |
| ------------------------- | ------------------------ | ---------------------------- |
| **Constraint evaluation** | Global (all constraints) | Local (per cell + neighbors) |
| **State communication**   | Centralized StateVector  | Neighbor-only exchange       |
| **Parallelism model**     | Constraint-parallel      | Cell-parallel                |
| **Best suited for**       | Continuous arithmetic    | Discrete structural          |
| **Convergence method**    | Error minimization       | Pattern stabilization        |
| **HW resource scaling**   | O(M×N) for M constraints | O(N) for N cells             |
| **Streaming support**     | DSIF (block load)        | DLIF (element stream)        |
| **Determinism**           | Via solver parameters    | Via local rules              |
---

## 6. Configuration via CAS-YAML

Per CAS-YAML-Specification.md §10:

### 6.1 Iterative Engine Configuration

```yaml
projection:
  method: iterative          # or: bounded_relaxation, newton, gradient
  max_iterations: 100
  convergence_epsilon: 1e-6

execution:
  deterministic: true
  numeric_mode: float64      # or: float32, fixed_point
  precision_bits: 64
```
### 6.2 Cellular Engine Configuration

```yaml
projection:
  method: cellular           # or: local_rules, self_organizing
  max_iterations: 32         # Interpreted as max_cycles
  convergence_epsilon: 0     # Ignored for cellular; uses stability_window

execution:
  deterministic: true
  numeric_mode: fixed_point
  precision_bits: 16

# Engine-specific extension (optional, not in core CAS-YAML spec)
cellular:
  boundary: active_left      # active_left | inactive | wrap
  max_propagation: 2         # PropagationRule max_distance
  stability_window: 4        # Cycles of stability for convergence
```
---

## 7. Binary Format Integration

### 7.1 DSIF (Block Format)

Per Binary-Format-Specification.md, DSIF is used for:
- Iterative Engine: Full DoF vector loaded at start
- Cellular Engine: Can load cell params from DoF vector (batch mode)

DSIF structure (Binary-Format-Specification.md §3):
```
[Header]           16 bytes - Magic, version, flags, numeric mode
[Model Metadata]   72 bytes - Hashes, DoF count, precision
[Stage Table]      Variable - Pipeline stage descriptors
[DoF Vector]       N×P bits - Packed DoF values
[Residual Stream]  Optional - Residual corrections
```
### 7.2 DSIF-to-Cellular Mapping

When using DSIF with Cellular Engine:
1. DoF vector values map to `cell_param` for each cell
2. `dof_count` determines number of cells
3. `precision_bits` determines `PARAM_WIDTH`

---

## 8. Relationship to Existing Specifications

### 8.1 CPSC-Specification.md

| Section               | This Specification                               |
| --------------------- | ------------------------------------------------ |
| §5 Projection         | Both engines implement projection semantics      |
| §6 Determinism        | Both engines guarantee deterministic convergence |
| §7 Degrees of Freedom | DoF vector initializes both engines              |
| §12 Hardware Guidance | Cellular Engine implements proto-cell fabric     |
### 8.2 CAS-YAML-Specification.md

| Section        | This Specification                                    |
| -------------- | ----------------------------------------------------- |
| §7 State       | Variables map to Iterative state or Cellular cells    |
| §8 Constraints | Iterative uses expressions; Cellular uses local rules |
| §10 Projection | `method` field selects engine mode                    |
| §11 Execution  | `numeric_mode`, `precision_bits` apply to both        |
### 8.3 Binary-Format-Specification.md

| Section            | This Specification                                     |
| ------------------ | ------------------------------------------------------ |
| §7 DoF Vector      | Loads Iterative state or Cellular cell params          |
| §8 Residual Stream | Applied before projection (Iterative only)             |
| §9 Streaming       | DSIF is block-oriented; DLIF (§10) is element-oriented |
### 8.4 Binary-Format-RTL-Mapping.md

| Section              | This Specification                                    |
| -------------------- | ----------------------------------------------------- |
| §6 DoF Mapping       | `dof_regs[]` in Iterative; `cell_param[]` in Cellular |
| §8 Constraint Fabric | Iterative uses CEUs; Cellular uses cell array         |
| §9 FSM               | Both engines use linear FSM (no nested control)       |
---

## 9. Reference Implementation

### 9.1 CAS-Example-Synthetic-Log.yaml Compatibility

The reference model `CAS-Example-Synthetic-Log.yaml` can be processed by either engine:

**Iterative Engine:**
- 4 DoF variables: `t_seconds`, `user`, `action`, `status`
- Constraint: `0.0 <= t_seconds && t_seconds <= 86400.0`
- Bounded relaxation projects to valid state

**Cellular Engine:**
- 4 cells with params derived from DoF values
- PropagationRule with default parameters
- Self-organizes to stable pattern

### 9.2 Expected Behavior

For the reference 4-cell scenario (per DDF ARCHITECTURE.md §4.4):
- Initial: `[INACTIVE, INACTIVE, INACTIVE, INACTIVE]`
- Boundary: Left=ACTIVE (virtual), Right=INACTIVE (virtual)
- Parameters: `[0, 1, 2, 3]` (cell indices)
- MAX_DISTANCE: 2
- Expected attractor: `[ACTIVE, ACTIVE, INACTIVE, INACTIVE]`
- Convergence: Within 8 cycles, stable for 4+ cycles

---

## 10. DLIF (Degrees-of-freedom Line-In Format)

### 10.1 Purpose

DLIF is a **streaming element format** for the Cellular Engine that enables:
- Element-by-element flow through cell arrays
- Runtime configuration without full model reload
- Self-organization based on data distribution
- Hardware-friendly shift-register style processing

DLIF complements DSIF (block format) for streaming-oriented cellular computation.

### 10.2 Design Goals

Per Binary-Format-Specification.md §2 design goals, DLIF is:
- **Deterministic**: Element order defines processing order
- **Streamable**: No lookahead required; process elements as they arrive
- **Hardware-compatible**: Fixed element sizes, no dynamic allocation
- **Minimal**: Small header, simple element encoding

### 10.3 Format Structure

```
┌─────────────────────────────────────┐
│            DLIF Stream              │
├─────────────────────────────────────┤
│  [Header]         8 bytes           │
│  [Element₀]       4 bytes           │
│  [Element₁]       4 bytes           │
│  ...                                │
│  [Elementₙ₋₁]     4 bytes           │
│  [End Marker]     4 bytes           │
└─────────────────────────────────────┘
```
### 10.4 Header Format

| Field         | Offset | Size    | Description                         |
| ------------- | ------ | ------- | ----------------------------------- |
| Magic         | 0      | 4 bytes | ASCII "DLIF" (0x444C4946)           |
| Version       | 4      | 1 byte  | Format version (1)                  |
| Flags         | 5      | 1 byte  | Feature flags                       |
| Element Count | 6      | 2 bytes | Number of elements following header |
**Total header size:** 8 bytes

**Flags:**
- Bit 0: Has end marker (1) or implicit end (0)
- Bits 1-7: Reserved (must be zero)

### 10.5 Element Format

Each element is 4 bytes (32 bits):

```
┌─────────────────────────────────────┐
│  31..28  │  27..16   │   15..0     │
│  Type    │  Index    │   Value     │
│  (4 bit) │  (12 bit) │  (16 bit)   │
└─────────────────────────────────────┘
```
| Field | Bits  | Description                                    |
| ----- | ----- | ---------------------------------------------- |
| Type  | 31:28 | Element type (see §10.6)                       |
| Index | 27:16 | Cell index or parameter ID                     |
| Value | 15:0  | Element value (interpretation depends on type) |
### 10.6 Element Types

| Type         | Code | Description                   | Index       | Value                        |
| ------------ | ---- | ----------------------------- | ----------- | ---------------------------- |
| CONFIG_PARAM | 0x0  | Set cell parameter            | Cell index  | Parameter value              |
| CONFIG_TYPE  | 0x1  | Set initial cell type         | Cell index  | Type (0=INACTIVE, 1=ACTIVE)  |
| CONFIG_RULE  | 0x2  | Set rule parameter            | Param ID    | Parameter value              |
| DATA_VALUE   | 0x4  | Data element (shifts through) | Entry point | Data value                   |
| CTRL_SYNC    | 0x8  | Synchronization marker        | —           | Cycle count                  |
| CTRL_RESET   | 0x9  | Reset cells to initial state  | —           | —                            |
| CTRL_RUN     | 0xA  | Begin/continue cycles         | —           | Cycle count (0=until stable) |
| END_MARKER   | 0xF  | End of stream                 | —           | Checksum (optional)          |
### 10.7 Streaming Semantics

#### 10.7.1 Configuration Phase

CONFIG elements are processed before cycles begin:

```
[Header: magic="DLIF", count=6]
[CONFIG_PARAM: index=0, value=0]    # Cell 0 param = 0
[CONFIG_PARAM: index=1, value=1]    # Cell 1 param = 1
[CONFIG_PARAM: index=2, value=2]    # Cell 2 param = 2
[CONFIG_PARAM: index=3, value=3]    # Cell 3 param = 3
[CONFIG_RULE:  index=0, value=2]    # max_distance = 2
[CTRL_RUN:     value=32]            # Run up to 32 cycles
[END_MARKER]
```
#### 10.7.2 Data Streaming (Advanced)

DATA elements can flow through cells during execution:

```
[DATA_VALUE: index=0, value=100]    # Inject at cell 0
[DATA_VALUE: index=0, value=200]    # Next value
[CTRL_SYNC:  value=1]               # Wait for cycle 1 completion
[DATA_VALUE: index=0, value=300]    # Continue streaming
```
Data elements shift through the cell array:
- Cycle N: Data at cell[i]
- Cycle N+1: Data at cell[i+1]

Cells may modify data based on their state (application-specific).

### 10.8 Software Interface

```python
@dataclass
class DlifHeader:
    magic: bytes          # b"DLIF"
    version: int          # 1
    flags: int
    element_count: int

@dataclass  
class DlifElement:
    type: int             # Element type code
    index: int            # Cell index or param ID
    value: int            # Element value

class DlifStream:
    """DLIF stream encoder/decoder."""
    
    @staticmethod
    def encode(elements: list[DlifElement]) -> bytes:
        """Encode elements to DLIF binary stream."""
        header = struct.pack('<4sBBH', b'DLIF', 1, 0x01, len(elements) + 1)
        body = b''.join(
            struct.pack('<I', (e.type << 28) | (e.index << 16) | (e.value & 0xFFFF))
            for e in elements
        )
        end = struct.pack('<I', 0xF0000000)  # END_MARKER
        return header + body + end
    
    @staticmethod
    def decode(blob: bytes) -> Generator[DlifElement, None, None]:
        """Decode DLIF binary stream to elements."""
        magic, version, flags, count = struct.unpack_from('<4sBBH', blob, 0)
        if magic != b'DLIF':
            raise ValueError("Invalid DLIF magic")
        
        offset = 8
        for _ in range(count):
            word, = struct.unpack_from('<I', blob, offset)
            offset += 4
            
            elem_type = (word >> 28) & 0xF
            if elem_type == 0xF:  # END_MARKER
                break
            
            yield DlifElement(
                type=elem_type,
                index=(word >> 16) & 0xFFF,
                value=word & 0xFFFF
            )
    
    @staticmethod
    def from_dof(dof_values: Sequence[float], max_cycles: int = 32) -> bytes:
        """Create DLIF stream from DoF values (convenience method)."""
        elements = [
            DlifElement(type=0x0, index=i, value=int(v))  # CONFIG_PARAM
            for i, v in enumerate(dof_values)
        ]
        elements.append(DlifElement(type=0xA, index=0, value=max_cycles))  # CTRL_RUN
        return DlifStream.encode(elements)
```
### 10.9 Hardware Interface

#### 10.9.1 AXI4-Stream Interface

DLIF streams are transported via AXI4-Stream:

| Signal               | Width | Description                             |
| -------------------- | ----- | --------------------------------------- |
| `s_axis_dlif_tdata`  | 32    | Element data (header words or elements) |
| `s_axis_dlif_tvalid` | 1     | Data valid                              |
| `s_axis_dlif_tready` | 1     | Ready to accept                         |
| `s_axis_dlif_tlast`  | 1     | Last element in stream                  |
#### 10.9.2 DLIF Decoder RTL

```vhdl
entity dlif_decoder is
  generic (
    N_CELLS     : positive := 4;
    PARAM_WIDTH : positive := 16
  );
  port (
    clk               : in  std_logic;
    rst_n             : in  std_logic;
    
    -- AXI4-Stream input
    s_axis_tdata      : in  std_logic_vector(31 downto 0);
    s_axis_tvalid     : in  std_logic;
    s_axis_tready     : out std_logic;
    s_axis_tlast      : in  std_logic;
    
    -- Configuration outputs (directly to cell array)
    cell_param        : out std_logic_vector(N_CELLS*PARAM_WIDTH-1 downto 0);
    cell_param_valid  : out std_logic_vector(N_CELLS-1 downto 0);
    
    -- Control outputs
    cfg_done          : out std_logic;  -- All config received
    run_cycles        : out std_logic_vector(7 downto 0);
    run_start         : out std_logic
  );
end entity;
```
### 10.10 DLIF vs DSIF Comparison

| Aspect             | DSIF                                 | DLIF                             |
| ------------------ | ------------------------------------ | -------------------------------- |
| **Orientation**    | Block (complete state)               | Stream (element-by-element)      |
| **Header size**    | 16 bytes + 72 bytes metadata         | 8 bytes                          |
| **Element size**   | Variable (precision-dependent)       | Fixed 4 bytes                    |
| **Use case**       | Initial configuration, checkpointing | Streaming input, runtime updates |
| **Engine support** | Both (Iterative preferred)           | Cellular only                    |
| **HW interface**   | AXI4 DMA / register load             | AXI4-Stream                      |
### 10.11 DLIF Conformance

An implementation claiming DLIF conformance MUST:
1. Parse header magic "DLIF" and version 1
2. Process CONFIG_PARAM elements to configure cells
3. Process CTRL_RUN to initiate cycle execution
4. Process END_MARKER or `tlast` as stream termination
5. Reject unknown element types with an error

An implementation MAY:
1. Support DATA_VALUE streaming during execution
2. Support CTRL_SYNC for cycle synchronization
3. Support CTRL_RESET for runtime reset
4. Extend with additional element types (codes 0xC-0xE reserved)

---

## 11. Conformance

### 11.1 Mandatory Requirements

An implementation claiming conformance to this specification MUST:

1. Implement at least one engine mode (Iterative or Cellular)
2. Produce deterministic results for identical inputs (per CPSC-Specification.md §6)
3. Respect `max_iterations` / `max_cycles` bounds from CAS-YAML
4. Report success/failure accurately in ProjectionResult
5. Document which engine modes and features are supported
6. Follow CPSC-Implementation-Governance.md §2 spec-first workflow

### 11.2 Optional Features

Implementations MAY:
1. Support both engine modes with runtime selection
2. Implement additional local rules for Cellular Engine
3. Support 2D grids for Cellular Engine
4. Implement DLIF streaming (§10)
5. Provide engine-specific configuration extensions

### 11.3 Implementation Notes

Per CPSC-Implementation-Governance.md §3:
- Numeric modes and precision MUST be explicit
- Convergence criteria MUST be declared
- Changes affecting determinism MUST be documented

---

## 12. References

| Document                            | Description                        |
| ----------------------------------- | ---------------------------------- |
| `CPSC-Specification.md`             | Core CPSC computation model        |
| `CAS-YAML-Specification.md`         | Constraint model definition format |
| `Binary-Format-Specification.md`    | DSIF binary interchange format     |
| `Binary-Format-RTL-Mapping.md`      | Hardware signal-level mapping      |
| `CPSC-Implementation-Governance.md` | Development practices              |
| `CAS-Example-Synthetic-Log.yaml`    | Reference 4-variable CAS model     |
