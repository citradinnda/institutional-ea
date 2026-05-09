"""H024 chronological validation diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

This diagnostic keeps H024 fixed:
- hold = 3 H4
- baseline stop ATR multiple = 2.0
- baseline cost model
- no time/session filters
- no 2023 exclusion
- no parameter optimization

It evaluates temporal generalization by running fixed H024 on chronological
out-of-sample test folds defined only by accepted bridge-window order.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd

from quantcore.data.bridge_windows import (
    assess_common_complete_h4_m1_windows_cached,
    build_common_complete_bridge_window_cache_key,
)
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from scripts.diagnose_h024_fixed_lifecycle_real import (
    BRIDGE_WINDOW_CACHE_PATH,
    H024DiagnosticRun,
    format_h024_diagnostic_report,
    run_h024_fixed_lifecycle_diagnostic,
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

DEFAULT_H024_WALK_FORWARD_HOLD_H4_BARS = 3
DEFAULT_H024_WALK_FORWARD_TEST_FRACTIONS: tuple[float, ...] = (0.25, 0.50, 0.75)


@dataclass(frozen=True)
class H024WalkForwardFold:
    label: str
    train_start_utc: pd.Timestamp
    train_end_utc: pd.Timestamp
    test_start_utc: pd.Timestamp
    test_end_utc: pd.Timestamp
    train_count: int
    test_count: int
    test_entry_times: tuple[pd.Timestamp, ...]


@dataclass(frozen=True)
class H024WalkForwardFoldResult:
    fold: H024WalkForwardFold
    run: H024DiagnosticRun


def build_h024_walk_forward_folds(
    accepted_entry_times: Sequence[pd.Timestamp],
    *,
    test_fractions: Sequence[float] = DEFAULT_H024_WALK_FORWARD_TEST_FRACTIONS,
) -> tuple[H024WalkForwardFold, ...]:
    """Build anchored chronological test folds from accepted bridge windows.

    The train segment is descriptive only. H024 parameters are not fit on it.
    """

    accepted = tuple(sorted(pd.Timestamp(ts).tz_convert("UTC") for ts in accepted_entry_times))
    if len(accepted) < 4:
        raise ValueError("accepted_entry_times must contain at least 4 timestamps")
    if not test_fractions:
        raise ValueError("test_fractions must be non-empty")

    folds: list[H024WalkForwardFold] = []
    previous_cut = 0

    for fraction in test_fractions:
        if fraction <= 0.0 or fraction >= 1.0:
            raise ValueError("test_fractions must be between 0 and 1")

        cut = int(len(accepted) * fraction)
        if cut <= 0 or cut >= len(accepted):
            raise ValueError("test fraction produces empty train or test window")
        if cut <= previous_cut:
            raise ValueError("test_fractions must be strictly increasing")
        previous_cut = cut

        test_times = accepted[cut:]
        folds.append(
            H024WalkForwardFold(
                label=f"anchored_train_{fraction:.0%}_test_rest",
                train_start_utc=accepted[0],
                train_end_utc=accepted[cut - 1],
                test_start_utc=test_times[0],
                test_end_utc=test_times[-1],
                train_count=cut,
                test_count=len(test_times),
                test_entry_times=test_times,
            )
        )

    return tuple(folds)


def run_h024_walk_forward_validation(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    test_fractions: Sequence[float] = DEFAULT_H024_WALK_FORWARD_TEST_FRACTIONS,
    starting_equity_usd: float = 10_000.0,
) -> tuple[H024WalkForwardFoldResult, ...]:
    """Run fixed H024 hold=3 over chronological out-of-sample test folds."""

    folds = build_h024_walk_forward_folds(
        accepted_entry_times,
        test_fractions=test_fractions,
    )

    results: list[H024WalkForwardFoldResult] = []
    for fold in folds:
        run = run_h024_fixed_lifecycle_diagnostic(
            usdjpy_h4=usdjpy_h4,
            xauusd_h4=xauusd_h4,
            usdjpy_m1=usdjpy_m1,
            xauusd_m1=xauusd_m1,
            accepted_entry_times=fold.test_entry_times,
            hold_h4_bars_values=(DEFAULT_H024_WALK_FORWARD_HOLD_H4_BARS,),
            starting_equity_usd=starting_equity_usd,
        )[0]
        results.append(H024WalkForwardFoldResult(fold=fold, run=run))

    return tuple(results)


def format_h024_walk_forward_summary(
    results: Sequence[H024WalkForwardFoldResult],
) -> str:
    lines = [
        "H024 hold=3 chronological validation summary",
        "=" * 72,
        "fold | train_count | test_count | test_start_utc | test_end_utc | fills | total_return | max_drawdown | profit_factor | pass_headline",
        "--- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---",
    ]

    for result in results:
        summary = result.run.summary
        pass_headline = (
            summary.total_return > 0.0
            and summary.profit_factor >= 1.15
            and summary.max_drawdown > -0.25
        )
        lines.append(
            " | ".join(
                [
                    result.fold.label,
                    str(result.fold.train_count),
                    str(result.fold.test_count),
                    result.fold.test_start_utc.isoformat(),
                    result.fold.test_end_utc.isoformat(),
                    str(summary.fill_count),
                    f"{summary.total_return:.4%}",
                    f"{summary.max_drawdown:.4%}",
                    f"{summary.profit_factor:.6f}",
                    "yes" if pass_headline else "no",
                ]
            )
        )

    lines.extend(
        [
            "",
            "Verdict reminder: this is chronological validation only.",
            "No demo trading is approved. No live trading is approved. Phase 4 is not approved.",
        ]
    )
    return "\n".join(lines)


def format_h024_walk_forward_report(
    results: Sequence[H024WalkForwardFoldResult],
) -> str:
    sections = [format_h024_walk_forward_summary(results)]

    for result in results:
        sections.extend(
            [
                "",
                f"Detailed fold report: {result.fold.label}",
                format_h024_diagnostic_report((result.run,)),
            ]
        )

    return "\n".join(sections)


def main() -> None:
    print("H024 hold=3 chronological validation diagnostic")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
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

    cache_key = build_common_complete_bridge_window_cache_key(
        source_paths={
            "usdjpy_h4": USDJPY_H4_PATH,
            "xauusd_h4": XAUUSD_H4_PATH,
            "usdjpy_m1": USDJPY_M1_PATH,
            "xauusd_m1": XAUUSD_M1_PATH,
        },
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )
    assessment = assess_common_complete_h4_m1_windows_cached(
        cache_path=BRIDGE_WINDOW_CACHE_PATH,
        cache_key=cache_key,
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(
            "accepted_count mismatch: "
            f"expected={EXPECTED_ACCEPTED_COUNT}, observed={assessment.accepted_count}"
        )

    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print("Running chronological validation folds...")
    print()

    results = run_h024_walk_forward_validation(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
    )

    print(format_h024_walk_forward_report(results))


if __name__ == "__main__":
    main()
