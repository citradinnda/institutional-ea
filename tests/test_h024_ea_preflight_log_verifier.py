from pathlib import Path

from scripts.verify_h024_ea_preflight_log import verify_h024_ea_preflight_log


HEADER = (
    "generated_at_server,schema_version,ea_version,source_version,timer_seconds,"
    "runtime_mode,run_label,event,kill_switch_blocked,symbol,"
    "account_company,account_server,account_currency,account_balance,"
    "account_equity,account_leverage,account_trade_allowed,account_trade_expert,"
    "terminal_connected,terminal_trade_allowed,mql_trade_allowed,bid,ask,"
    "spread_points,volume_min,volume_max,volume_step,stops_level,freeze_level,"
    "point,digits,detail\n"
)


def write_log(path: Path, rows: list[str]) -> None:
    path.write_text(HEADER + "".join(rows), encoding="utf-8")


def valid_row(
    event: str = "INIT",
    symbol: str = "USDJPYm",
    kill_switch: str = "true",
    detail: str = "blocked_by_default",
) -> str:
    return (
        "2026.05.09 22:00:00,h024_ea_log_only_preflight_v2,0.6,manual,1,"
        f"log_only_preflight,H024_LOG_ONLY_PREFLIGHT,{event},{kill_switch},{symbol},"
        "Exness Technologies Ltd,Exness-MT5Trial6,USD,1246.45,1246.45,2000,"
        "true,true,true,false,false,156.676,156.694,18,0.01,300.00,0.01,0,0,"
        f"0.0010000000,3,{detail}\n"
    )


def test_verify_h024_ea_preflight_log_accepts_valid_log(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(path, [valid_row(symbol="USDJPYm"), valid_row(symbol="XAUUSDm")])

    result = verify_h024_ea_preflight_log(path)

    assert result.passed
    assert result.rows == 2
    assert result.violations == []


def test_verify_h024_ea_preflight_log_rejects_stale_unversioned_log(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    stale_header = (
        "generated_at_server,run_label,event,kill_switch_blocked,symbol,"
        "account_company,account_server,account_currency,account_balance,"
        "account_equity,account_leverage,account_trade_allowed,account_trade_expert,"
        "terminal_connected,terminal_trade_allowed,mql_trade_allowed,bid,ask,"
        "spread_points,volume_min,volume_max,volume_step,stops_level,freeze_level,"
        "point,digits,detail\n"
    )
    stale_row = (
        "2026.05.09 22:00:00,H024_LOG_ONLY_PREFLIGHT,INIT,true,USDJPYm,"
        "Exness Technologies Ltd,Exness-MT5Trial6,USD,1246.45,1246.45,2000,"
        "true,true,true,false,false,156.676,156.694,18,0.01,300.00,0.01,0,0,"
        "0.0010000000,3,blocked_by_default\n"
    )
    path.write_text(stale_header + stale_row, encoding="utf-8")

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("missing columns" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_rejects_wrong_schema_version(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(path, [valid_row(symbol="USDJPYm").replace("h024_ea_log_only_preflight_v2", "v1", 1), valid_row(symbol="XAUUSDm")])

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("unexpected schema_version" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_accepts_market_state_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="MARKET_STATE", symbol="USDJPYm", detail="H4:time=2026.05.09 20:00:00;open=156.000;high=157.000;low=155.000;close=156.500;tick_volume=10|M1:time=2026.05.09 23:59:00;open=156.400;high=156.600;low=156.300;close=156.500;tick_volume=5"),
            valid_row(symbol="XAUUSDm"),
            valid_row(event="MARKET_STATE", symbol="XAUUSDm", detail="H4:unavailable|M1:unavailable"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert result.passed
    assert result.rows == 4
    assert result.violations == []


def test_verify_h024_ea_preflight_log_rejects_bad_market_state_detail(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="MARKET_STATE", symbol="USDJPYm", detail="H4:unavailable"),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("MARKET_STATE detail must include H4 and M1 observations" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_accepts_bar_observation_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(
                event="BAR_OBSERVATION",
                symbol="USDJPYm",
                detail=(
                    "H4_closed:time=2026.05.09 20:00:00;open=156.000;high=157.000;"
                    "low=155.000;close=156.500;tick_volume=10|"
                    "M1_closed:time=2026.05.09 23:59:00;open=156.400;high=156.600;"
                    "low=156.300;close=156.500;tick_volume=5"
                ),
            ),
            valid_row(symbol="XAUUSDm"),
            valid_row(
                event="BAR_OBSERVATION",
                symbol="XAUUSDm",
                detail="H4_closed:unavailable|M1_closed:unavailable",
            ),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert result.passed


def test_verify_h024_ea_preflight_log_rejects_bad_bar_observation_detail(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="BAR_OBSERVATION", symbol="USDJPYm", detail="H4:unavailable|M1:unavailable"),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any(
        "BAR_OBSERVATION detail must include closed H4 and M1 observations" in item
        for item in result.violations
    )


def test_verify_h024_ea_preflight_log_accepts_h024_state_observation_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    detail = (
        "closed_h4_time=2026.05.08 16:00:00;h4_warmup_bars=256;slow_window=5;slope_lag=2;atr_window=3;"
        "pullback_window=3;slow_ma=1.0000000000;slow_ma_lag=0.9000000000;atr=0.1000000000;"
        "previous_atr=0.1000000000;slope=0.1000000000;slope_threshold=0.0050000000;"
        "trend_up=true;trend_down=false;previous_bearish=true;previous_bullish=false;"
        "recent_high_before_signal=1.2000000000;recent_low_before_signal=0.8000000000;"
        "long_pullback_depth_atr=1.0000000000;short_pullback_depth_atr=0.5000000000;"
        "long_pullback_ok=true;short_pullback_ok=true;long_resumption=true;short_resumption=false;"
        "long_signal_observed=true;short_signal_observed=false;action=NO_ACTION:state_observation_only"
    )
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="H024_STATE_OBSERVATION", symbol="USDJPYm", detail=detail),
            valid_row(symbol="XAUUSDm"),
            valid_row(event="H024_STATE_OBSERVATION", symbol="XAUUSDm", detail="unavailable:insufficient_h4_warmup_bars"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert result.passed


def test_verify_h024_ea_preflight_log_rejects_bad_h024_state_observation_detail(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="H024_STATE_OBSERVATION", symbol="USDJPYm", detail="closed_h4_time=2026.05.08 16:00:00"),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any(
        "H024_STATE_OBSERVATION detail must include frozen H024 state fields" in item
        for item in result.violations
    )


def test_verify_h024_ea_preflight_log_accepts_no_action_intent_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="INTENT", symbol="USDJPYm", detail="NO_ACTION:kill_switch_blocked"),
            valid_row(symbol="XAUUSDm"),
            valid_row(event="INTENT", symbol="XAUUSDm", detail="NO_ACTION:kill_switch_blocked"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert result.passed
    assert result.rows == 4
    assert result.violations == []


def test_verify_h024_ea_preflight_log_accepts_constrained_would_open_intent_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(
                event="INTENT",
                symbol="USDJPYm",
                detail=(
                    "WOULD_OPEN:side=long;closed_h4_time=2026.05.08 16:00:00;"
                    "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
                ),
            ),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert result.passed


def test_verify_h024_ea_preflight_log_rejects_unconstrained_would_open_intent_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="INTENT", symbol="USDJPYm", detail="WOULD_OPEN:dry_run_only"),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("WOULD_OPEN intent rows must be log-only" in item for item in result.violations)



def test_verify_h024_ea_preflight_log_accepts_constrained_short_would_open_intent_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(
                event="INTENT",
                symbol="XAUUSDm",
                detail=(
                    "WOULD_OPEN:side=short;closed_h4_time=2026.05.08 16:00:00;"
                    "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
                ),
            ),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert result.passed
    assert result.violations == []


def test_verify_h024_ea_preflight_log_rejects_would_open_without_side(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(
                event="INTENT",
                symbol="USDJPYm",
                detail=(
                    "WOULD_OPEN:closed_h4_time=2026.05.08 16:00:00;"
                    "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
                ),
            ),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("WOULD_OPEN intent rows must include side=long or side=short" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_rejects_unblocked_would_open(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(
                event="INTENT",
                symbol="USDJPYm",
                kill_switch="false",
                detail=(
                    "WOULD_OPEN:side=long;closed_h4_time=2026.05.08 16:00:00;"
                    "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
                ),
            ),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("WOULD_OPEN intent rows require kill_switch_blocked=true" in item for item in result.violations)
    assert any("kill_switch_blocked must be true" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_rejects_blocked_intent_rows(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="INTENT", symbol="USDJPYm", detail="BLOCKED:strategy_conflict_log_only"),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("EA runtime preflight may only emit NO_ACTION or constrained WOULD_OPEN intent rows" in item for item in result.violations)

def test_verify_h024_ea_preflight_log_rejects_unknown_intent_action(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(
        path,
        [
            valid_row(symbol="USDJPYm"),
            valid_row(event="INTENT", symbol="USDJPYm", detail="SEND_ORDER:forbidden"),
            valid_row(symbol="XAUUSDm"),
        ],
    )

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("unexpected intent action" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_requires_existing_file(tmp_path: Path) -> None:
    result = verify_h024_ea_preflight_log(tmp_path / "missing.csv")

    assert not result.passed
    assert result.rows == 0
    assert "missing log file" in result.violations[0]


def test_verify_h024_ea_preflight_log_rejects_missing_init(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(path, [valid_row("TICK", "USDJPYm"), valid_row("TICK", "XAUUSDm")])

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert "log must include at least one INIT row" in result.violations


def test_verify_h024_ea_preflight_log_rejects_unblocked_kill_switch(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(path, [valid_row(symbol="USDJPYm", kill_switch="false"), valid_row(symbol="XAUUSDm")])

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("kill_switch_blocked must be true" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_rejects_unexpected_symbol(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(path, [valid_row(symbol="EURUSDm"), valid_row(symbol="XAUUSDm")])

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("unexpected symbol" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_rejects_bad_numeric_field(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    row = valid_row(symbol="USDJPYm").replace(",2000,", ",not_int,", 1)
    write_log(path, [row, valid_row(symbol="XAUUSDm")])

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert any("account_leverage must be an integer" in item for item in result.violations)


def test_verify_h024_ea_preflight_log_requires_both_symbols(tmp_path: Path) -> None:
    path = tmp_path / "h024_ea_log_only_preflight.csv"
    write_log(path, [valid_row(symbol="USDJPYm")])

    result = verify_h024_ea_preflight_log(path)

    assert not result.passed
    assert "log missing required symbols: ['XAUUSDm']" in result.violations


def _run_preflight_verifier_for_intended_action_test(path):
    import importlib

    module = importlib.import_module("scripts.verify_h024_ea_preflight_log")

    for name in (
        "verify_h024_ea_preflight_log",
        "verify_preflight_log",
        "verify_log",
        "verify",
    ):
        verifier = getattr(module, name, None)
        if callable(verifier):
            try:
                return verifier(path)
            except TypeError:
                return verifier(str(path))

    main = getattr(module, "main", None)
    if callable(main):
        return main([str(path)])

    raise AssertionError("Could not find callable verifier in scripts.verify_h024_ea_preflight_log")


def _verifier_violations_for_intended_action_test(result):
    if isinstance(result, int):
        return [] if result == 0 else [f"verifier returned exit code {result}"]
    if hasattr(result, "violations"):
        return list(result.violations)
    if hasattr(result, "errors"):
        return list(result.errors)
    if isinstance(result, (list, tuple)):
        return list(result)
    return []


def _intended_action_base_columns_for_test():
    return [
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


def _intended_action_base_values_for_test(event, symbol, detail):
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


def _write_intended_action_preflight_log_for_test(path, *, schema_version="h024_intended_action_log_v1"):
    header = _intended_action_base_columns_for_test()
    intended_header_payload = [
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
    intended_row_payload = [
        schema_version,
        "0.6",
        "USDJPYm",
        "USDJPY",
        "H4",
        "NO_ACTION",
        "",
        "0.0000000000",
        "0.0000000000",
        "0.0000000000",
        "0.0010000000",
        "0.6381865292",
        "1246.45",
        "0.01000000",
        "12.46",
        "0.0000000000",
        "0.0000000000",
        "0.0100000000",
        "300.0000000000",
        "0.0100000000",
        "2",
        "NO_ACTION:strategy_no_signal;closed_h4_time=2026.05.08 16:00:00;mode=log_only_no_execution",
    ]

    rows = [
        header,
        _intended_action_base_values_for_test("INIT", "USDJPYm", "blocked_by_default"),
        _intended_action_base_values_for_test("INIT", "XAUUSDm", "blocked_by_default"),
        _intended_action_base_values_for_test("H024_INTENDED_ACTION_HEADER", "USDJPYm", "timestamp")
        + intended_header_payload,
        _intended_action_base_values_for_test("H024_INTENDED_ACTION_ROW", "USDJPYm", "2026.05.10 06:51:16")
        + intended_row_payload,
    ]

    path.write_text("\n".join(",".join(row) for row in rows) + "\n", encoding="utf-8")


def test_h024_preflight_verifier_accepts_runtime_intended_action_rows(tmp_path):
    path = tmp_path / "h024_preflight_with_intended_action.csv"
    _write_intended_action_preflight_log_for_test(path)

    result = _run_preflight_verifier_for_intended_action_test(path)

    assert _verifier_violations_for_intended_action_test(result) == []


def test_h024_preflight_verifier_rejects_bad_intended_action_schema(tmp_path):
    path = tmp_path / "h024_preflight_with_bad_intended_action_schema.csv"
    _write_intended_action_preflight_log_for_test(path, schema_version="bad_schema")

    result = _run_preflight_verifier_for_intended_action_test(path)
    violations = _verifier_violations_for_intended_action_test(result)

    assert any("schema_version" in violation for violation in violations)
