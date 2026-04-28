$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"

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
                ProcessId = [int]$proc.ProcessId
                Name = $proc.Name
                ExecutablePath = $exe
                CommandLine = $cmd
            }
        }
    }
}

$targets = @(Get-ProjectBotProcesses)

if (-not $targets) {
    Write-Output "No project bot process is running."
    exit 0
}

$targets | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
Write-Output ("Stopped {0} bot process(es)." -f $targets.Count)
