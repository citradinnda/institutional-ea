[CmdletBinding()]
param(
    [string]$Root = "",
    [int]$MaxAgeMinutes = 30,
    [string]$HealthOutPath = "",
    [switch]$NoFailExit
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
else {
    $Root = (Resolve-Path $Root).Path
}

if ($MaxAgeMinutes -lt 1) {
    throw "MaxAgeMinutes must be positive."
}

$nowUtc = (Get-Date).ToUniversalTime()
$stateDirectory = Join-Path $Root "reports\runtime\h024_read_only_vps_observer"
$defaultLogDirectory = Join-Path $stateDirectory "logs"

if ([string]::IsNullOrWhiteSpace($HealthOutPath)) {
    $HealthOutPath = Join-Path $Root "reports\h024_read_only_vps_observer_healthcheck.json"
}

function Get-PropertyValue {
    param(
        [Parameter(Mandatory=$true)]$Object,
        [Parameter(Mandatory=$true)][string[]]$Names
    )

    foreach ($name in $Names) {
        $property = $Object.PSObject.Properties[$name]
        if ($null -ne $property) {
            return $property.Value
        }
    }

    return $null
}

function Convert-ToUtcDateTime {
    param($Value)

    if ($null -eq $Value) {
        return $null
    }

    try {
        $parsed = [DateTimeOffset]::Parse(
            [string]$Value,
            [System.Globalization.CultureInfo]::InvariantCulture,
            [System.Globalization.DateTimeStyles]::AssumeUniversal
        )
        return $parsed.UtcDateTime
    }
    catch {
        return $null
    }
}

function Count-Violations {
    param($Value)

    if ($null -eq $Value) {
        return 0
    }

    if ($Value -is [array]) {
        return $Value.Count
    }

    if ($Value -is [System.Collections.ICollection]) {
        return $Value.Count
    }

    if ([string]::IsNullOrWhiteSpace([string]$Value)) {
        return 0
    }

    return 1
}

function Read-JsonlComponent {
    param(
        [Parameter(Mandatory=$true)][string]$Name,
        [Parameter(Mandatory=$true)][string]$RelativePath
    )

    $path = Join-Path $Root $RelativePath
    $problems = @()

    $component = [ordered]@{
        name = $Name
        path = $path
        exists = $false
        parsed = $false
        verdict = $null
        operator_state = $null
        timestamp_utc = $null
        age_seconds = $null
        stale = $true
        upstream_violation_count = $null
        health_pass = $false
        problems = @()
    }

    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $problems += "MISSING_REPORT"
        $component.problems = $problems
        return [pscustomobject]$component
    }

    $component.exists = $true
    $line = Get-Content -LiteralPath $path -Tail 1

    if ([string]::IsNullOrWhiteSpace($line)) {
        $problems += "EMPTY_REPORT"
        $component.problems = $problems
        return [pscustomobject]$component
    }

    try {
        $record = $line | ConvertFrom-Json -ErrorAction Stop
        $component.parsed = $true
    }
    catch {
        $problems += "MALFORMED_JSONL"
        $component.problems = $problems
        return [pscustomobject]$component
    }

    $verdict = Get-PropertyValue -Object $record -Names @("verdict", "record_verdict")
    $operatorState = Get-PropertyValue -Object $record -Names @("operator_state", "state")
    $violations = Get-PropertyValue -Object $record -Names @("violations", "safety_violations")

    $component.verdict = $verdict
    $component.operator_state = $operatorState
    $component.upstream_violation_count = Count-Violations -Value $violations

    if ($verdict -ne "PASS") {
        $problems += "UPSTREAM_NOT_PASS"
    }

    if ($component.upstream_violation_count -gt 0) {
        $problems += "UPSTREAM_VIOLATIONS_PRESENT"
    }

    $timestampValue = Get-PropertyValue -Object $record -Names @(
        "observed_at_utc",
        "generated_at_utc",
        "created_at_utc",
        "evaluated_at_utc",
        "built_at_utc",
        "timestamp_utc",
        "timestamp"
    )

    $timestampUtc = Convert-ToUtcDateTime -Value $timestampValue
    if ($null -eq $timestampUtc) {
        $problems += "MISSING_OR_INVALID_TIMESTAMP"
    }
    else {
        $component.timestamp_utc = $timestampUtc.ToString("o")
        $ageSeconds = [math]::Round(($nowUtc - $timestampUtc).TotalSeconds, 3)
        $component.age_seconds = $ageSeconds
        $component.stale = ($ageSeconds -gt ($MaxAgeMinutes * 60))

        if ($component.stale) {
            $problems += "STALE_REPORT"
        }
    }

    if ($problems.Count -eq 0) {
        $component.health_pass = $true
    }

    $component.problems = $problems
    return [pscustomobject]$component
}

function Read-LastRunSummary {
    $summaryPath = Join-Path $stateDirectory "last_run_summary.json"
    $problems = @()

    $summary = [ordered]@{
        path = $summaryPath
        exists = $false
        parsed = $false
        status = $null
        exit_code = $null
        completed_at_utc = $null
        age_seconds = $null
        stale = $true
        log_path = $null
        log_exists = $false
        health_pass = $false
        problems = @()
    }

    if (-not (Test-Path -LiteralPath $summaryPath -PathType Leaf)) {
        $problems += "MISSING_LAST_RUN_SUMMARY"
        $summary.problems = $problems
        return [pscustomobject]$summary
    }

    $summary.exists = $true

    try {
        $record = Get-Content -LiteralPath $summaryPath -Raw | ConvertFrom-Json -ErrorAction Stop
        $summary.parsed = $true
    }
    catch {
        $problems += "MALFORMED_LAST_RUN_SUMMARY"
        $summary.problems = $problems
        return [pscustomobject]$summary
    }

    $status = Get-PropertyValue -Object $record -Names @("status")
    $exitCode = Get-PropertyValue -Object $record -Names @("exit_code")
    $completedValue = Get-PropertyValue -Object $record -Names @("completed_at_utc")
    $logPath = Get-PropertyValue -Object $record -Names @("log_path")

    $summary.status = $status
    $summary.exit_code = $exitCode
    $summary.log_path = $logPath

    if ($status -ne "COMPLETED") {
        $problems += "LAST_RUN_NOT_COMPLETED"
    }

    if ([int]$exitCode -ne 0) {
        $problems += "LAST_RUN_EXIT_NONZERO"
    }

    $completedUtc = Convert-ToUtcDateTime -Value $completedValue
    if ($null -eq $completedUtc) {
        $problems += "MISSING_OR_INVALID_LAST_RUN_TIMESTAMP"
    }
    else {
        $summary.completed_at_utc = $completedUtc.ToString("o")
        $ageSeconds = [math]::Round(($nowUtc - $completedUtc).TotalSeconds, 3)
        $summary.age_seconds = $ageSeconds
        $summary.stale = ($ageSeconds -gt ($MaxAgeMinutes * 60))

        if ($summary.stale) {
            $problems += "STALE_LAST_RUN"
        }
    }

    if ([string]::IsNullOrWhiteSpace([string]$logPath)) {
        $problems += "MISSING_LAST_RUN_LOG_PATH"
    }
    elseif (Test-Path -LiteralPath ([string]$logPath) -PathType Leaf) {
        $summary.log_exists = $true
    }
    else {
        $problems += "LAST_RUN_LOG_NOT_FOUND"
    }

    if ($problems.Count -eq 0) {
        $summary.health_pass = $true
    }

    $summary.problems = $problems
    return [pscustomobject]$summary
}

$components = [ordered]@{
    readiness = Read-JsonlComponent -Name "readiness" -RelativePath "reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl"
    black_swan = Read-JsonlComponent -Name "black_swan" -RelativePath "reports\h024_read_only_black_swan_guard.jsonl"
    heartbeat = Read-JsonlComponent -Name "heartbeat" -RelativePath "reports\h024_runtime_safety_heartbeat.jsonl"
    no_mutation_gate = Read-JsonlComponent -Name "no_mutation_gate" -RelativePath "reports\h024_runtime_no_mutation_safety_gate.jsonl"
}

$lastRunSummary = Read-LastRunSummary

$logDirectoryExists = Test-Path -LiteralPath $defaultLogDirectory -PathType Container
$logCount = 0
if ($logDirectoryExists) {
    $logCount = @(Get-ChildItem -LiteralPath $defaultLogDirectory -Filter "*.log" -File).Count
}

$violations = @()

foreach ($entry in $components.GetEnumerator()) {
    foreach ($problem in $entry.Value.problems) {
        $violations += "$($entry.Key):$problem"
    }
}

foreach ($problem in $lastRunSummary.problems) {
    $violations += "last_run:$problem"
}

if (-not $logDirectoryExists) {
    $violations += "logs:MISSING_LOG_DIRECTORY"
}

$verdict = "PASS"
$operatorState = "READ_ONLY_VPS_OBSERVER_HEALTHCHECK_OK_BUT_TRADING_NOT_AUTHORIZED"
$operatorNextAction = "CONTINUE_READ_ONLY_VPS_OBSERVER_NO_TRADING_AUTHORIZED"

if ($violations.Count -gt 0) {
    $verdict = "FAIL_CLOSED"
    $operatorState = "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_HEALTHCHECK_UNVERIFIED_NO_TRADING_AUTHORIZED"
    $operatorNextAction = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
}

$packet = [ordered]@{
    schema_version = 1
    strategy = "H024"
    component = "read_only_vps_observer_healthcheck"
    checked_at_utc = $nowUtc.ToString("o")
    verdict = $verdict
    operator_state = $operatorState
    operator_next_action = $operatorNextAction
    max_age_minutes = $MaxAgeMinutes
    violations = $violations
    components = $components
    last_run_summary = $lastRunSummary
    log_directory = $defaultLogDirectory
    log_directory_exists = $logDirectoryExists
    log_count = $logCount
    read_only_observer_healthcheck_authorizes_trading = $false
    trading_authorized = $false
    broker_mutation_authorized = $false
    live_execution_authorized = $false
}

$healthDirectory = Split-Path $HealthOutPath -Parent
if (-not [string]::IsNullOrWhiteSpace($healthDirectory)) {
    New-Item -ItemType Directory -Force -Path $healthDirectory | Out-Null
}

$packetJson = $packet | ConvertTo-Json -Depth 14
$utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
[System.IO.File]::WriteAllText($HealthOutPath, ($packetJson + [Environment]::NewLine), $utf8NoBom)

Write-Host "H024 read-only VPS observer healthcheck verdict: $verdict"
Write-Host "Operator state: $operatorState"
Write-Host "Violations: $($violations.Count)"
Write-Host "Health packet: $HealthOutPath"

if ($verdict -ne "PASS" -and -not $NoFailExit) {
    exit 1
}

exit 0
