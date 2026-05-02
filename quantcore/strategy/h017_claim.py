from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from quantcore.strategy.h017 import H017Config, run_h017
from quantcore.validation.validator import (
    DSRResult,
    MinTRLResult,
    PSRResult,
    deflated_sharpe_ratio,
    min_track_record_length_from_returns,
    probabilistic_sharpe_ratio,
)


@dataclass(frozen=True)
class H017BacktestResult:
    """Result of running H017 over OHLCV panels with a t+1 position lag.

    WHY: A position decided at the close of bar t cannot be traded until bar
    t+1 — we have not yet observed bar t's close at the moment we would have
    needed to act. Lagging by one bar is the load-bearing no-look-ahead
    invariant for this 2.5 claim. Phase 2.4 already inner-joins USDJPY and
    XAUUSD timestamps inside run_h017, so positions and per-symbol returns
    share a single calendar.
    """

    portfolio_returns: pd.Series
    per_symbol_returns: pd.DataFrame
    positions: pd.DataFrame
    n_bars: int


@dataclass(frozen=True)
class H017Claim:
    """Validator-gated promotion claim for H017.

    WHY: The H001-H016 graveyard is 16 dead strategies. Any new claim must
    clear PSR (probability the true Sharpe exceeds benchmark) AND MinTRL
    (do we have enough bars to actually detect that Sharpe). DSR is opt-in
    via sr_estimates and explicitly deflates for the multiple-testing bias
    of having tried prior strategies. promotable = AND of every gate that
    actually ran (§6 validator convention). Summary uses ASCII +/- only to
    stay PowerShell-safe (§6 validator orchestrator note).
    """

    psr: PSRResult
    min_trl: MinTRLResult
    dsr: Optional[DSRResult]
    n_trials: Optional[int]
    periods_per_year: int
    n_bars: int
    promotable: bool
    summary: str


def backtest_h017(
    usdjpy_ohlcv: pd.DataFrame,
    xauusd_ohlcv: pd.DataFrame,
    config: H017Config | None = None,
) -> H017BacktestResult:
    """Zero-cost H017 backtest with t+1 position lag.

    WHY: 2.5 isolates the validator gate from cost-model assumptions.
    Realistic spread / slippage / commission lives in Phase 3's intrabar
    M1 fill engine. Per-bar P&L = position[t-1] * close.pct_change()[t].
    Portfolio return = sum across symbols (single portfolio series, since
    H017 is a portfolio strategy with a heat governor — gating per-symbol
    would defeat the governor's purpose).
    """
    if config is None:
        config = H017Config.default()

    h017_result = run_h017(usdjpy_ohlcv, xauusd_ohlcv, config)
    positions = h017_result.positions

    # Per-symbol close-to-close returns reindexed onto the inner-joined panel.
    usdjpy_close = usdjpy_ohlcv["close"].reindex(positions.index)
    xauusd_close = xauusd_ohlcv["close"].reindex(positions.index)

    usdjpy_ret = usdjpy_close.pct_change()
    xauusd_ret = xauusd_close.pct_change()

    # t+1 lag: position decided at close of bar t is realized over bar t+1.
    per_symbol = pd.DataFrame(
        {
            "USDJPY": positions["USDJPY"].shift(1) * usdjpy_ret,
            "XAUUSD": positions["XAUUSD"].shift(1) * xauusd_ret,
        },
        index=positions.index,
    )

    portfolio = per_symbol.sum(axis=1, skipna=True)
    portfolio.name = "portfolio_returns"

    return H017BacktestResult(
        portfolio_returns=portfolio,
        per_symbol_returns=per_symbol,
        positions=positions,
        n_bars=len(portfolio),
    )


def build_h017_claim(
    returns: pd.Series,
    *,
    periods_per_year: int = 1512,
    sr_benchmark: float = 0.0,
    confidence: float = 0.95,
    psr_threshold: float = 0.95,
    sr_estimates: np.ndarray | pd.Series | None = None,
    dsr_threshold: float = 0.95,
) -> H017Claim:
    """Run PSR + MinTRL (mandatory) and DSR (opt-in) on portfolio returns.

    WHY: PSR alone can be high if the track record is short and lucky;
    MinTRL gates the length question. DSR deflates for selection bias when
    sr_estimates is provided (one Sharpe per attempted strategy). Default
    periods_per_year=1512 matches the H4 bar convention from §6 / 2.4.
    All thresholds are explicit kwargs so the caller can tighten them later
    without editing this module.
    """
    clean = returns.dropna()
    n_bars = len(clean)

    psr = probabilistic_sharpe_ratio(
        clean, sr_benchmark=sr_benchmark, periods_per_year=periods_per_year
    )
    min_trl = min_track_record_length_from_returns(
        clean,
        sr_benchmark=sr_benchmark,
        confidence=confidence,
        periods_per_year=periods_per_year,
    )

    dsr: DSRResult | None = None
    n_trials: int | None = None
    if sr_estimates is not None:
        dsr = deflated_sharpe_ratio(
            clean,
            sr_estimates=sr_estimates,
            sr_benchmark=sr_benchmark,
            periods_per_year=periods_per_year,
        )
        n_trials = dsr.n_trials

    psr_pass = psr.psr >= psr_threshold
    # MinTRL passes only if (a) feasible per §6 sentinel AND (b) we have
    # enough bars to satisfy the required track-record length.
    min_trl_pass = bool(min_trl.feasible) and (min_trl.min_n <= n_bars)
    dsr_pass = True if dsr is None else (dsr.dsr >= dsr_threshold)

    promotable = bool(psr_pass and min_trl_pass and dsr_pass)

    lines = [
        f"H017 Claim Summary (n={n_bars}, ppy={periods_per_year})",
        (
            f"  PSR:    psr={psr.psr:.4f}  obs_SR={psr.observed_sr:+.4f}  "
            f"[{'PASS' if psr_pass else 'FAIL'} >= {psr_threshold:.2f}]"
        ),
        (
            f"  MinTRL: feasible={min_trl.feasible}  min_n={min_trl.min_n}  "
            f"have_n={n_bars}  [{'PASS' if min_trl_pass else 'FAIL'}]"
        ),
    ]
    if dsr is not None:
        lines.append(
            f"  DSR:    dsr={dsr.dsr:.4f}  n_trials={dsr.n_trials}  "
            f"[{'PASS' if dsr_pass else 'FAIL'} >= {dsr_threshold:.2f}]"
        )
    else:
        lines.append("  DSR:    SKIPPED (no sr_estimates provided)")
    lines.append(f"  PROMOTABLE: {promotable}")
    summary = "\n".join(lines)

    return H017Claim(
        psr=psr,
        min_trl=min_trl,
        dsr=dsr,
        n_trials=n_trials,
        periods_per_year=periods_per_year,
        n_bars=n_bars,
        promotable=promotable,
        summary=summary,
    )


def _synthetic_panel(
    n_bars: int = 400, seed: int = 7
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Synthetic two-symbol H4 OHLCV for the __main__ runner only.

    WHY: 2.5 deliberately uses synthetic data so the validator gate is
    exercised end-to-end without a real-data dependency. Real-data wiring
    (Kaggle dataset / local CSV) is a separate sub-step or Phase 3.
    """
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2020-01-01", periods=n_bars, freq="4h", tz="UTC")

    def _make(start: float, vol: float, sub_seed: int) -> pd.DataFrame:
        sub = np.random.default_rng(seed + sub_seed)
        rets = sub.normal(0.0, vol, size=n_bars)
        close = start * np.exp(np.cumsum(rets))
        high = close * (1.0 + np.abs(sub.normal(0, vol, n_bars)))
        low = close * (1.0 - np.abs(sub.normal(0, vol, n_bars)))
        open_ = np.concatenate([[start], close[:-1]])
        volume = sub.integers(100, 1000, n_bars).astype(float)
        return pd.DataFrame(
            {"open": open_, "high": high, "low": low,
             "close": close, "volume": volume},
            index=idx,
        )

    return _make(110.0, 0.003, 1), _make(1800.0, 0.005, 2)


if __name__ == "__main__":
    usdjpy, xauusd = _synthetic_panel()
    bt = backtest_h017(usdjpy, xauusd)
    claim = build_h017_claim(bt.portfolio_returns)
    print(claim.summary)