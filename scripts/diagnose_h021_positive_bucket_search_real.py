"""H021 positive bucket search diagnostic.

This script is diagnostic-only. It searches enriched H021 fill records for
decision-time observable buckets with positive expectancy after modeled costs.

It is not:
- a new strategy,
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

_ALLOWED_BUCKET_FIELDS = frozenset(
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
    ("symbol", "stop_distance_spread_bucket"),
    ("symbol", "estimated_gross_leverage_bucket"),
    ("side", "decision_hour_utc"),
    ("stop_distance_spread_bucket", "estimated_gross_leverage_bucket"),
    ("symbol", "side", "decision_hour_utc"),
    ("symbol", "side", "stop_distance_spread_bucket"),
    ("symbol", "side", "estimated_gross_leverage_bucket"),
    ("symbol", "stop_distance_spread_bucket", "estimated_gross_leverage_bucket"),
)

DEFAULT_MIN_FILL_COUNTS: tuple[int, ...] = (30, 50, 100)


@dataclass(frozen=True)
class H021PositiveBucketRow:
    group_fields: tuple[str, ...]
    group: tuple[tuple[str, str], ...]
    min_fill_count: int
    fill_count: int
    stop_count: int
    stop_rate: float
    total_pnl_usd: float
    mean_pnl_usd: float
    median_pnl_usd: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float

    @property
    def group_fields_label(self) -> str:
        return "+".join(self.group_fields)

    @property
    def group_label(self) -> str:
        return " | ".join(f"{field}={value}" for field, value in self.group)


def summarize_positive_buckets(
    records: Iterable[H021StopPrecursorRecord],
    *,
    group_fields: Sequence[str],
    min_fill_count: int,
    positive_only: bool = True,
) -> list[H021PositiveBucketRow]:
    """Summarize records by decision-time bucket fields."""
    validated_fields = _validate_group_fields(group_fields)
    if min_fill_count < 1:
        raise ValueError("min_fill_count must be >= 1")

    buckets: dict[tuple[str, ...], list[H021StopPrecursorRecord]] = {}
    for record in records:
        key = tuple(str(getattr(record, field)) for field in validated_fields)
        buckets.setdefault(key, []).append(record)

    rows: list[H021PositiveBucketRow] = []
    for key, bucket_records in buckets.items():
        fill_count = len(bucket_records)
        if fill_count < min_fill_count:
            continue

        pnl_values = [record.pnl_usd for record in bucket_records]
        stop_count = sum(1 for record in bucket_records if record.exit_reason == "stop")
        gross_profit_usd = sum(value for value in pnl_values if value > 0.0)
        gross_loss_usd = sum(value for value in pnl_values if value < 0.0)
        total_pnl_usd = sum(pnl_values)
        profit_factor = _profit_factor(
            gross_profit_usd=gross_profit_usd,
            gross_loss_usd=gross_loss_usd,
        )

        if positive_only and not (total_pnl_usd > 0.0 and profit_factor > 1.0):
            continue

        rows.append(
            H021PositiveBucketRow(
                group_fields=validated_fields,
                group=tuple(zip(validated_fields, key, strict=True)),
                min_fill_count=min_fill_count,
                fill_count=fill_count,
                stop_count=stop_count,
                stop_rate=stop_count / fill_count,
                total_pnl_usd=total_pnl_usd,
                mean_pnl_usd=total_pnl_usd / fill_count,
                median_pnl_usd=median(pnl_values),
                gross_profit_usd=gross_profit_usd,
                gross_loss_usd=gross_loss_usd,
                profit_factor=profit_factor,
            )
        )

    return sorted(rows, key=_bucket_sort_key)


def evaluate_positive_bucket_search(
    records: Iterable[H021StopPrecursorRecord],
    *,
    group_field_sets: Sequence[Sequence[str]] = DEFAULT_GROUP_FIELD_SETS,
    min_fill_counts: Sequence[int] = DEFAULT_MIN_FILL_COUNTS,
    positive_only: bool = True,
) -> list[H021PositiveBucketRow]:
    """Run the configured positive-bucket scan."""
    record_tuple = tuple(records)
    rows: list[H021PositiveBucketRow] = []

    for min_fill_count in min_fill_counts:
        for group_fields in group_field_sets:
            rows.extend(
                summarize_positive_buckets(
                    record_tuple,
                    group_fields=group_fields,
                    min_fill_count=min_fill_count,
                    positive_only=positive_only,
                )
            )

    return sorted(rows, key=_bucket_sort_key)


def format_positive_bucket_table(
    rows: Sequence[H021PositiveBucketRow],
    *,
    title: str,
    limit: int = 25,
) -> str:
    """Format positive-bucket rows as a compact text table."""
    lines = [title]
    if not rows:
        lines.append("(no positive buckets at this threshold)")
        return "\n".join(lines)

    lines.append(
        "min_fills | field_set | group | fills | stops | stop_rate | "
        "total_pnl_usd | mean_pnl_usd | median_pnl_usd | "
        "gross_profit_usd | gross_loss_usd | profit_factor"
    )

    for row in rows[:limit]:
        lines.append(
            f"{row.min_fill_count} | "
            f"{row.group_fields_label} | "
            f"{row.group_label} | "
            f"{row.fill_count} | "
            f"{row.stop_count} | "
            f"{_format_percent(row.stop_rate)} | "
            f"{_format_float(row.total_pnl_usd)} | "
            f"{_format_float(row.mean_pnl_usd)} | "
            f"{_format_float(row.median_pnl_usd)} | "
            f"{_format_float(row.gross_profit_usd)} | "
            f"{_format_float(row.gross_loss_usd)} | "
            f"{_format_float(row.profit_factor)}"
        )

    return "\n".join(lines)


def main() -> None:
    print("H021 positive bucket search diagnostic from H020 strict event fills")
    print("=" * 76)
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

    rows = evaluate_positive_bucket_search(records)
    for min_fill_count in DEFAULT_MIN_FILL_COUNTS:
        threshold_rows = [row for row in rows if row.min_fill_count == min_fill_count]
        print(
            format_positive_bucket_table(
                threshold_rows,
                title=f"Positive buckets with at least {min_fill_count} fills",
                limit=30,
            )
        )
        print()

    print("Interpretation reminder:")
    print("- A profitable bucket is not a strategy.")
    print("- Tiny buckets are likely noise.")
    print("- Any positive-core lead still needs temporal stability checks.")
    print("No live trading is approved. Phase 4 is not approved.")


def _validate_group_fields(group_fields: Sequence[str]) -> tuple[str, ...]:
    if not group_fields:
        raise ValueError("group_fields must not be empty")

    validated_fields = tuple(group_fields)
    unknown_fields = sorted(set(validated_fields) - _ALLOWED_BUCKET_FIELDS)
    if unknown_fields:
        raise ValueError(f"unsupported group field(s): {unknown_fields}")

    return validated_fields


def _profit_factor(*, gross_profit_usd: float, gross_loss_usd: float) -> float:
    if gross_loss_usd < 0.0:
        return gross_profit_usd / abs(gross_loss_usd)
    if gross_profit_usd > 0.0:
        return inf
    return float("nan")


def _bucket_sort_key(row: H021PositiveBucketRow) -> tuple[float, float, float, int]:
    profit_factor = row.profit_factor
    if isnan(profit_factor):
        profit_factor = -inf

    return (
        -profit_factor,
        -row.total_pnl_usd,
        -row.mean_pnl_usd,
        -row.fill_count,
    )


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
