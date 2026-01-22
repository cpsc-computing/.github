param(
    [string]$Input,
    [string]$Output,
    [switch]$TestDiagrams,
    [switch]$AllDocs,
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

# $PSScriptRoot points to .github\scripts.
# The .github directory (which contains the Python script) is its parent.
$githubRoot = Split-Path $PSScriptRoot -Parent

$scriptPath = Join-Path $githubRoot "scripts\render_markdown_to_pdf.py"
if (-not (Test-Path $scriptPath)) {
    throw "render_markdown_to_pdf.py not found at $scriptPath"
}

if ($TestDiagrams) {
    # Just exercise the renderer's built-in test mode.
    $args = @($scriptPath, "--test-diagrams")
    Write-Host "[render] Using Python executable: $Python"
    Write-Host "[render] Running: $Python $($args -join ' ')"
    & $Python @args
    return
}

if ($AllDocs) {
    # Render every Markdown file under docs/ into a mirrored docs-pdf/ tree.
    $docsRoot    = Join-Path $githubRoot "docs"
    $docsPdfRoot = Join-Path $githubRoot "docs-pdf"

    if (-not (Test-Path $docsRoot)) {
        throw "docs directory not found at $docsRoot"
    }

    if (-not (Test-Path $docsPdfRoot)) {
        Write-Host "[render] Creating docs-pdf directory at $docsPdfRoot"
        New-Item -ItemType Directory -Path $docsPdfRoot | Out-Null
    }

    $markdownFiles = Get-ChildItem -Path $docsRoot -Recurse -Filter "*.md" -File
    if (-not $markdownFiles) {
        Write-Host "[render] No Markdown files found under $docsRoot"
        return
    }

    foreach ($file in $markdownFiles) {
        $inputPath = $file.FullName

        # Compute relative path under docs/ and map it into docs-pdf/.
        $relativePath = Resolve-Path $inputPath -Relative
        # Normalize to use forward slashes, then strip leading "docs/".
        $relativePath = $relativePath -replace "^\.\\", ""
        $relativePath = $relativePath -replace "^docs[\\/]", ""

        $targetDir   = Join-Path $docsPdfRoot ([System.IO.Path]::GetDirectoryName($relativePath))
        $targetFile  = [System.IO.Path]::GetFileNameWithoutExtension($relativePath) + ".pdf"
        $outputPath  = Join-Path $targetDir $targetFile

        if (-not (Test-Path $targetDir)) {
            Write-Host "[render] Creating directory" $targetDir
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }

        Write-Host "[render] Rendering" $inputPath "->" $outputPath

        $args = @($scriptPath, "--input", $inputPath, "--output", $outputPath)

        Write-Host "[render] Using Python executable: $Python"
        Write-Host "[render] Running: $Python $($args -join ' ')"

        & $Python @args
    }

    return
}

# Fallback: single-input mode, defaulting to the provisional if not specified.
if (-not $Input) {
    $Input = "docs/patents/CPSC-CPAC-Provisional-2026-01.md"
}
if (-not $Output) {
    # By default, emit the provisional PDF under docs-pdf/ mirroring docs/.
    $Output = "docs-pdf/patents/CPSC-CPAC-Provisional-2026-01.pdf"
}

$inputPath  = Join-Path $githubRoot $Input
$outputPath = Join-Path $githubRoot $Output

Write-Host "[render] Resolved input path : $inputPath"
Write-Host "[render] Resolved output path: $outputPath"

$args = @($scriptPath, "--input", $inputPath, "--output", $outputPath)

Write-Host "[render] Using Python executable: $Python"
Write-Host "[render] Running: $Python $($args -join ' ')"

& $Python @args
