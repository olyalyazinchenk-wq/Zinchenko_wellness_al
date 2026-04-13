 = New-Object System.Net.HttpListener
.Prefixes.Add('http://localhost:8080/')
.Start()
Write-Output 'Started on http://localhost:8080'
while ($true) {
    $context = $listener.GetContext()
    $res = $context.Response
    $req = $context.Request
    
    if ($req.Url.LocalPath -match 'mini') {
        $file = 'C:\Users\HP\Desktop\Новая папка\mini-app\index.html'
    } else {
        $file = 'C:\Users\HP\Desktop\Новая папка\landing\index.html'
    }
    
    $bytes = [System.IO.File]::ReadAllBytes($file)
    $res.ContentType = 'text/html; charset=utf-8'
    $res.ContentLength64 = $bytes.Length
    $res.OutputStream.Write($bytes, 0, $bytes.Length)
    $res.Close()
}
