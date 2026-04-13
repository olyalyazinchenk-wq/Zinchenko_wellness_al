Write-Output "=== connection-check ==="

$gitOk = [bool](Get-Command git -ErrorAction SilentlyContinue)
$venvOk = Test-Path -LiteralPath ".\.venv\Scripts\python.exe"
$ycOk = Test-Path -LiteralPath "C:\Users\HP\yandex-cloud-cli\yc.exe"
$telegramOk = Test-Path -LiteralPath "C:\Users\HP\AppData\Roaming\Telegram Desktop\Telegram.exe"

$rows = @(
    @{ Name = "Git CLI"; Ok = $gitOk },
    @{ Name = "Python venv"; Ok = $venvOk },
    @{ Name = "Yandex CLI"; Ok = $ycOk },
    @{ Name = "Telegram Desktop"; Ok = $telegramOk }
)

foreach ($row in $rows) {
    $status = if ($row.Ok) { "OK" } else { "MISSING" }
    Write-Output ("[{0}] {1}" -f $status, $row.Name)
}
