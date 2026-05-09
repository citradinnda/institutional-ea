"""H024 pullback-continuation signal diagnostic shell.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

This module intentionally starts with signal/reporting diagnostics only. It does
not run real-data validation unless explicitly wired and authorized later.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, Sequence

import pandas as pd

from quantcore.strategy.h024 import H024SignalConfig, generate_h024_signals


DEFAULT_H024_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class H024SignalSummary:
    symbol: str
    bar_count: int
    signal_count: int
    long_signal_count: int
    short_signal_count: int
    flat_count: int
    signal_rate: float
    long_share: float
    short_share: float
    first_signal_time_utc: pd.Timestamp | None
    last_signal_time_utc: pd.Timestamp | None


@dataclass(frozen=True)
class H024SignalSplitSummary:
    label: str
    symbol: str
    bar_count: int
    signal_count: int
    long_signal_count: int
    short_signal_count: int
    signal_rate: float


def summarize_h024_signals(
    *,
    symbol: str,
    h4_bars: pd.DataFrame,
    config: H024SignalConfig | None = None,
) -> H024SignalSummary:
    """Summarize H024 signal frequency for one symbol."""

    if not symbol:
        raise ValueError("symbol must be non-empty")
    if not isinstance(h4_bars.index, pd.DatetimeIndex):
        raise ValueError("h4_bars must use a DatetimeIndex")

    signals = generate_h024_signals(h4_bars, config=config)
    return summarize_h024_signal_series(symbol=symbol, signals=signals)


def summarize_h024_signal_series(*, symbol: str, signals: pd.Series) -> H024SignalSummary:
    """Summarize a precomputed H024 signal series."""

    if not symbol:
        raise ValueError("symbol must be non-empty")
    if not isinstance(signals.index, pd.DatetimeIndex):
        raise ValueError("signals must use a DatetimeIndex")

    cleaned = signals.fillna(0).astype(int)
    bar_count = int(len(cleaned))
    long_signal_count = int((cleaned == 1).sum())
    short_signal_count = int((cleaned == -1).sum())
    signal_count = long_signal_count + short_signal_count
    flat_count = int((cleaned == 0).sum())

    signal_times = cleaned.index[cleaned != 0]
    first_signal_time = None
    last_signal_time = None
    if len(signal_times) > 0:
        first_signal_time = pd.Timestamp(signal_times[0])
        last_signal_time = pd.Timestamp(signal_times[-1])

    return H024SignalSummary(
        symbol=symbol,
        bar_count=bar_count,
        signal_count=signal_count,
        long_signal_count=long_signal_count,
        short_signal_count=short_signal_count,
        flat_count=flat_count,
        signal_rate=_safe_ratio(signal_count, bar_count),
        long_share=_safe_ratio(long_signal_count, signal_count),
        short_share=_safe_ratio(short_signal_count, signal_count),
        first_signal_time_utc=first_signal_time,
        last_signal_time_utc=last_signal_time,
    )


def summarize_h024_chronological_splits(
    *,
    symbol: str,
    signals: pd.Series,
    split_count: int,
) -> tuple[H024SignalSplitSummary, ...]:
    """Split one signal series into chronological equal-sized slices."""

    if not symbol:
        raise ValueError("symbol must be non-empty")
    if split_count < 2:
        raise ValueError("split_count must be >= 2")
    if not isinstance(signals.index, pd.DatetimeIndex):
        raise ValueError("signals must use a DatetimeIndex")

    cleaned = signals.fillna(0).astype(int)
    if cleaned.empty:
        return tuple()

    split_indices = _chronological_split_indices(len(cleaned), split_count)
    summaries = []

    for split_number, index_values in enumerate(split_indices, start=1):
        split_signals = cleaned.iloc[index_values]
        long_count = int((split_signals == 1).sum())
        short_count = int((split_signals == -1).sum())
        signal_count = long_count + short_count
        bar_count = int(len(split_signals))
        summaries.append(
            H024SignalSplitSummary(
                label=f"part_{split_number}_of_{split_count}",
                symbol=symbol,
                bar_count=bar_count,
                signal_count=signal_count,
                long_signal_count=long_count,
                short_signal_count=short_count,
                signal_rate=_safe_ratio(signal_count, bar_count),
            )
        )

    return tuple(summaries)


def summarize_h024_multi_symbol_signals(
    *,
    h4_bars_by_symbol: dict[str, pd.DataFrame],
    config: H024SignalConfig | None = None,
) -> tuple[H024SignalSummary, ...]:
    """Summarize H024 signal frequency for multiple symbols."""

    summaries = []
    for symbol in sorted(h4_bars_by_symbol):
        summaries.append(
            summarize_h024_signals(
                symbol=symbol,
                h4_bars=h4_bars_by_symbol[symbol],
                config=config,
            )
        )
    return tuple(summaries)


def format_h024_signal_summary_table(summaries: Sequence[H024SignalSummary]) -> str:
    """Format H024 signal summaries as a stable text table."""

    rows = [
        "symbol | bars | signals | long | short | flat | signal_rate | long_share | short_share | first_signal_utc | last_signal_utc",
        "--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---",
    ]

    for summary in summaries:
        rows.append(
            " | ".join(
                [
                    summary.symbol,
                    str(summary.bar_count),
                    str(summary.signal_count),
                    str(summary.long_signal_count),
                    str(summary.short_signal_count),
                    str(summary.flat_count),
                    _format_float(summary.signal_rate),
                    _format_float(summary.long_share),
                    _format_float(summary.short_share),
                    _format_timestamp(summary.first_signal_time_utc),
                    _format_timestamp(summary.last_signal_time_utc),
                ]
            )
        )

    return "\n".join(rows)


def format_h024_split_summary_table(summaries: Sequence[H024SignalSplitSummary]) -> str:
    """Format H024 chronological split summaries as a stable text table."""

    rows = [
        "label | symbol | bars | signals | long | short | signal_rate",
        "--- | --- | ---: | ---: | ---: | ---: | ---:",
    ]

    for summary in summaries:
        rows.append(
            " | ".join(
                [
                    summary.label,
                    summary.symbol,
                    str(summary.bar_count),
                    str(summary.signal_count),
                    str(summary.long_signal_count),
                    str(summary.short_signal_count),
                    _format_float(summary.signal_rate),
                ]
            )
        )

    return "\n".join(rows)


def build_h024_signal_diagnostic_report(
    *,
    h4_bars_by_symbol: dict[str, pd.DataFrame],
    config: H024SignalConfig | None = None,
) -> str:
    """Build a signal-only H024 diagnostic report.

    This intentionally reports signal frequency and chronological stability
    before any real-data P&L diagnostic is introduced.
    """

    summaries = summarize_h024_multi_symbol_signals(
        h4_bars_by_symbol=h4_bars_by_symbol,
        config=config,
    )

    split_summaries: list[H024SignalSplitSummary] = []
    for symbol in sorted(h4_bars_by_symbol):
        signals = generate_h024_signals(h4_bars_by_symbol[symbol], config=config)
        split_summaries.extend(
            summarize_h024_chronological_splits(
                symbol=symbol,
                signals=signals,
                split_count=2,
            )
        )
        split_summaries.extend(
            summarize_h024_chronological_splits(
                symbol=symbol,
                signals=signals,
                split_count=3,
            )
        )

    return "\n\n".join(
        [
            "H024 signal diagnostic report",
            "Signal summary:",
            format_h024_signal_summary_table(summaries),
            "Chronological splits:",
            format_h024_split_summary_table(split_summaries),
        ]
    )


def _chronological_split_indices(length: int, split_count: int) -> tuple[list[int], ...]:
    base_size = length // split_count
    remainder = length % split_count

    splits = []
    cursor = 0
    for split_index in range(split_count):
        split_size = base_size + (1 if split_index < remainder else 0)
        splits.append(list(range(cursor, cursor + split_size)))
        cursor += split_size

    return tuple(splits)


def _safe_ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return float("nan")
    return float(numerator) / float(denominator)


def _format_float(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.6f}"


def _format_timestamp(value: pd.Timestamp | None) -> str:
    if value is None:
        return "none"
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    else:
        timestamp = timestamp.tz_convert("UTC")
    return timestamp.isoformat()
