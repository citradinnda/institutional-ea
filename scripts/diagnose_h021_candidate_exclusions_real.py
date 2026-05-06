"""H021 candidate exclusion diagnostic.

This script is diagnostic-only. It evaluates simple decision-time exclusion
candidates against already-enriched H021 stop precursor records.

It is not:
- a new strategy,
- a validation pass,
- live-trading approval,
- Phase 4 approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, Sequence

import pandas as pd

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
class H021ExclusionRule:
    field: str
    values: tuple[str, ...]


@dataclass(frozen=True)
class H021CandidateExclusion:
    name: str
    rules: tuple[H021ExclusionRule, ...]


@dataclass(frozen=True)
class H021RecordSetSummary:
    fill_count: int
    stop_count: int
    stop_rate: float
    winning_fill_count: int
    losing_fill_count: int
    total_pnl_usd: float
    mean_pnl_usd: float
    median_pnl_usd: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float


@dataclass(frozen=True)
class H021CandidateExclusionResult:
    candidate: H021CandidateExclusion
    baseline: H021RecordSetSummary
    excluded: H021RecordSetSummary
    retained: H021RecordSetSummary

    @property
    def removed_pnl_usd(self) -> float:
        return self.excluded.total_pnl_usd

    @property
    def retained_pnl_improvement_usd(self) -> float:
        return self.retained.total_pnl_usd - self.baseline.total_pnl_usd


DEFAULT_CANDIDATE_EXCLUSIONS = (
    H021CandidateExclusion(
        name="exclude_decision_hour_05",
        rules=(H021ExclusionRule("decision_hour_utc", ("05",)),),
    ),
    H021CandidateExclusion(
        name="exclude_decision_hours_05_10_22",
        rules=(H021ExclusionRule("decision_hour_utc", ("05", "10", "22")),),
    ),
    H021CandidateExclusion(
        name="exclude_entry_hour_09",
        rules=(H021ExclusionRule("entry_hour_utc", ("09",)),),
    ),
    H021CandidateExclusion(
        name="exclude_stop_distance_lt_10x_spread",
        rules=(H021ExclusionRule("stop_distance_spread_bucket", ("<2x", "2-5x", "5-10x")),),
    ),
    H021CandidateExclusion(
        name="exclude_stop_distance_lt_20x_spread",
        rules=(
            H021ExclusionRule(
                "stop_distance_spread_bucket",
                ("<2x", "2-5x", "5-10x", "10-20x"),
            ),
        ),
    ),
    H021CandidateExclusion(
        name="exclude_stop_distance_lt_50x_spread",
        rules=(
            H021ExclusionRule(
                "stop_distance_spread_bucket",
                ("<2x", "2-5x", "5-10x", "10-20x", "20-50x"),
            ),
        ),
    ),
    H021CandidateExclusion(
        name="exclude_estimated_gross_leverage_6_9x",
        rules=(H021ExclusionRule("estimated_gross_leverage_bucket", ("6-9x",)),),
    ),
    H021CandidateExclusion(
        name="exclude_estimated_gross_leverage_ge_3x",
        rules=(H021ExclusionRule("estimated_gross_leverage_bucket", ("3-6x", "6-9x")),),
    ),
    H021CandidateExclusion(
        name="exclude_usdjpy_all",
        rules=(H021ExclusionRule("symbol", ("USDJPY",)),),
    ),
    H021CandidateExclusion(
        name="exclude_usdjpy_sell",
        rules=(
            H021ExclusionRule("symbol", ("USDJPY",)),
            H021ExclusionRule("side", ("sell",)),
        ),
    ),
    H021CandidateExclusion(
        name="exclude_usdjpy_decision_hour_05",
        rules=(
            H021ExclusionRule("symbol", ("USDJPY",)),
            H021ExclusionRule("decision_hour_utc", ("05",)),
        ),
    ),
    H021CandidateExclusion(
        name="exclude_xauusd_decision_hour_05",
        rules=(
            H021ExclusionRule("symbol", ("XAUUSD",)),
            H021ExclusionRule("decision_hour_utc", ("05",)),
        ),
    ),
    H021CandidateExclusion(
        name="exclude_usdjpy_buy_stop_distance_20_50x",
        rules=(
            H021ExclusionRule("symbol", ("USDJPY",)),
            H021ExclusionRule("side", ("buy",)),
            H021ExclusionRule("stop_distance_spread_bucket", ("20-50x",)),
        ),
    ),
)


def summarize_record_set(records: Iterable[H021StopPrecursorRecord]) -> H021RecordSetSummary:
    """Summarize a set of enriched H021 records."""
    record_tuple = tuple(records)
    if not record_tuple:
        return H021RecordSetSummary(
            fill_count=0,
            stop_count=0,
            stop_rate=float("nan"),
            winning_fill_count=0,
            losing_fill_count=0,
            total_pnl_usd=0.0,
            mean_pnl_usd=float("nan"),
            median_pnl_usd=float("nan"),
            gross_profit_usd=0.0,
            gross_loss_usd=0.0,
            profit_factor=float("nan"),
        )

    pnl = pd.Series([record.pnl_usd for record in record_tuple], dtype=float)
    winning = pnl[pnl > 0.0]
    losing = pnl[pnl < 0.0]
    stop_count = sum(record.exit_reason == "stop" for record in record_tuple)
    gross_profit = float(winning.sum())
    gross_loss = float(losing.sum())

    return H021RecordSetSummary(
        fill_count=len(record_tuple),
        stop_count=int(stop_count),
        stop_rate=float(stop_count / len(record_tuple)),
        winning_fill_count=int(len(winning)),
        losing_fill_count=int(len(losing)),
        total_pnl_usd=float(pnl.sum()),
        mean_pnl_usd=float(pnl.mean()),
        median_pnl_usd=float(pnl.median()),
        gross_profit_usd=gross_profit,
        gross_loss_usd=gross_loss,
        profit_factor=gross_profit / abs(gross_loss) if gross_loss < 0.0 else float("nan"),
    )


def evaluate_candidate_exclusion(
    records: Iterable[H021StopPrecursorRecord],
    candidate: H021CandidateExclusion,
) -> H021CandidateExclusionResult:
    """Evaluate one exclusion candidate against enriched records."""
    _validate_candidate(candidate)

    record_tuple = tuple(records)
    excluded = tuple(record for record in record_tuple if _record_matches_candidate(record, candidate))
    retained = tuple(record for record in record_tuple if not _record_matches_candidate(record, candidate))

    return H021CandidateExclusionResult(
        candidate=candidate,
        baseline=summarize_record_set(record_tuple),
        excluded=summarize_record_set(excluded),
        retained=summarize_record_set(retained),
    )


def evaluate_candidate_exclusions(
    records: Iterable[H021StopPrecursorRecord],
    candidates: Sequence[H021CandidateExclusion] = DEFAULT_CANDIDATE_EXCLUSIONS,
) -> tuple[H021CandidateExclusionResult, ...]:
    """Evaluate multiple exclusion candidates."""
    record_tuple = tuple(records)
    return tuple(
        evaluate_candidate_exclusion(record_tuple, candidate)
        for candidate in candidates
    )


def format_candidate_exclusion_table(
    results: Sequence[H021CandidateExclusionResult],
    *,
    title: str,
) -> str:
    """Format candidate exclusion results as a compact console table."""
    lines = [title, "-" * len(title)]

    if not results:
        lines.append("(no candidates)")
        return "\n".join(lines)

    header = (
        "candidate | excluded_fills | excluded_stops | excluded_pnl_usd | "
        "retained_fills | retained_stops | retained_stop_rate | retained_pnl_usd | "
        "pnl_improvement_usd | retained_profit_factor"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for result in sorted(
        results,
        key=lambda item: item.retained_pnl_improvement_usd,
        reverse=True,
    ):
        lines.append(
            " | ".join(
                [
                    result.candidate.name,
                    str(result.excluded.fill_count),
                    str(result.excluded.stop_count),
                    f"{result.excluded.total_pnl_usd:.2f}",
                    str(result.retained.fill_count),
                    str(result.retained.stop_count),
                    _format_percent(result.retained.stop_rate),
                    f"{result.retained.total_pnl_usd:.2f}",
                    f"{result.retained_pnl_improvement_usd:.2f}",
                    _format_float(result.retained.profit_factor),
                ]
            )
        )

    return "\n".join(lines)


def main() -> None:
    print("H021 candidate exclusion diagnostic from H020 strict event fills")
    print("=" * 72)
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

    baseline = summarize_record_set(records)
    print(f"Fill rows enriched: {len(records)}")
    print(
        "Baseline: "
        f"fills={baseline.fill_count}, "
        f"stops={baseline.stop_count}, "
        f"stop_rate={_format_percent(baseline.stop_rate)}, "
        f"total_pnl_usd={baseline.total_pnl_usd:.2f}, "
        f"profit_factor={_format_float(baseline.profit_factor)}"
    )
    print()

    results = evaluate_candidate_exclusions(records)
    print(format_candidate_exclusion_table(results, title="Candidate exclusions"))
    print()

    print("Interpretation reminder:")
    print("- A better retained P&L is not a validated strategy.")
    print("- Candidates are decision-time exclusions only if their fields were known before entry.")
    print("- Any promising candidate still needs separate out-of-sample-style validation work.")
    print("No live trading is approved. Phase 4 is not approved.")


def _record_matches_candidate(
    record: H021StopPrecursorRecord,
    candidate: H021CandidateExclusion,
) -> bool:
    return all(
        str(getattr(record, rule.field)) in rule.values
        for rule in candidate.rules
    )


def _validate_candidate(candidate: H021CandidateExclusion) -> None:
    if not candidate.name:
        raise ValueError("candidate name must not be empty")
    if not candidate.rules:
        raise ValueError("candidate rules must not be empty")

    for rule in candidate.rules:
        if not rule.field:
            raise ValueError("candidate rule field must not be empty")
        if not rule.values:
            raise ValueError("candidate rule values must not be empty")


def _format_float(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.6f}"


def _format_percent(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.4%}"


if __name__ == "__main__":
    main()
