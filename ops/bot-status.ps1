$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"
$stderrPath = Join-Path $projectRoot "bot.stderr.log"
$stdoutPath = Join-Path $projectRoot "bot.stdout.log"

function Get-ProjectBotProcesses {
    $allPython = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -like "python*"
    }

    foreach ($proc in $allPython) {
        $cmd = [string]$proc.CommandLine
        $exe = [string]$proc.ExecutablePath
        $isProjectBot = $false

        if ($exe -eq $venvPython) { $isProjectBot = $true }
        if ($cmd.Contains($entryPath)) { $isProjectBot = $true }
        elseif ($cmd.Contains("WellnessBot\main.py")) { $isProjectBot = $true }

        if ($isProjectBot) {
            [pscustomobject]@{
                Id = [int]$proc.ProcessId
                ProcessName = $proc.Name
                Path = $exe
                Runtime = if ($exe -eq $venvPython) { "venv" } else { "external" }
                CommandLine = $cmd
            }
        }
    }
}

$botProcesses = @(Get-ProjectBotProcesses)

Write-Output "=== bot-process ==="
if ($botProcesses) {
    $botProcesses | Select-Object Id, ProcessName, Runtime, Path | Format-Table -AutoSize
    $external = @($botProcesses | Where-Object { $_.Runtime -ne "venv" })
    if ($external.Count -gt 0) {
        Write-Output ""
        Write-Output "WARNING: External bot process detected."
        $external | Select-Object Id, Path, CommandLine | Format-List
    }
} else {
    Write-Output "Project bot process is not running."
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
