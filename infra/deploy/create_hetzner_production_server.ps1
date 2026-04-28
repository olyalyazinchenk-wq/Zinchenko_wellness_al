[CmdletBinding()]
param(
    [string]$Token = $env:HCLOUD_TOKEN,
    [string]$ServerName = ("wellness-prod-" + (Get-Date -Format "yyyyMMddHHmmss")),
    [string]$Location = "hel1",
    [string]$ServerType = "cx43",
    [string]$Image = "ubuntu-24.04",
    [string]$SshKeyPath = "$HOME\.ssh\id_ed25519",
    [switch]$SkipDeploy
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    Write-Host ""
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message)
}

function Invoke-HcloudApi {
    param(
        [Parameter(Mandatory = $true)][ValidateSet("GET", "POST")] [string]$Method,
        [Parameter(Mandatory = $true)][string]$Path,
        [object]$Body
    )

    $headers = @{
        Authorization = "Bearer $Token"
        "Content-Type" = "application/json"
    }

    $uri = "https://api.hetzner.cloud/v1$Path"
    if ($PSBoundParameters.ContainsKey("Body")) {
        return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers -Body ($Body | ConvertTo-Json -Depth 10)
    }

    return Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers
}

function Require-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

function Ensure-SshKey {
    param([string]$PrivateKeyPath)

    $publicKeyPath = "$PrivateKeyPath.pub"
    if ((Test-Path $PrivateKeyPath) -and (Test-Path $publicKeyPath)) {
        return
    }

    $sshDir = Split-Path -Parent $PrivateKeyPath
    if (-not (Test-Path $sshDir)) {
        New-Item -ItemType Directory -Force -Path $sshDir | Out-Null
    }

    Write-Log "Generating local SSH key pair at $PrivateKeyPath"
    & ssh-keygen -t ed25519 -N "" -f $PrivateKeyPath | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "ssh-keygen failed."
    }
}

function Get-OrCreateHcloudSshKey {
    param(
        [string]$PublicKey,
        [string]$KeyName
    )

    Write-Log "Checking Hetzner SSH keys"
    $keysResponse = Invoke-HcloudApi -Method GET -Path "/ssh_keys?per_page=50"
    $existing = $keysResponse.ssh_keys | Where-Object { $_.public_key.Trim() -eq $PublicKey.Trim() } | Select-Object -First 1
    if ($existing) {
        return $existing.id
    }

    Write-Log "Uploading SSH key to Hetzner Cloud"
    $created = Invoke-HcloudApi -Method POST -Path "/ssh_keys" -Body @{
        name       = $KeyName
        public_key = $PublicKey
    }
    return $created.ssh_key.id
}

function Wait-HcloudAction {
    param([int]$ActionId)

    do {
        Start-Sleep -Seconds 5
        $action = Invoke-HcloudApi -Method GET -Path "/actions/$ActionId"
        Write-Log ("Server action status: {0}" -f $action.action.status)
    } while ($action.action.status -eq "running")

    if ($action.action.status -ne "success") {
        throw "Hetzner action $ActionId did not complete successfully."
    }
}

function Get-ServerIpv4 {
    param([int]$ServerId)

    $server = Invoke-HcloudApi -Method GET -Path "/servers/$ServerId"
    return $server.server.public_net.ipv4.ip
}

function Wait-ForSsh {
    param([string]$HostName)

    for ($i = 0; $i -lt 48; $i++) {
        $ready = Test-NetConnection -ComputerName $HostName -Port 22 -InformationLevel Quiet -WarningAction SilentlyContinue
        if ($ready) {
            return
        }
        Write-Log "Waiting for SSH on $HostName:22"
        Start-Sleep -Seconds 5
    }

    throw "SSH did not become reachable on $HostName:22 in time."
}

if (-not $Token) {
    throw "Set HCLOUD_TOKEN or pass -Token with a Hetzner Cloud API token."
}

Require-Command -Name ssh
Require-Command -Name scp
Require-Command -Name ssh-keygen
Require-Command -Name tar

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$metadataPath = Join-Path $scriptDir "$ServerName.hetzner.json"

Ensure-SshKey -PrivateKeyPath $SshKeyPath
$publicKey = (Get-Content -Raw "$SshKeyPath.pub").Trim()
$keyName = "codex-wellness-$env:COMPUTERNAME"
$sshKeyId = Get-OrCreateHcloudSshKey -PublicKey $publicKey -KeyName $keyName

Write-Log "Creating production reserve server $ServerName ($ServerType, $Location)"
$createResponse = Invoke-HcloudApi -Method POST -Path "/servers" -Body @{
    name               = $ServerName
    server_type        = $ServerType
    image              = $Image
    location           = $Location
    ssh_keys           = @($sshKeyId)
    start_after_create = $true
    backups            = $true
    public_net         = @{
        enable_ipv4 = $true
        enable_ipv6 = $false
    }
    labels             = @{
        app         = "antigravity-wellness"
        role        = "telegram-bot"
        environment = "production"
        managed     = "codex"
    }
}

$serverId = $createResponse.server.id
$actionId = $createResponse.action.id

@{
    server_id   = $serverId
    action_id   = $actionId
    name        = $ServerName
    location    = $Location
    server_type = $ServerType
    image       = $Image
    backups     = $true
} | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 $metadataPath

Wait-HcloudAction -ActionId $actionId

Write-Log "Fetching server IP"
$ipAddress = $null
for ($i = 0; $i -lt 20 -and -not $ipAddress; $i++) {
    $ipAddress = Get-ServerIpv4 -ServerId $serverId
    if (-not $ipAddress) {
        Start-Sleep -Seconds 3
    }
}

if (-not $ipAddress) {
    throw "Server was created, but no public IPv4 address was found."
}

Write-Log "Server public IP: $ipAddress"
Wait-ForSsh -HostName $ipAddress

if (-not $SkipDeploy) {
    Write-Log "Deploying WellnessBot to the new server"
    & (Join-Path $scriptDir "deploy_to_vps.ps1") -HostName $ipAddress -SshKeyPath $SshKeyPath
    if ($LASTEXITCODE -ne 0) {
        throw "Deploy helper failed."
    }
}

Write-Log "Production server is ready"
Write-Host ""
Write-Host "Server: $ServerName"
Write-Host "IP: $ipAddress"
Write-Host "Type: $ServerType"
Write-Host "Location: $Location"
Write-Host "Backups: enabled"
Write-Host "Metadata: $metadataPath"
