[CmdletBinding()]
param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$TaskName = "H024 Read Only VPS Observer",
    [int]$ExpectedIntervalMinutes = 5,
    [int]$MinRunCount = 4,
    [int]$MinCadenceWindowMinutes = 15,
    [int]$MaxLatestRunAgeMinutes = 20,
    [int]$MaxPacketAgeMinutes = 60,
    [int]$MaxAllowedGapMinutes = 10,
    [int]$MinInterRunGapMinutes = 3,
    [string]$RuntimeDir = "reports/runtime/h024_read_only_vps_observer",
    [string]$OutputJson = "reports/h024_read_only_vps_observer_scheduled_cadence_summary.json",
    [string]$OutputText = "reports/h024_read_only_vps_observer_scheduled_cadence_summary.txt"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$UnsafeFlagNames = @(
    "broker_mutation_authorized",
    "order_check_authorized",
    "order_send_authorized",
    "entry_authorized",
    "close_modify_authorized",
    "xauusd_order_authorized",
    "usdjpy_order_authorized",
    "trading_loop_authorized",
    "automatic_execution_authorized",
    "live_broker_request_constructed",
    "executable_trade_request_constructed",
    "mt5_request_dictionary_constructed",
    "symbol_select_authorized",
    "vps_deployment_readiness_authorizes_trading",
    "black_swan_guard_authorizes_trading",
    "manual_approval_gate_preview_authorizes_action",
    "operator_decision_v2_preview_authorizes_action",
    "execution_readiness_dry_run_schema_preview_authorizes_execution",
    "scheduled_cadence_summary_authorizes_trading"
)

function Join-UnderRoot {
    param(
        [Parameter(Mandatory = $true)][string]$RelativeOrAbsolutePath
    )

    if ([System.IO.Path]::IsPathRooted($RelativeOrAbsolutePath)) {
        return [System.IO.Path]::GetFullPath($RelativeOrAbsolutePath)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $script:RootPath $RelativeOrAbsolutePath))
}

function New-Violation {
    param(
        [Parameter(Mandatory = $true)][string]$Code,
        [Parameter(Mandatory = $true)][string]$Severity,
        [Parameter(Mandatory = $true)][string]$Message
    )

    [pscustomobject]@{
        code = $Code
        severity = $Severity
        message = $Message
    }
}

function Read-JsonFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }

    try {
        return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    }
    catch {
        throw "Could not parse JSON file '$Path': $($_.Exception.Message)"
    }
}

function Get-ObjectProperty {
    param(
        [Parameter(Mandatory = $false)]$Object,
        [Parameter(Mandatory = $true)][string[]]$Names
    )

    if ($null -eq $Object) {
        return $null
    }

    foreach ($name in $Names) {
        $property = $Object.PSObject.Properties[$name]
        if ($null -ne $property) {
            return $property.Value
        }
    }

    return $null
}

function Convert-ToUtcDateTime {
    param(
        [Parameter(Mandatory = $false)]$Value
    )

    if ($null -eq $Value) {
        return $null
    }

    try {
        if ($Value -is [datetime]) {
            return $Value.ToUniversalTime()
        }

        $text = [string]$Value
        if ([string]::IsNullOrWhiteSpace($text)) {
            return $null
        }

        return [datetime]::Parse(
            $text,
            [System.Globalization.CultureInfo]::InvariantCulture,
            [System.Globalization.DateTimeStyles]::AssumeUniversal -bor [System.Globalization.DateTimeStyles]::AdjustToUniversal
        )
    }
    catch {
        return $null
    }
}

function Get-EvidenceTimestampUtc {
    param(
        [Parameter(Mandatory = $false)]$Object
    )

    $timestampValue = Get-ObjectProperty -Object $Object -Names @(
        "generated_at_utc",
        "checked_at_utc",
        "observed_at_utc",
        "created_at_utc",
        "built_at_utc",
        "completed_at_utc",
        "run_completed_at_utc",
        "latest_run_completed_at_utc",
        "latest_observed_run_at_utc"
    )

    return Convert-ToUtcDateTime -Value $timestampValue
}

function Convert-LogStampToUtcDateTime {
    param(
        [Parameter(Mandatory = $true)][string]$Stamp
    )

    if ($Stamp -notmatch "^(?<base>\d{8}T\d{6})(?<frac>\d{0,7})Z$") {
        return $null
    }

    try {
        $baseUtc = [datetime]::ParseExact(
            ($Matches["base"] + "Z"),
            "yyyyMMddTHHmmssZ",
            [System.Globalization.CultureInfo]::InvariantCulture,
            [System.Globalization.DateTimeStyles]::AssumeUniversal -bor [System.Globalization.DateTimeStyles]::AdjustToUniversal
        )

        $frac = $Matches["frac"]
        if (-not [string]::IsNullOrWhiteSpace($frac)) {
            if ($frac.Length -gt 7) {
                $frac = $frac.Substring(0, 7)
            }
            $ticksText = $frac.PadRight(7, "0")
            $ticks = [int64]::Parse($ticksText, [System.Globalization.CultureInfo]::InvariantCulture)
            return $baseUtc.AddTicks($ticks)
        }

        return $baseUtc
    }
    catch {
        return $null
    }
}

function Find-UnsafeTrueFlags {
    param(
        [Parameter(Mandatory = $false)]$Value,
        [string]$Prefix = ""
    )

    $found = @()

    if ($null -eq $Value) {
        return $found
    }

    if ($Value -is [System.Collections.IEnumerable] -and $Value -isnot [string] -and $Value -isnot [pscustomobject]) {
        $index = 0
        foreach ($item in $Value) {
            $found += Find-UnsafeTrueFlags -Value $item -Prefix "$Prefix[$index]"
            $index += 1
        }
        return $found
    }

    if ($Value -is [pscustomobject]) {
        foreach ($property in $Value.PSObject.Properties) {
            $name = $property.Name
            $childPath = if ([string]::IsNullOrWhiteSpace($Prefix)) { $name } else { "$Prefix.$name" }

            if (($script:UnsafeFlagNames -contains $name) -and ($property.Value -is [bool]) -and $property.Value) {
                $found += $childPath
            }

            $found += Find-UnsafeTrueFlags -Value $property.Value -Prefix $childPath
        }
    }

    return $found
}

function Get-LogRunObservations {
    param(
        [Parameter(Mandatory = $true)][string]$LogsDir
    )

    if (-not (Test-Path -LiteralPath $LogsDir)) {
        return @()
    }

    $observations = @()

    foreach ($file in Get-ChildItem -LiteralPath $LogsDir -Filter "*.log" -File) {
        if ($file.Name -match "(?<stamp>\d{8}T\d{6}\d{0,7}Z)") {
            $timestamp = Convert-LogStampToUtcDateTime -Stamp $Matches["stamp"]
            if ($null -ne $timestamp) {
                $observations += [pscustomobject]@{
                    path = $file.FullName
                    file_name = $file.Name
                    observed_run_at_utc = $timestamp
                }
            }
        }
    }

    return @($observations | Sort-Object observed_run_at_utc)
}

$RootPath = [System.IO.Path]::GetFullPath($Root)
$reportsDir = Join-UnderRoot -RelativeOrAbsolutePath "reports"
$outputJsonPath = Join-UnderRoot -RelativeOrAbsolutePath $OutputJson
$outputTextPath = Join-UnderRoot -RelativeOrAbsolutePath $OutputText
$runtimeRoot = Join-UnderRoot -RelativeOrAbsolutePath $RuntimeDir
$logsDir = Join-Path $runtimeRoot "logs"
$lastRunSummaryPath = Join-Path $runtimeRoot "last_run_summary.json"

New-Item -ItemType Directory -Force -Path ([System.IO.Path]::GetDirectoryName($outputJsonPath)) | Out-Null
New-Item -ItemType Directory -Force -Path ([System.IO.Path]::GetDirectoryName($outputTextPath)) | Out-Null

$nowUtc = (Get-Date).ToUniversalTime()
$violations = @()

$packetSpecs = @(
    @{ name = "healthcheck"; path = "reports/h024_read_only_vps_observer_healthcheck.json" },
    @{ name = "task_state"; path = "reports/h024_read_only_vps_observer_task_state.json" },
    @{ name = "recovery_drill"; path = "reports/h024_read_only_vps_recovery_drill_preview.json" },
    @{ name = "evidence_bundle"; path = "reports/h024_read_only_vps_observer_evidence_bundle.json" },
    @{ name = "continuity_summary"; path = "reports/h024_read_only_vps_observer_continuity_summary.json" }
)

$packetSummaries = @()

foreach ($spec in $packetSpecs) {
    $packetPath = Join-UnderRoot -RelativeOrAbsolutePath $spec.path
    $packet = Read-JsonFile -Path $packetPath

    if ($null -eq $packet) {
        $violations += New-Violation -Code "$($spec.name)_evidence_missing" -Severity "ERROR" -Message "$($spec.name) evidence packet is missing: $packetPath"
        $packetSummaries += [pscustomobject]@{
            name = $spec.name
            path = $packetPath
            verdict = $null
            timestamp_utc = $null
            age_minutes = $null
            unsafe_true_flags = @()
        }
        continue
    }

    $verdict = Get-ObjectProperty -Object $packet -Names @("verdict", "Verdict")
    if ($verdict -ne "PASS") {
        $violations += New-Violation -Code "$($spec.name)_evidence_verdict_not_pass" -Severity "ERROR" -Message "$($spec.name) evidence verdict is not PASS."
    }

    $timestampUtc = Get-EvidenceTimestampUtc -Object $packet
    $ageMinutes = $null

    if ($null -eq $timestampUtc) {
        $violations += New-Violation -Code "$($spec.name)_evidence_timestamp_missing" -Severity "ERROR" -Message "$($spec.name) evidence timestamp is missing or malformed."
    }
    else {
        $ageMinutes = ($nowUtc - $timestampUtc).TotalMinutes

        if ($ageMinutes -lt -5) {
            $violations += New-Violation -Code "$($spec.name)_evidence_timestamp_from_future" -Severity "ERROR" -Message "$($spec.name) evidence timestamp is more than five minutes in the future."
        }

        if ($ageMinutes -gt $MaxPacketAgeMinutes) {
            $violations += New-Violation -Code "$($spec.name)_evidence_stale" -Severity "ERROR" -Message "$($spec.name) evidence is stale."
        }
    }

    $unsafeFlags = @(Find-UnsafeTrueFlags -Value $packet)
    if ($unsafeFlags.Count -gt 0) {
        $violations += New-Violation -Code "$($spec.name)_unsafe_true_flag" -Severity "ERROR" -Message "$($spec.name) evidence contains unsafe true flag(s): $($unsafeFlags -join ', ')"
    }

    if ($spec.name -eq "task_state") {
        $observedTaskName = Get-ObjectProperty -Object $packet -Names @("task_name", "TaskName", "taskName", "expected_task_name")
        if ($null -ne $observedTaskName -and ([string]$observedTaskName) -ne $TaskName) {
            $violations += New-Violation -Code "task_state_name_mismatch" -Severity "ERROR" -Message "Task-state packet task name does not match expected task name."
        }

        $taskResult = Get-ObjectProperty -Object $packet -Names @("last_task_result", "LastTaskResult", "last_run_result", "last_result", "last_run_exit_code", "last_task_exit_code")
        if ($null -ne $taskResult) {
            try {
                if ([int]$taskResult -ne 0) {
                    $violations += New-Violation -Code "task_state_last_result_nonzero" -Severity "ERROR" -Message "Task-state packet reports a nonzero last result."
                }
            }
            catch {
                $violations += New-Violation -Code "task_state_last_result_malformed" -Severity "ERROR" -Message "Task-state packet last result is malformed."
            }
        }
    }

    $packetSummaries += [pscustomobject]@{
        name = $spec.name
        path = $packetPath
        verdict = $verdict
        timestamp_utc = if ($null -ne $timestampUtc) { $timestampUtc.ToString("o") } else { $null }
        age_minutes = if ($null -ne $ageMinutes) { [math]::Round($ageMinutes, 3) } else { $null }
        unsafe_true_flags = $unsafeFlags
    }
}

$lastRunSummary = Read-JsonFile -Path $lastRunSummaryPath
$lastRunStatus = $null
$lastRunExitCode = $null
$lastRunTimestampUtc = $null

if ($null -eq $lastRunSummary) {
    $violations += New-Violation -Code "last_run_summary_missing" -Severity "ERROR" -Message "Last-run summary is missing: $lastRunSummaryPath"
}
else {
    $lastRunStatus = Get-ObjectProperty -Object $lastRunSummary -Names @("status", "Status")
    if ($null -ne $lastRunStatus) {
        $allowedStatuses = @("COMPLETED", "PASS", "SUCCESS")
        if ($allowedStatuses -notcontains ([string]$lastRunStatus).ToUpperInvariant()) {
            $violations += New-Violation -Code "last_run_summary_status_not_completed" -Severity "ERROR" -Message "Last-run summary status is not completed."
        }
    }

    $exitValue = Get-ObjectProperty -Object $lastRunSummary -Names @("exit_code", "ExitCode", "observer_exit_code", "process_exit_code")
    if ($null -ne $exitValue) {
        try {
            $lastRunExitCode = [int]$exitValue
            if ($lastRunExitCode -ne 0) {
                $violations += New-Violation -Code "last_run_summary_exit_code_nonzero" -Severity "ERROR" -Message "Last-run summary exit code is nonzero."
            }
        }
        catch {
            $violations += New-Violation -Code "last_run_summary_exit_code_malformed" -Severity "ERROR" -Message "Last-run summary exit code is malformed."
        }
    }

    $lastRunTimestampUtc = Get-EvidenceTimestampUtc -Object $lastRunSummary
}

$logObservations = @(Get-LogRunObservations -LogsDir $logsDir)
$runTimes = @($logObservations | ForEach-Object { $_.observed_run_at_utc })

if ($runTimes.Count -lt $MinRunCount) {
    $violations += New-Violation -Code "scheduled_log_count_insufficient" -Severity "ERROR" -Message "Observed scheduled log count is below MinRunCount."
}

$firstRunUtc = $null
$latestRunUtc = $null
$spanMinutes = $null
$minGapMinutes = $null
$maxGapMinutes = $null
$gapMinutes = @()

if ($runTimes.Count -gt 0) {
    $firstRunUtc = $runTimes[0]
    $latestRunUtc = $runTimes[$runTimes.Count - 1]

    $latestAgeMinutes = ($nowUtc - $latestRunUtc).TotalMinutes
    if ($latestAgeMinutes -lt -5) {
        $violations += New-Violation -Code "scheduled_latest_run_from_future" -Severity "ERROR" -Message "Latest observed run timestamp is more than five minutes in the future."
    }

    if ($latestAgeMinutes -gt $MaxLatestRunAgeMinutes) {
        $violations += New-Violation -Code "scheduled_latest_run_stale" -Severity "ERROR" -Message "Latest observed scheduled run is stale."
    }

    if ($runTimes.Count -gt 1) {
        $spanMinutes = ($latestRunUtc - $firstRunUtc).TotalMinutes

        for ($index = 1; $index -lt $runTimes.Count; $index += 1) {
            $gapMinutes += ($runTimes[$index] - $runTimes[$index - 1]).TotalMinutes
        }

        if ($gapMinutes.Count -gt 0) {
            $minGapMinutes = ($gapMinutes | Measure-Object -Minimum).Minimum
            $maxGapMinutes = ($gapMinutes | Measure-Object -Maximum).Maximum
        }

        if ($spanMinutes -lt $MinCadenceWindowMinutes) {
            $violations += New-Violation -Code "scheduled_log_span_insufficient" -Severity "ERROR" -Message "Observed scheduled logs do not span the required cadence window."
        }

        if ($null -ne $maxGapMinutes -and $maxGapMinutes -gt $MaxAllowedGapMinutes) {
            $violations += New-Violation -Code "scheduled_log_gap_too_large" -Severity "ERROR" -Message "Observed scheduled logs contain a gap larger than MaxAllowedGapMinutes."
        }

        if ($null -ne $minGapMinutes -and $minGapMinutes -lt $MinInterRunGapMinutes) {
            $violations += New-Violation -Code "scheduled_log_clustered" -Severity "ERROR" -Message "Observed scheduled logs are too tightly clustered to prove scheduler cadence."
        }
    }
}

$verdict = if ($violations.Count -eq 0) { "PASS" } else { "FAIL_CLOSED" }

$packet = [pscustomobject]@{
    verdict = $verdict
    operator_state = if ($verdict -eq "PASS") { "READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED" } else { "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_SCHEDULED_CADENCE_SUMMARY_UNVERIFIED_NO_TRADING_AUTHORIZED" }
    operator_next_action = if ($verdict -eq "PASS") { "CONTINUE_LOCAL_WINDOWS_READ_ONLY_OBSERVER_CADENCE_MONITORING_NO_TRADING_AUTHORIZED" } else { "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED" }
    generated_at_utc = $nowUtc.ToString("o")
    task_name = $TaskName
    expected_interval_minutes = $ExpectedIntervalMinutes
    min_run_count = $MinRunCount
    min_cadence_window_minutes = $MinCadenceWindowMinutes
    max_latest_run_age_minutes = $MaxLatestRunAgeMinutes
    max_packet_age_minutes = $MaxPacketAgeMinutes
    max_allowed_gap_minutes = $MaxAllowedGapMinutes
    min_inter_run_gap_minutes = $MinInterRunGapMinutes
    runtime_dir = $runtimeRoot
    logs_dir = $logsDir
    last_run_summary_path = $lastRunSummaryPath
    last_run_summary_status = $lastRunStatus
    last_run_summary_exit_code = $lastRunExitCode
    last_run_summary_timestamp_utc = if ($null -ne $lastRunTimestampUtc) { $lastRunTimestampUtc.ToString("o") } else { $null }
    observed_run_count = $runTimes.Count
    first_observed_run_at_utc = if ($null -ne $firstRunUtc) { $firstRunUtc.ToString("o") } else { $null }
    latest_observed_run_at_utc = if ($null -ne $latestRunUtc) { $latestRunUtc.ToString("o") } else { $null }
    observed_span_minutes = if ($null -ne $spanMinutes) { [math]::Round($spanMinutes, 3) } else { $null }
    min_observed_gap_minutes = if ($null -ne $minGapMinutes) { [math]::Round($minGapMinutes, 3) } else { $null }
    max_observed_gap_minutes = if ($null -ne $maxGapMinutes) { [math]::Round($maxGapMinutes, 3) } else { $null }
    observed_logs = @($logObservations | ForEach-Object {
        [pscustomobject]@{
            file_name = $_.file_name
            path = $_.path
            observed_run_at_utc = $_.observed_run_at_utc.ToString("o")
        }
    })
    upstream_packets = $packetSummaries
    violations = $violations
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
    scheduled_cadence_summary_authorizes_trading = $false
}
[System.IO.File]::WriteAllText($outputJsonPath, (($packet | ConvertTo-Json -Depth 100) + [Environment]::NewLine), [System.Text.UTF8Encoding]::new($false))
$textLines = @(
    "H024 read-only VPS observer scheduled cadence summary verdict: $($packet.verdict)",
    "Operator state: $($packet.operator_state)",
    "Violations: $($violations.Count)",
    "Task name: $TaskName",
    "Observed run count: $($packet.observed_run_count)",
    "First observed run UTC: $($packet.first_observed_run_at_utc)",
    "Latest observed run UTC: $($packet.latest_observed_run_at_utc)",
    "Observed span minutes: $($packet.observed_span_minutes)",
    "Min observed gap minutes: $($packet.min_observed_gap_minutes)",
    "Max observed gap minutes: $($packet.max_observed_gap_minutes)",
    "Output JSON: $outputJsonPath",
    "Output text: $outputTextPath",
    "Trading authorized: False",
    "Broker mutation authorized: False",
    "order_check authorized: False",
    "order_send authorized: False",
    "symbol_select authorized: False"
)

if ($violations.Count -gt 0) {
    $textLines += ""
    $textLines += "Violations:"
    foreach ($violation in $violations) {
        $textLines += "- $($violation.code): $($violation.message)"
    }
}
[System.IO.File]::WriteAllText($outputTextPath, (($textLines -join [Environment]::NewLine) + [Environment]::NewLine), [System.Text.UTF8Encoding]::new($false))
Write-Host "H024 read-only VPS observer scheduled cadence summary verdict: $($packet.verdict)"
Write-Host "Operator state: $($packet.operator_state)"
Write-Host "Violations: $($violations.Count)"
Write-Host "Scheduled cadence JSON: $outputJsonPath"
Write-Host "Scheduled cadence text: $outputTextPath"

if ($packet.verdict -eq "PASS") {
    exit 0
}

exit 1
