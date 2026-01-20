param(
    [string]$Input,
    [string]$Output,
    [switch]$TestDiagrams,
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

# $PSScriptRoot points to .github\scripts.
# The .github directory (which contains the Python script) is its parent.
$githubRoot = Split-Path $PSScriptRoot -Parent

# Default input/output if not provided.
if (-not $Input) {
    $Input = "patents/CPSC-CPAC-Provisional-2026-01.md"
}
if (-not $Output) {
    $Output = "patents/CPSC-CPAC-Provisional-2026-01.pdf"
}

$inputPath  = Join-Path $githubRoot $Input
$outputPath = Join-Path $githubRoot $Output

Write-Host "[render] Resolved input path : $inputPath"
Write-Host "[render] Resolved output path: $outputPath"

$scriptPath = Join-Path $githubRoot "scripts\render_markdown_to_pdf.py"

if (-not (Test-Path $scriptPath)) {
    throw "render_markdown_to_pdf.py not found at $scriptPath"
}

$args = @($scriptPath, "--input", $inputPath, "--output", $outputPath)
if ($TestDiagrams) {
    $args = @($scriptPath, "--test-diagrams")
}

Write-Host "[render] Using Python executable: $Python"
Write-Host "[render] Running: $Python $($args -join ' ')"

& $Python @args
