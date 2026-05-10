import csv
import json
from pathlib import Path

from scripts.reconcile_h024_runtime_dry_run_requests import (
    main,
    reconcile_h024_runtime_dry_run_requests,
)
from scripts.verify_h024_ea_preflight_log import (
    INTENDED_ACTION_LOG_ROW_FIELDS,
    REQUIRED_COLUMNS,
)


def _base_row(symbol: str, event: str, detail: str) -> list[str]:
    values = {
        "generated_at_server": "2026.05.08 13:00:00",
        "schema_version": "h024_ea_log_only_preflight_v2",
        "ea_version": "0.6",
        "source_version": "manual",
        "timer_seconds": "1",
        "runtime_mode": "log_only_preflight",
        "run_label": "H024_LOG_ONLY_PREFLIGHT",
        "event": event,
        "kill_switch_blocked": "true",
        "symbol": symbol,
        "account_company": "Exness",
        "account_server": "Demo",
        "account_currency": "USD",
        "account_balance": "10000.0",
        "account_equity": "10000.0",
        "account_leverage": "500",
        "account_trade_allowed": "true",
        "account_trade_expert": "true",
        "terminal_connected": "true",
        "terminal_trade_allowed": "true",
        "mql_trade_allowed": "true",
        "bid": "155.25",
        "ask": "155.26",
        "spread_points": "10",
        "volume_min": "0.01",
        "volume_max": "200.0",
        "volume_step": "0.01",
        "stops_level": "0",
        "freeze_level": "0",
        "point": "0.001",
        "digits": "3",
        "detail": detail,
    }
    return [values[column] for column in REQUIRED_COLUMNS]


def _header_row(symbol: str = "USDJPYm") -> list[str]:
    return _base_row(symbol, "H024_INTENDED_ACTION_HEADER", "timestamp") + list(
        INTENDED_ACTION_LOG_ROW_FIELDS
    )


def _intended_action_payload(
    *,
    symbol: str = "USDJPYm",
    normalized_symbol: str = "USDJPY",
    decision: str = "WOULD_OPEN",
    direction: str = "long",
    entry_price: str = "155.25",
    stop_price: str = "154.25",
    stop_distance_price: str = "1.0",
    lots: str = "0.03",
    reason: str = "signal_ready",
) -> list[str]:
    return [
        "h024_intended_action_log_v1",
        "0.6",
        symbol,
        normalized_symbol,
        "H4",
        decision,
        direction,
        entry_price,
        stop_price,
        stop_distance_price,
        "0.001",
        "0.65",
        "10000.0",
        "0.002",
        "20.0",
        "0.03076923076923077",
        lots,
        "0.01",
        "200.0",
        "0.01",
        "2",
        reason,
    ]


def _action_row(
    *,
    timestamp: str = "2026-05-08T13:00:00+00:00",
    symbol: str = "USDJPYm",
    payload: list[str] | None = None,
) -> list[str]:
    return _base_row(symbol, "H024_INTENDED_ACTION_ROW", timestamp) + (
        payload if payload is not None else _intended_action_payload(symbol=symbol)
    )


def _write_runtime_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(REQUIRED_COLUMNS)
        writer.writerows(rows)


def _minimum_valid_rows() -> list[list[str]]:
    return [
        _base_row("USDJPYm", "INIT", "init"),
        _base_row("XAUUSDm", "INIT", "init"),
    ]


def test_reconciles_would_open_intended_action_row_to_dry_run_request(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    _write_runtime_csv(
        csv_path,
        _minimum_valid_rows() + [_header_row(), _action_row()],
    )

    result = reconcile_h024_runtime_dry_run_requests(csv_path, require_request=True)

    assert result.passed
    assert result.rows == 4
    assert result.intended_action_rows == 1
    assert result.would_open_rows == 1
    assert result.skipped_rows == 0
    assert len(result.dry_run_requests) == 1

    request = result.dry_run_requests[0]
    assert request["timestamp"] == "2026-05-08T13:00:00+00:00"
    assert request["symbol"] == "USDJPYm"
    assert request["normalized_symbol"] == "USDJPY"
    assert request["side"] == "BUY"
    assert request["volume_lots"] == 0.03
    assert request["entry_price"] == 155.25
    assert request["stop_loss"] == 154.25
    assert request["risk_usd"] == 20.0


def test_reconciles_short_would_open_to_sell_request(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    payload = _intended_action_payload(
        decision="WOULD_OPEN",
        direction="short",
        entry_price="154.25",
        stop_price="155.25",
    )
    _write_runtime_csv(
        csv_path,
        _minimum_valid_rows() + [_header_row(), _action_row(payload=payload)],
    )

    result = reconcile_h024_runtime_dry_run_requests(csv_path, require_request=True)

    assert result.passed
    assert len(result.dry_run_requests) == 1
    assert result.dry_run_requests[0]["side"] == "SELL"
    assert result.dry_run_requests[0]["entry_price"] == 154.25
    assert result.dry_run_requests[0]["stop_loss"] == 155.25


def test_require_request_fails_when_runtime_has_no_would_open(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    payload = _intended_action_payload(
        symbol="XAUUSDm",
        normalized_symbol="XAUUSD",
        decision="NO_ACTION",
        direction="",
        entry_price="0.0",
        stop_price="0.0",
        stop_distance_price="0.0",
        lots="0.0",
        reason="no_signal",
    )
    _write_runtime_csv(
        csv_path,
        _minimum_valid_rows()
        + [_header_row("XAUUSDm"), _action_row(symbol="XAUUSDm", payload=payload)],
    )

    result = reconcile_h024_runtime_dry_run_requests(csv_path, require_request=True)

    assert not result.passed
    assert result.intended_action_rows == 1
    assert result.would_open_rows == 0
    assert result.skipped_rows == 1
    assert "missing required dry-run execution request" in result.violations


def test_cli_writes_jsonl_output_for_reconstructed_requests(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    jsonl_path = tmp_path / "dry_run_requests.jsonl"
    _write_runtime_csv(
        csv_path,
        _minimum_valid_rows() + [_header_row(), _action_row()],
    )

    assert main([str(csv_path), "--require-request", "--output-jsonl", str(jsonl_path)]) == 0

    lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    request = json.loads(lines[0])
    assert request["request_kind"] == "DRY_RUN_MARKET_OPEN"
    assert request["side"] == "BUY"
    assert request["symbol"] == "USDJPYm"


def test_preflight_verification_violations_block_reconciliation(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    _write_runtime_csv(csv_path, [_header_row(), _action_row()])

    result = reconcile_h024_runtime_dry_run_requests(csv_path, require_request=True)

    assert not result.passed
    assert result.rows == 2
    assert result.dry_run_requests == ()
    assert any(
        violation.startswith("preflight verification:")
        for violation in result.violations
    )


def test_reconciler_source_has_no_mt5_trade_api_surface():
    source = Path("scripts/reconcile_h024_runtime_dry_run_requests.py").read_text(
        encoding="utf-8"
    )

    forbidden_tokens = [
        "OrderSend",
        "OrderSendAsync",
        "OrderCheck",
        "CTrade",
        "#include <Trade",
        "MqlTradeRequest",
        "MqlTradeResult",
        "PositionOpen",
        "PositionClose",
        "PositionModify",
    ]

    for token in forbidden_tokens:
        assert token not in source

def test_blocked_rows_with_positive_sizing_diagnostics_do_not_emit_dry_run_requests(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    payload = _intended_action_payload(
        decision="BLOCKED",
        direction="short",
        entry_price="155.821",
        stop_price="158.163",
        stop_distance_price="2.342",
        lots="0.0",
        reason=(
            "BLOCKED:volume_below_min_for_would_open;"
            "WOULD_OPEN:side=short;"
            "source=H024_STATE_OBSERVATION;"
            "mode=log_only_no_execution"
        ),
    )
    _write_runtime_csv(
        csv_path,
        _minimum_valid_rows() + [_header_row(), _action_row(payload=payload)],
    )

    result = reconcile_h024_runtime_dry_run_requests(csv_path, require_request=False)

    assert result.passed
    assert result.intended_action_rows == 1
    assert result.would_open_rows == 0
    assert result.skipped_rows == 1
    assert result.dry_run_requests == ()
    assert result.violations == ()
