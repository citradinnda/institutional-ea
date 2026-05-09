import pandas as pd
import pytest

from scripts.diagnose_h024_ledger_permutation import (
    STARTING_EQUITY_USD,
    compute_path_stats,
    format_ledger_permutation_report,
    run_ledger_permutation_diagnostic,
)


def _ledger() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "exit_time_utc": [
                "2024-01-01T00:00:00+00:00",
                "2024-01-02T00:00:00+00:00",
                "2024-01-03T00:00:00+00:00",
                "2024-01-04T00:00:00+00:00",
            ],
            "pnl_usd": [100.0, -50.0, 25.0, -10.0],
        }
    )


def test_compute_path_stats_tracks_equity_and_drawdown():
    stats = compute_path_stats([100.0, -50.0, 25.0], starting_equity_usd=1000.0)

    assert stats.total_pnl_usd == pytest.approx(75.0)
    assert stats.ending_equity_usd == pytest.approx(1075.0)
    assert stats.min_equity_usd == pytest.approx(1000.0)
    assert stats.max_drawdown == pytest.approx(1050.0 / 1100.0 - 1.0)
    assert stats.ruin is False


def test_compute_path_stats_detects_ruin():
    stats = compute_path_stats([-1200.0], starting_equity_usd=1000.0)

    assert stats.ruin is True
    assert stats.min_equity_usd == pytest.approx(-200.0)


def test_ledger_permutation_is_deterministic():
    first = run_ledger_permutation_diagnostic(ledger=_ledger(), runs=5, seed=123)
    second = run_ledger_permutation_diagnostic(ledger=_ledger(), runs=5, seed=123)

    pd.testing.assert_frame_equal(first.permutations, second.permutations)
    assert first.observed.total_pnl_usd == pytest.approx(65.0)
    assert len(first.permutations) == 5


def test_ledger_permutation_report_contains_interpretation():
    result = run_ledger_permutation_diagnostic(ledger=_ledger(), runs=5, seed=123)
    report = format_ledger_permutation_report(result)

    assert "H024 ledger-level permutation diagnostic" in report
    assert "Research only. No demo/live/Phase 4 approval." in report
    assert "Max-drawdown empirical worse/equal rate:" in report
    assert "does not replace full execution timestamp shuffle" in report


def test_ledger_permutation_rejects_bad_inputs():
    with pytest.raises(ValueError, match="runs must be positive"):
        run_ledger_permutation_diagnostic(ledger=_ledger(), runs=0)

    with pytest.raises(ValueError, match="ledger must contain pnl_usd"):
        run_ledger_permutation_diagnostic(ledger=_ledger().drop(columns=["pnl_usd"]))

    with pytest.raises(ValueError, match="ledger must contain exit_time_utc"):
        run_ledger_permutation_diagnostic(ledger=_ledger().drop(columns=["exit_time_utc"]))

    with pytest.raises(ValueError, match="starting_equity_usd must be positive"):
        compute_path_stats([1.0], starting_equity_usd=0.0)


def test_starting_equity_constant_is_expected_anchor():
    assert STARTING_EQUITY_USD == 10_000.0
