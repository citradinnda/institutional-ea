[CmdletBinding()]
param(
    [string]$Root = (Resolve-Path ".").Path,
    [string]$TaskName = "H024 Read Only VPS Observer",
    [int]$ExpectedIntervalMinutes = 5,
    [int]$MinScheduledRunCount = 12,
    [double]$MinScheduledSpanMinutes = 55,
    [int]$MaxPacketAgeMinutes = 120,
    [int]$MaxLatestRunAgeMinutes = 30
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path $Root).Path
$ReportsDir = Join-Path $RepoRoot "reports"
$RuntimeDir = Join-Path $ReportsDir "runtime\h024_read_only_vps_observer"
$LastRunSummaryPath = Join-Path $RuntimeDir "last_run_summary.json"
$OutputJsonPath = Join-Path $ReportsDir "h024_free_local_read_only_demo_deployment_readiness.json"
$OutputTextPath = Join-Path $ReportsDir "h024_free_local_read_only_demo_deployment_readiness.txt"
$ExpectedLauncherPath = Join-Path $RepoRoot "scripts\run_h024_read_only_vps_observer_scheduled_hidden.vbs"

New-Item -ItemType Directory -Force -Path $ReportsDir | Out-Null

$GeneratedAt = [DateTime]::UtcNow
$Violations = @()

function Add-Violation {
    param(
        [Parameter(Mandatory = $true)][string]$Code,
        [Parameter(Mandatory = $true)][string]$Message,
        [string]$Severity = "ERROR"
    )

    $script:Violations += [pscustomobject]@{
        code = $Code
        severity = $Severity
        message = $Message
    }
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )
    $Directory = Split-Path -Parent $Path
    if ($Directory -and -not (Test-Path $Directory)) {
        New-Item -ItemType Directory -Force -Path $Directory | Out-Null
    }
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Get-Prop {
    param(
        [object]$Object,
        [string]$Name
    )

    if ($null -eq $Object) {
        return $null
    }

    $Property = $Object.PSObject.Properties[$Name]
    if ($null -eq $Property) {
        return $null
    }

    return $Property.Value
}

function Convert-ToUtcDate {
    param([object]$Value)

    if ($null -eq $Value) {
        return $null
    }

    try {
        $Styles = [System.Globalization.DateTimeStyles]::AssumeUniversal -bor [System.Globalization.DateTimeStyles]::AdjustToUniversal
        return ([DateTime]::Parse($Value.ToString(), [System.Globalization.CultureInfo]::InvariantCulture, $Styles)).ToUniversalTime()
    } catch {
        return $null
    }
}

function Get-PacketTimestamp {
    param([object]$Packet)

    foreach ($Field in @("generated_at_utc", "checked_at_utc", "timestamp_utc", "completed_at_utc", "latest_observed_run_at_utc", "last_run_summary_timestamp_utc")) {
        $Timestamp = Convert-ToUtcDate -Value (Get-Prop -Object $Packet -Name $Field)
        if ($null -ne $Timestamp) {
            return $Timestamp
        }
    }

    return $null
}

function Test-UnsafeFlagName {
    param([string]$Name)

    if ([string]::IsNullOrWhiteSpace($Name)) {
        return $false
    }

    $Lower = $Name.ToLowerInvariant()

    if ($Lower.EndsWith("_authorized")) {
        return $true
    }

    if ($Lower.EndsWith("_constructed")) {
        return $true
    }

    if ($Lower -eq "trading_authorized") {
        return $true
    }

    if ($Lower -eq "live_execution_authorized") {
        return $true
    }

    if ($Lower -match "authorizes.*trading") {
        return $true
    }

    if ($Lower -match "authorizes.*execution") {
        return $true
    }

    return $false
}

function Find-UnsafeTrueFlags {
    param(
        [object]$Value,
        [string]$Path = ""
    )

    $Findings = @()

    if ($null -eq $Value) {
        return @()
    }

    if ($Value -is [pscustomobject]) {
        foreach ($Property in $Value.PSObject.Properties) {
            $ChildPath = if ($Path) { "$Path.$($Property.Name)" } else { $Property.Name }

            if (($Property.Value -is [bool]) -and $Property.Value -and (Test-UnsafeFlagName -Name $Property.Name)) {
                $Findings += $ChildPath
            }

            $Findings += @(Find-UnsafeTrueFlags -Value $Property.Value -Path $ChildPath)
        }

        return @($Findings)
    }

    if (($Value -is [System.Collections.IEnumerable]) -and -not ($Value -is [string])) {
        $Index = 0
        foreach ($Item in $Value) {
            $Findings += @(Find-UnsafeTrueFlags -Value $Item -Path "$Path[$Index]")
            $Index += 1
        }

        return @($Findings)
    }

    return @($Findings)
}

function Read-JsonFile {
    param(
        [string]$Path,
        [string]$Name,
        [string]$MissingCode = "packet_missing",
        [string]$MalformedCode = "packet_malformed_json"
    )

    if (-not (Test-Path $Path)) {
        Add-Violation -Code $MissingCode -Message "$Name JSON file is missing: $Path"
        return $null
    }

    try {
        return Get-Content -Raw -Path $Path | ConvertFrom-Json
    } catch {
        Add-Violation -Code $MalformedCode -Message "$Name JSON file is malformed or unreadable: $Path"
        return $null
    }
}

function Convert-RepetitionIntervalMinutes {
    param([object]$Interval)

    if ($null -eq $Interval) {
        return $null
    }

    if ($Interval -is [TimeSpan]) {
        return [double]$Interval.TotalMinutes
    }

    $Text = $Interval.ToString()

    try {
        $Parsed = [TimeSpan]::Parse($Text, [System.Globalization.CultureInfo]::InvariantCulture)
        return [double]$Parsed.TotalMinutes
    } catch {
        # Continue to ISO-8601 parsing.
    }

    if ($Text -match "^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$") {
        $Hours = if ($Matches[1]) { [double]$Matches[1] } else { 0 }
        $Minutes = if ($Matches[2]) { [double]$Matches[2] } else { 0 }
        $Seconds = if ($Matches[3]) { [double]$Matches[3] } else { 0 }
        return ($Hours * 60) + $Minutes + ($Seconds / 60)
    }

    return $null
}

$ScheduledTaskInfo = [pscustomobject]@{
    task_name = $TaskName
    expected_execute = "wscript.exe"
    observed_execute = $null
    expected_argument = $ExpectedLauncherPath
    observed_argument = $null
    expected_interval_minutes = $ExpectedIntervalMinutes
    observed_triggers = @()
    action_ok = $false
    interval_ok = $false
}

try {
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction Stop
    $Action = @($Task.Actions)[0]

    if ($null -eq $Action) {
        Add-Violation -Code "scheduled_task_action_missing" -Message "Scheduled task action is missing."
    } else {
        $ScheduledTaskInfo.observed_execute = $Action.Execute
        $ScheduledTaskInfo.observed_argument = $Action.Arguments

        $ObservedArgumentNormalized = $Action.Arguments
        try {
            if (-not [string]::IsNullOrWhiteSpace($Action.Arguments)) {
                $ObservedArgumentNormalized = [System.IO.Path]::GetFullPath($Action.Arguments.Trim('"'))
            }
        } catch {
            $ObservedArgumentNormalized = $Action.Arguments
        }

        $ExpectedArgumentNormalized = [System.IO.Path]::GetFullPath($ExpectedLauncherPath)

        if ($Action.Execute -ne "wscript.exe") {
            Add-Violation -Code "scheduled_task_execute_not_wscript" -Message "Scheduled task Execute must be wscript.exe."
        }

        if ($ObservedArgumentNormalized -ne $ExpectedArgumentNormalized) {
            Add-Violation -Code "scheduled_task_argument_mismatch" -Message "Scheduled task argument must be the hidden VBS launcher."
        }

        if (($Action.Execute -eq "wscript.exe") -and ($ObservedArgumentNormalized -eq $ExpectedArgumentNormalized)) {
            $ScheduledTaskInfo.action_ok = $true
        }
    }

    $TriggerInfos = @()
    $IntervalMatches = $false

    foreach ($Trigger in @($Task.Triggers)) {
        $RawInterval = $null
        $IntervalMinutes = $null

        if ($null -ne $Trigger.Repetition) {
            $RawInterval = $Trigger.Repetition.Interval
            $IntervalMinutes = Convert-RepetitionIntervalMinutes -Interval $RawInterval
        }

        if (($null -ne $IntervalMinutes) -and ([Math]::Abs([double]$IntervalMinutes - [double]$ExpectedIntervalMinutes) -lt 0.001)) {
            $IntervalMatches = $true
        }

        $TriggerInfos += [pscustomobject]@{
            enabled = Get-Prop -Object $Trigger -Name "Enabled"
            raw_interval = if ($null -eq $RawInterval) { $null } else { $RawInterval.ToString() }
            interval_minutes = $IntervalMinutes
            start_boundary = Get-Prop -Object $Trigger -Name "StartBoundary"
        }
    }

    $ScheduledTaskInfo.observed_triggers = @($TriggerInfos)
    $ScheduledTaskInfo.interval_ok = $IntervalMatches

    if (-not $IntervalMatches) {
        Add-Violation -Code "scheduled_task_interval_unverified" -Message "Scheduled task does not expose a verified 5-minute repetition interval."
    }
} catch {
    Add-Violation -Code "scheduled_task_missing_or_unreadable" -Message "Scheduled task is missing or unreadable: $TaskName"
}

$RequiredPackets = @(
    @{ Name = "healthcheck"; Path = Join-Path $ReportsDir "h024_read_only_vps_observer_healthcheck.json" },
    @{ Name = "task_state"; Path = Join-Path $ReportsDir "h024_read_only_vps_observer_task_state.json" },
    @{ Name = "recovery_drill_preview"; Path = Join-Path $ReportsDir "h024_read_only_vps_recovery_drill_preview.json" },
    @{ Name = "evidence_bundle"; Path = Join-Path $ReportsDir "h024_read_only_vps_observer_evidence_bundle.json" },
    @{ Name = "continuity_summary"; Path = Join-Path $ReportsDir "h024_read_only_vps_observer_continuity_summary.json" },
    @{ Name = "scheduled_cadence_summary"; Path = Join-Path $ReportsDir "h024_read_only_vps_observer_scheduled_cadence_summary.json" }
)

$PacketSummaries = @()

foreach ($PacketSpec in $RequiredPackets) {
    $Packet = Read-JsonFile -Path $PacketSpec.Path -Name $PacketSpec.Name
    if ($null -eq $Packet) {
        continue
    }

    $Verdict = Get-Prop -Object $Packet -Name "verdict"
    $Timestamp = Get-PacketTimestamp -Packet $Packet
    $AgeMinutes = $null

    if ($null -eq $Timestamp) {
        Add-Violation -Code "packet_timestamp_missing" -Message "$($PacketSpec.Name) does not expose a recognized UTC timestamp."
    } else {
        $AgeMinutes = [Math]::Round((New-TimeSpan -Start $Timestamp -End $GeneratedAt).TotalMinutes, 3)
        if ($AgeMinutes -gt $MaxPacketAgeMinutes) {
            Add-Violation -Code "packet_stale" -Message "$($PacketSpec.Name) is stale: $AgeMinutes minutes old."
        }
    }

    if ($Verdict -ne "PASS") {
        Add-Violation -Code "packet_not_pass" -Message "$($PacketSpec.Name) verdict is not PASS."
    }

    $UnsafeTrueFlags = @(Find-UnsafeTrueFlags -Value $Packet -Path $PacketSpec.Name)
    if ($UnsafeTrueFlags.Count -gt 0) {
        Add-Violation -Code "packet_unsafe_true_flags" -Message "$($PacketSpec.Name) has unsafe true flags: $($UnsafeTrueFlags -join ', ')"
    }

    if ($PacketSpec.Name -eq "scheduled_cadence_summary") {
        $ObservedRunCount = Get-Prop -Object $Packet -Name "observed_run_count"
        $ObservedSpanMinutes = Get-Prop -Object $Packet -Name "observed_span_minutes"
        $LatestObservedRunAt = Convert-ToUtcDate -Value (Get-Prop -Object $Packet -Name "latest_observed_run_at_utc")

        if (($null -eq $ObservedRunCount) -or ([int]$ObservedRunCount -lt $MinScheduledRunCount)) {
            Add-Violation -Code "scheduled_cadence_run_count_insufficient" -Message "Scheduled cadence proof must show at least $MinScheduledRunCount natural scheduled runs."
        }

        if (($null -eq $ObservedSpanMinutes) -or ([double]$ObservedSpanMinutes -lt $MinScheduledSpanMinutes)) {
            Add-Violation -Code "scheduled_cadence_span_insufficient" -Message "Scheduled cadence proof must span at least $MinScheduledSpanMinutes minutes."
        }

        if ($null -eq $LatestObservedRunAt) {
            Add-Violation -Code "scheduled_cadence_latest_run_timestamp_missing" -Message "Scheduled cadence proof latest run timestamp is missing."
        } else {
            $LatestRunAgeMinutes = [Math]::Round((New-TimeSpan -Start $LatestObservedRunAt -End $GeneratedAt).TotalMinutes, 3)
            if ($LatestRunAgeMinutes -gt $MaxLatestRunAgeMinutes) {
                Add-Violation -Code "scheduled_cadence_latest_run_stale" -Message "Scheduled cadence latest observed run is stale: $LatestRunAgeMinutes minutes old."
            }
        }
    }

    $PacketSummaries += [pscustomobject]@{
        name = $PacketSpec.Name
        path = $PacketSpec.Path
        verdict = $Verdict
        timestamp_utc = if ($null -eq $Timestamp) { $null } else { $Timestamp.ToString("o") }
        age_minutes = $AgeMinutes
        unsafe_true_flags = @($UnsafeTrueFlags)
    }
}

$LastRunSummary = Read-JsonFile `
    -Path $LastRunSummaryPath `
    -Name "last_run_summary" `
    -MissingCode "last_run_summary_missing" `
    -MalformedCode "last_run_summary_malformed_json"

$LastRunInfo = [pscustomobject]@{
    path = $LastRunSummaryPath
    status = $null
    exit_code = $null
    completed_at_utc = $null
    age_minutes = $null
    read_only_observer_only = $null
    trading_authorized = $null
    broker_mutation_authorized = $null
    live_execution_authorized = $null
    unsafe_true_flags = @()
}

if ($null -ne $LastRunSummary) {
    $LastRunInfo.status = Get-Prop -Object $LastRunSummary -Name "status"
    $LastRunInfo.exit_code = Get-Prop -Object $LastRunSummary -Name "exit_code"
    $LastRunInfo.completed_at_utc = Get-Prop -Object $LastRunSummary -Name "completed_at_utc"
    $LastRunInfo.read_only_observer_only = Get-Prop -Object $LastRunSummary -Name "read_only_observer_only"
    $LastRunInfo.trading_authorized = Get-Prop -Object $LastRunSummary -Name "trading_authorized"
    $LastRunInfo.broker_mutation_authorized = Get-Prop -Object $LastRunSummary -Name "broker_mutation_authorized"
    $LastRunInfo.live_execution_authorized = Get-Prop -Object $LastRunSummary -Name "live_execution_authorized"

    if ($LastRunInfo.status -ne "COMPLETED") {
        Add-Violation -Code "last_run_not_completed" -Message "Latest scheduled wrapper last_run_summary status is not COMPLETED."
    }

    if ([int]$LastRunInfo.exit_code -ne 0) {
        Add-Violation -Code "last_run_exit_nonzero" -Message "Latest scheduled wrapper last_run_summary exit_code is nonzero."
    }

    if ($LastRunInfo.read_only_observer_only -ne $true) {
        Add-Violation -Code "last_run_not_marked_read_only" -Message "Latest scheduled wrapper last_run_summary is not marked read_only_observer_only=true."
    }

    $LastRunTimestamp = Convert-ToUtcDate -Value $LastRunInfo.completed_at_utc
    if ($null -eq $LastRunTimestamp) {
        Add-Violation -Code "last_run_timestamp_missing" -Message "Latest scheduled wrapper completed_at_utc timestamp is missing."
    } else {
        $LastRunInfo.age_minutes = [Math]::Round((New-TimeSpan -Start $LastRunTimestamp -End $GeneratedAt).TotalMinutes, 3)
        if ($LastRunInfo.age_minutes -gt $MaxLatestRunAgeMinutes) {
            Add-Violation -Code "last_run_stale" -Message "Latest scheduled wrapper completion is stale: $($LastRunInfo.age_minutes) minutes old."
        }
    }

    $LastRunUnsafeTrueFlags = @(Find-UnsafeTrueFlags -Value $LastRunSummary -Path "last_run_summary")
    $LastRunInfo.unsafe_true_flags = @($LastRunUnsafeTrueFlags)

    if ($LastRunUnsafeTrueFlags.Count -gt 0) {
        Add-Violation -Code "last_run_unsafe_true_flags" -Message "Latest scheduled wrapper last_run_summary has unsafe true flags: $($LastRunUnsafeTrueFlags -join ', ')"
    }
}

$TrackedReports = @()
try {
    $TrackedReports = @(git -C $RepoRoot ls-files -- reports 2>$null)
} catch {
    $TrackedReports = @()
}

if ($TrackedReports.Count -gt 0) {
    Add-Violation -Code "reports_tracked_in_git" -Message "reports/ contains tracked files and must remain generated runtime evidence only."
}

$VerdictFinal = if (@($Violations).Count -eq 0) { "PASS" } else { "FAIL_CLOSED" }
$OperatorState = if ($VerdictFinal -eq "PASS") {
    "FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED"
} else {
    "FAIL_CLOSED_FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_UNVERIFIED_NO_TRADING_AUTHORIZED"
}
$OperatorNextAction = if ($VerdictFinal -eq "PASS") {
    "DEMO_LOCAL_READ_ONLY_OBSERVER_STATUS_ONLY_NO_TRADING_AUTHORIZED"
} else {
    "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
}

$Output = [pscustomobject]@{
    schema_version = 1
    strategy = "H024"
    component = "free_local_read_only_demo_deployment_readiness"
    verdict = $VerdictFinal
    operator_state = $OperatorState
    operator_next_action = $OperatorNextAction
    generated_at_utc = $GeneratedAt.ToString("o")

    free_local_windows_only = $true
    oracle_vps_required = $false
    paid_vps_required = $false
    read_only_demo_ready = ($VerdictFinal -eq "PASS")
    read_only_demo_deployment_readiness_authorizes_trading = $false

    expected_task_name = $TaskName
    scheduled_task = $ScheduledTaskInfo

    expected_interval_minutes = $ExpectedIntervalMinutes
    min_scheduled_run_count = $MinScheduledRunCount
    min_scheduled_span_minutes = $MinScheduledSpanMinutes
    max_packet_age_minutes = $MaxPacketAgeMinutes
    max_latest_run_age_minutes = $MaxLatestRunAgeMinutes

    upstream_packets = @($PacketSummaries)
    latest_run_summary = $LastRunInfo

    reports_dir = $ReportsDir
    reports_tracked_in_git = @($TrackedReports)

    effective_new_entries_blocked = $true
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

    violations = @($Violations)
}

$Json = $Output | ConvertTo-Json -Depth 80
Write-Utf8NoBom -Path $OutputJsonPath -Content $Json

$TextLines = @(
    "H024 Free Local Read-Only Demo Deployment Readiness",
    "Verdict: $VerdictFinal",
    "Operator state: $OperatorState",
    "Operator next action: $OperatorNextAction",
    "Read-only demo ready: $($Output.read_only_demo_ready)",
    "Trading authorized: False",
    "Broker mutation authorized: False",
    "Order-capable execution authorized: False",
    "Local Windows only: True",
    "Oracle VPS required: False",
    "Paid VPS required: False",
    "Reports tracked in git: $($TrackedReports.Count)",
    "Violations: $(@($Violations).Count)",
    "",
    "Meaning:",
    "PASS means the free local Windows no-console read-only observer is demo-ready for status observation only.",
    "PASS does not authorize trading, broker mutation, request construction, entries, close/modify, or order-capable loops.",
    ""
)

if (@($Violations).Count -gt 0) {
    $TextLines += "Violations:"
    foreach ($Violation in @($Violations)) {
        $TextLines += "- [$($Violation.severity)] $($Violation.code): $($Violation.message)"
    }
}

Write-Utf8NoBom -Path $OutputTextPath -Content ($TextLines -join [Environment]::NewLine)

Write-Host "H024 free local read-only demo deployment readiness verdict: $VerdictFinal"
Write-Host "Operator state: $OperatorState"
Write-Host "Violations: $(@($Violations).Count)"
Write-Host "Read-only demo ready: $($Output.read_only_demo_ready)"
Write-Host "Trading authorized: False"
Write-Host "Broker mutation authorized: False"
Write-Host "Output JSON: $OutputJsonPath"
Write-Host "Output text: $OutputTextPath"

if (@($Violations).Count -gt 0) {
    foreach ($Violation in @($Violations)) {
        Write-Host "Violation [$($Violation.severity)] $($Violation.code): $($Violation.message)"
    }
    exit 1
}

exit 0