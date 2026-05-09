"""Build H024 dry-run action logs from strategy output.

This module connects frozen H024/H017-compatible strategy output to the
dry-run/log-only execution-preparation layer. It does not import MT5 and cannot
place orders.

Research/preparation only. No demo/live/Phase 4 approval.
"""
from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pandas as pd

from quantcore.backtest.portfolio import get_default_instrument_spec, size_position_from_risk
from quantcore.execution.h024_dry_run import (
    BrokerSymbolFacts,
    DryRunAction,
    DryRunConfig,
    TradeCandidate,
    build_dry_run_action,
)
from quantcore.strategy.h017 import H017Result

_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")

_ACTION_CSV_FIELDS: tuple[str, ...] = (
    "action",
    "model_symbol",
    "broker_symbol",
    "side",
    "timestamp_utc",
    "reason",
    "raw_lots",
    "normalized_lots",
    "raw_entry_price",
    "raw_stop_price",
    "raw_stop_distance",
    "notional_quote",
    "notional_usd",
    "per_trade_gross_leverage",
    "kill_switch_enabled",
    "mode",
)


def build_h024_dry_run_actions(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    accepted_entry_times: Iterable[pd.Timestamp],
    config: DryRunConfig,
    broker_facts_by_symbol: Mapping[str, BrokerSymbolFacts] | None = None,
    starting_equity_usd: float = 10_000.0,
    hold_h4_bars: int = 3,
) -> tuple[DryRunAction, ...]:
    """Build non-overlapping H024 dry-run action records.

    Timing follows the fixed-lifecycle diagnostic convention:

    - decision at H4 timestamp t
    - entry at next accepted H4 timestamp t+1
    - lifecycle horizon is ``hold_h4_bars``
    - after an executable lifecycle is inspected, later entries before the
      forced exit are skipped, matching non-overlap behavior

    This function emits intended dry-run actions only; it cannot place orders.
    """

    if starting_equity_usd <= 0.0:
        raise ValueError("starting_equity_usd must be positive")
    if hold_h4_bars <= 0:
        raise ValueError("hold_h4_bars must be positive")

    h4_by_symbol = {
        "USDJPY": _with_utc_index(usdjpy_h4),
        "XAUUSD": _with_utc_index(xauusd_h4),
    }
    decision_index = _require_utc_index(h017_result.positions.index, name="positions.index")
    accepted = tuple(sorted(pd.Timestamp(ts).tz_convert("UTC") for ts in accepted_entry_times))
    accepted_set = set(accepted)

    actions: list[DryRunAction] = []
    next_eligible_entry_time: pd.Timestamp | None = None

    for entry_time in accepted:
        if next_eligible_entry_time is not None and entry_time < next_eligible_entry_time:
            continue

        if entry_time not in decision_index:
            continue

        entry_location = decision_index.get_loc(entry_time)
        if not isinstance(entry_location, int):
            raise ValueError(f"non-unique entry_time in decision index: {entry_time}")

        decision_location = entry_location - 1
        forced_exit_location = entry_location + hold_h4_bars

        if decision_location < 0 or forced_exit_location >= len(decision_index):
            continue

        horizon_times = tuple(decision_index[entry_location + offset] for offset in range(hold_h4_bars))
        if any(pd.Timestamp(ts).tz_convert("UTC") not in accepted_set for ts in horizon_times):
            continue

        decision_time = pd.Timestamp(decision_index[decision_location]).tz_convert("UTC")
        forced_exit_time = pd.Timestamp(decision_index[forced_exit_location]).tz_convert("UTC")

        interval_actions = tuple(
            build_dry_run_action(
                config=config,
                candidate=_build_trade_candidate(
                    symbol=symbol,
                    h017_result=h017_result,
                    h4_bars=h4_by_symbol[symbol],
                    decision_time=decision_time,
                    entry_time=entry_time,
                    equity_usd=starting_equity_usd,
                ),
                broker_facts_by_symbol=broker_facts_by_symbol,
            )
            for symbol in _SYMBOLS
        )
        actions.extend(interval_actions)

        if any(action.action == "WOULD_OPEN" for action in interval_actions):
            next_eligible_entry_time = forced_exit_time

    return tuple(actions)


def write_dry_run_actions_csv(*, actions: Sequence[DryRunAction], output_path: Path) -> None:
    """Write dry-run action records to CSV."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=_ACTION_CSV_FIELDS)
        writer.writeheader()
        for action in actions:
            row = asdict(action)
            writer.writerow({field: row[field] for field in _ACTION_CSV_FIELDS})


def summarize_dry_run_actions(actions: Sequence[DryRunAction]) -> dict[str, int]:
    """Return action counts keyed by action kind."""

    summary = {"WOULD_OPEN": 0, "NO_ACTION": 0, "BLOCKED": 0}
    for action in actions:
        summary[action.action] += 1
    return summary


def _build_trade_candidate(
    *,
    symbol: str,
    h017_result: H017Result,
    h4_bars: pd.DataFrame,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    equity_usd: float,
) -> TradeCandidate:
    signed_risk_fraction = float(h017_result.positions.at[decision_time, symbol])
    entry_price = float(h4_bars.at[entry_time, "open"])

    if pd.isna(signed_risk_fraction) or signed_risk_fraction == 0.0:
        return TradeCandidate(
            model_symbol=symbol,
            side=None,
            timestamp_utc=entry_time.isoformat(),
            equity_usd=equity_usd,
            signed_risk_fraction=0.0,
            raw_entry_price=entry_price,
            raw_stop_price=entry_price,
            raw_lots=0.0,
        )

    side = "buy" if signed_risk_fraction > 0.0 else "sell"
    stop_panel = h017_result.stops_long if side == "buy" else h017_result.stops_short
    stop_price = float(stop_panel.at[decision_time, symbol])

    if pd.isna(stop_price):
        return TradeCandidate(
            model_symbol=symbol,
            side=None,
            timestamp_utc=entry_time.isoformat(),
            equity_usd=equity_usd,
            signed_risk_fraction=0.0,
            raw_entry_price=entry_price,
            raw_stop_price=entry_price,
            raw_lots=0.0,
        )

    stop_distance = abs(entry_price - stop_price)
    if stop_distance <= 0.0:
        raw_lots = 0.0
    else:
        position_size = size_position_from_risk(
            symbol=symbol,
            signed_risk_fraction=signed_risk_fraction,
            equity_usd=equity_usd,
            entry_price=entry_price,
            stop_distance_price=stop_distance,
            instrument_spec=get_default_instrument_spec(symbol),
        )
        raw_lots = position_size.lots

    return TradeCandidate(
        model_symbol=symbol,
        side=side,
        timestamp_utc=entry_time.isoformat(),
        equity_usd=equity_usd,
        signed_risk_fraction=signed_risk_fraction,
        raw_entry_price=entry_price,
        raw_stop_price=stop_price,
        raw_lots=raw_lots,
    )


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
