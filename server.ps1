#Requires -Version 5.1

$scriptPath = $MyInvocation.MyCommand.Path
$projectRoot = if ($scriptPath) { Split-Path -Parent $scriptPath } else { (Get-Location).Path }

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add('http://localhost:8080/')
$listener.Start()

Write-Output "Started on http://localhost:8080"
Write-Output "Project: $projectRoot"

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $res = $context.Response
        $req = $context.Request

        try {
            if ($req.Url.LocalPath -match 'mini') {
                $file = Join-Path $projectRoot "mini-app\\index.html"
            } else {
                $file = Join-Path $projectRoot "landing\\index.html"
            }

            if (-not (Test-Path -LiteralPath $file)) {
                $res.StatusCode = 404
                $bytes = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $file")
            } else {
                $bytes = [System.IO.File]::ReadAllBytes($file)
                $res.ContentType = 'text/html; charset=utf-8'
            }

            $res.ContentLength64 = $bytes.Length
            $res.OutputStream.Write($bytes, 0, $bytes.Length)
        } catch {
            Write-Error "Request error: $_"
            $res.StatusCode = 500
        } finally {
            $res.Close()
        }
    }
} catch {
    Write-Error "Server error: $_"
} finally {
    if ($listener.IsListening) {
        $listener.Stop()
    }
    $listener.Close()
    Write-Output "Server stopped."
}
