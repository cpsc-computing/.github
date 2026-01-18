# CPSC Binary Format Specification
## Deterministic State Interchange Format

**Version:** 1.0  
**Status:** Draft Specification  
**Published:** January 17, 2026  

---

## License Notice

This specification is released under the **CPSC Research & Evaluation License**.

It may be used, shared, and cited for non-commercial research, evaluation, and educational purposes.
Commercial use, production deployment, or implementation in commercial systems requires a separate license.

The technology described herein may be subject to patent protection.
All rights are reserved.

---

## Abstract

This document specifies the **CPSC Binary Format**, a deterministic, streamable binary representation used to encode degrees of freedom, optional residuals, and reconstruction metadata for Constraint-Projected State Computing (CPSC). The format is designed for efficient software execution, direct mapping to FPGA/RTL hardware, and deterministic reconstruction of valid system state.

---

## 1. Purpose and Scope

The CPSC Binary Format defines how CPSC state information is serialized for:

- storage
- transmission
- compression pipelines
- hardware streaming interfaces

This format is **not** a general-purpose container.
It exists solely to support CPSC reconstruction semantics.

---

## 2. Design Goals

The binary format is designed to be:

- Deterministic
- Self-describing
- Streamable
- Hardware-friendly
- Versioned
- Minimal

It avoids:
- dynamic allocation
- recursion
- variable control structures
- hidden execution semantics

---

## 3. High-Level Structure

A CPSC binary blob consists of the following ordered sections:

```

[Header]
[Model Metadata]
[Stage Table]
[Degree-of-Freedom Vector]
[Residual Stream] (optional)

```

All sections appear in the order listed.

---

## 4. Header

### 4.1 Header Purpose

The header allows:
- fast identification
- version validation
- endian detection
- early rejection of incompatible blobs

---

### 4.2 Header Fields

| Field | Size | Description |
|------|------|-------------|
| Magic | 4 bytes | ASCII "CPSC" |
| Format Version | 2 bytes | Binary format version |
| Flags | 2 bytes | Feature flags |
| Endianness | 1 byte | 0 = little, 1 = big |
| Numeric Mode | 1 byte | Fixed / floating |
| Reserved | 6 bytes | Must be zero |

Total header size: **16 bytes**

---

## 5. Model Metadata Section

### 5.1 Purpose

This section binds the binary blob to a specific CPSC model.

---

### 5.2 Fields

| Field | Size | Description |
|------|------|-------------|
| Model ID Hash | 32 bytes | Hash of CAS-YAML model_id |
| CAS Hash | 32 bytes | Hash of resolved CAS-YAML |
| DoF Count | 4 bytes | Number of free variables |
| Precision Bits | 2 bytes | Numeric precision |
| Reserved | 2 bytes | Must be zero |

---

## 6. Stage Table

### 6.1 Purpose

The stage table describes which pipeline stages were applied during encoding.

This enables:
- forward compatibility
- partial decoding
- hardware routing decisions

---

### 6.2 Structure

```

[Stage Count] (2 bytes)
[Stage Entries...]

```

Each stage entry:

| Field | Size | Description |
|------|------|-------------|
| Stage ID | 2 bytes | Symbolic stage identifier |
| Flags | 2 bytes | Stage-specific flags |
| Reserved | 4 bytes | Must be zero |

---

## 7. Degree-of-Freedom Vector

### 7.1 Purpose

This section encodes the **minimal independent state information**.

---

### 7.2 Layout

```

[DoF₁][DoF₂]...[DoFₙ]

```

Each DoF value:
- uses declared numeric mode
- uses declared precision
- appears in deterministic order defined by CAS-YAML

This section is fixed-size once the model is known.

---

## 8. Residual Stream (Optional)

### 8.1 Purpose

Residuals encode deviations not captured by DoF alone.

This section is optional and may be omitted if not required.

---

### 8.2 Semantics

- Residuals are applied before final projection
- Residual decoding MUST be deterministic
- Residuals MUST NOT violate declared constraints

---

## 9. Streaming and Hardware Mapping

### 9.1 Streaming Properties

- Header and metadata are small and fixed
- DoF vector is sequential and bounded
- Residual stream may be processed incrementally

---

### 9.2 RTL / FPGA Mapping

| Section | Hardware Mapping |
|-------|------------------|
| Header | FSM parser |
| Metadata | Registers / ROM |
| Stage Table | Static decode |
| DoF Vector | Register bank or FIFO |
| Residual Stream | Streaming decoder |

No dynamic memory or instruction sequencing is required.

---

## 10. Reconstruction Algorithm (Normative)

To reconstruct a valid state:

1. Parse header
2. Validate format version
3. Read model metadata
4. Load CAS-YAML model
5. Inject DoF vector
6. Apply residuals (if present)
7. Run CPSC projection
8. Emit valid state

Failure at any step MUST abort reconstruction.

---

## 11. Validation Rules

A binary blob is valid only if:

- Magic and version match
- Model hash matches CAS-YAML
- DoF count matches model
- Numeric modes are compatible
- Reserved fields are zero

---

## 12. Relationship to Other Specifications

This document depends on:
- CPSC-Specification.md
- CAS-YAML-Specification.md

It does not redefine execution or constraint semantics.

---

## 13. Summary

The CPSC Binary Format provides a deterministic, compact, and hardware-aligned representation of CPSC state information. It enables efficient storage, transmission, and reconstruction across software and hardware implementations.

This document is the authoritative specification for the CPSC binary format.
