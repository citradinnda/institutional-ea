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
from pathlib import Path

import pandas as pd

from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.strategy.h017_claim import (
    H017BacktestResult,
    H017Claim,
    backtest_h017,
    build_h017_claim,
)
from quantcore.data.leakage import (
    MIN_H4_BARS_PER_ACTIVE_DAY,
    LeakageScan,
    detect_d1_leakage,
    trim_to_common_start,
)


# Repository root resolved from this script's location, so the script works
# regardless of the user's current working directory.
REPO_ROOT: Path = Path(__file__).resolve().parent.parent
DEFAULT_USDJPY_CSV: Path = REPO_ROOT / "data" / "raw" / "USDJPY" / "H4.csv"
DEFAULT_XAUUSD_CSV: Path = REPO_ROOT / "data" / "raw" / "XAUUSD" / "H4.csv"


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