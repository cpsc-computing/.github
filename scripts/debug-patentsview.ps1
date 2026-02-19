# Copyright (c) 2026 BitConcepts, LLC
# SPDX-License-Identifier: LicenseRef-CPAC-Research-Evaluation-1.0
#
# This file is part of the CPSC Specifications.
# For full license terms, see LICENSE in the repository root.

Param()

$ErrorActionPreference = 'Stop'

Write-Host "[Debug] Reading PATENTSVIEW_API_KEY from patent_mcp_server/.env" -ForegroundColor Cyan
$envPath = "C:\Users\trist\patent_mcp_server\.env"
if (-not (Test-Path -LiteralPath $envPath)) {
    Write-Host "[Debug] .env file not found at $envPath" -ForegroundColor Red
    exit 1
}

$kv = Get-Content $envPath | Where-Object { $_ -match '^PATENTSVIEW_API_KEY=' } | Select-Object -First 1
if (-not $kv) {
    Write-Host "[Debug] PATENTSVIEW_API_KEY line not found in .env" -ForegroundColor Red
    exit 1
}

$parts = $kv.Split('=', 2)
if ($parts.Count -lt 2 -or [string]::IsNullOrWhiteSpace($parts[1])) {
    Write-Host "[Debug] PATENTSVIEW_API_KEY value is empty" -ForegroundColor Red
    exit 1
}

$apiKey = $parts[1].Trim()
Write-Host "[Debug] Found PATENTSVIEW_API_KEY (redacted)" -ForegroundColor Green

$qObj = @{
    _or = @(
        @{ _text_any = @{ patent_title    = 'neural network' } },
        @{ _text_any = @{ patent_abstract = 'neural network' } }
    )
}

$oObj = @{ size = 5 }

$bodyObj = @{ q = $qObj; o = $oObj }
$bodyJson = $bodyObj | ConvertTo-Json -Depth 6

$headers = @{
    'Accept'       = 'application/json'
    'Content-Type' = 'application/json'
    'X-Api-Key'    = $apiKey
}

Write-Host "[Debug] Sending POST to https://search.patentsview.org/api/v1/patent/" -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri 'https://search.patentsview.org/api/v1/patent/' -Headers $headers -Method Post -Body $bodyJson
    Write-Host "[Debug] StatusCode: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "[Debug] Response body:" -ForegroundColor Green
    $response.Content
} catch {
    if ($_.Exception.Response -ne $null) {
        $resp = $_.Exception.Response
        Write-Host "[Debug] HTTP error: $($resp.StatusCode.value__)" -ForegroundColor Yellow
        try {
            $reader = New-Object System.IO.StreamReader($resp.GetResponseStream())
            $text = $reader.ReadToEnd()
            Write-Host "[Debug] Response body:" -ForegroundColor Yellow
            $text
        } catch {
            Write-Host "[Debug] Failed to read error response body: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "[Debug] Unexpected error: $($_.Exception.Message)" -ForegroundColor Red
    }
    exit 1
}
