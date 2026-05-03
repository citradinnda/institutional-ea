"""MT5 History Center CSV loader.

WHY this is a separate module from loaders.py:
    The existing load_histdata_csv handles HistData.com's ASCII format
    (semicolon-separated, single combined datetime, naive UTC).
    MT5's History Center exports a structurally different format:
        - tab-separated
        - <DATE> + <TIME> in two columns (YYYY.MM.DD and HH:MM:SS)
        - timestamps in BROKER WALL-CLOCK TIME, not UTC
        - extra <TICKVOL> / <VOL> / <SPREAD> columns

WHY broker_tz matters:
    Exness's MT5 server runs on Europe/Athens (EET in winter / EEST in summer,
    with DST). A bar labeled "2024.06.03 04:00:00" in the CSV is actually
    01:00 UTC, not 04:00 UTC. §6 of the project conventions mandates a UTC
    DatetimeIndex on every canonical frame, so we localize-then-convert
    BEFORE handing the frame to ensure_canonical.

WHY <TICKVOL> -> volume:
    On OTC FX, real volume is unobservable, so <VOL> is always 0.
    MT5's tick volume (count of price updates within the bar) is the
    standard activity proxy; per §6 canonical OHLCV the column name is
    'volume'. <VOL> and <SPREAD> are dropped from the canonical frame.
    Spread may be re-introduced as a separate cost-model input in Phase 3.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.data.loaders import ensure_canonical

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Default broker timezone for Exness MT5 servers (and most EU brokers).
#: EET in winter (UTC+2), EEST in summer (UTC+3), DST-aware.
DEFAULT_BROKER_TZ: str = "Europe/Athens"

#: Required columns in an MT5-exported CSV. <VOL> and <SPREAD> are tolerated
#: but not required — older MT5 builds omitted them.
_MT5_REQUIRED_COLUMNS: tuple[str, ...] = (
    "<DATE>",
    "<TIME>",
    "<OPEN>",
    "<HIGH>",
    "<LOW>",
    "<CLOSE>",
    "<TICKVOL>",
)

#: MT5's date+time format string used by pd.to_datetime.
_MT5_DT_FORMAT: str = "%Y.%m.%d %H:%M:%S"


# ---------------------------------------------------------------------------
# Result dataclass (per §6: structured returns, frozen, self-describing fields)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class MT5LoadResult:
    """Structured result of loading an MT5-exported CSV.

    Attributes
    ----------
    bars
        Canonical OHLCV DataFrame (lowercase open/high/low/close/volume,
        UTC DatetimeIndex, deduplicated, sorted ascending).
    n_bars
        Number of bars in `bars` after canonicalization.
    n_input_rows
        Number of data rows read from the CSV before dedup. The difference
        n_input_rows - n_bars equals the number of rows dropped during
        canonicalization (typically duplicate timestamps from broker
        re-syncs across DST or maintenance windows).
    earliest_utc, latest_utc
        First and last bar timestamps in UTC.
    broker_tz
        The IANA timezone string the loader used to interpret the raw
        wall-clock timestamps. Surfaced for audit / reconciliation.
    """

    bars: pd.DataFrame
    n_bars: int
    n_input_rows: int
    earliest_utc: pd.Timestamp
    latest_utc: pd.Timestamp
    broker_tz: str


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_mt5_csv(
    path: str | Path,
    broker_tz: str = DEFAULT_BROKER_TZ,
) -> MT5LoadResult:
    """Load an MT5 History Center CSV export into a canonical OHLCV frame.

    Parameters
    ----------
    path
        Filesystem path to the CSV file produced by MT5's History Center
        Export button.
    broker_tz
        IANA timezone string for the broker's server clock. Defaults to
        Europe/Athens (Exness standard). Use "UTC" if your CSV is already
        in UTC (rare for MT5).

    Returns
    -------
    MT5LoadResult
        Structured result containing canonical bars + metadata.

    Raises
    ------
    ValueError
        If the CSV is missing any required column (<DATE>, <TIME>, <OPEN>,
        <HIGH>, <LOW>, <CLOSE>, <TICKVOL>) or if the canonicalization step
        rejects the frame.

    Notes
    -----
    DST handling: ambiguous timestamps (the fall-back hour, where the
    same wall-clock minute occurs twice) are resolved with
    ``ambiguous="infer"``, which uses the sort order of the data to pick
    summer-time first then winter-time. Nonexistent timestamps (the
    spring-forward gap) are shifted forward by one hour. For H4 bars at
    Exness, both edge cases are extremely rare in practice.
    """
    path = Path(path)

    # Step 1: parse raw CSV (tab-separated, MT5 standard).
    raw = pd.read_csv(path, sep="\t")

    # Step 2: validate columns. We check against the angle-bracketed names
    # MT5 actually emits — this surfaces format drift early instead of
    # silently producing a malformed frame downstream.
    missing = [c for c in _MT5_REQUIRED_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(
            f"MT5 CSV at {path} is missing required columns: {missing}. "
            f"Got columns: {list(raw.columns)}"
        )

    # Step 3: combine <DATE> + <TIME> into a single naive datetime.
    # We coerce to str defensively in case pd.read_csv inferred a non-string
    # dtype (e.g. for purely-numeric date strings on some locales).
    dt_str = raw["<DATE>"].astype(str) + " " + raw["<TIME>"].astype(str)
    naive = pd.to_datetime(dt_str, format=_MT5_DT_FORMAT)

    # Step 4: sort by naive timestamp BEFORE localizing. ambiguous="infer"
    # requires sorted input to disambiguate the DST fall-back hour.
    sort_idx = naive.argsort()
    naive_sorted = naive.iloc[sort_idx].reset_index(drop=True)
    raw_sorted = raw.iloc[sort_idx].reset_index(drop=True)

    # Step 5: localize broker wall-clock -> UTC.
    # WHY two branches: tz_localize("UTC") with ambiguous=/nonexistent= is
    # a no-op edge case in pandas; treat UTC explicitly for clarity.
    if broker_tz == "UTC":
        utc_idx = pd.DatetimeIndex(naive_sorted).tz_localize("UTC")
    else:
        aware = naive_sorted.dt.tz_localize(
            broker_tz,
            ambiguous="infer",
            nonexistent="shift_forward",
        )
        utc_idx = pd.DatetimeIndex(aware.dt.tz_convert("UTC"))

    # Step 6: build canonical frame. <TICKVOL> -> volume (see module docstring).
    canonical = pd.DataFrame(
        {
            "open": raw_sorted["<OPEN>"].astype(float).to_numpy(),
            "high": raw_sorted["<HIGH>"].astype(float).to_numpy(),
            "low": raw_sorted["<LOW>"].astype(float).to_numpy(),
            "close": raw_sorted["<CLOSE>"].astype(float).to_numpy(),
            "volume": raw_sorted["<TICKVOL>"].astype(float).to_numpy(),
        },
        index=utc_idx,
    )
    canonical.index.name = "dt"

    n_input = len(canonical)

    # Step 7: hand off to the canonical enforcer (lowercase cols already done,
    # but this also dedups, sorts, and re-validates UTC tz).
    canonical = ensure_canonical(canonical)

    return MT5LoadResult(
        bars=canonical,
        n_bars=len(canonical),
        n_input_rows=n_input,
        earliest_utc=canonical.index[0],
        latest_utc=canonical.index[-1],
        broker_tz=broker_tz,
    )