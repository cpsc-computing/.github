# CPSC Computing

**Constraint-Projected State Computing — declarative computing through constraint projection.**

CPSC is a computing model in which computation is performed by projecting system state onto explicit constraints, rather than executing ordered instructions. It provides a foundation for deterministic, constraint-driven systems including reasoning engines, compliance enforcement, control systems, and hardware (FPGA/ASIC).

---

## Repositories

- **[cpsc-core](https://github.com/cpsc-computing/cpsc-core)** — CPSC specifications, CAS-YAML format, CGAD governance, and documentation
- **[cpsc-engine-rtl](https://github.com/cpsc-computing/cpsc-engine-rtl)** — CPSC Reasoning Engine (CPSC-RE) implementation — Layers 0–5
- **[cpsc-engine-python](https://github.com/cpsc-computing/cpsc-engine-python)** — Python reference engine for CPSC
- **[cpac](https://github.com/cpsc-computing/cpac)** — Constraint-Projected Adaptive Compression (CPAC) engine (Rust)

### CPAC Benchmark Highlights (v0.3.0)

777 files benchmarked across 8 industry-standard corpora (Canterbury, Silesia, Calgary, enwik8, loghub2_2k, nasa_logs, cloud_configs, kodak). 12 entropy backends, all results verified lossless.

| Corpus | Files | Avg Best Ratio |
|--------|-------|----------------|
| loghub2_2k | 14 | **16.63×** |
| nasa_logs | 4 | **8.56×** |
| canterbury | 11 | **5.84×** |
| silesia | 12 | **4.30×** |
| calgary | 18 | **4.03×** |
| enwik8 | 1 | **3.75×** |

See [CPAC BENCHMARKING.md](https://github.com/cpsc-computing/cpac/blob/develop/docs/BENCHMARKING.md) for full results.

---

## Key Concepts

- **State** — the full configuration of a system
- **Constraints** — rules defining valid states
- **Projection** — resolving state into validity
- **Epoch Cycle** — Sense → Compute → Evaluate → Commit
- **CAS-YAML** — declarative constraint model format
- **CGAD** — Constraint-Governed Agentic Development

---

## Licensing

CPSC specifications and materials are released under the **CPSC Research & Evaluation License**.
Non-commercial research, evaluation, and educational use is permitted. Commercial use requires a separate license.

---

## Contact

For research questions, discussion, or licensing inquiries, contact **BitConcepts, LLC**.

© 2026 BitConcepts, LLC
