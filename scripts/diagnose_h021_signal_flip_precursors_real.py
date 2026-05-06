"""H021 signal-flip winner precursor diagnostic.

Diagnostic-only check for whether profitable signal_flip exits from the H020
guard-safe strict event backtest cluster in decision-time observable features.

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
from typing import Iterable, Sequence

from quantcore.backtest.h020_strict_event import backtest_h020_strict_event
from quantcore.data.bridge_windows import assess_common_complete_h4_m1_windows
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

_ALLOWED_GROUP_FIELDS = frozenset(
    {
        "symbol",
        "side",
        "decision_hour_utc",
        "entry_hour_utc",
        "stop_distance_spread_bucket",
        "estimated_gross_leverage_bucket",
    }
)

DEFAULT_GROUP_FIELD_SETS: tuple[tuple[str, ...], ...] = (
    ("symbol",),
    ("side",),
    ("decision_hour_utc",),
    ("entry_hour_utc",),
    ("stop_distance_spread_bucket",),
    ("estimated_gross_leverage_bucket",),
    ("symbol", "side"),
    ("symbol", "decision_hour_utc"),
    ("symbol", "side", "decision_hour_utc"),
    ("symbol", "stop_distance_spread_bucket"),
    ("symbol", "estimated_gross_leverage_bucket"),
    ("side", "decision_hour_utc"),
    ("stop_distance_spread_bucket", "estimated_gross_leverage_bucket"),
)


@dataclass(frozen=True)
class H021SignalFlipContrastRow:
    group_fields: tuple[str, ...]
    group: tuple[tuple[str, str], ...]
    fill_count: int
    signal_flip_winner_count: int
    signal_flip_winner_rate: float
    stop_count: int
    stop_rate: float
    losing_fill_count: int
    total_pnl_usd: float
    mean_pnl_usd: float
    median_pnl_usd: float
    signal_flip_winner_pnl_usd: float
    adverse_pnl_usd: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float


def summarize_signal_flip_contrasts(
    records: Iterable[H021StopPrecursorRecord],
    *,
    group_fields: Sequence[str],
) -> tuple[H021SignalFlipContrastRow, ...]:
    """Summarize profitable signal_flip clustering by decision-time fields."""
    _validate_group_fields(group_fields)

    groups: dict[tuple[tuple[str, str], ...], list[H021StopPrecursorRecord]] = {}
    for record in records:
        key = tuple((field, str(getattr(record, field))) for field in group_fields)
        groups.setdefault(key, []).append(record)

    rows = [
        _summarize_group(
            group_fields=tuple(group_fields),
            group=group,
            records=group_records,
        )
        for group, group_records in groups.items()
    ]

    return tuple(
        sorted(
            rows,
            key=lambda row: (
                -row.profit_factor if not isnan(row.profit_factor) else -inf,
                -row.total_pnl_usd,
                -row.fill_count,
                row.group,
            ),
        )
    )


def scan_signal_flip_winner_buckets(
    records: Iterable[H021StopPrecursorRecord],
    *,
    group_field_sets: Sequence[Sequence[str]] = DEFAULT_GROUP_FIELD_SETS,
    min_fill_count: int = 50,
    require_positive_total_pnl: bool = True,
) -> tuple[H021SignalFlipContrastRow, ...]:
    """Scan observable groupings for profitable signal_flip winner clusters."""
    if min_fill_count <= 0:
        raise ValueError("min_fill_count must be positive")

    all_rows: list[H021SignalFlipContrastRow] = []
    record_tuple = tuple(records)

    for group_fields in group_field_sets:
        rows = summarize_signal_flip_contrasts(record_tuple, group_fields=group_fields)
        for row in rows:
            if row.fill_count < min_fill_count:
                continue
            if row.signal_flip_winner_count <= 0:
                continue
            if require_positive_total_pnl and row.total_pnl_usd <= 0.0:
                continue
            all_rows.append(row)

    return tuple(
        sorted(
            all_rows,
            key=lambda row: (
                -row.profit_factor if not isnan(row.profit_factor) else -inf,
                -row.signal_flip_winner_rate,
                -row.total_pnl_usd,
                -row.fill_count,
                row.group_fields,
                row.group,
            ),
        )
    )


def format_signal_flip_contrast_table(
    rows: Sequence[H021SignalFlipContrastRow],
    *,
    title: str = "H021 signal-flip winner precursor contrast",
    max_rows: int | None = 40,
) -> str:
    """Format signal-flip contrast rows as a compact console table."""
    lines = [title]
    if not rows:
        lines.append("(no matching buckets)")
        return "\n".join(lines)

    header = (
        "fields | group | fills | sf_winners | sf_winner_rate | stops | stop_rate | "
        "losers | total_pnl_usd | median_pnl_usd | sf_winner_pnl_usd | "
        "adverse_pnl_usd | profit_factor"
    )
    lines.append(header)

    display_rows = rows if max_rows is None else rows[:max_rows]
    for row in display_rows:
        lines.append(
            " | ".join(
                [
                    ",".join(row.group_fields),
                    _format_group(row.group),
                    str(row.fill_count),
                    str(row.signal_flip_winner_count),
                    _format_percent(row.signal_flip_winner_rate),
                    str(row.stop_count),
                    _format_percent(row.stop_rate),
                    str(row.losing_fill_count),
                    _format_float(row.total_pnl_usd),
                    _format_float(row.median_pnl_usd),
                    _format_float(row.signal_flip_winner_pnl_usd),
                    _format_float(row.adverse_pnl_usd),
                    _format_float(row.profit_factor),
                ]
            )
        )

    if max_rows is not None and len(rows) > max_rows:
        lines.append(f"... truncated: showing {max_rows} of {len(rows)} rows")

    return "\n".join(lines)


def main() -> None:
    print("H021 signal-flip winner precursor diagnostic")
    print("=" * 48)
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

    assessment = assess_common_complete_h4_m1_windows(
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

    print(f"Context rows reconstructed: {len(contexts)}")
    print(f"Fill rows enriched: {len(records)}")
    print()

    rows = scan_signal_flip_winner_buckets(records, min_fill_count=50)
    print(format_signal_flip_contrast_table(rows))
    print()

    print("Interpretation reminder:")
    print("- A profitable bucket here is only an in-sample diagnostic lead.")
    print("- Signal-flip winners must still survive adverse outcomes and temporal tests.")
    print("- Do not implement trading rules from this table alone.")
    print("No live trading is approved. Phase 4 is not approved.")


def _summarize_group(
    *,
    group_fields: tuple[str, ...],
    group: tuple[tuple[str, str], ...],
    records: Sequence[H021StopPrecursorRecord],
) -> H021SignalFlipContrastRow:
    if not records:
        raise ValueError("records must not be empty")

    pnl_values = [record.pnl_usd for record in records]
    fill_count = len(records)
    signal_flip_winners = [
        record
        for record in records
        if record.exit_reason == "signal_flip" and record.pnl_usd > 0.0
    ]
    stop_count = sum(1 for record in records if record.exit_reason == "stop")
    losing_fill_count = sum(1 for value in pnl_values if value < 0.0)
    gross_profit_usd = sum(value for value in pnl_values if value > 0.0)
    gross_loss_usd = sum(value for value in pnl_values if value < 0.0)
    signal_flip_winner_pnl_usd = sum(record.pnl_usd for record in signal_flip_winners)

    return H021SignalFlipContrastRow(
        group_fields=group_fields,
        group=group,
        fill_count=fill_count,
        signal_flip_winner_count=len(signal_flip_winners),
        signal_flip_winner_rate=len(signal_flip_winners) / fill_count,
        stop_count=stop_count,
        stop_rate=stop_count / fill_count,
        losing_fill_count=losing_fill_count,
        total_pnl_usd=sum(pnl_values),
        mean_pnl_usd=sum(pnl_values) / fill_count,
        median_pnl_usd=median(pnl_values),
        signal_flip_winner_pnl_usd=signal_flip_winner_pnl_usd,
        adverse_pnl_usd=sum(pnl_values) - signal_flip_winner_pnl_usd,
        gross_profit_usd=gross_profit_usd,
        gross_loss_usd=gross_loss_usd,
        profit_factor=_profit_factor(
            gross_profit_usd=gross_profit_usd,
            gross_loss_usd=gross_loss_usd,
        ),
    )


def _validate_group_fields(group_fields: Sequence[str]) -> None:
    if not group_fields:
        raise ValueError("group_fields must not be empty")

    invalid = [field for field in group_fields if field not in _ALLOWED_GROUP_FIELDS]
    if invalid:
        raise ValueError(f"unsupported group_fields: {invalid}")


def _profit_factor(*, gross_profit_usd: float, gross_loss_usd: float) -> float:
    if gross_loss_usd < 0.0:
        return gross_profit_usd / abs(gross_loss_usd)
    if gross_profit_usd > 0.0:
        return inf
    return float("nan")


def _format_group(group: Sequence[tuple[str, str]]) -> str:
    return ",".join(f"{field}={value}" for field, value in group)


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
