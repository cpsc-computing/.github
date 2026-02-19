# Constraint-Projected State Computing (CPSC)

**A declarative computing model where computation is constraint projection, not instruction execution.**

CPSC provides a foundation for deterministic, constraint-driven systems across software, compression, control systems, and hardware (FPGA/ASIC).

---

## 🏗️ Organization Repositories

| Repository | Description |
|------------|-------------|
| **[cpsc-core](https://github.com/cpsc-computing/cpsc-core)** | Core specifications, CAS-YAML schema, and governance |
| **[cpsc-engine-python](https://github.com/cpsc-computing/cpsc-engine-python)** | Python reference implementation with adaptive projection engines |
| **[cpsc-engine-rtl](https://github.com/cpsc-computing/cpsc-engine-rtl)** | RTL/FPGA implementation for Zynq-7000 (Pynq-Z2) |
| **[cpac-engine-python](https://github.com/cpsc-computing/cpac-engine-python)** | CPAC lossless compression engine (+20% over gzip-9) |

---

## 🎯 Why CPSC?

Many real-world systems are governed by strong rules: physical limits, protocol invariants, safety constraints, structural relationships.

Traditional computing handles these indirectly through control logic, tuning, and exception handling — increasing complexity as systems grow.

**CPSC makes constraints the primary computational primitive.**

---

## 💡 Core Concepts

- **State** — the full configuration of a system
- **Constraints** — declarative rules defining valid states  
- **Projection** — resolving state into validity
- **Degrees of Freedom (DoF)** — minimal independent information needed
- **Constraint Fabric** — parallel enforcement of rules

---

## 🚀 Applications

- **Compression** — Structure-aware lossless compression (CPAC)
- **FPGA/ASIC** — Hardware constraint fabrics
- **Control Systems** — Power electronics, robotics
- **Protocol Enforcement** — Network validation, state machines
- **Secure Reconstruction** — Deterministic state recovery

---

## 📊 Status

CPSC is in the **specification and early reference phase**.

- ✅ Core specification published
- ✅ Python reference engine available
- ✅ RTL implementation for Pynq-Z2
- ✅ CPAC compression achieving +20% over gzip-9

---

## 📜 Licensing

All specifications and implementations are released under the **CPSC Research & Evaluation License v1.0**.

- ✅ Non-commercial research, evaluation, and educational use
- ❌ Commercial use requires separate license

---

## 📖 Getting Started

1. Read the [CPSC Specification](https://github.com/cpsc-computing/cpsc-core/blob/main/docs/specification/CPSC-Specification.md)
2. Explore [CAS-YAML examples](https://github.com/cpsc-computing/cpsc-core/tree/main/docs/specification)
3. Try the [Python engine](https://github.com/cpsc-computing/cpsc-engine-python)

---

## 📬 Contact

For research questions, discussion, or licensing inquiries, contact **BitConcepts, LLC**.
