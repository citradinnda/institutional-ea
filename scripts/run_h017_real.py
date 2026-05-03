from __future__ import annotations

"""scripts/run_h017_real.py

Phase 2.6b first-contact smoke test: run H017 against real Exness MT5 H4
exports for USDJPY + XAUUSD. This is the first time the strategy sees real
market microstructure.

Why this exists
---------------
Phase 2.5 validated H017 against synthetic random data and correctly returned
PROMOTABLE=False because random data has no edge. Phase 2.6b is first contact
with real data. We expect this to be informative, not necessarily promotable:
spread / slippage / commission are not modelled until Phase 3, and zero-cost
H017 may or may not pass the PSR + MinTRL gates. Either outcome is useful.

Pipeline
--------
1. Load USDJPY + XAUUSD H4 CSVs via the Phase 2.6a MT5 loader.
2. Detect "D1-disguised-as-H4" leakage in the early portion by counting bars
   per BROKER-LOCAL date (grouping by UTC date would split legitimate Athens
   trading days at midnight and produce false flags).
3. Trim both frames to the LATEST first-reliable date between the two symbols
   so they align on a common reliable region.
4. Run backtest_h017 (t+1 lag, zero-cost portfolio returns).
5. Run build_h017_claim (PSR + MinTRL mandatory; DSR skipped at first contact
   via sr_estimates=None per design brief Q3).
6. Print a structured summary to stdout. No DB or file writes (Q3 lean).

Design-brief lock-ins (Phase 2.6b §11)
--------------------------------------
- Q1 lean: lives in scripts/ (top-level), not quantcore/.
- Q2 lean: hermetic fixture parquet deferred to Phase 2.6c.
- Q3 lean: stdout only, no persistence.
- Q4 lean: --start-date optional override; default None = auto-detect cutoff.

This is an operational script, NOT a library module. Tests live in
quantcore-side modules; this script is excluded from the test anchor (413).
"""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.strategy.h017_claim import (
    H017BacktestResult,
    H017Claim,
    backtest_h017,
    build_h017_claim,
)


# Repository root resolved from this script's location, so the script works
# regardless of the user's current working directory.
REPO_ROOT: Path = Path(__file__).resolve().parent.parent
DEFAULT_USDJPY_CSV: Path = REPO_ROOT / "data" / "raw" / "USDJPY" / "H4.csv"
DEFAULT_XAUUSD_CSV: Path = REPO_ROOT / "data" / "raw" / "XAUUSD" / "H4.csv"

# H4 = 6 bars per UTC day in 24/5 FX, but real weekend gaps and Athens DST
# mean a "fully populated" forex weekday typically yields 5-6 H4 bars from a
# broker. We flag any broker-local date where bar count drops below this
# threshold as suspect (likely D1-disguised-as-H4 leakage in the early
# 2018 portion of the export).
MIN_H4_BARS_PER_ACTIVE_DAY: int = 4


@dataclass(frozen=True)
class LeakageScan:
    """Result of the D1-disguised-as-H4 leakage detector.

    Why frozen: structured returns must be self-describing per §6 conventions.

    Fields
    ------
    first_reliable_date:
        First broker-local date with >= min_bars_per_day H4 bars. Earlier
        dates with fewer bars are presumed to be D1-disguised-as-H4 leakage.
    leaked_dates:
        Number of dates BEFORE first_reliable_date that fell below the
        threshold. This is the actual leaky region we trim away.
    weekend_dates:
        Number of dates AT-OR-AFTER first_reliable_date that are still below
        threshold. These are normal FX weekends / holidays and are NOT a
        problem; reported only for transparency. About half of all calendar
        dates land here in 24/5 FX, which is why a "last suspect date"
        heuristic is wrong.
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

    Why this algorithm
    ------------------
    Naive "walk backward to the last suspect date" is WRONG: forex weekends
    and holidays produce sporadic low-bar-count dates throughout the entire
    history (Saturdays usually have 0-1 H4 bars because the market is
    closed). About half of all calendar dates are weekends/holidays, so the
    "last suspect date" heuristic effectively skips to the end of the data.

    The correct shape of D1-disguised-as-H4 leakage is a CONTIGUOUS run of
    low-count dates at the START of the series (the early Exness export
    delivered daily bars labelled as H4). Once real H4 data begins, weekday
    counts jump to 5-6 bars/day. So: find the first date whose count meets
    the threshold; everything before is presumed leaked, everything after
    that fails the threshold is a normal FX weekend or holiday and is left
    in place for the strategy to handle (signals naturally produce no edge
    on missing bars; H017 inner-joins on timestamps anyway).

    Why broker-local grouping
    -------------------------
    Athens midnight is the natural broker-day boundary. Grouping by UTC
    date would slice a single broker trading day across two UTC dates in
    summer (UTC+3) and inflate the leaked-date count.
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

    # First True in reliable_mask = first reliable date. argmax on a boolean
    # array returns the index of the first True (NumPy guarantees this when
    # at least one True exists, which we just asserted).
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
    backtest_h017, but a naive inner-join over the full history would still
    let early D1-leaked bars on EITHER symbol contaminate indicator warm-up
    on the OTHER. Trimming both frames symmetrically before the join is the
    cleanest fix.
    """
    u = usdjpy.loc[usdjpy.index >= start_date_utc]
    x = xauusd.loc[xauusd.index >= start_date_utc]
    return u, x


def _print_load_summary(symbol: str, result: MT5LoadResult) -> None:
    print(f"  {symbol}:")
    print(f"    n_input_rows : {result.n_input_rows}")
    print(f"    n_bars       : {result.n_bars}")
    print(f"    earliest_utc : {result.earliest_utc}")
    print(f"    latest_utc   : {result.latest_utc}")
    print(f"    broker_tz    : {result.broker_tz}")


def _print_leakage_summary(symbol: str, scan: LeakageScan) -> None:
    print(f"  {symbol}:")
    print(f"    leaked_dates        : {scan.leaked_dates} (early D1-disguised region, trimmed)")
    print(f"    weekend_dates       : {scan.weekend_dates} (normal FX off-days, kept)")
    print(f"    total_dates         : {scan.total_dates}")
    print(f"    first_reliable_date : {scan.first_reliable_date.date()} ({scan.broker_tz})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Phase 2.6b: H017 first-contact smoke test against real Exness "
            "MT5 H4 CSV exports. Prints a structured stdout summary; no "
            "files or DB rows are written."
        ),
    )
    parser.add_argument(
        "--usdjpy-csv",
        type=Path,
        default=DEFAULT_USDJPY_CSV,
        help=f"Path to USDJPY H4 CSV. Default: {DEFAULT_USDJPY_CSV}",
    )
    parser.add_argument(
        "--xauusd-csv",
        type=Path,
        default=DEFAULT_XAUUSD_CSV,
        help=f"Path to XAUUSD H4 CSV. Default: {DEFAULT_XAUUSD_CSV}",
    )
    parser.add_argument(
        "--broker-tz",
        type=str,
        default=DEFAULT_BROKER_TZ,
        help=f"IANA broker timezone. Default: {DEFAULT_BROKER_TZ}",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help=(
            "Optional manual override (YYYY-MM-DD, interpreted as UTC) for "
            "the post-trim start date. Default: auto-detect via D1-leakage "
            "scanner."
        ),
    )
    parser.add_argument(
        "--min-bars-per-day",
        type=int,
        default=MIN_H4_BARS_PER_ACTIVE_DAY,
        help=(
            f"Minimum H4 bars per broker-local date to be considered "
            f"reliable. Default: {MIN_H4_BARS_PER_ACTIVE_DAY}."
        ),
    )
    args = parser.parse_args(argv)

    print("=" * 72)
    print("Phase 2.6b - H017 first-contact smoke test (real Exness MT5 data)")
    print("=" * 72)

    # --- Step 1: Load both CSVs -----------------------------------------
    print("\n[1/5] Loading MT5 CSVs...")
    usdjpy_load = load_mt5_csv(args.usdjpy_csv, broker_tz=args.broker_tz)
    xauusd_load = load_mt5_csv(args.xauusd_csv, broker_tz=args.broker_tz)
    _print_load_summary("USDJPY", usdjpy_load)
    _print_load_summary("XAUUSD", xauusd_load)

    # --- Step 2: D1-leakage scan ----------------------------------------
    print("\n[2/5] Scanning for D1-disguised-as-H4 leakage...")
    usdjpy_scan = detect_d1_leakage(
        usdjpy_load.bars, args.broker_tz, args.min_bars_per_day
    )
    xauusd_scan = detect_d1_leakage(
        xauusd_load.bars, args.broker_tz, args.min_bars_per_day
    )
    _print_leakage_summary("USDJPY", usdjpy_scan)
    _print_leakage_summary("XAUUSD", xauusd_scan)

    # --- Step 3: Determine common start ---------------------------------
    print("\n[3/5] Determining common start date...")
    if args.start_date is not None:
        start_utc = pd.Timestamp(args.start_date, tz="UTC")
        print(f"  Manual override     : {start_utc.date()} (UTC)")
    else:
        # The leakage scanner returned broker-local dates. Convert each to a
        # tz-aware UTC midnight on that date. We take MAX so both symbols are
        # in their respective reliable regions.
        u_start_utc = pd.Timestamp(usdjpy_scan.first_reliable_date.date(), tz="UTC")
        x_start_utc = pd.Timestamp(xauusd_scan.first_reliable_date.date(), tz="UTC")
        start_utc = max(u_start_utc, x_start_utc)
        print(f"  USDJPY first-reliable : {u_start_utc.date()}")
        print(f"  XAUUSD first-reliable : {x_start_utc.date()}")
        print(f"  Common start (UTC)    : {start_utc.date()} (max of both)")

    usdjpy_bars, xauusd_bars = trim_to_common_start(
        usdjpy_load.bars, xauusd_load.bars, start_utc
    )
    print(f"  USDJPY post-trim bars : {len(usdjpy_bars)}")
    print(f"  XAUUSD post-trim bars : {len(xauusd_bars)}")

    if usdjpy_bars.empty or xauusd_bars.empty:
        print("\nERROR: post-trim frame is empty. Aborting.", file=sys.stderr)
        return 2

    # --- Step 4: Run H017 backtest --------------------------------------
    print("\n[4/5] Running H017 backtest (zero-cost, t+1 lag)...")
    bt: H017BacktestResult = backtest_h017(usdjpy_bars, xauusd_bars)
    print(f"  n_bars (joined)        : {bt.n_bars}")
    print(f"  portfolio_returns len  : {len(bt.portfolio_returns)}")
    nz = int((bt.portfolio_returns.fillna(0.0) != 0.0).sum())
    print(f"  non-zero return bars   : {nz}")

    # --- Step 5: Build claim --------------------------------------------
    print("\n[5/5] Building H017 claim (PSR + MinTRL mandatory; DSR skipped)...")
    claim: H017Claim = build_h017_claim(
        bt.portfolio_returns,
        periods_per_year=1512,  # H4 = 6 bars/day * 252 trading days
        sr_estimates=None,      # Q3 lean: skip DSR at first contact
    )

    print("\n" + "-" * 72)
    print("H017 CLAIM SUMMARY")
    print("-" * 72)
    print(claim.summary)
    print("-" * 72)
    verdict = "PROMOTABLE" if claim.promotable else "NOT PROMOTABLE"
    print(f"VERDICT: {verdict}")
    print("-" * 72)

    if not claim.promotable:
        print(
            "\nNote: zero-cost first contact. Phase 3 will add spread, "
            "slippage, and commission, which can only DECREASE Sharpe. "
            "A non-promotable result here does not necessarily kill H017; "
            "it just means we proceed to Phase 3 with eyes open."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())