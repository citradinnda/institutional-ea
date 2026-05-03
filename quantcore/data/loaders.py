"""Data loaders for FX/CFD historical data.

All loaders return a canonical OHLCV DataFrame:
    - columns: open, high, low, close, volume (lowercase)
    - index: pandas DatetimeIndex in UTC timezone
    - no duplicate timestamps, sorted ascending
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pandas as pd


CANONICAL_COLS = ["open", "high", "low", "close", "volume"]
Timeframe = Literal["M1", "M5", "M15", "H1", "H4", "D1"]


@dataclass(frozen=True)
class BarsRequest:
    """A request for a specific symbol/timeframe/date range."""
    symbol: str
    timeframe: Timeframe
    start: pd.Timestamp
    end: pd.Timestamp


def _ensure_canonical(df: pd.DataFrame) -> pd.DataFrame:
    """Force a DataFrame into canonical OHLCV form."""
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]

    missing = [c for c in CANONICAL_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[CANONICAL_COLS]

    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("Index must be a pandas DatetimeIndex")

    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")

    df = df[~df.index.duplicated(keep="first")].sort_index()

    return df
# ---------------------------------------------------------------------------
# Public alias (added Phase 2.6a).
#
# WHY: §6 of the project conventions treats `ensure_canonical` as part of the
# canonical-OHLCV public contract. Other modules (mt5_loader, future Phase 3
# engine) need to import it by a public name. The original underscore-prefixed
# definition is retained because tests/test_loaders.py imports it by that name
# and we never break already-passing tests (Handoff §8). The alias is an
# identity binding, so behavior is bit-for-bit identical.
# ---------------------------------------------------------------------------
ensure_canonical = _ensure_canonical


def load_parquet(path: str | Path) -> pd.DataFrame:
    """Load OHLCV from a parquet file."""
    df = pd.read_parquet(path)
    return _ensure_canonical(df)


def load_histdata_csv(path: str | Path, timeframe: Timeframe = "M1") -> pd.DataFrame:
    """Load HistData.com ASCII M1 CSV.

    Format: YYYYMMDD HHMMSS;open;high;low;close;volume
    """
    df = pd.read_csv(
        path,
        sep=";",
        header=None,
        names=["dt", "open", "high", "low", "close", "volume"],
    )
    df["dt"] = pd.to_datetime(df["dt"], format="%Y%m%d %H%M%S", utc=True)
    df = df.set_index("dt")
    df = _ensure_canonical(df)
    if timeframe != "M1":
        df = resample(df, timeframe)
    return df


def resample(df: pd.DataFrame, timeframe: Timeframe) -> pd.DataFrame:
    """Resample lower-timeframe OHLCV to a higher timeframe.

    Uses MT5-compatible bar labeling: each bar's timestamp is its OPEN time,
    and the bar contains data from [open_time, open_time + timeframe).

    Example: an H4 bar at 04:00 contains hours 04, 05, 06, 07.
    """
    rule_map = {
        "M1": "1min",
        "M5": "5min",
        "M15": "15min",
        "H1": "1h",
        "H4": "4h",
        "D1": "1D",
    }
    rule = rule_map[timeframe]
    out = df.resample(rule, label="left", closed="left").agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    )
    return out.dropna()