from __future__ import annotations

"""Tests for Phase 2.2 per-symbol signal generators.

Coverage targets (~25 tests):
    - SignalConfig validation (3)
    - Input validation / canonical-OHLCV guards (4)
    - Donchian engine: warm-up, breakout, hold, flip, no-signal (8)
    - ATR floor suppression (4)
    - USDJPY wrapper (3)
    - XAUUSD wrapper (3)
    - Determinism / reproducibility (1)
"""

import numpy as np
import pandas as pd
import pytest

from quantcore.indicators import average_true_range
from quantcore.strategy import (
    SignalConfig,
    donchian_signal,
    usdjpy_trend_signal,
    xauusd_trend_signal,
)


# ---------- helpers ----------

def _make_ohlcv(closes: list[float], freq: str = "4h") -> pd.DataFrame:
    """Build a canonical OHLCV frame from a close-price path.

    high = close * 1.001, low = close * 0.999, open = previous close.
    Volume is constant. Index is UTC, hourly-multiple frequency.
    """
    n = len(closes)
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    closes_arr = np.asarray(closes, dtype=float)
    opens = np.concatenate([[closes_arr[0]], closes_arr[:-1]])
    highs = np.maximum(opens, closes_arr) * 1.001
    lows = np.minimum(opens, closes_arr) * 0.999
    return pd.DataFrame(
        {
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes_arr,
            "volume": np.full(n, 1000.0),
        },
        index=idx,
    )


def _make_breakout_path(
    n_warmup: int = 25,
    base: float = 100.0,
    breakout_up: bool = True,
) -> pd.DataFrame:
    """Build a path that holds flat for n_warmup bars then breaks out.

    Used to test that the first breakout fires at the right bar.
    """
    flat = [base] * n_warmup
    move = [base + (i + 1) * 0.5 if breakout_up else base - (i + 1) * 0.5 for i in range(10)]
    return _make_ohlcv(flat + move)


# ---------- SignalConfig validation ----------

def test_signal_config_defaults() -> None:
    cfg = SignalConfig()
    assert cfg.lookback == 20
    assert cfg.min_atr_pct is None
    assert cfg.atr_col == "atr14"


def test_signal_config_rejects_lookback_below_2() -> None:
    with pytest.raises(ValueError, match="lookback must be >= 2"):
        SignalConfig(lookback=1)


def test_signal_config_rejects_negative_atr_pct() -> None:
    with pytest.raises(ValueError, match="min_atr_pct must be >= 0"):
        SignalConfig(min_atr_pct=-0.01)


# ---------- input validation ----------

def test_rejects_missing_columns() -> None:
    df = pd.DataFrame(
        {"close": [1.0, 2.0]},
        index=pd.date_range("2024-01-01", periods=2, freq="4h", tz="UTC"),
    )
    with pytest.raises(ValueError, match="missing required canonical columns"):
        donchian_signal(df, SignalConfig(lookback=2))


def test_rejects_non_datetime_index() -> None:
    df = _make_ohlcv([100.0] * 30)
    df = df.reset_index(drop=True)
    with pytest.raises(TypeError, match="DatetimeIndex"):
        donchian_signal(df, SignalConfig(lookback=20))


def test_rejects_duplicated_index() -> None:
    df = _make_ohlcv([100.0] * 30)
    bad_index = df.index.tolist()
    bad_index[5] = bad_index[4]
    df.index = pd.DatetimeIndex(bad_index)
    with pytest.raises(ValueError, match="duplicates"):
        donchian_signal(df, SignalConfig(lookback=20))


def test_rejects_unsorted_index() -> None:
    df = _make_ohlcv([100.0] * 30)
    df = df.iloc[::-1]
    with pytest.raises(ValueError, match="sorted ascending"):
        donchian_signal(df, SignalConfig(lookback=20))


# ---------- Donchian engine ----------

def test_warmup_bars_are_nan() -> None:
    """First `lookback` bars have no channel and must be NaN."""
    df = _make_ohlcv([100.0] * 30)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    assert sig.iloc[:20].isna().all()
    assert not sig.iloc[20:].isna().any()


def test_short_input_returns_all_nan() -> None:
    """If len(df) <= lookback, signal is fully NaN (no crash)."""
    df = _make_ohlcv([100.0] * 5)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    assert sig.isna().all()
    assert len(sig) == 5


def test_long_breakout_fires_on_correct_bar() -> None:
    """Breakout above prior 20-bar high triggers +1 on that bar."""
    df = _make_breakout_path(n_warmup=25, base=100.0, breakout_up=True)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    # First 20 bars are warm-up. Bars 20..24 are flat (no breakout).
    # Bar 25 onward is the breakout move.
    assert (sig.iloc[20:25] == 0.0).all()
    assert sig.iloc[25] == 1.0


def test_short_breakout_fires_on_correct_bar() -> None:
    df = _make_breakout_path(n_warmup=25, base=100.0, breakout_up=False)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    assert (sig.iloc[20:25] == 0.0).all()
    assert sig.iloc[25] == -1.0


def test_signal_holds_between_breakouts() -> None:
    """After a long breakout, signal stays +1 until an opposite break."""
    df = _make_breakout_path(n_warmup=25, base=100.0, breakout_up=True)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    assert (sig.iloc[25:] == 1.0).all()


def test_signal_flips_on_opposite_breakout() -> None:
    """+1 → -1 transition fires on the bar that breaks the prior low."""
    n_warmup = 25
    up_leg = [100.0 + (i + 1) * 0.5 for i in range(15)]  # break above
    down_leg = [up_leg[-1] - (i + 1) * 1.5 for i in range(20)]  # break below
    closes = [100.0] * n_warmup + up_leg + down_leg
    df = _make_ohlcv(closes)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    # Should be +1 somewhere in the up leg, -1 somewhere in the down leg.
    assert (sig == 1.0).any()
    assert (sig == -1.0).any()
    # And the last value should be -1 (we ended on a sustained downtrend).
    assert sig.iloc[-1] == -1.0


def test_no_breakout_stays_flat() -> None:
    """Pure flat input → all post-warmup signals are 0."""
    df = _make_ohlcv([100.0] * 50)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    assert (sig.iloc[20:] == 0.0).all()


def test_signal_values_only_in_allowed_set() -> None:
    """After dropna, every value must be in {-1, 0, +1}."""
    n_warmup = 25
    closes = [100.0] * n_warmup + [100.0 + i * 0.5 for i in range(15)]
    df = _make_ohlcv(closes)
    sig = donchian_signal(df, SignalConfig(lookback=20)).dropna()
    assert set(sig.unique()).issubset({-1.0, 0.0, 1.0})


def test_output_is_named_signal() -> None:
    df = _make_ohlcv([100.0] * 30)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    assert sig.name == "signal"


def test_output_index_matches_input() -> None:
    df = _make_ohlcv([100.0] * 30)
    sig = donchian_signal(df, SignalConfig(lookback=20))
    assert sig.index.equals(df.index)


# ---------- ATR floor suppression ----------

def test_atr_floor_requires_atr_column() -> None:
    df = _make_ohlcv([100.0] * 30)
    cfg = SignalConfig(lookback=20, min_atr_pct=0.01, atr_col="atr14")
    with pytest.raises(ValueError, match="not in DataFrame"):
        donchian_signal(df, cfg)


def test_atr_floor_suppresses_breakout_when_vol_too_low() -> None:
    """When ATR/close < floor, even a price breakout is ignored."""
    df = _make_breakout_path(n_warmup=25, base=100.0, breakout_up=True)
    df["atr14"] = 0.001  # ATR/close ≈ 0.00001, well below any sane floor
    cfg = SignalConfig(lookback=20, min_atr_pct=0.01, atr_col="atr14")
    sig = donchian_signal(df, cfg)
    # No breakout should fire — signal stays flat post warm-up.
    assert (sig.iloc[20:] == 0.0).all()


def test_atr_floor_allows_breakout_when_vol_high_enough() -> None:
    df = _make_breakout_path(n_warmup=25, base=100.0, breakout_up=True)
    df["atr14"] = 5.0  # ATR/close ≈ 0.05, well above floor
    cfg = SignalConfig(lookback=20, min_atr_pct=0.01, atr_col="atr14")
    sig = donchian_signal(df, cfg)
    assert sig.iloc[25] == 1.0


def test_atr_floor_zero_is_permissive() -> None:
    """min_atr_pct=0 allows everything (only NaN ATR is suppressed)."""
    df = _make_breakout_path(n_warmup=25, base=100.0, breakout_up=True)
    df["atr14"] = 0.5
    cfg = SignalConfig(lookback=20, min_atr_pct=0.0, atr_col="atr14")
    sig = donchian_signal(df, cfg)
    assert sig.iloc[25] == 1.0


# ---------- USDJPY wrapper ----------

def test_usdjpy_default_config_no_atr_filter() -> None:
    """USDJPY default has no ATR floor, so no atr column needed."""
    df = _make_breakout_path(n_warmup=25, base=150.0, breakout_up=True)
    sig = usdjpy_trend_signal(df)
    assert sig.iloc[25] == 1.0


def test_usdjpy_accepts_config_override() -> None:
    df = _make_breakout_path(n_warmup=15, base=150.0, breakout_up=True)
    sig = usdjpy_trend_signal(df, SignalConfig(lookback=10))
    # Warm-up is now 10 bars, breakout move starts at index 15.
    assert sig.iloc[:10].isna().all()
    assert sig.iloc[15] == 1.0


def test_usdjpy_returns_named_series() -> None:
    df = _make_ohlcv([150.0] * 30)
    sig = usdjpy_trend_signal(df)
    assert sig.name == "signal"
    assert sig.index.equals(df.index)


# ---------- XAUUSD wrapper ----------

def test_xauusd_default_requires_atr_column() -> None:
    """XAUUSD default config has min_atr_pct set, so atr14 is required."""
    df = _make_ohlcv([2000.0] * 30)
    with pytest.raises(ValueError, match="not in DataFrame"):
        xauusd_trend_signal(df)


def test_xauusd_works_with_real_atr() -> None:
    """End-to-end: compute ATR via indicators, attach, run XAUUSD signal."""
    rng = np.random.default_rng(42)
    base = 2000.0
    n = 60
    # Trending path with realistic gold-like volatility.
    drift = np.linspace(0, 50, n)
    noise = rng.normal(0, 2.0, n)
    closes = (base + drift + noise).tolist()
    df = _make_ohlcv(closes)
    df["atr14"] = average_true_range(df, window=14)
    sig = xauusd_trend_signal(df)
    # After warm-up + ATR warm-up, we should see at least one +1.
    assert (sig.dropna() == 1.0).any()


def test_xauusd_accepts_config_override() -> None:
    """Override with a permissive config (no ATR floor) for testing.

    Builds an explicit path: at gold-scale prices (~2000), the synthetic
    high-wick in _make_ohlcv is ~2.0, so the breakout step must be larger
    than that to actually clear the prior 20-bar high. We use +10/bar.
    """
    n_warmup = 25
    base = 2000.0
    flat = [base] * n_warmup
    move = [base + (i + 1) * 10.0 for i in range(10)]
    df = _make_ohlcv(flat + move)
    sig = xauusd_trend_signal(df, SignalConfig(lookback=20, min_atr_pct=None))
    assert sig.iloc[25] == 1.0


# ---------- determinism ----------

def test_signal_is_deterministic() -> None:
    """Same input + same config → bit-for-bit identical output."""
    df = _make_breakout_path(n_warmup=25, base=100.0, breakout_up=True)
    cfg = SignalConfig(lookback=20)
    sig1 = donchian_signal(df, cfg)
    sig2 = donchian_signal(df, cfg)
    pd.testing.assert_series_equal(sig1, sig2)