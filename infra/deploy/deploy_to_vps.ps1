[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$HostName,

    [string]$SshUser = "root",
    [string]$SshKeyPath = "$HOME\.ssh\id_ed25519",
    [string]$RemoteAppDir = "/opt/antigravity-wellness",
    [string]$ArchiveName = "antigravity-wellness-deploy.tar.gz"
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    Write-Host ""
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message)
}

function Require-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

function Run-External {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $FilePath $($Arguments -join ' ')"
    }
}

Require-Command -Name ssh
Require-Command -Name scp
Require-Command -Name tar

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$archivePath = Join-Path $env:TEMP $ArchiveName
$remote = "${SshUser}@${HostName}"
$remoteArchive = "/tmp/$ArchiveName"

if (Test-Path $archivePath) {
    Remove-Item -LiteralPath $archivePath -Force
}

Write-Log "Packing project without secrets, venv, logs, and runtime data"
Push-Location $projectRoot
try {
    Run-External -FilePath "tar" -Arguments @(
        "--exclude=.git",
        "--exclude=.venv",
        "--exclude=.env",
        "--exclude=WellnessBot/data",
        "--exclude=bot.stdout.log",
        "--exclude=bot.stderr.log",
        "--exclude=ops/reports",
        "-czf",
        $archivePath,
        "."
    )
}
finally {
    Pop-Location
}

$sshCommonArgs = @(
    "-i", $SshKeyPath,
    "-o", "BatchMode=yes",
    "-o", "StrictHostKeyChecking=accept-new"
)

Write-Log "Uploading archive to $remote"
Run-External -FilePath "scp" -Arguments ($sshCommonArgs + @($archivePath, "${remote}:${remoteArchive}"))

Write-Log "Extracting project and running server installer"
$remoteCommand = @"
set -euo pipefail
mkdir -p '$RemoteAppDir'
tar -xzf '$remoteArchive' -C '$RemoteAppDir'
rm -f '$remoteArchive'
cd '$RemoteAppDir'
bash infra/deploy/install_ubuntu.sh
"@

Run-External -FilePath "ssh" -Arguments ($sshCommonArgs + @($remote, $remoteCommand))

Write-Log "Deploy package uploaded. Fill $RemoteAppDir/.env on the server if it is not there yet, then run: systemctl restart wellness-bot"
