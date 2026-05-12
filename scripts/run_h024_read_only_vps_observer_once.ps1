$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $RepoRoot

function Run-Native {
    param(
        [Parameter(Mandatory=$true)][string]$Exe,
        [Parameter(ValueFromRemainingArguments=$true)][string[]]$Args
    )
    & $Exe @Args
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Exe $($Args -join ' ')"
    }
}

$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    throw "Missing expected venv Python at $Python. Activate/create .venv before running the read-only observer."
}

$Reports = Join-Path $RepoRoot "reports"
New-Item -ItemType Directory -Force -Path $Reports | Out-Null

function Run-Builder {
    param(
        [Parameter(Mandatory=$true)][string]$Name,
        [Parameter(Mandatory=$true)][string]$Script,
        [string[]]$ScriptArgs = @()
    )

    $path = Join-Path $RepoRoot $Script
    if (-not (Test-Path $path)) {
        throw "Missing required read-only observer builder for ${Name}: $Script"
    }

    Write-Host "=== $Name ==="
    Write-Host "Using builder: $Script"
    Run-Native $Python @($Script) @ScriptArgs
}

Write-Host "H024 read-only VPS observer starting."
Write-Host "Mode: read-only packet generation only. No trading or broker mutation is authorized."

Run-Builder "runtime heartbeat" "scripts\build_h024_runtime_safety_heartbeat_jsonl.py"
Run-Builder "runtime lockout reader" "scripts\build_h024_runtime_safety_lockout_jsonl.py"
Run-Builder "tick/spread supervisor" "scripts\build_h024_runtime_tick_spread_safety_supervisor_jsonl.py"
Run-Builder "exposure/inventory supervisor" "scripts\build_h024_runtime_exposure_inventory_safety_supervisor_jsonl.py"
Run-Builder "account risk/margin supervisor" "scripts\build_h024_runtime_account_risk_margin_safety_supervisor_jsonl.py"
Run-Builder "runtime safety aggregate" "scripts\build_h024_runtime_safety_aggregate_supervisor_jsonl.py"
Run-Builder "unified read-only runtime supervision" "scripts\build_h024_unified_read_only_post_canary_runtime_supervision_jsonl.py"
Run-Builder "runtime no-mutation safety gate" "scripts\build_h024_runtime_no_mutation_safety_gate_jsonl.py"

Write-Host "=== exact-ticket stack ==="
Write-Host "Using existing exact-ticket governance/decision/evidence/preview reports as upstream evidence."
Write-Host "The readiness aggregate and black-swan guard fail closed if those reports are missing, stale, malformed, fail-closed, or unsafe."

Run-Builder "read-only black-swan guard" "scripts\build_h024_read_only_black_swan_guard_jsonl.py"
Run-Native $Python "scripts\verify_h024_read_only_black_swan_guard_jsonl.py" "reports\h024_read_only_black_swan_guard.jsonl" "--require-pass"

Run-Builder "read-only VPS deployment readiness aggregate" "scripts\build_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py"
Run-Native $Python "scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py" "reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl" "--require-pass"

Write-Host "H024 read-only VPS observer run complete."
Write-Host "No trading, broker mutation, order_check, order_send, symbol_select, entry, close/modify, executable trade request, live broker request, or order-capable trading loop was authorized."