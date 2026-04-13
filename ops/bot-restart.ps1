$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

& (Join-Path $projectRoot "ops\bot-stop.ps1")
& (Join-Path $projectRoot "ops\bot-start.ps1")
Start-Sleep -Seconds 1
& (Join-Path $projectRoot "ops\bot-status.ps1")
