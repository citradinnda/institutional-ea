"""HistData M1 CSV loader.

The newly inventoried HistData M1 files use a no-header comma-separated format:

    YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

Observed example:

    2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0

WHY this is separate from dukascopy_loader.py:
    The observed Dukascopy sample format has an explicit UTC column and header:

        UTC,Open,High,Low,Close,Volume

    The observed HistData files have no header and separate date/time columns.
    Treating HistData as Dukascopy would erase source identity and hide schema
    differences that matter for provenance.

WHY this is separate from load_histdata_csv in loaders.py:
    loaders.load_histdata_csv handles an older semicolon-separated HistData-style
    format:

        YYYYMMDD HHMMSS;open;high;low;close;volume

    The newly inventoried raw files are comma-separated and use:

        YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume

This loader is infrastructure only. Its existence does not mean HistData is an
accepted research source for H017.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import pandas as pd

from quantcore.data.loaders import ensure_canonical


_HISTDATA_M1_COLUMN_NAMES: tuple[str, ...] = (
    "date",
    "time",
    "open",
    "high",
    "low",
    "close",
    "volume",
)

_HISTDATA_M1_EXPECTED_N_COLUMNS: int = len(_HISTDATA_M1_COLUMN_NAMES)
_HISTDATA_M1_TIMESTAMP_FORMAT: str = "%Y.%m.%d %H:%M"

DuplicatePolicy = Literal["reject", "drop_exact"]
DuplicateTimestampRange = tuple[pd.Timestamp, pd.Timestamp, int]


@dataclass(frozen=True)
class HistDataM1LoadResult:
    """Structured result of loading an observed HistData M1 CSV file.

    Attributes
    ----------
    bars
        Canonical OHLCV DataFrame with lowercase open/high/low/close/volume
        columns and a UTC DatetimeIndex.
    n_bars
        Number of canonical bars loaded.
    n_input_rows
        Number of CSV data rows read before canonicalization and before any
        explicit exact-duplicate removal.
    earliest_utc, latest_utc
        First and last loaded timestamps in UTC.
    source_tz
        Timezone used to interpret the raw no-timezone HistData timestamps.
        This is surfaced because the raw file does not label timestamps with a
        timezone. The default is UTC, but that is still an explicit loader
        assumption, not a source-acceptance decision.
    duplicate_policy
        Duplicate timestamp policy used by the loader. The default is "reject".
        "drop_exact" is an explicit opt-in policy that removes only exact
        duplicate OHLCV rows and rejects conflicting duplicate timestamp groups.
    n_duplicate_rows_removed
        Number of rows removed by the explicit duplicate policy.
    n_duplicate_timestamp_values
        Number of distinct duplicated timestamp values observed before any
        explicit duplicate removal.
    duplicate_timestamp_ranges
        Tuple of contiguous duplicate timestamp ranges. Each item is:
        (start_utc, end_utc, n_duplicate_timestamp_values_in_range).
    n_missing_minutes
        Count of missing 1-minute timestamps between earliest_utc and latest_utc.
    missing_minutes
        Tuple of the exact missing UTC minute timestamps. This is reported but
        not automatically fatal because normal weekend closures and metals
        breaks still need source-specific coverage analysis.
    """

    bars: pd.DataFrame
    n_bars: int
    n_input_rows: int
    earliest_utc: pd.Timestamp
    latest_utc: pd.Timestamp
    source_tz: str
    duplicate_policy: str
    n_duplicate_rows_removed: int
    n_duplicate_timestamp_values: int
    duplicate_timestamp_ranges: tuple[DuplicateTimestampRange, ...]
    n_missing_minutes: int
    missing_minutes: tuple[pd.Timestamp, ...]


def _numeric_column(raw: pd.DataFrame, column: str, *, path: Path) -> pd.Series:
    """Parse one numeric CSV column and raise a clear vendor-format error."""

    try:
        return pd.to_numeric(raw[column], errors="raise")
    except Exception as exc:
        raise ValueError(
            f"HistData M1 CSV at {path} has non-numeric values in column {column!r}."
        ) from exc


def _missing_minutes(index: pd.DatetimeIndex) -> tuple[pd.Timestamp, ...]:
    """Return missing UTC 1-minute timestamps between the first and last bar."""

    if len(index) <= 1:
        return ()

    expected = pd.date_range(index[0], index[-1], freq="1min", tz="UTC")
    missing = expected.difference(index)
    return tuple(pd.Timestamp(ts) for ts in missing)


def _histdata_timestamp_index(
    raw: pd.DataFrame,
    *,
    path: Path,
    source_tz: str,
) -> pd.DatetimeIndex:
    """Parse raw HistData date/time columns into a UTC DatetimeIndex."""

    dt_text = raw["date"].astype(str) + " " + raw["time"].astype(str)

    try:
        naive = pd.to_datetime(dt_text, format=_HISTDATA_M1_TIMESTAMP_FORMAT)
    except Exception as exc:
        raise ValueError(
            f"HistData M1 CSV at {path} has timestamps that do not match "
            f"format {_HISTDATA_M1_TIMESTAMP_FORMAT!r}."
        ) from exc

    if source_tz == "UTC":
        index = pd.DatetimeIndex(naive).tz_localize("UTC")
    else:
        try:
            aware = naive.dt.tz_localize(
                source_tz,
                ambiguous="infer",
                nonexistent="shift_forward",
            )
        except Exception as exc:
            raise ValueError(
                f"HistData M1 CSV at {path} could not localize timestamps "
                f"using source_tz={source_tz!r}."
            ) from exc

        index = pd.DatetimeIndex(aware.dt.tz_convert("UTC"))

    index.name = "dt"
    return index


def _duplicate_timestamp_ranges(
    index: pd.DatetimeIndex,
) -> tuple[DuplicateTimestampRange, ...]:
    """Summarize duplicated timestamps as contiguous UTC minute ranges."""

    duplicate_values = pd.DatetimeIndex(index[index.duplicated(keep=False)].unique())
    if len(duplicate_values) == 0:
        return ()

    duplicate_values = duplicate_values.sort_values()
    ranges: list[DuplicateTimestampRange] = []

    start = pd.Timestamp(duplicate_values[0])
    previous = pd.Timestamp(duplicate_values[0])
    count = 1

    for value in duplicate_values[1:]:
        current = pd.Timestamp(value)
        if current == previous + pd.Timedelta(minutes=1):
            previous = current
            count += 1
            continue

        ranges.append((start, previous, count))
        start = current
        previous = current
        count = 1

    ranges.append((start, previous, count))
    return tuple(ranges)


def _validate_duplicate_policy(duplicate_policy: str) -> DuplicatePolicy:
    """Validate and narrow the duplicate policy string."""

    if duplicate_policy not in {"reject", "drop_exact"}:
        raise ValueError(
            "duplicate_policy must be one of {'reject', 'drop_exact'}; "
            f"got {duplicate_policy!r}."
        )

    return duplicate_policy  # type: ignore[return-value]


def _drop_exact_duplicate_timestamps(
    canonical: pd.DataFrame,
    *,
    path: Path,
) -> tuple[pd.DataFrame, int]:
    """Drop exact duplicate OHLCV timestamp rows and reject conflicts."""

    duplicate_mask = canonical.index.duplicated(keep=False)
    if not duplicate_mask.any():
        return canonical, 0

    duplicate_rows = canonical.loc[duplicate_mask]

    conflicting_timestamps: list[pd.Timestamp] = []
    for timestamp, group in duplicate_rows.groupby(level=0, sort=True):
        if len(group.drop_duplicates()) != 1:
            conflicting_timestamps.append(pd.Timestamp(timestamp))

    if conflicting_timestamps:
        first_conflicts = tuple(conflicting_timestamps[:10])
        raise ValueError(
            f"HistData M1 CSV at {path} has conflicting duplicate timestamps. "
            f"First conflicts: {first_conflicts}"
        )

    before = len(canonical)
    canonical = canonical.loc[~canonical.index.duplicated(keep="first")]
    removed = before - len(canonical)

    return canonical, removed


def _apply_duplicate_policy(
    canonical: pd.DataFrame,
    *,
    path: Path,
    duplicate_policy: DuplicatePolicy,
) -> tuple[pd.DataFrame, int]:
    """Apply the explicit duplicate timestamp policy."""

    if not canonical.index.has_duplicates:
        return canonical, 0

    if duplicate_policy == "reject":
        raise ValueError(f"HistData M1 CSV at {path} has duplicate timestamps.")

    return _drop_exact_duplicate_timestamps(canonical, path=path)


def load_histdata_m1_csv(
    path: str | Path,
    *,
    source_tz: str = "UTC",
    duplicate_policy: DuplicatePolicy = "reject",
) -> HistDataM1LoadResult:
    """Load an observed HistData M1 CSV export into canonical OHLCV form.

    Parameters
    ----------
    path
        Filesystem path to a HistData M1 CSV file using the observed no-header
        comma-separated schema:
        YYYY.MM.DD,HH:MM,Open,High,Low,Close,Volume.
    source_tz
        Timezone used to interpret raw timestamps before conversion to UTC.
        The raw files do not label their timezone, so this parameter makes the
        assumption explicit. The default is "UTC".
    duplicate_policy
        Duplicate timestamp policy. The default "reject" keeps strict vendor
        validation. The opt-in "drop_exact" removes only exact duplicate OHLCV
        rows and rejects conflicting duplicate timestamp groups.

    Returns
    -------
    HistDataM1LoadResult
        Structured result containing canonical bars, duplicate audit metadata,
        and missing-minute metadata.

    Raises
    ------
    ValueError
        If the CSV shape is wrong, timestamps cannot be parsed, duplicate
        policy is invalid, timestamps are duplicated under the strict policy,
        duplicate timestamps conflict under the exact-drop policy, timestamps
        remain non-monotonic after duplicate handling, OHLC values are invalid,
        prices are non-positive, or volume is negative.
    """

    path = Path(path)
    duplicate_policy = _validate_duplicate_policy(duplicate_policy)

    try:
        raw = pd.read_csv(path, header=None)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"HistData M1 CSV at {path} contains no data rows.") from exc

    if raw.empty:
        raise ValueError(f"HistData M1 CSV at {path} contains no data rows.")

    if raw.shape[1] != _HISTDATA_M1_EXPECTED_N_COLUMNS:
        raise ValueError(
            f"HistData M1 CSV at {path} expected "
            f"{_HISTDATA_M1_EXPECTED_N_COLUMNS} columns but got {raw.shape[1]}."
        )

    raw.columns = list(_HISTDATA_M1_COLUMN_NAMES)

    index = _histdata_timestamp_index(raw, path=path, source_tz=source_tz)

    open_ = _numeric_column(raw, "open", path=path)
    high = _numeric_column(raw, "high", path=path)
    low = _numeric_column(raw, "low", path=path)
    close = _numeric_column(raw, "close", path=path)
    volume = _numeric_column(raw, "volume", path=path)

    ohlc = pd.DataFrame(
        {
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
        }
    )

    if (ohlc <= 0).any().any():
        raise ValueError(f"HistData M1 CSV at {path} has non-positive OHLC prices.")

    bad_ohlc = (
        (ohlc["high"] < ohlc["open"])
        | (ohlc["high"] < ohlc["low"])
        | (ohlc["high"] < ohlc["close"])
        | (ohlc["low"] > ohlc["open"])
        | (ohlc["low"] > ohlc["high"])
        | (ohlc["low"] > ohlc["close"])
    )
    if bad_ohlc.any():
        raise ValueError(f"HistData M1 CSV at {path} has bad OHLC rows.")

    if (volume < 0).any():
        raise ValueError(f"HistData M1 CSV at {path} has negative volume rows.")

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
    duplicate_timestamp_ranges = _duplicate_timestamp_ranges(canonical.index)
    n_duplicate_timestamp_values = sum(
        n_values for _, _, n_values in duplicate_timestamp_ranges
    )

    canonical, n_duplicate_rows_removed = _apply_duplicate_policy(
        canonical,
        path=path,
        duplicate_policy=duplicate_policy,
    )

    if not canonical.index.is_monotonic_increasing:
        raise ValueError(f"HistData M1 CSV at {path} has non-monotonic timestamps.")

    missing_minutes = _missing_minutes(canonical.index)

    canonical = ensure_canonical(canonical)

    return HistDataM1LoadResult(
        bars=canonical,
        n_bars=len(canonical),
        n_input_rows=n_input_rows,
        earliest_utc=canonical.index[0],
        latest_utc=canonical.index[-1],
        source_tz=source_tz,
        duplicate_policy=duplicate_policy,
        n_duplicate_rows_removed=n_duplicate_rows_removed,
        n_duplicate_timestamp_values=n_duplicate_timestamp_values,
        duplicate_timestamp_ranges=duplicate_timestamp_ranges,
        n_missing_minutes=len(missing_minutes),
        missing_minutes=missing_minutes,
    )
