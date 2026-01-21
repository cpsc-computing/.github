param(
    [string]$RootDir = "$env:USERPROFILE",
    [switch]$SkipClone,
    [switch]$SkipSetup,
    [switch]$ConfigurePatentMcp
)

<#
.SYNOPSIS
    Install or update John Walkoe's USPTO MCP servers (PTAB, PFW, FPD, Enriched Citation)
    under the current user's profile for use with Warp / Claude MCP.

.DESCRIPTION
    This script is a thin, repo-local wrapper that ensures the following USPTO MCP
    servers are cloned and their upstream Windows setup scripts are run:

      * uspto_ptab_mcp              - PTAB Open Data v3 MCP
      * uspto_pfw_mcp               - Patent File Wrapper MCP
      * uspto_fpd_mcp               - Final Petition Decisions MCP
      * uspto_enriched_citation_mcp - Enriched Citation API v3 MCP

    For each server, this script will:

      1. Clone or update the corresponding GitHub repository under $RootDir
         (for example C:\Users\<USER>\uspto_ptab_mcp).
      2. Unless -SkipSetup is specified, invoke that repository's
         .\deploy\windows_setup.ps1 script, which:
           - installs uv if needed,
           - installs dependencies,
           - prompts for and securely stores USPTO / Mistral API keys using DPAPI,
           - optionally configures Claude Desktop MCP integration.

    This script does NOT manage API keys directly for the John Walkoe MCPs and does NOT
    write Claude config itself; it delegates those responsibilities to each upstream
    MCP's installer.

    Optionally (when -ConfigurePatentMcp is specified), this script will also clone or
    update the upstream `patent_mcp_server` repository from
    https://github.com/riemannzeta/patent_mcp_server under `$env:USERPROFILE` and run
    `uv sync` there so PPUBS/PatentsView/ODP tooling is available via a separate MCP
    server. In that mode it can also create or refresh a local `.env` for
    `patent_mcp_server` containing USPTO_API_KEY / PATENTSVIEW_API_KEY values.

.PARAMETER RootDir
    Root directory under which the MCP repositories will be cloned/updated.
    Defaults to "$env:USERPROFILE" (for example C:\Users\<USER>). Each repo
    will live under RootDir as a sibling directory (e.g. C:\Users\<USER>\uspto_ptab_mcp).

.PARAMETER SkipClone
    If specified, skip the clone/update step and only run each repo's
    windows_setup.ps1 (useful if you keep the repos in sync separately).

.PARAMETER SkipSetup
    If specified, skip running windows_setup.ps1 for each USPTO MCP repo. Only
    clone/update the repositories.

.PARAMETER ConfigurePatentMcp
    If specified, also clone or update the upstream `patent_mcp_server` repository
    under `$env:USERPROFILE\patent_mcp_server`, run `uv sync` there, and optionally
    prompt for USPTO/PatentsView API keys to write into a local `.env` for that
    server.

.EXAMPLE
    # Install or update all John Walkoe USPTO MCP servers under the current user's profile
    ./setup-ptab-mcp-for-warp.ps1

.EXAMPLE
    # Only run setup scripts (assumes repos already cloned/updated)
    ./setup-ptab-mcp-for-warp.ps1 -SkipClone

.EXAMPLE
    # Clone/update John Walkoe MCPs and also prepare patent_mcp_server for PPUBS
    ./setup-ptab-mcp-for-warp.ps1 -ConfigurePatentMcp

#>

$servers = @(
    @{ Name = "uspto_ptab_mcp";              Url = "https://github.com/john-walkoe/uspto_ptab_mcp.git" },
    @{ Name = "uspto_pfw_mcp";               Url = "https://github.com/john-walkoe/uspto_pfw_mcp.git" },
    @{ Name = "uspto_fpd_mcp";               Url = "https://github.com/john-walkoe/uspto_fpd_mcp.git" },
    @{ Name = "uspto_enriched_citation_mcp"; Url = "https://github.com/john-walkoe/uspto_enriched_citation_mcp.git" }
)

Write-Host "[USPTO MCP] Root directory: $RootDir" -ForegroundColor Cyan

$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git -and -not $SkipClone) {
    Write-Warning "[USPTO MCP] 'git' was not found on PATH. Install git or clone the repositories manually, then re-run with -SkipClone."
}

foreach ($server in $servers) {
    $name = $server.Name
    $url  = $server.Url
    $repoDir = Join-Path $RootDir $name

    Write-Host "[USPTO MCP] ==================================================" -ForegroundColor DarkCyan
    Write-Host "[USPTO MCP] Processing $name in $repoDir" -ForegroundColor Cyan

    if (-not $SkipClone) {
        if (-not (Test-Path -LiteralPath $repoDir)) {
            if ($git) {
                Write-Host "[USPTO MCP] Cloning $url ..." -ForegroundColor Cyan
                git clone $url $repoDir
            }
            else {
                Write-Warning "[USPTO MCP] git not available; please clone $url into $repoDir manually."
            }
        }
        else {
            if ($git) {
                Write-Host "[USPTO MCP] Repository already exists; updating..." -ForegroundColor Cyan
                Push-Location $repoDir
                try {
                    git pull --ff-only
                }
                finally {
                    Pop-Location
                }
            }
            else {
                Write-Host "[USPTO MCP] Repository exists and SkipClone is false, but git is not available; skipping update." -ForegroundColor Yellow
            }
        }
    }

    if ($SkipSetup) {
        Write-Host "[USPTO MCP] SkipSetup specified; not running deploy\windows_setup.ps1 for $name." -ForegroundColor Yellow
        continue
    }

    if (-not (Test-Path -LiteralPath $repoDir)) {
        Write-Warning "[USPTO MCP] Repository directory $repoDir does not exist; skipping setup for $name."
        continue
    }

    $setupScript = Join-Path $repoDir "deploy\windows_setup.ps1"
    if (-not (Test-Path -LiteralPath $setupScript)) {
        Write-Warning "[USPTO MCP] Setup script $setupScript not found; skipping setup for $name."
        continue
    }

    Write-Host "[USPTO MCP] Running $setupScript ..." -ForegroundColor Cyan
    Push-Location $repoDir
    try {
        Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process -Force
        & $setupScript
    }
    finally {
        Pop-Location
    }
}

Write-Host "[USPTO MCP] Completed processing all USPTO MCP servers." -ForegroundColor Green

# Optionally set up riemannzeta/patent_mcp_server for PPUBS/PatentsView/ODP tooling
if ($ConfigurePatentMcp) {
    $patentRepo = Join-Path $RootDir "patent_mcp_server"
    Write-Host "[Patent MCP] ==================================================" -ForegroundColor DarkCyan
    Write-Host "[Patent MCP] Processing patent_mcp_server in $patentRepo" -ForegroundColor Cyan

    if (-not $SkipClone) {
        if (-not (Test-Path -LiteralPath $patentRepo)) {
            if ($git) {
                Write-Host "[Patent MCP] Cloning https://github.com/riemannzeta/patent_mcp_server.git ..." -ForegroundColor Cyan
                git clone https://github.com/riemannzeta/patent_mcp_server.git $patentRepo
            }
            else {
                Write-Warning "[Patent MCP] git not available; please clone https://github.com/riemannzeta/patent_mcp_server.git into $patentRepo manually."
            }
        }
        else {
            if ($git) {
                Write-Host "[Patent MCP] Repository already exists; updating..." -ForegroundColor Cyan
                Push-Location $patentRepo
                try {
                    git pull --ff-only
                }
                finally {
                    Pop-Location
                }
            }
            else {
                Write-Host "[Patent MCP] Repository exists and SkipClone is false, but git is not available; skipping update." -ForegroundColor Yellow
            }
        }
    }

    if (-not (Test-Path -LiteralPath $patentRepo)) {
        Write-Warning "[Patent MCP] Repository directory $patentRepo does not exist; skipping patent_mcp_server setup."
    }
    else {
        Push-Location $patentRepo
        try {
            Write-Host "[Patent MCP] Running 'uv sync' in $patentRepo..." -ForegroundColor Cyan
            uv sync
        }
        finally {
            Pop-Location
        }

        if ($LASTEXITCODE -ne 0) {
            Write-Warning "[Patent MCP] 'uv sync' for patent_mcp_server exited with code $LASTEXITCODE. Review its output for details."
        }
        else {
            # Minimal .env configurator for patent_mcp_server
            $envPath = Join-Path $patentRepo ".env"
            Write-Host "[Patent MCP] Optionally configure USPTO_API_KEY / PATENTSVIEW_API_KEY for patent_mcp_server (.env)." -ForegroundColor Yellow
            Write-Host "[Patent MCP] Enter USPTO_API_KEY for patent_mcp_server (leave blank to skip):" -ForegroundColor Cyan
            $usptoSecure = Read-Host -AsSecureString
            $usptoPlain = if ($usptoSecure.Length -gt 0) { [System.Net.NetworkCredential]::new("", $usptoSecure).Password } else { "" }

            Write-Host "[Patent MCP] Enter PATENTSVIEW_API_KEY for patent_mcp_server (optional, leave blank to skip):" -ForegroundColor Cyan
            $pvSecure = Read-Host -AsSecureString
            $pvPlain = if ($pvSecure.Length -gt 0) { [System.Net.NetworkCredential]::new("", $pvSecure).Password } else { "" }

            $lines = @()
            if ($usptoPlain -ne "") { $lines += "USPTO_API_KEY=$usptoPlain" }
            if ($pvPlain   -ne "") { $lines += "PATENTSVIEW_API_KEY=$pvPlain" }

            if ($lines.Count -eq 0) {
                Write-Host "[Patent MCP] No keys entered for patent_mcp_server; leaving .env unchanged (if present)." -ForegroundColor Yellow
            }
            else {
                if (Test-Path -LiteralPath $envPath) {
                    $backupPath = "$envPath.bak_" + (Get-Date -Format "yyyyMMdd_HHmmss")
                    Write-Host "[Patent MCP] Backing up existing .env to $backupPath" -ForegroundColor Yellow
                    Copy-Item -LiteralPath $envPath -Destination $backupPath -Force
                }
                $content = ($lines -join "`r`n") + "`r`n"
                Set-Content -LiteralPath $envPath -Value $content -Encoding UTF8 -Force
                Write-Host "[Patent MCP] Wrote patent_mcp_server .env with $(($lines).Count) key(s)." -ForegroundColor Green
            }
        }
    }
}
