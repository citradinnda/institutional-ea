from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

from scripts.verify_h024_ea_state_observation_parity_real import (
    BOOL_FIELDS,
    FLOAT_FIELDS,
    INT_FIELDS,
    compute_h024_state_for_closed_bar,
    mt5_server_time_to_utc,
    parse_h024_state_detail,
    verify_h024_ea_state_observation_parity,
)


def _synthetic_h4() -> pd.DataFrame:
    index = pd.date_range("2026-05-01 00:00:00+00:00", periods=12, freq="4h")
    return pd.DataFrame(
        {
            "open": [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0],
            "high": [101.0, 102.5, 103.0, 104.5, 105.0, 106.5, 107.0, 108.5, 109.0, 110.5, 111.0, 112.5],
            "low": [99.0, 100.5, 101.0, 102.5, 103.0, 104.5, 105.0, 106.5, 107.0, 108.5, 109.0, 110.5],
            "close": [100.5, 101.5, 102.5, 103.5, 104.5, 105.5, 106.5, 107.5, 108.5, 109.5, 110.5, 112.0],
            "volume": [10.0] * 12,
        },
        index=index,
    )


def _format_detail(state: dict[str, float | bool | int], closed_h4_time: str) -> str:
    parts = [f"closed_h4_time={closed_h4_time}"]
    for field in INT_FIELDS:
        parts.append(f"{field}={state[field]}")
    for field in FLOAT_FIELDS:
        parts.append(f"{field}={float(state[field]):.10f}")
    for field in BOOL_FIELDS:
        parts.append(f"{field}={'true' if state[field] else 'false'}")
    parts.append("action=NO_ACTION:state_observation_only")
    return ";".join(parts)


def _write_log(path: Path, *, detail: str, symbol: str = "USDJPYm") -> None:
    fieldnames = ["event", "symbol", "detail"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "event": "H024_STATE_OBSERVATION",
                "symbol": symbol,
                "detail": detail,
            }
        )


def test_parse_h024_state_detail_rejects_unavailable_rows():
    try:
        parse_h024_state_detail("unavailable:not_enough_bars")
    except ValueError as exc:
        assert "state observation unavailable" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_mt5_server_time_to_utc_uses_broker_timezone():
    assert str(mt5_server_time_to_utc("2026.05.01 03:00:00")) == "2026-05-01 00:00:00+00:00"


def test_compute_h024_state_for_closed_bar_uses_bounded_warmup():
    bars = _synthetic_h4()
    state = compute_h024_state_for_closed_bar(
        bars,
        pd.Timestamp("2026-05-01 20:00:00+00:00"),
        h4_warmup_bars=6,
    )

    assert state["h4_warmup_bars"] == 6
    assert state["slow_window"] == 5
    assert state["slope_lag"] == 2
    assert state["atr_window"] == 3
    assert state["pullback_window"] == 3
    assert isinstance(state["trend_up"], bool)
    assert isinstance(state["long_signal_observed"], bool)


def test_verify_h024_ea_state_observation_parity_passes_on_matching_synthetic_log(tmp_path):
    bars = _synthetic_h4()
    closed_utc = pd.Timestamp("2026-05-01 20:00:00+00:00")
    state = compute_h024_state_for_closed_bar(
        bars,
        closed_utc,
        h4_warmup_bars=6,
    )
    detail = _format_detail(state, "2026.05.01 23:00:00")
    log_path = tmp_path / "h024_ea_log_only_preflight.csv"
    _write_log(log_path, detail=detail)

    result = verify_h024_ea_state_observation_parity(
        log_path,
        h4_bars_by_symbol={"USDJPY": bars},
    )

    assert result.passed
    assert result.rows_checked == 1
    assert result.comparisons == len(INT_FIELDS) + len(FLOAT_FIELDS) + len(BOOL_FIELDS)


def test_verify_h024_ea_state_observation_parity_fails_on_numeric_mismatch(tmp_path):
    bars = _synthetic_h4()
    closed_utc = pd.Timestamp("2026-05-01 20:00:00+00:00")
    state = compute_h024_state_for_closed_bar(
        bars,
        closed_utc,
        h4_warmup_bars=6,
    )
    detail = _format_detail(state, "2026.05.01 23:00:00").replace(
        "slow_window=5",
        "slow_window=4",
    )
    log_path = tmp_path / "h024_ea_log_only_preflight.csv"
    _write_log(log_path, detail=detail)

    result = verify_h024_ea_state_observation_parity(
        log_path,
        h4_bars_by_symbol={"USDJPY": bars},
    )

    assert not result.passed
    assert any("slow_window" in violation for violation in result.violations)
