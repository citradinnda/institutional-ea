"""H024 timestamp-shuffle negative-control diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

Purpose:
- test whether frozen H024 hold=3 depends on its actual timestamps,
- preserve the observed H024 non-zero intent rows as much as possible,
- randomly reassign those intents to valid decision timestamps,
- preserve raw stop distance at the reassigned entry timestamp,
- avoid parameter optimization.

If shuffled controls routinely match or beat frozen H024, curve-fit risk rises.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd

from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h024_runner import H024BridgeConfig, run_h024_bridge_shim
from scripts.diagnose_h021_fixed_lifecycle_variants_real import (
    H021FixedLifecycleBacktestResult,
    H021FixedLifecycleSummary,
    backtest_fixed_lifecycle_from_result,
    format_lifecycle_summary_table,
    summarize_lifecycle_backtest,
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

DEFAULT_H024_TIMESTAMP_SHUFFLE_HOLD_H4_BARS = 3
DEFAULT_H024_TIMESTAMP_SHUFFLE_RUNS = 100
DEFAULT_H024_TIMESTAMP_SHUFFLE_SEED = 24024
_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class H024TimestampShuffleSummary:
    seed: int
    fill_count: int
    stop_count: int
    stop_rate: float
    total_pnl_usd: float
    total_return: float
    max_drawdown: float
    win_rate: float
    profit_factor: float


@dataclass(frozen=True)
class H024TimestampShuffleDiagnosticResult:
    baseline: H021FixedLifecycleBacktestResult
    baseline_summary: H021FixedLifecycleSummary
    shuffle_summaries: tuple[H024TimestampShuffleSummary, ...]


def build_timestamp_shuffled_h017_result(
    *,
    h024_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    seed: int,
    hold_h4_bars: int = DEFAULT_H024_TIMESTAMP_SHUFFLE_HOLD_H4_BARS,
) -> H017Result:
    """Randomly reassign H024 non-zero intents to valid decision timestamps.

    Each original non-zero symbol intent contributes:
    - symbol,
    - side/risk fraction magnitude,
    - original raw stop distance.

    The reassigned intent is placed at a random valid decision timestamp for
    that symbol. The stop is rebuilt around the new raw H4 entry open using the
    preserved raw stop distance. This prevents invalid stop geometry from
    dominating the control while still breaking the original timestamp link.
    """

    if hold_h4_bars <= 0:
        raise ValueError("hold_h4_bars must be positive")

    rng = random.Random(seed)
    decision_index = _require_utc_index(h024_result.positions.index, name="positions.index")
    h4_by_symbol = {
        "USDJPY": _with_utc_index(usdjpy_h4),
        "XAUUSD": _with_utc_index(xauusd_h4),
    }

    valid_decision_times = _valid_decision_times(
        decision_index=decision_index,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars=hold_h4_bars,
    )
    if not valid_decision_times:
        raise ValueError("no valid decision times for timestamp shuffle")

    shuffled_positions = pd.DataFrame(0.0, index=decision_index, columns=_SYMBOLS)
    shuffled_signals = pd.DataFrame(0.0, index=decision_index, columns=_SYMBOLS)
    shuffled_stops_long = pd.DataFrame(float("nan"), index=decision_index, columns=_SYMBOLS)
    shuffled_stops_short = pd.DataFrame(float("nan"), index=decision_index, columns=_SYMBOLS)

    tickets = _extract_h024_intent_tickets(
        h024_result=h024_result,
        h4_by_symbol=h4_by_symbol,
        decision_index=decision_index,
        hold_h4_bars=hold_h4_bars,
    )

    for ticket in tickets:
        symbol = str(ticket["symbol"])
        side = str(ticket["side"])
        signed_risk = float(ticket["signed_risk"])
        raw_stop_distance = float(ticket["raw_stop_distance"])

        candidates = [
            decision_time for decision_time in valid_decision_times
            if shuffled_positions.at[decision_time, symbol] == 0.0
        ]
        if not candidates:
            continue

        decision_time = rng.choice(candidates)
        entry_time = _entry_time_for_decision(decision_index, decision_time)
        entry_raw_price = float(h4_by_symbol[symbol].at[entry_time, "open"])

        shuffled_positions.at[decision_time, symbol] = signed_risk
        shuffled_signals.at[decision_time, symbol] = 1.0 if signed_risk > 0.0 else -1.0

        if side == "buy":
            shuffled_stops_long.at[decision_time, symbol] = entry_raw_price - raw_stop_distance
        elif side == "sell":
            shuffled_stops_short.at[decision_time, symbol] = entry_raw_price + raw_stop_distance
        else:
            raise ValueError(f"unsupported side: {side!r}")

    multipliers = pd.DataFrame(1.0, index=decision_index, columns=_SYMBOLS)
    heat = pd.Series(0.0, index=decision_index)

    return H017Result(
        positions=shuffled_positions,
        signals=shuffled_signals,
        stops_long=shuffled_stops_long,
        stops_short=shuffled_stops_short,
        vol_multipliers=multipliers,
        heat_multipliers=multipliers,
        heat_pre=heat,
        heat_post=heat,
        heat_binding=pd.Series(False, index=decision_index),
    )


def run_h024_timestamp_shuffle_diagnostic(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    hold_h4_bars: int = DEFAULT_H024_TIMESTAMP_SHUFFLE_HOLD_H4_BARS,
    shuffle_runs: int = DEFAULT_H024_TIMESTAMP_SHUFFLE_RUNS,
    seed: int = DEFAULT_H024_TIMESTAMP_SHUFFLE_SEED,
    bridge_config: H024BridgeConfig | None = None,
    starting_equity_usd: float = 10_000.0,
) -> H024TimestampShuffleDiagnosticResult:
    """Run frozen H024 and timestamp-shuffled negative controls."""

    if shuffle_runs <= 0:
        raise ValueError("shuffle_runs must be positive")

    h024_result = run_h024_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=bridge_config,
    )

    baseline = backtest_fixed_lifecycle_from_result(
        h017_result=h024_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        hold_h4_bars=hold_h4_bars,
        starting_equity_usd=starting_equity_usd,
    )
    baseline_summary = summarize_lifecycle_backtest(baseline)

    summaries: list[H024TimestampShuffleSummary] = []
    for offset in range(shuffle_runs):
        run_seed = seed + offset
        shuffled_result = build_timestamp_shuffled_h017_result(
            h024_result=h024_result,
            usdjpy_h4=usdjpy_h4,
            xauusd_h4=xauusd_h4,
            accepted_entry_times=accepted_entry_times,
            seed=run_seed,
            hold_h4_bars=hold_h4_bars,
        )
        shuffle_backtest = backtest_fixed_lifecycle_from_result(
            h017_result=shuffled_result,
            usdjpy_h4=usdjpy_h4,
            xauusd_h4=xauusd_h4,
            usdjpy_m1=usdjpy_m1,
            xauusd_m1=xauusd_m1,
            accepted_entry_times=accepted_entry_times,
            hold_h4_bars=hold_h4_bars,
            starting_equity_usd=starting_equity_usd,
        )
        summary = summarize_lifecycle_backtest(shuffle_backtest)
        summaries.append(
            H024TimestampShuffleSummary(
                seed=run_seed,
                fill_count=summary.fill_count,
                stop_count=summary.stop_count,
                stop_rate=summary.stop_rate,
                total_pnl_usd=summary.total_pnl_usd,
                total_return=summary.total_return,
                max_drawdown=summary.max_drawdown,
                win_rate=summary.win_rate,
                profit_factor=summary.profit_factor,
            )
        )

    return H024TimestampShuffleDiagnosticResult(
        baseline=baseline,
        baseline_summary=baseline_summary,
        shuffle_summaries=tuple(summaries),
    )


def format_h024_timestamp_shuffle_report(
    diagnostic: H024TimestampShuffleDiagnosticResult,
) -> str:
    shuffles = pd.DataFrame([summary.__dict__ for summary in diagnostic.shuffle_summaries])
    baseline = diagnostic.baseline_summary

    baseline_row = format_lifecycle_summary_table(
        [baseline],
        title="Frozen H024 baseline",
    )

    if shuffles.empty:
        shuffle_report = "(no shuffles)"
        exceed_count = 0
        exceed_rate = float("nan")
    else:
        exceed_count = int((shuffles["total_pnl_usd"] >= baseline.total_pnl_usd).sum())
        exceed_rate = exceed_count / len(shuffles)
        shuffle_report = _format_shuffle_distribution(shuffles)

    sections = [
        "H024 timestamp-shuffle negative-control diagnostic",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        baseline_row,
        "",
        "Timestamp-shuffle distribution:",
        shuffle_report,
        "",
        f"Shuffle runs: {len(diagnostic.shuffle_summaries)}",
        f"Shuffles >= frozen H024 PnL: {exceed_count}",
        f"Empirical exceedance rate: {exceed_rate:.4%}",
        "",
        "Interpretation rule:",
        "- Frozen H024 should outperform most timestamp-shuffled controls.",
        "- If many shuffles match or beat frozen H024, curve-fit risk increases.",
        "- This diagnostic cannot approve demo/live/Phase 4.",
    ]
    return "\n".join(sections)


def main() -> None:
    print("H024 timestamp-shuffle negative-control diagnostic")
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
    print(f"Running baseline and {DEFAULT_H024_TIMESTAMP_SHUFFLE_RUNS} timestamp shuffles...")
    print()

    diagnostic = run_h024_timestamp_shuffle_diagnostic(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
    )
    print(format_h024_timestamp_shuffle_report(diagnostic))


def _extract_h024_intent_tickets(
    *,
    h024_result: H017Result,
    h4_by_symbol: dict[str, pd.DataFrame],
    decision_index: pd.DatetimeIndex,
    hold_h4_bars: int,
) -> tuple[dict[str, object], ...]:
    tickets: list[dict[str, object]] = []
    for entry_location in range(1, len(decision_index) - hold_h4_bars):
        decision_time = pd.Timestamp(decision_index[entry_location - 1]).tz_convert("UTC")
        entry_time = pd.Timestamp(decision_index[entry_location]).tz_convert("UTC")

        for symbol in _SYMBOLS:
            signed_risk = float(h024_result.positions.at[decision_time, symbol])
            if pd.isna(signed_risk) or signed_risk == 0.0:
                continue

            side = "buy" if signed_risk > 0.0 else "sell"
            stop_panel = h024_result.stops_long if side == "buy" else h024_result.stops_short
            stop_price = float(stop_panel.at[decision_time, symbol])
            if pd.isna(stop_price):
                continue

            entry_raw_price = float(h4_by_symbol[symbol].at[entry_time, "open"])
            raw_stop_distance = abs(entry_raw_price - stop_price)
            if raw_stop_distance <= 0.0:
                continue

            tickets.append(
                {
                    "symbol": symbol,
                    "side": side,
                    "signed_risk": signed_risk,
                    "raw_stop_distance": raw_stop_distance,
                }
            )

    return tuple(tickets)


def _valid_decision_times(
    *,
    decision_index: pd.DatetimeIndex,
    accepted_entry_times: Sequence[pd.Timestamp],
    hold_h4_bars: int,
) -> tuple[pd.Timestamp, ...]:
    accepted = {pd.Timestamp(ts).tz_convert("UTC") for ts in accepted_entry_times}
    result = []
    for entry_location in range(1, len(decision_index) - hold_h4_bars):
        decision_time = pd.Timestamp(decision_index[entry_location - 1]).tz_convert("UTC")
        horizon_times = tuple(
            pd.Timestamp(decision_index[entry_location + offset]).tz_convert("UTC")
            for offset in range(hold_h4_bars)
        )
        if all(timestamp in accepted for timestamp in horizon_times):
            result.append(decision_time)
    return tuple(result)


def _entry_time_for_decision(
    decision_index: pd.DatetimeIndex,
    decision_time: pd.Timestamp,
) -> pd.Timestamp:
    location = decision_index.get_loc(pd.Timestamp(decision_time).tz_convert("UTC"))
    if not isinstance(location, int):
        raise ValueError(f"non-unique decision_time in index: {decision_time}")
    return pd.Timestamp(decision_index[location + 1]).tz_convert("UTC")


def _format_shuffle_distribution(shuffles: pd.DataFrame) -> str:
    rows = []
    for metric in ("total_pnl_usd", "total_return", "max_drawdown", "profit_factor", "stop_rate"):
        series = shuffles[metric]
        rows.append(
            {
                "metric": metric,
                "min": series.min(),
                "p10": series.quantile(0.10),
                "median": series.median(),
                "mean": series.mean(),
                "p90": series.quantile(0.90),
                "max": series.max(),
            }
        )
    return pd.DataFrame(rows).to_string(index=False, float_format=lambda value: f"{value:.6f}")


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
