$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$runnerPath = Join-Path $projectRoot "ops\bot-start.ps1"

if (-not (Test-Path -LiteralPath $runnerPath)) {
    Write-Error "ops\bot-start.ps1 is missing."
    exit 1
}

powershell -ExecutionPolicy Bypass -File $runnerPath
