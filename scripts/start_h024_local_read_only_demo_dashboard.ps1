[CmdletBinding()]
param(
    [string]$Root = (Resolve-Path ".").Path,
    [switch]$SkipRefresh,
    [switch]$NoOpen
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path $Root).Path
$ReportsDir = Join-Path -Path $RepoRoot -ChildPath "reports"
$DemoDir = Join-Path -Path $ReportsDir -ChildPath "demo"
$DashboardPath = Join-Path -Path $DemoDir -ChildPath "h024_local_read_only_demo_dashboard.html"
$VerifierPath = Join-Path -Path $RepoRoot -ChildPath "scripts\verify_h024_free_local_read_only_demo_deployment_readiness.ps1"
$ReadinessPath = Join-Path -Path $ReportsDir -ChildPath "h024_free_local_read_only_demo_deployment_readiness.json"
$CadencePath = Join-Path -Path $ReportsDir -ChildPath "h024_read_only_vps_observer_scheduled_cadence_summary.json"
$LastRunPath = Join-Path -Path $ReportsDir -ChildPath "runtime\h024_read_only_vps_observer\last_run_summary.json"
$NoTradingBannerText = "READ-ONLY DEMO ONLY " + [char]0x2014 + " NO TRADING AUTHORIZED"

New-Item -ItemType Directory -Force -Path $DemoDir | Out-Null

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

function HtmlSafe {
    param([object]$Value)
    if ($null -eq $Value) {
        return ""
    }
    return [System.Net.WebUtility]::HtmlEncode([string]$Value)
}

function Read-JsonFile {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        return $null
    }

    try {
        return Get-Content -Raw -Path $Path | ConvertFrom-Json
    } catch {
        return $null
    }
}

function Read-JsonOrJsonlFile {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        return $null
    }

    try {
        if ($Path.ToLowerInvariant().EndsWith(".jsonl")) {
            $Lines = @(Get-Content -Path $Path | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
            if ($Lines.Count -eq 0) {
                return $null
            }
            return $Lines[-1] | ConvertFrom-Json
        }

        return Get-Content -Raw -Path $Path | ConvertFrom-Json
    } catch {
        return $null
    }
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

function Find-FirstField {
    param(
        [object]$Object,
        [string[]]$Names,
        [int]$Depth = 0
    )

    if ($null -eq $Object -or $Depth -gt 8) {
        return $null
    }

    if ($Object -is [pscustomobject]) {
        foreach ($Name in $Names) {
            $Value = Get-Prop -Object $Object -Name $Name
            if ($null -ne $Value) {
                return $Value
            }
        }

        foreach ($Property in $Object.PSObject.Properties) {
            $Found = Find-FirstField -Object $Property.Value -Names $Names -Depth ($Depth + 1)
            if ($null -ne $Found) {
                return $Found
            }
        }
    } elseif (($Object -is [System.Collections.IEnumerable]) -and -not ($Object -is [string])) {
        foreach ($Item in $Object) {
            $Found = Find-FirstField -Object $Item -Names $Names -Depth ($Depth + 1)
            if ($null -ne $Found) {
                return $Found
            }
        }
    }

    return $null
}

function Render-KvRow {
    param(
        [string]$Key,
        [object]$Value
    )
    return "<tr><th>$(HtmlSafe $Key)</th><td>$(HtmlSafe $Value)</td></tr>"
}

function Render-StatusClass {
    param([object]$Value)

    if ([string]$Value -eq "PASS" -or [string]$Value -eq "True" -or $Value -eq $true -or [string]$Value -eq "COMPLETED") {
        return "good"
    }

    if ([string]::IsNullOrWhiteSpace([string]$Value)) {
        return "muted"
    }

    return "bad"
}

$ReadinessRefreshFailed = $false
$ReadinessRefreshExitCode = $null
$ReadinessRefreshStatus = "SKIPPED"

if (-not $SkipRefresh) {
    Write-Host "=== Refresh existing free local read-only demo deployment readiness verifier ==="
    & powershell -NoProfile -ExecutionPolicy Bypass -File $VerifierPath
    $ReadinessRefreshExitCode = $LASTEXITCODE

    if ($LASTEXITCODE -ne 0) {
        $ReadinessRefreshFailed = $true
        $ReadinessRefreshStatus = "FAILED"
        Write-Host "Read-only demo readiness verifier failed. Generating fail-safe dashboard. No trading authorized."
    } else {
        $ReadinessRefreshStatus = "PASS"
    }
}

$Readiness = Read-JsonFile -Path $ReadinessPath
if ($null -eq $Readiness) {
    $ReadinessRefreshFailed = $true
    $ReadinessRefreshStatus = "FAILED_MISSING_READINESS_JSON"
    $Readiness = [pscustomobject]@{
        verdict = "FAIL_CLOSED"
        read_only_demo_ready = $false
        read_only_demo_deployment_readiness_authorizes_trading = $false
        operator_state = "FAIL_CLOSED_LOCAL_READ_ONLY_DEMO_DASHBOARD_MISSING_READINESS_JSON_NO_TRADING_AUTHORIZED"
        generated_at_utc = $null
        scheduled_task = $null
        latest_run_summary = $null
        upstream_packets = @()
    }
}

$Cadence = Read-JsonFile -Path $CadencePath
$LastRun = Read-JsonFile -Path $LastRunPath

$CanaryCandidateFileNames = @(
    "h024_unified_post_canary_runtime_supervision.json",
    "h024_unified_post_canary_runtime_supervision.jsonl",
    "h024_runtime_safety_aggregate.json",
    "h024_runtime_safety_aggregate.jsonl",
    "h024_exposure_inventory_supervisor.json",
    "h024_exposure_inventory_supervisor.jsonl",
    "h024_account_risk_margin_supervisor.json",
    "h024_account_risk_margin_supervisor.jsonl",
    "h024_read_only_vps_observer_healthcheck.json"
)

$CanaryCandidatePaths = @(
    $CanaryCandidateFileNames | ForEach-Object {
        Join-Path -Path $ReportsDir -ChildPath $_
    }
)

$CanarySourcePath = $null
$CanarySource = $null
foreach ($CandidatePath in $CanaryCandidatePaths) {
    $Candidate = Read-JsonOrJsonlFile -Path $CandidatePath
    if ($null -ne $Candidate) {
        $CanarySourcePath = $CandidatePath
        $CanarySource = $Candidate
        break
    }
}

$ReadinessVerdict = Get-Prop -Object $Readiness -Name "verdict"
$ReadOnlyDemoReady = Get-Prop -Object $Readiness -Name "read_only_demo_ready"
$TradingAuthorized = Get-Prop -Object $Readiness -Name "read_only_demo_deployment_readiness_authorizes_trading"
$OperatorState = Get-Prop -Object $Readiness -Name "operator_state"
$GeneratedAt = Get-Prop -Object $Readiness -Name "generated_at_utc"

if ($ReadinessRefreshFailed) {
    $ReadinessVerdict = "FAIL_CLOSED"
    $ReadOnlyDemoReady = $false
    $TradingAuthorized = $false
    $OperatorState = "FAIL_CLOSED_LOCAL_READ_ONLY_DEMO_DASHBOARD_REFRESH_FAILED_NO_TRADING_AUTHORIZED"
}
$ScheduledTask = Get-Prop -Object $Readiness -Name "scheduled_task"
$LatestRunSummary = Get-Prop -Object $Readiness -Name "latest_run_summary"
if ($null -eq $LatestRunSummary) {
    $LatestRunSummary = $LastRun
}

$UpstreamPackets = @(Get-Prop -Object $Readiness -Name "upstream_packets")
$UpstreamRows = @()
foreach ($Packet in $UpstreamPackets) {
    $PacketName = HtmlSafe (Get-Prop -Object $Packet -Name "name")
    $PacketVerdict = HtmlSafe (Get-Prop -Object $Packet -Name "verdict")
    $PacketVerdictClass = Render-StatusClass (Get-Prop -Object $Packet -Name "verdict")
    $PacketAge = HtmlSafe (Get-Prop -Object $Packet -Name "age_minutes")
    $UnsafeFlags = HtmlSafe ((@(Get-Prop -Object $Packet -Name "unsafe_true_flags")) -join ", ")

    $UpstreamRows += "<tr><td>$PacketName</td><td><span class=""$PacketVerdictClass"">$PacketVerdict</span></td><td>$PacketAge</td><td>$UnsafeFlags</td></tr>"
}

if ($UpstreamRows.Count -eq 0) {
    $UpstreamRows += "<tr><td colspan=""4"" class=""muted"">No upstream packet summary found in readiness report.</td></tr>"
}

$CanaryRows = @()
if ($null -ne $CanarySource) {
    $CanaryFieldMap = @(
        @{ Label = "Source"; Names = @("__source_path") },
        @{ Label = "Verdict"; Names = @("verdict") },
        @{ Label = "Operator state"; Names = @("operator_state") },
        @{ Label = "Canary state"; Names = @("canary_state", "exact_canary_state") },
        @{ Label = "Ticket"; Names = @("ticket", "exact_ticket") },
        @{ Label = "Identifier"; Names = @("identifier", "exact_identifier") },
        @{ Label = "Symbol"; Names = @("symbol", "runtime_symbol", "position_symbol", "h024_position_symbol") },
        @{ Label = "Position count"; Names = @("h024_position_count", "position_count") },
        @{ Label = "Order count"; Names = @("h024_order_count", "order_count") },
        @{ Label = "Account server"; Names = @("account_server", "server") },
        @{ Label = "Account currency"; Names = @("account_currency", "currency") },
        @{ Label = "Balance"; Names = @("balance") },
        @{ Label = "Equity"; Names = @("equity") },
        @{ Label = "Margin"; Names = @("margin") },
        @{ Label = "Free margin"; Names = @("free_margin") },
        @{ Label = "Margin level"; Names = @("margin_level") }
    )

    foreach ($Field in $CanaryFieldMap) {
        if ($Field.Label -eq "Source") {
            $Value = $CanarySourcePath
        } else {
            $Value = Find-FirstField -Object $CanarySource -Names $Field.Names
        }

        if ($null -ne $Value -and -not [string]::IsNullOrWhiteSpace([string]$Value)) {
            $CanaryRows += Render-KvRow -Key $Field.Label -Value $Value
        }
    }
}

if ($CanaryRows.Count -eq 0) {
    $CanaryRows += "<tr><td colspan=""2"" class=""muted"">No canary/account summary found in the currently available reports. This dashboard remains valid for readiness/status demo.</td></tr>"
}

$GeneratedLocal = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"

$Html = @"
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>H024 Local Read-Only Demo Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {
  --bg: #0f172a;
  --panel: #111827;
  --panel2: #1f2937;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --good: #22c55e;
  --bad: #ef4444;
  --warn: #f59e0b;
  --line: #374151;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Segoe UI, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
}
header {
  padding: 24px;
  border-bottom: 1px solid var(--line);
  background: linear-gradient(135deg, #111827, #1e293b);
}
h1 { margin: 0 0 8px 0; font-size: 28px; }
h2 { margin: 0 0 14px 0; font-size: 18px; }
.banner {
  margin-top: 16px;
  padding: 16px;
  border: 2px solid var(--warn);
  border-radius: 12px;
  color: #fff7ed;
  background: rgba(245, 158, 11, 0.16);
  font-weight: 800;
  letter-spacing: .03em;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 16px;
  padding: 16px;
}
.card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,.25);
}
.card.full { grid-column: 1 / -1; }
.status {
  font-size: 34px;
  font-weight: 800;
  margin: 6px 0 10px 0;
}
.good { color: var(--good); font-weight: 700; }
.bad { color: var(--bad); font-weight: 700; }
.warn { color: var(--warn); font-weight: 700; }
.muted { color: var(--muted); }
table {
  width: 100%;
  border-collapse: collapse;
  overflow-wrap: anywhere;
}
th, td {
  text-align: left;
  padding: 9px 8px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
th {
  width: 38%;
  color: var(--muted);
  font-weight: 600;
}
footer {
  padding: 20px 24px;
  color: var(--muted);
  border-top: 1px solid var(--line);
}
.small { font-size: 13px; color: var(--muted); }
</style>
</head>
<body>
<header>
  <h1>H024 Local Read-Only Demo Dashboard</h1>
  <div class="small">Generated locally: $(HtmlSafe $GeneratedLocal)</div>
  <div class="banner">$(HtmlSafe $NoTradingBannerText)</div>
</header>

<main class="grid">
  <section class="card">
    <h2>Demo readiness</h2>
    <div class="status $(Render-StatusClass $ReadinessVerdict)">$(HtmlSafe $ReadinessVerdict)</div>
    <table>
      $(Render-KvRow -Key "Readiness refresh status" -Value $ReadinessRefreshStatus)
      $(Render-KvRow -Key "Readiness refresh exit code" -Value $ReadinessRefreshExitCode)
      $(Render-KvRow -Key "Read-only demo ready" -Value $ReadOnlyDemoReady)
      $(Render-KvRow -Key "Trading authorized" -Value $TradingAuthorized)
      $(Render-KvRow -Key "Operator state" -Value $OperatorState)
      $(Render-KvRow -Key "Readiness generated UTC" -Value $GeneratedAt)
    </table>
  </section>

  <section class="card">
    <h2>No-console scheduled task</h2>
    <table>
      $(Render-KvRow -Key "Task name" -Value (Get-Prop -Object $ScheduledTask -Name "task_name"))
      $(Render-KvRow -Key "Execute" -Value (Get-Prop -Object $ScheduledTask -Name "observed_execute"))
      $(Render-KvRow -Key "Argument" -Value (Get-Prop -Object $ScheduledTask -Name "observed_argument"))
      $(Render-KvRow -Key "Action OK" -Value (Get-Prop -Object $ScheduledTask -Name "action_ok"))
      $(Render-KvRow -Key "5-minute interval OK" -Value (Get-Prop -Object $ScheduledTask -Name "interval_ok"))
    </table>
  </section>

  <section class="card">
    <h2>Scheduled cadence</h2>
    <table>
      $(Render-KvRow -Key "Verdict" -Value (Get-Prop -Object $Cadence -Name "verdict"))
      $(Render-KvRow -Key "Observed runs" -Value (Get-Prop -Object $Cadence -Name "observed_run_count"))
      $(Render-KvRow -Key "Observed span minutes" -Value (Get-Prop -Object $Cadence -Name "observed_span_minutes"))
      $(Render-KvRow -Key "Min gap minutes" -Value (Get-Prop -Object $Cadence -Name "min_observed_gap_minutes"))
      $(Render-KvRow -Key "Max gap minutes" -Value (Get-Prop -Object $Cadence -Name "max_observed_gap_minutes"))
      $(Render-KvRow -Key "Latest observed run UTC" -Value (Get-Prop -Object $Cadence -Name "latest_observed_run_at_utc"))
    </table>
  </section>

  <section class="card">
    <h2>Latest scheduled run</h2>
    <table>
      $(Render-KvRow -Key "Status" -Value (Get-Prop -Object $LatestRunSummary -Name "status"))
      $(Render-KvRow -Key "Exit code" -Value (Get-Prop -Object $LatestRunSummary -Name "exit_code"))
      $(Render-KvRow -Key "Completed UTC" -Value (Get-Prop -Object $LatestRunSummary -Name "completed_at_utc"))
      $(Render-KvRow -Key "Age minutes" -Value (Get-Prop -Object $LatestRunSummary -Name "age_minutes"))
      $(Render-KvRow -Key "Read-only observer only" -Value (Get-Prop -Object $LatestRunSummary -Name "read_only_observer_only"))
    </table>
  </section>

  <section class="card full">
    <h2>Upstream packet summary</h2>
    <table>
      <thead>
        <tr><th>Packet</th><th>Verdict</th><th>Age minutes</th><th>Unsafe true flags</th></tr>
      </thead>
      <tbody>
        $($UpstreamRows -join [Environment]::NewLine)
      </tbody>
    </table>
  </section>

  <section class="card full">
    <h2>Canary / account observation summary</h2>
    <table>
      $($CanaryRows -join [Environment]::NewLine)
    </table>
  </section>

  <section class="card full">
    <h2>Operational boundary</h2>
    <p>
      This dashboard is a local UX layer over existing read-only reports. It is for status/demo observation only.
      It does not authorize trading, broker mutation, request construction, entries, close/modify, or any order-capable execution path.
    </p>
  </section>
</main>

<footer>
  Dashboard path: $(HtmlSafe $DashboardPath)<br>
  Generated under reports/demo/. Do not commit reports/.
</footer>
</body>
</html>
"@

Write-Utf8NoBom -Path $DashboardPath -Content $Html

Write-Host "H024 local read-only demo dashboard generated: $DashboardPath"
Write-Host "Readiness refresh status: $ReadinessRefreshStatus"
Write-Host "Readiness verdict: $ReadinessVerdict"
Write-Host "Read-only demo ready: $ReadOnlyDemoReady"
Write-Host "Trading authorized: False"
Write-Host "Broker mutation authorized: False"
Write-Host "Generated under reports/demo/. Do not commit reports/."

if (-not $NoOpen) {
    Start-Process $DashboardPath
}

exit 0