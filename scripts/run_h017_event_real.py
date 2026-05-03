from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.backtest.h017_event import H017EventBacktestResult, backtest_h017_event_driven
from quantcore.data.leakage import LeakageScan, detect_d1_leakage, trim_to_common_start
from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.strategy.h017_claim import H017Claim, build_h017_claim


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data" / "raw"

USDJPY_H4_PATH = DATA_ROOT / "USDJPY" / "H4.csv"
XAUUSD_H4_PATH = DATA_ROOT / "XAUUSD" / "H4.csv"
USDJPY_M1_PATH = DATA_ROOT / "USDJPY" / "M1.csv"
XAUUSD_M1_PATH = DATA_ROOT / "XAUUSD" / "M1.csv"

PERIODS_PER_YEAR_H4 = 1512
DESIRED_M1_START_UTC = pd.Timestamp("2021-07-02 00:00:00", tz="UTC")
MIN_RESEARCH_H4_BARS = PERIODS_PER_YEAR_H4


@dataclass(frozen=True)
class LoadedMarketData:
    """Keep raw loader metadata beside bars so smoke output can diagnose data coverage."""

    usdjpy_h4: MT5LoadResult
    xauusd_h4: MT5LoadResult
    usdjpy_m1: MT5LoadResult
    xauusd_m1: MT5LoadResult


@dataclass(frozen=True)
class CleanMarketData:
    """Separate cleaned bars from raw bars because leakage trimming is a research assumption."""

    usdjpy_h4: pd.DataFrame
    xauusd_h4: pd.DataFrame
    usdjpy_m1: pd.DataFrame
    xauusd_m1: pd.DataFrame
    usdjpy_scan: LeakageScan
    xauusd_scan: LeakageScan
    clean_start_utc: pd.Timestamp
    clean_end_utc: pd.Timestamp


@dataclass(frozen=True)
class CoverageAssessment:
    """Make data sufficiency explicit so a short smoke run is never mistaken for validation."""

    desired_m1_start_utc: pd.Timestamp
    actual_common_start_utc: pd.Timestamp
    actual_common_end_utc: pd.Timestamp
    n_common_h4_bars: int
    minimum_research_h4_bars: int
    meets_desired_m1_start: bool
    has_minimum_h4_bars: bool
    research_sufficient: bool
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class EventSmokeResult:
    """Bundle event backtest, claim, and coverage so the smoke result is auditable."""

    backtest: H017EventBacktestResult
    claim: H017Claim
    annualized_sharpe: float
    coverage: CoverageAssessment


def _require_file(path: Path) -> None:
    """Fail early with a clear path because MT5 exports are local and intentionally gitignored."""

    if not path.exists():
        raise FileNotFoundError(f"Required MT5 export not found: {path}")


def _load_market_data() -> LoadedMarketData:
    """Load all four MT5 exports before trimming so coverage problems are visible."""

    for path in [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH]:
        _require_file(path)

    return LoadedMarketData(
        usdjpy_h4=load_mt5_csv(USDJPY_H4_PATH),
        xauusd_h4=load_mt5_csv(XAUUSD_H4_PATH),
        usdjpy_m1=load_mt5_csv(USDJPY_M1_PATH),
        xauusd_m1=load_mt5_csv(XAUUSD_M1_PATH),
    )


def _as_utc_timestamp(value: object) -> pd.Timestamp:
    """Normalize leakage dates to UTC timestamps before comparing against UTC bar indexes."""

    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        return timestamp.tz_localize("UTC")
    return timestamp.tz_convert("UTC")


def _max_timestamp(values: list[pd.Timestamp]) -> pd.Timestamp:
    """Choose the latest required start so both symbols and both timeframes overlap."""

    if not values:
        raise ValueError("Cannot choose a maximum timestamp from an empty list.")
    return max(values)


def _min_timestamp(values: list[pd.Timestamp]) -> pd.Timestamp:
    """Choose the earliest available end so both symbols and both timeframes overlap."""

    if not values:
        raise ValueError("Cannot choose a minimum timestamp from an empty list.")
    return min(values)


def _trim_to_window(bars: pd.DataFrame, *, start_utc: pd.Timestamp, end_utc: pd.Timestamp) -> pd.DataFrame:
    """Use an explicit UTC window because H4 and M1 must cover the same tradable period."""

    return bars.loc[(bars.index >= start_utc) & (bars.index <= end_utc)].copy()


def _clean_market_data(data: LoadedMarketData) -> CleanMarketData:
    """Apply the known H4 leakage rule, then force H4 and M1 onto a common real-data window."""

    usdjpy_scan = detect_d1_leakage(data.usdjpy_h4.bars, DEFAULT_BROKER_TZ)
    xauusd_scan = detect_d1_leakage(data.xauusd_h4.bars, DEFAULT_BROKER_TZ)

    if usdjpy_scan.first_reliable_date is None:
        raise ValueError("USDJPY H4 leakage scan did not find a reliable start date.")
    if xauusd_scan.first_reliable_date is None:
        raise ValueError("XAUUSD H4 leakage scan did not find a reliable start date.")

    h4_clean_start = _max_timestamp(
        [
            _as_utc_timestamp(usdjpy_scan.first_reliable_date),
            _as_utc_timestamp(xauusd_scan.first_reliable_date),
        ]
    )

    usdjpy_h4_clean, xauusd_h4_clean = trim_to_common_start(
        data.usdjpy_h4.bars,
        data.xauusd_h4.bars,
        h4_clean_start,
    )

    clean_start = _max_timestamp(
        [
            usdjpy_h4_clean.index.min(),
            xauusd_h4_clean.index.min(),
            data.usdjpy_m1.bars.index.min(),
            data.xauusd_m1.bars.index.min(),
        ]
    )
    clean_end = _min_timestamp(
        [
            usdjpy_h4_clean.index.max(),
            xauusd_h4_clean.index.max(),
            data.usdjpy_m1.bars.index.max(),
            data.xauusd_m1.bars.index.max(),
        ]
    )

    if clean_start >= clean_end:
        raise ValueError(
            "H4 and M1 exports do not overlap after leakage trimming. "
            f"clean_start={clean_start}, clean_end={clean_end}"
        )

    usdjpy_h4_final = _trim_to_window(usdjpy_h4_clean, start_utc=clean_start, end_utc=clean_end)
    xauusd_h4_final = _trim_to_window(xauusd_h4_clean, start_utc=clean_start, end_utc=clean_end)
    usdjpy_m1_final = _trim_to_window(data.usdjpy_m1.bars, start_utc=clean_start, end_utc=clean_end)
    xauusd_m1_final = _trim_to_window(data.xauusd_m1.bars, start_utc=clean_start, end_utc=clean_end)

    if usdjpy_h4_final.empty:
        raise ValueError("USDJPY H4 is empty after common-window trimming.")
    if xauusd_h4_final.empty:
        raise ValueError("XAUUSD H4 is empty after common-window trimming.")
    if usdjpy_m1_final.empty:
        raise ValueError("USDJPY M1 is empty after common-window trimming.")
    if xauusd_m1_final.empty:
        raise ValueError("XAUUSD M1 is empty after common-window trimming.")

    return CleanMarketData(
        usdjpy_h4=usdjpy_h4_final,
        xauusd_h4=xauusd_h4_final,
        usdjpy_m1=usdjpy_m1_final,
        xauusd_m1=xauusd_m1_final,
        usdjpy_scan=usdjpy_scan,
        xauusd_scan=xauusd_scan,
        clean_start_utc=clean_start,
        clean_end_utc=clean_end,
    )


def _annualized_sharpe(returns: pd.Series, *, periods_per_year: int) -> float:
    """Report a familiar scale while keeping validation decisions inside build_h017_claim."""

    clean_returns = returns.dropna()
    if clean_returns.empty:
        return float("nan")

    std = float(clean_returns.std(ddof=1))
    if std < 1e-12:
        return float("nan")

    return float(clean_returns.mean() / std * (periods_per_year**0.5))


def _assess_research_coverage(clean: CleanMarketData) -> CoverageAssessment:
    """Separate an operational smoke pass from enough history for research validation."""

    n_common_h4_bars = min(len(clean.usdjpy_h4), len(clean.xauusd_h4))
    meets_desired_m1_start = clean.clean_start_utc <= DESIRED_M1_START_UTC
    has_minimum_h4_bars = n_common_h4_bars >= MIN_RESEARCH_H4_BARS

    reasons: list[str] = []
    if not meets_desired_m1_start:
        reasons.append(
            "M1 common start is later than the desired clean H4 start. "
            f"desired={DESIRED_M1_START_UTC}, actual={clean.clean_start_utc}"
        )
    if not has_minimum_h4_bars:
        reasons.append(
            "Common H4 sample is shorter than one approximate H4 trading year. "
            f"minimum={MIN_RESEARCH_H4_BARS}, actual={n_common_h4_bars}"
        )

    research_sufficient = meets_desired_m1_start and has_minimum_h4_bars

    if research_sufficient:
        reasons.append("M1 coverage is sufficient for a first research-grade event validation pass.")

    return CoverageAssessment(
        desired_m1_start_utc=DESIRED_M1_START_UTC,
        actual_common_start_utc=clean.clean_start_utc,
        actual_common_end_utc=clean.clean_end_utc,
        n_common_h4_bars=n_common_h4_bars,
        minimum_research_h4_bars=MIN_RESEARCH_H4_BARS,
        meets_desired_m1_start=meets_desired_m1_start,
        has_minimum_h4_bars=has_minimum_h4_bars,
        research_sufficient=research_sufficient,
        reasons=tuple(reasons),
    )


def run_smoke() -> EventSmokeResult:
    """Run the real-data event backtest end-to-end as an operational gate, not a promotion claim."""

    loaded = _load_market_data()
    clean = _clean_market_data(loaded)

    result = backtest_h017_event_driven(
        usdjpy_h4=clean.usdjpy_h4,
        xauusd_h4=clean.xauusd_h4,
        usdjpy_m1=clean.usdjpy_m1,
        xauusd_m1=clean.xauusd_m1,
    )

    claim = build_h017_claim(
        result.portfolio.returns,
        periods_per_year=PERIODS_PER_YEAR_H4,
    )

    return EventSmokeResult(
        backtest=result,
        claim=claim,
        annualized_sharpe=_annualized_sharpe(
            result.portfolio.returns,
            periods_per_year=PERIODS_PER_YEAR_H4,
        ),
        coverage=_assess_research_coverage(clean),
    )


def _print_loader_summary(name: str, loaded: MT5LoadResult) -> None:
    """Print raw coverage because most real-data failures are export-range problems."""

    print(
        f"{name}: rows={loaded.n_input_rows} bars={loaded.n_bars} "
        f"earliest={loaded.earliest_utc} latest={loaded.latest_utc}"
    )


def _count_or_len(value: object) -> int:
    """Support leakage APIs that expose either an integer count or a collection."""

    if isinstance(value, int):
        return value

    try:
        return len(value)  # type: ignore[arg-type]
    except TypeError as exc:
        raise TypeError(f"Expected an int or sized collection, got {type(value)!r}") from exc


def _print_leakage_summary(name: str, scan: LeakageScan) -> None:
    """Print leakage findings so the H4 clean-start assumption is visible in every run."""

    print(
        f"{name}: first_reliable_date={scan.first_reliable_date} "
        f"leaked_dates={_count_or_len(scan.leaked_dates)} "
        f"weekend_dates={_count_or_len(scan.weekend_dates)} "
        f"total_dates={scan.total_dates}"
    )


def _print_coverage_summary(coverage: CoverageAssessment) -> None:
    """Print a blunt research-sufficiency warning before anyone interprets performance."""

    print("Coverage guard")
    print("-" * 40)
    print(f"desired_m1_start_utc={coverage.desired_m1_start_utc}")
    print(f"actual_common_start_utc={coverage.actual_common_start_utc}")
    print(f"actual_common_end_utc={coverage.actual_common_end_utc}")
    print(f"n_common_h4_bars={coverage.n_common_h4_bars}")
    print(f"minimum_research_h4_bars={coverage.minimum_research_h4_bars}")
    print(f"meets_desired_m1_start={coverage.meets_desired_m1_start}")
    print(f"has_minimum_h4_bars={coverage.has_minimum_h4_bars}")
    print(f"research_sufficient={coverage.research_sufficient}")

    for reason in coverage.reasons:
        print(f"- {reason}")


def main() -> None:
    """Console entry point for manual Windows/PowerShell operation."""

    print("H017 event-driven real-data smoke")
    print("=" * 40)
    print(f"Broker timezone: {DEFAULT_BROKER_TZ}")
    print()

    loaded = _load_market_data()

    print("Raw MT5 exports")
    print("-" * 40)
    _print_loader_summary("USDJPY H4", loaded.usdjpy_h4)
    _print_loader_summary("XAUUSD H4", loaded.xauusd_h4)
    _print_loader_summary("USDJPY M1", loaded.usdjpy_m1)
    _print_loader_summary("XAUUSD M1", loaded.xauusd_m1)
    print()

    clean = _clean_market_data(loaded)

    print("H4 leakage scan")
    print("-" * 40)
    _print_leakage_summary("USDJPY H4", clean.usdjpy_scan)
    _print_leakage_summary("XAUUSD H4", clean.xauusd_scan)
    print()

    print("Clean common window")
    print("-" * 40)
    print(f"start_utc={clean.clean_start_utc}")
    print(f"end_utc={clean.clean_end_utc}")
    print(f"USDJPY H4 bars={len(clean.usdjpy_h4)}")
    print(f"XAUUSD H4 bars={len(clean.xauusd_h4)}")
    print(f"USDJPY M1 bars={len(clean.usdjpy_m1)}")
    print(f"XAUUSD M1 bars={len(clean.xauusd_m1)}")
    print()

    coverage = _assess_research_coverage(clean)
    _print_coverage_summary(coverage)
    print()

    result = backtest_h017_event_driven(
        usdjpy_h4=clean.usdjpy_h4,
        xauusd_h4=clean.xauusd_h4,
        usdjpy_m1=clean.usdjpy_m1,
        xauusd_m1=clean.xauusd_m1,
    )
    claim = build_h017_claim(
        result.portfolio.returns,
        periods_per_year=PERIODS_PER_YEAR_H4,
    )
    annualized_sharpe = _annualized_sharpe(
        result.portfolio.returns,
        periods_per_year=PERIODS_PER_YEAR_H4,
    )

    print("Event-driven backtest")
    print("-" * 40)
    print(f"symbols={result.symbols}")
    print(f"n_bars={result.n_bars}")
    print(f"fills={len(result.fills)}")
    print(f"starting_equity_usd={result.portfolio.starting_equity_usd:.2f}")
    print(f"ending_equity_usd={result.portfolio.ending_equity_usd:.2f}")
    print(f"total_return_pct={(result.portfolio.ending_equity_usd / result.portfolio.starting_equity_usd - 1.0) * 100.0:.2f}")
    print(f"max_drawdown_pct={result.portfolio.max_drawdown * 100.0:.2f}")
    print(f"annualized_sharpe={annualized_sharpe:.4f}")
    print()

    print("H017 claim on realistic event-driven returns")
    print("-" * 40)
    print(claim.summary)
    print()

    print("Operational verdict")
    print("-" * 40)
    print("PIPELINE SMOKE PASSED: True")
    print(f"RESEARCH VALIDATION SUFFICIENT: {coverage.research_sufficient}")
    if not coverage.research_sufficient:
        print(
            "Interpretation: the event pipeline works, but the available M1 history is too short "
            "to treat this as a research-grade validation result."
        )


if __name__ == "__main__":
    main()
