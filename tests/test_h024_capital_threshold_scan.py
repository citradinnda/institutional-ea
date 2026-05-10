from datetime import UTC
from functools import partial

import pandas as pd
import pytest

from scripts.scan_h024_capital_thresholds import (
    CapitalThresholdResult,
    count_candidates,
    find_first_balance_with_candidate,
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
