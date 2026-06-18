$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$stagePath = Join-Path $projectRoot "docs\CURRENT_STAGE.json"
$stage = Get-Content -Raw -Encoding UTF8 -LiteralPath $stagePath | ConvertFrom-Json

Push-Location $projectRoot
try {
    $branch = (git branch --show-current).Trim()
    $head = (git rev-parse HEAD).Trim()
    $remoteHead = (git rev-parse origin/master).Trim()
    $trackedDirty = @(git status --short --untracked-files=no)
    $botTask = Get-ScheduledTask -TaskName "WellnessBot" -ErrorAction SilentlyContinue
    $botProcessCount = -1
    try {
        $botProcesses = @(
            Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object {
                $_.Name -like "python*" -and
                ([string]$_.CommandLine).Contains("WellnessBot\main.py")
            }
        )
        $botProcessCount = $botProcesses.Count
    } catch {
        # Some agent shells cannot query Win32_Process. Task state remains the
        # portable runtime ownership signal in that environment.
    }
    $legacyPollingRaw = @(
        wsl -d Ubuntu -u hermes -- pgrep -af -x "/home/hermes/projects/nutrition_bot/venv/bin/python3 -m bot.main" 2>$null
    )
    $legacyPolling = @(
        $legacyPollingRaw | Where-Object {
            $_ -match '^\d+ /home/hermes/projects/nutrition_bot/venv/bin/python3 -m bot\.main$'
        }
    )
    $taskState = if ($botTask) { [string]$botTask.State } else { "Unavailable" }
    if ($taskState -eq "Unavailable") {
        try {
            $schedule = New-Object -ComObject "Schedule.Service"
            $schedule.Connect()
            $scheduledTask = $schedule.GetFolder("\").GetTask("WellnessBot")
            $taskState = if ($scheduledTask.State -eq 4) { "Running" } else { "Present" }
        } catch {
            $taskState = "Unavailable"
        }
    }

    [pscustomobject]@{
        StageId = $stage.stage_id
        Workspace = $projectRoot
        Branch = $branch
        BranchOk = $branch -eq $stage.branch
        Head = $head
        OriginMaster = $remoteHead
        Published = $head -eq $remoteHead
        TrackedDirtyFiles = $trackedDirty.Count
        BotTaskState = $taskState
        BotProcessCount = if ($botProcessCount -ge 0) { $botProcessCount } else { "Unavailable" }
        LegacyHermesPolling = $legacyPolling.Count -gt 0
        Synchronized = (
            $branch -eq $stage.branch -and
            $head -eq $remoteHead -and
            $trackedDirty.Count -eq 0 -and
            $legacyPolling.Count -eq 0
        )
    } | Format-List
} finally {
    Pop-Location
}
