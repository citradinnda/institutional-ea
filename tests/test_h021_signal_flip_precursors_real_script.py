import pandas as pd
import pytest

from scripts.diagnose_h021_signal_flip_precursors_real import (
    format_signal_flip_contrast_table,
    scan_signal_flip_winner_buckets,
    summarize_signal_flip_contrasts,
)
from scripts.diagnose_h021_stop_precursors_real import H021StopPrecursorRecord


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _record(
    *,
    symbol: str = "XAUUSD",
    side: str = "buy",
    exit_reason: str = "signal_flip",
    decision_time: str = "2024-01-01 18:00",
    decision_hour_utc: str = "18",
    entry_hour_utc: str = "22",
    stop_distance_spread_bucket: str = ">=50x",
    estimated_gross_leverage_bucket: str = "<1x",
    pnl_usd: float = 10.0,
) -> H021StopPrecursorRecord:
    return H021StopPrecursorRecord(
        symbol=symbol,
        side=side,
        exit_reason=exit_reason,
        decision_time=_utc(decision_time),
        entry_time=_utc("2024-01-01 22:00"),
        decision_hour_utc=decision_hour_utc,
        entry_hour_utc=entry_hour_utc,
        entry_raw_price=2000.0,
        stop_price=1990.0,
        raw_stop_distance=10.0,
        stop_distance_spread_multiple=33.333333,
        stop_distance_spread_bucket=stop_distance_spread_bucket,
        signed_risk_fraction=0.01,
        lots=0.10,
        estimated_notional_usd=20000.0,
        estimated_gross_leverage=2.0,
        estimated_gross_leverage_bucket=estimated_gross_leverage_bucket,
        pnl_usd=pnl_usd,
    )


def test_summarize_signal_flip_contrasts_groups_by_requested_fields():
    rows = summarize_signal_flip_contrasts(
        (
            _record(symbol="XAUUSD", pnl_usd=20.0),
            _record(symbol="XAUUSD", exit_reason="stop", pnl_usd=-5.0),
            _record(symbol="USDJPY", pnl_usd=3.0),
        ),
        group_fields=("symbol",),
    )
    by_group = {row.group: row for row in rows}

    xauusd = by_group[(("symbol", "XAUUSD"),)]
    assert xauusd.fill_count == 2
    assert xauusd.signal_flip_winner_count == 1
    assert xauusd.signal_flip_winner_rate == pytest.approx(0.5)
    assert xauusd.stop_count == 1
    assert xauusd.stop_rate == pytest.approx(0.5)
    assert xauusd.losing_fill_count == 1
    assert xauusd.total_pnl_usd == pytest.approx(15.0)
    assert xauusd.median_pnl_usd == pytest.approx(7.5)
    assert xauusd.signal_flip_winner_pnl_usd == pytest.approx(20.0)
    assert xauusd.adverse_pnl_usd == pytest.approx(-5.0)
    assert xauusd.profit_factor == pytest.approx(4.0)


def test_summarize_signal_flip_contrasts_rejects_invalid_group_field():
    with pytest.raises(ValueError, match="unsupported group_fields"):
        summarize_signal_flip_contrasts((_record(),), group_fields=("not_a_field",))


def test_summarize_signal_flip_contrasts_rejects_empty_group_fields():
    with pytest.raises(ValueError, match="group_fields must not be empty"):
        summarize_signal_flip_contrasts((_record(),), group_fields=())


def test_scan_signal_flip_winner_buckets_applies_min_fill_and_positive_pnl_filters():
    records = (
        _record(symbol="XAUUSD", pnl_usd=20.0),
        _record(symbol="XAUUSD", pnl_usd=-5.0),
        _record(symbol="USDJPY", pnl_usd=100.0),
        _record(symbol="USDJPY", exit_reason="stop", pnl_usd=-200.0),
    )

    rows = scan_signal_flip_winner_buckets(
        records,
        group_field_sets=(("symbol",),),
        min_fill_count=2,
        require_positive_total_pnl=True,
    )

    assert [row.group for row in rows] == [(("symbol", "XAUUSD"),)]


def test_scan_signal_flip_winner_buckets_can_include_negative_total_pnl():
    records = (
        _record(symbol="USDJPY", pnl_usd=100.0),
        _record(symbol="USDJPY", exit_reason="stop", pnl_usd=-200.0),
    )

    rows = scan_signal_flip_winner_buckets(
        records,
        group_field_sets=(("symbol",),),
        min_fill_count=2,
        require_positive_total_pnl=False,
    )

    assert len(rows) == 1
    assert rows[0].total_pnl_usd == pytest.approx(-100.0)


def test_scan_signal_flip_winner_buckets_rejects_non_positive_min_fill_count():
    with pytest.raises(ValueError, match="min_fill_count must be positive"):
        scan_signal_flip_winner_buckets((_record(),), min_fill_count=0)


def test_format_signal_flip_contrast_table_includes_core_columns_and_truncation():
    rows = summarize_signal_flip_contrasts(
        (
            _record(symbol="XAUUSD", pnl_usd=20.0),
            _record(symbol="USDJPY", pnl_usd=10.0),
        ),
        group_fields=("symbol",),
    )

    table = format_signal_flip_contrast_table(rows, max_rows=1)

    assert "H021 signal-flip winner precursor contrast" in table
    assert "fields | group | fills" in table
    assert "sf_winners" in table
    assert "profit_factor" in table
    assert "truncated: showing 1 of 2 rows" in table


def test_format_signal_flip_contrast_table_handles_empty_rows():
    table = format_signal_flip_contrast_table(())

    assert "H021 signal-flip winner precursor contrast" in table
    assert "no matching buckets" in table
