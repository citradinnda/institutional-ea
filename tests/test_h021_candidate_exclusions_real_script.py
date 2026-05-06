import pandas as pd
import pytest

from scripts.diagnose_h021_candidate_exclusions_real import (
    H021CandidateExclusion,
    H021ExclusionRule,
    evaluate_candidate_exclusion,
    evaluate_candidate_exclusions,
    format_candidate_exclusion_table,
    summarize_record_set,
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


def test_summarize_record_set_reports_stop_rate_and_profit_factor():
    records = (
        _record(exit_reason="signal_flip", pnl_usd=20.0),
        _record(exit_reason="stop", pnl_usd=-10.0),
        _record(exit_reason="stop", pnl_usd=-30.0),
    )

    summary = summarize_record_set(records)

    assert summary.fill_count == 3
    assert summary.stop_count == 2
    assert summary.stop_rate == pytest.approx(2 / 3)
    assert summary.winning_fill_count == 1
    assert summary.losing_fill_count == 2
    assert summary.total_pnl_usd == pytest.approx(-20.0)
    assert summary.gross_profit_usd == pytest.approx(20.0)
    assert summary.gross_loss_usd == pytest.approx(-40.0)
    assert summary.profit_factor == pytest.approx(0.5)


def test_summarize_empty_record_set_is_safe():
    summary = summarize_record_set(())

    assert summary.fill_count == 0
    assert summary.stop_count == 0
    assert summary.total_pnl_usd == pytest.approx(0.0)
    assert summary.stop_rate != summary.stop_rate
    assert summary.profit_factor != summary.profit_factor


def test_evaluate_candidate_exclusion_splits_excluded_and_retained_records():
    records = (
        _record(estimated_gross_leverage_bucket="6-9x", exit_reason="stop", pnl_usd=-100.0),
        _record(estimated_gross_leverage_bucket="<1x", exit_reason="signal_flip", pnl_usd=25.0),
    )
    candidate = H021CandidateExclusion(
        name="exclude_high_leverage",
        rules=(H021ExclusionRule("estimated_gross_leverage_bucket", ("6-9x",)),),
    )

    result = evaluate_candidate_exclusion(records, candidate)

    assert result.baseline.fill_count == 2
    assert result.baseline.total_pnl_usd == pytest.approx(-75.0)
    assert result.excluded.fill_count == 1
    assert result.excluded.stop_count == 1
    assert result.excluded.total_pnl_usd == pytest.approx(-100.0)
    assert result.retained.fill_count == 1
    assert result.retained.total_pnl_usd == pytest.approx(25.0)
    assert result.retained_pnl_improvement_usd == pytest.approx(100.0)


def test_evaluate_candidate_exclusion_supports_and_rules():
    records = (
        _record(symbol="USDJPY", side="sell", pnl_usd=-50.0),
        _record(symbol="USDJPY", side="buy", pnl_usd=10.0),
        _record(symbol="XAUUSD", side="sell", pnl_usd=20.0),
    )
    candidate = H021CandidateExclusion(
        name="exclude_usdjpy_sell",
        rules=(
            H021ExclusionRule("symbol", ("USDJPY",)),
            H021ExclusionRule("side", ("sell",)),
        ),
    )

    result = evaluate_candidate_exclusion(records, candidate)

    assert result.excluded.fill_count == 1
    assert result.excluded.total_pnl_usd == pytest.approx(-50.0)
    assert result.retained.fill_count == 2
    assert result.retained.total_pnl_usd == pytest.approx(30.0)


def test_evaluate_candidate_exclusions_uses_multiple_candidates():
    records = (
        _record(decision_hour_utc="05", pnl_usd=-10.0),
        _record(estimated_gross_leverage_bucket="6-9x", pnl_usd=-20.0),
    )
    candidates = (
        H021CandidateExclusion(
            name="exclude_hour_05",
            rules=(H021ExclusionRule("decision_hour_utc", ("05",)),),
        ),
        H021CandidateExclusion(
            name="exclude_leverage_6_9",
            rules=(H021ExclusionRule("estimated_gross_leverage_bucket", ("6-9x",)),),
        ),
    )

    results = evaluate_candidate_exclusions(records, candidates)

    assert len(results) == 2
    assert {result.candidate.name for result in results} == {
        "exclude_hour_05",
        "exclude_leverage_6_9",
    }


def test_candidate_validation_rejects_empty_rules():
    candidate = H021CandidateExclusion(name="bad", rules=())

    with pytest.raises(ValueError, match="candidate rules"):
        evaluate_candidate_exclusion((), candidate)


def test_format_candidate_exclusion_table_sorts_by_pnl_improvement():
    records = (
        _record(decision_hour_utc="05", pnl_usd=-10.0),
        _record(estimated_gross_leverage_bucket="6-9x", pnl_usd=-50.0),
        _record(pnl_usd=5.0),
    )
    candidates = (
        H021CandidateExclusion(
            name="exclude_hour_05",
            rules=(H021ExclusionRule("decision_hour_utc", ("05",)),),
        ),
        H021CandidateExclusion(
            name="exclude_leverage_6_9",
            rules=(H021ExclusionRule("estimated_gross_leverage_bucket", ("6-9x",)),),
        ),
    )
    results = evaluate_candidate_exclusions(records, candidates)

    table = format_candidate_exclusion_table(results, title="Candidate exclusions")

    assert "Candidate exclusions" in table
    assert "retained_pnl_usd" in table
    assert table.index("exclude_leverage_6_9") < table.index("exclude_hour_05")
