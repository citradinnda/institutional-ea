import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_h024_demo_order_plan_jsonl.py"
VERIFY_SCRIPT = ROOT / "scripts" / "verify_h024_demo_order_plan_jsonl.py"


def run_cli(args):
    return subprocess.run(
        [sys.executable, *[str(arg) for arg in args]],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def write_jsonl(path, records):
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def valid_request(**overrides):
    record = {
        "schema_version": "h024_dry_run_execution_request_v1",
        "request_kind": "DRY_RUN_MARKET_OPEN",
        "source_schema_version": "h024_intended_action_log_v1",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "timeframe": "H4",
        "side": "SELL",
        "entry_price": 4930.041,
        "stop_loss": 5019.068,
        "risk_usd": 100.0,
        "volume_lots": 0.01,
        "timestamp": "2026.05.11 07:45:49",
        "source_reason": (
            "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;"
            "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
        ),
    }
    record.update(overrides)
    return record


def valid_plan(**overrides):
    record = {
        "schema_version": "h024_demo_order_plan_v1",
        "plan_kind": "PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY",
        "source_schema_version": "h024_intended_action_log_v1",
        "source_request_kind": "DRY_RUN_MARKET_OPEN",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "timeframe": "H4",
        "side": "SELL",
        "entry_price": 4930.041,
        "stop_loss": 5019.068,
        "risk_usd": 100.0,
        "volume_lots": 0.01,
        "source_timestamp": "2026.05.11 07:45:49",
        "source_reason": (
            "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;"
            "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
        ),
        "account_server": "Exness-MT5Trial6",
        "account_currency": "USD",
        "account_balance": 10000.0,
        "account_equity": 10000.0,
        "broker": "Exness Technologies Ltd",
        "account_login": None,
    }
    record.update(overrides)
    return record


def test_builder_writes_verifiable_plan_jsonl(tmp_path):
    request_jsonl = tmp_path / "requests.jsonl"
    plan_jsonl = tmp_path / "plans.jsonl"
    write_jsonl(request_jsonl, [valid_request()])

    result = run_cli(
        [
            BUILD_SCRIPT,
            request_jsonl,
            "--output-jsonl",
            plan_jsonl,
            "--server",
            "Exness-MT5Trial6",
            "--account-currency",
            "USD",
            "--account-balance",
            "10000",
            "--account-equity",
            "10000",
            "--broker",
            "Exness Technologies Ltd",
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-plan",
        ]
    )

    assert result.returncode == 0, result.stdout + result.stderr
    written = [json.loads(line) for line in plan_jsonl.read_text(encoding="utf-8").splitlines()]
    assert len(written) == 1
    assert written[0]["schema_version"] == "h024_demo_order_plan_v1"
    assert written[0]["plan_kind"] == "PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY"
    assert written[0]["account_server"] == "Exness-MT5Trial6"

    verify = run_cli(
        [
            VERIFY_SCRIPT,
            plan_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-plan",
        ]
    )

    assert verify.returncode == 0, verify.stdout + verify.stderr


def test_builder_rejects_live_like_server_even_when_allowlisted(tmp_path):
    request_jsonl = tmp_path / "requests.jsonl"
    plan_jsonl = tmp_path / "plans.jsonl"
    write_jsonl(request_jsonl, [valid_request()])

    result = run_cli(
        [
            BUILD_SCRIPT,
            request_jsonl,
            "--output-jsonl",
            plan_jsonl,
            "--server",
            "Exness-Live",
            "--account-currency",
            "USD",
            "--account-balance",
            "10000",
            "--account-equity",
            "10000",
            "--allowed-demo-server",
            "Exness-Live",
            "--require-plan",
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 1
    assert "live-like" in combined
    assert not plan_jsonl.exists()


def test_builder_require_plan_fails_on_empty_jsonl(tmp_path):
    request_jsonl = tmp_path / "requests.jsonl"
    plan_jsonl = tmp_path / "plans.jsonl"
    request_jsonl.write_text("", encoding="utf-8")

    result = run_cli(
        [
            BUILD_SCRIPT,
            request_jsonl,
            "--output-jsonl",
            plan_jsonl,
            "--server",
            "Exness-MT5Trial6",
            "--account-currency",
            "USD",
            "--account-balance",
            "10000",
            "--account-equity",
            "10000",
            "--require-plan",
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 1
    assert "required at least one proposed plan" in combined
    assert not plan_jsonl.exists()


def test_verifier_rejects_execution_like_ticket_key(tmp_path):
    plan_jsonl = tmp_path / "plans.jsonl"
    write_jsonl(plan_jsonl, [valid_plan(ticket=123456)])

    result = run_cli(
        [
            VERIFY_SCRIPT,
            plan_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-plan",
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 1
    assert "execution-like key is forbidden" in combined


def test_verifier_rejects_unknown_demo_server(tmp_path):
    plan_jsonl = tmp_path / "plans.jsonl"
    write_jsonl(plan_jsonl, [valid_plan(account_server="Unknown-Demo")])

    result = run_cli(
        [
            VERIFY_SCRIPT,
            plan_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-plan",
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 1
    assert "demo allowlist" in combined


def test_verifier_rejects_invalid_stop_geometry(tmp_path):
    plan_jsonl = tmp_path / "plans.jsonl"
    write_jsonl(
        plan_jsonl,
        [valid_plan(side="SELL", entry_price=4930.0, stop_loss=4929.0)],
    )

    result = run_cli(
        [
            VERIFY_SCRIPT,
            plan_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-plan",
        ]
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 1
    assert "SELL stop_loss must be above entry" in combined
