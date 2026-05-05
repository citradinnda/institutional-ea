from __future__ import annotations

"""Diagnostic-only H018 stop-state checks.

This module measures whether H017 is holding a Donchian signal after the
same-side raw Chandelier stop has become non-protective at decision close.

It does not:
- validate H018,
- promote H017,
- change event execution,
- skip trades,
- clip trades,
- switch stop panels,
- tune parameters.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd


@dataclass(frozen=True)
class StopStateObservation:
    symbol: str
    side: str
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    signal_value: float
    previous_signal_value: float | None
    decision_close: float
    stop_price: float
    selected_stop_panel: str
    signal_state: str
    same_side_stop_valid_at_decision_close: bool


@dataclass(frozen=True)
class StopStateBucket:
    symbol: str
    side: str
    total_nonzero_signal_count: int
    same_side_stop_valid_at_decision_close_count: int
    same_side_stop_breached_at_decision_close_count: int
    fresh_signal_count: int
    held_continuation_count: int
    breached_fresh_signal_count: int
    breached_held_continuation_count: int


@dataclass(frozen=True)
class StopStateDiagnostic:
    event_interval_count: int
    accepted_entry_count: int | None
    skipped_entry_count: int | None
    total_nonzero_signal_count: int
    flat_signal_skipped_count: int
    nan_signal_skipped_count: int
    unavailable_price_or_stop_skipped_count: int
    same_side_stop_valid_at_decision_close_count: int
    same_side_stop_breached_at_decision_close_count: int
    fresh_signal_count: int
    held_continuation_count: int
    breached_fresh_signal_count: int
    breached_held_continuation_count: int
    buckets: tuple[StopStateBucket, ...]
    observations: tuple[StopStateObservation, ...]

    @property
    def bucket_counts_by_symbol_side(self) -> dict[str, dict[str, int]]:
        return {
            f"{bucket.symbol}:{bucket.side}": {
                "total_nonzero_signal_count": bucket.total_nonzero_signal_count,
                "same_side_stop_valid_at_decision_close_count": (
                    bucket.same_side_stop_valid_at_decision_close_count
                ),
                "same_side_stop_breached_at_decision_close_count": (
                    bucket.same_side_stop_breached_at_decision_close_count
                ),
                "fresh_signal_count": bucket.fresh_signal_count,
                "held_continuation_count": bucket.held_continuation_count,
                "breached_fresh_signal_count": bucket.breached_fresh_signal_count,
                "breached_held_continuation_count": (
                    bucket.breached_held_continuation_count
                ),
            }
            for bucket in self.buckets
        }


def diagnose_h018_stop_state(
    *,
    h017_result: Any,
    h4_by_symbol: Mapping[str, pd.DataFrame],
    accepted_entry_times: pd.DatetimeIndex | None = None,
    expected_h4_delta: pd.Timedelta | None = pd.Timedelta(hours=4),
) -> StopStateDiagnostic:
    """Count held-signal observations with non-protective same-side stops.

    The diagnostic evaluates the H017 signal at decision close. If the
    signal is long, the long Chandelier panel must be below decision close.
    If the signal is short, the short Chandelier panel must be above
    decision close.

    If accepted_entry_times is provided, only decision bars whose next H4
    timestamp is in that accepted entry set are counted.
    """
    signals = h017_result.signals
    stops_long = h017_result.stops_long
    stops_short = h017_result.stops_short

    index = signals.index
    accepted_set = (
        {pd.Timestamp(timestamp) for timestamp in accepted_entry_times}
        if accepted_entry_times is not None
        else None
    )

    event_interval_count = 0
    skipped_entry_count = 0

    total_nonzero_signal_count = 0
    flat_signal_skipped_count = 0
    nan_signal_skipped_count = 0
    unavailable_price_or_stop_skipped_count = 0
    same_side_valid_count = 0
    same_side_breached_count = 0
    fresh_signal_count = 0
    held_continuation_count = 0
    breached_fresh_signal_count = 0
    breached_held_continuation_count = 0

    bucket_counts: defaultdict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    observations: list[StopStateObservation] = []

    for i in range(len(index) - 1):
        decision_time = index[i]
        entry_time = index[i + 1]

        if expected_h4_delta is not None and entry_time - decision_time != expected_h4_delta:
            continue

        event_interval_count += 1

        if accepted_set is not None and entry_time not in accepted_set:
            skipped_entry_count += 1
            continue

        for symbol in signals.columns:
            signal_value = float(signals.at[decision_time, symbol])

            if pd.isna(signal_value):
                nan_signal_skipped_count += 1
                continue

            if signal_value == 0.0:
                flat_signal_skipped_count += 1
                continue

            side = _side_from_signal(signal_value)
            stop_panel_name = "stops_long" if side == "buy" else "stops_short"
            stop_panel = stops_long if side == "buy" else stops_short

            decision_close = _optional_decision_close(
                h4_by_symbol=h4_by_symbol,
                symbol=symbol,
                decision_time=decision_time,
            )
            stop_price = _optional_stop_price(
                panel=stop_panel,
                symbol=symbol,
                decision_time=decision_time,
            )

            if decision_close is None or stop_price is None:
                unavailable_price_or_stop_skipped_count += 1
                continue

            previous_signal_value = _previous_signal_value(
                signals=signals,
                symbol=symbol,
                i=i,
            )
            signal_state = _classify_signal_state(
                current_signal_value=signal_value,
                previous_signal_value=previous_signal_value,
            )

            same_side_valid = _is_directionally_valid(
                side=side,
                reference_price=decision_close,
                stop_price=stop_price,
            )

            total_nonzero_signal_count += 1
            bucket_key = (symbol, side)
            bucket_counts[bucket_key]["total"] += 1

            if same_side_valid:
                same_side_valid_count += 1
                bucket_counts[bucket_key]["valid"] += 1
            else:
                same_side_breached_count += 1
                bucket_counts[bucket_key]["breached"] += 1

            if signal_state == "fresh_signal":
                fresh_signal_count += 1
                bucket_counts[bucket_key]["fresh"] += 1
                if not same_side_valid:
                    breached_fresh_signal_count += 1
                    bucket_counts[bucket_key]["breached_fresh"] += 1
            elif signal_state == "held_continuation":
                held_continuation_count += 1
                bucket_counts[bucket_key]["held"] += 1
                if not same_side_valid:
                    breached_held_continuation_count += 1
                    bucket_counts[bucket_key]["breached_held"] += 1
            else:
                raise ValueError(f"unexpected signal_state: {signal_state}")

            observations.append(
                StopStateObservation(
                    symbol=symbol,
                    side=side,
                    decision_time=decision_time,
                    entry_time=entry_time,
                    signal_value=signal_value,
                    previous_signal_value=previous_signal_value,
                    decision_close=decision_close,
                    stop_price=stop_price,
                    selected_stop_panel=stop_panel_name,
                    signal_state=signal_state,
                    same_side_stop_valid_at_decision_close=same_side_valid,
                )
            )

    return StopStateDiagnostic(
        event_interval_count=event_interval_count,
        accepted_entry_count=len(accepted_set) if accepted_set is not None else None,
        skipped_entry_count=skipped_entry_count if accepted_set is not None else None,
        total_nonzero_signal_count=total_nonzero_signal_count,
        flat_signal_skipped_count=flat_signal_skipped_count,
        nan_signal_skipped_count=nan_signal_skipped_count,
        unavailable_price_or_stop_skipped_count=unavailable_price_or_stop_skipped_count,
        same_side_stop_valid_at_decision_close_count=same_side_valid_count,
        same_side_stop_breached_at_decision_close_count=same_side_breached_count,
        fresh_signal_count=fresh_signal_count,
        held_continuation_count=held_continuation_count,
        breached_fresh_signal_count=breached_fresh_signal_count,
        breached_held_continuation_count=breached_held_continuation_count,
        buckets=_build_buckets(bucket_counts),
        observations=tuple(observations),
    )


def _side_from_signal(signal_value: float) -> str:
    if signal_value > 0.0:
        return "buy"
    if signal_value < 0.0:
        return "sell"
    raise ValueError("signal_value must be nonzero")


def _optional_decision_close(
    *,
    h4_by_symbol: Mapping[str, pd.DataFrame],
    symbol: str,
    decision_time: pd.Timestamp,
) -> float | None:
    if symbol not in h4_by_symbol:
        return None
    frame = h4_by_symbol[symbol]
    if decision_time not in frame.index:
        return None

    value = float(frame.at[decision_time, "close"])
    if pd.isna(value):
        return None
    return value


def _optional_stop_price(
    *,
    panel: pd.DataFrame,
    symbol: str,
    decision_time: pd.Timestamp,
) -> float | None:
    if symbol not in panel.columns or decision_time not in panel.index:
        return None

    value = float(panel.at[decision_time, symbol])
    if pd.isna(value):
        return None
    return value


def _previous_signal_value(
    *,
    signals: pd.DataFrame,
    symbol: str,
    i: int,
) -> float | None:
    if i == 0:
        return None

    value = float(signals.iloc[i - 1][symbol])
    if pd.isna(value):
        return None
    return value


def _classify_signal_state(
    *,
    current_signal_value: float,
    previous_signal_value: float | None,
) -> str:
    if previous_signal_value is None:
        return "fresh_signal"
    if previous_signal_value == 0.0:
        return "fresh_signal"
    if current_signal_value > 0.0 and previous_signal_value > 0.0:
        return "held_continuation"
    if current_signal_value < 0.0 and previous_signal_value < 0.0:
        return "held_continuation"
    return "fresh_signal"


def _is_directionally_valid(
    *,
    side: str,
    reference_price: float,
    stop_price: float,
) -> bool:
    if side == "buy":
        return stop_price < reference_price
    if side == "sell":
        return stop_price > reference_price
    raise ValueError("side must be 'buy' or 'sell'")


def _build_buckets(
    bucket_counts: defaultdict[tuple[str, str], Counter[str]],
) -> tuple[StopStateBucket, ...]:
    buckets = []
    for symbol, side in sorted(bucket_counts):
        counts = bucket_counts[(symbol, side)]
        buckets.append(
            StopStateBucket(
                symbol=symbol,
                side=side,
                total_nonzero_signal_count=counts["total"],
                same_side_stop_valid_at_decision_close_count=counts["valid"],
                same_side_stop_breached_at_decision_close_count=counts["breached"],
                fresh_signal_count=counts["fresh"],
                held_continuation_count=counts["held"],
                breached_fresh_signal_count=counts["breached_fresh"],
                breached_held_continuation_count=counts["breached_held"],
            )
        )
    return tuple(buckets)