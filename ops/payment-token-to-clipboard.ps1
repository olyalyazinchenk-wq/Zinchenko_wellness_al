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

try {
    $secureToken = Read-Host "Вставьте PAYMENT_TOKEN (ввод скрыт)" -AsSecureString
    $token = Convert-SecureStringToPlainText -SecureValue $secureToken

    if ([string]::IsNullOrWhiteSpace($token)) {
        Write-Host "Токен пустой. Ничего не скопировано."
        exit 1
    }

    $line = "PAYMENT_TOKEN=$token"
    Set-Clipboard -Value $line

    Write-Host ""
    Write-Host "Готово. Строка скопирована в буфер обмена."
    Write-Host "Теперь просто вставьте её в чат: Ctrl+V"
}
catch {
    Write-Host "Ошибка: $($_.Exception.Message)"
    exit 1
}
