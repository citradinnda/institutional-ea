"""Diagnostic classification for H018 invalid directional stops.

Diagnostic-only. This module does not execute trades, tune H017, skip/clip
trades in validation, promote H018, or approve live trading.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd

from quantcore.backtest.h017_event import _SYMBOLS
from quantcore.backtest.h017_strict_event import (
    _as_strict_utc_datetime_index,
    _mask_h017_to_strict_entries,
    _validate_h017_decision_index,
)
from quantcore.strategy.h017 import H017Result


@dataclass(frozen=True)
class InvalidStopCauseObservation:
    symbol: str
    side: str
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    decision_close: float
    entry_open: float
    stop_price: float
    valid_at_decision_close: bool
    valid_at_entry_open: bool
    cause: str
    signed_risk_fraction: float = 0.0
    signal_value: float | None = None
    selected_stop_panel: str = ""
    long_stop_price: float | None = None
    short_stop_price: float | None = None
    long_stop_valid_at_decision_close: bool | None = None
    short_stop_valid_at_decision_close: bool | None = None
    stop_panel_diagnostic: str = ""

    @property
    def decision_margin(self) -> float:
        """Positive means valid versus decision close."""

        if self.side == "buy":
            return self.decision_close - self.stop_price
        return self.stop_price - self.decision_close

    @property
    def entry_margin(self) -> float:
        """Positive means valid versus entry open."""

        if self.side == "buy":
            return self.entry_open - self.stop_price
        return self.stop_price - self.entry_open


@dataclass(frozen=True)
class InvalidStopCauseDiagnostic:
    event_interval_count: int
    trade_intent_count: int
    invalid_at_entry_count: int
    accepted_entry_count: int | None
    executed_entry_count: int | None
    skipped_entry_count: int | None
    observations: tuple[InvalidStopCauseObservation, ...]

    @property
    def cause_counts(self) -> dict[str, int]:
        return dict(Counter(obs.cause for obs in self.observations))

    @property
    def invalid_counts_by_symbol(self) -> dict[str, int]:
        return dict(Counter(obs.symbol for obs in self.observations))

    @property
    def invalid_counts_by_side(self) -> dict[str, int]:
        return dict(Counter(obs.side for obs in self.observations))

    @property
    def stop_panel_diagnostic_counts(self) -> dict[str, int]:
        return dict(Counter(obs.stop_panel_diagnostic for obs in self.observations))


def diagnose_invalid_stop_causes(
    *,
    h017_result: H017Result,
    h4_by_symbol: Mapping[str, pd.DataFrame],
    accepted_entry_times: pd.DatetimeIndex,
    expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
) -> InvalidStopCauseDiagnostic:
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

    base = diagnose_invalid_stop_causes_from_masked_result(
        h017_result=masked_h017,
        h4_by_symbol=h4_by_symbol,
    )

    return InvalidStopCauseDiagnostic(
        event_interval_count=base.event_interval_count,
        trade_intent_count=base.trade_intent_count,
        invalid_at_entry_count=base.invalid_at_entry_count,
        accepted_entry_count=len(accepted_index),
        executed_entry_count=len(executed_entry_times),
        skipped_entry_count=len(skipped_entry_times),
        observations=base.observations,
    )


def diagnose_invalid_stop_causes_from_masked_result(
    *,
    h017_result: Any,
    h4_by_symbol: Mapping[str, pd.DataFrame],
) -> InvalidStopCauseDiagnostic:
    index = pd.DatetimeIndex(h017_result.positions.index)
    observations: list[InvalidStopCauseObservation] = []
    trade_intent_count = 0

    if len(index) < 3:
        return InvalidStopCauseDiagnostic(
            event_interval_count=0,
            trade_intent_count=0,
            invalid_at_entry_count=0,
            accepted_entry_count=None,
            executed_entry_count=None,
            skipped_entry_count=None,
            observations=(),
        )

    for i in range(1, len(index) - 1):
        decision_time = pd.Timestamp(index[i - 1])
        entry_time = pd.Timestamp(index[i])

        for symbol in _SYMBOLS:
            signed_risk_fraction = float(
                h017_result.positions.at[decision_time, symbol]
            )
            if pd.isna(signed_risk_fraction) or signed_risk_fraction == 0.0:
                continue

            trade_intent_count += 1
            side = "buy" if signed_risk_fraction > 0.0 else "sell"
            selected_stop_panel = "stops_long" if side == "buy" else "stops_short"

            long_stop_price = _optional_stop_price(
                h017_result.stops_long,
                decision_time,
                symbol,
            )
            short_stop_price = _optional_stop_price(
                h017_result.stops_short,
                decision_time,
                symbol,
            )
            stop_price = long_stop_price if side == "buy" else short_stop_price

            if stop_price is None:
                continue

            signal_value = _optional_signal_value(
                h017_result=h017_result,
                decision_time=decision_time,
                symbol=symbol,
            )

            h4_bars = h4_by_symbol[symbol]
            decision_close = float(h4_bars.at[decision_time, "close"])
            entry_open = float(h4_bars.at[entry_time, "open"])

            long_stop_valid_at_decision_close = (
                None
                if long_stop_price is None
                else _is_directionally_valid(
                    side="buy",
                    reference_price=decision_close,
                    stop_price=long_stop_price,
                )
            )
            short_stop_valid_at_decision_close = (
                None
                if short_stop_price is None
                else _is_directionally_valid(
                    side="sell",
                    reference_price=decision_close,
                    stop_price=short_stop_price,
                )
            )

            valid_at_decision_close = _is_directionally_valid(
                side=side,
                reference_price=decision_close,
                stop_price=stop_price,
            )
            valid_at_entry_open = _is_directionally_valid(
                side=side,
                reference_price=entry_open,
                stop_price=stop_price,
            )

            if valid_at_entry_open:
                continue

            observations.append(
                InvalidStopCauseObservation(
                    symbol=symbol,
                    side=side,
                    decision_time=decision_time,
                    entry_time=entry_time,
                    decision_close=decision_close,
                    entry_open=entry_open,
                    stop_price=stop_price,
                    valid_at_decision_close=valid_at_decision_close,
                    valid_at_entry_open=valid_at_entry_open,
                    cause=_classify_cause(
                        valid_at_decision_close=valid_at_decision_close,
                        valid_at_entry_open=valid_at_entry_open,
                    ),
                    signed_risk_fraction=signed_risk_fraction,
                    signal_value=signal_value,
                    selected_stop_panel=selected_stop_panel,
                    long_stop_price=long_stop_price,
                    short_stop_price=short_stop_price,
                    long_stop_valid_at_decision_close=(
                        long_stop_valid_at_decision_close
                    ),
                    short_stop_valid_at_decision_close=(
                        short_stop_valid_at_decision_close
                    ),
                    stop_panel_diagnostic=_classify_stop_panel_diagnostic(
                        selected_stop_valid_at_decision_close=(
                            valid_at_decision_close
                        ),
                        opposite_stop_valid_at_decision_close=(
                            short_stop_valid_at_decision_close
                            if side == "buy"
                            else long_stop_valid_at_decision_close
                        ),
                    ),
                )
            )

    return InvalidStopCauseDiagnostic(
        event_interval_count=len(index) - 2,
        trade_intent_count=trade_intent_count,
        invalid_at_entry_count=len(observations),
        accepted_entry_count=None,
        executed_entry_count=None,
        skipped_entry_count=None,
        observations=tuple(observations),
    )


def _optional_stop_price(
    panel: pd.DataFrame,
    decision_time: pd.Timestamp,
    symbol: str,
) -> float | None:
    stop_price = float(panel.at[decision_time, symbol])
    if pd.isna(stop_price):
        return None
    return stop_price


def _optional_signal_value(
    *,
    h017_result: Any,
    decision_time: pd.Timestamp,
    symbol: str,
) -> float | None:
    signals = getattr(h017_result, "signals", None)
    if signals is None:
        return None
    if symbol not in signals.columns:
        return None

    signal_value = float(signals.at[decision_time, symbol])
    if pd.isna(signal_value):
        return None
    return signal_value


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


def _classify_cause(
    *,
    valid_at_decision_close: bool,
    valid_at_entry_open: bool,
) -> str:
    if valid_at_entry_open:
        return "valid_at_entry_open"
    if valid_at_decision_close:
        return "crossed_between_decision_close_and_entry_open"
    return "already_invalid_at_decision_close"


def _classify_stop_panel_diagnostic(
    *,
    selected_stop_valid_at_decision_close: bool,
    opposite_stop_valid_at_decision_close: bool | None,
) -> str:
    if selected_stop_valid_at_decision_close:
        return "selected_panel_protective_at_decision_close"
    if opposite_stop_valid_at_decision_close is True:
        return "selected_panel_nonprotective_opposite_panel_protective"
    if opposite_stop_valid_at_decision_close is False:
        return "selected_panel_nonprotective_both_panels_nonprotective"
    return "selected_panel_nonprotective_opposite_panel_unavailable"