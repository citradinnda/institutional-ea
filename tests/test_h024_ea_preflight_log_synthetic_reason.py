import csv
from pathlib import Path

from scripts.verify_h024_ea_preflight_log import (
    INTENDED_ACTION_LOG_ROW_FIELDS,
    REQUIRED_COLUMNS,
    verify_h024_ea_preflight_log,
)


def _base_values(event: str, symbol: str, detail: str) -> list[str]:
    row = {column: "" for column in REQUIRED_COLUMNS}
    row.update(
        {
            "generated_at_server": "2026.05.11 07:25:44",
            "schema_version": "h024_ea_log_only_preflight_v2",
            "ea_version": "0.6",
            "source_version": "1",
            "timer_seconds": "1",
            "runtime_mode": "log_only_preflight",
            "run_label": "H024_LOG_ONLY_PREFLIGHT",
            "event": event,
            "detail": detail,
            "kill_switch_blocked": "true",
            "symbol": symbol,
            "account_company": "Exness Technologies Ltd",
            "account_server": "Exness-MT5Trial6",
            "account_currency": "USD",
            "account_balance": "10000.00",
            "account_equity": "10000.00",
            "account_leverage": "2000",
            "account_trade_allowed": "true",
            "account_trade_expert": "true",
            "terminal_connected": "true",
            "terminal_trade_allowed": "false",
            "mql_trade_allowed": "false",
            "bid": "4930.048",
            "ask": "4930.328",
            "spread_points": "280",
            "volume_min": "0.01",
            "volume_max": "200.00",
            "volume_step": "0.01",
            "stops_level": "0",
            "freeze_level": "0",
            "point": "0.0010000000",
            "digits": "3",
        }
    )
    return [row[column] for column in REQUIRED_COLUMNS]


def _intended_action_payload(reason: str) -> list[str]:
    values = {
        "timestamp": "2026.05.11 07:25:44",
        "schema_version": "h024_intended_action_log_v1",
        "ea_version": "0.6",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "timeframe": "H4",
        "decision": "WOULD_OPEN",
        "direction": "short",
        "entry_price": "4930.0480000000",
        "stop_price": "5019.1630000000",
        "stop_distance_price": "89.1150000000",
        "tick_size": "0.0010000000",
        "tick_value_usd_per_lot": "0.1000000000",
        "account_balance_usd": "10000.00",
        "risk_fraction": "0.01000000",
        "risk_usd": "100.00",
        "raw_lots": "0.0112214554",
        "lots": "0.0100000000",
        "min_volume": "0.0100000000",
        "max_volume": "200.0000000000",
        "volume_step": "0.0100000000",
        "volume_digits": "2",
        "reason": reason,
    }
    return [values[field] for field in INTENDED_ACTION_LOG_ROW_FIELDS]


def _write_log(path: Path, intended_reason: str) -> None:
    rows = [
        _base_values("INIT", "USDJPYm", "blocked_by_default"),
        _base_values("INIT", "XAUUSDm", "blocked_by_default"),
        _base_values("H024_INTENDED_ACTION_HEADER", "XAUUSDm", "timestamp")
        + INTENDED_ACTION_LOG_ROW_FIELDS,
        _base_values("H024_INTENDED_ACTION_ROW", "XAUUSDm", "2026.05.11 07:25:44")
        + _intended_action_payload(intended_reason),
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(REQUIRED_COLUMNS)
        writer.writerows(rows)


def test_verify_h024_ea_preflight_log_accepts_complete_synthetic_balance_reason(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    reason = (
        "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;"
        "source=H024_STATE_OBSERVATION;mode=log_only_no_execution;"
        "balance_source=synthetic_research_only;synthetic_balance=10000.00;real_account_balance=0.00"
    )
    _write_log(path, reason)

    result = verify_h024_ea_preflight_log(path)

    assert result.passed
    assert result.violations == []


def test_verify_h024_ea_preflight_log_rejects_synthetic_balance_reason_without_real_balance(
    tmp_path: Path,
) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    reason = (
        "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;"
        "source=H024_STATE_OBSERVATION;mode=log_only_no_execution;"
        "balance_source=synthetic_research_only;synthetic_balance=10000.00"
    )
    _write_log(path, reason)

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any(
        "synthetic balance intended-action reason missing required fragments" in violation
        and "real_account_balance=" in violation
        for violation in result.violations
    )
