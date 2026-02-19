# CPSC-Guided MAX-SAT Architecture
## Constraint-Projected Acceleration for Exact Solving

**Version:** 0.1.0-draft  
**Status:** Research Specification  
**Last Updated:** 2026-02-19

---

## 1. Overview

This specification defines an architecture for accelerating exact MAX-SAT solving using CPSC (Constraint-Projected State Computing) as a guidance layer. The approach preserves the completeness guarantees of core-guided solvers like RC2 while using constraint projection to reduce the number of SAT oracle calls required.

### 1.1 Design Philosophy

**CPSC does not replace the SAT solver.** Instead, it provides:
1. **Structural preprocessing** — Analyze constraint graph to inform solving strategy
2. **Core prediction** — Project likely conflict sets before SAT calls
3. **Relaxation guidance** — Order relaxation variables by projected impact
4. **Incremental state** — Maintain projection state across iterations

### 1.2 Target Problem

**Weighted Partial MAX-SAT:**
- Hard clauses (must satisfy)
- Soft clauses (satisfy if possible, minimize weight of unsatisfied)
- Find assignment minimizing total weight of unsatisfied soft clauses

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CPSC-MAXSAT Solver                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                     Preprocessing Layer                           │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐  │   │
│  │  │ CNF Parser     │  │ Constraint     │  │ Structure          │  │   │
│  │  │                │─▶│ Graph Builder  │─▶│ Classifier         │  │   │
│  │  └────────────────┘  └────────────────┘  └────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    CPSC Projection Engine                         │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐  │   │
│  │  │ Clause-Cell    │  │ Conflict       │  │ Relaxation         │  │   │
│  │  │ State Matrix   │  │ Projector      │  │ Orderer            │  │   │
│  │  └────────────────┘  └────────────────┘  └────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Core-Guided Solver (RC2)                       │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐  │   │
│  │  │ SAT Oracle     │  │ Core           │  │ Cardinality        │  │   │
│  │  │ (incremental)  │  │ Extractor      │  │ Encoder            │  │   │
│  │  └────────────────┘  └────────────────┘  └────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│                            Optimal Assignment                            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. State Model for MAX-SAT

### 3.1 Clause-Cell Matrix

Map the MAX-SAT instance to a CPSC state matrix where:
- Each **row** represents a clause
- Each **column** represents a variable
- Each **cell** encodes the variable's participation in that clause

```
State Matrix S[m × n]:
  - m = number of clauses
  - n = number of variables
  
Cell values:
  S[i,j] = +1  if variable j appears positive in clause i
  S[i,j] = -1  if variable j appears negated in clause i
  S[i,j] =  0  if variable j does not appear in clause i
```

### 3.2 CPSC State Variables

Per CPSC-Specification.md §3, define the state for MAX-SAT:

```yaml
state:
  variables:
    # Variable assignments (Boolean encoded as 0/1)
    - name: x[0..n-1]
      type: int
      domain: [0, 1]
      derived: false
    
    # Clause satisfaction status (derived)
    - name: sat[0..m-1]
      type: int
      domain: [0, 1]
      derived: true
    
    # Relaxation variables for soft clauses
    - name: r[0..k-1]
      type: int
      domain: [0, 1]
      derived: false
    
    # Projected conflict potential (fitness analog)
    - name: conflict_score[0..m-1]
      type: float
      domain: [0.0, 1.0]
      derived: true
```

### 3.3 Constraint Model

```yaml
constraints:
  # Hard clause constraints (must satisfy)
  - id: hard_clause_{i}
    type: hard
    expression: "sat[i] == 1"
    
  # Soft clause constraints (relaxable)
  - id: soft_clause_{i}
    type: soft
    weight: w_i
    expression: "sat[i] == 1 OR r[i] == 1"
    
  # Clause satisfaction definition
  - id: sat_def_{i}
    type: definition
    expression: "sat[i] = (any literal in clause i is true)"
    
  # Objective: minimize sum of relaxation variables (weighted)
  - id: objective
    type: minimize
    expression: "sum(w[i] * r[i] for i in soft_clauses)"
```

---

## 4. CPSC Projection for MAX-SAT

### 4.1 Projection Modes

The CPSC engine operates in two modes for MAX-SAT:

#### 4.1.1 Iterative Mode (Global Analysis)

Use the Iterative Engine (CPSC-Engine-Modes-Specification.md §3) for:
- Global constraint violation analysis
- Gradient-based conflict scoring
- Clause interaction detection

```python
class MaxSatIterativeProjector:
    """
    Global projection for conflict analysis.
    
    Computes conflict_score for each clause based on:
    - Current partial assignment
    - Constraint graph structure
    - Historical core membership
    """
    
    def project(self, state: MaxSatState) -> ProjectionResult:
        # 1. Evaluate all clauses under current assignment
        violations = self._evaluate_clauses(state)
        
        # 2. Compute conflict scores via constraint propagation
        conflict_scores = self._propagate_conflicts(violations)
        
        # 3. Identify high-confidence conflict clusters
        predicted_cores = self._cluster_conflicts(conflict_scores)
        
        return ProjectionResult(
            state=state,
            conflict_scores=conflict_scores,
            predicted_cores=predicted_cores
        )
```

#### 4.1.2 Cellular Mode (Local Propagation)

Use the Cellular Engine (CPSC-Engine-Modes-Specification.md §4) for:
- Unit propagation simulation
- Local conflict cascade detection
- Neighbor-based constraint interaction

```python
class MaxSatCellularProjector:
    """
    Cellular projection for conflict propagation.
    
    Each cell represents a clause. Cells communicate conflict
    potential based on shared variables (neighbors).
    """
    
    def __init__(self):
        self.rule = ConflictPropagationRule()
    
    def project(self, state: MaxSatState) -> ProjectionResult:
        # Build clause-clause adjacency from shared variables
        grid = self._build_clause_grid(state)
        
        # Run cellular cycles until stable
        controller = CycleController(max_cycles=16, stability_window=3)
        while not controller.converged:
            grid.observe()   # Read neighbor conflict scores
            grid.compute(self.rule)  # Propagate conflicts
            grid.apply()     # Commit
            controller.step(grid)
        
        return self._extract_predictions(grid)
```

### 4.2 Conflict Propagation Rule

Per CPSC-Engine-Modes-Specification.md §4.2.6 LocalRule protocol:

```python
class ConflictPropagationRule:
    """
    Local rule for MAX-SAT conflict propagation.
    
    A clause's conflict potential increases if:
    - Its current satisfaction is uncertain (undecided variables)
    - Neighboring clauses (shared variables) have high conflict scores
    - Historical cores included this clause
    """
    
    def __init__(self, decay: float = 0.9, boost: float = 0.2):
        self.decay = decay
        self.boost = boost
    
    def evaluate(
        self,
        current: ClauseCellState,
        neighbors: list[ClauseCellState]
    ) -> ClauseCellState:
        # Decay existing score
        new_score = current.conflict_score * self.decay
        
        # Boost from unsatisfied neighbors
        for neighbor in neighbors:
            if neighbor.satisfied == False:
                new_score += self.boost * neighbor.conflict_score
        
        # Boost from shared variable conflicts
        shared_conflict = self._compute_shared_variable_tension(current, neighbors)
        new_score += shared_conflict
        
        # Clamp to [0, 1]
        new_score = max(0.0, min(1.0, new_score))
        
        return ClauseCellState(
            clause_id=current.clause_id,
            satisfied=current.satisfied,
            conflict_score=new_score,
            core_count=current.core_count
        )
```

---

## 5. Integration with RC2 Solver

### 5.1 RC2 Algorithm Overview

Standard RC2 core-guided MAX-SAT:

```
1. Initialize: formula F, cost = 0
2. While SAT(F):
   - If SAT: return assignment (optimal)
3. If UNSAT:
   - Extract core κ from F
   - Add relaxation variables to κ
   - Add cardinality constraint: AtMost(1, relaxations in κ)
   - cost += 1
   - Goto 2
```

### 5.2 CPSC-Guided RC2

Insert CPSC projection as a guidance layer:

```python
class CPSCGuidedRC2:
    """
    RC2 MAX-SAT solver with CPSC projection guidance.
    
    CPSC does not affect correctness (completeness preserved).
    CPSC reduces SAT calls by:
    1. Predicting likely cores before SAT call
    2. Ordering relaxation variables by projected impact
    3. Pruning obviously satisfiable subproblems
    """
    
    def __init__(self, sat_oracle: SATSolver, projector: MaxSatProjector):
        self.sat = sat_oracle
        self.projector = projector
        self.stats = SolverStats()
    
    def solve(self, formula: CNF, weights: dict[int, float]) -> MaxSatResult:
        state = MaxSatState.from_cnf(formula, weights)
        cost = 0.0
        
        while True:
            # === CPSC GUIDANCE PHASE ===
            projection = self.projector.project(state)
            
            # Check if CPSC predicts satisfiability
            if projection.likely_sat and self._validate_prediction(projection):
                # Skip SAT call, trust projection (with verification)
                self.stats.sat_calls_avoided += 1
                assignment = projection.suggested_assignment
                if self._verify_assignment(formula, assignment):
                    return MaxSatResult(assignment=assignment, cost=cost)
            
            # Order assumptions by projected conflict score
            assumptions = self._order_assumptions(state, projection)
            
            # === SAT ORACLE PHASE ===
            result = self.sat.solve(formula, assumptions=assumptions)
            self.stats.sat_calls += 1
            
            if result.satisfiable:
                return MaxSatResult(assignment=result.model, cost=cost)
            
            # === CORE EXTRACTION ===
            core = result.unsat_core
            
            # Update CPSC state with core information (learning)
            self.projector.update_with_core(core)
            
            # === RELAXATION (guided by CPSC) ===
            relaxation_order = self._cpsc_relaxation_order(core, projection)
            self._add_relaxations(formula, core, relaxation_order)
            cost += min(weights[c] for c in core)
    
    def _order_assumptions(
        self, 
        state: MaxSatState, 
        projection: ProjectionResult
    ) -> list[int]:
        """
        Order assumptions to help SAT solver find conflicts faster.
        
        High conflict_score clauses should be checked first.
        This improves core quality (smaller, more relevant).
        """
        scored = [
            (clause_id, projection.conflict_scores[clause_id])
            for clause_id in state.soft_clause_ids
        ]
        # Sort descending by conflict score
        scored.sort(key=lambda x: -x[1])
        return [clause_id for clause_id, _ in scored]
    
    def _cpsc_relaxation_order(
        self,
        core: list[int],
        projection: ProjectionResult
    ) -> list[int]:
        """
        Order relaxation variables within a core.
        
        CPSC guidance: relax clauses with highest projected
        conflict potential first (they're likely to conflict again).
        """
        scored = [
            (clause_id, projection.conflict_scores.get(clause_id, 0.0))
            for clause_id in core
        ]
        scored.sort(key=lambda x: -x[1])
        return [clause_id for clause_id, _ in scored]
```

### 5.3 Incremental State Maintenance

Key optimization: maintain CPSC state across RC2 iterations.

```python
class IncrementalMaxSatProjector:
    """
    Maintains projection state incrementally across solver iterations.
    
    Per CPSC-Specification.md §8: "Each stage MUST be explicitly declared
    and reconstructible." The incremental state tracks:
    - Historical core membership counts
    - Accumulated conflict scores
    - Variable activity (how often in cores)
    """
    
    def __init__(self, base_projector: MaxSatProjector):
        self.base = base_projector
        self.core_history: list[set[int]] = []
        self.clause_core_count: dict[int, int] = defaultdict(int)
        self.variable_activity: dict[int, float] = defaultdict(float)
    
    def update_with_core(self, core: set[int]) -> None:
        """
        Update incremental state when a new core is extracted.
        
        This is the key learning mechanism:
        - Clauses in cores increase their conflict_score base
        - Variables in core clauses increase their activity
        """
        self.core_history.append(core)
        
        for clause_id in core:
            self.clause_core_count[clause_id] += 1
            
            # Increase activity of variables in this clause
            for var in self._get_clause_variables(clause_id):
                self.variable_activity[abs(var)] += 1.0
    
    def project(self, state: MaxSatState) -> ProjectionResult:
        """
        Project with historical information.
        """
        # Get base projection
        result = self.base.project(state)
        
        # Augment with historical core information
        for clause_id, score in result.conflict_scores.items():
            history_boost = self.clause_core_count[clause_id] * 0.1
            result.conflict_scores[clause_id] = min(1.0, score + history_boost)
        
        return result
```

---

## 6. Matrix Engine Implementation

### 6.1 Clause-Variable Matrix Operations

```python
class ClauseVariableMatrix:
    """
    Matrix representation of CNF formula for CPSC operations.
    
    Sparse matrix where:
    - Rows = clauses
    - Columns = variables
    - Values = polarity (+1, -1, 0)
    """
    
    def __init__(self, n_clauses: int, n_vars: int):
        self.n_clauses = n_clauses
        self.n_vars = n_vars
        # Sparse representation: clause_id -> list[(var_id, polarity)]
        self.clauses: dict[int, list[tuple[int, int]]] = {}
        # Inverted index: var_id -> list[(clause_id, polarity)]
        self.var_to_clauses: dict[int, list[tuple[int, int]]] = defaultdict(list)
    
    def add_clause(self, clause_id: int, literals: list[int]) -> None:
        """Add a clause: literals are signed (positive = true, negative = negated)."""
        self.clauses[clause_id] = []
        for lit in literals:
            var_id = abs(lit)
            polarity = 1 if lit > 0 else -1
            self.clauses[clause_id].append((var_id, polarity))
            self.var_to_clauses[var_id].append((clause_id, polarity))
    
    def clause_adjacency(self) -> dict[int, set[int]]:
        """
        Build clause-clause adjacency based on shared variables.
        
        Two clauses are adjacent if they share at least one variable.
        This defines the neighbor topology for cellular projection.
        """
        adjacency: dict[int, set[int]] = defaultdict(set)
        
        for var_id, clause_list in self.var_to_clauses.items():
            clause_ids = [cid for cid, _ in clause_list]
            for i, cid1 in enumerate(clause_ids):
                for cid2 in clause_ids[i+1:]:
                    adjacency[cid1].add(cid2)
                    adjacency[cid2].add(cid1)
        
        return adjacency
    
    def variable_clause_tension(self, var_id: int, assignment: dict[int, bool]) -> float:
        """
        Compute tension for a variable based on clause requirements.
        
        Tension = fraction of clauses that would prefer opposite polarity.
        High tension variables are likely to be in conflicts.
        """
        if var_id not in self.var_to_clauses:
            return 0.0
        
        prefer_true = 0
        prefer_false = 0
        
        for clause_id, polarity in self.var_to_clauses[var_id]:
            # Check if clause is already satisfied by other literals
            if self._clause_satisfied_without(clause_id, var_id, assignment):
                continue
            
            # This clause needs this variable
            if polarity > 0:
                prefer_true += 1
            else:
                prefer_false += 1
        
        total = prefer_true + prefer_false
        if total == 0:
            return 0.0
        
        # Tension is how balanced the preferences are
        # Max tension = 0.5 (equal preference for true and false)
        return min(prefer_true, prefer_false) / total
```

### 6.2 CPSC Grid Mapping

Map clauses to a cellular grid for conflict propagation:

```python
class MaxSatGrid(Grid):
    """
    Grid implementation for MAX-SAT clause cells.
    
    Topology: clause-clause adjacency based on shared variables.
    This is a GraphGrid where edges are defined by shared variables.
    """
    
    def __init__(self, matrix: ClauseVariableMatrix, weights: dict[int, float]):
        self.matrix = matrix
        self.weights = weights
        
        # Build adjacency graph
        adjacency = matrix.clause_adjacency()
        
        # Create cells for each clause
        self.cells: dict[int, ClauseCell] = {}
        for clause_id in matrix.clauses:
            self.cells[clause_id] = ClauseCell(
                clause_id=clause_id,
                weight=weights.get(clause_id, 1.0),
                neighbors=list(adjacency.get(clause_id, set()))
            )
    
    def get_neighbors(self, clause_id: int) -> list[ClauseCellState]:
        """Get neighbor states for cellular rule evaluation."""
        cell = self.cells[clause_id]
        return [self.cells[n].state for n in cell.neighbors if n in self.cells]
    
    def observe(self) -> None:
        """OBSERVE phase: cache neighbor states."""
        for cell in self.cells.values():
            cell.observe(self.get_neighbors(cell.clause_id))
    
    def compute(self, rule: LocalRule) -> None:
        """COMPUTE phase: evaluate local rule."""
        for cell in self.cells.values():
            cell.compute(rule)
    
    def apply(self) -> None:
        """APPLY phase: commit state changes."""
        for cell in self.cells.values():
            cell.apply()
```

---

## 7. Ideal Variation: Predictive Core Projection

### 7.1 Core Prediction via Constraint Projection

The "ideal" CPSC-MAXSAT would predict UNSAT cores before calling the SAT solver:

```python
class PredictiveCoreProjector:
    """
    Ideal variation: predict UNSAT cores via constraint projection.
    
    Key insight: UNSAT cores are minimal unsatisfiable subsets.
    CPSC can project which clause combinations are likely to conflict
    by simulating constraint propagation without full SAT solving.
    
    This is approximate but can dramatically reduce SAT calls when accurate.
    """
    
    def predict_cores(
        self, 
        state: MaxSatState,
        k: int = 3  # Number of cores to predict
    ) -> list[set[int]]:
        """
        Predict k most likely UNSAT cores.
        
        Algorithm:
        1. Project conflict scores for all clauses
        2. Cluster high-conflict clauses by variable overlap
        3. For each cluster, check minimality (no proper subset is UNSAT)
        4. Return top-k clusters ordered by confidence
        """
        # 1. Get conflict scores
        projection = self.project(state)
        
        # 2. Filter to high-conflict clauses
        threshold = self._adaptive_threshold(projection.conflict_scores)
        candidates = {
            cid for cid, score in projection.conflict_scores.items()
            if score > threshold
        }
        
        # 3. Cluster by variable overlap
        clusters = self._cluster_by_overlap(candidates, state.matrix)
        
        # 4. Score and rank clusters
        scored_clusters = []
        for cluster in clusters:
            confidence = self._estimate_unsat_probability(cluster, state)
            scored_clusters.append((cluster, confidence))
        
        scored_clusters.sort(key=lambda x: -x[1])
        
        return [cluster for cluster, _ in scored_clusters[:k]]
    
    def _estimate_unsat_probability(
        self, 
        clause_set: set[int], 
        state: MaxSatState
    ) -> float:
        """
        Estimate probability that clause_set is UNSAT.
        
        Uses CPSC projection to simulate constraint propagation:
        - Extract subformula for clause_set
        - Run projection to convergence
        - If converges to invalid state, high UNSAT probability
        """
        # Create sub-state for clause subset
        sub_state = state.restrict_to_clauses(clause_set)
        
        # Run projection
        result = self.iterative_engine.solve(
            sub_state.to_cas_model(),
            sub_state.initial_dof(),
            max_iterations=10  # Quick check
        )
        
        if not result.success:
            # Projection failed to converge = likely UNSAT
            return 0.9
        elif result.max_violation > 0.1:
            # High residual violation = possibly UNSAT
            return 0.5 + 0.4 * result.max_violation
        else:
            # Clean convergence = likely SAT
            return 0.1
```

### 7.2 Proactive Relaxation

Instead of waiting for core extraction, proactively relax predicted conflicts:

```python
class ProactiveRelaxationStrategy:
    """
    Proactively add relaxation variables based on CPSC predictions.
    
    Trade-off:
    - More relaxations = fewer SAT calls but potentially suboptimal
    - Must verify optimality at end
    
    This is sound because RC2 correctness doesn't depend on
    which clauses have relaxation variables, only on the
    cardinality constraints added when cores are found.
    """
    
    def suggest_relaxations(
        self,
        state: MaxSatState,
        predictor: PredictiveCoreProjector,
        budget: int = 10
    ) -> list[int]:
        """
        Suggest clauses to add relaxation variables to.
        
        These are soft clauses with high predicted conflict scores
        that are likely to end up relaxed anyway.
        """
        # Get predictions
        predicted_cores = predictor.predict_cores(state, k=3)
        
        # Collect clauses that appear in multiple predicted cores
        clause_counts: dict[int, int] = defaultdict(int)
        for core in predicted_cores:
            for clause_id in core:
                clause_counts[clause_id] += 1
        
        # Sort by frequency in predicted cores
        candidates = sorted(clause_counts.items(), key=lambda x: -x[1])
        
        # Return top budget clauses
        return [cid for cid, _ in candidates[:budget]]
```

---

## 8. Convergence and Correctness

### 8.1 CPSC Convergence (Per CPSC-Specification.md §6)

The CPSC projection layer MUST:
- Converge deterministically under declared bounds
- Produce consistent results given identical inputs
- Report failure if convergence cannot be achieved

For MAX-SAT guidance, convergence failure simply means "no confident prediction" — the solver falls back to standard RC2 behavior.

### 8.2 Solver Correctness (Completeness Preservation)

**Theorem:** CPSC-Guided RC2 is complete (finds optimal solution if one exists).

**Proof sketch:**
1. CPSC guidance only affects assumption ordering and relaxation order
2. The SAT oracle is still called on the full formula
3. Cores are still extracted from the actual formula (not predictions)
4. Cardinality constraints are added based on actual cores
5. Therefore, the RC2 invariants are preserved

CPSC predictions that are wrong simply result in:
- Suboptimal assumption ordering (may find core slower)
- Suboptimal relaxation ordering (same final cost)

Neither affects correctness, only performance.

### 8.3 Optimality Verification

When using proactive relaxation, verify optimality:

```python
def verify_optimality(
    solution: MaxSatResult,
    formula: CNF,
    weights: dict[int, float],
    sat_oracle: SATSolver
) -> bool:
    """
    Verify that a solution is optimal.
    
    Check that no solution exists with lower cost.
    This is a single SAT call with cardinality constraint.
    """
    # Add constraint: cost < current_cost
    verify_formula = formula.copy()
    current_cost = solution.cost
    
    # Add "at most (current_cost - 1) soft clauses can be unsatisfied"
    soft_clause_lits = [relaxation_var(c) for c in formula.soft_clauses]
    verify_formula.add_cardinality(soft_clause_lits, current_cost - 1, "at_most")
    
    result = sat_oracle.solve(verify_formula)
    
    if result.satisfiable:
        # Found better solution — our solution was not optimal
        return False
    else:
        # No better solution exists — optimal confirmed
        return True
```

---

## 9. API Specification

### 9.1 CAS-YAML Schema Extension

Extend CAS-YAML for MAX-SAT problems:

```yaml
cpsc_maxsat:
  version: "1.0"
  
  model:
    format: "cnf"  # Or "wcnf" for weighted
    source: "problem.cnf"
    
  projection:
    mode: "hybrid"  # "iterative", "cellular", or "hybrid"
    max_iterations: 100
    convergence_epsilon: 1e-4
    
    # MAX-SAT specific
    conflict_propagation:
      enabled: true
      decay: 0.9
      boost: 0.2
      
    core_prediction:
      enabled: true
      confidence_threshold: 0.7
      max_predictions: 3
      
  solver:
    backend: "rc2"  # Or "rc2-stratified", "oll", etc.
    incremental: true
    
    # CPSC guidance settings
    cpsc_guidance:
      assumption_ordering: true
      relaxation_ordering: true
      proactive_relaxation: false  # Conservative default
      
  output:
    format: "solution"  # Or "trace" for debugging
    include_stats: true
```

### 9.2 Python API

```python
from cpsc_maxsat import CPSCMaxSatSolver, MaxSatConfig

# Create solver with CPSC guidance
config = MaxSatConfig(
    projection_mode="hybrid",
    core_prediction=True,
    confidence_threshold=0.7
)

solver = CPSCMaxSatSolver(config)

# Solve MAX-SAT instance
result = solver.solve("problem.wcnf")

print(f"Optimal cost: {result.cost}")
print(f"SAT calls: {result.stats.sat_calls}")
print(f"SAT calls avoided: {result.stats.sat_calls_avoided}")
print(f"Core predictions correct: {result.stats.prediction_accuracy:.1%}")
```

---

## 10. Performance Expectations

### 10.1 When CPSC Helps

CPSC guidance is most effective for:
- **Structured problems** — Industrial instances with modular constraint structure
- **Iterative solving** — Problems solved repeatedly with small changes
- **High conflict locality** — Cores tend to involve related clauses

### 10.2 When CPSC Hurts

CPSC overhead may exceed benefit for:
- **Random instances** — No exploitable structure
- **Very small problems** — Projection overhead dominates
- **Single-shot solving** — No opportunity to learn from history

### 10.3 Expected Metrics

| Metric | Baseline RC2 | CPSC-Guided RC2 | Notes |
|--------|--------------|-----------------|-------|
| SAT calls | 100% | 70-90% | Depends on prediction accuracy |
| Time per call | 1x | 1x | SAT solver unchanged |
| CPSC overhead | 0 | 5-15% | Projection computation |
| **Total time** | 1x | 0.8-1.1x | Net effect varies |

The goal is **SAT call reduction > CPSC overhead** for net speedup.

---

## 11. Future Extensions

### 11.1 Hardware Acceleration

Map CPSC-MAXSAT to the Cellular Engine hardware (CPSC-Engine-Modes-Specification.md §4.3):
- Clause cells as hardware cells
- Conflict propagation as local rule
- Parallel projection on FPGA

### 11.2 Portfolio Integration

Combine CPSC guidance with portfolio solvers:
- Use CPSC structure analysis to select solver
- Share learned conflict information across solvers

### 11.3 Anytime Extension

Extend to anytime MAX-SAT:
- CPSC provides intermediate cost bounds
- Progressive refinement of conflict predictions

---

## 12. References

1. **CPSC-Specification.md** — Core CPSC computation model
2. **CPSC-Engine-Modes-Specification.md** — Iterative and Cellular engines
3. **RC2** — Ignatiev, Morgado, Marques-Silva. "RC2: An Efficient MaxSAT Solver" (2019)
4. **pysat** — Python SAT toolkit with RC2 implementation
5. **CAS-YAML-Specification.md** — Constraint model format

---

**CPSC-MAXSAT-Architecture.md** | © 2026 BitConcepts, LLC | Licensed under CPAC Research & Evaluation License v1.0
