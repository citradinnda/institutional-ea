from pathlib import Path

from scripts.summarize_h024_ea_intended_action_runtime import summarize_runtime_csv


BASE_HEADER = [
    "generated_at_server",
    "schema_version",
    "ea_version",
    "source_version",
    "timer_seconds",
    "runtime_mode",
    "run_label",
    "event",
    "kill_switch_blocked",
    "symbol",
    "account_company",
    "account_server",
    "account_currency",
    "account_balance",
    "account_equity",
    "account_leverage",
    "account_trade_allowed",
    "account_trade_expert",
    "terminal_connected",
    "terminal_trade_allowed",
    "mql_trade_allowed",
    "bid",
    "ask",
    "spread_points",
    "volume_min",
    "volume_max",
    "volume_step",
    "stops_level",
    "freeze_level",
    "point",
    "digits",
    "detail",
]


INTENDED_HEADER_PAYLOAD = [
    "schema_version",
    "ea_version",
    "symbol",
    "normalized_symbol",
    "timeframe",
    "decision",
    "direction",
    "entry_price",
    "stop_price",
    "stop_distance_price",
    "tick_size",
    "tick_value_usd_per_lot",
    "account_balance_usd",
    "risk_fraction",
    "risk_usd",
    "raw_lots",
    "lots",
    "min_volume",
    "max_volume",
    "volume_step",
    "volume_digits",
    "reason",
]


def base_row(event: str, symbol: str, detail: str) -> list[str]:
    return [
        "2026.05.10 06:51:16",
        "h024_ea_log_only_preflight_v2",
        "0.6",
        "manual",
        "1",
        "log_only_preflight",
        "H024_LOG_ONLY_PREFLIGHT",
        event,
        "true",
        symbol,
        "Exness Technologies Ltd",
        "Exness-MT5Trial6",
        "USD",
        "1246.45",
        "1246.45",
        "2000",
        "true",
        "true",
        "true",
        "false",
        "false",
        "156.676",
        "156.694",
        "18",
        "0.01",
        "300.00",
        "0.01",
        "0",
        "0",
        "0.0010000000",
        "3",
        detail,
    ]


def intended_row_payload(
    symbol: str,
    normalized_symbol: str,
    decision: str = "NO_ACTION",
    direction: str = "",
) -> list[str]:
    return [
        "h024_intended_action_log_v1",
        "0.6",
        symbol,
        normalized_symbol,
        "H4",
        decision,
        direction,
        "156.6760000000" if decision == "WOULD_OPEN" else "0.0000000000",
        "156.1760000000" if decision == "WOULD_OPEN" else "0.0000000000",
        "0.5000000000" if decision == "WOULD_OPEN" else "0.0000000000",
        "0.0010000000",
        "0.6381865292",
        "1246.45",
        "0.01000000",
        "12.46",
        "0.2500000000" if decision == "WOULD_OPEN" else "0.0000000000",
        "0.2500000000" if decision == "WOULD_OPEN" else "0.0000000000",
        "0.0100000000",
        "300.0000000000",
        "0.0100000000",
        "2",
        f"{decision}:test_reason;closed_h4_time=2026.05.08 16:00:00;mode=log_only_no_execution",
    ]


def write_csv(path: Path, rows: list[list[str]]) -> None:
    path.write_text("\n".join(",".join(row) for row in rows) + "\n", encoding="utf-8")


def both_symbol_rows(
    usd_payload: list[str] | None = None,
    xau_payload: list[str] | None = None,
) -> list[list[str]]:
    return [
        BASE_HEADER,
        base_row("H024_INTENDED_ACTION_HEADER", "USDJPYm", "timestamp") + INTENDED_HEADER_PAYLOAD,
        base_row("H024_INTENDED_ACTION_ROW", "USDJPYm", "2026.05.10 06:51:16")
        + (usd_payload or intended_row_payload("USDJPYm", "USDJPY")),
        base_row("H024_INTENDED_ACTION_HEADER", "XAUUSDm", "timestamp") + INTENDED_HEADER_PAYLOAD,
        base_row("H024_INTENDED_ACTION_ROW", "XAUUSDm", "2026.05.10 06:51:16")
        + (xau_payload or intended_row_payload("XAUUSDm", "XAUUSD")),
    ]


def test_summarize_h024_intended_action_runtime_csv_passes_for_both_symbols(tmp_path):
    csv_path = tmp_path / "runtime.csv"
    write_csv(csv_path, both_symbol_rows())

    lines, violations = summarize_runtime_csv(csv_path)

    assert violations == []
    report = "\n".join(lines)
    assert "USDJPYm:" in report
    assert "XAUUSDm:" in report
    assert "NO_ACTION: 1" in report
    assert "Verdict: PASS" in report


def test_summarize_h024_intended_action_runtime_csv_fails_when_symbol_missing(tmp_path):
    csv_path = tmp_path / "runtime_missing_symbol.csv"
    rows = [
        BASE_HEADER,
        base_row("H024_INTENDED_ACTION_HEADER", "USDJPYm", "timestamp") + INTENDED_HEADER_PAYLOAD,
        base_row("H024_INTENDED_ACTION_ROW", "USDJPYm", "2026.05.10 06:51:16")
        + intended_row_payload("USDJPYm", "USDJPY"),
    ]
    write_csv(csv_path, rows)

    _lines, violations = summarize_runtime_csv(csv_path)

    assert "missing intended-action header for XAUUSDm" in violations
    assert "missing intended-action rows for XAUUSDm" in violations


def test_require_would_open_fails_when_runtime_csv_has_only_no_action(tmp_path):
    csv_path = tmp_path / "runtime_no_action_only.csv"
    write_csv(csv_path, both_symbol_rows())

    lines, violations = summarize_runtime_csv(csv_path, require_would_open=True)

    assert "missing required runtime WOULD_OPEN intended-action row" in violations
    report = "\n".join(lines)
    assert "Required WOULD_OPEN rows: at least 1" in report
    assert "Observed WOULD_OPEN rows: 0" in report
    assert "Verdict: FAIL" in report


def test_require_would_open_passes_when_runtime_csv_has_valid_would_open(tmp_path):
    csv_path = tmp_path / "runtime_with_would_open.csv"
    write_csv(
        csv_path,
        both_symbol_rows(
            usd_payload=intended_row_payload("USDJPYm", "USDJPY", decision="WOULD_OPEN", direction="long")
        ),
    )

    lines, violations = summarize_runtime_csv(csv_path, require_would_open=True)

    assert violations == []
    report = "\n".join(lines)
    assert "Observed WOULD_OPEN rows: 1" in report
    assert "WOULD_OPEN: 1" in report
    assert "Verdict: PASS" in report


def test_would_open_requires_direction(tmp_path):
    csv_path = tmp_path / "runtime_with_bad_would_open.csv"
    write_csv(
        csv_path,
        both_symbol_rows(
            usd_payload=intended_row_payload("USDJPYm", "USDJPY", decision="WOULD_OPEN", direction="")
        ),
    )

    _lines, violations = summarize_runtime_csv(csv_path, require_would_open=True)

    assert "row 3: WOULD_OPEN requires long or short direction" in violations