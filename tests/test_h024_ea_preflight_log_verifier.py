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
        "2026.05.09 22:00:00,h024_ea_log_only_preflight_v2,0.3,manual,1,"
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


def test_verify_h024_ea_preflight_log_rejects_would_open_intent_rows(tmp_path: Path) -> None:
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
    assert any("may only emit NO_ACTION intent rows" in item for item in result.violations)


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
