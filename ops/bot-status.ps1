$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"
$stderrCandidates = @(
    (Join-Path $projectRoot "bot.stderr"),
    (Join-Path $projectRoot "bot.stderr.log")
)
$stdoutCandidates = @(
    (Join-Path $projectRoot "bot.stdout"),
    (Join-Path $projectRoot "bot.stdout.log")
)

function Resolve-LatestLogPath {
    param(
        [string[]]$Candidates
    )

    $existing = foreach ($candidate in $Candidates) {
        if (Test-Path -LiteralPath $candidate) {
            Get-Item -LiteralPath $candidate
        }
    }

    if (-not $existing) {
        return $Candidates[0]
    }

    return ($existing | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
}

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
                ParentId = [int]$proc.ParentProcessId
                ProcessName = $proc.Name
                Path = $exe
                Runtime = if ($exe -eq $venvPython) { "venv" } else { "external" }
                CommandLine = $cmd
            }
        }
    }
}

$botProcesses = @(Get-ProjectBotProcesses)
$venvParentIds = @($botProcesses | Where-Object { $_.Runtime -eq "venv" } | Select-Object -ExpandProperty Id)
$stderrPath = Resolve-LatestLogPath -Candidates $stderrCandidates
$stdoutPath = Resolve-LatestLogPath -Candidates $stdoutCandidates

Write-Output "=== bot-process ==="
if ($botProcesses) {
    $botProcesses | Select-Object Id, ProcessName, Runtime, Path | Format-Table -AutoSize
    $external = @(
        $botProcesses | Where-Object {
            $_.Runtime -ne "venv" -and $_.ParentId -notin $venvParentIds
        }
    )
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
    Write-Output ("log: {0}" -f $stderrPath)
    Get-Content -LiteralPath $stderrPath -Tail 80
} else {
    Write-Output "No stderr log yet."
}

Write-Output ""
Write-Output "=== stdout (tail 80) ==="
if (Test-Path -LiteralPath $stdoutPath) {
    Write-Output ("log: {0}" -f $stdoutPath)
    Get-Content -LiteralPath $stdoutPath -Tail 80
} else {
    Write-Output "No stdout log yet."
}
