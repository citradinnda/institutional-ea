from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

import pandas as pd

from quantcore.backtest.h017_event import (
    H017EventBacktestResult,
    backtest_h017_event_from_result,
)
from quantcore.strategy.h017 import H017Config, H017Result, run_h017


@dataclass(frozen=True)
class StrictH017EventBacktestResult:
    """Strict event wrapper output for audited complete-window H017 validation.

    The wrapped event engine is unchanged. This object records which native H4
    entry intervals were allowed to execute after strict complete-window
    filtering and which native intervals were forced flat.
    """

    backtest: H017EventBacktestResult
    accepted_entry_times: pd.DatetimeIndex
    executed_entry_times: pd.DatetimeIndex
    skipped_entry_times: pd.DatetimeIndex
    accepted_entry_count: int
    executed_entry_count: int
    skipped_entry_count: int
    expected_h4_delta: pd.Timedelta


def backtest_h017_strict_event_driven(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Iterable[pd.Timestamp],
    config: H017Config | None = None,
    starting_equity_usd: float = 10_000.0,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
    expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
) -> StrictH017EventBacktestResult:
    """Run H017, then execute only strict accepted native H4 entry windows.

    This wrapper is intentionally separate from ``backtest_h017_event_driven``.
    It prevents a future validation script from filtering H4 down to accepted
    timestamps and accidentally creating forced exits across multi-bar gaps.
    """

    h017_result = run_h017(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=config,
    )

    return backtest_h017_strict_event_from_result(
        h017_result=h017_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        starting_equity_usd=starting_equity_usd,
        slippage_atr_by_symbol=slippage_atr_by_symbol,
        expected_h4_delta=expected_h4_delta,
    )


def backtest_h017_strict_event_from_result(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Iterable[pd.Timestamp],
    starting_equity_usd: float = 10_000.0,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
    expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
) -> StrictH017EventBacktestResult:
    """Execute H017 only when the native entry interval is strictly complete.

    The underlying event engine uses adjacent H4 rows as:

    - decision time: ``index[i - 1]``
    - entry time: ``index[i]``
    - forced exit time: ``index[i + 1]``

    Therefore this wrapper preserves the native H4/H017 index and forces the
    decision exposure to zero unless the entry timestamp is in the strict
    accepted bridge-window set and the forced-exit timestamp is exactly one H4
    interval later.
    """

    if expected_h4_delta <= pd.Timedelta(0):
        raise ValueError(
            f"expected_h4_delta must be positive, got {expected_h4_delta}."
        )

    accepted_index = _as_strict_utc_datetime_index(
        accepted_entry_times,
        label="accepted_entry_times",
    )
    decision_index = _validate_h017_decision_index(h017_result.positions.index)

    masked_h017, executed_entry_times, skipped_entry_times = _mask_h017_to_strict_entries(
        h017_result=h017_result,
        decision_index=decision_index,
        accepted_entry_times=accepted_index,
        expected_h4_delta=expected_h4_delta,
    )

    backtest = backtest_h017_event_from_result(
        h017_result=masked_h017,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        starting_equity_usd=starting_equity_usd,
        slippage_atr_by_symbol=slippage_atr_by_symbol,
    )

    return StrictH017EventBacktestResult(
        backtest=backtest,
        accepted_entry_times=accepted_index,
        executed_entry_times=executed_entry_times,
        skipped_entry_times=skipped_entry_times,
        accepted_entry_count=len(accepted_index),
        executed_entry_count=len(executed_entry_times),
        skipped_entry_count=len(skipped_entry_times),
        expected_h4_delta=expected_h4_delta,
    )


def _mask_h017_to_strict_entries(
    *,
    h017_result: H017Result,
    decision_index: pd.DatetimeIndex,
    accepted_entry_times: pd.DatetimeIndex,
    expected_h4_delta: pd.Timedelta,
) -> tuple[H017Result, pd.DatetimeIndex, pd.DatetimeIndex]:
    """Return an H017 result whose invalid execution intervals are forced flat."""

    accepted_set = set(accepted_entry_times)
    original_positions = h017_result.positions
    masked_positions = original_positions.copy() * 0.0

    executed_entries: list[pd.Timestamp] = []
    skipped_entries: list[pd.Timestamp] = []
    decision_labels_to_keep: list[pd.Timestamp] = []

    for i in range(1, len(decision_index) - 1):
        decision_time = decision_index[i - 1]
        entry_time = decision_index[i]
        forced_exit_time = decision_index[i + 1]

        interval_is_strict = (
            entry_time in accepted_set
            and forced_exit_time - entry_time == expected_h4_delta
        )

        if interval_is_strict:
            executed_entries.append(entry_time)
            decision_labels_to_keep.append(decision_time)
        else:
            skipped_entries.append(entry_time)

    for decision_time in decision_labels_to_keep:
        masked_positions.loc[decision_time] = original_positions.loc[decision_time]

    masked_h017 = H017Result(
        positions=masked_positions,
        signals=h017_result.signals,
        stops_long=h017_result.stops_long,
        stops_short=h017_result.stops_short,
        vol_multipliers=h017_result.vol_multipliers,
        heat_multipliers=h017_result.heat_multipliers,
        heat_pre=h017_result.heat_pre,
        heat_post=h017_result.heat_post,
        heat_binding=h017_result.heat_binding,
    )

    return (
        masked_h017,
        pd.DatetimeIndex(executed_entries, tz="UTC"),
        pd.DatetimeIndex(skipped_entries, tz="UTC"),
    )


def _validate_h017_decision_index(index: pd.Index) -> pd.DatetimeIndex:
    """Validate the H017 decision index before deriving strict event intervals."""

    if not isinstance(index, pd.DatetimeIndex):
        raise ValueError("H017 positions must use a DatetimeIndex.")

    if index.tz is None:
        raise ValueError("H017 positions index must be timezone-aware UTC.")

    index_utc = index.tz_convert("UTC")

    if not index_utc.is_monotonic_increasing:
        raise ValueError("H017 positions index must be sorted ascending.")

    if index_utc.has_duplicates:
        raise ValueError("H017 positions index must not contain duplicate timestamps.")

    return index_utc


def _as_strict_utc_datetime_index(
    values: Iterable[pd.Timestamp],
    *,
    label: str,
) -> pd.DatetimeIndex:
    """Require an explicit sorted unique timezone-aware UTC timestamp set."""

    index = pd.DatetimeIndex(values)

    if len(index) == 0:
        return pd.DatetimeIndex([], tz="UTC")

    if index.tz is None:
        raise ValueError(f"{label} must be timezone-aware UTC.")

    probe = pd.Timestamp("2024-01-01 00:00:00", tz=index.tz)
    if probe.utcoffset() != pd.Timedelta(0):
        raise ValueError(f"{label} must be UTC, got timezone {index.tz!r}.")

    index_utc = index.tz_convert("UTC")

    if index_utc.has_duplicates:
        raise ValueError(f"{label} must not contain duplicate timestamps.")

    if not index_utc.is_monotonic_increasing:
        raise ValueError(f"{label} must be sorted ascending.")

    return index_utc
