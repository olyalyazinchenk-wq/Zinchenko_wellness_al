$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"
$stdoutPath = Join-Path $projectRoot "bot.stdout.log"
$stderrPath = Join-Path $projectRoot "bot.stderr.log"

Write-Host "=== Zinchenko Wellness Bot Admin Cleanup ==="
Write-Host "Project: $projectRoot"

$portOwners = @()
try {
    $portOwners = Get-NetTCPConnection -LocalPort 8000,8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
} catch {}

$processes = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq "python.exe" }
$targets = @()
foreach ($p in $processes) {
    $cmd = [string]$p.CommandLine
    $exe = [string]$p.ExecutablePath
    $pid = [int]$p.ProcessId
    $isProjectBot = $false
    if ($cmd -like "*WellnessBot*main.py*") { $isProjectBot = $true }
    if ($cmd -like "*$projectRoot*") { $isProjectBot = $true }
    if ($exe -eq $venvPython) { $isProjectBot = $true }
    if ($portOwners -contains $pid) { $isProjectBot = $true }
    if ($isProjectBot) { $targets += $pid }
}

$targets = $targets | Sort-Object -Unique
if ($targets.Count -gt 0) {
    Write-Host "Stopping bot-related Python processes: $($targets -join ', ')"
    foreach ($pid in $targets) {
        try {
            Stop-Process -Id $pid -Force -ErrorAction Stop
            Write-Host "Stopped PID $pid"
        } catch {
            Write-Host "Could not stop PID $pid: $($_.Exception.Message)"
        }
    }
    Start-Sleep -Seconds 3
} else {
    Write-Host "No bot-related Python processes found."
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "Missing venv python: $venvPython"
    pause
    exit 1
}
if (-not (Test-Path -LiteralPath $entryPath)) {
    Write-Host "Missing bot entry: $entryPath"
    pause
    exit 1
}

Write-Host "Starting clean bot instance..."
Start-Process -FilePath $venvPython -ArgumentList "WellnessBot\main.py" -WorkingDirectory $projectRoot -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
Start-Sleep -Seconds 8

Write-Host "=== Current Python processes ==="
Get-CimInstance Win32_Process | Where-Object { $_.Name -eq "python.exe" } | Select-Object ProcessId,CommandLine,ExecutablePath | Format-List
Write-Host "=== Recent bot stderr ==="
if (Test-Path -LiteralPath $stderrPath) { Get-Content -LiteralPath $stderrPath -Tail 20 }
Write-Host "Done. You can close this window after checking there is no TelegramConflictError in the last lines."
pause
