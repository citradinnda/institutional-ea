param(
    [string]$OutputPath = "reports/h024_read_only_vps_observer_evidence_bundle.json",
    [string]$TextOutputPath = "reports/h024_read_only_vps_observer_evidence_bundle.txt",
    [string]$RuntimeStateDirectory = "reports/runtime/h024_read_only_vps_observer",
    [string]$LastRunSummaryPath = "reports/runtime/h024_read_only_vps_observer/last_run_summary.json",
    [string]$HealthPacketPath = "reports/h024_read_only_vps_observer_healthcheck.json",
    [string]$TaskStatePacketPath = "reports/h024_read_only_vps_observer_task_state.json",
    [string]$RecoveryDrillPacketPath = "reports/h024_read_only_vps_recovery_drill_preview.json",
    [string]$InstallPreviewOutputPath = "reports/h024_read_only_vps_observer_install_preview_output.txt",
    [int]$MaxPacketAgeMinutes = 60,
    [int]$LogTailLines = 80,
    [switch]$IncludeInstallPreviewIfTaskMissing
)

$ErrorActionPreference = "Stop"

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDirectory "..")

function Resolve-RepoPath {
    param([Parameter(Mandatory=$true)][string]$Path)
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return (Join-Path $RepoRoot $Path)
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Content
    )
    $Directory = Split-Path -Parent $Path
    if ($Directory) {
        New-Item -ItemType Directory -Force -Path $Directory | Out-Null
    }
    $Encoding = New-Object System.Text.UTF8Encoding -ArgumentList $false
    [System.IO.File]::WriteAllText($Path, $Content, $Encoding)
}

function Get-ObjectValue {
    param(
        [Parameter(Mandatory=$true)]$Object,
        [Parameter(Mandatory=$true)][string[]]$Names
    )
    foreach ($Name in $Names) {
        $Property = $Object.PSObject.Properties[$Name]
        if ($null -ne $Property -and $null -ne $Property.Value -and "$($Property.Value)" -ne "") {
            return $Property.Value
        }
    }
    return $null
}

function Get-TimestampValue {
    param($Object)
    if ($null -eq $Object) {
        return $null
    }
    return Get-ObjectValue -Object $Object -Names @(
        "generated_at_utc", "checked_at_utc",
        "observed_at_utc",
        "created_at_utc",
        "evaluated_at_utc",
        "built_at_utc",
        "completed_at_utc",
        "started_at_utc",
        "timestamp_utc",
        "timestamp"
    )
}

function Test-FreshUtcTimestamp {
    param(
        $Timestamp,
        [int]$MaxAgeMinutes
    )
    if ($null -eq $Timestamp -or "$Timestamp" -eq "") {
        return @{
            ok = $false
            reason = "missing timestamp"
            parsed_utc = $null
            age_minutes = $null
        }
    }

    try {
        $Parsed = [datetimeoffset]::Parse("$Timestamp").ToUniversalTime()
        $Now = [datetimeoffset]::UtcNow
        $Age = ($Now - $Parsed).TotalMinutes
        if ($Age -lt -5) {
            return @{
                ok = $false
                reason = "timestamp is in the future"
                parsed_utc = $Parsed.ToString("o")
                age_minutes = $Age
            }
        }
        if ($Age -gt $MaxAgeMinutes) {
            return @{
                ok = $false
                reason = "timestamp is stale"
                parsed_utc = $Parsed.ToString("o")
                age_minutes = $Age
            }
        }
        return @{
            ok = $true
            reason = "fresh"
            parsed_utc = $Parsed.ToString("o")
            age_minutes = $Age
        }
    } catch {
        return @{
            ok = $false
            reason = "malformed timestamp: $($_.Exception.Message)"
            parsed_utc = $null
            age_minutes = $null
        }
    }
}

function Invoke-GitReadOnly {
    param([Parameter(Mandatory=$true)][string[]]$Arguments)

    Push-Location $RepoRoot
    try {
        $Output = & git @Arguments 2>&1
        $Code = $LASTEXITCODE
        return @{
            args = $Arguments
            exit_code = $Code
            output = @($Output | ForEach-Object { "$_" })
        }
    } finally {
        Pop-Location
    }
}

function Read-JsonPacket {
    param(
        [Parameter(Mandatory=$true)][string]$Label,
        [Parameter(Mandatory=$true)][string]$Path,
        [bool]$RequirePass = $true
    )

    $Resolved = Resolve-RepoPath $Path
    $Result = @{
        label = $Label
        path = $Path
        resolved_path = $Resolved
        exists = $false
        parsed = $false
        verdict = $null
        operator_state = $null
        timestamp_utc = $null
        freshness = $null
        violations_count = $null
        parse_error = $null
        require_pass = $RequirePass
        content = $null
    }

    if (-not (Test-Path -LiteralPath $Resolved)) {
        return $Result
    }

    $Result.exists = $true

    try {
        $Raw = Get-Content -LiteralPath $Resolved -Raw
        $Json = $Raw | ConvertFrom-Json
        $Result.parsed = $true
        $Result.content = $Json
        $Result.verdict = Get-ObjectValue -Object $Json -Names @("verdict", "status")
        $Result.operator_state = Get-ObjectValue -Object $Json -Names @("operator_state", "state")
        $Timestamp = Get-TimestampValue $Json
        $Result.timestamp_utc = $Timestamp
        $Result.freshness = Test-FreshUtcTimestamp -Timestamp $Timestamp -MaxAgeMinutes $MaxPacketAgeMinutes

        $Violations = Get-ObjectValue -Object $Json -Names @("violations")
        if ($null -ne $Violations) {
            try {
                $Result.violations_count = @($Violations).Count
            } catch {
                $Result.violations_count = $null
            }
        }

        return $Result
    } catch {
        $Result.parse_error = $_.Exception.Message
        return $Result
    }
}

function Add-PacketViolations {
    param(
        [Parameter(Mandatory=$true)]$Packet,
        [System.Collections.ArrayList]$Violations
    )

    if ($null -eq $Violations) {
        $Violations = New-Object System.Collections.ArrayList
    }

    if (-not $Packet.exists) {
        [void]$Violations.Add("$($Packet.label) missing at $($Packet.path)")
        return
    }
    if (-not $Packet.parsed) {
        [void]$Violations.Add("$($Packet.label) could not be parsed: $($Packet.parse_error)")
        return
    }
    if ($Packet.require_pass -and "$($Packet.verdict)" -ne "PASS") {
        [void]$Violations.Add("$($Packet.label) verdict is not PASS: $($Packet.verdict)")
    }
    if ($null -eq $Packet.freshness -or -not $Packet.freshness.ok) {
        $Reason = "unknown freshness failure"
        if ($null -ne $Packet.freshness) {
            $Reason = $Packet.freshness.reason
        }
        [void]$Violations.Add("$($Packet.label) evidence is not fresh: $Reason")
    }
}

function Get-LatestLogEvidence {
    param($LastRunSummary)

    $RuntimeResolved = Resolve-RepoPath $RuntimeStateDirectory
    $CandidatePath = $null

    if ($null -ne $LastRunSummary -and $LastRunSummary.parsed) {
        $CandidatePath = Get-ObjectValue -Object $LastRunSummary.content -Names @("log_path", "latest_log_path", "observer_log_path")
    }

    if ($null -eq $CandidatePath -or "$CandidatePath" -eq "") {
        $LogsDirectory = Join-Path $RuntimeResolved "logs"
        if (Test-Path -LiteralPath $LogsDirectory) {
            $Latest = Get-ChildItem -LiteralPath $LogsDirectory -Filter "*.log" -File |
                Sort-Object LastWriteTimeUtc -Descending |
                Select-Object -First 1
            if ($null -ne $Latest) {
                $CandidatePath = $Latest.FullName
            }
        }
    }

    if ($null -eq $CandidatePath -or "$CandidatePath" -eq "") {
        return @{
            path = $null
            resolved_path = $null
            exists = $false
            tail_line_count = 0
            tail = @()
            error = "no log path found in last-run summary or runtime logs directory"
        }
    }

    $ResolvedLog = Resolve-RepoPath "$CandidatePath"
    if (-not (Test-Path -LiteralPath $ResolvedLog)) {
        return @{
            path = "$CandidatePath"
            resolved_path = $ResolvedLog
            exists = $false
            tail_line_count = 0
            tail = @()
            error = "latest log path does not exist"
        }
    }

    $Tail = @(Get-Content -LiteralPath $ResolvedLog -Tail $LogTailLines)
    return @{
        path = "$CandidatePath"
        resolved_path = $ResolvedLog
        exists = $true
        tail_line_count = $Tail.Count
        tail = @($Tail | ForEach-Object { "$_" })
        error = $null
    }
}

function Test-TaskMissing {
    param($TaskStatePacket)
    if ($null -eq $TaskStatePacket -or -not $TaskStatePacket.parsed) {
        return $false
    }
    $Text = ($TaskStatePacket.content | ConvertTo-Json -Depth 32)
    return (
        $Text -match "TASK_NOT_INSTALLED" -or
        $Text -match "TASK_MISSING" -or
        $Text -match "not installed" -or
        $Text -match "not found" -or
        $Text -match "missing"
    )
}

function Run-InstallPreviewIfNeeded {
    param(
        $TaskStatePacket,
        [System.Collections.ArrayList]$Violations
    )

    if ($null -eq $Violations) {
        $Violations = New-Object System.Collections.ArrayList
    }

    $PreviewResolved = Resolve-RepoPath $InstallPreviewOutputPath
    $InstallScript = Resolve-RepoPath "scripts/install_h024_read_only_vps_observer_task.ps1"

    $Result = @{
        ran = $false
        reason = "not requested or task-state evidence does not indicate missing task"
        output_path = $InstallPreviewOutputPath
        resolved_output_path = $PreviewResolved
        exit_code = $null
        output = @()
    }

    if (-not $IncludeInstallPreviewIfTaskMissing) {
        return $Result
    }

    if (-not (Test-TaskMissing -TaskStatePacket $TaskStatePacket)) {
        return $Result
    }

    $Result.ran = $true
    $Result.reason = "task-state evidence indicates the scheduled task may be missing"

    if (-not (Test-Path -LiteralPath $InstallScript)) {
        $Result.exit_code = -1
        $Result.output = @("install preview script missing: $InstallScript")
        [void]$Violations.Add("install preview requested but install script is missing")
        Write-Utf8NoBom -Path $PreviewResolved -Content (($Result.output -join [Environment]::NewLine) + [Environment]::NewLine)
        return $Result
    }

    $Output = & powershell -NoProfile -ExecutionPolicy Bypass -File $InstallScript -Preview 2>&1
    $Code = $LASTEXITCODE
    $Result.exit_code = $Code
    $Result.output = @($Output | ForEach-Object { "$_" })

    Write-Utf8NoBom -Path $PreviewResolved -Content (($Result.output -join [Environment]::NewLine) + [Environment]::NewLine)

    if ($Code -ne 0) {
        [void]$Violations.Add("install preview command failed with exit code $Code")
    }

    return $Result
}

$Violations = New-Object System.Collections.ArrayList

$GitHead = Invoke-GitReadOnly @("rev-parse", "HEAD")
$GitBranch = Invoke-GitReadOnly @("branch", "--show-current")
$GitStatus = Invoke-GitReadOnly @("status")
$GitStatusPorcelain = Invoke-GitReadOnly @("status", "--porcelain")

foreach ($GitResult in @($GitHead, $GitBranch, $GitStatus, $GitStatusPorcelain)) {
    if ($GitResult.exit_code -ne 0) {
        [void]$Violations.Add("git command failed: git $($GitResult.args -join ' ')")
    }
}

$LastRun = Read-JsonPacket -Label "scheduled wrapper last-run summary" -Path $LastRunSummaryPath -RequirePass $false
$Health = Read-JsonPacket -Label "observer healthcheck packet" -Path $HealthPacketPath -RequirePass $true
$TaskState = Read-JsonPacket -Label "observer task-state packet" -Path $TaskStatePacketPath -RequirePass $true
$Recovery = Read-JsonPacket -Label "recovery drill preview packet" -Path $RecoveryDrillPacketPath -RequirePass $true

foreach ($Packet in @($LastRun, $Health, $TaskState, $Recovery)) {
    Add-PacketViolations -Packet $Packet -Violations $Violations
}

if ($LastRun.parsed) {
    $ExitCode = Get-ObjectValue -Object $LastRun.content -Names @("exit_code", "observer_exit_code", "last_exit_code", "process_exit_code")
    if ($null -eq $ExitCode) {
        [void]$Violations.Add("scheduled wrapper last-run summary does not expose an exit code")
    } elseif ([int]$ExitCode -ne 0) {
        [void]$Violations.Add("scheduled wrapper last-run exit code is non-zero: $ExitCode")
    }
}

$LatestLog = Get-LatestLogEvidence -LastRunSummary $LastRun
if (-not $LatestLog.exists) {
    [void]$Violations.Add("latest scheduled observer log is missing: $($LatestLog.error)")
}
if ($LatestLog.exists -and $LatestLog.tail_line_count -eq 0) {
    [void]$Violations.Add("latest scheduled observer log exists but has no readable tail lines")
}

$InstallPreview = Run-InstallPreviewIfNeeded -TaskStatePacket $TaskState -Violations $Violations

$Verdict = "PASS"
$OperatorState = "READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_OK_BUT_TRADING_NOT_AUTHORIZED"
$NextAction = "REVIEW_LOCAL_EVIDENCE_BUNDLE_NO_TRADING_AUTHORIZED"

if ($Violations.Count -gt 0) {
    $Verdict = "FAIL_CLOSED"
    $OperatorState = "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_EVIDENCE_BUNDLE_UNVERIFIED_NO_TRADING_AUTHORIZED"
    $NextAction = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
}

$Bundle = [ordered]@{
    schema_version = 1
    generated_at_utc = [datetimeoffset]::UtcNow.ToString("o")
    verdict = $Verdict
    operator_state = $OperatorState
    operator_next_action = $NextAction
    read_only_observer_only = $true
    evidence_bundle_authorizes_trading = $false
    safety = [ordered]@{
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
        external_alert_mutation_authorized = $false
        scheduler_mutation_authorized = $false
    }
    repository = [ordered]@{
        root = "$RepoRoot"
        head = if ($GitHead.output.Count -gt 0) { $GitHead.output[0] } else { $null }
        branch = if ($GitBranch.output.Count -gt 0) { $GitBranch.output[0] } else { $null }
        status = $GitStatus.output
        status_porcelain = $GitStatusPorcelain.output
        git_head_exit_code = $GitHead.exit_code
        git_branch_exit_code = $GitBranch.exit_code
        git_status_exit_code = $GitStatus.exit_code
        git_status_porcelain_exit_code = $GitStatusPorcelain.exit_code
    }
    evidence_paths = [ordered]@{
        last_run_summary = $LastRunSummaryPath
        healthcheck_packet = $HealthPacketPath
        task_state_packet = $TaskStatePacketPath
        recovery_drill_packet = $RecoveryDrillPacketPath
        latest_log = $LatestLog.path
        output_json = $OutputPath
        output_text = $TextOutputPath
    }
    packets = [ordered]@{
        scheduled_wrapper_last_run_summary = $LastRun
        observer_healthcheck = $Health
        observer_task_state = $TaskState
        recovery_drill_preview = $Recovery
    }
    latest_log = $LatestLog
    install_preview = $InstallPreview
    violations = @($Violations | ForEach-Object { "$_" })
}

$OutputResolved = Resolve-RepoPath $OutputPath
$TextResolved = Resolve-RepoPath $TextOutputPath

$Json = $Bundle | ConvertTo-Json -Depth 32
Write-Utf8NoBom -Path $OutputResolved -Content ($Json + [Environment]::NewLine)

$TextLines = @(
    "H024 read-only VPS observer evidence bundle verdict: $Verdict",
    "Operator state: $OperatorState",
    "Operator next action: $NextAction",
    "Violations: $($Violations.Count)",
    "Git HEAD: $($Bundle.repository.head)",
    "Git branch: $($Bundle.repository.branch)",
    "Latest log: $($LatestLog.path)",
    "Output JSON: $OutputPath",
    "Output text: $TextOutputPath",
    "",
    "Safety:",
    "trading_authorized: false",
    "broker_mutation_authorized: false",
    "order_check_authorized: false",
    "order_send_authorized: false",
    "entry_authorized: false",
    "close_modify_authorized: false",
    "xauusd_order_authorized: false",
    "usdjpy_order_authorized: false",
    "trading_loop_authorized: false",
    "automatic_execution_authorized: false",
    "live_broker_request_constructed: false",
    "executable_trade_request_constructed: false",
    "mt5_request_dictionary_constructed: false",
    "symbol_select_authorized: false",
    "external_alert_mutation_authorized: false",
    "scheduler_mutation_authorized: false"
)

if ($Violations.Count -gt 0) {
    $TextLines += ""
    $TextLines += "Violations:"
    foreach ($Violation in $Violations) {
        $TextLines += "- $Violation"
    }
}

Write-Utf8NoBom -Path $TextResolved -Content (($TextLines -join [Environment]::NewLine) + [Environment]::NewLine)

Write-Host "H024 read-only VPS observer evidence bundle verdict: $Verdict"
Write-Host "Operator state: $OperatorState"
Write-Host "Violations: $($Violations.Count)"
Write-Host "Evidence bundle JSON: $OutputPath"
Write-Host "Evidence bundle text: $TextOutputPath"

if ($Verdict -ne "PASS") {
    exit 2
}
