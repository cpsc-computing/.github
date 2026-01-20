#!/usr/bin/env python
"""Render Markdown to PDF with Mermaid support using Pandoc.

This script is intended for local use when preparing patent drafts
(such as `patents/CPSC-CPAC-Provisional-2026-01.md`) for PDF export.

It relies on:
  - Pandoc installed on the system and available on PATH
  - A LaTeX engine (e.g., xelatex)
  - The `pandoc-mermaid-filter` Python package
  - Mermaid CLI (`mmdc`) installed separately (Node-based) for diagram rendering

Python dependencies are declared in `requirements.txt`.
"""

import argparse
import os
import shutil
import sys

from typing import List

try:
    import pypandoc
except ImportError as exc:  # pragma: no cover
    print("pypandoc is not installed. Install dependencies from requirements.txt first.", file=sys.stderr)
    raise


def check_tool_on_path(name: str) -> None:
    """Exit with a message if a required CLI tool is not on PATH."""
    if shutil.which(name) is None:
        print(f"Required tool '{name}' is not available on PATH.", file=sys.stderr)
        sys.exit(1)


def render_markdown_to_pdf(input_path: str, output_path: str, extra_args: List[str] | None = None) -> None:
    if extra_args is None:
        extra_args = []

    if not os.path.exists(input_path):
        print(f"Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Ensure required external tools are present
    check_tool_on_path("pandoc")
    check_tool_on_path("mmdc")  # Mermaid CLI

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    args = [
        "--pdf-engine=xelatex",
        "--filter=pandoc-mermaid-filter",
    ] + extra_args

    try:
        pypandoc.convert_file(  # type: ignore[arg-type]
            source_file=input_path,
            to="pdf",
            outputfile=output_path,
            extra_args=args,
        )
    except Exception as exc:  # pragma: no cover
        print(f"Error during Pandoc conversion: {exc}", file=sys.stderr)
        sys.exit(1)


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Render Markdown to PDF with Mermaid diagrams using Pandoc.")
    parser.add_argument(
        "input",
        nargs="?",
        default="patents/CPSC-CPAC-Provisional-2026-01.md",
        help="Input Markdown file (default: patents/CPSC-CPAC-Provisional-2026-01.md)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="patents/CPSC-CPAC-Provisional-2026-01.pdf",
        help="Output PDF file path (default: patents/CPSC-CPAC-Provisional-2026-01.pdf)",
    )
    parser.add_argument(
        "--pandoc-arg",
        action="append",
        default=[],
        help="Additional argument to pass through to pandoc (may be repeated)",
    )

    args = parser.parse_args(argv)

    render_markdown_to_pdf(args.input, args.output, extra_args=args.pandoc_arg)


if __name__ == "__main__":  # pragma: no cover
    main()
