from datetime import UTC
from functools import partial

import pandas as pd
import pytest

from scripts.scan_h024_capital_thresholds import (
    CapitalThresholdResult,
    count_candidates,
    find_first_balance_with_candidate,
    parse_risk_fraction_list,
    print_risk_fraction_threshold_comparison,
    summarize_risk_fraction_threshold_comparison,
    summarize_threshold,
)
from scripts.scan_h024_executable_candidate_shifts import ExecutableCandidateShift


def _candidate(symbol: str = "USDJPY") -> ExecutableCandidateShift:
    return ExecutableCandidateShift(
        symbol=symbol,
        side="buy",
        decision_time=pd.Timestamp("2026-01-01T00:00:00", tz=UTC),
        entry_time=pd.Timestamp("2026-01-01T04:00:00", tz=UTC),
        ea_closed_shift_from_latest_common_h4=3,
        signal_signed_risk_fraction=0.01,
        final_signed_risk_fraction=0.009,
        entry_price=100.0,
        stop_price=99.0,
        stop_distance=1.0,
    )


def test_count_candidates_supports_any_and_symbol_filters():
    candidates = [_candidate("USDJPY"), _candidate("XAUUSD"), _candidate("USDJPY")]

    assert count_candidates(candidates, None) == 3
    assert count_candidates(candidates, "USDJPY") == 2
    assert count_candidates(candidates, "XAUUSD") == 1


def test_find_first_balance_with_candidate_binary_searches_boundary():
    def provider(balance: int):
        if balance >= 245:
            return [_candidate("USDJPY")]
        return []

    assert find_first_balance_with_candidate(
        low_exclusive=120,
        high_inclusive=250,
        symbol=None,
        candidate_provider=provider,
    ) == 245


def test_find_first_balance_with_candidate_respects_symbol_filter():
    def provider(balance: int):
        candidates = []
        if balance >= 245:
            candidates.append(_candidate("USDJPY"))
        if balance >= 935:
            candidates.append(_candidate("XAUUSD"))
        return candidates

    assert find_first_balance_with_candidate(
        low_exclusive=550,
        high_inclusive=1000,
        symbol="XAUUSD",
        candidate_provider=provider,
    ) == 935


def test_find_first_balance_requires_valid_boundaries():
    with pytest.raises(ValueError, match="low boundary"):
        find_first_balance_with_candidate(
            low_exclusive=120,
            high_inclusive=250,
            symbol=None,
            candidate_provider=lambda _balance: [_candidate("USDJPY")],
        )

    with pytest.raises(ValueError, match="high boundary"):
        find_first_balance_with_candidate(
            low_exclusive=120,
            high_inclusive=250,
            symbol=None,
            candidate_provider=lambda _balance: [],
        )


def test_summarize_threshold_returns_counts_and_first_matching_candidate():
    def provider(balance: int):
        if balance < 935:
            return []
        return [_candidate("USDJPY"), _candidate("XAUUSD")]

    result = summarize_threshold(
        label="XAUUSD",
        symbol="XAUUSD",
        low_exclusive=550,
        high_inclusive=1000,
        candidate_provider=provider,
    )

    assert isinstance(result, CapitalThresholdResult)
    assert result.label == "XAUUSD"
    assert result.balance_usd == 935
    assert result.total_candidates == 2
    assert result.usdjpy_candidates == 1
    assert result.xauusd_candidates == 1
    assert result.first_matching_candidate.symbol == "XAUUSD"

class _SyntheticCandidate:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol


def test_expand_high_boundary_until_candidate_expands_initial_empty_high() -> None:
    from scripts.scan_h024_capital_thresholds import expand_high_boundary_until_candidate

    def provider(balance: int):
        if balance >= 490:
            return [_SyntheticCandidate("USDJPY")]
        return []

    expanded_high = expand_high_boundary_until_candidate(
        low_exclusive=0,
        high_inclusive=250,
        symbol=None,
        candidate_provider=provider,
        max_high=1000,
    )

    assert expanded_high == 500


def test_summarize_threshold_auto_expands_high_boundary() -> None:
    from scripts.scan_h024_capital_thresholds import summarize_threshold

    def provider(balance: int):
        if balance >= 490:
            return [_SyntheticCandidate("USDJPY")]
        return []

    result = summarize_threshold(
        label="ANY",
        symbol=None,
        low_exclusive=0,
        high_inclusive=250,
        candidate_provider=provider,
        auto_expand_high=True,
        max_high=1000,
    )

    assert result.balance_usd == 490
    assert result.total_candidates == 1
    assert result.usdjpy_candidates == 1
    assert result.xauusd_candidates == 0

def test_parse_risk_fraction_list_parses_comma_separated_values() -> None:
    assert parse_risk_fraction_list("0.005, 0.0075,0.01") == [
        0.005,
        0.0075,
        0.01,
    ]


def test_parse_risk_fraction_list_rejects_empty_and_nonpositive_values() -> None:
    with pytest.raises(ValueError, match="empty"):
        parse_risk_fraction_list("0.005,,0.01")

    with pytest.raises(ValueError, match="positive"):
        parse_risk_fraction_list("0.005,0")


def test_summarize_risk_fraction_threshold_comparison_builds_rows() -> None:
    thresholds = {
        0.01: {"USDJPY": 245, "XAUUSD": 935},
        0.02: {"USDJPY": 123, "XAUUSD": 468},
    }

    def factory(risk_fraction: float):
        def provider(balance: int):
            candidates = []
            if balance >= thresholds[risk_fraction]["USDJPY"]:
                candidates.append(_candidate("USDJPY"))
            if balance >= thresholds[risk_fraction]["XAUUSD"]:
                candidates.append(_candidate("XAUUSD"))
            return candidates

        return provider

    rows = summarize_risk_fraction_threshold_comparison(
        risk_fractions=[0.01, 0.02],
        candidate_provider_factory=factory,
        any_high=250,
        usdjpy_high=250,
        xauusd_high=500,
        max_high=1000,
    )

    assert [row.risk_fraction for row in rows] == [0.01, 0.02]
    assert rows[0].any_threshold.balance_usd == 245
    assert rows[0].usdjpy_threshold.balance_usd == 245
    assert rows[0].xauusd_threshold.balance_usd == 935
    assert rows[1].any_threshold.balance_usd == 123
    assert rows[1].usdjpy_threshold.balance_usd == 123
    assert rows[1].xauusd_threshold.balance_usd == 468


def test_print_risk_fraction_threshold_comparison_outputs_research_only_table(
    capsys,
) -> None:
    result_245 = CapitalThresholdResult(
        label="ANY",
        balance_usd=245,
        total_candidates=1,
        usdjpy_candidates=1,
        xauusd_candidates=0,
        first_matching_candidate=_candidate("USDJPY"),
    )
    result_935 = CapitalThresholdResult(
        label="XAUUSD",
        balance_usd=935,
        total_candidates=569,
        usdjpy_candidates=568,
        xauusd_candidates=1,
        first_matching_candidate=_candidate("XAUUSD"),
    )
    rows = [
        __import__(
            "scripts.scan_h024_capital_thresholds",
            fromlist=["RiskFractionThresholdComparisonRow"],
        ).RiskFractionThresholdComparisonRow(
            risk_fraction=0.01,
            any_threshold=result_245,
            usdjpy_threshold=result_245,
            xauusd_threshold=result_935,
        )
    ]

    print_risk_fraction_threshold_comparison(rows)

    output = capsys.readouterr().out
    assert "Risk fraction" in output
    assert "1.00%" in output
    assert "245 USD" in output
    assert "935 USD" in output
    assert "no higher-risk" in output
    assert "no higher-balance" in output
    assert "no execution approval" in output
