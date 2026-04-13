$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

$targets = Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -like "python*" -and $_.Path -eq $venvPython
}

if (-not $targets) {
    Write-Output "No bot process from project virtualenv is running."
    exit 0
}

$targets | Stop-Process -Force
Write-Output ("Stopped {0} bot process(es)." -f $targets.Count)
