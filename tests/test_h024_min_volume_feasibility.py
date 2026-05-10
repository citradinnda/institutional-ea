from pathlib import Path

import pytest

from scripts.summarize_h024_min_volume_feasibility import (
    compute_feasibility,
    compute_from_runtime_csv,
)


def test_under_min_volume_quantifies_required_balance_and_risk_fraction():
    result = compute_feasibility(
        symbol="USDJPY",
        action="BLOCKED",
        balance=100.0,
        risk_fraction=0.01,
        raw_lots=0.008,
        min_volume=0.01,
    )

    assert result.feasible_at_current_settings is False
    assert result.risk_usd == pytest.approx(1.0)
    assert result.loss_per_1_lot_usd == pytest.approx(125.0)
    assert result.minimum_risk_usd_for_min_volume == pytest.approx(1.25)
    assert result.minimum_balance_at_same_risk_fraction == pytest.approx(125.0)
    assert result.minimum_risk_fraction_at_same_balance == pytest.approx(0.0125)


def test_at_or_above_min_volume_is_feasible_without_execution_approval():
    result = compute_feasibility(
        symbol="USDJPY",
        action="WOULD_OPEN",
        balance=100.0,
        risk_fraction=0.01,
        raw_lots=0.01,
        min_volume=0.01,
    )

    assert result.feasible_at_current_settings is True
    assert result.minimum_balance_at_same_risk_fraction == pytest.approx(100.0)
    assert result.minimum_risk_fraction_at_same_balance == pytest.approx(0.01)


def test_mixed_schema_runtime_csv_parses_only_intended_action_rows(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    csv_path.write_text(
        "\n".join(
            [
                "schema,event,symbol,ok",
                "h024_ea_log_only_preflight_v2,tick,USDJPYm,true",
                "schema,action,symbol,normalized_symbol,raw_lots,lots,min_volume,reason",
                "h024_intended_action_log_v1,BLOCKED,USDJPYm,USDJPY,0.0083395062,0,0.01,BLOCKED:volume_below_min_for_would_open",
                "h024_ea_log_only_preflight_v2,tick,USDJPYm,true",
                "schema,action,symbol,normalized_symbol,raw_lots,lots,min_volume,reason",
                "h024_intended_action_log_v1,BLOCKED,XAUUSDm,XAUUSD,0.001824723,0,0.01,BLOCKED:volume_below_min_for_would_open",
            ]
        ),
        encoding="utf-8",
    )

    results = compute_from_runtime_csv(
        path=csv_path,
        balance=100.0,
        risk_fraction=0.01,
    )

    assert [result.symbol for result in results] == ["USDJPY", "XAUUSD"]
    assert all(result.action == "BLOCKED" for result in results)
    assert all(result.feasible_at_current_settings is False for result in results)
    assert results[0].minimum_balance_at_same_risk_fraction > 100.0
    assert results[1].minimum_balance_at_same_risk_fraction > results[0].minimum_balance_at_same_risk_fraction

def test_runtime_csv_collapses_repeated_timer_observations(tmp_path: Path):
    csv_path = tmp_path / "runtime.csv"
    csv_path.write_text(
        "\n".join(
            [
                "schema,action,symbol,normalized_symbol,raw_lots,lots,min_volume,reason",
                "h024_intended_action_log_v1,BLOCKED,USDJPYm,USDJPY,0.0083395062,0,0.01,BLOCKED:volume_below_min_for_would_open",
                "h024_intended_action_log_v1,BLOCKED,USDJPYm,USDJPY,0.0083395062,0,0.01,BLOCKED:volume_below_min_for_would_open",
                "h024_intended_action_log_v1,BLOCKED,USDJPYm,USDJPY,0.0083395062,0,0.01,BLOCKED:volume_below_min_for_would_open",
            ]
        ),
        encoding="utf-8",
    )

    results = compute_from_runtime_csv(
        path=csv_path,
        balance=100.0,
        risk_fraction=0.01,
    )

    assert len(results) == 1
    assert results[0].symbol == "USDJPY"
    assert results[0].observation_count == 3
    assert results[0].feasible_at_current_settings is False

