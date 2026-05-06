import pandas as pd
import pytest

from quantcore.backtest.fill_engine import Fill
from quantcore.backtest.portfolio import fill_pnl_usd
from scripts.diagnose_h021_bridge_hold_horizon_real import (
    H021BridgeHorizonObservation,
    compare_signal_flip_horizons,
    format_bridge_horizon_summary_table,
    simulate_alternate_horizon_fill,
    summarize_bridge_horizon_observations,
)
from scripts.diagnose_h021_stop_precursors_real import H021StopPrecursorRecord


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _h4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100.0, 102.0, 105.0, 106.0],
            "high": [101.0, 103.0, 106.0, 107.0],
            "low": [99.0, 101.0, 104.0, 105.0],
            "close": [100.5, 102.5, 105.5, 106.5],
        },
        index=pd.DatetimeIndex(
            [
                _utc("2024-01-01 00:00"),
                _utc("2024-01-01 04:00"),
                _utc("2024-01-01 08:00"),
                _utc("2024-01-01 12:00"),
            ]
        ),
    )


def _m1_no_stop() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100.0, 102.0, 104.0],
            "high": [101.0, 103.0, 106.0],
            "low": [99.0, 101.0, 103.0],
            "close": [100.5, 102.5, 105.5],
        },
        index=pd.DatetimeIndex(
            [
                _utc("2024-01-01 00:00"),
                _utc("2024-01-01 04:00"),
                _utc("2024-01-01 08:00"),
            ]
        ),
    )


def _m1_stop() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100.0, 96.0, 104.0],
            "high": [101.0, 97.0, 106.0],
            "low": [99.0, 94.0, 103.0],
            "close": [100.5, 95.5, 105.5],
        },
        index=pd.DatetimeIndex(
            [
                _utc("2024-01-01 00:00"),
                _utc("2024-01-01 01:00"),
                _utc("2024-01-01 08:00"),
            ]
        ),
    )


def _fill(*, exit_reason: str = "signal_flip", pnl_quote: float = 10.0) -> Fill:
    return Fill(
        symbol="XAUUSD",
        side="buy",
        entry_time_utc=_utc("2024-01-01 00:00"),
        entry_price=100.15,
        exit_time_utc=_utc("2024-01-01 04:00"),
        exit_price=101.85,
        lots=0.10,
        pnl_quote=pnl_quote,
        commission=2.0,
        slippage=0.0,
        exit_reason=exit_reason,
    )


def _record(*, exit_reason: str = "signal_flip") -> H021StopPrecursorRecord:
    return H021StopPrecursorRecord(
        symbol="XAUUSD",
        side="buy",
        exit_reason=exit_reason,
        decision_time=_utc("2023-12-31 20:00"),
        entry_time=_utc("2024-01-01 00:00"),
        decision_hour_utc="20",
        entry_hour_utc="00",
        entry_raw_price=100.0,
        stop_price=95.0,
        raw_stop_distance=5.0,
        stop_distance_spread_multiple=16.666667,
        stop_distance_spread_bucket="10-20x",
        signed_risk_fraction=0.01,
        lots=0.10,
        estimated_notional_usd=1000.0,
        estimated_gross_leverage=0.10,
        estimated_gross_leverage_bucket="<1x",
        pnl_usd=8.0,
    )


def test_simulate_alternate_horizon_fill_forced_exits_at_requested_h4_open():
    fill = simulate_alternate_horizon_fill(
        baseline_fill=_fill(),
        record=_record(),
        h4_bars=_h4(),
        m1_bars=_m1_no_stop(),
        hold_h4_bars=2,
    )

    assert fill.exit_reason == "signal_flip"
    assert fill.exit_time_utc == _utc("2024-01-01 08:00")
    assert fill.exit_price == pytest.approx(104.85)
    assert fill.commission == pytest.approx(2.0)
    assert fill_pnl_usd(fill=fill) == pytest.approx(45.0)


def test_simulate_alternate_horizon_fill_preserves_stop_first_rule_and_stop_costs():
    fill = simulate_alternate_horizon_fill(
        baseline_fill=_fill(),
        record=_record(),
        h4_bars=_h4(),
        m1_bars=_m1_stop(),
        hold_h4_bars=2,
    )

    assert fill.exit_reason == "stop"
    assert fill.exit_time_utc == _utc("2024-01-01 01:00")
    assert fill.exit_price == pytest.approx(94.60)
    assert fill.slippage == pytest.approx(0.25)
    assert fill_pnl_usd(fill=fill) == pytest.approx(-57.5)


def test_simulate_alternate_horizon_fill_rejects_invalid_horizon():
    with pytest.raises(ValueError, match="hold_h4_bars must be positive"):
        simulate_alternate_horizon_fill(
            baseline_fill=_fill(),
            record=_record(),
            h4_bars=_h4(),
            m1_bars=_m1_no_stop(),
            hold_h4_bars=0,
        )


def test_compare_signal_flip_horizons_skips_non_signal_flip_records():
    observations = compare_signal_flip_horizons(
        records=(_record(exit_reason="signal_flip"), _record(exit_reason="stop")),
        fills=(_fill(),),
        h4_by_symbol={"XAUUSD": _h4()},
        m1_by_symbol={"XAUUSD": _m1_no_stop()},
        hold_h4_bars_values=(2,),
    )

    assert len(observations) == 1
    assert observations[0].hold_h4_bars == 2
    assert observations[0].alternate_pnl_usd == pytest.approx(45.0)
    assert observations[0].outcome_label == "winner_improved"


def test_compare_signal_flip_horizons_rejects_empty_horizon_set():
    with pytest.raises(ValueError, match="hold_h4_bars_values must not be empty"):
        compare_signal_flip_horizons(
            records=(_record(),),
            fills=(_fill(),),
            h4_by_symbol={"XAUUSD": _h4()},
            m1_by_symbol={"XAUUSD": _m1_no_stop()},
            hold_h4_bars_values=(),
        )


def test_summarize_bridge_horizon_observations_counts_winner_transitions():
    observations = (
        H021BridgeHorizonObservation(
            symbol="XAUUSD",
            side="buy",
            entry_time=_utc("2024-01-01 00:00"),
            baseline_exit_time=_utc("2024-01-01 04:00"),
            baseline_exit_reason="signal_flip",
            baseline_pnl_usd=10.0,
            hold_h4_bars=2,
            alternate_exit_time=_utc("2024-01-01 08:00"),
            alternate_exit_reason="signal_flip",
            alternate_pnl_usd=15.0,
            pnl_delta_usd=5.0,
            outcome_label="winner_improved",
        ),
        H021BridgeHorizonObservation(
            symbol="XAUUSD",
            side="buy",
            entry_time=_utc("2024-01-02 00:00"),
            baseline_exit_time=_utc("2024-01-02 04:00"),
            baseline_exit_reason="signal_flip",
            baseline_pnl_usd=5.0,
            hold_h4_bars=2,
            alternate_exit_time=_utc("2024-01-02 01:00"),
            alternate_exit_reason="stop",
            alternate_pnl_usd=-20.0,
            pnl_delta_usd=-25.0,
            outcome_label="winner_to_loss",
        ),
        H021BridgeHorizonObservation(
            symbol="XAUUSD",
            side="buy",
            entry_time=_utc("2024-01-03 00:00"),
            baseline_exit_time=_utc("2024-01-03 04:00"),
            baseline_exit_reason="signal_flip",
            baseline_pnl_usd=-3.0,
            hold_h4_bars=2,
            alternate_exit_time=_utc("2024-01-03 08:00"),
            alternate_exit_reason="signal_flip",
            alternate_pnl_usd=6.0,
            pnl_delta_usd=9.0,
            outcome_label="loser_to_profit",
        ),
    )

    rows = summarize_bridge_horizon_observations(observations)

    assert len(rows) == 1
    row = rows[0]
    assert row.observation_count == 3
    assert row.alternate_stop_count == 1
    assert row.alternate_stop_rate == pytest.approx(1 / 3)
    assert row.baseline_total_pnl_usd == pytest.approx(12.0)
    assert row.alternate_total_pnl_usd == pytest.approx(1.0)
    assert row.total_pnl_delta_usd == pytest.approx(-11.0)
    assert row.median_pnl_delta_usd == pytest.approx(5.0)
    assert row.baseline_winner_count == 2
    assert row.winner_retained_profit_count == 1
    assert row.winner_to_loss_count == 1
    assert row.winner_stopped_count == 1
    assert row.winner_improved_count == 1
    assert row.loser_to_profit_count == 1
    assert row.alternate_profit_factor == pytest.approx(21.0 / 20.0)


def test_format_bridge_horizon_summary_table_includes_core_columns():
    rows = summarize_bridge_horizon_observations(
        (
            H021BridgeHorizonObservation(
                symbol="XAUUSD",
                side="buy",
                entry_time=_utc("2024-01-01 00:00"),
                baseline_exit_time=_utc("2024-01-01 04:00"),
                baseline_exit_reason="signal_flip",
                baseline_pnl_usd=10.0,
                hold_h4_bars=2,
                alternate_exit_time=_utc("2024-01-01 08:00"),
                alternate_exit_reason="signal_flip",
                alternate_pnl_usd=15.0,
                pnl_delta_usd=5.0,
                outcome_label="winner_improved",
            ),
        )
    )

    table = format_bridge_horizon_summary_table(rows)

    assert "H021 bridge hold-horizon summary" in table
    assert "hold_h4_bars | observations" in table
    assert "alternate_profit_factor" in table


def test_format_bridge_horizon_summary_table_handles_empty_rows():
    table = format_bridge_horizon_summary_table(())

    assert "H021 bridge hold-horizon summary" in table
    assert "no observations" in table
