param(
    [string]$Root = "",
    [string]$TaskName = "H024 Read Only VPS Observer",
    [int]$MaxEvidenceAgeMinutes = 60,
    [string]$TaskStatePacketPath = "",
    [string]$HealthPacketPath = "",
    [string]$OutputPath = "",
    [string]$AlertJsonPath = "",
    [string]$AlertTextPath = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = Split-Path -Parent $PSScriptRoot
}

$Root = [System.IO.Path]::GetFullPath($Root)

if ([string]::IsNullOrWhiteSpace($TaskStatePacketPath)) {
    $TaskStatePacketPath = Join-Path $Root "reports\h024_read_only_vps_observer_task_state.json"
}
if ([string]::IsNullOrWhiteSpace($HealthPacketPath)) {
    $HealthPacketPath = Join-Path $Root "reports\h024_read_only_vps_observer_healthcheck.json"
}
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $Root "reports\h024_read_only_vps_recovery_drill_preview.json"
}
if ([string]::IsNullOrWhiteSpace($AlertJsonPath)) {
    $AlertJsonPath = Join-Path $Root "reports\h024_read_only_vps_recovery_drill_operator_alert.json"
}
if ([string]::IsNullOrWhiteSpace($AlertTextPath)) {
    $AlertTextPath = Join-Path $Root "reports\h024_read_only_vps_recovery_drill_operator_alert.txt"
}

$violations = @()

function Add-Violation {
    param(
        [Parameter(Mandatory=$true)][string]$Code,
        [Parameter(Mandatory=$true)][string]$Message,
        [string]$Severity = "ERROR"
    )
    $script:violations += [ordered]@{
        code = $Code
        severity = $Severity
        message = $Message
    }
}

function Write-JsonNoBom {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)]$Object
    )
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $json = $Object | ConvertTo-Json -Depth 32
    $utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
    [System.IO.File]::WriteAllText($Path, ($json + [Environment]::NewLine), $utf8NoBom)
}

function Get-PropertyValue {
    param(
        $Object,
        [string[]]$Names
    )
    if ($null -eq $Object) {
        return $null
    }
    foreach ($name in $Names) {
        if ($Object.PSObject.Properties.Name -contains $name) {
            return $Object.$name
        }
    }
    return $null
}

function Convert-DateToUtcIso {
    param($Value)

    if ($null -eq $Value) {
        return $null
    }

    $text = ([string]$Value).Trim()
    if ([string]::IsNullOrWhiteSpace($text)) {
        return $null
    }

    try {
        $styles = [System.Globalization.DateTimeStyles]::AssumeUniversal -bor [System.Globalization.DateTimeStyles]::AdjustToUniversal
        $dto = [DateTimeOffset]::Parse($text, [System.Globalization.CultureInfo]::InvariantCulture, $styles)
        return $dto.ToUniversalTime().ToString("o")
    } catch {
        return $null
    }
}

function New-SafetyMap {
    return [ordered]@{
        read_only_observer_only = $true
        trading_authorized = $false
        broker_mutation_authorized = $false
        order_check_authorized = $false
        order_send_authorized = $false
        entry_authorized = $false
        close_modify_authorized = $false
        xauusd_order_authorized = $false
        usdjpy_order_authorized = $false
        trading_loop_authorized = $false
        automatic_execution_authorized = $false
        live_broker_request_constructed = $false
        executable_trade_request_constructed = $false
        mt5_request_dictionary_constructed = $false
        symbol_select_authorized = $false
        recovery_drill_authorizes_trading = $false
    }
}

function Read-EvidencePacket {
    param(
        [Parameter(Mandatory=$true)][string]$Name,
        [Parameter(Mandatory=$true)][string]$Path
    )

    $summary = [ordered]@{
        name = $Name
        path = $Path
        exists = $false
        parses = $false
        verdict = $null
        operator_state = $null
        generated_at_utc = $null
        age_minutes = $null
        violation_count = $null
    }

    if (-not (Test-Path $Path)) {
        Add-Violation "$($Name)_evidence_missing" "$Name evidence packet is missing: $Path"
        return $summary
    }

    $summary.exists = $true

    try {
        $packet = Get-Content -Raw -Path $Path | ConvertFrom-Json
        $summary.parses = $true
    } catch {
        Add-Violation "$($Name)_evidence_malformed" "$Name evidence packet is malformed JSON: $Path"
        return $summary
    }

    $verdict = Get-PropertyValue $packet @("verdict","record_verdict","VerifierVerdict")
    $operatorState = Get-PropertyValue $packet @("operator_state","operatorState")
    $violationsValue = Get-PropertyValue $packet @("violations","Violations")
    $timestamp = Get-PropertyValue $packet @(
        "generated_at_utc",
        "observed_at_utc",
        "created_at_utc",
        "evaluated_at_utc",
        "built_at_utc",
        "timestamp_utc",
        "timestamp"
    )

    $summary.verdict = if ($null -eq $verdict) { $null } else { [string]$verdict }
    $summary.operator_state = if ($null -eq $operatorState) { $null } else { [string]$operatorState }

    if ($null -eq $violationsValue) {
        $summary.violation_count = 0
    } else {
        $summary.violation_count = @($violationsValue).Count
    }

    if ([string]::IsNullOrWhiteSpace($summary.verdict) -or $summary.verdict -ne "PASS") {
        Add-Violation "$($Name)_evidence_not_pass" "$Name evidence verdict is not PASS."
    }

    if ($summary.violation_count -gt 0) {
        Add-Violation "$($Name)_evidence_contains_violations" "$Name evidence contains embedded violations."
    }

    $timestampUtc = Convert-DateToUtcIso $timestamp
    $summary.generated_at_utc = $timestampUtc

    if ([string]::IsNullOrWhiteSpace($timestampUtc)) {
        Add-Violation "$($Name)_evidence_timestamp_missing" "$Name evidence timestamp is missing or malformed."
    } else {
        try {
            $dto = [DateTimeOffset]::Parse($timestampUtc, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::AdjustToUniversal)
            $ageMinutes = ([DateTimeOffset]::UtcNow - $dto.ToUniversalTime()).TotalMinutes
            $summary.age_minutes = [Math]::Round($ageMinutes, 3)
            if ($ageMinutes -lt -1) {
                Add-Violation "$($Name)_evidence_timestamp_in_future" "$Name evidence timestamp is in the future."
            } elseif ($ageMinutes -gt $MaxEvidenceAgeMinutes) {
                Add-Violation "$($Name)_evidence_stale" "$Name evidence is stale: $([Math]::Round($ageMinutes, 3)) minute(s)."
            }
        } catch {
            Add-Violation "$($Name)_evidence_timestamp_malformed" "$Name evidence timestamp failed parsing after normalization."
        }
    }

    return $summary
}

$now = [DateTimeOffset]::UtcNow

$requiredScripts = @(
    [ordered]@{ name = "one_shot_observer"; path = Join-Path $Root "scripts\run_h024_read_only_vps_observer_once.ps1" },
    [ordered]@{ name = "scheduled_wrapper"; path = Join-Path $Root "scripts\run_h024_read_only_vps_observer_scheduled.ps1" },
    [ordered]@{ name = "healthcheck"; path = Join-Path $Root "scripts\check_h024_read_only_vps_observer_health.ps1" },
    [ordered]@{ name = "task_state_checker"; path = Join-Path $Root "scripts\check_h024_read_only_vps_observer_task_state.ps1" },
    [ordered]@{ name = "install_preview"; path = Join-Path $Root "scripts\install_h024_read_only_vps_observer_task.ps1" },
    [ordered]@{ name = "uninstall_preview"; path = Join-Path $Root "scripts\uninstall_h024_read_only_vps_observer_task.ps1" }
)

$scriptSummaries = @()
foreach ($script in $requiredScripts) {
    $exists = Test-Path $script.path
    if (-not $exists) {
        Add-Violation "required_recovery_script_missing" "Required recovery script is missing: $($script.path)"
    }
    $scriptSummaries += [ordered]@{
        name = $script.name
        path = $script.path
        exists = $exists
    }
}

$taskStateSummary = Read-EvidencePacket -Name "task_state" -Path $TaskStatePacketPath
$healthSummary = Read-EvidencePacket -Name "healthcheck" -Path $HealthPacketPath

$recoverySteps = @(
    [ordered]@{
        step = 1
        title = "Confirm repository state"
        command = "git status; git log --oneline -8"
        read_only = $true
        broker_mutation = $false
    },
    [ordered]@{
        step = 2
        title = "Refresh read-only observer once if evidence is stale"
        command = "powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_scheduled.ps1"
        read_only = $true
        broker_mutation = $false
    },
    [ordered]@{
        step = 3
        title = "Run observer healthcheck"
        command = "powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_health.ps1 -MaxAgeMinutes 60"
        read_only = $true
        broker_mutation = $false
    },
    [ordered]@{
        step = 4
        title = "Audit scheduled task state"
        command = "powershell -NoProfile -ExecutionPolicy Bypass -File scripts\check_h024_read_only_vps_observer_task_state.ps1 -ExpectedIntervalMinutes 5 -MaxLastRunAgeMinutes 15"
        read_only = $true
        broker_mutation = $false
    },
    [ordered]@{
        step = 5
        title = "Preview scheduler install command only if task is missing"
        command = "powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install_h024_read_only_vps_observer_task.ps1 -Preview"
        read_only = $true
        broker_mutation = $false
    },
    [ordered]@{
        step = 6
        title = "Escalate to operator review if task, health, or runtime evidence remains fail-closed"
        command = "No automatic remediation. Operator review required."
        read_only = $true
        broker_mutation = $false
    }
)

$passed = ($violations.Count -eq 0)

if ($passed) {
    $verdict = "PASS"
    $operatorState = "READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED"
    $operatorNextAction = "CONTINUE_READ_ONLY_VPS_OBSERVER_OPERATIONS_NO_TRADING_AUTHORIZED"
    $alertSeverity = "INFO"
    $alertState = "RECOVERY_DRILL_PREVIEW_OK_BUT_TRADING_NOT_AUTHORIZED"
    $operatorMessage = "Recovery drill evidence is coherent for read-only VPS observer operations only. Trading remains unauthorized."
    $exitCode = 0
} else {
    $verdict = "FAIL_CLOSED"
    $operatorState = "FAIL_CLOSED_READ_ONLY_VPS_RECOVERY_DRILL_PREVIEW_UNVERIFIED_NO_TRADING_AUTHORIZED"
    $operatorNextAction = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    $alertSeverity = "CRITICAL"
    $alertState = "RECOVERY_DRILL_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    $operatorMessage = "Recovery drill evidence is missing, stale, failing, malformed, or unverifiable. Operator review required. Trading remains unauthorized."
    $exitCode = 1
}

$alert = [ordered]@{
    generated_at_utc = $now.ToString("o")
    alert_surface = "local_json_text_console_only"
    alert_state = $alertState
    severity = $alertSeverity
    operator_message = $operatorMessage
    operator_next_action = $operatorNextAction
    external_notification_sent = $false
    external_mutation_performed = $false
    task_name = $TaskName
    violation_count = $violations.Count
    violations = $violations
    safety = New-SafetyMap
}

$packet = [ordered]@{
    generated_at_utc = $now.ToString("o")
    verdict = $verdict
    preview_only = $true
    operator_state = $operatorState
    operator_next_action = $operatorNextAction
    task_name = $TaskName
    max_evidence_age_minutes = $MaxEvidenceAgeMinutes
    evidence = [ordered]@{
        task_state = $taskStateSummary
        healthcheck = $healthSummary
    }
    required_scripts = $scriptSummaries
    recovery_drill_steps = $recoverySteps
    violations = $violations
    operator_alert_surface = $alert
    safety = New-SafetyMap
}

Write-JsonNoBom -Path $OutputPath -Object $packet
Write-JsonNoBom -Path $AlertJsonPath -Object $alert

$alertText = @(
    "H024 read-only VPS recovery drill operator alert"
    "Generated UTC: $($now.ToString("o"))"
    "Severity: $alertSeverity"
    "State: $alertState"
    "Task: $TaskName"
    "Message: $operatorMessage"
    "Next action: $operatorNextAction"
    "Preview only: true"
    "Trading authorized: false"
    "Broker mutation authorized: false"
    "External notification sent: false"
    "External mutation performed: false"
    "Violations: $($violations.Count)"
) -join [Environment]::NewLine

$utf8NoBom = New-Object System.Text.UTF8Encoding -ArgumentList $false
$alertDir = Split-Path -Parent $AlertTextPath
if (-not (Test-Path $alertDir)) {
    New-Item -ItemType Directory -Force -Path $alertDir | Out-Null
}
[System.IO.File]::WriteAllText($AlertTextPath, ($alertText + [Environment]::NewLine), $utf8NoBom)

Write-Host "H024 read-only VPS recovery drill preview verdict: $verdict"
Write-Host "Operator state: $operatorState"
Write-Host "Violations: $($violations.Count)"
Write-Host "Recovery drill packet: $OutputPath"
Write-Host "Operator alert JSON: $AlertJsonPath"
Write-Host "Operator alert text: $AlertTextPath"

exit $exitCode