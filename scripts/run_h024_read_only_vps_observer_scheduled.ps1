[CmdletBinding()]
param(
    [string]$Root = "",
    [string]$ObserverScriptPath = "",
    [string]$LogDirectory = "",
    [int]$RetentionCount = 288,
    [int]$RetentionDays = 14
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-Root {
    param([string]$InputRoot)
    if ([string]::IsNullOrWhiteSpace($InputRoot)) {
        return (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
    }
    return (Resolve-Path $InputRoot).Path
}

function Invoke-LogRotation {
    param(
        [Parameter(Mandatory=$true)][string]$Directory,
        [int]$KeepCount,
        [int]$KeepDays
    )

    if (-not (Test-Path -LiteralPath $Directory -PathType Container)) {
        return
    }

    if ($KeepDays -gt 0) {
        $cutoff = (Get-Date).ToUniversalTime().AddDays(-1 * $KeepDays)
        Get-ChildItem -LiteralPath $Directory -Filter "*.log" -File |
            Where-Object { $_.LastWriteTimeUtc -lt $cutoff } |
            Remove-Item -Force
    }

    if ($KeepCount -gt 0) {
        Get-ChildItem -LiteralPath $Directory -Filter "*.log" -File |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -Skip $KeepCount |
            Remove-Item -Force
    }
}

$Root = Resolve-Root -InputRoot $Root

if ([string]::IsNullOrWhiteSpace($ObserverScriptPath)) {
    $ObserverScriptPath = Join-Path $Root "scripts\run_h024_read_only_vps_observer_once.ps1"
}

if ([string]::IsNullOrWhiteSpace($LogDirectory)) {
    $LogDirectory = Join-Path $Root "reports\runtime\h024_read_only_vps_observer\logs"
}

$StateDirectory = Split-Path $LogDirectory -Parent
New-Item -ItemType Directory -Force -Path $StateDirectory, $LogDirectory | Out-Null

$startedAtUtc = (Get-Date).ToUniversalTime()
$stamp = $startedAtUtc.ToString("yyyyMMddTHHmmssfffZ")
$logPath = Join-Path $LogDirectory "h024_read_only_vps_observer_${stamp}.log"

$status = "COMPLETED"
$exitCode = 0

try {
    if (-not (Test-Path -LiteralPath $ObserverScriptPath -PathType Leaf)) {
        throw "Observer script not found: $ObserverScriptPath"
    }

    Push-Location $Root
    try {
        & powershell -NoProfile -ExecutionPolicy Bypass -File $ObserverScriptPath *>&1 |
            Tee-Object -FilePath $logPath
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    if ($exitCode -ne 0) {
        $status = "FAILED"
    }
}
catch {
    $status = "FAILED"
    $exitCode = 1
    $_ | Out-String | Out-File -LiteralPath $logPath -Append -Encoding UTF8
}
finally {
    Invoke-LogRotation -Directory $LogDirectory -KeepCount $RetentionCount -KeepDays $RetentionDays
}

$completedAtUtc = (Get-Date).ToUniversalTime()

$summary = [ordered]@{
    schema_version = 1
    strategy = "H024"
    component = "read_only_vps_observer_scheduled_wrapper"
    started_at_utc = $startedAtUtc.ToString("o")
    completed_at_utc = $completedAtUtc.ToString("o")
    status = $status
    exit_code = $exitCode
    observer_script_path = $ObserverScriptPath
    log_path = $logPath
    log_directory = $LogDirectory
    retention_count = $RetentionCount
    retention_days = $RetentionDays
    read_only_observer_only = $true
    trading_authorized = $false
    broker_mutation_authorized = $false
    live_execution_authorized = $false
}

$summaryPath = Join-Path $StateDirectory "last_run_summary.json"
$summaryJson = $summary | ConvertTo-Json -Depth 8
$utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
[System.IO.File]::WriteAllText($summaryPath, ($summaryJson + [Environment]::NewLine), $utf8NoBom)

Write-Host "H024 read-only VPS observer scheduled wrapper finished."
Write-Host "Status: $status"
Write-Host "Exit code: $exitCode"
Write-Host "Log: $logPath"
Write-Host "Summary: $summaryPath"

exit $exitCode
