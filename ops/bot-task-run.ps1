$ErrorActionPreference = "Continue"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"
$stdoutPath = Join-Path $projectRoot "bot.stdout.log"
$stderrPath = Join-Path $projectRoot "bot.stderr.log"
$runnerLogPath = Join-Path $projectRoot "bot.task-runner.log"

try {
    Add-Content -LiteralPath $runnerLogPath -Value "$(Get-Date -Format o) task started"
    Set-Location -LiteralPath $projectRoot
    & $pythonPath $entryPath 1>> $stdoutPath 2>> $stderrPath
    Add-Content -LiteralPath $runnerLogPath -Value "$(Get-Date -Format o) python exited with code $LASTEXITCODE"
    exit $LASTEXITCODE
} catch {
    Add-Content -LiteralPath $runnerLogPath -Value "$(Get-Date -Format o) runner error: $($_.Exception.Message)"
    exit 1
}
