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


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO_ROOT / "patents" / "CPSC-CPAC-Provisional-2026-01.md"
DEFAULT_OUTPUT = REPO_ROOT / "patents" / "CPSC-CPAC-Provisional-2026-01.pdf"


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

    # Call the installed console script; rely on PATH resolution.
    cmd: list[str] = ["md2pdf"]

    # Input markdown (can be absolute); working directory will be
    # the markdown's parent folder so that relative image references
    # are resolved as expected.
    cmd.append(str(input_md))

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
        # relative image paths like `figures/*.svg` are resolved correctly.
        workdir = str(input_md.parent)
        print(f"[render] Working directory: {workdir}")
        result = subprocess.run(cmd, check=False, cwd=workdir)
    except FileNotFoundError as exc:
        print("error: failed to invoke md2pdf via Python module 'md2pdf'.", file=sys.stderr)
        print("       Ensure 'md2pdf-mermaid' is installed in this environment.", file=sys.stderr)
        print(f"       Details: {exc}", file=sys.stderr)
        return 1

    if result.returncode != 0:
        print(f"error: md2pdf exited with status {result.returncode}", file=sys.stderr)
    return result.returncode


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render the CPSC/CPAC provisional Markdown to PDF using md2pdf-mermaid "
            "(headless Chromium with Mermaid support)."
        )
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=(
            "Input Markdown file (default: patents/CPSC-CPAC-Provisional-2026-01.md "
            "relative to repo root)."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=(
            "Output PDF file (default: patents/CPSC-CPAC-Provisional-2026-01.pdf "
            "relative to repo root)."
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
            "to validate that Merlin/Chromium are working, without touching the "
            "provisional itself."
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

    if args.test_diagrams:
        return run_test_mode(args.html_out, args.output)

    input_md = args.input
    output_pdf = args.output

    # Normalize to absolute paths based on repo root when a relative path is given.
    if not input_md.is_absolute():
        input_md = (REPO_ROOT / input_md).resolve()
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
