$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"
$stdoutPath = Join-Path $projectRoot "bot.stdout.log"
$stderrPath = Join-Path $projectRoot "bot.stderr.log"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    Write-Error "Python virtual environment is missing at .venv\Scripts\python.exe."
    exit 1
}

if (-not (Test-Path -LiteralPath $entryPath)) {
    Write-Error "Bot entry file is missing: WellnessBot\main.py"
    exit 1
}

# Normalize PATH casing to avoid Start-Process dictionary collision on some Windows setups.
$pathValue = $env:Path
if (Test-Path Env:PATH) {
    Remove-Item Env:PATH -ErrorAction SilentlyContinue
}
$env:Path = $pathValue

Start-Process `
    -FilePath $pythonPath `
    -ArgumentList "WellnessBot\main.py" `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath

Write-Output "Bot start command issued."
