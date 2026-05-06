"""H021 bridge hold-horizon diagnostic.

Diagnostic-only check for whether H020/H021 outcomes are materially shaped by
the current bridge simplification:

- decide at H4 timestamp t,
- enter at next H4 open,
- close any non-stopped exposure at the following H4 open.

This script mechanically replays baseline signal_flip fills with longer fixed
H4 hold horizons while preserving the same entry, stop, lots, execution costs,
and M1 stop-first rule.

This is not:
- a strategy,
- a validation pass,
- live-trading approval,
- Phase 4 approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import inf, isnan
from statistics import median
from typing import Iterable, Mapping, Sequence

import pandas as pd

from quantcore.backtest.cost_model import price_with_execution_costs
from quantcore.backtest.fill_engine import Fill, simulate_bracket_trade
from quantcore.backtest.h020_strict_event import backtest_h020_strict_event
from quantcore.backtest.portfolio import fill_pnl_usd, get_default_instrument_spec
from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h020_runner import run_h020_bridge_shim
from scripts.diagnose_h021_stop_precursors_real import (
    H021StopPrecursorRecord,
    build_decision_contexts,
    enrich_fills_with_decision_context,
)
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)

DEFAULT_HOLD_H4_BARS: tuple[int, ...] = (2, 3, 4)


@dataclass(frozen=True)
class H021BridgeHorizonObservation:
    symbol: str
    side: str
    entry_time: pd.Timestamp
    baseline_exit_time: pd.Timestamp
    baseline_exit_reason: str
    baseline_pnl_usd: float
    hold_h4_bars: int
    alternate_exit_time: pd.Timestamp
    alternate_exit_reason: str
    alternate_pnl_usd: float
    pnl_delta_usd: float
    outcome_label: str


@dataclass(frozen=True)
class H021BridgeHorizonSummaryRow:
    hold_h4_bars: int
    observation_count: int
    alternate_stop_count: int
    alternate_stop_rate: float
    baseline_total_pnl_usd: float
    alternate_total_pnl_usd: float
    total_pnl_delta_usd: float
    median_pnl_delta_usd: float
    baseline_winner_count: int
    winner_retained_profit_count: int
    winner_to_loss_count: int
    winner_stopped_count: int
    winner_improved_count: int
    loser_to_profit_count: int
    alternate_profit_factor: float


def simulate_alternate_horizon_fill(
    *,
    baseline_fill: Fill,
    record: H021StopPrecursorRecord,
    h4_bars: pd.DataFrame,
    m1_bars: pd.DataFrame,
    hold_h4_bars: int,
) -> Fill:
    """Replay one fill with a longer fixed H4 forced-exit horizon."""
    if hold_h4_bars <= 0:
        raise ValueError("hold_h4_bars must be positive")

    h4 = _with_utc_index(h4_bars)
    entry_time = pd.Timestamp(baseline_fill.entry_time_utc).tz_convert("UTC")
    if entry_time not in h4.index:
        raise ValueError(f"entry_time missing from h4_bars: {entry_time}")

    entry_location = h4.index.get_loc(entry_time)
    if not isinstance(entry_location, int):
        raise ValueError(f"non-unique entry_time in h4_bars: {entry_time}")

    forced_exit_location = entry_location + hold_h4_bars
    if forced_exit_location >= len(h4.index):
        raise ValueError(
            "hold_h4_bars extends beyond available h4_bars: "
            f"entry_time={entry_time}, hold_h4_bars={hold_h4_bars}"
        )

    forced_exit_time = pd.Timestamp(h4.index[forced_exit_location]).tz_convert("UTC")
    forced_exit_raw_price = float(h4.iloc[forced_exit_location]["open"])

    instrument_spec = get_default_instrument_spec(baseline_fill.symbol)
    entry_cost = price_with_execution_costs(
        symbol=baseline_fill.symbol,
        side=baseline_fill.side,
        action="entry",
        raw_price=record.entry_raw_price,
        lots=baseline_fill.lots,
    )

    raw_fill = simulate_bracket_trade(
        symbol=baseline_fill.symbol,
        side=baseline_fill.side,
        entry_time_utc=entry_time,
        entry_price=entry_cost.fill_price,
        lots=baseline_fill.lots,
        m1_bars=_with_utc_index(m1_bars),
        stop_price=record.stop_price,
        take_profit_price=None,
        forced_exit_time_utc=forced_exit_time,
        forced_exit_price=forced_exit_raw_price,
        contract_size=instrument_spec.contract_size,
        commission=0.0,
        stop_slippage=0.0,
    )

    exit_cost = price_with_execution_costs(
        symbol=baseline_fill.symbol,
        side=baseline_fill.side,
        action="exit",
        raw_price=raw_fill.exit_price,
        lots=baseline_fill.lots,
        exit_reason=raw_fill.exit_reason,
        atr=record.raw_stop_distance,
    )

    commission = entry_cost.commission_usd + exit_cost.commission_usd
    pnl_quote = _pnl_quote(
        side=baseline_fill.side,
        entry_price=entry_cost.fill_price,
        exit_price=exit_cost.fill_price,
        lots=baseline_fill.lots,
        contract_size=instrument_spec.contract_size,
    )

    return Fill(
        symbol=baseline_fill.symbol,
        side=baseline_fill.side,
        entry_time_utc=entry_time,
        entry_price=entry_cost.fill_price,
        exit_time_utc=raw_fill.exit_time_utc,
        exit_price=exit_cost.fill_price,
        lots=baseline_fill.lots,
        pnl_quote=pnl_quote,
        commission=commission,
        slippage=exit_cost.slippage_price,
        exit_reason=raw_fill.exit_reason,
    )


def compare_signal_flip_horizons(
    *,
    records: Iterable[H021StopPrecursorRecord],
    fills: Iterable[Fill],
    h4_by_symbol: Mapping[str, pd.DataFrame],
    m1_by_symbol: Mapping[str, pd.DataFrame],
    hold_h4_bars_values: Sequence[int] = DEFAULT_HOLD_H4_BARS,
) -> tuple[H021BridgeHorizonObservation, ...]:
    """Compare baseline one-H4 signal_flip fills against alternate horizons."""
    if not hold_h4_bars_values:
        raise ValueError("hold_h4_bars_values must not be empty")
    if any(value <= 0 for value in hold_h4_bars_values):
        raise ValueError("hold_h4_bars_values must be positive")

    fill_by_key = {_fill_key(fill): fill for fill in fills}

    observations: list[H021BridgeHorizonObservation] = []
    for record in records:
        if record.exit_reason != "signal_flip":
            continue

        key = (record.symbol, record.side, pd.Timestamp(record.entry_time).tz_convert("UTC"))
        if key not in fill_by_key:
            raise ValueError(f"missing baseline fill for key={key}")

        baseline_fill = fill_by_key[key]
        baseline_pnl = fill_pnl_usd(fill=baseline_fill)

        for hold_h4_bars in hold_h4_bars_values:
            try:
                alternate_fill = simulate_alternate_horizon_fill(
                    baseline_fill=baseline_fill,
                    record=record,
                    h4_bars=h4_by_symbol[record.symbol],
                    m1_bars=m1_by_symbol[record.symbol],
                    hold_h4_bars=hold_h4_bars,
                )
            except ValueError as exc:
                if "extends beyond available h4_bars" in str(exc):
                    continue
                raise

            alternate_pnl = fill_pnl_usd(fill=alternate_fill)
            observations.append(
                H021BridgeHorizonObservation(
                    symbol=record.symbol,
                    side=record.side,
                    entry_time=pd.Timestamp(record.entry_time).tz_convert("UTC"),
                    baseline_exit_time=pd.Timestamp(baseline_fill.exit_time_utc).tz_convert("UTC"),
                    baseline_exit_reason=baseline_fill.exit_reason,
                    baseline_pnl_usd=baseline_pnl,
                    hold_h4_bars=hold_h4_bars,
                    alternate_exit_time=pd.Timestamp(alternate_fill.exit_time_utc).tz_convert("UTC"),
                    alternate_exit_reason=alternate_fill.exit_reason,
                    alternate_pnl_usd=alternate_pnl,
                    pnl_delta_usd=alternate_pnl - baseline_pnl,
                    outcome_label=_classify_outcome(
                        baseline_pnl_usd=baseline_pnl,
                        alternate_pnl_usd=alternate_pnl,
                    ),
                )
            )

    return tuple(observations)


def summarize_bridge_horizon_observations(
    observations: Iterable[H021BridgeHorizonObservation],
) -> tuple[H021BridgeHorizonSummaryRow, ...]:
    """Summarize alternate hold-horizon observations."""
    grouped: dict[int, list[H021BridgeHorizonObservation]] = {}
    for observation in observations:
        grouped.setdefault(observation.hold_h4_bars, []).append(observation)

    rows: list[H021BridgeHorizonSummaryRow] = []
    for hold_h4_bars in sorted(grouped):
        group = grouped[hold_h4_bars]
        baseline_values = [row.baseline_pnl_usd for row in group]
        alternate_values = [row.alternate_pnl_usd for row in group]
        delta_values = [row.pnl_delta_usd for row in group]
        alternate_winners = [value for value in alternate_values if value > 0.0]
        alternate_losers = [value for value in alternate_values if value < 0.0]
        baseline_winners = [row for row in group if row.baseline_pnl_usd > 0.0]
        alternate_stop_count = sum(1 for row in group if row.alternate_exit_reason == "stop")

        rows.append(
            H021BridgeHorizonSummaryRow(
                hold_h4_bars=hold_h4_bars,
                observation_count=len(group),
                alternate_stop_count=alternate_stop_count,
                alternate_stop_rate=alternate_stop_count / len(group),
                baseline_total_pnl_usd=sum(baseline_values),
                alternate_total_pnl_usd=sum(alternate_values),
                total_pnl_delta_usd=sum(delta_values),
                median_pnl_delta_usd=median(delta_values),
                baseline_winner_count=len(baseline_winners),
                winner_retained_profit_count=sum(
                    1 for row in baseline_winners if row.alternate_pnl_usd > 0.0
                ),
                winner_to_loss_count=sum(
                    1 for row in baseline_winners if row.alternate_pnl_usd <= 0.0
                ),
                winner_stopped_count=sum(
                    1 for row in baseline_winners if row.alternate_exit_reason == "stop"
                ),
                winner_improved_count=sum(
                    1
                    for row in baseline_winners
                    if row.alternate_pnl_usd > row.baseline_pnl_usd
                ),
                loser_to_profit_count=sum(
                    1
                    for row in group
                    if row.baseline_pnl_usd <= 0.0 and row.alternate_pnl_usd > 0.0
                ),
                alternate_profit_factor=_profit_factor(
                    gross_profit_usd=sum(alternate_winners),
                    gross_loss_usd=sum(alternate_losers),
                ),
            )
        )

    return tuple(rows)


def format_bridge_horizon_summary_table(
    rows: Sequence[H021BridgeHorizonSummaryRow],
    *,
    title: str = "H021 bridge hold-horizon summary",
) -> str:
    """Format bridge horizon summary rows as a compact console table."""
    lines = [title]
    if not rows:
        lines.append("(no observations)")
        return "\n".join(lines)

    header = (
        "hold_h4_bars | observations | alt_stops | alt_stop_rate | "
        "baseline_total_pnl_usd | alternate_total_pnl_usd | total_delta_usd | "
        "median_delta_usd | baseline_winners | winners_retained_profit | "
        "winners_to_loss | winners_stopped | winners_improved | loser_to_profit | "
        "alternate_profit_factor"
    )
    lines.append(header)

    for row in rows:
        lines.append(
            " | ".join(
                [
                    str(row.hold_h4_bars),
                    str(row.observation_count),
                    str(row.alternate_stop_count),
                    _format_percent(row.alternate_stop_rate),
                    _format_float(row.baseline_total_pnl_usd),
                    _format_float(row.alternate_total_pnl_usd),
                    _format_float(row.total_pnl_delta_usd),
                    _format_float(row.median_pnl_delta_usd),
                    str(row.baseline_winner_count),
                    str(row.winner_retained_profit_count),
                    str(row.winner_to_loss_count),
                    str(row.winner_stopped_count),
                    str(row.winner_improved_count),
                    str(row.loser_to_profit_count),
                    _format_float(row.alternate_profit_factor),
                ]
            )
        )

    return "\n".join(lines)


def main() -> None:
    print("H021 bridge hold-horizon diagnostic")
    print("=" * 38)
    print("Diagnostic only. No live trading. No Phase 4.")
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
        cache_path=USDJPY_H4_PATH.parents[2]
        / "cache"
        / "strict_usdjpy_xauusd_h4_m1_bridge_windows.json",
        cache_key=cache_key,
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(f"accepted_count mismatch: {assessment.accepted_count}")

    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print("Running strict H020 event backtest...")
    print()

    result = backtest_h020_strict_event(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
        starting_equity_usd=10000.0,
    )

    shim = run_h020_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4.bars,
        xauusd_ohlcv=xauusd_h4.bars,
    )
    contexts = build_decision_contexts(
        h017_result=shim,
        h4_by_symbol={"USDJPY": usdjpy_h4.bars, "XAUUSD": xauusd_h4.bars},
        accepted_entry_times=assessment.accepted_timestamps,
    )
    records = enrich_fills_with_decision_context(
        result.backtest.fills,
        contexts,
        starting_equity_usd=10000.0,
    )

    observations = compare_signal_flip_horizons(
        records=records,
        fills=result.backtest.fills,
        h4_by_symbol={"USDJPY": usdjpy_h4.bars, "XAUUSD": xauusd_h4.bars},
        m1_by_symbol={"USDJPY": usdjpy_m1.bars, "XAUUSD": xauusd_m1.bars},
        hold_h4_bars_values=DEFAULT_HOLD_H4_BARS,
    )
    rows = summarize_bridge_horizon_observations(observations)

    print(f"Context rows reconstructed: {len(contexts)}")
    print(f"Fill rows enriched: {len(records)}")
    print(f"Baseline signal_flip observations replayed: {len(observations)}")
    print()
    print(format_bridge_horizon_summary_table(rows))
    print()

    print("Interpretation reminder:")
    print("- This mechanically changes hold horizon; it is not a strategy.")
    print("- If longer horizons destroy winners, the one-bar bridge may be carrying edge.")
    print("- If longer horizons improve outcomes, lifecycle design needs new pre-registered tests.")
    print("- Do not deploy from this diagnostic alone.")
    print("No live trading is approved. Phase 4 is not approved.")


def _fill_key(fill: Fill) -> tuple[str, str, pd.Timestamp]:
    return (fill.symbol, fill.side, pd.Timestamp(fill.entry_time_utc).tz_convert("UTC"))


def _with_utc_index(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result.index = pd.DatetimeIndex(result.index).tz_convert("UTC")
    return result


def _pnl_quote(
    *,
    side: str,
    entry_price: float,
    exit_price: float,
    lots: float,
    contract_size: float,
) -> float:
    direction = 1.0 if side == "buy" else -1.0
    return direction * (exit_price - entry_price) * lots * contract_size


def _classify_outcome(
    *,
    baseline_pnl_usd: float,
    alternate_pnl_usd: float,
) -> str:
    if baseline_pnl_usd > 0.0:
        if alternate_pnl_usd > baseline_pnl_usd:
            return "winner_improved"
        if alternate_pnl_usd > 0.0:
            return "winner_retained_profit"
        return "winner_to_loss"

    if alternate_pnl_usd > 0.0:
        return "loser_to_profit"
    if alternate_pnl_usd > baseline_pnl_usd:
        return "loser_less_bad"
    return "loser_worse"


def _profit_factor(*, gross_profit_usd: float, gross_loss_usd: float) -> float:
    if gross_loss_usd < 0.0:
        return gross_profit_usd / abs(gross_loss_usd)
    if gross_profit_usd > 0.0:
        return inf
    return float("nan")


def _format_float(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.6f}"


def _format_percent(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{100.0 * value:.4f}%"


if __name__ == "__main__":
    main()
