#!/usr/bin/env python
"""Render CPSC/CPAC provisional Markdown to PDF with Mermaid diagrams.

This is a thin, repo-local wrapper around the `md2pdf` CLI provided by the
`md2pdf-mermaid` package. It ensures that:

- Headless Chromium is used for HTML→PDF rendering.
- Mermaid fenced code blocks in the provisional render to SVG/graphics
  correctly inside the PDF.

Prerequisites (run once, from the repository root or any active venv):

    pip install md2pdf-mermaid playwright
    python -m playwright install chromium

Usage examples (from repo root):

    python scripts/render_markdown_to_pdf.py
    python scripts/render_markdown_to_pdf.py \
        --input patents/CPSC-CPAC-Provisional-2026-01.md \
        --output patents/CPSC-CPAC-Provisional-2026-01.pdf

You can also generate just an HTML preview:

    python scripts/render_markdown_to_pdf.py --html-out patents/provisional.html

This script does *not* change any patent semantics. It is tooling only.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_md2pdf(input_md: Path, output_pdf: Path | None, html_out: Path | None) -> int:
    """Invoke the `md2pdf` console script from `md2pdf-mermaid`.

    We call the `md2pdf` entry point directly rather than using
    `python -m md2pdf`, because the package does not expose a
    `__main__` module. This assumes that the current environment's
    Python `Scripts`/`bin` directory (containing the `md2pdf` CLI)
    is on PATH.

    To ensure that relative image paths (for example `figures/*.svg`)
    are resolved correctly, we run the CLI with the current working
    directory set to the *directory containing the input markdown*.
    """

    # Call the installed console script. Prefer PATH resolution but fall back to the
    # Scripts/ directory next to the current Python executable on Windows when
    # md2pdf is not on PATH.
    md2pdf_cmd = shutil.which("md2pdf")
    if md2pdf_cmd is None:
        # On Windows, pip typically installs console scripts into the Scripts/
        # directory next to the python executable. Derive that path and use it
        # directly if present.
        exe_path = Path(sys.executable)
        candidate = exe_path.with_name("Scripts") / "md2pdf.exe"
        if candidate.exists():
            md2pdf_cmd = str(candidate)
        else:
            raise FileNotFoundError(
                "md2pdf executable not found on PATH or in the Python Scripts/ directory. "
                "Ensure 'md2pdf-mermaid' is installed and that its console script is "
                "available."
            )

    cmd: list[str] = [md2pdf_cmd]

    # Input markdown (can be absolute); we will run md2pdf from the markdown's
    # parent directory and pass only the local filename so relative resources
    # (like `images/foo.png`) resolve against the markdown directory.
    local_name = input_md.name
    cmd.append(local_name)

    # Optional output PDF
    if output_pdf is not None:
        cmd.extend(["-o", str(output_pdf)])

    # md2pdf-mermaid's CLI does not currently expose a separate HTML-output
    # flag; it renders directly to PDF. We keep `html_out` in the function
    # signature so the script interface is future-proof, but we do not pass
    # it through to the CLI.

    print(f"[render] Running: {' '.join(cmd)}")
    try:
        # Run md2pdf with CWD set to the markdown's parent directory so that
        # relative image paths like `images/*.png` are resolved correctly.
        workdir = str(input_md.parent)
        print(f"[render] Working directory: {workdir}")
        print(f"[render] Debug: full input_md path : {input_md}")
        print(f"[render] Debug: expected image dir : {input_md.parent / 'images'}")
        print(f"[render] Debug: output PDF path    : {output_pdf}")
        result = subprocess.run(cmd, check=False, cwd=workdir)
    except FileNotFoundError as exc:
        print("error: failed to invoke md2pdf via Python module 'md2pdf'.", file=sys.stderr)
        print("       Ensure 'md2pdf-mermaid' is installed in this environment.", file=sys.stderr)
        print(f"       Details: {exc}", file=sys.stderr)
        return 1

    print(f"[render] md2pdf return code: {result.returncode}")
    if result.returncode != 0:
        print(f"error: md2pdf exited with status {result.returncode}", file=sys.stderr)
    return result.returncode


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render Markdown to PDF using md2pdf-mermaid (headless Chromium with "
            "Mermaid support). If no input/output is provided and no test flag "
            "is set, this script defaults to rendering all Markdown files under "
            "docs/ into a mirrored docs-pdf/ tree."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        help=(
            "Input Markdown file (relative to repo root). If omitted and "
            "--all-docs is not set, no single-file render is performed."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Output PDF file (relative to repo root). If omitted in single-file "
            "mode, the output path will mirror the docs/ hierarchy under "
            "docs-pdf/."
        ),
    )

    parser.add_argument(
        "--html-out",
        type=Path,
        default=None,
        help=(
            "Reserved for potential future use if md2pdf-mermaid adds a flag "
            "to emit intermediate HTML. Currently ignored."
        ),
    )

    parser.add_argument(
        "--test-diagrams",
        action="store_true",
        help=(
            "If set, render only a small, inline-mermaid test document to HTML/PDF "
            "to validate that Mermaid/Chromium are working, without touching other "
            "documents."
        ),
    )

    parser.add_argument(
        "--all-docs",
        action="store_true",
        help=(
            "If set (or if no other flags are provided), render all Markdown files "
            "under docs/ into a mirrored docs-pdf/ tree."
        ),
    )

    return parser.parse_args(argv)


def build_test_markdown() -> str:
    """Return a tiny Markdown string containing a few Mermaid diagrams.

    This exercises the same fenced code block style used in the provisional.
    """

    return """# Mermaid Test

This is a minimal test to confirm that md2pdf-mermaid can render flowcharts.

```mermaid
flowchart LR
    A[Start] --> B[Check]
    B -->|OK| C[Done]
    B -->|Fail| D[Error]
```

```mermaid
flowchart TD
    X[Input] --> Y[Projection Engine]
    Y --> Z[Valid State]
```
"""


def run_test_mode(html_out: Path | None, pdf_out: Path | None) -> int:
    """Write a temporary Markdown file and render it via md2pdf.

    The user can inspect the HTML/PDF to confirm diagrams look correct.
    """

    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        md_path = tmpdir_path / "mermaid-test.md"
        md_path.write_text(build_test_markdown(), encoding="utf-8")

        # Default outputs in the patents/figures directory if not overridden.
        figures_dir = REPO_ROOT / "patents" / "figures"
        figures_dir.mkdir(parents=True, exist_ok=True)

        if pdf_out is None:
            pdf_out = figures_dir / "mermaid-test.pdf"
        if html_out is None:
            html_out = figures_dir / "mermaid-test.html"

        print(f"[test] Writing temporary Markdown to {md_path}")
        print(f"[test] HTML out: {html_out}")
        print(f"[test] PDF out:  {pdf_out}")

        return run_md2pdf(md_path, pdf_out, html_out)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    # Default behavior: if no explicit input/output and no test flag was provided,
    # treat this as an "all docs" render under docs/.
    if not argv and not args.test_diagrams:
        args.all_docs = True

    if args.test_diagrams:
        return run_test_mode(args.html_out, args.output)

    # All-docs mode: mirror docs/ into docs-pdf/.
    if args.all_docs:
        docs_root = REPO_ROOT / "docs"
        docs_pdf_root = REPO_ROOT / "docs-pdf"

        if not docs_root.exists():
            print(f"error: docs directory not found at {docs_root}", file=sys.stderr)
            return 1

        docs_pdf_root.mkdir(parents=True, exist_ok=True)

        md_files = list(docs_root.rglob("*.md"))
        if not md_files:
            print(f"[render] No Markdown files found under {docs_root}")
            return 0

        for md in md_files:
            # Compute relative path under docs/.
            rel = md.relative_to(docs_root)
            out_dir = docs_pdf_root / rel.parent
            out_pdf = out_dir / (md.stem + ".pdf")

            out_dir.mkdir(parents=True, exist_ok=True)
            print(f"[render] Rendering {md} -> {out_pdf}")
            rc = run_md2pdf(md, out_pdf, html_out=None)
            if rc != 0:
                print(f"[render] WARNING: md2pdf exited with {rc} for {md}", file=sys.stderr)

        return 0

    # Single-file mode.
    input_md = args.input
    output_pdf = args.output

    if input_md is None:
        print("error: --input is required for single-file mode (when --all-docs is not used)", file=sys.stderr)
        return 1

    # Normalize to absolute paths based on repo root when a relative path is given.
    if not input_md.is_absolute():
        input_md = (REPO_ROOT / input_md).resolve()

    if output_pdf is None:
        # Mirror docs/ hierarchy under docs-pdf/ by default.
        docs_root = REPO_ROOT / "docs"
        docs_pdf_root = REPO_ROOT / "docs-pdf"
        try:
            rel = input_md.relative_to(docs_root)
        except ValueError:
            # If the input is not under docs/, fall back to placing the PDF next to it.
            output_pdf = input_md.with_suffix(".pdf")
        else:
            out_dir = docs_pdf_root / rel.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            output_pdf = out_dir / (input_md.stem + ".pdf")

    if not output_pdf.is_absolute():
        output_pdf = (REPO_ROOT / output_pdf).resolve()

    html_out = args.html_out
    if html_out is not None and not html_out.is_absolute():
        html_out = (REPO_ROOT / html_out).resolve()

    if not input_md.exists():
        print(f"error: input Markdown does not exist: {input_md}", file=sys.stderr)
        return 1

    print(f"[render] Input : {input_md}")
    print(f"[render] Output: {output_pdf}")
    if html_out is not None:
        print(f"[render] HTML  : {html_out}")

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    if html_out is not None:
        html_out.parent.mkdir(parents=True, exist_ok=True)

    return run_md2pdf(input_md, output_pdf, html_out)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
