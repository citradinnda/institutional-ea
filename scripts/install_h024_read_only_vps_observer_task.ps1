[CmdletBinding()]
param(
    [string]$Root = "",
    [string]$TaskName = "H024 Read Only VPS Observer",
    [int]$IntervalMinutes = 5,
    [int]$RetentionCount = 288,
    [int]$RetentionDays = 14,
    [switch]$Preview,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
else {
    $Root = (Resolve-Path $Root).Path
}

if ($IntervalMinutes -lt 1 -or $IntervalMinutes -gt 1440) {
    throw "IntervalMinutes must be between 1 and 1440."
}

$wrapper = Join-Path $Root "scripts\run_h024_read_only_vps_observer_scheduled.ps1"
if (-not (Test-Path -LiteralPath $wrapper -PathType Leaf)) {
    throw "Scheduled wrapper script not found: $wrapper"
}

$argument = "-NoProfile -ExecutionPolicy Bypass -File `"$wrapper`" -Root `"$Root`" -RetentionCount $RetentionCount -RetentionDays $RetentionDays"

$previewPayload = [ordered]@{
    task_name = $TaskName
    root = $Root
    executable = "powershell.exe"
    argument = $argument
    interval_minutes = $IntervalMinutes
    retention_count = $RetentionCount
    retention_days = $RetentionDays
    preview_only = [bool]$Preview
    read_only_observer_only = $true
    trading_authorized = $false
    broker_mutation_authorized = $false
    live_execution_authorized = $false
}

if ($Preview) {
    $previewPayload | ConvertTo-Json -Depth 6
    Write-Host "Preview only. No scheduled task was registered."
    return
}

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($null -ne $existing -and -not $Force) {
    throw "Scheduled task already exists. Re-run with -Force to replace it: $TaskName"
}

$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument $argument `
    -WorkingDirectory $Root

$trigger = New-ScheduledTaskTrigger `
    -Once `
    -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) `
    -RepetitionDuration (New-TimeSpan -Days 3650)

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Runs the H024 read-only VPS observer wrapper. It is non-executing and mutation-blocked." `
    -Force:$Force | Out-Null

Write-Host "Registered scheduled task: $TaskName"
Write-Host "Interval minutes: $IntervalMinutes"
Write-Host "Wrapper: $wrapper"
