param(
    [string]$Root = "",
    [string]$TaskName = "H024 Read Only VPS Observer",
    [int]$ExpectedIntervalMinutes = 5,
    [int]$MaxLastRunAgeMinutes = 15,
    [string]$OutputPath = "",
    [string]$AlertJsonPath = "",
    [string]$AlertTextPath = "",
    [string]$MockTaskJsonPath = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = Split-Path -Parent $PSScriptRoot
}

$Root = [System.IO.Path]::GetFullPath($Root)

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $Root "reports\h024_read_only_vps_observer_task_state.json"
}
if ([string]::IsNullOrWhiteSpace($AlertJsonPath)) {
    $AlertJsonPath = Join-Path $Root "reports\h024_read_only_vps_observer_operator_alert.json"
}
if ([string]::IsNullOrWhiteSpace($AlertTextPath)) {
    $AlertTextPath = Join-Path $Root "reports\h024_read_only_vps_observer_operator_alert.txt"
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

function Convert-IsoDurationToMinutes {
    param($Value)

    if ($null -eq $Value) {
        return $null
    }

    if ($Value -is [TimeSpan]) {
        return [double]$Value.TotalMinutes
    }

    $text = ([string]$Value).Trim()
    if ([string]::IsNullOrWhiteSpace($text)) {
        return $null
    }

    try {
        return [double]([TimeSpan]::Parse($text)).TotalMinutes
    } catch {
    }

    if ($text -match '^(?i)P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$') {
        $days = 0
        $hours = 0
        $minutes = 0
        $seconds = 0

        if ($Matches[1]) { $days = [int]$Matches[1] }
        if ($Matches[2]) { $hours = [int]$Matches[2] }
        if ($Matches[3]) { $minutes = [int]$Matches[3] }
        if ($Matches[4]) { $seconds = [int]$Matches[4] }

        return [double](($days * 1440) + ($hours * 60) + $minutes + ($seconds / 60.0))
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
        task_state_audit_authorizes_trading = $false
    }
}

$now = [DateTimeOffset]::UtcNow
$taskExists = $false
$sourceMode = "windows_task_scheduler"
$state = $null
$lastRunTimeUtc = $null
$lastTaskResult = $null
$triggerSummaries = @()
$rawTaskPath = $null

if (-not [string]::IsNullOrWhiteSpace($MockTaskJsonPath)) {
    $sourceMode = "mock_task_json"
    if (-not (Test-Path $MockTaskJsonPath)) {
        Add-Violation "mock_task_json_missing" "Mock task JSON path does not exist: $MockTaskJsonPath"
    } else {
        $mock = Get-Content -Raw -Path $MockTaskJsonPath | ConvertFrom-Json
        $taskExists = [bool](Get-PropertyValue $mock @("task_exists","taskExists","exists"))
        $state = [string](Get-PropertyValue $mock @("state","State"))
        $lastRunTimeUtc = Convert-DateToUtcIso (Get-PropertyValue $mock @("last_run_time_utc","lastRunTimeUtc","LastRunTimeUtc","last_run_time","LastRunTime"))
        $lastTaskResult = Get-PropertyValue $mock @("last_task_result","lastTaskResult","LastTaskResult")
        $rawTaskPath = [string](Get-PropertyValue $mock @("task_path","TaskPath"))

        $mockTriggers = @(Get-PropertyValue $mock @("triggers","Triggers"))
        if ($mockTriggers.Count -eq 0) {
            $topInterval = Get-PropertyValue $mock @("repetition_interval","RepetitionInterval")
            if ($null -ne $topInterval) {
                $mockTriggers = @([ordered]@{
                    enabled = $true
                    repetition_interval = $topInterval
                    start_boundary = $null
                })
            }
        }

        foreach ($trigger in $mockTriggers) {
            $enabledValue = Get-PropertyValue $trigger @("enabled","Enabled")
            if ($null -eq $enabledValue) {
                $enabledValue = $true
            }

            $intervalRaw = Get-PropertyValue $trigger @("repetition_interval","RepetitionInterval","interval","Interval")
            $intervalMinutes = Convert-IsoDurationToMinutes $intervalRaw
            $intervalMinutesExplicit = Get-PropertyValue $trigger @("repetition_interval_minutes","RepetitionIntervalMinutes")
            if ($null -eq $intervalMinutes -and $null -ne $intervalMinutesExplicit) {
                $intervalMinutes = [double]$intervalMinutesExplicit
            }

            $triggerSummaries += [ordered]@{
                enabled = [bool]$enabledValue
                repetition_interval = if ($null -eq $intervalRaw) { $null } else { [string]$intervalRaw }
                repetition_interval_minutes = $intervalMinutes
                start_boundary = Get-PropertyValue $trigger @("start_boundary","StartBoundary")
            }
        }
    }
} else {
    $getTaskCommand = Get-Command "Get-ScheduledTask" -ErrorAction SilentlyContinue
    $getTaskInfoCommand = Get-Command "Get-ScheduledTaskInfo" -ErrorAction SilentlyContinue

    if ($null -eq $getTaskCommand -or $null -eq $getTaskInfoCommand) {
        Add-Violation "scheduled_task_cmdlets_unavailable" "Windows scheduled task cmdlets are unavailable in this shell."
    } else {
        $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
        if ($null -eq $task) {
            Add-Violation "scheduled_task_not_installed" "Scheduled task is not installed: $TaskName"
        } else {
            $taskExists = $true
            $state = [string]$task.State
            $rawTaskPath = [string]$task.TaskPath

            foreach ($trigger in @($task.Triggers)) {
                $enabledValue = $true
                if ($trigger.PSObject.Properties.Name -contains "Enabled") {
                    $enabledValue = [bool]$trigger.Enabled
                }

                $intervalRaw = $null
                if ($null -ne $trigger.Repetition -and $trigger.Repetition.PSObject.Properties.Name -contains "Interval") {
                    $intervalRaw = $trigger.Repetition.Interval
                }

                $triggerSummaries += [ordered]@{
                    enabled = $enabledValue
                    repetition_interval = if ($null -eq $intervalRaw) { $null } else { [string]$intervalRaw }
                    repetition_interval_minutes = Convert-IsoDurationToMinutes $intervalRaw
                    start_boundary = if ($trigger.PSObject.Properties.Name -contains "StartBoundary") { [string]$trigger.StartBoundary } else { $null }
                }
            }

            $taskInfo = Get-ScheduledTaskInfo -TaskName $TaskName -ErrorAction SilentlyContinue
            if ($null -ne $taskInfo) {
                $lastTaskResult = $taskInfo.LastTaskResult
                if ($null -ne $taskInfo.LastRunTime -and ([DateTime]$taskInfo.LastRunTime).Year -gt 2000) {
                    $lastRunTimeUtc = ([DateTime]$taskInfo.LastRunTime).ToUniversalTime().ToString("o")
                }
            }
        }
    }
}

if (-not $taskExists) {
    if (-not ($violations | Where-Object { $_.code -eq "scheduled_task_not_installed" -or $_.code -eq "mock_task_json_missing" })) {
        Add-Violation "scheduled_task_not_installed" "Scheduled task is not installed or could not be observed: $TaskName"
    }
}

if ($taskExists) {
    if ([string]::IsNullOrWhiteSpace($state)) {
        Add-Violation "scheduled_task_state_missing" "Scheduled task state is missing."
    } elseif ($state -match "Disabled") {
        Add-Violation "scheduled_task_disabled" "Scheduled task is disabled."
    } elseif ($state -notmatch "Ready|Running|Queued") {
        Add-Violation "scheduled_task_state_unexpected" "Scheduled task state is unexpected: $state"
    }

    if ($triggerSummaries.Count -eq 0) {
        Add-Violation "scheduled_task_trigger_missing" "Scheduled task has no observable trigger."
    } else {
        $enabledTriggers = @($triggerSummaries | Where-Object { $_.enabled -eq $true })
        if ($enabledTriggers.Count -eq 0) {
            Add-Violation "scheduled_task_trigger_disabled" "Scheduled task has no enabled trigger."
        }

        $matchingIntervals = @(
            $triggerSummaries |
            Where-Object {
                $null -ne $_.repetition_interval_minutes -and
                [Math]::Abs(([double]$_.repetition_interval_minutes) - [double]$ExpectedIntervalMinutes) -lt 0.01
            }
        )

        if ($matchingIntervals.Count -eq 0) {
            Add-Violation "scheduled_task_trigger_interval_mismatch" "No scheduled task trigger repeats every expected $ExpectedIntervalMinutes minute(s)."
        }
    }

    if ($null -eq $lastTaskResult -or [string]::IsNullOrWhiteSpace([string]$lastTaskResult)) {
        Add-Violation "scheduled_task_last_result_missing" "Scheduled task last result is missing."
    } else {
        try {
            $lastTaskResultInt = [int]$lastTaskResult
            if ($lastTaskResultInt -ne 0) {
                Add-Violation "scheduled_task_last_result_nonzero" "Scheduled task last result is non-zero: $lastTaskResultInt"
            }
        } catch {
            Add-Violation "scheduled_task_last_result_malformed" "Scheduled task last result is malformed: $lastTaskResult"
        }
    }

    if ([string]::IsNullOrWhiteSpace($lastRunTimeUtc)) {
        Add-Violation "scheduled_task_last_run_missing" "Scheduled task has no valid last run timestamp."
    } else {
        try {
            $lastRunDto = [DateTimeOffset]::Parse($lastRunTimeUtc, [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::AdjustToUniversal)
            $ageMinutes = ($now - $lastRunDto.ToUniversalTime()).TotalMinutes
            if ($ageMinutes -lt -1) {
                Add-Violation "scheduled_task_last_run_in_future" "Scheduled task last run timestamp is in the future."
            } elseif ($ageMinutes -gt $MaxLastRunAgeMinutes) {
                Add-Violation "scheduled_task_last_run_stale" "Scheduled task last run is stale: $([Math]::Round($ageMinutes, 3)) minute(s)."
            }
        } catch {
            Add-Violation "scheduled_task_last_run_malformed" "Scheduled task last run timestamp is malformed: $lastRunTimeUtc"
        }
    }
}

$passed = ($violations.Count -eq 0)

if ($passed) {
    $verdict = "PASS"
    $operatorState = "READ_ONLY_VPS_OBSERVER_TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED"
    $operatorNextAction = "CONTINUE_READ_ONLY_OBSERVER_SCHEDULER_SUPERVISION_NO_TRADING_AUTHORIZED"
    $alertSeverity = "INFO"
    $alertState = "TASK_STATE_OK_BUT_TRADING_NOT_AUTHORIZED"
    $operatorMessage = "Scheduled task state is coherent for read-only observer operations only. Trading remains unauthorized."
    $exitCode = 0
} else {
    $verdict = "FAIL_CLOSED"
    $operatorState = "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_TASK_STATE_UNVERIFIED_NO_TRADING_AUTHORIZED"
    $operatorNextAction = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    $alertSeverity = "CRITICAL"
    $alertState = "OPERATOR_ALERT_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
    $operatorMessage = "Scheduled task state is missing, stale, disabled, failing, malformed, or unverifiable. Operator review required. Trading remains unauthorized."
    $exitCode = 1
}

$taskState = [ordered]@{
    task_name = $TaskName
    task_path = $rawTaskPath
    source_mode = $sourceMode
    task_exists = $taskExists
    state = $state
    expected_interval_minutes = $ExpectedIntervalMinutes
    max_last_run_age_minutes = $MaxLastRunAgeMinutes
    trigger_count = $triggerSummaries.Count
    triggers = $triggerSummaries
    last_run_time_utc = $lastRunTimeUtc
    last_task_result = $lastTaskResult
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
    operator_state = $operatorState
    operator_next_action = $operatorNextAction
    task_state = $taskState
    violations = $violations
    operator_alert_surface = $alert
    safety = New-SafetyMap
}

Write-JsonNoBom -Path $OutputPath -Object $packet
Write-JsonNoBom -Path $AlertJsonPath -Object $alert

$alertText = @(
    "H024 read-only VPS observer operator alert"
    "Generated UTC: $($now.ToString("o"))"
    "Severity: $alertSeverity"
    "State: $alertState"
    "Task: $TaskName"
    "Message: $operatorMessage"
    "Next action: $operatorNextAction"
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

Write-Host "H024 read-only VPS observer task-state verdict: $verdict"
Write-Host "Operator state: $operatorState"
Write-Host "Violations: $($violations.Count)"
Write-Host "Task-state packet: $OutputPath"
Write-Host "Operator alert JSON: $AlertJsonPath"
Write-Host "Operator alert text: $AlertTextPath"

exit $exitCode