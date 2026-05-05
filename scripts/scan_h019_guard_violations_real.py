"""Scan real broker-native data for H019 guard violations.

Diagnostic-only:
- does not tune H019,
- does not execute fills,
- does not skip or clip trades in validation,
- does not promote H019 or H020,
- does not approve live trading.

Purpose:
- measure the H019/H020 guard-failure distribution before H020 sizing design.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.backtest.h018_guard_scan import (
    H018GuardScanResult,
    scan_h018_guard_violations,
)
from quantcore.data.bridge_windows import (
    CommonCompleteBridgeWindowAssessment,
    assess_common_complete_h4_m1_windows,
)
from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h019 import run_h019


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data" / "raw"

USDJPY_H4_PATH = DATA_ROOT / "USDJPY" / "H4.csv"
XAUUSD_H4_PATH = DATA_ROOT / "XAUUSD" / "H4.csv"
USDJPY_M1_PATH = DATA_ROOT / "USDJPY" / "M1.csv"
XAUUSD_M1_PATH = DATA_ROOT / "XAUUSD" / "M1.csv"

EXPECTED_ACCEPTED_COUNT = 5476
EXPECTED_FIRST_ACCEPTED_TIMESTAMP = pd.Timestamp("2021-07-02 13:00:00", tz="UTC")
EXPECTED_LAST_ACCEPTED_TIMESTAMP = pd.Timestamp("2026-04-30 01:00:00", tz="UTC")
EXPECTED_M1_BARS_PER_H4 = 240
EXPECTED_H4_DELTA = pd.Timedelta(hours=4)


@dataclass(frozen=True)
class LoadedBrokerNativeExports:
    usdjpy_h4: MT5LoadResult
    xauusd_h4: MT5LoadResult
    usdjpy_m1: MT5LoadResult
    xauusd_m1: MT5LoadResult


@dataclass(frozen=True)
class H019GuardDiagnosticRun:
    bridge_window_assessment: CommonCompleteBridgeWindowAssessment
    scan: H018GuardScanResult


def _load_broker_native_exports() -> LoadedBrokerNativeExports:
    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="broker-native MT5 exports",
    )

    return LoadedBrokerNativeExports(
        usdjpy_h4=load_mt5_csv(USDJPY_H4_PATH),
        xauusd_h4=load_mt5_csv(XAUUSD_H4_PATH),
        usdjpy_m1=load_mt5_csv(USDJPY_M1_PATH),
        xauusd_m1=load_mt5_csv(XAUUSD_M1_PATH),
    )


def _assess_bridge_windows(
    loaded: LoadedBrokerNativeExports,
) -> CommonCompleteBridgeWindowAssessment:
    return assess_common_complete_h4_m1_windows(
        usdjpy_h4=loaded.usdjpy_h4.bars,
        xauusd_h4=loaded.xauusd_h4.bars,
        usdjpy_m1=loaded.usdjpy_m1.bars,
        xauusd_m1=loaded.xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )


def _assert_expected_bridge_window_assessment(
    assessment: CommonCompleteBridgeWindowAssessment,
) -> None:
    problems: list[str] = []

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        problems.append(
            "accepted_count mismatch: "
            f"expected {EXPECTED_ACCEPTED_COUNT}, got {assessment.accepted_count}"
        )

    if assessment.first_accepted_timestamp != EXPECTED_FIRST_ACCEPTED_TIMESTAMP:
        problems.append(
            "first_accepted_timestamp mismatch: "
            f"expected {EXPECTED_FIRST_ACCEPTED_TIMESTAMP}, "
            f"got {assessment.first_accepted_timestamp}"
        )

    if assessment.last_accepted_timestamp != EXPECTED_LAST_ACCEPTED_TIMESTAMP:
        problems.append(
            "last_accepted_timestamp mismatch: "
            f"expected {EXPECTED_LAST_ACCEPTED_TIMESTAMP}, "
            f"got {assessment.last_accepted_timestamp}"
        )

    if assessment.common_complete_count != assessment.accepted_count:
        problems.append(
            "common_complete_count does not match accepted_count: "
            f"common_complete_count={assessment.common_complete_count}, "
            f"accepted_count={assessment.accepted_count}"
        )

    if problems:
        raise RuntimeError(
            "Strict bridge-window assessment did not match the accepted contract:\n"
            + "\n".join(f"- {problem}" for problem in problems)
        )


def _print_loader_summary(label: str, result: MT5LoadResult) -> None:
    print(
        f"{label}: "
        f"n_input_rows={result.n_input_rows}, "
        f"n_bars={result.n_bars}, "
        f"earliest_utc={result.earliest_utc}, "
        f"latest_utc={result.latest_utc}, "
        f"broker_tz={result.broker_tz}"
    )


def _summary(values: Iterable[float]) -> dict[str, float] | None:
    series = pd.Series(list(values), dtype="float64").dropna()
    if series.empty:
        return None

    return {
        "count": float(series.count()),
        "min": float(series.min()),
        "median": float(series.median()),
        "p95": float(series.quantile(0.95)),
        "max": float(series.max()),
    }


def _format_summary(summary: dict[str, float] | None) -> str:
    if summary is None:
        return "{}"

    return (
        "{"
        f"'count': {int(summary['count'])}, "
        f"'min': {summary['min']:.6f}, "
        f"'median': {summary['median']:.6f}, "
        f"'p95': {summary['p95']:.6f}, "
        f"'max': {summary['max']:.6f}"
        "}"
    )


def _print_violation_severity(scan: H018GuardScanResult) -> None:
    per_trade_leverage = [
        violation.gross_leverage
        for violation in scan.violations
        if violation.guard_name == "maximum_per_trade_usd_gross_leverage"
        and violation.gross_leverage is not None
    ]
    portfolio_leverage = [
        violation.portfolio_gross_leverage
        for violation in scan.violations
        if violation.guard_name == "maximum_portfolio_usd_gross_leverage"
        and violation.portfolio_gross_leverage is not None
    ]
    stop_distance_ratio = [
        violation.raw_stop_distance / violation.minimum_stop_distance
        for violation in scan.violations
        if violation.guard_name == "minimum_stop_distance"
        and violation.raw_stop_distance is not None
        and violation.minimum_stop_distance not in (None, 0.0)
    ]

    print("Violation severity")
    print("-" * 40)
    print(
        "per_trade_gross_leverage="
        f"{_format_summary(_summary(per_trade_leverage))}"
    )
    print(
        "portfolio_gross_leverage="
        f"{_format_summary(_summary(portfolio_leverage))}"
    )
    print(
        "minimum_stop_distance_ratio="
        f"{_format_summary(_summary(stop_distance_ratio))}"
    )
    print()


def _print_bridge_window_assessment(
    assessment: CommonCompleteBridgeWindowAssessment,
) -> None:
    print("Strict bridge-window preflight")
    print("-" * 40)
    print(f"expected_m1_bars_per_h4={EXPECTED_M1_BARS_PER_H4}")
    print(f"expected_h4_delta={EXPECTED_H4_DELTA}")
    print(f"candidate_common_h4_count={assessment.candidate_common_h4_count}")
    print(f"usdjpy_complete_count={assessment.usdjpy_complete_count}")
    print(f"xauusd_complete_count={assessment.xauusd_complete_count}")
    print(f"common_complete_count={assessment.common_complete_count}")
    print(f"accepted_count={assessment.accepted_count}")
    print(f"first_accepted_timestamp={assessment.first_accepted_timestamp}")
    print(f"last_accepted_timestamp={assessment.last_accepted_timestamp}")
    print(f"usdjpy_only_complete_count={assessment.usdjpy_only_complete_count}")
    print(f"xauusd_only_complete_count={assessment.xauusd_only_complete_count}")
    print(f"rejected_count={assessment.rejected_count}")


def build_h019_guard_diagnostic(
    loaded: LoadedBrokerNativeExports,
) -> H019GuardDiagnosticRun:
    assessment = _assess_bridge_windows(loaded)
    _assert_expected_bridge_window_assessment(assessment)

    h019_result = run_h019(
        usdjpy_ohlcv=loaded.usdjpy_h4.bars,
        xauusd_ohlcv=loaded.xauusd_h4.bars,
    )

    scan = scan_h018_guard_violations(
        h017_result=h019_result,
        h4_by_symbol={
            "USDJPY": loaded.usdjpy_h4.bars,
            "XAUUSD": loaded.xauusd_h4.bars,
        },
        accepted_entry_times=assessment.accepted_timestamps,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    return H019GuardDiagnosticRun(
        bridge_window_assessment=assessment,
        scan=scan,
    )


def main() -> None:
    print("H019/H020 guard violation diagnostic scan")
    print("=" * 60)
    print(f"Broker timezone: {DEFAULT_BROKER_TZ}")
    print("Symbols: USDJPY, XAUUSD")
    print("Source: Exness demo MT5 broker-native H4/M1 exports")
    print("Mode: diagnostic-only; not validation promotion")
    print()

    loaded = _load_broker_native_exports()

    print("Raw MT5 exports")
    print("-" * 40)
    _print_loader_summary("USDJPY H4", loaded.usdjpy_h4)
    _print_loader_summary("XAUUSD H4", loaded.xauusd_h4)
    _print_loader_summary("USDJPY M1", loaded.usdjpy_m1)
    _print_loader_summary("XAUUSD M1", loaded.xauusd_m1)
    print()

    diagnostic = build_h019_guard_diagnostic(loaded)
    assessment = diagnostic.bridge_window_assessment
    scan = diagnostic.scan

    _print_bridge_window_assessment(assessment)
    print()

    print("H019/H020 guard diagnostic summary")
    print("-" * 40)
    print(f"accepted_entry_count={scan.accepted_entry_count}")
    print(f"executed_entry_count={scan.executed_entry_count}")
    print(f"skipped_entry_count={scan.skipped_entry_count}")
    print(f"event_interval_count={scan.event_interval_count}")
    print(f"trade_intent_count={scan.trade_intent_count}")
    print(f"candidate_count={scan.candidate_count}")
    print(f"skipped_intent_count={scan.skipped_intent_count}")
    print(f"violation_count={scan.violation_count}")
    print(f"violation_counts_by_guard={scan.violation_counts_by_guard}")
    print(f"violation_counts_by_symbol={scan.violation_counts_by_symbol}")
    print(f"violation_counts_by_side={scan.violation_counts_by_side}")
    print()

    _print_violation_severity(scan)

    print("First violations")
    print("-" * 40)
    for violation in scan.violations[:20]:
        print(
            f"guard={violation.guard_name}, "
            f"symbol={violation.symbol}, "
            f"side={violation.side}, "
            f"decision_time={violation.decision_time}, "
            f"entry_time={violation.entry_time}, "
            f"entry_raw_price={violation.entry_raw_price}, "
            f"stop_price={violation.stop_price}, "
            f"raw_stop_distance={violation.raw_stop_distance}, "
            f"gross_leverage={violation.gross_leverage}, "
            f"portfolio_gross_leverage={violation.portfolio_gross_leverage}"
        )

    print()
    print("Interpretation guardrails")
    print("-" * 40)
    print("STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True")
    print("H019 VALIDATED: False")
    print("H019 PROMOTABLE: False")
    print("H020 IMPLEMENTED: False")
    print("H020 VALIDATED: False")
    print("LIVE TRADING APPROVED: False")
    print("- This scanner is diagnostic-only.")
    print("- It does not execute fills or update equity through time.")
    print("- Leverage counts use constant starting equity and are diagnostic.")
    print("- It does not tune H019.")
    print("- It does not weaken H018 guards.")
    print("- It does not use HistData.")
    print("- It does not write derived datasets.")


if __name__ == "__main__":
    main()
