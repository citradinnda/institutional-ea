from __future__ import annotations

"""tests/test_integration_h017_pipeline.py

Phase 2.6c-ii hermetic integration test for the Phase 2.6b real-data
pipeline.

Pipeline under test
-------------------
load_mt5_csv -> detect_d1_leakage -> trim_to_common_start ->
backtest_h017 -> build_h017_claim

Why hermetic
------------
- No real CSVs.
- No network.
- No wall-clock dependence.
- Synthetic prices generated deterministically (sinusoid), no RNG.
- The fixture-builder code IS the spec for what each CSV contains.
"""

import math
from pathlib import Path

import pandas as pd
import pytest

from quantcore.data.leakage import detect_d1_leakage, trim_to_common_start
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.strategy.h017_claim import (
    H017BacktestResult,
    H017Claim,
    backtest_h017,
    build_h017_claim,
)


MT5_HEADER = (
    "<DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\t<VOL>\t<SPREAD>"
)


def _format_mt5_row(ts: pd.Timestamp, price: float) -> str:
    """Format a single MT5 CSV row in broker-local tab-separated form."""
    date_s = ts.strftime("%Y.%m.%d")
    time_s = ts.strftime("%H:%M:%S")
    h = price + 0.05
    low = price - 0.05
    return (
        f"{date_s}\t{time_s}\t{price:.5f}\t{h:.5f}\t{low:.5f}\t"
        f"{price:.5f}\t100\t0\t10"
    )


def _build_mt5_csv_content(
    *,
    n_d1_dates: int,
    n_h4_trading_days: int,
    base_price: float,
    amplitude: float,
    period_bars: int,
    start_broker: pd.Timestamp,
) -> str:
    """Construct MT5-format CSV content as a single string.

    Layout:
        - n_d1_dates D1-disguised bars (1 bar/weekday at 00:00:00).
        - n_h4_trading_days real H4 weekdays (6 bars/day at
          00/04/08/12/16/20 broker time).

    Prices follow a deterministic sinusoid; weekends are skipped to
    mirror real FX market hours.
    """
    rows: list[str] = [MT5_HEADER]
    bar_idx = 0
    cur = start_broker

    def _next_weekday(ts: pd.Timestamp) -> pd.Timestamp:
        while ts.weekday() >= 5:  # 5=Sat, 6=Sun
            ts = ts + pd.Timedelta(days=1)
        return ts

    def _price(i: int) -> float:
        return base_price + amplitude * math.sin(2 * math.pi * i / period_bars)

    # D1-disguised prefix: one bar per WEEKDAY at 00:00:00 broker time.
    cur = _next_weekday(cur)
    for _ in range(n_d1_dates):
        ts = cur.normalize()
        rows.append(_format_mt5_row(ts, _price(bar_idx)))
        bar_idx += 1
        cur = _next_weekday(cur + pd.Timedelta(days=1))

    # Real H4 region: six bars per WEEKDAY at 00/04/08/12/16/20.
    for _ in range(n_h4_trading_days):
        for hour in (0, 4, 8, 12, 16, 20):
            ts = cur.normalize() + pd.Timedelta(hours=hour)
            rows.append(_format_mt5_row(ts, _price(bar_idx)))
            bar_idx += 1
        cur = _next_weekday(cur + pd.Timedelta(days=1))

    return "\n".join(rows) + "\n"


@pytest.fixture
def synthetic_mt5_csvs(tmp_path: Path) -> tuple[Path, Path]:
    """Write two synthetic MT5 CSVs to a temp dir.

    USDJPY-shaped: base_price=150, amplitude=2.0.
    XAUUSD-shaped: base_price=2000, amplitude=40.0, slightly different
    period to ensure the inner-join inside backtest_h017 actually
    intersects rather than coincides bar-for-bar.

    5 D1-disguised dates + 60 H4 trading days each. 60 weekdays * 6
    bars/day = 360 H4 bars per symbol, well above the warm-up needs of
    ATR(14) + Donchian(20) + vol_target(20).
    """
    start = pd.Timestamp("2024-01-01 00:00:00")
    usdjpy_csv = _build_mt5_csv_content(
        n_d1_dates=5,
        n_h4_trading_days=60,
        base_price=150.0,
        amplitude=2.0,
        period_bars=80,
        start_broker=start,
    )
    xauusd_csv = _build_mt5_csv_content(
        n_d1_dates=5,
        n_h4_trading_days=60,
        base_price=2000.0,
        amplitude=40.0,
        period_bars=96,
        start_broker=start,
    )
    u_path = tmp_path / "USDJPY_H4.csv"
    x_path = tmp_path / "XAUUSD_H4.csv"
    u_path.write_text(usdjpy_csv, encoding="utf-8")
    x_path.write_text(xauusd_csv, encoding="utf-8")
    return u_path, x_path


def test_loader_to_leakage_to_trim_chain(
    synthetic_mt5_csvs: tuple[Path, Path],
) -> None:
    """First link: loader produces canonical UTC frames; leakage scanner
    correctly identifies the 5 D1-disguised dates; trim drops them."""
    u_path, x_path = synthetic_mt5_csvs

    u_load = load_mt5_csv(u_path)
    x_load = load_mt5_csv(x_path)

    # Canonical OHLCV invariants per Phase 1.
    assert str(u_load.bars.index.tz) == "UTC"
    assert list(u_load.bars.columns) == ["open", "high", "low", "close", "volume"]
    assert u_load.bars.index.is_monotonic_increasing
    assert not u_load.bars.index.has_duplicates

    # 5 D1 + 60*6 H4 = 365 input rows -> 365 output bars.
    assert u_load.n_bars == 365
    assert x_load.n_bars == 365

    u_scan = detect_d1_leakage(u_load.bars, broker_tz="Europe/Athens")
    x_scan = detect_d1_leakage(x_load.bars, broker_tz="Europe/Athens")

    # 5 D1 weekdays were prepended; both should see exactly 5 leaked.
    assert u_scan.leaked_dates == 5
    assert x_scan.leaked_dates == 5

    # Trim using the later of the two cutoffs (UTC midnight).
    cutoff = max(
        pd.Timestamp(u_scan.first_reliable_date.date(), tz="UTC"),
        pd.Timestamp(x_scan.first_reliable_date.date(), tz="UTC"),
    )
    u_trim, x_trim = trim_to_common_start(u_load.bars, x_load.bars, cutoff)

    # Post-trim: both frames start at-or-after cutoff, retain most bars.
    assert (u_trim.index >= cutoff).all()
    assert (x_trim.index >= cutoff).all()
    assert len(u_trim) >= 350  # 5 D1 trimmed; some H4 may also drop if cutoff is generous
    assert len(x_trim) >= 350


def test_full_pipeline_produces_valid_h017_claim(
    synthetic_mt5_csvs: tuple[Path, Path],
) -> None:
    """End-to-end: loader -> leakage -> trim -> backtest -> claim.

    Asserts the SHAPE of the result (types, finiteness, gate booleans
    are real bools), NOT a specific numeric Sharpe. Synthetic sinusoid
    prices have no claim to a particular edge; we just verify the chain
    runs without raising and produces a well-formed claim.
    """
    u_path, x_path = synthetic_mt5_csvs

    u_load = load_mt5_csv(u_path)
    x_load = load_mt5_csv(x_path)

    u_scan = detect_d1_leakage(u_load.bars, broker_tz="Europe/Athens")
    x_scan = detect_d1_leakage(x_load.bars, broker_tz="Europe/Athens")
    cutoff = max(
        pd.Timestamp(u_scan.first_reliable_date.date(), tz="UTC"),
        pd.Timestamp(x_scan.first_reliable_date.date(), tz="UTC"),
    )
    u_trim, x_trim = trim_to_common_start(u_load.bars, x_load.bars, cutoff)

    bt = backtest_h017(u_trim, x_trim)
    assert isinstance(bt, H017BacktestResult)
    assert bt.n_bars > 0
    assert len(bt.portfolio_returns) == bt.n_bars
    # No infinities; NaNs allowed during warm-up only.
    finite_or_nan = bt.portfolio_returns.replace([float("inf"), float("-inf")], pd.NA)
    assert finite_or_nan.notna().sum() > 0  # at least some real returns

    claim = build_h017_claim(
        bt.portfolio_returns,
        periods_per_year=1512,
        sr_estimates=None,
    )
    assert isinstance(claim, H017Claim)
    assert isinstance(claim.promotable, bool)
    assert isinstance(claim.summary, str)
    assert "PROMOTABLE" in claim.summary  # ASCII-only summary per §6


def test_pipeline_rejects_naive_cutoff(
    synthetic_mt5_csvs: tuple[Path, Path],
) -> None:
    """Regression guard: trim_to_common_start must reject tz-naive
    timestamps. This is one of the repo's documented footguns."""
    u_path, x_path = synthetic_mt5_csvs
    u_load = load_mt5_csv(u_path)
    x_load = load_mt5_csv(x_path)

    naive = pd.Timestamp("2024-01-10")  # no tz
    with pytest.raises(ValueError, match="tz-aware"):
        trim_to_common_start(u_load.bars, x_load.bars, naive)