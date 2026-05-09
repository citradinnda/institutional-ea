"""H024 hold=3 H4 trade ledger export diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

The ledger is intended for trade-level audit:
- individual fills,
- largest winners/losses,
- 2023 failure inspection,
- lot sizes,
- stop distances,
- execution prices,
- symbol/side/year concentration.

Do not run on real broker-native data without explicit user authorization.
"""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd

from quantcore.backtest.portfolio import (
    fill_pnl_usd,
    get_default_instrument_spec,
)
from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h024_runner import run_h024_bridge_shim
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    H021FixedLifecycleBacktestResult,
    backtest_fixed_lifecycle_from_result,
    format_group_summary_table,
    summarize_fills_by_field,
    summarize_fills_by_year,
)
from scripts.diagnose_h024_fixed_lifecycle_real import BRIDGE_WINDOW_CACHE_PATH
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)

DEFAULT_H024_LEDGER_HOLD_H4_BARS = 3
DEFAULT_H024_LEDGER_OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "reports"
    / "h024_hold3_trade_ledger.csv"
)

_LEDGER_COLUMNS: tuple[str, ...] = (
    "decision_time_utc",
    "entry_time_utc",
    "forced_exit_time_utc",
    "exit_time_utc",
    "exit_year",
    "symbol",
    "side",
    "exit_reason",
    "entry_raw_price",
    "entry_fill_price",
    "stop_price",
    "raw_stop_distance",
    "raw_stop_distance_pct",
    "forced_exit_raw_price",
    "exit_fill_price",
    "lots",
    "contract_size",
    "quote_currency",
    "notional_quote",
    "notional_usd",
    "gross_leverage_vs_10000_usd",
    "pnl_quote",
    "commission_usd",
    "slippage_price",
    "pnl_usd",
)


def build_h024_trade_ledger(
    *,
    h017_result: H017Result,
    fixed_lifecycle_result: H021FixedLifecycleBacktestResult,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    hold_h4_bars: int = DEFAULT_H024_LEDGER_HOLD_H4_BARS,
    reference_equity_usd: float = 10_000.0,
) -> pd.DataFrame:
    """Build a fill-level H024 audit ledger from an existing lifecycle result."""

    if hold_h4_bars <= 0:
        raise ValueError("hold_h4_bars must be positive")
    if reference_equity_usd <= 0.0:
        raise ValueError("reference_equity_usd must be positive")

    decision_index = _require_utc_index(h017_result.positions.index, name="positions.index")
    h4_by_symbol = {
        "USDJPY": _with_utc_index(usdjpy_h4),
        "XAUUSD": _with_utc_index(xauusd_h4),
    }

    rows: list[dict[str, object]] = []
    for fill in sorted(
        fixed_lifecycle_result.fills,
        key=lambda item: (item.entry_time_utc, item.symbol, item.exit_time_utc),
    ):
        symbol = fill.symbol.upper()
        if symbol not in h4_by_symbol:
            raise ValueError(f"unsupported fill symbol: {fill.symbol!r}")

        entry_time = pd.Timestamp(fill.entry_time_utc).tz_convert("UTC")
        entry_location = decision_index.get_loc(entry_time)
        if not isinstance(entry_location, int):
            raise ValueError(f"non-unique entry_time in decision index: {entry_time}")

        decision_location = entry_location - 1
        forced_exit_location = entry_location + hold_h4_bars
        if decision_location < 0 or forced_exit_location >= len(decision_index):
            raise ValueError(
                "fill cannot be reconciled to requested lifecycle horizon: "
                f"entry_time={entry_time}, hold_h4_bars={hold_h4_bars}"
            )

        decision_time = pd.Timestamp(decision_index[decision_location]).tz_convert("UTC")
        forced_exit_time = pd.Timestamp(decision_index[forced_exit_location]).tz_convert("UTC")

        stop_panel = h017_result.stops_long if fill.side == "buy" else h017_result.stops_short
        stop_price = float(stop_panel.at[decision_time, symbol])
        signed_risk_fraction = float(h017_result.positions.at[decision_time, symbol])

        if fill.side == "buy" and signed_risk_fraction <= 0.0:
            raise ValueError(f"buy fill does not match positive signal: {entry_time} {symbol}")
        if fill.side == "sell" and signed_risk_fraction >= 0.0:
            raise ValueError(f"sell fill does not match negative signal: {entry_time} {symbol}")

        h4 = h4_by_symbol[symbol]
        entry_raw_price = float(h4.at[entry_time, "open"])
        forced_exit_raw_price = float(h4.at[forced_exit_time, "open"])
        raw_stop_distance = abs(entry_raw_price - stop_price)

        spec = get_default_instrument_spec(symbol)
        notional_quote = float(fill.lots) * spec.contract_size * entry_raw_price
        notional_usd = (
            notional_quote / entry_raw_price
            if spec.quote_currency.upper() == "JPY"
            else notional_quote
        )

        rows.append(
            {
                "decision_time_utc": decision_time.isoformat(),
                "entry_time_utc": entry_time.isoformat(),
                "forced_exit_time_utc": forced_exit_time.isoformat(),
                "exit_time_utc": pd.Timestamp(fill.exit_time_utc).tz_convert("UTC").isoformat(),
                "exit_year": pd.Timestamp(fill.exit_time_utc).tz_convert("UTC").year,
                "symbol": symbol,
                "side": fill.side,
                "exit_reason": fill.exit_reason,
                "entry_raw_price": entry_raw_price,
                "entry_fill_price": float(fill.entry_price),
                "stop_price": stop_price,
                "raw_stop_distance": raw_stop_distance,
                "raw_stop_distance_pct": raw_stop_distance / entry_raw_price,
                "forced_exit_raw_price": forced_exit_raw_price,
                "exit_fill_price": float(fill.exit_price),
                "lots": float(fill.lots),
                "contract_size": float(spec.contract_size),
                "quote_currency": spec.quote_currency,
                "notional_quote": notional_quote,
                "notional_usd": notional_usd,
                "gross_leverage_vs_10000_usd": notional_usd / reference_equity_usd,
                "pnl_quote": float(fill.pnl_quote),
                "commission_usd": float(fill.commission),
                "slippage_price": float(fill.slippage),
                "pnl_usd": fill_pnl_usd(fill=fill),
            }
        )

    return pd.DataFrame(rows, columns=_LEDGER_COLUMNS)


def format_h024_trade_ledger_audit_report(
    *,
    ledger: pd.DataFrame,
    result: H021FixedLifecycleBacktestResult,
    output_path: Path,
    top_n: int = 10,
) -> str:
    """Format compact ledger audit output for console review."""

    lines = [
        "H024 hold=3 H4 trade ledger export/audit diagnostic",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        f"Output CSV: {output_path}",
        f"Ledger rows: {len(ledger)}",
        f"Lifecycle fills: {len(result.fills)}",
        f"Net PnL USD: {ledger['pnl_usd'].sum():.2f}" if not ledger.empty else "Net PnL USD: 0.00",
        "",
        "By symbol:",
        format_group_summary_table(
            summarize_fills_by_field(result.fills, field="symbol"),
            title="By symbol",
        ),
        "",
        "By side:",
        format_group_summary_table(
            summarize_fills_by_field(result.fills, field="side"),
            title="By side",
        ),
        "",
        "By exit year:",
        format_group_summary_table(
            summarize_fills_by_year(result.fills),
            title="By exit year",
        ),
    ]

    if ledger.empty:
        lines.extend(["", "No fills to rank."])
        return "\n".join(lines)

    lines.extend(
        [
            "",
            f"Top {top_n} losses:",
            _format_ranked_trades(ledger.nsmallest(top_n, "pnl_usd")),
            "",
            f"Top {top_n} winners:",
            _format_ranked_trades(ledger.nlargest(top_n, "pnl_usd")),
            "",
            "2023 audit slice:",
            _format_2023_slice(ledger),
        ]
    )
    return "\n".join(lines)


def run_h024_trade_ledger_export(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    output_path: Path = DEFAULT_H024_LEDGER_OUTPUT_PATH,
    hold_h4_bars: int = DEFAULT_H024_LEDGER_HOLD_H4_BARS,
    starting_equity_usd: float = 10_000.0,
) -> tuple[pd.DataFrame, H021FixedLifecycleBacktestResult]:
    """Run H024 hold=3 and write a fill-level ledger CSV."""

    h024_result = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
    )
    fixed_lifecycle_result = backtest_fixed_lifecycle_from_result(
        h017_result=h024_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars=hold_h4_bars,
        starting_equity_usd=starting_equity_usd,
    )
    ledger = build_h024_trade_ledger(
        h017_result=h024_result,
        fixed_lifecycle_result=fixed_lifecycle_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        hold_h4_bars=hold_h4_bars,
        reference_equity_usd=starting_equity_usd,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    ledger.to_csv(output_path, index=False)
    return ledger, fixed_lifecycle_result


def main() -> None:
    print("H024 hold=3 H4 trade ledger export/audit diagnostic")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print()

    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="broker-native MT5 exports",
    )

    print("Loading exports...")
    usdjpy_h4 = load_mt5_csv(USDJPY_H4_PATH)
    xauusd_h4 = load_mt5_csv(XAUUSD_H4_PATH)
    usdjpy_m1 = load_mt5_csv(USDJPY_M1_PATH)
    xauusd_m1 = load_mt5_csv(XAUUSD_M1_PATH)

    cache_key = build_common_complete_bridge_window_cache_key(
        source_paths={
            "usdjpy_h4": USDJPY_H4_PATH,
            "xauusd_h4": XAUUSD_H4_PATH,
            "usdjpy_m1": USDJPY_M1_PATH,
            "xauusd_m1": XAUUSD_M1_PATH,
        },
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )
    assessment = assess_common_complete_h4_m1_windows_cached(
        cache_path=BRIDGE_WINDOW_CACHE_PATH,
        cache_key=cache_key,
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(
            "accepted_count mismatch: "
            f"expected={EXPECTED_ACCEPTED_COUNT}, observed={assessment.accepted_count}"
        )

    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print("Running H024 hold=3 ledger export...")
    print()

    ledger, result = run_h024_trade_ledger_export(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
    )

    print(
        format_h024_trade_ledger_audit_report(
            ledger=ledger,
            result=result,
            output_path=DEFAULT_H024_LEDGER_OUTPUT_PATH,
        )
    )


def _format_ranked_trades(rows: pd.DataFrame) -> str:
    if rows.empty:
        return "(no rows)"

    fields = [
        "exit_time_utc",
        "symbol",
        "side",
        "exit_reason",
        "lots",
        "raw_stop_distance",
        "entry_fill_price",
        "exit_fill_price",
        "pnl_usd",
    ]
    return rows.loc[:, fields].to_string(index=False)


def _format_2023_slice(ledger: pd.DataFrame) -> str:
    rows = ledger.loc[ledger["exit_year"] == 2023]
    if rows.empty:
        return "(no 2023 rows)"

    summary = rows.groupby(["symbol", "side", "exit_reason"], dropna=False).agg(
        fills=("pnl_usd", "size"),
        pnl_usd=("pnl_usd", "sum"),
        avg_lots=("lots", "mean"),
        avg_raw_stop_distance=("raw_stop_distance", "mean"),
    )
    return summary.reset_index().to_string(index=False)


def _with_utc_index(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result.index = _require_utc_index(result.index, name="frame.index")
    return result


def _require_utc_index(index: pd.Index, *, name: str) -> pd.DatetimeIndex:
    if not isinstance(index, pd.DatetimeIndex):
        raise ValueError(f"{name} must be a DatetimeIndex")
    if index.tz is None:
        raise ValueError(f"{name} must be timezone-aware")
    return index.tz_convert("UTC")


if __name__ == "__main__":
    main()
