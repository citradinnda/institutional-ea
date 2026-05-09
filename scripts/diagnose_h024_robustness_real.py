"""H024 targeted robustness diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

This script intentionally tests only the pre-identified H024 hold=3 H4 candidate
under modest pre-specified stresses. It is not a broad parameter sweep.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Iterator, Sequence

import pandas as pd

import quantcore.backtest.h017_event as h017_event
from quantcore.backtest.cost_model import SymbolCostSpec, get_default_cost_spec
from scripts.diagnose_h024_fixed_lifecycle_real import (
    H024DiagnosticRun,
    format_h024_diagnostic_report,
    run_h024_fixed_lifecycle_diagnostic,
)


DEFAULT_H024_ROBUSTNESS_HOLD_H4_BARS = 3
DEFAULT_H024_ROBUSTNESS_STOP_ATR_MULTIPLES: tuple[float, ...] = (1.5, 2.0, 2.5)
DEFAULT_H024_ROBUSTNESS_COST_MULTIPLIERS: tuple[float, ...] = (1.0, 1.25, 1.5)


@dataclass(frozen=True)
class H024RobustnessScenario:
    label: str
    stop_atr_multiple: float
    cost_multiplier: float


@dataclass(frozen=True)
class H024RobustnessScenarioResult:
    scenario: H024RobustnessScenario
    run: H024DiagnosticRun


def default_h024_robustness_scenarios() -> tuple[H024RobustnessScenario, ...]:
    """Return the small pre-specified robustness grid.

    This is deliberately narrow:
    - hold is fixed at the observed H024 candidate: 3 H4
    - stop ATR multiple varies only near the seed value
    - costs are stressed upward only
    """

    scenarios = []
    for stop_atr_multiple in DEFAULT_H024_ROBUSTNESS_STOP_ATR_MULTIPLES:
        for cost_multiplier in DEFAULT_H024_ROBUSTNESS_COST_MULTIPLIERS:
            scenarios.append(
                H024RobustnessScenario(
                    label=(
                        f"stop_atr_{stop_atr_multiple:.2f}_"
                        f"cost_{cost_multiplier:.2f}x"
                    ),
                    stop_atr_multiple=stop_atr_multiple,
                    cost_multiplier=cost_multiplier,
                )
            )

    return tuple(scenarios)


def run_h024_robustness_diagnostic(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: Sequence[pd.Timestamp],
    scenarios: Sequence[H024RobustnessScenario] | None = None,
    starting_equity_usd: float = 10_000.0,
) -> tuple[H024RobustnessScenarioResult, ...]:
    """Run targeted H024 hold=3 robustness checks from loaded bars."""

    if scenarios is None:
        resolved_scenarios = default_h024_robustness_scenarios()
    else:
        resolved_scenarios = tuple(scenarios)

    if not resolved_scenarios:
        raise ValueError("scenarios must be non-empty")

    results: list[H024RobustnessScenarioResult] = []

    for scenario in resolved_scenarios:
        _validate_scenario(scenario)
        with _patched_h024_cost_multiplier(scenario.cost_multiplier):
            from quantcore.strategy.h024_runner import H024BridgeConfig

            bridge_config = H024BridgeConfig(
                stop_atr_multiple=scenario.stop_atr_multiple,
                starting_equity_usd=starting_equity_usd,
            )
            runs = run_h024_fixed_lifecycle_diagnostic(
                usdjpy_h4=usdjpy_h4,
                xauusd_h4=xauusd_h4,
                usdjpy_m1=usdjpy_m1,
                xauusd_m1=xauusd_m1,
                accepted_entry_times=accepted_entry_times,
                hold_h4_bars_values=(DEFAULT_H024_ROBUSTNESS_HOLD_H4_BARS,),
                bridge_config=bridge_config,
                starting_equity_usd=starting_equity_usd,
            )

        results.append(
            H024RobustnessScenarioResult(
                scenario=scenario,
                run=runs[0],
            )
        )

    return tuple(results)


def format_h024_robustness_summary(
    results: Sequence[H024RobustnessScenarioResult],
) -> str:
    """Format compact H024 robustness results."""

    lines = [
        "H024 hold=3 targeted robustness diagnostic",
        "=" * 72,
        "scenario | stop_atr | cost_mult | fills | stops | stop_rate | total_return | max_drawdown | profit_factor | pass_headline",
        "--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---",
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
                    result.scenario.label,
                    f"{result.scenario.stop_atr_multiple:.2f}",
                    f"{result.scenario.cost_multiplier:.2f}",
                    str(summary.fill_count),
                    str(summary.stop_count),
                    f"{summary.stop_rate:.4%}",
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
            "Verdict reminder: this is robustness diagnostics only.",
            "No demo trading is approved. No live trading is approved. Phase 4 is not approved.",
        ]
    )

    return "\n".join(lines)


def format_h024_robustness_detailed_report(
    results: Sequence[H024RobustnessScenarioResult],
) -> str:
    """Format robustness summary plus detailed reports for each scenario."""

    sections = [format_h024_robustness_summary(results)]

    for result in results:
        sections.extend(
            [
                "",
                f"Detailed scenario report: {result.scenario.label}",
                format_h024_diagnostic_report((result.run,)),
            ]
        )

    return "\n".join(sections)


def _validate_scenario(scenario: H024RobustnessScenario) -> None:
    if not scenario.label:
        raise ValueError("scenario label must be non-empty")
    if scenario.stop_atr_multiple <= 0.0:
        raise ValueError("stop_atr_multiple must be positive")
    if scenario.cost_multiplier <= 0.0:
        raise ValueError("cost_multiplier must be positive")
    if scenario.cost_multiplier < 1.0:
        raise ValueError("cost_multiplier must not reduce modeled costs")


@contextmanager
def _patched_h024_cost_multiplier(cost_multiplier: float) -> Iterator[None]:
    original = h017_event.price_with_execution_costs

    def stressed_price_with_execution_costs(**kwargs):
        symbol = kwargs["symbol"]
        base = get_default_cost_spec(symbol)
        stressed = SymbolCostSpec(
            symbol=base.symbol,
            spread_price=base.spread_price * cost_multiplier,
            commission_usd_per_lot_per_fill=(
                base.commission_usd_per_lot_per_fill * cost_multiplier
            ),
            stop_slippage_atr_fraction=base.stop_slippage_atr_fraction * cost_multiplier,
        )
        return original(**{**kwargs, "cost_spec": stressed})

    h017_event.price_with_execution_costs = stressed_price_with_execution_costs
    try:
        yield
    finally:
        h017_event.price_with_execution_costs = original
