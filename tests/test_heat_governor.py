from __future__ import annotations

"""Tests for Phase 2.3 portfolio heat governor.

Coverage targets (~26 tests):
    - HeatConfig validation (5)
    - Input validation (6)
    - Single-symbol behavior (3)
    - Two-symbol uncorrelated (3)
    - Two-symbol perfectly correlated (3)
    - Correlation floor behavior (2)
    - Multiplier output structure (3)
    - Determinism + edge cases (1)
"""

import numpy as np
import pandas as pd
import pytest

from quantcore.strategy import HeatConfig, HeatResult, heat_governor


# ---------- helpers ----------

def _make_panels(
    signals_data: dict[str, list[float]],
    returns_data: dict[str, list[float]],
    freq: str = "4h",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build aligned signals + returns panels with a UTC datetime index."""
    n = len(next(iter(signals_data.values())))
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    signals = pd.DataFrame(signals_data, index=idx)
    returns = pd.DataFrame(returns_data, index=idx)
    return signals, returns


def _independent_returns(n: int, seed: int = 0) -> tuple[list[float], list[float]]:
    """Generate two uncorrelated return streams for warm-up periods."""
    rng = np.random.default_rng(seed)
    a = rng.normal(0, 0.01, n).tolist()
    b = rng.normal(0, 0.01, n).tolist()
    return a, b


def _correlated_returns(n: int, seed: int = 0) -> tuple[list[float], list[float]]:
    """Two streams with rho ≈ 1: b is a copy of a."""
    rng = np.random.default_rng(seed)
    a = rng.normal(0, 0.01, n).tolist()
    return a, list(a)


# ---------- HeatConfig validation ----------

def test_heat_config_defaults() -> None:
    cfg = HeatConfig()
    assert cfg.max_portfolio_heat == 0.015
    assert cfg.per_trade_risk == 0.01
    assert cfg.correlation_window == 120
    assert cfg.correlation_floor == 0.0


def test_heat_config_rejects_zero_cap() -> None:
    with pytest.raises(ValueError, match="max_portfolio_heat"):
        HeatConfig(max_portfolio_heat=0.0)


def test_heat_config_rejects_negative_per_trade_risk() -> None:
    with pytest.raises(ValueError, match="per_trade_risk"):
        HeatConfig(per_trade_risk=-0.01)


def test_heat_config_rejects_short_corr_window() -> None:
    with pytest.raises(ValueError, match="correlation_window"):
        HeatConfig(correlation_window=1)


def test_heat_config_rejects_corr_floor_above_one() -> None:
    with pytest.raises(ValueError, match="correlation_floor"):
        HeatConfig(correlation_floor=1.5)


# ---------- input validation ----------

def test_rejects_non_dataframe_signals() -> None:
    rets = pd.DataFrame(
        {"USDJPY": [0.01, 0.02]},
        index=pd.date_range("2024-01-01", periods=2, freq="4h", tz="UTC"),
    )
    with pytest.raises(TypeError, match="signals must be DataFrame"):
        heat_governor(signals=[1, 0], returns=rets)  # type: ignore[arg-type]


def test_rejects_mismatched_columns() -> None:
    n = 130
    a, b = _independent_returns(n)
    sig = pd.DataFrame(
        {"USDJPY": [0] * n, "XAUUSD": [0] * n},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame(
        {"USDJPY": a, "EURUSD": b},
        index=sig.index,
    )
    with pytest.raises(ValueError, match="identical columns"):
        heat_governor(sig, rets)


def test_rejects_mismatched_index() -> None:
    n = 130
    a, b = _independent_returns(n)
    sig = pd.DataFrame(
        {"USDJPY": [0] * n, "XAUUSD": [0] * n},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame(
        {"USDJPY": a, "XAUUSD": b},
        index=pd.date_range("2024-06-01", periods=n, freq="4h", tz="UTC"),
    )
    with pytest.raises(ValueError, match="identical"):
        heat_governor(sig, rets)


def test_rejects_non_datetime_index() -> None:
    sig = pd.DataFrame({"USDJPY": [0, 1], "XAUUSD": [0, 0]})
    rets = pd.DataFrame({"USDJPY": [0.01, 0.01], "XAUUSD": [0.01, 0.01]})
    with pytest.raises(TypeError, match="DatetimeIndex"):
        heat_governor(sig, rets)


def test_rejects_empty_columns() -> None:
    idx = pd.date_range("2024-01-01", periods=3, freq="4h", tz="UTC")
    sig = pd.DataFrame(index=idx)
    rets = pd.DataFrame(index=idx)
    with pytest.raises(ValueError, match="at least one column"):
        heat_governor(sig, rets)


def test_rejects_unsorted_index() -> None:
    n = 130
    a, b = _independent_returns(n)
    idx = pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC")
    sig = pd.DataFrame({"USDJPY": [0] * n, "XAUUSD": [0] * n}, index=idx).iloc[::-1]
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=idx).iloc[::-1]
    with pytest.raises(ValueError, match="sorted ascending"):
        heat_governor(sig, rets)


# ---------- single-symbol behavior ----------

def test_single_symbol_long_full_size() -> None:
    """One symbol, signal=+1: heat = r = 1% < cap; multiplier = 1."""
    n = 130
    rng = np.random.default_rng(0)
    rets_data = rng.normal(0, 0.01, n).tolist()
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": rets_data}, index=sig.index)
    result = heat_governor(sig, rets)
    # Bars 125..129 should have multiplier 1, heat = per_trade_risk.
    assert (result.multipliers["USDJPY"].iloc[125:] == 1.0).all()
    np.testing.assert_allclose(
        result.portfolio_heat_pre.iloc[125:].to_numpy(),
        np.full(5, 0.01),
        atol=1e-12,
    )
    assert not result.binding.iloc[125:].any()


def test_single_symbol_flat_zero_multiplier() -> None:
    n = 130
    rng = np.random.default_rng(0)
    sig = pd.DataFrame(
        {"USDJPY": [0] * n},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": rng.normal(0, 0.01, n).tolist()}, index=sig.index)
    result = heat_governor(sig, rets)
    assert (result.multipliers["USDJPY"] == 0.0).all()
    assert (result.portfolio_heat_pre == 0.0).all()


def test_single_symbol_short_full_size() -> None:
    """Direction sign doesn't matter for single-symbol heat."""
    n = 130
    rng = np.random.default_rng(0)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [-1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": rng.normal(0, 0.01, n).tolist()}, index=sig.index)
    result = heat_governor(sig, rets)
    assert (result.multipliers["USDJPY"].iloc[125:] == 1.0).all()


# ---------- two-symbol uncorrelated ----------

def test_two_symbol_uncorrelated_both_on_under_cap() -> None:
    """rho=0, both long: heat = r*sqrt(2) ≈ 1.41% < 1.5% cap, full size."""
    n = 130
    a, b = _independent_returns(n, seed=42)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5, "XAUUSD": [0] * 125 + [1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    # Heat should be approximately r*sqrt(2) ≈ 0.01414, under 1.5% cap.
    last_heat = result.portfolio_heat_pre.iloc[-1]
    assert last_heat < 0.015
    assert last_heat > 0.013  # well above r alone (0.01)
    assert result.multipliers.iloc[-1].tolist() == [1.0, 1.0]
    assert not result.binding.iloc[-1]


def test_two_symbol_one_on_one_off() -> None:
    """Only one position active: heat = r, both multipliers as expected."""
    n = 130
    a, b = _independent_returns(n, seed=1)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5, "XAUUSD": [0] * n},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    np.testing.assert_allclose(result.portfolio_heat_pre.iloc[-1], 0.01, atol=1e-12)
    assert result.multipliers["USDJPY"].iloc[-1] == 1.0
    assert result.multipliers["XAUUSD"].iloc[-1] == 0.0


def test_two_symbol_opposite_directions() -> None:
    """Long/short with corr floored at 0: heat = r*sqrt(2) under cap."""
    n = 130
    a, b = _independent_returns(n, seed=7)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5, "XAUUSD": [0] * 125 + [-1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    # With corr floor at 0, signs cancel via floor, so heat = r*sqrt(2).
    last_heat = result.portfolio_heat_pre.iloc[-1]
    assert last_heat < 0.015
    assert result.multipliers.iloc[-1].tolist() == [1.0, 1.0]


# ---------- two-symbol perfectly correlated ----------

def test_two_symbol_perfectly_correlated_binds() -> None:
    """rho≈1, both long: heat = 2r = 2% > 1.5% cap; multiplier = 0.75."""
    n = 130
    a, b = _correlated_returns(n, seed=3)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5, "XAUUSD": [0] * 125 + [1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    # Pre-governor: heat ≈ 2r = 0.02 (2 perfectly correlated 1% positions).
    np.testing.assert_allclose(result.portfolio_heat_pre.iloc[-1], 0.02, atol=1e-6)
    # Post: capped at 0.015.
    np.testing.assert_allclose(result.portfolio_heat_post.iloc[-1], 0.015, atol=1e-6)
    # Multiplier: 0.015 / 0.02 = 0.75.
    np.testing.assert_allclose(result.multipliers.iloc[-1].to_numpy(), [0.75, 0.75], atol=1e-6)
    assert result.binding.iloc[-1]


def test_perfectly_correlated_opposite_directions_unbinds() -> None:
    """rho≈1, opposite directions: w'Cw = r²+r²-2r² = 0; heat = 0."""
    n = 130
    a, b = _correlated_returns(n, seed=5)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5, "XAUUSD": [0] * 125 + [-1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    # Long-short with rho=1 perfectly hedges -> heat ≈ 0.
    last_heat = result.portfolio_heat_pre.iloc[-1]
    assert last_heat < 1e-6
    # No binding when heat is below cap.
    assert not result.binding.iloc[-1]


def test_post_heat_never_exceeds_cap() -> None:
    """Post-governor heat must always be <= cap (within tolerance)."""
    n = 130
    a, b = _correlated_returns(n, seed=9)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 100 + [1] * 30, "XAUUSD": [0] * 100 + [1] * 30},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    cap = 0.015
    assert (result.portfolio_heat_post <= cap + 1e-9).all()


# ---------- correlation floor ----------

def test_negative_correlation_floored_at_zero() -> None:
    """rho≈-1 with floor=0: heat = r*sqrt(2), NOT zero."""
    n = 130
    rng = np.random.default_rng(11)
    a = rng.normal(0, 0.01, n).tolist()
    b = [-x for x in a]  # rho ≈ -1
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5, "XAUUSD": [0] * 125 + [1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    # With floor=0, even rho=-1 is treated as 0, so heat = r*sqrt(2),
    # NOT zero (the conservative H015-graveyard treatment).
    last_heat = result.portfolio_heat_pre.iloc[-1]
    np.testing.assert_allclose(last_heat, 0.01 * np.sqrt(2), atol=1e-6)


def test_floor_can_be_raised() -> None:
    """Custom floor > 0 inflates heat for low-corr pairs (more conservative)."""
    n = 130
    a, b = _independent_returns(n, seed=13)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 125 + [1] * 5, "XAUUSD": [0] * 125 + [1] * 5},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    cfg = HeatConfig(correlation_floor=0.5)
    result = heat_governor(sig, rets, cfg)
    # With floor=0.5, heat = r*sqrt(1+1+2*0.5) = r*sqrt(3) ≈ 0.01732.
    last_heat = result.portfolio_heat_pre.iloc[-1]
    np.testing.assert_allclose(last_heat, 0.01 * np.sqrt(3), atol=1e-6)
    # Now over the 1.5% cap, should bind.
    assert result.binding.iloc[-1]


# ---------- output structure ----------

def test_result_is_heat_result_dataclass() -> None:
    n = 130
    a, b = _independent_returns(n)
    sig = pd.DataFrame(
        {"USDJPY": [0] * n, "XAUUSD": [0] * n},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    assert isinstance(result, HeatResult)


def test_multipliers_indexed_like_signals() -> None:
    n = 130
    a, b = _independent_returns(n)
    sig = pd.DataFrame(
        {"USDJPY": [0] * n, "XAUUSD": [0] * n},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    assert result.multipliers.index.equals(sig.index)
    assert list(result.multipliers.columns) == list(sig.columns)


def test_multipliers_all_in_zero_one() -> None:
    n = 130
    a, b = _correlated_returns(n, seed=17)
    sig = pd.DataFrame(
        {"USDJPY": ([0] * 100 + [1, -1, 1, -1, 1] * 6),
         "XAUUSD": ([0] * 100 + [1, 1, -1, -1, 1] * 6)},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    result = heat_governor(sig, rets)
    flat = result.multipliers.to_numpy().flatten()
    assert (flat >= 0.0 - 1e-12).all()
    assert (flat <= 1.0 + 1e-12).all()


# ---------- determinism + edges ----------

def test_governor_is_deterministic() -> None:
    """Same input + same config -> bit-for-bit identical output."""
    n = 130
    a, b = _correlated_returns(n, seed=23)
    sig = pd.DataFrame(
        {"USDJPY": [0] * 100 + [1] * 30, "XAUUSD": [0] * 100 + [1] * 30},
        index=pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC"),
    )
    rets = pd.DataFrame({"USDJPY": a, "XAUUSD": b}, index=sig.index)
    r1 = heat_governor(sig, rets)
    r2 = heat_governor(sig, rets)
    pd.testing.assert_frame_equal(r1.multipliers, r2.multipliers)
    pd.testing.assert_series_equal(r1.portfolio_heat_pre, r2.portfolio_heat_pre)
    pd.testing.assert_series_equal(r1.portfolio_heat_post, r2.portfolio_heat_post)
    pd.testing.assert_series_equal(r1.binding, r2.binding)