$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$scriptPath = Join-Path $projectRoot "ops\quality_probe.py"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    Write-Error "Python virtual environment missing."
    exit 1
}

if (-not (Test-Path -LiteralPath $scriptPath)) {
    Write-Error "quality_probe.py is missing."
    exit 1
}

& $pythonPath $scriptPath --mode smoke
