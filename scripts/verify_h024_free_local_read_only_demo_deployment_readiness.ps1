[CmdletBinding()]
param(
    [string]$Root = (Resolve-Path ".").Path,
    [string]$TaskName = "H024 Read Only VPS Observer",
    [int]$ExpectedIntervalMinutes = 5,
    [int]$MinScheduledRunCount = 12,
    [double]$MinScheduledSpanMinutes = 55,
    [int]$MaxPacketAgeMinutes = 120,
    [int]$MaxLatestRunAgeMinutes = 30,
    [switch]$SkipRefresh
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path $Root).Path
$BuilderPath = Join-Path $RepoRoot "scripts\build_h024_free_local_read_only_demo_deployment_readiness.ps1"
$OutputJsonPath = Join-Path $RepoRoot "reports\h024_free_local_read_only_demo_deployment_readiness.json"

function Invoke-CheckedPowerShell {
    param(
        [Parameter(Mandatory = $true)][string]$ScriptPath,
        [Parameter(Mandatory = $true)][object[]]$Arguments
    )

    & powershell -NoProfile -ExecutionPolicy Bypass -File $ScriptPath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $ScriptPath"
    }
}

if (-not $SkipRefresh) {
    Write-Host "=== Refresh prerequisite read-only observer packets ==="

    Invoke-CheckedPowerShell `
        -ScriptPath (Join-Path $RepoRoot "scripts\check_h024_read_only_vps_observer_health.ps1") `
        -Arguments @("-MaxAgeMinutes", $MaxPacketAgeMinutes)

    Invoke-CheckedPowerShell `
        -ScriptPath (Join-Path $RepoRoot "scripts\check_h024_read_only_vps_observer_task_state.ps1") `
        -Arguments @("-ExpectedIntervalMinutes", $ExpectedIntervalMinutes, "-MaxLastRunAgeMinutes", $MaxLatestRunAgeMinutes)

    Invoke-CheckedPowerShell `
        -ScriptPath (Join-Path $RepoRoot "scripts\run_h024_read_only_vps_recovery_drill_preview.ps1") `
        -Arguments @("-MaxEvidenceAgeMinutes", $MaxPacketAgeMinutes)

    Invoke-CheckedPowerShell `
        -ScriptPath (Join-Path $RepoRoot "scripts\build_h024_read_only_vps_observer_evidence_bundle.ps1") `
        -Arguments @("-MaxPacketAgeMinutes", $MaxPacketAgeMinutes)

    Invoke-CheckedPowerShell `
        -ScriptPath (Join-Path $RepoRoot "scripts\build_h024_read_only_vps_observer_continuity_summary.ps1") `
        -Arguments @("-MinRunCount", 6, "-MaxPacketAgeMinutes", $MaxPacketAgeMinutes, "-MaxLatestRunAgeMinutes", 60)

    Invoke-CheckedPowerShell `
        -ScriptPath (Join-Path $RepoRoot "scripts\build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1") `
        -Arguments @(
            "-Root", $RepoRoot,
            "-ExpectedIntervalMinutes", $ExpectedIntervalMinutes,
            "-MinRunCount", $MinScheduledRunCount,
            "-MinCadenceWindowMinutes", $MinScheduledSpanMinutes,
            "-MaxLatestRunAgeMinutes", $MaxLatestRunAgeMinutes,
            "-MaxPacketAgeMinutes", $MaxPacketAgeMinutes,
            "-MaxAllowedGapMinutes", 10,
            "-MinInterRunGapMinutes", 3
        )
}

Write-Host ""
Write-Host "=== Build H024 free local read-only demo deployment readiness packet ==="

Invoke-CheckedPowerShell `
    -ScriptPath $BuilderPath `
    -Arguments @(
        "-Root", $RepoRoot,
        "-TaskName", $TaskName,
        "-ExpectedIntervalMinutes", $ExpectedIntervalMinutes,
        "-MinScheduledRunCount", $MinScheduledRunCount,
        "-MinScheduledSpanMinutes", $MinScheduledSpanMinutes,
        "-MaxPacketAgeMinutes", $MaxPacketAgeMinutes,
        "-MaxLatestRunAgeMinutes", $MaxLatestRunAgeMinutes
    )

$Packet = Get-Content -Raw -Path $OutputJsonPath | ConvertFrom-Json

Write-Host ""
Write-Host "=== Demo readiness packet summary ==="

[pscustomobject]@{
    verdict = $Packet.verdict
    violations = @($Packet.violations).Count
    read_only_demo_ready = $Packet.read_only_demo_ready
    trading_authorized = $Packet.read_only_demo_deployment_readiness_authorizes_trading
    operator_state = $Packet.operator_state
} | Format-List

if ($Packet.verdict -ne "PASS" -or @($Packet.violations).Count -ne 0) {
    Write-Host ""
    Write-Host "=== Violations ==="
    $Packet.violations | ConvertTo-Json -Depth 30
    throw "FAIL_CLOSED: H024 free local read-only demo deployment readiness is not proven. No trading authorized."
}

Write-Host ""
Write-Host "H024 FREE LOCAL READ-ONLY DEMO DEPLOYMENT READINESS: PASS"
Write-Host "This authorizes status/demo observation only."
Write-Host "No trading authorized. No broker mutation authorized. reports/ must remain untracked."

Write-Host ""
Write-Host "=== Git state ==="
git -C $RepoRoot status --short
git -C $RepoRoot status