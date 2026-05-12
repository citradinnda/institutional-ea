[CmdletBinding()]
param(
    [string]$Root = ".",
    [int]$MinRunCount = 2,
    [int]$MaxPacketAgeMinutes = 60,
    [int]$MaxLatestRunAgeMinutes = 60,
    [int]$LogTailLines = 60,
    [string]$OutputJson = "",
    [string]$OutputText = ""
)

$ErrorActionPreference = "Stop"

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$reportsRoot = Join-Path $resolvedRoot "reports"
$runtimeRoot = Join-Path $reportsRoot "runtime\h024_read_only_vps_observer"
$logsRoot = Join-Path $runtimeRoot "logs"
$lastRunSummaryPath = Join-Path $runtimeRoot "last_run_summary.json"

if ([string]::IsNullOrWhiteSpace($OutputJson)) {
    $OutputJson = Join-Path $reportsRoot "h024_read_only_vps_observer_continuity_summary.json"
}
if ([string]::IsNullOrWhiteSpace($OutputText)) {
    $OutputText = Join-Path $reportsRoot "h024_read_only_vps_observer_continuity_summary.txt"
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputJson) | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputText) | Out-Null

$now = [DateTimeOffset]::UtcNow
$script:Violations = New-Object System.Collections.ArrayList

function Add-Violation {
    param(
        [string]$Code,
        [string]$Message
    )
    [void]$script:Violations.Add([ordered]@{
        code = $Code
        severity = "ERROR"
        message = $Message
    })
}

function Get-RelativePath {
    param([string]$Path)
    try {
        $rootWithSlash = $resolvedRoot.TrimEnd("\") + "\"
        if ($Path.StartsWith($rootWithSlash, [System.StringComparison]::OrdinalIgnoreCase)) {
            return $Path.Substring($rootWithSlash.Length)
        }
        return $Path
    } catch {
        return $Path
    }
}

function Read-JsonFile {
    param(
        [string]$Path,
        [string]$Component
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        Add-Violation "${Component}_missing" "$Component evidence is missing at $Path."
        return $null
    }

    try {
        return Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    } catch {
        Add-Violation "${Component}_malformed_json" "$Component evidence is not valid JSON: $($_.Exception.Message)"
        return $null
    }
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
        $prop = $Object.PSObject.Properties[$name]
        if ($null -ne $prop) {
            return $prop.Value
        }
    }

    return $null
}

function Convert-ToTimestamp {
    param($Value)

    if ($null -eq $Value) {
        return $null
    }

    $text = [string]$Value
    if ([string]::IsNullOrWhiteSpace($text)) {
        return $null
    }

    $parsed = [DateTimeOffset]::MinValue
    $styles = [System.Globalization.DateTimeStyles]::AssumeUniversal -bor [System.Globalization.DateTimeStyles]::AdjustToUniversal

    if ([DateTimeOffset]::TryParse($text, [System.Globalization.CultureInfo]::InvariantCulture, $styles, [ref]$parsed)) {
        return $parsed.ToUniversalTime()
    }

    return $null
}

function Test-UnsafeTrueKey {
    param([string]$Name)

    $n = $Name.ToLowerInvariant()

    if ($n -eq "read_only_observer_workflow_authorized_for_operator_review") {
        return $false
    }

    $patterns = @(
        "trading_authorized$",
        "authorizes_trading$",
        "broker_mutation_authorized$",
        "live_execution_authorized$",
        "automatic_execution_authorized$",
        "entry_authorized$",
        "close_modify_authorized$",
        "_check_authorized$",
        "_send_authorized$",
        "xauusd_.*authorized$",
        "usdjpy_.*authorized$",
        "trading_loop_authorized$",
        "request.*constructed$",
        "dictionary.*constructed$",
        "select_authorized$"
    )

    foreach ($pattern in $patterns) {
        if ($n -match $pattern) {
            return $true
        }
    }

    return $false
}

function Find-UnsafeTrueFlags {
    param(
        $Value,
        [string]$Path = ""
    )

    $found = New-Object System.Collections.ArrayList

    if ($null -eq $Value) {
        return $found
    }

    if ($Value -is [System.Array]) {
        for ($i = 0; $i -lt $Value.Count; $i++) {
            $childPath = "$Path[$i]"
            $childFound = Find-UnsafeTrueFlags -Value $Value[$i] -Path $childPath
            foreach ($item in $childFound) {
                [void]$found.Add($item)
            }
        }
        return $found
    }

    if ($Value -is [System.Management.Automation.PSCustomObject]) {
        foreach ($prop in $Value.PSObject.Properties) {
            $childPath = $prop.Name
            if (-not [string]::IsNullOrWhiteSpace($Path)) {
                $childPath = "$Path.$($prop.Name)"
            }

            if (($prop.Value -is [bool]) -and ($prop.Value -eq $true) -and (Test-UnsafeTrueKey -Name $prop.Name)) {
                [void]$found.Add($childPath)
            }

            $childFound = Find-UnsafeTrueFlags -Value $prop.Value -Path $childPath
            foreach ($item in $childFound) {
                [void]$found.Add($item)
            }
        }
    }

    return $found
}

function Read-PacketEvidence {
    param(
        [string]$Component,
        [string]$Path
    )

    $packet = Read-JsonFile -Path $Path -Component $Component
    $timestampAliases = @(
        "generated_at_utc",
        "checked_at_utc",
        "created_at_utc",
        "completed_at_utc",
        "timestamp_utc",
        "run_completed_at_utc"
    )

    $info = [ordered]@{
        component = $Component
        path = Get-RelativePath -Path $Path
        present = $false
        verdict = $null
        timestamp_utc = $null
        age_seconds = $null
        unsafe_true_flags = @()
    }

    if ($null -eq $packet) {
        return $info
    }

    $info.present = $true

    $verdict = Get-PropertyValue -Object $packet -Names @("verdict")
    $info.verdict = $verdict
    if ($verdict -ne "PASS") {
        Add-Violation "${Component}_packet_verdict_not_pass" "$Component packet verdict is not PASS: $verdict."
    }

    $timestampRaw = Get-PropertyValue -Object $packet -Names $timestampAliases
    $timestamp = Convert-ToTimestamp -Value $timestampRaw

    if ($null -eq $timestamp) {
        Add-Violation "${Component}_packet_timestamp_missing" "$Component packet evidence is not fresh: missing or malformed timestamp."
    } else {
        $age = $now - $timestamp
        $info.timestamp_utc = $timestamp.ToString("o")
        $info.age_seconds = [Math]::Round($age.TotalSeconds, 3)

        if ($age.TotalMinutes -gt $MaxPacketAgeMinutes) {
            Add-Violation "${Component}_packet_stale" "$Component packet evidence is stale: age minutes $([Math]::Round($age.TotalMinutes, 3)) exceeds max $MaxPacketAgeMinutes."
        }

        if ($age.TotalMinutes -lt -5) {
            Add-Violation "${Component}_packet_future_timestamp" "$Component packet timestamp is more than five minutes in the future."
        }
    }

    $unsafeFlags = Find-UnsafeTrueFlags -Value $packet -Path $Component
    $info.unsafe_true_flags = @($unsafeFlags)
    foreach ($flag in $unsafeFlags) {
        Add-Violation "${Component}_unsafe_true_flag" "$Component packet contains unsafe true flag: $flag."
    }

    return $info
}

$packetSpecs = @(
    @{ Component = "healthcheck"; Path = (Join-Path $reportsRoot "h024_read_only_vps_observer_healthcheck.json") },
    @{ Component = "task_state"; Path = (Join-Path $reportsRoot "h024_read_only_vps_observer_task_state.json") },
    @{ Component = "recovery_drill_preview"; Path = (Join-Path $reportsRoot "h024_read_only_vps_recovery_drill_preview.json") },
    @{ Component = "evidence_bundle"; Path = (Join-Path $reportsRoot "h024_read_only_vps_observer_evidence_bundle.json") }
)

$upstreamPackets = @()
foreach ($spec in $packetSpecs) {
    $upstreamPackets += Read-PacketEvidence -Component $spec.Component -Path $spec.Path
}

$lastRunSummary = $null
$lastRunSummaryInfo = [ordered]@{
    path = Get-RelativePath -Path $lastRunSummaryPath
    present = $false
    status = $null
    exit_code = $null
    timestamp_utc = $null
    age_seconds = $null
}

if (-not (Test-Path -LiteralPath $lastRunSummaryPath)) {
    Add-Violation "last_run_summary_missing" "Scheduled wrapper last-run summary is missing at $lastRunSummaryPath."
} else {
    $lastRunSummary = Read-JsonFile -Path $lastRunSummaryPath -Component "last_run_summary"
    if ($null -ne $lastRunSummary) {
        $lastRunSummaryInfo.present = $true

        $status = Get-PropertyValue -Object $lastRunSummary -Names @("status", "run_status", "wrapper_status")
        if ($null -ne $status) {
            $lastRunSummaryInfo.status = [string]$status
            $statusUpper = ([string]$status).ToUpperInvariant()
            if (@("COMPLETED", "PASS", "OK", "SUCCESS") -notcontains $statusUpper) {
                Add-Violation "last_run_summary_status_not_completed" "Scheduled wrapper last-run summary status is not completed/success: $status."
            }
        }

        $exitCode = Get-PropertyValue -Object $lastRunSummary -Names @("exit_code", "exitCode", "observer_exit_code", "process_exit_code")
        if ($null -ne $exitCode) {
            $lastRunSummaryInfo.exit_code = $exitCode
            try {
                if ([int]$exitCode -ne 0) {
                    Add-Violation "last_run_summary_exit_code_nonzero" "Scheduled wrapper last-run summary exit code is nonzero: $exitCode."
                }
            } catch {
                Add-Violation "last_run_summary_exit_code_malformed" "Scheduled wrapper last-run summary exit code is malformed: $exitCode."
            }
        }

        $summaryTimestampRaw = Get-PropertyValue -Object $lastRunSummary -Names @(
            "generated_at_utc",
            "checked_at_utc",
            "completed_at_utc",
            "finished_at_utc",
            "run_completed_at_utc",
            "timestamp_utc"
        )
        $summaryTimestamp = Convert-ToTimestamp -Value $summaryTimestampRaw
        if ($null -ne $summaryTimestamp) {
            $summaryAge = $now - $summaryTimestamp
            $lastRunSummaryInfo.timestamp_utc = $summaryTimestamp.ToString("o")
            $lastRunSummaryInfo.age_seconds = [Math]::Round($summaryAge.TotalSeconds, 3)
            if ($summaryAge.TotalMinutes -gt $MaxLatestRunAgeMinutes) {
                Add-Violation "last_run_summary_stale" "Scheduled wrapper last-run summary is stale: age minutes $([Math]::Round($summaryAge.TotalMinutes, 3)) exceeds max $MaxLatestRunAgeMinutes."
            }
        }
    }
}

$runLogs = @()
$completedLogCount = 0

if (-not (Test-Path -LiteralPath $logsRoot)) {
    Add-Violation "runtime_logs_directory_missing" "Scheduled wrapper runtime logs directory is missing at $logsRoot."
} else {
    $logs = @(Get-ChildItem -LiteralPath $logsRoot -Filter "*.log" -File | Sort-Object LastWriteTimeUtc -Descending)

    if ($logs.Count -lt $MinRunCount) {
        Add-Violation "insufficient_runtime_logs" "Only $($logs.Count) runtime logs exist; required at least $MinRunCount."
    }

    $selectedLogs = @($logs | Select-Object -First ([Math]::Max($MinRunCount, 1)))

    if ($logs.Count -gt 0) {
        $latestAge = $now - ([DateTimeOffset]$logs[0].LastWriteTimeUtc)
        if ($latestAge.TotalMinutes -gt $MaxLatestRunAgeMinutes) {
            Add-Violation "latest_runtime_log_stale" "Latest runtime log is stale: age minutes $([Math]::Round($latestAge.TotalMinutes, 3)) exceeds max $MaxLatestRunAgeMinutes."
        }
    }

    foreach ($log in $selectedLogs) {
        $content = ""
        try {
            $content = Get-Content -LiteralPath $log.FullName -Raw
        } catch {
            Add-Violation "runtime_log_unreadable" "Could not read runtime log $($log.FullName): $($_.Exception.Message)"
        }

        $completionMarkers = @(
            "H024 read-only VPS observer run complete.",
            "Status: COMPLETED",
            "Verifier verdict: PASS"
        )

        $readOnlyMarkers = @(
            "read-only",
            "No trading"
        )

        $containsCompletionMarker = $false
        foreach ($marker in $completionMarkers) {
            if ($content.Contains($marker)) {
                $containsCompletionMarker = $true
            }
        }

        $containsReadOnlyMarker = $false
        foreach ($marker in $readOnlyMarkers) {
            if ($content.Contains($marker)) {
                $containsReadOnlyMarker = $true
            }
        }

        if ($containsCompletionMarker) {
            $completedLogCount += 1
        } else {
            Add-Violation "runtime_log_completion_marker_missing" "Runtime log does not contain a completion marker: $($log.FullName)."
        }

        if (-not $containsReadOnlyMarker) {
            Add-Violation "runtime_log_read_only_marker_missing" "Runtime log does not contain a read-only/no-trading marker: $($log.FullName)."
        }

        $tail = ""
        try {
            $tail = (Get-Content -LiteralPath $log.FullName -Tail $LogTailLines) -join "`n"
        } catch {
            $tail = ""
        }

        $logAge = $now - ([DateTimeOffset]$log.LastWriteTimeUtc)

        $runLogs += [ordered]@{
            path = Get-RelativePath -Path $log.FullName
            last_write_time_utc = ([DateTimeOffset]$log.LastWriteTimeUtc).ToUniversalTime().ToString("o")
            age_seconds = [Math]::Round($logAge.TotalSeconds, 3)
            contains_completion_marker = $containsCompletionMarker
            contains_read_only_marker = $containsReadOnlyMarker
            tail = $tail
        }
    }
}

if ($completedLogCount -lt $MinRunCount) {
    Add-Violation "insufficient_completed_observer_runs" "Only $completedLogCount completed observer runtime logs were found in the newest window; required at least $MinRunCount."
}

$verdict = "PASS"
$operatorState = "READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_OK_BUT_TRADING_NOT_AUTHORIZED"
$operatorNextAction = "CONTINUE_LOCAL_WINDOWS_READ_ONLY_OBSERVER_SUPERVISION_NO_TRADING_AUTHORIZED"

if ($script:Violations.Count -gt 0) {
    $verdict = "FAIL_CLOSED"
    $operatorState = "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_CONTINUITY_SUMMARY_UNVERIFIED_NO_TRADING_AUTHORIZED"
    $operatorNextAction = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
}

$packet = [ordered]@{
    schema_version = 1
    strategy = "H024"
    component = "read_only_vps_observer_continuity_summary"
    generated_at_utc = $now.ToString("o")
    verdict = $verdict
    operator_state = $operatorState
    operator_next_action = $operatorNextAction
    root = $resolvedRoot
    reports_root = Get-RelativePath -Path $reportsRoot
    runtime_root = Get-RelativePath -Path $runtimeRoot
    min_run_count = $MinRunCount
    max_packet_age_minutes = $MaxPacketAgeMinutes
    max_latest_run_age_minutes = $MaxLatestRunAgeMinutes
    runtime_log_count_evaluated = $runLogs.Count
    completed_runtime_log_count_evaluated = $completedLogCount
    last_run_summary = $lastRunSummaryInfo
    upstream_packets = $upstreamPackets
    runtime_logs = $runLogs
    violations = @($script:Violations)
    read_only_observer_continuity_authorizes_trading = $false
    trading_authorized = $false
    broker_mutation_authorized = $false
    live_execution_authorized = $false
}

$packet | ConvertTo-Json -Depth 32 | Set-Content -LiteralPath $OutputJson -Encoding UTF8

$textLines = @(
    "H024 read-only VPS observer continuity summary",
    "",
    ("verdict              : {0}" -f $verdict),
    ("operator_state       : {0}" -f $operatorState),
    ("operator_next_action : {0}" -f $operatorNextAction),
    ("generated_at_utc     : {0}" -f $now.ToString("o")),
    "",
    ("min_run_count                         : {0}" -f $MinRunCount),
    ("runtime_log_count_evaluated           : {0}" -f $runLogs.Count),
    ("completed_runtime_log_count_evaluated : {0}" -f $completedLogCount),
    ("last_run_summary_present              : {0}" -f $lastRunSummaryInfo.present),
    ("last_run_summary_status               : {0}" -f $lastRunSummaryInfo.status),
    ("last_run_summary_exit_code            : {0}" -f $lastRunSummaryInfo.exit_code),
    "",
    "Upstream packets:"
)

foreach ($upstream in $upstreamPackets) {
    $textLines += ("- {0}: verdict={1} age_seconds={2} path={3}" -f $upstream.component, $upstream.verdict, $upstream.age_seconds, $upstream.path)
}

$textLines += ""
$textLines += "Runtime logs:"
foreach ($runLog in $runLogs) {
    $textLines += ("- {0}: completion_marker={1} read_only_marker={2} age_seconds={3}" -f $runLog.path, $runLog.contains_completion_marker, $runLog.contains_read_only_marker, $runLog.age_seconds)
}

$textLines += ""
$textLines += "Violations:"
if ($script:Violations.Count -eq 0) {
    $textLines += "- none"
} else {
    foreach ($violation in $script:Violations) {
        $textLines += ("- {0}: {1}" -f $violation.code, $violation.message)
    }
}

$textLines += ""
$textLines += "Safety:"
$textLines += "- read-only observer continuity evidence only"
$textLines += "- no trading authorization"
$textLines += "- no broker mutation authorization"
$textLines += "- no live execution authorization"

$textLines | Set-Content -LiteralPath $OutputText -Encoding UTF8

Write-Host "H024 read-only VPS observer continuity summary verdict: $verdict"
Write-Host "Operator state: $operatorState"
Write-Host "Violations: $($script:Violations.Count)"
Write-Host "Continuity JSON: $OutputJson"
Write-Host "Continuity text: $OutputText"

if ($verdict -ne "PASS") {
    exit 1
}

exit 0
