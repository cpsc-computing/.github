param(
    [string]$RepoDir = "$env:USERPROFILE\patent_mcp_server",
    [switch]$SkipClone,
    [switch]$SkipSetup
)

<#
.SYNOPSIS
    Helper script to install or update the local `patent_mcp_server` repo and
    prepare it for use with Warp and other MCP-aware clients.

.DESCRIPTION
    This script is a thin, repo-local wrapper around the upstream patent MCP server
    (https://github.com/riemannzeta/patent_mcp_server).

    It is intended to:
      * Clone or update the `patent_mcp_server` repository locally (optional).
      * Run `uv sync` in that repository so it is ready to serve MCP requests.

    This script does NOT modify Warp configuration directly. Instead, it ensures
    that the local MCP server repo is present and its Python environment is
    hydrated so that Warp (or another MCP client) can be pointed at it.

.PARAMETER RepoDir
    Directory where the `patent_mcp_server` repository will be cloned/updated.
    Defaults to "$env:USERPROFILE\patent_mcp_server".

.PARAMETER SkipClone
    If specified, skip the clone/update step and only run `uv sync`.
    Useful if you manage the repo manually.

.PARAMETER SkipSetup
    If specified, skip the `uv sync` step.
    Useful if you only want to clone/update the repo.

.EXAMPLE
    # Default installation under the current user's profile
    ./setup-ptab-mcp-for-warp.ps1

.EXAMPLE
    # Custom repo directory
    ./setup-ptab-mcp-for-warp.ps1 -RepoDir "$env:USERPROFILE\src\patent_mcp_server"

.NOTES
    After running this script, configure your MCP-aware client (such as Warp) to
    launch the patent MCP server with a command similar to:

        uv --directory "$env:USERPROFILE\patent_mcp_server" run patent-mcp-server

    In a classic `cmd.exe` shell, the equivalent path would use `%USERPROFILE%`,
    for example: `uv --directory "%USERPROFILE%\patent_mcp_server" run patent-mcp-server`.

    The upstream server loads its API key(s) from a `.env` file or environment
    variables such as `USPTO_API_KEY`. Do not commit secrets to this repository.
#>

Write-Host "[Patent MCP] Repository directory: $RepoDir" -ForegroundColor Cyan

if (-not $SkipClone) {
    if (-not (Test-Path -LiteralPath $RepoDir)) {
        Write-Host "[Patent MCP] Cloning upstream repository..." -ForegroundColor Cyan
        git clone https://github.com/riemannzeta/patent_mcp_server.git $RepoDir
    }
    else {
        Write-Host "[Patent MCP] Repository already exists; updating..." -ForegroundColor Cyan
        Push-Location $RepoDir
        try {
            git pull --ff-only
        }
        finally {
            Pop-Location
        }
    }
}

if ($SkipSetup) {
    Write-Host "[Patent MCP] SkipSetup specified; not running 'uv sync'." -ForegroundColor Yellow
    return
}

$uv = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uv) {
    Write-Warning "[Patent MCP] The 'uv' tool was not found on PATH. Install it from https://docs.astral.sh/uv/ and re-run this script."
    return
}

if (-not (Test-Path -LiteralPath $RepoDir)) {
    Write-Error "[Patent MCP] Repository directory $RepoDir does not exist. Clone it or adjust -RepoDir."
    exit 1
}

Push-Location $RepoDir
try {
    Write-Host "[Patent MCP] Running 'uv sync' in $RepoDir..." -ForegroundColor Cyan
    uv sync
}
finally {
    Pop-Location
}

if ($LASTEXITCODE -ne 0) {
    Write-Warning "[Patent MCP] 'uv sync' exited with code $LASTEXITCODE. Review its output for details."
}
else {
    # Print a ready-to-paste Warp MCP JSON snippet using this repo directory.
    $jsonRepoPath = $RepoDir -replace "\\", "/"

    Write-Host "[Patent MCP] Repository is ready. Configure Warp with an MCP server entry like:" -ForegroundColor Green

    $json = @"
{
  "mcpServers": {
    "patents": {
      "command": "uv",
      "args": [
        "--directory",
        "$jsonRepoPath",
        "run",
        "patent-mcp-server"
      ]
    }
  }
}
"@

    Write-Host $json
}
