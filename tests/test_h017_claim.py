from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.strategy.h017 import H017Config
from quantcore.strategy.h017_claim import (
    H017BacktestResult,
    H017Claim,
    backtest_h017,
    build_h017_claim,
)


# ---------- Synthetic data helpers ----------

def _make_ohlcv(
    n_bars: int = 400,
    start: float = 100.0,
    vol: float = 0.003,
    seed: int = 7,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2020-01-01", periods=n_bars, freq="4h", tz="UTC")
    rets = rng.normal(0.0, vol, size=n_bars)
    close = start * np.exp(np.cumsum(rets))
    high = close * (1.0 + np.abs(rng.normal(0, vol, n_bars)))
    low = close * (1.0 - np.abs(rng.normal(0, vol, n_bars)))
    open_ = np.concatenate([[start], close[:-1]])
    volume = rng.integers(100, 1000, n_bars).astype(float)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low,
         "close": close, "volume": volume},
        index=idx,
    )


def _strong_returns(n: int = 1500, seed: int = 42) -> pd.Series:
    """Returns with high Sharpe — should clear PSR and MinTRL gates."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2020-01-01", periods=n, freq="4h", tz="UTC")
    return pd.Series(rng.normal(0.001, 0.01, size=n), index=idx)


def _zero_returns(n: int = 1500, seed: int = 0) -> pd.Series:
    """Near-zero-edge noise: variance > 0, mean ~= 0.

    WHY: True zero-variance returns make Sharpe mathematically undefined,
    and probabilistic_sharpe_ratio correctly raises on that. To exercise
    the 'promotable=False because PSR fails' path we need real dispersion
    around a zero mean — Sharpe ~ 0, PSR ~ 0.5, well below the 0.95 gate.
    """
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2020-01-01", periods=n, freq="4h", tz="UTC")
    return pd.Series(rng.normal(0.0, 0.01, size=n), index=idx)


# ---------- backtest_h017 tests ----------

def test_backtest_result_is_frozen_dataclass():
    usdjpy = _make_ohlcv(seed=1)
    xauusd = _make_ohlcv(start=1800, vol=0.005, seed=2)
    result = backtest_h017(usdjpy, xauusd)
    assert isinstance(result, H017BacktestResult)
    with pytest.raises(Exception):
        result.n_bars = 0  # type: ignore[misc]


def test_backtest_returns_correct_shape():
    usdjpy = _make_ohlcv(seed=1)
    xauusd = _make_ohlcv(start=1800, vol=0.005, seed=2)
    result = backtest_h017(usdjpy, xauusd)
    assert len(result.portfolio_returns) == result.n_bars
    assert set(result.per_symbol_returns.columns) == {"USDJPY", "XAUUSD"}
    assert len(result.positions) == result.n_bars


def test_backtest_position_lag_no_lookahead():
    """Per-symbol return at t = position[t-1] * close.pct_change()[t]."""
    usdjpy = _make_ohlcv(seed=1)
    xauusd = _make_ohlcv(start=1800, vol=0.005, seed=2)
    result = backtest_h017(usdjpy, xauusd)

    usdjpy_ret = usdjpy["close"].reindex(result.positions.index).pct_change()
    expected_usdjpy = result.positions["USDJPY"].shift(1) * usdjpy_ret

    pd.testing.assert_series_equal(
        result.per_symbol_returns["USDJPY"],
        expected_usdjpy,
        check_names=False,
    )


def test_backtest_first_bar_per_symbol_returns_nan():
    """First bar has no prior position AND no prior close — must be NaN."""
    usdjpy = _make_ohlcv(seed=1)
    xauusd = _make_ohlcv(start=1800, vol=0.005, seed=2)
    result = backtest_h017(usdjpy, xauusd)
    assert pd.isna(result.per_symbol_returns.iloc[0]).all()


def test_backtest_portfolio_is_sum_of_per_symbol():
    usdjpy = _make_ohlcv(seed=1)
    xauusd = _make_ohlcv(start=1800, vol=0.005, seed=2)
    result = backtest_h017(usdjpy, xauusd)
    expected = result.per_symbol_returns.sum(axis=1, skipna=True)
    np.testing.assert_allclose(
        result.portfolio_returns.to_numpy(),
        expected.to_numpy(),
    )


def test_backtest_accepts_custom_config():
    usdjpy = _make_ohlcv(seed=1)
    xauusd = _make_ohlcv(start=1800, vol=0.005, seed=2)
    cfg = H017Config.default()
    result = backtest_h017(usdjpy, xauusd, config=cfg)
    assert result.n_bars > 0


# ---------- build_h017_claim tests ----------

def test_claim_is_frozen_dataclass():
    claim = build_h017_claim(_strong_returns())
    assert isinstance(claim, H017Claim)
    with pytest.raises(Exception):
        claim.promotable = False  # type: ignore[misc]


def test_claim_psr_always_runs():
    claim = build_h017_claim(_strong_returns())
    assert claim.psr is not None
    assert 0.0 <= claim.psr.psr <= 1.0


def test_claim_min_trl_always_runs():
    claim = build_h017_claim(_strong_returns())
    assert claim.min_trl is not None
    # Strong positive returns vs zero benchmark => MinTRL must be feasible.
    assert claim.min_trl.feasible is True


def test_claim_dsr_absent_when_no_sr_estimates():
    claim = build_h017_claim(_strong_returns())
    assert claim.dsr is None
    assert claim.n_trials is None


def test_claim_dsr_present_when_sr_estimates_given():
    sr_estimates = np.array([0.1, 0.2, -0.05, 0.3, 0.15])
    claim = build_h017_claim(_strong_returns(), sr_estimates=sr_estimates)
    assert claim.dsr is not None
    assert claim.n_trials == 5


def test_promotable_true_for_strong_returns():
    claim = build_h017_claim(_strong_returns())
    assert claim.promotable is True


def test_promotable_false_for_zero_edge_returns():
    """No edge => PSR ~ 0.5, fails the 0.95 gate, promotable must be False."""
    claim = build_h017_claim(_zero_returns())
    assert claim.promotable is False
    assert claim.psr.psr < 0.95


def test_promotable_false_when_min_trl_infeasible():
    """Per §6 MinTRL sentinel: observed_sr <= sr_benchmark => feasible=False."""
    # Benchmark above the strongest plausible observed annualized SR.
    claim = build_h017_claim(_strong_returns(), sr_benchmark=10.0)
    assert claim.min_trl.feasible is False
    assert claim.promotable is False


def test_summary_is_ascii_only():
    """Per §6 validator orchestrator: ASCII +/- only (PowerShell-safe)."""
    claim = build_h017_claim(_strong_returns())
    claim.summary.encode("ascii")  # raises if any non-ASCII glyph snuck in.
    assert "PROMOTABLE" in claim.summary


def test_n_bars_excludes_nan():
    """n_bars on the claim reflects clean (non-NaN) sample size."""
    rets = _strong_returns().copy()
    rets.iloc[0:5] = np.nan
    claim = build_h017_claim(rets)
    assert claim.n_bars == len(rets) - 5


def test_periods_per_year_propagates():
    claim = build_h017_claim(_strong_returns(), periods_per_year=1512)
    assert claim.periods_per_year == 1512
    assert "ppy=1512" in claim.summary