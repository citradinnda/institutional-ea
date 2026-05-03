"""Dukascopy CSV loader.

The observed Dukascopy sample format is comma-separated with columns:

    UTC,Open,High,Low,Close,Volume

Observed timestamp example:

    03.01.2024 00:00:00.000 UTC

WHY this is separate from mt5_loader.py:
    MT5 exports use broker wall-clock time and need broker timezone conversion.
    Dukascopy sample timestamps are explicitly labeled UTC, so broker timezone
    localization would be wrong here.

This loader is infrastructure only. Its existence does not mean Dukascopy is an
accepted research source for H017.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.data.loaders import ensure_canonical


_DUKASCOPY_REQUIRED_COLUMNS: tuple[str, ...] = (
    "UTC",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
)

_DUKASCOPY_TIMESTAMP_FORMAT: str = "%d.%m.%Y %H:%M:%S.%f UTC"


@dataclass(frozen=True)
class DukascopyLoadResult:
    """Structured result of loading a Dukascopy CSV file.

    Attributes
    ----------
    bars
        Canonical OHLCV DataFrame with lowercase open/high/low/close/volume
        columns and a UTC DatetimeIndex.
    n_bars
        Number of canonical bars loaded.
    n_input_rows
        Number of CSV data rows read before canonicalization.
    earliest_utc, latest_utc
        First and last loaded timestamps in UTC.
    n_missing_minutes
        Count of missing 1-minute timestamps between earliest_utc and latest_utc.
    missing_minutes
        Tuple of the exact missing UTC minute timestamps. This is reported but
        not automatically fatal because XAUUSD may have normal daily trading
        breaks that still need multi-day confirmation.
    """

    bars: pd.DataFrame
    n_bars: int
    n_input_rows: int
    earliest_utc: pd.Timestamp
    latest_utc: pd.Timestamp
    n_missing_minutes: int
    missing_minutes: tuple[pd.Timestamp, ...]


def _numeric_column(raw: pd.DataFrame, column: str, *, path: Path) -> pd.Series:
    """Parse one numeric CSV column and raise a clear vendor-format error."""

    try:
        return pd.to_numeric(raw[column], errors="raise")
    except Exception as exc:
        raise ValueError(
            f"Dukascopy CSV at {path} has non-numeric values in column {column!r}."
        ) from exc


def _missing_minutes(index: pd.DatetimeIndex) -> tuple[pd.Timestamp, ...]:
    """Return missing UTC 1-minute timestamps between the first and last bar."""

    if len(index) <= 1:
        return ()

    expected = pd.date_range(index[0], index[-1], freq="1min", tz="UTC")
    missing = expected.difference(index)
    return tuple(pd.Timestamp(ts) for ts in missing)


def load_dukascopy_csv(path: str | Path) -> DukascopyLoadResult:
    """Load an observed Dukascopy CSV export into canonical OHLCV form.

    Parameters
    ----------
    path
        Filesystem path to a Dukascopy CSV file with columns:
        UTC,Open,High,Low,Close,Volume.

    Returns
    -------
    DukascopyLoadResult
        Structured result containing canonical bars and missing-minute metadata.

    Raises
    ------
    ValueError
        If required columns are missing, timestamps cannot be parsed, timestamps
        are duplicated or non-monotonic, OHLC values are invalid, prices are
        non-positive, or volume is negative.
    """

    path = Path(path)
    raw = pd.read_csv(path)

    missing_columns = [
        column for column in _DUKASCOPY_REQUIRED_COLUMNS if column not in raw.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Dukascopy CSV at {path} is missing required columns: {missing_columns}. "
            f"Got columns: {list(raw.columns)}"
        )

    if raw.empty:
        raise ValueError(f"Dukascopy CSV at {path} contains no data rows.")

    try:
        dt = pd.to_datetime(
            raw["UTC"].astype(str),
            format=_DUKASCOPY_TIMESTAMP_FORMAT,
            utc=True,
        )
    except Exception as exc:
        raise ValueError(
            f"Dukascopy CSV at {path} has timestamps that do not match "
            f"format {_DUKASCOPY_TIMESTAMP_FORMAT!r}."
        ) from exc

    index = pd.DatetimeIndex(dt, name="dt")

    if index.has_duplicates:
        raise ValueError(f"Dukascopy CSV at {path} has duplicate timestamps.")

    if not index.is_monotonic_increasing:
        raise ValueError(f"Dukascopy CSV at {path} has non-monotonic timestamps.")

    open_ = _numeric_column(raw, "Open", path=path)
    high = _numeric_column(raw, "High", path=path)
    low = _numeric_column(raw, "Low", path=path)
    close = _numeric_column(raw, "Close", path=path)
    volume = _numeric_column(raw, "Volume", path=path)

    ohlc = pd.DataFrame(
        {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
        }
    )

    if (ohlc <= 0).any().any():
        raise ValueError(f"Dukascopy CSV at {path} has non-positive OHLC prices.")

    bad_ohlc = (
        (ohlc["high"] < ohlc["open"])
        | (ohlc["high"] < ohlc["low"])
        | (ohlc["high"] < ohlc["close"])
        | (ohlc["low"] > ohlc["open"])
        | (ohlc["low"] > ohlc["high"])
        | (ohlc["low"] > ohlc["close"])
    )
    if bad_ohlc.any():
        raise ValueError(f"Dukascopy CSV at {path} has bad OHLC rows.")

    if (volume < 0).any():
        raise ValueError(f"Dukascopy CSV at {path} has negative volume rows.")

    canonical = pd.DataFrame(
        {
            "open": open_.to_numpy(dtype=float),
            "high": high.to_numpy(dtype=float),
            "low": low.to_numpy(dtype=float),
            "close": close.to_numpy(dtype=float),
            "volume": volume.to_numpy(dtype=float),
        },
        index=index,
    )

    n_input_rows = len(canonical)
    missing_minutes = _missing_minutes(index)

    canonical = ensure_canonical(canonical)

    return DukascopyLoadResult(
        bars=canonical,
        n_bars=len(canonical),
        n_input_rows=n_input_rows,
        earliest_utc=canonical.index[0],
        latest_utc=canonical.index[-1],
        n_missing_minutes=len(missing_minutes),
        missing_minutes=missing_minutes,
    )
