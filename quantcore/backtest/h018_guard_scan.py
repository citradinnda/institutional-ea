"""Diagnostic H018 guard-violation scanner.

This module is diagnostic-only. It does not execute trades, skip trades in a
validation run, clip sizes, tune H017, promote H018, or approve live trading.
"""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Mapping

import pandas as pd

from quantcore.backtest.h017_event import (
    H017EventInvalidStopError,
    H018MaximumPerTradeLeverageError,
    H018MinimumStopDistanceError,
    _MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE,
    _SYMBOLS,
    _build_symbol_interval_candidate,
)
from quantcore.backtest.h017_strict_event import (
    _as_strict_utc_datetime_index,
    _mask_h017_to_strict_entries,
    _validate_h017_decision_index,
)
from quantcore.strategy.h017 import H017Result


@dataclass(frozen=True)
class H018GuardViolation:
    """One diagnostic guard violation found outside promotable validation."""

    guard_name: str
    symbol: str | None
    side: str | None
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_raw_price: float | None
    stop_price: float | None
    message: str


@dataclass(frozen=True)
class H018GuardScanResult:
    """Diagnostic summary of H018 guard failures across event intervals."""

    event_interval_count: int
    trade_intent_count: int
    candidate_count: int
    skipped_intent_count: int
    accepted_entry_count: int | None
    executed_entry_count: int | None
    skipped_entry_count: int | None
    violations: tuple[H018GuardViolation, ...]

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    @property
    def violation_counts_by_guard(self) -> dict[str, int]:
        return dict(Counter(violation.guard_name for violation in self.violations))

    @property
    def violation_counts_by_symbol(self) -> dict[str, int]:
        return dict(
            Counter(
                violation.symbol
                for violation in self.violations
                if violation.symbol is not None
            )
        )


def scan_h018_guard_violations(
    *,
    h017_result: H017Result,
    h4_by_symbol: Mapping[str, pd.DataFrame],
    accepted_entry_times: pd.DatetimeIndex,
    starting_equity_usd: float = 10_000.0,
    expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
) -> H018GuardScanResult:
    """Scan strict accepted H017 intervals for H018 guard violations.

    Equity is held constant at ``starting_equity_usd`` because this scanner does
    not execute fills. Leverage findings are therefore diagnostic, not a
    promotable validation result.
    """

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

    base_result = scan_h018_guard_violations_from_masked_result(
        h017_result=masked_h017,
        h4_by_symbol=h4_by_symbol,
        starting_equity_usd=starting_equity_usd,
    )

    return H018GuardScanResult(
        event_interval_count=base_result.event_interval_count,
        trade_intent_count=base_result.trade_intent_count,
        candidate_count=base_result.candidate_count,
        skipped_intent_count=base_result.skipped_intent_count,
        accepted_entry_count=len(accepted_index),
        executed_entry_count=len(executed_entry_times),
        skipped_entry_count=len(skipped_entry_times),
        violations=base_result.violations,
    )


def scan_h018_guard_violations_from_masked_result(
    *,
    h017_result: Any,
    h4_by_symbol: Mapping[str, pd.DataFrame],
    starting_equity_usd: float = 10_000.0,
) -> H018GuardScanResult:
    """Scan an already-masked H017 result.

    This lower-level function is useful for focused tests and diagnostics where
    the caller already controls which event intervals are allowed to express
    trade intent.
    """

    if starting_equity_usd <= 0.0:
        raise ValueError("starting_equity_usd must be positive")

    index = pd.DatetimeIndex(h017_result.positions.index)
    violations: list[H018GuardViolation] = []
    trade_intent_count = 0
    candidate_count = 0
    skipped_intent_count = 0

    if len(index) < 3:
        return H018GuardScanResult(
            event_interval_count=0,
            trade_intent_count=0,
            candidate_count=0,
            skipped_intent_count=0,
            accepted_entry_count=None,
            executed_entry_count=None,
            skipped_entry_count=None,
            violations=(),
        )

    for i in range(1, len(index) - 1):
        decision_time = pd.Timestamp(index[i - 1])
        entry_time = pd.Timestamp(index[i])
        forced_exit_time = pd.Timestamp(index[i + 1])

        interval_candidates = []

        for symbol in _SYMBOLS:
            signed_risk_fraction = float(
                h017_result.positions.at[decision_time, symbol]
            )
            if pd.isna(signed_risk_fraction) or signed_risk_fraction == 0.0:
                continue

            trade_intent_count += 1

            try:
                maybe_candidate = _build_symbol_interval_candidate(
                    symbol=symbol,
                    h017_result=h017_result,
                    h4_bars=h4_by_symbol[symbol],
                    decision_time=decision_time,
                    entry_time=entry_time,
                    forced_exit_time=forced_exit_time,
                    equity_usd=starting_equity_usd,
                )
            except H017EventInvalidStopError as exc:
                violations.append(
                    _violation_from_exception(
                        guard_name="invalid_directional_stop",
                        exc=exc,
                        symbol=symbol,
                        h017_result=h017_result,
                        h4_bars=h4_by_symbol[symbol],
                        decision_time=decision_time,
                        entry_time=entry_time,
                    )
                )
                continue
            except H018MinimumStopDistanceError as exc:
                violations.append(
                    _violation_from_exception(
                        guard_name="minimum_stop_distance",
                        exc=exc,
                        symbol=symbol,
                        h017_result=h017_result,
                        h4_bars=h4_by_symbol[symbol],
                        decision_time=decision_time,
                        entry_time=entry_time,
                    )
                )
                continue
            except H018MaximumPerTradeLeverageError as exc:
                violations.append(
                    _violation_from_exception(
                        guard_name="maximum_per_trade_usd_gross_leverage",
                        exc=exc,
                        symbol=symbol,
                        h017_result=h017_result,
                        h4_bars=h4_by_symbol[symbol],
                        decision_time=decision_time,
                        entry_time=entry_time,
                    )
                )
                continue

            if maybe_candidate is None:
                skipped_intent_count += 1
                continue

            candidate_count += 1
            interval_candidates.append(maybe_candidate)

        if interval_candidates:
            portfolio_notional_usd = sum(
                abs(float(candidate.notional_usd)) for candidate in interval_candidates
            )
            portfolio_gross_leverage = portfolio_notional_usd / starting_equity_usd

            if (
                portfolio_gross_leverage
                > _MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE
            ) and not math.isclose(
                portfolio_gross_leverage,
                _MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE,
                rel_tol=1e-12,
                abs_tol=1e-12,
            ):
                violations.append(
                    H018GuardViolation(
                        guard_name="maximum_portfolio_usd_gross_leverage",
                        symbol=None,
                        side=None,
                        decision_time=decision_time,
                        entry_time=entry_time,
                        entry_raw_price=None,
                        stop_price=None,
                        message=(
                            "portfolio USD gross leverage exceeded "
                            f"{_MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE}: "
                            f"{portfolio_gross_leverage:.12f}"
                        ),
                    )
                )

    return H018GuardScanResult(
        event_interval_count=len(index) - 2,
        trade_intent_count=trade_intent_count,
        candidate_count=candidate_count,
        skipped_intent_count=skipped_intent_count,
        accepted_entry_count=None,
        executed_entry_count=None,
        skipped_entry_count=None,
        violations=tuple(violations),
    )


def _violation_from_exception(
    *,
    guard_name: str,
    exc: Exception,
    symbol: str,
    h017_result: Any,
    h4_bars: pd.DataFrame,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
) -> H018GuardViolation:
    snapshot = _symbol_snapshot(
        symbol=symbol,
        h017_result=h017_result,
        h4_bars=h4_bars,
        decision_time=decision_time,
        entry_time=entry_time,
    )

    return H018GuardViolation(
        guard_name=guard_name,
        symbol=symbol,
        side=snapshot.side,
        decision_time=decision_time,
        entry_time=entry_time,
        entry_raw_price=snapshot.entry_raw_price,
        stop_price=snapshot.stop_price,
        message=str(exc),
    )


def _symbol_snapshot(
    *,
    symbol: str,
    h017_result: Any,
    h4_bars: pd.DataFrame,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
) -> SimpleNamespace:
    signed_risk_fraction = float(h017_result.positions.at[decision_time, symbol])
    side = "buy" if signed_risk_fraction > 0.0 else "sell"
    stop_panel = h017_result.stops_long if side == "buy" else h017_result.stops_short

    entry_raw_price = None
    stop_price = None

    try:
        entry_raw_price = float(h4_bars.at[entry_time, "open"])
    except Exception:
        entry_raw_price = None

    try:
        stop_price = float(stop_panel.at[decision_time, symbol])
    except Exception:
        stop_price = None

    return SimpleNamespace(
        side=side,
        entry_raw_price=entry_raw_price,
        stop_price=stop_price,
    )
