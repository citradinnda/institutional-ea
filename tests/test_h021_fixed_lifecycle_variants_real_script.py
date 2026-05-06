import pandas as pd
import pytest

from quantcore.backtest.fill_engine import Fill
from quantcore.strategy.h017 import H017Result
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    H021FixedLifecycleBacktestResult,
    backtest_fixed_lifecycle_from_result,
    format_group_summary_table,
    format_lifecycle_summary_table,
    summarize_chronological_halves,
    summarize_chronological_thirds,
    summarize_fills_by_field,
    summarize_lifecycle_backtest,
)


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _h4() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-01 00:00"),
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 12:00"),
            _utc("2024-01-01 16:00"),
        ]
    )
    return pd.DataFrame(
        {
            "open": [100.0, 102.0, 104.0, 106.0, 108.0],
            "high": [101.0, 103.0, 105.0, 107.0, 109.0],
            "low": [99.0, 101.0, 103.0, 105.0, 107.0],
            "close": [100.5, 102.5, 104.5, 106.5, 108.5],
        },
        index=index,
    )


def _m1_no_stop() -> pd.DataFrame:
    index = pd.DatetimeIndex(
        [
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 05:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 09:00"),
            _utc("2024-01-01 12:00"),
            _utc("2024-01-01 13:00"),
        ]
    )
    return pd.DataFrame(
        {
            "open": [102.0, 102.2, 104.0, 104.2, 106.0, 106.2],
            "high": [103.0, 103.2, 105.0, 105.2, 107.0, 107.2],
            "low": [101.0, 101.2, 103.0, 103.2, 105.0, 105.2],
            "close": [102.5, 102.7, 104.5, 104.7, 106.5, 106.7],
        },
        index=index,
    )


def _h017_result() -> H017Result:
    index = _h4().index
    columns = ["USDJPY", "XAUUSD"]

    positions = pd.DataFrame(0.0, index=index, columns=columns)
    positions.at[_utc("2024-01-01 00:00"), "XAUUSD"] = 0.01
    positions.at[_utc("2024-01-01 04:00"), "XAUUSD"] = 0.01
    positions.at[_utc("2024-01-01 08:00"), "XAUUSD"] = 0.01

    stops_long = pd.DataFrame(90.0, index=index, columns=columns)
    stops_short = pd.DataFrame(120.0, index=index, columns=columns)
    zeros = pd.DataFrame(0.0, index=index, columns=columns)

    return H017Result(
        positions=positions,
        stops_long=stops_long,
        stops_short=stops_short,
        signals=zeros,
        vol_multipliers=zeros,
        heat_multipliers=zeros,
        heat_pre=zeros,
        heat_post=zeros,
        heat_binding=zeros,
    )


def _fill(
    *,
    symbol: str = "XAUUSD",
    side: str = "buy",
    exit_reason: str = "signal_flip",
    pnl_quote: float = 10.0,
    commission: float = 2.0,
    exit_time: str = "2024-01-01 08:00",
) -> Fill:
    return Fill(
        symbol=symbol,
        side=side,
        entry_time_utc=_utc("2024-01-01 04:00"),
        entry_price=100.0,
        exit_time_utc=_utc(exit_time),
        exit_price=101.0,
        lots=0.10,
        pnl_quote=pnl_quote,
        commission=commission,
        slippage=0.0,
        exit_reason=exit_reason,
    )


def test_fixed_lifecycle_backtest_rejects_invalid_hold():
    with pytest.raises(ValueError, match="hold_h4_bars must be positive"):
        backtest_fixed_lifecycle_from_result(
            h017_result=_h017_result(),
            usdjpy_h4=_h4(),
            xauusd_h4=_h4(),
            usdjpy_m1=_m1_no_stop(),
            xauusd_m1=_m1_no_stop(),
            accepted_entry_times=(_utc("2024-01-01 04:00"),),
            hold_h4_bars=0,
        )


def test_fixed_lifecycle_backtest_runs_non_overlapping_horizon():
    result = backtest_fixed_lifecycle_from_result(
        h017_result=_h017_result(),
        usdjpy_h4=_h4(),
        xauusd_h4=_h4(),
        usdjpy_m1=_m1_no_stop(),
        xauusd_m1=_m1_no_stop(),
        accepted_entry_times=(
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
            _utc("2024-01-01 12:00"),
        ),
        hold_h4_bars=2,
        starting_equity_usd=10_000.0,
    )

    assert result.accepted_entry_count == 3
    assert result.executed_entry_count == 1
    assert result.lifecycle_skip_count == 1
    assert result.fill_count if hasattr(result, "fill_count") else len(result.fills) == 1
    assert result.fills[0].symbol == "XAUUSD"
    assert result.fills[0].exit_time_utc == _utc("2024-01-01 12:00")


def test_summarize_lifecycle_backtest_reports_core_metrics():
    portfolio_result = backtest_fixed_lifecycle_from_result(
        h017_result=_h017_result(),
        usdjpy_h4=_h4(),
        xauusd_h4=_h4(),
        usdjpy_m1=_m1_no_stop(),
        xauusd_m1=_m1_no_stop(),
        accepted_entry_times=(
            _utc("2024-01-01 04:00"),
            _utc("2024-01-01 08:00"),
        ),
        hold_h4_bars=1,
        starting_equity_usd=10_000.0,
    )

    summary = summarize_lifecycle_backtest(portfolio_result)

    assert summary.hold_h4_bars == 1
    assert summary.accepted_entry_count == 2
    assert summary.fill_count >= 1
    assert summary.starting_equity_usd == pytest.approx(10_000.0)
    assert "H021 fixed lifecycle variant summary" in format_lifecycle_summary_table((summary,))


def test_group_summaries_by_symbol_and_side():
    fills = (
        _fill(symbol="XAUUSD", side="buy", pnl_quote=12.0, commission=2.0),
        _fill(symbol="USDJPY", side="sell", pnl_quote=-1100.0, commission=2.0),
    )

    by_symbol = summarize_fills_by_field(fills, field="symbol")
    by_side = summarize_fills_by_field(fills, field="side")

    assert [row.label for row in by_symbol] == ["USDJPY", "XAUUSD"]
    assert [row.label for row in by_side] == ["buy", "sell"]
    assert "By symbol" in format_group_summary_table(by_symbol, title="By symbol")


def test_chronological_halves_and_thirds_return_expected_labels():
    fills = (
        _fill(exit_time="2024-01-01 04:00"),
        _fill(exit_time="2024-01-02 04:00"),
        _fill(exit_time="2024-01-03 04:00"),
        _fill(exit_time="2024-01-04 04:00"),
        _fill(exit_time="2024-01-05 04:00"),
        _fill(exit_time="2024-01-06 04:00"),
    )

    halves = summarize_chronological_halves(fills)
    thirds = summarize_chronological_thirds(fills)

    assert [row.label for row in halves] == ["first_half", "second_half"]
    assert [row.label for row in thirds] == ["third_1", "third_2", "third_3"]
    assert halves[0].fill_count == 3
    assert thirds[0].fill_count == 2


def test_summarize_lifecycle_backtest_can_handle_empty_result():
    empty = H021FixedLifecycleBacktestResult(
        hold_h4_bars=4,
        accepted_entry_count=0,
        executed_entry_count=0,
        skipped_entry_count=0,
        lifecycle_skip_count=0,
        incomplete_horizon_skip_count=0,
        flat_entry_count=0,
        fills=(),
        portfolio=backtest_fixed_lifecycle_from_result(
            h017_result=_h017_result(),
            usdjpy_h4=_h4(),
            xauusd_h4=_h4(),
            usdjpy_m1=_m1_no_stop(),
            xauusd_m1=_m1_no_stop(),
            accepted_entry_times=(),
            hold_h4_bars=4,
            starting_equity_usd=10_000.0,
        ).portfolio,
    )

    summary = summarize_lifecycle_backtest(empty)

    assert summary.fill_count == 0
    assert summary.ending_equity_usd == pytest.approx(10_000.0)
    assert "no rows" in format_lifecycle_summary_table(())
