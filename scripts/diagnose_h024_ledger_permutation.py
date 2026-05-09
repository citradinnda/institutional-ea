"""H024 ledger-level permutation diagnostic.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

Purpose:
- use the existing H024 hold=3 trade ledger,
- avoid expensive real-data M1 backtest shuffles,
- test whether the observed trade order/equity path is unusually benign
  compared with random reorderings of the same realized trade PnLs.

This is a cheap negative-control proxy, not a substitute for full execution
timestamp-shuffle validation.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd

DEFAULT_LEDGER_PATH = (
    Path(__file__).resolve().parents[1]
    / "reports"
    / "h024_hold3_trade_ledger.csv"
)
DEFAULT_PERMUTATION_RUNS = 10_000
DEFAULT_PERMUTATION_SEED = 240240
STARTING_EQUITY_USD = 10_000.0


@dataclass(frozen=True)
class LedgerPathStats:
    total_pnl_usd: float
    ending_equity_usd: float
    max_drawdown: float
    min_equity_usd: float
    ruin: bool


@dataclass(frozen=True)
class LedgerPermutationResult:
    observed: LedgerPathStats
    permutations: pd.DataFrame
    seed: int
    runs: int


def compute_path_stats(
    pnl_values: Sequence[float],
    *,
    starting_equity_usd: float = STARTING_EQUITY_USD,
) -> LedgerPathStats:
    """Compute equity-path stats from an ordered PnL sequence."""

    if starting_equity_usd <= 0.0:
        raise ValueError("starting_equity_usd must be positive")

    equity = float(starting_equity_usd)
    peak = equity
    max_drawdown = 0.0
    min_equity = equity
    ruin = False

    for pnl in pnl_values:
        equity += float(pnl)
        min_equity = min(min_equity, equity)
        if equity <= 0.0:
            ruin = True
        peak = max(peak, equity)
        drawdown = equity / peak - 1.0
        max_drawdown = min(max_drawdown, drawdown)

    return LedgerPathStats(
        total_pnl_usd=equity - starting_equity_usd,
        ending_equity_usd=equity,
        max_drawdown=max_drawdown,
        min_equity_usd=min_equity,
        ruin=ruin,
    )


def run_ledger_permutation_diagnostic(
    *,
    ledger: pd.DataFrame,
    runs: int = DEFAULT_PERMUTATION_RUNS,
    seed: int = DEFAULT_PERMUTATION_SEED,
    starting_equity_usd: float = STARTING_EQUITY_USD,
) -> LedgerPermutationResult:
    """Compare observed ledger order with random PnL reorderings."""

    if runs <= 0:
        raise ValueError("runs must be positive")
    if "pnl_usd" not in ledger.columns:
        raise ValueError("ledger must contain pnl_usd")
    if "exit_time_utc" not in ledger.columns:
        raise ValueError("ledger must contain exit_time_utc")

    ordered = ledger.sort_values("exit_time_utc")
    observed_pnls = [float(value) for value in ordered["pnl_usd"].tolist()]
    observed = compute_path_stats(
        observed_pnls,
        starting_equity_usd=starting_equity_usd,
    )

    rng = random.Random(seed)
    rows = []
    for run_id in range(runs):
        sample = list(observed_pnls)
        rng.shuffle(sample)
        stats = compute_path_stats(sample, starting_equity_usd=starting_equity_usd)
        rows.append(
            {
                "run_id": run_id,
                "ending_equity_usd": stats.ending_equity_usd,
                "total_pnl_usd": stats.total_pnl_usd,
                "max_drawdown": stats.max_drawdown,
                "min_equity_usd": stats.min_equity_usd,
                "ruin": stats.ruin,
            }
        )

    return LedgerPermutationResult(
        observed=observed,
        permutations=pd.DataFrame(rows),
        seed=seed,
        runs=runs,
    )


def format_ledger_permutation_report(result: LedgerPermutationResult) -> str:
    perms = result.permutations
    observed = result.observed

    dd_exceed = int((perms["max_drawdown"] <= observed.max_drawdown).sum())
    min_equity_exceed = int((perms["min_equity_usd"] <= observed.min_equity_usd).sum())
    ruin_count = int(perms["ruin"].sum())

    sections = [
        "H024 ledger-level permutation diagnostic",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        "Observed ledger path:",
        f"total_pnl_usd: {observed.total_pnl_usd:.2f}",
        f"ending_equity_usd: {observed.ending_equity_usd:.2f}",
        f"max_drawdown: {observed.max_drawdown:.4%}",
        f"min_equity_usd: {observed.min_equity_usd:.2f}",
        f"ruin: {observed.ruin}",
        "",
        "Permutation distribution:",
        _format_permutation_distribution(perms),
        "",
        f"Permutation runs: {result.runs}",
        f"Seed: {result.seed}",
        f"Permutations with max_drawdown <= observed max_drawdown: {dd_exceed}",
        f"Max-drawdown empirical worse/equal rate: {dd_exceed / result.runs:.4%}",
        f"Permutations with min_equity <= observed min_equity: {min_equity_exceed}",
        f"Min-equity empirical worse/equal rate: {min_equity_exceed / result.runs:.4%}",
        f"Permutation ruin count: {ruin_count}",
        "",
        "Interpretation rule:",
        "- This does not test signal direction.",
        "- This does not replace full execution timestamp shuffle.",
        "- It tests whether the realized trade-order path was unusually lucky.",
        "- If observed drawdown is better than most permutations, path-order risk remains manageable.",
        "- This diagnostic cannot approve demo/live/Phase 4.",
    ]
    return "\n".join(sections)


def main() -> None:
    print("H024 ledger-level permutation diagnostic")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print()

    if not DEFAULT_LEDGER_PATH.exists():
        raise FileNotFoundError(
            f"ledger not found: {DEFAULT_LEDGER_PATH}. "
            "Run scripts\\diagnose_h024_trade_ledger_real.py first."
        )

    ledger = pd.read_csv(DEFAULT_LEDGER_PATH)
    result = run_ledger_permutation_diagnostic(ledger=ledger)
    print(format_ledger_permutation_report(result))


def _format_permutation_distribution(perms: pd.DataFrame) -> str:
    rows = []
    for metric in ("ending_equity_usd", "total_pnl_usd", "max_drawdown", "min_equity_usd"):
        series = perms[metric]
        rows.append(
            {
                "metric": metric,
                "min": series.min(),
                "p10": series.quantile(0.10),
                "median": series.median(),
                "mean": series.mean(),
                "p90": series.quantile(0.90),
                "max": series.max(),
            }
        )
    return pd.DataFrame(rows).to_string(index=False, float_format=lambda value: f"{value:.6f}")


if __name__ == "__main__":
    main()
