$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$stderrPath = Join-Path $projectRoot "bot.stderr.log"
$stdoutPath = Join-Path $projectRoot "bot.stdout.log"

$botProcesses = Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -like "python*" -and $_.Path -eq $venvPython
}

Write-Output "=== bot-process ==="
if ($botProcesses) {
    $botProcesses | Select-Object Id, ProcessName, Path | Format-Table -AutoSize
} else {
    Write-Output "Bot process is not running from project virtualenv."
}

Write-Output ""
Write-Output "=== stderr (tail 80) ==="
if (Test-Path -LiteralPath $stderrPath) {
    Get-Content -LiteralPath $stderrPath -Tail 80
} else {
    Write-Output "No stderr log yet."
}

Write-Output ""
Write-Output "=== stdout (tail 80) ==="
if (Test-Path -LiteralPath $stdoutPath) {
    Get-Content -LiteralPath $stdoutPath -Tail 80
} else {
    Write-Output "No stdout log yet."
}
