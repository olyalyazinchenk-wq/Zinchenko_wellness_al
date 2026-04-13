$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$statusPath = Join-Path $projectRoot "ops\bot-status.ps1"

if (-not (Test-Path -LiteralPath $statusPath)) {
    Write-Error "ops\bot-status.ps1 is missing."
    exit 1
}

powershell -ExecutionPolicy Bypass -File $statusPath
