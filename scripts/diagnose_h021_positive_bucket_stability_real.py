"""H021 positive bucket temporal stability diagnostic.

Diagnostic-only check for whether in-sample positive H021 bucket leads remain
positive across chronological and calendar-year splits.

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


@dataclass(frozen=True)
class H021BucketLead:
    label: str
    criteria: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class H021BucketStabilityRow:
    bucket_label: str
    period_label: str
    fill_count: int
    stop_count: int
    stop_rate: float
    total_pnl_usd: float
    mean_pnl_usd: float
    median_pnl_usd: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float


DEFAULT_BUCKET_LEADS: tuple[H021BucketLead, ...] = (
    H021BucketLead(
        label="USDJPY sell decision_hour_utc=06",
        criteria=(("symbol", "USDJPY"), ("side", "sell"), ("decision_hour_utc", "06")),
    ),
    H021BucketLead(
        label="XAUUSD sell decision_hour_utc=01",
        criteria=(("symbol", "XAUUSD"), ("side", "sell"), ("decision_hour_utc", "01")),
    ),
    H021BucketLead(
        label="XAUUSD buy decision_hour_utc=18",
        criteria=(("symbol", "XAUUSD"), ("side", "buy"), ("decision_hour_utc", "18")),
    ),
    H021BucketLead(
        label="XAUUSD decision_hour_utc=17",
        criteria=(("symbol", "XAUUSD"), ("decision_hour_utc", "17")),
    ),
    H021BucketLead(
        label="XAUUSD sell decision_hour_utc=05",
        criteria=(("symbol", "XAUUSD"), ("side", "sell"), ("decision_hour_utc", "05")),
    ),
    H021BucketLead(
        label="XAUUSD decision_hour_utc=06",
        criteria=(("symbol", "XAUUSD"), ("decision_hour_utc", "06")),
    ),
    H021BucketLead(
        label="USDJPY buy decision_hour_utc=01",
        criteria=(("symbol", "USDJPY"), ("side", "buy"), ("decision_hour_utc", "01")),
    ),
    H021BucketLead(
        label="USDJPY >=50x spread and 1-3x leverage",
        criteria=(
            ("symbol", "USDJPY"),
            ("stop_distance_spread_bucket", ">=50x"),
            ("estimated_gross_leverage_bucket", "1-3x"),
        ),
    ),
)


def record_matches_lead(
    record: H021StopPrecursorRecord,
    lead: H021BucketLead,
) -> bool:
    """Return True when a fill record matches all decision-time lead criteria."""
    return all(str(getattr(record, field)) == value for field, value in lead.criteria)


def evaluate_bucket_stability(
    records: Iterable[H021StopPrecursorRecord],
    *,
    leads: Sequence[H021BucketLead] = DEFAULT_BUCKET_LEADS,
) -> tuple[H021BucketStabilityRow, ...]:
    """Evaluate bucket leads across overall, half-split, and calendar-year periods."""
    record_tuple = tuple(records)
    rows: list[H021BucketStabilityRow] = []

    for lead in leads:
        matched = sorted(
            (record for record in record_tuple if record_matches_lead(record, lead)),
            key=lambda record: record.decision_time,
        )
        if not matched:
            continue

        rows.append(_summarize_records(matched, bucket_label=lead.label, period_label="overall"))

        split_index = len(matched) // 2
        first_half = matched[:split_index]
        second_half = matched[split_index:]
        if first_half:
            rows.append(
                _summarize_records(
                    first_half,
                    bucket_label=lead.label,
                    period_label="chronological_first_half",
                )
            )
        if second_half:
            rows.append(
                _summarize_records(
                    second_half,
                    bucket_label=lead.label,
                    period_label="chronological_second_half",
                )
            )

        years = sorted({record.decision_time.year for record in matched})
        for year in years:
            year_records = [record for record in matched if record.decision_time.year == year]
            rows.append(
                _summarize_records(
                    year_records,
                    bucket_label=lead.label,
                    period_label=f"calendar_year_{year}",
                )
            )

    return tuple(rows)


def format_bucket_stability_table(
    rows: Sequence[H021BucketStabilityRow],
    *,
    title: str = "H021 positive bucket temporal stability",
) -> str:
    """Format stability rows as a compact console table."""
    lines = [title]
    if not rows:
        lines.append("(no matching fills)")
        return "\n".join(lines)

    header = (
        "bucket | period | fills | stops | stop_rate | total_pnl_usd | "
        "mean_pnl_usd | median_pnl_usd | gross_profit_usd | gross_loss_usd | profit_factor"
    )
    lines.append(header)

    for row in rows:
        lines.append(
            " | ".join(
                [
                    row.bucket_label,
                    row.period_label,
                    str(row.fill_count),
                    str(row.stop_count),
                    _format_percent(row.stop_rate),
                    _format_float(row.total_pnl_usd),
                    _format_float(row.mean_pnl_usd),
                    _format_float(row.median_pnl_usd),
                    _format_float(row.gross_profit_usd),
                    _format_float(row.gross_loss_usd),
                    _format_float(row.profit_factor),
                ]
            )
        )

    return "\n".join(lines)


def main() -> None:
    print("H021 positive bucket temporal stability diagnostic")
    print("=" * 58)
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

    rows = evaluate_bucket_stability(records)
    print(format_bucket_stability_table(rows))
    print()

    print("Interpretation reminder:")
    print("- Stable across time still would not be a strategy.")
    print("- One good year and several bad years is not stable.")
    print("- PF near 1.0 with unstable yearly splits is likely noise.")
    print("No live trading is approved. Phase 4 is not approved.")


def _summarize_records(
    records: Sequence[H021StopPrecursorRecord],
    *,
    bucket_label: str,
    period_label: str,
) -> H021BucketStabilityRow:
    if not records:
        raise ValueError("records must not be empty")

    pnl_values = [record.pnl_usd for record in records]
    fill_count = len(records)
    stop_count = sum(1 for record in records if record.exit_reason == "stop")
    gross_profit_usd = sum(value for value in pnl_values if value > 0.0)
    gross_loss_usd = sum(value for value in pnl_values if value < 0.0)

    return H021BucketStabilityRow(
        bucket_label=bucket_label,
        period_label=period_label,
        fill_count=fill_count,
        stop_count=stop_count,
        stop_rate=stop_count / fill_count,
        total_pnl_usd=sum(pnl_values),
        mean_pnl_usd=sum(pnl_values) / fill_count,
        median_pnl_usd=median(pnl_values),
        gross_profit_usd=gross_profit_usd,
        gross_loss_usd=gross_loss_usd,
        profit_factor=_profit_factor(
            gross_profit_usd=gross_profit_usd,
            gross_loss_usd=gross_loss_usd,
        ),
    )


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
