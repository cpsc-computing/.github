param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

Write-Host "[setup] Using Python executable: $Python"

# Install md2pdf-mermaid and Playwright into the current Python environment.
& $Python -m pip install --upgrade pip
& $Python -m pip install md2pdf-mermaid playwright

# Install the Chromium browser that md2pdf-mermaid will use via Playwright.
& $Python -m playwright install chromium

Write-Host "[setup] Environment ready for md2pdf-mermaid (md2pdf) rendering."