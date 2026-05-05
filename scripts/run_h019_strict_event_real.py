from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.backtest.h017_event import H017EventInsolvencyError
from quantcore.backtest.h017_strict_event import StrictH017EventBacktestResult
from quantcore.backtest.h019_strict_event import backtest_h019_strict_event
from quantcore.data.bridge_windows import (
    CommonCompleteBridgeWindowAssessment,
    assess_common_complete_h4_m1_windows,
)
from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017_claim import H017Claim, build_h017_claim


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data" / "raw"

USDJPY_H4_PATH = DATA_ROOT / "USDJPY" / "H4.csv"
XAUUSD_H4_PATH = DATA_ROOT / "XAUUSD" / "H4.csv"
USDJPY_M1_PATH = DATA_ROOT / "USDJPY" / "M1.csv"
XAUUSD_M1_PATH = DATA_ROOT / "XAUUSD" / "M1.csv"

PERIODS_PER_YEAR_H4 = 1512

EXPECTED_ACCEPTED_COUNT = 5476
EXPECTED_FIRST_ACCEPTED_TIMESTAMP = pd.Timestamp("2021-07-02 13:00:00", tz="UTC")
EXPECTED_LAST_ACCEPTED_TIMESTAMP = pd.Timestamp("2026-04-30 01:00:00", tz="UTC")
EXPECTED_M1_BARS_PER_H4 = 240
EXPECTED_H4_DELTA = pd.Timedelta(hours=4)


@dataclass(frozen=True)
class LoadedMarketData:
    """Keep broker-native loader metadata beside bars for audited console output."""

    usdjpy_h4: MT5LoadResult
    xauusd_h4: MT5LoadResult
    usdjpy_m1: MT5LoadResult
    xauusd_m1: MT5LoadResult


@dataclass(frozen=True)
class StrictExpandedH019ValidationResult:
    """Bundle strict expanded H019 validation artifacts for manual inspection."""

    backtest: StrictH017EventBacktestResult
    claim: H017Claim
    annualized_sharpe: float
    bridge_window_assessment: CommonCompleteBridgeWindowAssessment


def _load_market_data() -> LoadedMarketData:
    """Load all four broker-native MT5 exports without writing derived data."""

    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="MT5 export",
    )

    return LoadedMarketData(
        usdjpy_h4=load_mt5_csv(USDJPY_H4_PATH),
        xauusd_h4=load_mt5_csv(XAUUSD_H4_PATH),
        usdjpy_m1=load_mt5_csv(USDJPY_M1_PATH),
        xauusd_m1=load_mt5_csv(XAUUSD_M1_PATH),
    )


def _assess_bridge_windows(
    loaded: LoadedMarketData,
) -> CommonCompleteBridgeWindowAssessment:
    """Run the strict common complete H4/M1 bridge-window preflight."""

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
    """Fail closed if the accepted strict bridge-window set changes unexpectedly."""

    errors: list[str] = []

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        errors.append(
            "accepted_count mismatch: "
            f"expected {EXPECTED_ACCEPTED_COUNT}, got {assessment.accepted_count}"
        )

    if assessment.first_accepted_timestamp != EXPECTED_FIRST_ACCEPTED_TIMESTAMP:
        errors.append(
            "first_accepted_timestamp mismatch: "
            f"expected {EXPECTED_FIRST_ACCEPTED_TIMESTAMP}, "
            f"got {assessment.first_accepted_timestamp}"
        )

    if assessment.last_accepted_timestamp != EXPECTED_LAST_ACCEPTED_TIMESTAMP:
        errors.append(
            "last_accepted_timestamp mismatch: "
            f"expected {EXPECTED_LAST_ACCEPTED_TIMESTAMP}, "
            f"got {assessment.last_accepted_timestamp}"
        )

    if assessment.common_complete_count != assessment.accepted_count:
        errors.append(
            "common_complete_count does not match accepted_count: "
            f"common_complete_count={assessment.common_complete_count}, "
            f"accepted_count={assessment.accepted_count}"
        )

    if errors:
        message = "\n".join(f"- {error}" for error in errors)
        raise ValueError(
            "Strict bridge-window assessment did not match the accepted "
            f"expanded broker-native validation contract:\n{message}"
        )


def _annualized_sharpe(returns: pd.Series, *, periods_per_year: int) -> float:
    """Report a familiar Sharpe scale while leaving promotion logic to claim checks."""

    clean_returns = returns.dropna()
    if clean_returns.empty:
        return 0.0

    std = clean_returns.std(ddof=1)
    if std == 0.0 or pd.isna(std):
        return 0.0

    return float(clean_returns.mean() / std * (periods_per_year**0.5))


def run_validation() -> StrictExpandedH019ValidationResult:
    """Run strict expanded broker-native H019 validation.

    This function intentionally:
    - uses only broker-native MT5 USDJPY and XAUUSD H4/M1 exports,
    - runs the strict complete-window preflight,
    - verifies the exact accepted bridge-window contract,
    - routes through H019, not H017,
    - preserves all existing H018 guards in the strict event bridge,
    - writes no derived datasets,
    - does not tune H019,
    - does not change the cost model,
    - does not approve live trading.
    """

    loaded = _load_market_data()
    assessment = _assess_bridge_windows(loaded)
    _assert_expected_bridge_window_assessment(assessment)

    strict_result = backtest_h019_strict_event(
        usdjpy_h4=loaded.usdjpy_h4.bars,
        xauusd_h4=loaded.xauusd_h4.bars,
        usdjpy_m1=loaded.usdjpy_m1.bars,
        xauusd_m1=loaded.xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    claim = build_h017_claim(
        strict_result.backtest.portfolio.returns,
        periods_per_year=PERIODS_PER_YEAR_H4,
    )

    return StrictExpandedH019ValidationResult(
        backtest=strict_result,
        claim=claim,
        annualized_sharpe=_annualized_sharpe(
            strict_result.backtest.portfolio.returns,
            periods_per_year=PERIODS_PER_YEAR_H4,
        ),
        bridge_window_assessment=assessment,
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
    print("rejection_counts:")
    for item in assessment.rejection_counts:
        print(f"  {item.reason}: {item.count}")


def _print_strict_execution_summary(result: StrictH017EventBacktestResult) -> None:
    print("Strict H019 event wrapper execution")
    print("-" * 40)
    print(f"accepted_entry_count={result.accepted_entry_count}")
    print(f"executed_entry_count={result.executed_entry_count}")
    print(f"skipped_entry_count={result.skipped_entry_count}")
    print(f"expected_h4_delta={result.expected_h4_delta}")

    first_executed = (
        result.executed_entry_times[0]
        if result.executed_entry_count > 0
        else None
    )
    last_executed = (
        result.executed_entry_times[-1]
        if result.executed_entry_count > 0
        else None
    )
    first_skipped = (
        result.skipped_entry_times[0]
        if result.skipped_entry_count > 0
        else None
    )
    last_skipped = (
        result.skipped_entry_times[-1]
        if result.skipped_entry_count > 0
        else None
    )

    print(f"first_executed_entry_time={first_executed}")
    print(f"last_executed_entry_time={last_executed}")
    print(f"first_skipped_entry_time={first_skipped}")
    print(f"last_skipped_entry_time={last_skipped}")


def _print_backtest_summary(
    result: StrictH017EventBacktestResult,
    *,
    annualized_sharpe: float,
) -> None:
    backtest = result.backtest
    portfolio = backtest.portfolio

    print("Strict H019 event-driven backtest")
    print("-" * 40)
    print(f"symbols={backtest.symbols}")
    print(f"n_bars={backtest.n_bars}")
    print(f"fills={len(backtest.fills)}")
    print(f"starting_equity_usd={portfolio.starting_equity_usd:.2f}")
    print(f"ending_equity_usd={portfolio.ending_equity_usd:.2f}")
    print(
        "total_return_pct="
        f"{(portfolio.ending_equity_usd / portfolio.starting_equity_usd - 1.0) * 100.0:.2f}"
    )
    print(f"max_drawdown_pct={portfolio.max_drawdown * 100.0:.2f}")
    print(f"annualized_sharpe={annualized_sharpe:.4f}")


def _print_insolvency_failure(error: H017EventInsolvencyError) -> None:
    """Print a fail-closed validation result for account ruin."""

    print("Strict H019 event-driven backtest")
    print("-" * 40)
    print("completed=False")
    print("failure_reason=insolvency")
    print(f"decision_time={error.decision_time}")
    print(f"entry_time={error.entry_time}")
    print(f"forced_exit_time={error.forced_exit_time}")
    print(f"interval_start_equity_usd={error.interval_start_equity_usd:.2f}")
    print(f"interval_pnl_usd={error.interval_pnl_usd:.2f}")
    print(f"ending_equity_usd={error.ending_equity_usd:.2f}")
    print(
        "interval_return_pct="
        f"{error.interval_pnl_usd / error.interval_start_equity_usd * 100.0:.2f}"
    )
    print(f"interval_fills={len(error.interval_fills)}")

    for fill in error.interval_fills:
        print(
            "  fill: "
            f"symbol={fill.symbol}, "
            f"side={fill.side}, "
            f"entry_time={fill.entry_time_utc}, "
            f"exit_time={fill.exit_time_utc}, "
            f"entry_price={fill.entry_price:.9f}, "
            f"exit_price={fill.exit_price:.9f}, "
            f"lots={fill.lots:.2f}, "
            f"pnl_quote={fill.pnl_quote:.2f}, "
            f"commission={fill.commission:.2f}, "
            f"slippage={fill.slippage:.9f}, "
            f"exit_reason={fill.exit_reason}"
        )

    print()
    print("Research verdict")
    print("-" * 40)
    print("STRICT BRIDGE-WINDOW PREFLIGHT PASSED: True")
    print("H019 STRICT EVENT BACKTEST COMPLETED: False")
    print("H019 VALIDATION FAILED BY INSOLVENCY: True")
    print("H019 PROMOTABLE BY CLAIM: False")
    print("EXPANDED VALIDATION IS RESEARCH EVIDENCE ONLY: True")
    print("LIVE TRADING APPROVED: False")


def main() -> None:
    """Console entry point for manual Windows/PowerShell operation."""

    print("H019 strict expanded broker-native event-driven validation")
    print("=" * 60)
    print(f"Broker timezone: {DEFAULT_BROKER_TZ}")
    print("Symbols: USDJPY, XAUUSD")
    print("Source: Exness demo MT5 broker-native H4/M1 exports")
    print()

    loaded = _load_market_data()

    print("Raw MT5 exports")
    print("-" * 40)
    _print_loader_summary("USDJPY H4", loaded.usdjpy_h4)
    _print_loader_summary("XAUUSD H4", loaded.xauusd_h4)
    _print_loader_summary("USDJPY M1", loaded.usdjpy_m1)
    _print_loader_summary("XAUUSD M1", loaded.xauusd_m1)
    print()

    assessment = _assess_bridge_windows(loaded)
    _assert_expected_bridge_window_assessment(assessment)
    _print_bridge_window_assessment(assessment)
    print()

    try:
        strict_result = backtest_h019_strict_event(
            usdjpy_h4=loaded.usdjpy_h4.bars,
            xauusd_h4=loaded.xauusd_h4.bars,
            usdjpy_m1=loaded.usdjpy_m1.bars,
            xauusd_m1=loaded.xauusd_m1.bars,
            accepted_entry_times=assessment.accepted_timestamps,
            expected_h4_delta=EXPECTED_H4_DELTA,
        )
    except H017EventInsolvencyError as exc:
        _print_insolvency_failure(exc)
        raise SystemExit(1) from None

    claim = build_h017_claim(
        strict_result.backtest.portfolio.returns,
        periods_per_year=PERIODS_PER_YEAR_H4,
    )
    annualized_sharpe = _annualized_sharpe(
        strict_result.backtest.portfolio.returns,
        periods_per_year=PERIODS_PER_YEAR_H4,
    )

    _print_strict_execution_summary(strict_result)
    print()

    _print_backtest_summary(strict_result, annualized_sharpe=annualized_sharpe)
    print()

    print("H019 claim on strict expanded broker-native event-driven returns")
    print("-" * 40)
    print(claim.summary)
    print()

    print("Research verdict")
    print("-" * 40)
    print(f"H019 PROMOTABLE BY CLAIM: {claim.promotable}")
    print("EXPANDED VALIDATION IS RESEARCH EVIDENCE ONLY: True")
    print("LIVE TRADING APPROVED: False")
    print()
    print("Interpretation guardrails:")
    print("- This script routes through H019, not H017.")
    print("- This script does not tune H019.")
    print("- This script does not change the cost model.")
    print("- This script does not use HistData.")
    print("- This script does not write derived datasets.")
    print("- Source acceptance is not strategy promotion.")
    print("- Even a positive result would not approve live trading.")


if __name__ == "__main__":
    main()
