Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Convert-SecureStringToPlainText {
    param(
        [Parameter(Mandatory = $true)]
        [Security.SecureString]$SecureValue
    )

    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureValue)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

function Set-Or-AppendEnvLine {
    param(
        [Parameter(Mandatory = $true)]
        [string]$EnvPath,
        [Parameter(Mandatory = $true)]
        [string]$Key,
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    $line = "$Key=$Value"
    if (-not (Test-Path -LiteralPath $EnvPath)) {
        Set-Content -LiteralPath $EnvPath -Value "$line`r`n" -Encoding UTF8
        return
    }

    $content = Get-Content -LiteralPath $EnvPath -Encoding UTF8
    $updated = $false
    $newContent = @()
    foreach ($entry in $content) {
        if ($entry -match "^\s*$Key=") {
            $newContent += $line
            $updated = $true
        }
        else {
            $newContent += $entry
        }
    }

    if (-not $updated) {
        $newContent += $line
    }

    Set-Content -LiteralPath $EnvPath -Value ($newContent -join "`r`n") -Encoding UTF8
}

try {
    $secureToken = Read-Host "Вставьте PAYMENT_TOKEN (ввод скрыт)" -AsSecureString
    $token = Convert-SecureStringToPlainText -SecureValue $secureToken

    if ([string]::IsNullOrWhiteSpace($token)) {
        Write-Host "Токен пустой. Изменения не внесены."
        exit 1
    }

    if ($token.Length -lt 20 -or -not ($token.Contains(":"))) {
        Write-Host "Похоже, токен неполный или повреждён. Проверьте копирование и запустите ещё раз."
        exit 1
    }

    $opsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectRoot = Resolve-Path (Join-Path $opsDir "..")
    $rootEnv = Join-Path $projectRoot ".env"
    $botEnv = Join-Path $projectRoot "WellnessBot\\.env"

    Set-Or-AppendEnvLine -EnvPath $rootEnv -Key "PAYMENT_TOKEN" -Value $token
    Set-Or-AppendEnvLine -EnvPath $botEnv -Key "PAYMENT_TOKEN" -Value $token

    Write-Host ""
    Write-Host "Готово: PAYMENT_TOKEN записан в .env и WellnessBot/.env"
    Write-Host "Теперь напишите в чат: готово"
}
catch {
    Write-Host "Ошибка: $($_.Exception.Message)"
    exit 1
}
