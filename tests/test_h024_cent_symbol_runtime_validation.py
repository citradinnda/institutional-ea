
from __future__ import annotations

from pathlib import Path

from scripts.summarize_h024_ea_intended_action_runtime import summarize_runtime_csv
from scripts.verify_h024_ea_preflight_log import (
    CENT_ACCOUNT_ALLOWED_SYMBOLS,
    REQUIRED_COLUMNS,
    verify_h024_ea_preflight_log,
)


def _base_row(event: str, symbol: str, detail: str = "blocked_by_default") -> list[str]:
    values = {
        "generated_at_server": "2026.05.10 06:51:16",
        "schema_version": "h024_ea_log_only_preflight_v2",
        "ea_version": "0.6",
        "source_version": "test",
        "timer_seconds": "2",
        "runtime_mode": "log_only_preflight",
        "run_label": "H024_LOG_ONLY_PREFLIGHT",
        "event": event,
        "kill_switch_blocked": "true",
        "symbol": symbol,
        "account_company": "Exness",
        "account_server": "Exness-MT5Real25",
        "account_currency": "USC",
        "account_balance": "10000.00",
        "account_equity": "10000.00",
        "account_leverage": "2000",
        "account_trade_allowed": "true",
        "account_trade_expert": "true",
        "terminal_connected": "true",
        "terminal_trade_allowed": "true",
        "mql_trade_allowed": "false",
        "bid": "110.000",
        "ask": "110.018",
        "spread_points": "18",
        "volume_min": "0.01",
        "volume_max": "200.00",
        "volume_step": "0.01",
        "stops_level": "0",
        "freeze_level": "0",
        "point": "0.0010000000",
        "digits": "3",
        "detail": detail,
    }
    return [values[column] for column in REQUIRED_COLUMNS]


def _write_raw_csv(path: Path, rows: list[list[str]]) -> None:
    lines = [",".join(REQUIRED_COLUMNS)]
    lines.extend(",".join(row) for row in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _intended_action_payload(symbol: str, normalized_symbol: str) -> list[str]:
    return [
        "h024_intended_action_log_v1",
        "0.6",
        symbol,
        normalized_symbol,
        "H4",
        "NO_ACTION",
        "",
        "0.000",
        "0.000",
        "0.000",
        "0.001",
        "0.100000",
        "10000.00",
        "0.010000",
        "100.00",
        "0.000000",
        "0.00",
        "0.01",
        "200.00",
        "0.01",
        "2",
        "NO_ACTION:no_signal",
    ]


def test_preflight_verifier_accepts_cent_account_symbols_when_requested(tmp_path: Path) -> None:
    path = tmp_path / "cent_runtime.csv"
    _write_raw_csv(
        path,
        [
            _base_row("INIT", "USDJPYc"),
            _base_row("INIT", "XAUUSDc"),
        ],
    )

    result = verify_h024_ea_preflight_log(
        path,
        expected_symbols=CENT_ACCOUNT_ALLOWED_SYMBOLS,
    )

    assert result.passed
    assert result.violations == []


def test_preflight_verifier_default_still_rejects_cent_account_symbols(tmp_path: Path) -> None:
    path = tmp_path / "cent_runtime.csv"
    _write_raw_csv(
        path,
        [
            _base_row("INIT", "USDJPYc"),
            _base_row("INIT", "XAUUSDc"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert "row 2: unexpected symbol 'USDJPYc'" in result.violations
    assert "row 3: unexpected symbol 'XAUUSDc'" in result.violations


def test_intended_action_summary_accepts_cent_account_symbols_when_requested(tmp_path: Path) -> None:
    path = tmp_path / "cent_runtime.csv"
    _write_raw_csv(
        path,
        [
            _base_row("H024_INTENDED_ACTION_HEADER", "USDJPYc", "timestamp"),
            _base_row("H024_INTENDED_ACTION_ROW", "USDJPYc", "2026.05.10 06:51:16")
            + _intended_action_payload("USDJPYc", "USDJPY"),
            _base_row("H024_INTENDED_ACTION_HEADER", "XAUUSDc", "timestamp"),
            _base_row("H024_INTENDED_ACTION_ROW", "XAUUSDc", "2026.05.10 06:51:16")
            + _intended_action_payload("XAUUSDc", "XAUUSD"),
        ],
    )

    lines, violations = summarize_runtime_csv(
        path,
        expected_symbols=CENT_ACCOUNT_ALLOWED_SYMBOLS,
    )

    report = "\n".join(lines)
    assert violations == []
    assert "USDJPYc:" in report
    assert "XAUUSDc:" in report
    assert "normalized: USDJPY" in report
    assert "normalized: XAUUSD" in report
    assert "Verdict: PASS" in report
