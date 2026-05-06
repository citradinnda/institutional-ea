import pandas as pd
import pytest

from scripts.diagnose_h021_positive_bucket_stability_real import (
    H021BucketLead,
    evaluate_bucket_stability,
    format_bucket_stability_table,
    record_matches_lead,
)
from scripts.diagnose_h021_stop_precursors_real import H021StopPrecursorRecord


def _utc(value: str) -> pd.Timestamp:
    return pd.Timestamp(value, tz="UTC")


def _record(
    *,
    symbol: str = "XAUUSD",
    side: str = "sell",
    exit_reason: str = "signal_flip",
    decision_time: str = "2024-01-01 01:00",
    decision_hour_utc: str = "01",
    entry_hour_utc: str = "05",
    stop_distance_spread_bucket: str = ">=50x",
    estimated_gross_leverage_bucket: str = "<1x",
    pnl_usd: float = 10.0,
) -> H021StopPrecursorRecord:
    return H021StopPrecursorRecord(
        symbol=symbol,
        side=side,
        exit_reason=exit_reason,
        decision_time=_utc(decision_time),
        entry_time=_utc("2024-01-01 05:00"),
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


def test_record_matches_lead_requires_all_criteria():
    lead = H021BucketLead(
        label="XAUUSD sell 01",
        criteria=(("symbol", "XAUUSD"), ("side", "sell"), ("decision_hour_utc", "01")),
    )

    assert record_matches_lead(_record(), lead)
    assert not record_matches_lead(_record(side="buy"), lead)


def test_evaluate_bucket_stability_reports_overall_halves_and_years():
    lead = H021BucketLead(
        label="XAUUSD sell 01",
        criteria=(("symbol", "XAUUSD"), ("side", "sell"), ("decision_hour_utc", "01")),
    )
    records = (
        _record(decision_time="2022-01-01 01:00", pnl_usd=30.0),
        _record(decision_time="2022-02-01 01:00", exit_reason="stop", pnl_usd=-10.0),
        _record(decision_time="2023-01-01 01:00", pnl_usd=20.0),
        _record(decision_time="2023-02-01 01:00", exit_reason="stop", pnl_usd=-5.0),
        _record(symbol="USDJPY", side="buy", decision_hour_utc="01", pnl_usd=999.0),
    )

    rows = evaluate_bucket_stability(records, leads=(lead,))
    by_period = {row.period_label: row for row in rows}

    assert set(by_period) == {
        "overall",
        "chronological_first_half",
        "chronological_second_half",
        "calendar_year_2022",
        "calendar_year_2023",
    }

    overall = by_period["overall"]
    assert overall.fill_count == 4
    assert overall.stop_count == 2
    assert overall.stop_rate == pytest.approx(0.5)
    assert overall.total_pnl_usd == pytest.approx(35.0)
    assert overall.mean_pnl_usd == pytest.approx(8.75)
    assert overall.median_pnl_usd == pytest.approx(7.5)
    assert overall.gross_profit_usd == pytest.approx(50.0)
    assert overall.gross_loss_usd == pytest.approx(-15.0)
    assert overall.profit_factor == pytest.approx(50.0 / 15.0)


def test_evaluate_bucket_stability_uses_chronological_sort_before_half_split():
    lead = H021BucketLead(
        label="XAUUSD sell 01",
        criteria=(("symbol", "XAUUSD"), ("side", "sell"), ("decision_hour_utc", "01")),
    )
    records = (
        _record(decision_time="2023-01-01 01:00", pnl_usd=100.0),
        _record(decision_time="2022-01-01 01:00", pnl_usd=10.0),
        _record(decision_time="2024-01-01 01:00", pnl_usd=1000.0),
        _record(decision_time="2021-01-01 01:00", pnl_usd=1.0),
    )

    rows = evaluate_bucket_stability(records, leads=(lead,))
    by_period = {row.period_label: row for row in rows}

    assert by_period["chronological_first_half"].total_pnl_usd == pytest.approx(11.0)
    assert by_period["chronological_second_half"].total_pnl_usd == pytest.approx(1100.0)


def test_evaluate_bucket_stability_returns_no_rows_when_lead_has_no_matches():
    lead = H021BucketLead(
        label="USDJPY sell 06",
        criteria=(("symbol", "USDJPY"), ("side", "sell"), ("decision_hour_utc", "06")),
    )

    assert evaluate_bucket_stability((_record(),), leads=(lead,)) == ()


def test_format_bucket_stability_table_includes_core_columns():
    lead = H021BucketLead(
        label="XAUUSD sell 01",
        criteria=(("symbol", "XAUUSD"), ("side", "sell"), ("decision_hour_utc", "01")),
    )
    rows = evaluate_bucket_stability((_record(pnl_usd=10.0), _record(pnl_usd=-5.0)), leads=(lead,))

    table = format_bucket_stability_table(rows)

    assert "H021 positive bucket temporal stability" in table
    assert "bucket | period | fills" in table
    assert "XAUUSD sell 01" in table
    assert "profit_factor" in table


def test_format_bucket_stability_table_handles_empty_rows():
    table = format_bucket_stability_table(())

    assert "H021 positive bucket temporal stability" in table
    assert "no matching fills" in table
