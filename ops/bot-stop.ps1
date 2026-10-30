function Get-ProjectBotProcesses {
    $allProcs = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue)
    $roots = @(
        $allProcs | Where-Object {
            $_.Name -like "python*" -and
            ([string]$_.CommandLine -match 'WellnessBot[\\/]+main\.py')
        }
    )
    if (-not $roots) {
        return
    }

    $targetIds = New-Object 'System.Collections.Generic.HashSet[int]'
    foreach ($r in $roots) {
        [void]$targetIds.Add([int]$r.ProcessId)
    }

    $added = $true
    while ($added) {
        $added = $false
        foreach ($proc in $allProcs) {
            $pidVal = [int]$proc.ProcessId
            $ppidVal = [int]$proc.ParentProcessId
            if (-not $targetIds.Contains($pidVal) -and $targetIds.Contains($ppidVal)) {
                [void]$targetIds.Add($pidVal)
                $added = $true
            }
        }
    }

    foreach ($proc in $allProcs) {
        if ($targetIds.Contains([int]$proc.ProcessId)) {
            [pscustomobject]@{
                ProcessId = [int]$proc.ProcessId
                ParentProcessId = [int]$proc.ParentProcessId
                Name = $proc.Name
                ExecutablePath = [string]$proc.ExecutablePath
                CommandLine = [string]$proc.CommandLine
            }
        }
    }
}

$targets = @(Get-ProjectBotProcesses)

if (-not $targets) {
    Write-Output "No project bot process is running."
    exit 0
}

$targets | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Write-Output ("Stopped {0} bot process(es)." -f $targets.Count)
