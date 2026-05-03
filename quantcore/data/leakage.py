from __future__ import annotations

"""quantcore/data/leakage.py

D1-disguised-as-H4 leakage detection for broker MT5 exports.

Why this module exists
----------------------
Phase 2.6b first contact with real Exness exports revealed that the broker
delivered DAILY bars labelled as H4 from 2018-07 through 2021-07-01, then
switched to genuine H4 on 2021-07-02. Symmetric across USDJPY and XAUUSD,
which is consistent with a broker-side export-format change rather than a
per-symbol artifact.

The leakage detector finds the first calendar date from which H4 bar
density is reliable, so callers can trim contaminated early bars before
any indicator / signal / backtest runs against the data.

Why broker-local grouping
-------------------------
Athens midnight is the natural broker-day boundary. Grouping by UTC date
would slice a single broker trading day across two UTC dates in summer
(UTC+3) and inflate the leaked-date count.

Why this heuristic and not "last suspect date"
----------------------------------------------
Naive "walk backward to the last suspect date" is wrong: forex weekends
and holidays produce sporadic low-bar-count dates throughout the entire
history (Saturdays usually have 0-1 H4 bars because the market is
closed). About half of all calendar dates are weekends/holidays, so
"last suspect date" effectively skips to the end of the data.

The correct shape of D1-disguised-as-H4 leakage is a CONTIGUOUS run of
low-count dates at the START of the series. Once real H4 data begins,
weekday counts jump to 5-6 bars/day. So: find the first date whose count
meets the threshold; everything before is presumed leaked, everything
after that fails the threshold is a normal FX weekend or holiday and is
left in place for the strategy to handle.
"""

from dataclasses import dataclass

import pandas as pd

# H4 = 6 bars per UTC day in 24/5 FX, but real weekend gaps and Athens
# DST mean a "fully populated" forex weekday typically yields 5-6 H4
# bars from a broker. We flag any broker-local date where bar count
# drops below this threshold as suspect.
MIN_H4_BARS_PER_ACTIVE_DAY: int = 4


@dataclass(frozen=True)
class LeakageScan:
    """Result of the D1-disguised-as-H4 leakage detector.

    Why frozen: structured returns must be self-describing per project
    conventions; mutability would invite callers to "fix up" the scan
    after the fact, defeating its evidentiary purpose.

    Fields
    ------
    first_reliable_date:
        First broker-local date with >= min_bars_per_day H4 bars.
        Earlier dates with fewer bars are presumed to be
        D1-disguised-as-H4 leakage.
    leaked_dates:
        Number of dates BEFORE first_reliable_date that fell below the
        threshold. This is the actual leaky region trimmed away.
    weekend_dates:
        Number of dates AT-OR-AFTER first_reliable_date that are still
        below threshold. These are normal FX weekends / holidays and are
        NOT a problem; reported only for transparency. About half of all
        calendar dates land here in 24/5 FX, which is why a "last
        suspect date" heuristic is wrong.
    total_dates:
        Total distinct broker-local dates in the series.
    broker_tz:
        IANA timezone used for date grouping.
    """

    first_reliable_date: pd.Timestamp
    leaked_dates: int
    weekend_dates: int
    total_dates: int
    broker_tz: str


def detect_d1_leakage(
    bars: pd.DataFrame,
    broker_tz: str,
    min_bars_per_day: int = MIN_H4_BARS_PER_ACTIVE_DAY,
) -> LeakageScan:
    """Find the first calendar date from which H4 bar density is reliable.

    Parameters
    ----------
    bars:
        Canonical OHLCV frame with a UTC tz-aware DatetimeIndex (Phase 1
        convention; produced by `quantcore.data.mt5_loader.load_mt5_csv`).
    broker_tz:
        IANA timezone string (e.g. "Europe/Athens"). Used to group bars
        by broker-local date so weekend boundaries align naturally.
    min_bars_per_day:
        Threshold for a date to be considered "reliable" H4 density.

    Returns
    -------
    LeakageScan with first_reliable_date and counts.

    Raises
    ------
    ValueError
        If `bars` is empty or no date in the series meets the threshold
        (signals a fully D1-disguised export).
    """
    if bars.empty:
        raise ValueError("Cannot scan leakage on empty bars frame.")

    local_index = bars.index.tz_convert(broker_tz)
    local_dates = pd.Series(local_index.date, index=bars.index)
    counts = local_dates.value_counts().sort_index()

    reliable_mask = counts >= min_bars_per_day
    if not reliable_mask.any():
        raise ValueError(
            f"No date in the series has >= {min_bars_per_day} H4 bars; "
            "the entire dataset may be D1-disguised-as-H4."
        )

    # First True in reliable_mask = first reliable date. argmax on a
    # boolean array returns the index of the first True (NumPy
    # guarantees this when at least one True exists, which we just
    # asserted).
    first_reliable_idx = int(reliable_mask.to_numpy().argmax())
    first_reliable = counts.index[first_reliable_idx]

    leaked = int((~reliable_mask.iloc[:first_reliable_idx]).sum())
    weekend = int((~reliable_mask.iloc[first_reliable_idx:]).sum())

    return LeakageScan(
        first_reliable_date=pd.Timestamp(first_reliable),
        leaked_dates=leaked,
        weekend_dates=weekend,
        total_dates=int(len(counts)),
        broker_tz=broker_tz,
    )


def trim_to_common_start(
    usdjpy: pd.DataFrame,
    xauusd: pd.DataFrame,
    start_date_utc: pd.Timestamp,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Trim both frames to start at-or-after `start_date_utc`.

    Why this is its own function: H017 inner-joins on timestamps inside
    backtest_h017, but a naive inner-join over the full history would
    still let early D1-leaked bars on EITHER symbol contaminate
    indicator warm-up on the OTHER. Trimming both frames symmetrically
    before the join is the cleanest fix.

    Parameters
    ----------
    usdjpy, xauusd:
        Canonical OHLCV frames with UTC tz-aware DatetimeIndex.
    start_date_utc:
        Tz-aware UTC timestamp; bars with index < this are dropped.

    Returns
    -------
    Tuple of (trimmed_usdjpy, trimmed_xauusd).

    Raises
    ------
    ValueError
        If `start_date_utc` is tz-naive (would silently misalign bars).
    """
    if start_date_utc.tz is None:
        raise ValueError(
            "start_date_utc must be tz-aware (UTC). "
            "A naive timestamp would silently misalign bars."
        )

    u = usdjpy.loc[usdjpy.index >= start_date_utc]
    x = xauusd.loc[xauusd.index >= start_date_utc]
    return u, x