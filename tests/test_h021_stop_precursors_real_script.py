import pandas as pd
import pytest

from quantcore.backtest.fill_engine import Fill
from quantcore.strategy.h017 import H017Result
from scripts.diagnose_h021_stop_precursors_real import (
    build_decision_contexts,
    enrich_fills_with_decision_context,
    format_stop_precursor_table,
    summarize_records_by_fields,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _panel(value: float, *, index: pd.DatetimeIndex, columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(value, index=index, columns=columns)


def _h017_result_for_xauusd_buy() -> H017Result:
    index = pd.DatetimeIndex(
        [_utc("2024-01-01 00:00"), _utc("2024-01-01 04:00"), _utc("2024-01-01 08:00")]
    )
    columns = ["USDJPY", "XAUUSD"]

    positions = _panel(0.0, index=index, columns=columns)
    positions.at[index[0], "XAUUSD"] = 0.01

    stops_long = _panel(0.0, index=index, columns=columns)
    stops_long.at[index[0], "XAUUSD"] = 1990.0

    stops_short = _panel(0.0, index=index, columns=columns)

    return H017Result(
        positions=positions,
        stops_long=stops_long,
        stops_short=stops_short,
        signals=_panel(0.0, index=index, columns=columns),
        vol_multipliers=_panel(1.0, index=index, columns=columns),
        heat_multipliers=_panel(1.0, index=index, columns=columns),
        heat_pre=_panel(0.0, index=index, columns=columns),
        heat_post=_panel(0.0, index=index, columns=columns),
        heat_binding=_panel(False, index=index, columns=columns),
    )


def _xauusd_h4() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [_utc("2024-01-01 00:00"), _utc("2024-01-01 04:00"), _utc("2024-01-01 08:00")]
    )
    return pd.DataFrame(
        {
            "open": [1995.0, 2000.0, 2005.0],
            "high": [2000.0, 2010.0, 2015.0],
            "low": [1980.0, 1990.0, 1995.0],
            "close": [1998.0, 2004.0, 2006.0],
        },
        index=index,
    )


def _fill(*, exit_reason: str, pnl_quote: float) -> Fill:
    return Fill(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-01 04:00"),
        entry_price=2000.30,
        exit_time_utc=_utc("2024-01-01 08:00"),
        exit_price=2005.0,
        lots=0.10,
        pnl_quote=pnl_quote,
        commission=1.0,
        slippage=0.0,
        exit_reason=exit_reason,
    )


def test_build_decision_contexts_reconstructs_accepted_entry_context():
    h017 = _h017_result_for_xauusd_buy()

    contexts = build_decision_contexts(
        h017_result=h017,
        h4_by_symbol={"XAUUSD": _xauusd_h4()},
        accepted_entry_times=[_utc("2024-01-01 04:00")],
    )

    key = ("XAUUSD", "buy", _utc("2024-01-01 04:00"))
    assert key in contexts

    context = contexts[key]
    assert context.decision_time == _utc("2024-01-01 00:00")
    assert context.entry_raw_price == pytest.approx(2000.0)
    assert context.stop_price == pytest.approx(1990.0)
    assert context.raw_stop_distance == pytest.approx(10.0)
    assert context.stop_distance_spread_multiple == pytest.approx(10.0 / 0.30)


def test_enrich_fills_adds_decision_time_buckets_and_after_cost_pnl():
    h017 = _h017_result_for_xauusd_buy()
    contexts = build_decision_contexts(
        h017_result=h017,
        h4_by_symbol={"XAUUSD": _xauusd_h4()},
        accepted_entry_times=[_utc("2024-01-01 04:00")],
    )

    records = enrich_fills_with_decision_context(
        [_fill(exit_reason="stop", pnl_quote=-25.0)],
        contexts,
        starting_equity_usd=10000.0,
    )

    assert len(records) == 1
    record = records[0]
    assert record.decision_hour_utc == "00"
    assert record.entry_hour_utc == "04"
    assert record.stop_distance_spread_bucket == "20-50x"
    assert record.estimated_notional_usd == pytest.approx(2000.0 * 100.0 * 0.10)
    assert record.estimated_gross_leverage == pytest.approx(2.0)
    assert record.estimated_gross_leverage_bucket == "1-3x"
    assert record.pnl_usd == pytest.approx(-26.0)


def test_summarize_records_by_fields_reports_stop_rate_and_profit_factor():
    h017 = _h017_result_for_xauusd_buy()
    contexts = build_decision_contexts(
        h017_result=h017,
        h4_by_symbol={"XAUUSD": _xauusd_h4()},
        accepted_entry_times=[_utc("2024-01-01 04:00")],
    )
    records = enrich_fills_with_decision_context(
        [
            _fill(exit_reason="stop", pnl_quote=-25.0),
            _fill(exit_reason="signal_flip", pnl_quote=11.0),
        ],
        contexts,
        starting_equity_usd=10000.0,
    )

    rows = summarize_records_by_fields(records, group_fields=("stop_distance_spread_bucket",))

    assert len(rows) == 1
    row = rows[0]
    assert row.group == (("stop_distance_spread_bucket", "20-50x"),)
    assert row.fill_count == 2
    assert row.stop_count == 1
    assert row.stop_rate == pytest.approx(0.5)
    assert row.total_pnl_usd == pytest.approx(-16.0)
    assert row.gross_profit_usd == pytest.approx(10.0)
    assert row.gross_loss_usd == pytest.approx(-26.0)
    assert row.profit_factor == pytest.approx(10.0 / 26.0)


def test_summarize_records_rejects_unknown_group_field():
    with pytest.raises(ValueError, match="unsupported group field"):
        summarize_records_by_fields([], group_fields=("weekday",))


def test_format_stop_precursor_table_keeps_warning_visible():
    h017 = _h017_result_for_xauusd_buy()
    contexts = build_decision_contexts(
        h017_result=h017,
        h4_by_symbol={"XAUUSD": _xauusd_h4()},
        accepted_entry_times=[_utc("2024-01-01 04:00")],
    )
    records = enrich_fills_with_decision_context(
        [_fill(exit_reason="stop", pnl_quote=-25.0)],
        contexts,
        starting_equity_usd=10000.0,
    )
    rows = summarize_records_by_fields(records, group_fields=("decision_hour_utc",))

    table = format_stop_precursor_table(rows, title="By decision hour UTC")

    assert "By decision hour UTC" in table
    assert "decision_hour_utc=00" in table
    assert "stop_rate" in table
    assert "-26.00" in table
