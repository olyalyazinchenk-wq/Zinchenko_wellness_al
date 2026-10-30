param(
    [string]$ProjectRoot = (Get-Location).Path
)

$graphifyCmd = Get-Command graphify -ErrorAction SilentlyContinue
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
$pipxCmd = Get-Command pipx -ErrorAction SilentlyContinue

$graphDir = Join-Path $ProjectRoot "graphify-out"
$graphJson = Join-Path $graphDir "graph.json"
$graphReport = Join-Path $graphDir "GRAPH_REPORT.md"

$result = [pscustomobject]@{
    project_root = $ProjectRoot
    graphify_available = [bool]$graphifyCmd
    graphify_command = if ($graphifyCmd) { $graphifyCmd.Source } else { $null }
    python_available = [bool]$pythonCmd
    python_command = if ($pythonCmd) { $pythonCmd.Source } else { $null }
    pipx_available = [bool]$pipxCmd
    graph_json_exists = Test-Path $graphJson
    graph_report_exists = Test-Path $graphReport
    recommended_mode = $null
}

if ($result.graphify_available -and $result.graph_json_exists) {
    $result.recommended_mode = "query-or-update"
} elseif ($result.graphify_available) {
    $result.recommended_mode = "build"
} elseif ($result.python_available) {
    $result.recommended_mode = "install-or-fallback"
} else {
    $result.recommended_mode = "fallback"
}

$result | ConvertTo-Json -Depth 3
