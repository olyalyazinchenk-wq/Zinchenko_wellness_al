<#
.SYNOPSIS
    Unified Development & Operations CLI for Keto-Balance (NutriOK).
.DESCRIPTION
    Usage:
        .\ops\dev.ps1 status        - Check bot, proxy, disk, and sync health
        .\ops\dev.ps1 test          - Run full pytest test suite
        .\ops\dev.ps1 logs          - View recent bot logs
        .\ops\dev.ps1 bot-start     - Start the Scheduled Task WellnessBot
        .\ops\dev.ps1 bot-stop      - Stop the Scheduled Task WellnessBot
        .\ops\dev.ps1 bot-restart   - Cleanly restart the Scheduled Task
        .\ops\dev.ps1 sync          - Run multi-agent sync check
#>
param(
    [Parameter(Position=0)]
    [ValidateSet("status", "test", "logs", "bot-start", "bot-stop", "bot-restart", "sync", "help")]
    [string]$Command = "status"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$pytestExe = Join-Path $projectRoot ".venv\Scripts\pytest.exe"

switch ($Command) {
    "status" {
        Write-Host "=== 1. Windows Scheduled Task ===" -ForegroundColor Cyan
        $task = Get-ScheduledTask -TaskName "WellnessBot" -ErrorAction SilentlyContinue
        if ($task) {
            [PSCustomObject]@{
                TaskName = $task.TaskName
                State    = $task.State
            } | Format-Table -AutoSize
        } else {
            Write-Host "Task 'WellnessBot' not found!" -ForegroundColor Red
        }

        Write-Host "=== 2. Active Bot Processes ===" -ForegroundColor Cyan
        $procs = @(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*WellnessBot*main.py*" -and $_.Name -eq "python.exe" })
        if ($procs) {
            $owners = @($procs | Where-Object { $procs.ProcessId -notcontains $_.ParentProcessId })
            Write-Host "Process count: $($procs.Count) | Owner count: $($owners.Count)" -ForegroundColor Green
            $procs | Select-Object ProcessId, ParentProcessId, @{N='Started';E={$_.CreationDate}} | Format-Table -AutoSize
        } else {
            Write-Host "No active bot process running." -ForegroundColor Yellow
        }

        Write-Host "=== 3. VPN / Telegram Proxy (127.0.0.1:10808) ===" -ForegroundColor Cyan
        $conn = Get-NetTCPConnection -LocalPort 10808 -State Listen -ErrorAction SilentlyContinue
        if ($conn) {
            Write-Host "Port 10808 is LISTENING (PID: $($conn.OwningProcess[0]))" -ForegroundColor Green
            try {
                $code = & $venvPython -c "import urllib.request; p = urllib.request.ProxyHandler({'https':'http://127.0.0.1:10808'}); o = urllib.request.build_opener(p); r = o.open('https://api.telegram.org', timeout=4); print(r.status)"
                Write-Host "Telegram API connectivity: HTTP $code (OK)" -ForegroundColor Green
            } catch {
                Write-Host "Telegram API check failed: $_" -ForegroundColor Red
            }
        } else {
            Write-Host "Port 10808 is NOT listening. Please start Xray/VPN." -ForegroundColor Red
        }

        Write-Host "=== 4. Disk Space ===" -ForegroundColor Cyan
        $drive = Get-PSDrive C
        $freeGb = [math]::Round($drive.Free / 1GB, 2)
        Write-Host "C: Free space: $freeGb GB" -ForegroundColor $(if ($freeGb -ge 10) { "Green" } else { "Red" })

        Write-Host "=== 5. Git & Workspace ===" -ForegroundColor Cyan
        Set-Location $projectRoot
        $branch = git branch --show-current
        $dirty = (git status --short).Count
        Write-Host "Branch: $branch | Tracked/untracked items: $dirty" -ForegroundColor Cyan
    }

    "test" {
        Write-Host "Running test suite..." -ForegroundColor Cyan
        Set-Location $projectRoot
        & $pytestExe tests -v
    }

    "logs" {
        $logPath = Join-Path $projectRoot "bot.stderr.log"
        if (Test-Path $logPath) {
            Write-Host "=== bot.stderr.log (last 40 lines) ===" -ForegroundColor Cyan
            Get-Content $logPath -Tail 40
        } else {
            Write-Host "No bot.stderr.log found." -ForegroundColor Yellow
        }
    }

    "bot-start" {
        Write-Host "Starting Scheduled Task 'WellnessBot'..." -ForegroundColor Cyan
        Start-ScheduledTask -TaskName "WellnessBot"
        Start-Sleep -Seconds 3
        $task = Get-ScheduledTask -TaskName "WellnessBot"
        Write-Host "Task state: $($task.State)" -ForegroundColor Green
    }

    "bot-stop" {
        Write-Host "Stopping Scheduled Task 'WellnessBot'..." -ForegroundColor Yellow
        Stop-ScheduledTask -TaskName "WellnessBot" -ErrorAction SilentlyContinue
        & "$PSScriptRoot\bot-stop.ps1"
        Start-Sleep -Seconds 2
        $task = Get-ScheduledTask -TaskName "WellnessBot"
        Write-Host "Task state: $($task.State)" -ForegroundColor Yellow
    }

    "bot-restart" {
        Write-Host "Restarting Scheduled Task 'WellnessBot'..." -ForegroundColor Cyan
        Stop-ScheduledTask -TaskName "WellnessBot" -ErrorAction SilentlyContinue
        & "$PSScriptRoot\bot-stop.ps1"
        Start-Sleep -Seconds 2
        Start-ScheduledTask -TaskName "WellnessBot"
        Start-Sleep -Seconds 4
        $task = Get-ScheduledTask -TaskName "WellnessBot"
        Write-Host "Task state: $($task.State)" -ForegroundColor Green
    }

    "sync" {
        & "$PSScriptRoot\agent-sync-status.ps1"
    }

    "help" {
        Get-Help $PSCommandPath
    }
}
