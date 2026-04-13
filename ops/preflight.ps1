$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$envPath = Join-Path $projectRoot ".env"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"

Write-Output "=== preflight ==="
Write-Output ("projectRoot: {0}" -f $projectRoot)

$checks = @(
    @{ Name = "venv-python"; Ok = (Test-Path -LiteralPath $pythonPath) },
    @{ Name = ".env"; Ok = (Test-Path -LiteralPath $envPath) },
    @{ Name = "bot-entry"; Ok = (Test-Path -LiteralPath $entryPath) }
)

foreach ($check in $checks) {
    $status = if ($check.Ok) { "OK" } else { "FAIL" }
    Write-Output ("[{0}] {1}" -f $status, $check.Name)
}

if (-not (Test-Path -LiteralPath $pythonPath) -or -not (Test-Path -LiteralPath $envPath) -or -not (Test-Path -LiteralPath $entryPath)) {
    Write-Error "Preflight failed. Fix missing dependencies before start."
    exit 1
}

Write-Output "Preflight passed."
