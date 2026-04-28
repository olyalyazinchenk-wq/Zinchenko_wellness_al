$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$entryPath = Join-Path $projectRoot "WellnessBot\main.py"
$stdoutPath = Join-Path $projectRoot "bot.stdout.log"
$stderrPath = Join-Path $projectRoot "bot.stderr.log"
$rootEnvPath = Join-Path $projectRoot ".env"
$botEnvPath = Join-Path $projectRoot "WellnessBot\.env"
$ycPath = Join-Path $env:USERPROFILE "yandex-cloud-cli\yc.exe"

function Get-EnvValue {
    param(
        [string]$Path,
        [string]$Key
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }
    $match = Get-Content -Encoding UTF8 -LiteralPath $Path | Where-Object { $_ -match "^$Key=" } | Select-Object -First 1
    if (-not $match) {
        return $null
    }
    return ($match -split "=", 2)[1]
}

function Set-EnvValueNoBom {
    param(
        [string]$Path,
        [string]$Key,
        [string]$Value
    )
    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    $lines = Get-Content -Encoding UTF8 -LiteralPath $Path
    $updated = $false
    $out = foreach ($line in $lines) {
        if ($line -match "^$Key=") {
            $updated = $true
            "$Key=$Value"
        } else {
            $line
        }
    }
    if (-not $updated) {
        $out += "$Key=$Value"
    }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines((Resolve-Path -LiteralPath $Path), $out, $utf8NoBom)
}

function Test-EnvTrue {
    param([string]$Value)
    return ($Value -and $Value.Trim().ToLowerInvariant() -eq "true")
}

function Invoke-YcIamCreateToken {
    param(
        [string]$CliPath,
        [int]$TimeoutSeconds = 20
    )

    $stdoutFile = [System.IO.Path]::GetTempFileName()
    $stderrFile = [System.IO.Path]::GetTempFileName()

    try {
        $proc = Start-Process `
            -FilePath $CliPath `
            -ArgumentList @("iam", "create-token") `
            -RedirectStandardOutput $stdoutFile `
            -RedirectStandardError $stderrFile `
            -PassThru `
            -WindowStyle Hidden

        if (-not (Wait-Process -Id $proc.Id -Timeout $TimeoutSeconds -ErrorAction SilentlyContinue)) {
            Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
            throw "yc iam create-token timed out after $TimeoutSeconds seconds."
        }

        $stdout = (Get-Content -LiteralPath $stdoutFile -Raw -ErrorAction SilentlyContinue).Trim()
        $stderr = (Get-Content -LiteralPath $stderrFile -Raw -ErrorAction SilentlyContinue).Trim()

        if ($proc.ExitCode -ne 0) {
            if ($stderr) {
                throw $stderr
            }
            throw "yc iam create-token failed with exit code $($proc.ExitCode)."
        }

        return $stdout
    } finally {
        Remove-Item -LiteralPath $stdoutFile, $stderrFile -Force -ErrorAction SilentlyContinue
    }
}

function Get-ProjectBotProcesses {
    $allPython = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -like "python*"
    }

    foreach ($proc in $allPython) {
        $cmd = [string]$proc.CommandLine
        $exe = [string]$proc.ExecutablePath
        $isProjectBot = $false

        if ($exe -eq $pythonPath) { $isProjectBot = $true }
        if ($cmd.Contains($entryPath)) { $isProjectBot = $true }
        elseif ($cmd.Contains("WellnessBot\main.py")) { $isProjectBot = $true }

        if ($isProjectBot) {
            [pscustomobject]@{
                ProcessId = [int]$proc.ProcessId
            }
        }
    }
}

if (-not (Test-Path -LiteralPath $pythonPath)) {
    Write-Error "Python virtual environment is missing at .venv\Scripts\python.exe."
    exit 1
}

if (-not (Test-Path -LiteralPath $entryPath)) {
    Write-Error "Bot entry file is missing: WellnessBot\main.py"
    exit 1
}

$llmUseIamToken = Get-EnvValue -Path $rootEnvPath -Key "LLM_USE_IAM_TOKEN"
$sttUseIamToken = Get-EnvValue -Path $rootEnvPath -Key "STT_USE_IAM_TOKEN"
$needsIamToken = (Test-EnvTrue $llmUseIamToken) -or (Test-EnvTrue $sttUseIamToken)

if ($needsIamToken) {
    if (Test-Path -LiteralPath $ycPath) {
        try {
            $iamToken = Invoke-YcIamCreateToken -CliPath $ycPath
            if ($iamToken) {
                if (Test-EnvTrue $llmUseIamToken) {
                    Set-EnvValueNoBom -Path $rootEnvPath -Key "LLM_API_KEY" -Value $iamToken
                    Set-EnvValueNoBom -Path $botEnvPath -Key "LLM_API_KEY" -Value $iamToken
                    Set-EnvValueNoBom -Path $rootEnvPath -Key "LLM_USE_IAM_TOKEN" -Value "true"
                    Set-EnvValueNoBom -Path $botEnvPath -Key "LLM_USE_IAM_TOKEN" -Value "true"
                }
                if (Test-EnvTrue $sttUseIamToken) {
                    Set-EnvValueNoBom -Path $rootEnvPath -Key "STT_API_KEY" -Value $iamToken
                    Set-EnvValueNoBom -Path $botEnvPath -Key "STT_API_KEY" -Value $iamToken
                    Set-EnvValueNoBom -Path $rootEnvPath -Key "STT_USE_IAM_TOKEN" -Value "true"
                    Set-EnvValueNoBom -Path $botEnvPath -Key "STT_USE_IAM_TOKEN" -Value "true"
                }
                Write-Output "Yandex IAM token refreshed."
            } else {
                Write-Warning "Yandex IAM token refresh returned an empty value."
            }
        } catch {
            Write-Warning "Yandex IAM token refresh failed: $($_.Exception.Message)"
        }
    } else {
        Write-Warning "Yandex CLI was not found at $ycPath. Existing IAM-backed keys will be used."
    }
}

$existing = @(Get-ProjectBotProcesses)
if ($existing) {
    $existing | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
    Start-Sleep -Seconds 1
}

# Normalize PATH casing to avoid Start-Process dictionary collision on some Windows setups.
$pathValue = $env:Path
if (Test-Path Env:PATH) {
    Remove-Item Env:PATH -ErrorAction SilentlyContinue
}
$env:Path = $pathValue

Start-Process `
    -FilePath $pythonPath `
    -ArgumentList "WellnessBot\main.py" `
    -WorkingDirectory $projectRoot `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath

Write-Output "Bot start command issued."
