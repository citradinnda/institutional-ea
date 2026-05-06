import pandas as pd
import pytest

from scripts.diagnose_h021_positive_bucket_search_real import (
    evaluate_positive_bucket_search,
    format_positive_bucket_table,
    summarize_positive_buckets,
)
from scripts.diagnose_h021_stop_precursors_real import H021StopPrecursorRecord


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _record(
    *,
    symbol: str = "XAUUSD",
    side: str = "buy",
    exit_reason: str = "signal_flip",
    decision_hour_utc: str = "00",
    entry_hour_utc: str = "04",
    stop_distance_spread_bucket: str = ">=50x",
    estimated_gross_leverage_bucket: str = "<1x",
    pnl_usd: float = 10.0,
) -> H021StopPrecursorRecord:
    return H021StopPrecursorRecord(
        symbol=symbol,
        side=side,
        exit_reason=exit_reason,
        decision_time=_utc(f"2024-01-01 {decision_hour_utc}:00"),
        entry_time=_utc(f"2024-01-01 {entry_hour_utc}:00"),
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


def test_summarize_positive_buckets_reports_bucket_metrics():
    records = (
        _record(symbol="XAUUSD", pnl_usd=20.0),
        _record(symbol="XAUUSD", pnl_usd=10.0),
        _record(symbol="XAUUSD", exit_reason="stop", pnl_usd=-15.0),
        _record(symbol="USDJPY", pnl_usd=-5.0),
        _record(symbol="USDJPY", pnl_usd=-10.0),
    )

    rows = summarize_positive_buckets(
        records,
        group_fields=("symbol",),
        min_fill_count=2,
    )

    assert len(rows) == 1
    row = rows[0]
    assert row.group_fields == ("symbol",)
    assert row.group == (("symbol", "XAUUSD"),)
    assert row.fill_count == 3
    assert row.stop_count == 1
    assert row.stop_rate == pytest.approx(1 / 3)
    assert row.total_pnl_usd == pytest.approx(15.0)
    assert row.mean_pnl_usd == pytest.approx(5.0)
    assert row.median_pnl_usd == pytest.approx(10.0)
    assert row.gross_profit_usd == pytest.approx(30.0)
    assert row.gross_loss_usd == pytest.approx(-15.0)
    assert row.profit_factor == pytest.approx(2.0)


def test_summarize_positive_buckets_can_include_negative_rows():
    records = (
        _record(symbol="USDJPY", pnl_usd=-5.0),
        _record(symbol="USDJPY", pnl_usd=-10.0),
    )

    rows = summarize_positive_buckets(
        records,
        group_fields=("symbol",),
        min_fill_count=2,
        positive_only=False,
    )

    assert len(rows) == 1
    assert rows[0].total_pnl_usd == pytest.approx(-15.0)


def test_summarize_positive_buckets_respects_min_fill_count():
    records = (
        _record(symbol="XAUUSD", pnl_usd=20.0),
        _record(symbol="XAUUSD", pnl_usd=10.0),
    )

    rows = summarize_positive_buckets(
        records,
        group_fields=("symbol",),
        min_fill_count=3,
    )

    assert rows == []


def test_summarize_positive_buckets_supports_multi_field_groups():
    records = (
        _record(symbol="XAUUSD", side="buy", pnl_usd=20.0),
        _record(symbol="XAUUSD", side="buy", pnl_usd=-5.0),
        _record(symbol="XAUUSD", side="sell", pnl_usd=-10.0),
    )

    rows = summarize_positive_buckets(
        records,
        group_fields=("symbol", "side"),
        min_fill_count=2,
    )

    assert len(rows) == 1
    assert rows[0].group == (("symbol", "XAUUSD"), ("side", "buy"))


def test_evaluate_positive_bucket_search_uses_group_sets_and_thresholds():
    records = (
        _record(symbol="XAUUSD", side="buy", pnl_usd=20.0),
        _record(symbol="XAUUSD", side="buy", pnl_usd=-5.0),
        _record(symbol="USDJPY", side="sell", pnl_usd=-10.0),
        _record(symbol="USDJPY", side="sell", pnl_usd=-10.0),
    )

    rows = evaluate_positive_bucket_search(
        records,
        group_field_sets=(("symbol",), ("symbol", "side")),
        min_fill_counts=(2,),
    )

    assert {row.group_fields for row in rows} == {
        ("symbol",),
        ("symbol", "side"),
    }
    assert all(row.total_pnl_usd > 0.0 for row in rows)


def test_group_field_validation_rejects_unknown_fields():
    records = (_record(),)

    with pytest.raises(ValueError, match="unsupported group field"):
        summarize_positive_buckets(
            records,
            group_fields=("exit_reason",),
            min_fill_count=1,
        )


def test_group_field_validation_rejects_empty_fields():
    records = (_record(),)

    with pytest.raises(ValueError, match="group_fields"):
        summarize_positive_buckets(
            records,
            group_fields=(),
            min_fill_count=1,
        )


def test_min_fill_count_validation_rejects_zero():
    records = (_record(),)

    with pytest.raises(ValueError, match="min_fill_count"):
        summarize_positive_buckets(
            records,
            group_fields=("symbol",),
            min_fill_count=0,
        )


def test_format_positive_bucket_table_includes_core_columns():
    records = (
        _record(symbol="XAUUSD", pnl_usd=20.0),
        _record(symbol="XAUUSD", pnl_usd=-5.0),
    )
    rows = summarize_positive_buckets(
        records,
        group_fields=("symbol",),
        min_fill_count=2,
    )

    table = format_positive_bucket_table(rows, title="Positive buckets")

    assert "Positive buckets" in table
    assert "field_set" in table
    assert "profit_factor" in table
    assert "symbol=XAUUSD" in table


def test_format_positive_bucket_table_handles_empty_rows():
    table = format_positive_bucket_table((), title="Positive buckets")

    assert "Positive buckets" in table
    assert "no positive buckets" in table
