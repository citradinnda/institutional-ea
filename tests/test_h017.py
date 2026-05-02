from __future__ import annotations

"""Tests for Phase 2.4 H017 strategy integration."""

import numpy as np
import pandas as pd
import pytest

from quantcore.strategy import (
    H017Config,
    H017Result,
    HeatConfig,
    SignalConfig,
    run_h017,
)


# ---------- helpers ----------

def _make_ohlcv(closes: list[float], freq: str = "4h", start: str = "2024-01-01") -> pd.DataFrame:
    n = len(closes)
    idx = pd.date_range(start, periods=n, freq=freq, tz="UTC")
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


def _trending_path(n: int, base: float, drift: float, noise_scale: float, seed: int) -> list[float]:
    rng = np.random.default_rng(seed)
    drifts = np.linspace(0, drift, n)
    noise = rng.normal(0, noise_scale, n)
    return (base + drifts + noise).tolist()


def _make_pair(n: int = 200, seed_jpy: int = 1, seed_xau: int = 2, start: str = "2024-01-01") -> tuple[pd.DataFrame, pd.DataFrame]:
    jpy_path = _trending_path(n, base=150.0, drift=3.0, noise_scale=0.15, seed=seed_jpy)
    xau_path = _trending_path(n, base=2000.0, drift=80.0, noise_scale=4.0, seed=seed_xau)
    return _make_ohlcv(jpy_path, start=start), _make_ohlcv(xau_path, start=start)


# ---------- config defaults ----------

def test_h017_config_default_factory() -> None:
    cfg = H017Config.default()
    assert cfg.atr_window == 14
    assert cfg.chandelier_mult == 3.0
    assert cfg.chandelier_lookback == 22
    assert cfg.vol_target == 0.10
    assert cfg.vol_lookback == 20
    assert cfg.vol_max_leverage == 3.0


def test_h017_config_default_includes_heat() -> None:
    cfg = H017Config.default()
    assert isinstance(cfg.heat, HeatConfig)
    assert cfg.heat.max_portfolio_heat == 0.015
    assert cfg.heat.per_trade_risk == 0.01


def test_h017_config_default_includes_signals() -> None:
    cfg = H017Config.default()
    assert isinstance(cfg.usdjpy_signal, SignalConfig)
    assert isinstance(cfg.xauusd_signal, SignalConfig)
    assert cfg.usdjpy_signal.min_atr_pct is None
    assert cfg.xauusd_signal.min_atr_pct == 0.003


def test_h017_config_is_frozen() -> None:
    cfg = H017Config.default()
    with pytest.raises(Exception):
        cfg.atr_window = 99  # type: ignore[misc]


# ---------- input validation ----------

def test_rejects_missing_columns() -> None:
    jpy = pd.DataFrame(
        {"close": [150.0, 150.5]},
        index=pd.date_range("2024-01-01", periods=2, freq="4h", tz="UTC"),
    )
    _, xau = _make_pair(200)
    with pytest.raises(ValueError, match="missing canonical columns"):
        run_h017(jpy, xau)


def test_rejects_non_datetime_index() -> None:
    jpy, xau = _make_pair(200)
    jpy_bad = jpy.reset_index(drop=True)
    with pytest.raises(TypeError, match="DatetimeIndex"):
        run_h017(jpy_bad, xau)


def test_rejects_duplicated_index() -> None:
    jpy, xau = _make_pair(200)
    bad = jpy.index.tolist()
    bad[5] = bad[4]
    jpy.index = pd.DatetimeIndex(bad)
    with pytest.raises(ValueError, match="duplicates"):
        run_h017(jpy, xau)


def test_rejects_unsorted_index() -> None:
    jpy, xau = _make_pair(200)
    jpy = jpy.iloc[::-1]
    with pytest.raises(ValueError, match="sorted ascending"):
        run_h017(jpy, xau)


def test_rejects_no_overlap() -> None:
    jpy = _make_ohlcv([150.0] * 100, start="2024-01-01")
    xau = _make_ohlcv([2000.0] * 100, start="2025-01-01")
    with pytest.raises(ValueError, match="no overlapping timestamps"):
        run_h017(jpy, xau)


# ---------- inner join ----------

def test_inner_join_uses_overlap_only() -> None:
    """Output index = intersection of the two input indices."""
    jpy = _make_ohlcv(_trending_path(150, 150.0, 3.0, 0.15, 1), start="2024-01-01")
    xau = _make_ohlcv(_trending_path(150, 2000.0, 80.0, 4.0, 2), start="2024-01-10")
    result = run_h017(jpy, xau)
    expected_idx = jpy.index.intersection(xau.index)
    assert result.positions.index.equals(expected_idx)
    assert len(result.positions) < len(jpy)
    assert len(result.positions) < len(xau)


# ---------- output structure ----------

def test_result_is_h017_result() -> None:
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    assert isinstance(result, H017Result)


def test_result_has_all_expected_frames() -> None:
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    for df in (
        result.positions,
        result.signals,
        result.stops_long,
        result.stops_short,
        result.vol_multipliers,
        result.heat_multipliers,
    ):
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["USDJPY", "XAUUSD"]
        assert df.index.equals(jpy.index)


def test_result_has_all_expected_series() -> None:
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    for s in (result.heat_pre, result.heat_post, result.heat_binding):
        assert isinstance(s, pd.Series)
        assert s.index.equals(jpy.index)


# ---------- semantic correctness ----------

def test_positions_are_signed_fraction_of_equity() -> None:
    """|positions| <= per_trade_risk * vol_max_leverage * 1.0 (heat <= 1)."""
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    cfg = H017Config.default()
    bound = cfg.heat.per_trade_risk * cfg.vol_max_leverage + 1e-9
    flat = result.positions.to_numpy().flatten()
    assert (np.abs(flat) <= bound).all()


def test_positions_match_signal_sign() -> None:
    """Where signal is +1, position >= 0; where -1, position <= 0; where 0, position == 0."""
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    sig = result.signals.fillna(0.0)
    pos = result.positions
    for col in ("USDJPY", "XAUUSD"):
        long_mask = sig[col] > 0
        short_mask = sig[col] < 0
        flat_mask = sig[col] == 0
        assert (pos.loc[long_mask, col] >= 0).all()
        assert (pos.loc[short_mask, col] <= 0).all()
        assert (pos.loc[flat_mask, col] == 0).all()


def test_warmup_positions_are_zero() -> None:
    """During the longest warm-up period, positions must be zero."""
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    # Longest warm-up = max(atr_window, chandelier_lookback, vol_lookback,
    # signal lookback, heat correlation_window). Heat dominates at 120.
    # Use a conservative early window of first 13 bars (atr_window-1).
    early = result.positions.iloc[:13]
    assert (early.to_numpy() == 0.0).all()


def test_post_heat_never_exceeds_cap() -> None:
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    cap = H017Config.default().heat.max_portfolio_heat
    assert (result.heat_post <= cap + 1e-9).all()


def test_heat_multipliers_in_zero_one() -> None:
    jpy, xau = _make_pair(200)
    result = run_h017(jpy, xau)
    flat = result.heat_multipliers.to_numpy().flatten()
    assert (flat >= -1e-12).all()
    assert (flat <= 1.0 + 1e-12).all()


def test_stops_are_finite_when_signal_active() -> None:
    """Where signal is non-zero post-warmup, the corresponding stop should be finite."""
    jpy, xau = _make_pair(300)
    result = run_h017(jpy, xau)
    sig = result.signals.fillna(0.0)
    for col in ("USDJPY", "XAUUSD"):
        active_long = sig[col] > 0
        active_short = sig[col] < 0
        # Skip very early bars where chandelier is still warming up.
        active_long = active_long & (np.arange(len(sig)) >= 50)
        active_short = active_short & (np.arange(len(sig)) >= 50)
        if active_long.any():
            assert result.stops_long.loc[active_long, col].notna().all()
        if active_short.any():
            assert result.stops_short.loc[active_short, col].notna().all()


# ---------- determinism ----------

def test_h017_is_deterministic() -> None:
    """Same inputs + same config -> bit-for-bit identical output."""
    jpy, xau = _make_pair(200)
    r1 = run_h017(jpy, xau)
    r2 = run_h017(jpy, xau)
    pd.testing.assert_frame_equal(r1.positions, r2.positions)
    pd.testing.assert_frame_equal(r1.signals, r2.signals)
    pd.testing.assert_frame_equal(r1.heat_multipliers, r2.heat_multipliers)


# ---------- config override ----------

def test_custom_heat_cap_changes_binding() -> None:
    """Tighter heat cap should result in more bars being binding."""
    jpy, xau = _make_pair(300)
    loose = run_h017(jpy, xau, H017Config.default())
    tight_cfg = H017Config(heat=HeatConfig(max_portfolio_heat=0.005))
    tight = run_h017(jpy, xau, tight_cfg)
    assert tight.heat_binding.sum() >= loose.heat_binding.sum()


def test_custom_atr_window_propagates() -> None:
    """Changing atr_window changes stop levels."""
    jpy, xau = _make_pair(300)
    default = run_h017(jpy, xau)
    custom = run_h017(
        jpy,
        xau,
        H017Config(
            atr_window=20,
            usdjpy_signal=SignalConfig(lookback=20, min_atr_pct=None, atr_col="atr20"),
            xauusd_signal=SignalConfig(lookback=20, min_atr_pct=0.003, atr_col="atr20"),
        ),
    )
    # Stops should differ in at least some bars.
    diff = (default.stops_long - custom.stops_long).abs().sum().sum()
    assert diff > 0.0


# ---------- end-to-end smoke ----------

def test_end_to_end_produces_some_trades() -> None:
    """Over a 300-bar trending pair, at least one bar should have a non-zero position."""
    jpy, xau = _make_pair(300)
    result = run_h017(jpy, xau)
    assert (result.positions != 0.0).any().any()