$ErrorActionPreference = "Stop"
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$rootEnvPath = Join-Path $projectRoot ".env"
$botEnvPath = Join-Path $projectRoot "WellnessBot\.env"

function Get-EnvValue {
    param([string]$Path, [string]$Key)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $match = Get-Content -Encoding UTF8 -LiteralPath $Path | Where-Object { $_ -match "^$Key=" } | Select-Object -First 1
    if (-not $match) { return $null }
    return ($match -split "=", 2)[1]
}

function Set-EnvValueNoBom {
    param([string]$Path, [string]$Key, [string]$Value)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType File -Path $Path -Force | Out-Null
        $lines = @()
    } else {
        $lines = Get-Content -Encoding UTF8 -LiteralPath $Path
    }
    $updated = $false
    $out = foreach ($line in $lines) {
        if ($line -match "^$Key=") {
            $updated = $true
            "$Key=$Value"
        } else {
            $line
        }
    }
    if (-not $updated) { $out += "$Key=$Value" }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllLines((Resolve-Path -LiteralPath $Path), $out, $utf8NoBom)
}

function Read-SecretPlainText {
    param([string]$Prompt)
    $secure = Read-Host $Prompt -AsSecureString
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
}

$key = (Read-SecretPlainText "Введите AITUNNEL API Key").Trim()
if (-not $key) {
    Write-Error "API key пустой. Запустите скрипт ещё раз и вставьте ключ."
    exit 1
}

$sttProjectId = Get-EnvValue -Path $rootEnvPath -Key "STT_PROJECT_ID"
if (-not $sttProjectId) { $sttProjectId = Get-EnvValue -Path $rootEnvPath -Key "LLM_PROJECT_ID" }
$currentSttKey = Get-EnvValue -Path $rootEnvPath -Key "STT_API_KEY"
if (-not $currentSttKey) { $currentSttKey = Get-EnvValue -Path $rootEnvPath -Key "LLM_API_KEY" }

foreach ($envPath in @($rootEnvPath, $botEnvPath)) {
    Set-EnvValueNoBom -Path $envPath -Key "AITUNNEL_API_KEY" -Value $key
    Set-EnvValueNoBom -Path $envPath -Key "AITUNNEL_MODEL" -Value "deepseek-v3.2"
    Set-EnvValueNoBom -Path $envPath -Key "AITUNNEL_BASE_URL" -Value "https://api.aitunnel.ru/v1/"
    Set-EnvValueNoBom -Path $envPath -Key "LLM_PROVIDER" -Value "openai_compatible"
    Set-EnvValueNoBom -Path $envPath -Key "LLM_API_KEY" -Value $key
    Set-EnvValueNoBom -Path $envPath -Key "LLM_MODEL" -Value "deepseek-v3.2"
    Set-EnvValueNoBom -Path $envPath -Key "LLM_API_MODE" -Value "chat_completions"
    Set-EnvValueNoBom -Path $envPath -Key "LLM_BASE_URL" -Value "https://api.aitunnel.ru/v1/"
    Set-EnvValueNoBom -Path $envPath -Key "LLM_USE_IAM_TOKEN" -Value "false"
    Set-EnvValueNoBom -Path $envPath -Key "STT_PROVIDER" -Value "yandex_speechkit"
    Set-EnvValueNoBom -Path $envPath -Key "STT_USE_IAM_TOKEN" -Value "true"
    if ($sttProjectId) { Set-EnvValueNoBom -Path $envPath -Key "STT_PROJECT_ID" -Value $sttProjectId }
    if ($currentSttKey) { Set-EnvValueNoBom -Path $envPath -Key "STT_API_KEY" -Value $currentSttKey }
}

Write-Output "AITUNNEL DeepSeek подключён: base_url=https://api.aitunnel.ru/v1/, model=deepseek-v3.2. Ключ не выводился на экран."
Write-Output "Голосовые оставлены через Yandex SpeechKit."
Write-Output "Теперь перезапустите бота через ops\bot-start.ps1."