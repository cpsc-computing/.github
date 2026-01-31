#!/usr/bin/env python
"""CGAD constraint checker.

Usage (from repo root):

    python scripts/cgad_check.py \
        --model-path path/to/CGAD-*.cas.yaml \
        --state-json path/to/session_state.json

This is a minimal, non-normative helper that:
- loads a CAS/YAML-style constraint model (as used by CGAD-CPSC-Python.cas.yaml or CGAD-DDF.cas.yaml),
- loads a JSON session state object,
- evaluates each constraint expression against the state, and
- reports which constraints are satisfied or violated.

Expressions are evaluated in a restricted environment. The intent is
inspection and debugging, not formal proof.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List
from types import SimpleNamespace

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore


@dataclass
class ConstraintResult:
    name: str
    ok: bool
    error: str | None = None


def _flatten_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare an evaluation environment from a flat JSON state.

    We support two access patterns:

    - direct lookup by full key (e.g., env["tests.status"]), and
    - attribute-style groups for common prefixes (e.g., command.kind,
      cpsc.ledger.updated, ddf.phase).

    This keeps expressions readable in CAS models while allowing simple JSON
    state files.
    """

    env: Dict[str, Any] = dict(state)

    def to_namespace(obj: Any) -> Any:
        if isinstance(obj, dict):
            return SimpleNamespace(**{k: to_namespace(v) for k, v in obj.items()})
        return obj

    # Build grouped views for well-known prefixes.
    prefixes = [
        "tests",
        "plan",
        "cpsc",
        "command",
        "ddf",
    ]
    for prefix in prefixes:
        raw_group: Dict[str, Any] = {}
        for k, v in state.items():
            if not k.startswith(prefix + "."):
                continue
            suffix = k[len(prefix) + 1 :]
            # Support nested attributes like `ledger.updated`.
            parts = suffix.split(".")
            cursor = raw_group
            for part in parts[:-1]:
                cursor = cursor.setdefault(part, {})  # type: ignore[assignment]
            cursor[parts[-1]] = v
        if raw_group:
            env[prefix] = to_namespace(raw_group)

    return env


def _prepare_expression(expr: str) -> str:
    """Translate a CAS-style implication (`->`) into Python.

    We support using `A -> B` as logical implication. This is rewritten as
    `(not (A)) or (B)`.
    """

    # Very minimal rewrite: handle single-level `->` patterns on each line.
    # This is intentionally simple; CGAD expressions are short.
    lines: List[str] = []
    for line in expr.splitlines():
        # Normalize && to Python "and" for convenience.
        line = line.replace("&&", " and ")
        if "->" in line:
            left, right = line.split("->", 1)
            line = f"((not ({left.strip()})) or ({right.strip()}))"
        lines.append(line)
    return " and ".join(l for l in lines if l.strip()) or "True"


def _eval_constraint(expr: str, env: Dict[str, Any]) -> ConstraintResult:
    py_expr = _prepare_expression(expr)
    try:
        ok = bool(
            eval(
                py_expr,
                {
                    "__builtins__": {},
                    # CAS-style helpers
                    "True": True,
                    "False": False,
                    "true": True,
                    "false": False,
                    "size": lambda x: len(x),
                },
                env,
            )
        )
        return ConstraintResult(name="", ok=ok)
    except Exception as exc:  # pragma: no cover - defensive
        return ConstraintResult(name="", ok=False, error=str(exc))


def check_model(model_path: Path, state_path: Path) -> int:
    if yaml is None:
        print("pyyaml is required to run cgad_check.py", file=sys.stderr)
        return 2

    model_data = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    state_data = json.loads(state_path.read_text(encoding="utf-8"))

    state_env = _flatten_state(state_data)

    constraints = model_data.get("constraints", []) or []
    results: List[ConstraintResult] = []

    for c in constraints:
        name = c.get("name", "<unnamed>")
        expr = c.get("expr", "True")
        cr = _eval_constraint(expr, state_env)
        cr.name = name
        results.append(cr)

    failed = [r for r in results if not r.ok]

    print(f"Model: {model_path}")
    print(f"State: {state_path}")
    print("")
    for r in results:
        status = "OK" if r.ok else "FAIL"
        line = f"- [{status}] {r.name}"
        if r.error:
            line += f" (error: {r.error})"
        print(line)

    print("")
    if failed:
        print(f"{len(failed)} constraint(s) violated.")
        return 1
    else:
        print("All constraints satisfied.")
        return 0


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a CGAD CAS/YAML model against a JSON session state.")
    parser.add_argument("--model-path", type=Path, required=True, help="Path to CGAD-*.cas.yaml model file")
    parser.add_argument("--state-json", type=Path, required=True, help="Path to JSON file describing session state")

    args = parser.parse_args(argv)
    return check_model(args.model_path, args.state_json)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
