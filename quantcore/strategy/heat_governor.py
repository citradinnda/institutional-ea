from __future__ import annotations

"""Portfolio heat governor — the H017 fix.

Why this module exists (read this before changing anything):
    H016 (graveyard §7) ran USDJPY + XAUUSD with 1% per-trade risk per
    symbol. The per-trade math was correct. But when both symbols were
    simultaneously in a position — which trend-following systems do
    constantly during macro regime trends — the PORTFOLIO-level open
    risk was 2%, not 1%. When those positions correlated (gold and yen
    co-move during USD-strength regimes), effective combined risk
    exceeded the naive sum. Result: -19.43% drawdown on a 10%-target
    system.

    H017 = H016 + this governor. The governor caps simultaneous open
    risk at the portfolio level and accounts for correlation, scaling
    desired positions down (never up) when the cap would be breached.

Key design decisions (locked from §11 design brief):
    - Fixed-fraction per-trade risk (1%); avoids double-counting with
      vol-target sizing in indicators/vol_target.py.
    - Portfolio heat cap 1.5% (H016 blew up at 2%, giving zero slippage
      margin; 1% would forbid both-on; 1.5% is the H017 sweet spot).
    - Combined heat via portfolio variance: sqrt(w'Σw) where Σ uses
      r² on the diagonal and r²·ρ_ij off-diagonal.
    - Correlation floored at 0 (H015 graveyard: never assume
      diversification benefit; only penalise positive coupling).
    - Proportional scaling when over cap: k = cap / desired_heat,
      applied equally to all symbols (symmetric, no hidden bias).
    - Stateless vectorized function — pure given (signals, returns, config).

Output convention:
    HeatResult.multipliers is a DataFrame aligned to signals.index, with
    one column per symbol, values in [0, 1]. The caller (Phase 2.4)
    multiplies each symbol's vol-target size by the corresponding
    multiplier to get the final position size. A multiplier of 0 means
    'no position'; 1 means 'full intended size'; intermediate means
    'scaled down for portfolio risk'.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class HeatConfig:
    """Configuration for the portfolio heat governor.

    Attributes:
        max_portfolio_heat: Hard cap on combined open risk as a fraction
            of equity. 0.015 = 1.5%. Must be > 0.
        per_trade_risk: Per-symbol intended risk pre-governor, as a
            fraction of equity. 0.01 = 1%. Must be > 0.
        correlation_window: Rolling window in bars for correlation
            estimation. Must be >= 2.
        correlation_floor: Lower bound applied to correlations before
            heat calculation. 0.0 = treat negative correlations as zero
            (institutional default; never bank diversification benefit).
            Must be in [0, 1].
    """

    max_portfolio_heat: float = 0.015
    per_trade_risk: float = 0.01
    correlation_window: int = 120
    correlation_floor: float = 0.0

    def __post_init__(self) -> None:
        if self.max_portfolio_heat <= 0:
            raise ValueError(
                f"max_portfolio_heat must be > 0, got {self.max_portfolio_heat}."
            )
        if self.per_trade_risk <= 0:
            raise ValueError(
                f"per_trade_risk must be > 0, got {self.per_trade_risk}."
            )
        if self.correlation_window < 2:
            raise ValueError(
                f"correlation_window must be >= 2, got {self.correlation_window}."
            )
        if not 0.0 <= self.correlation_floor <= 1.0:
            raise ValueError(
                f"correlation_floor must be in [0, 1], got {self.correlation_floor}."
            )


@dataclass(frozen=True)
class HeatResult:
    """Output of the heat governor.

    Attributes:
        multipliers: DataFrame indexed like signals, one column per
            symbol, values in [0, 1]. Multiply this by the per-symbol
            vol-target size in the integration layer (Phase 2.4) to get
            final position size.
        portfolio_heat_pre: Series of pre-governor combined heat per bar
            (i.e. what risk WOULD be if we honoured every signal at full
            per_trade_risk). Useful for diagnostics / governance.
        portfolio_heat_post: Series of post-governor combined heat per
            bar. Should always be <= max_portfolio_heat (within float
            tolerance).
        binding: Boolean Series, True when the cap was binding on that
            bar (i.e. governor scaled positions down).
    """

    multipliers: pd.DataFrame
    portfolio_heat_pre: pd.Series
    portfolio_heat_post: pd.Series
    binding: pd.Series


def _validate_inputs(signals: pd.DataFrame, returns: pd.DataFrame) -> None:
    """Defensive depth: validate panel inputs at module boundary."""
    if not isinstance(signals, pd.DataFrame):
        raise TypeError(f"signals must be DataFrame, got {type(signals).__name__}.")
    if not isinstance(returns, pd.DataFrame):
        raise TypeError(f"returns must be DataFrame, got {type(returns).__name__}.")
    if not isinstance(signals.index, pd.DatetimeIndex):
        raise TypeError("signals.index must be DatetimeIndex.")
    if not isinstance(returns.index, pd.DatetimeIndex):
        raise TypeError("returns.index must be DatetimeIndex.")
    if signals.shape[1] < 1:
        raise ValueError("signals must have at least one column.")
    if list(signals.columns) != list(returns.columns):
        raise ValueError(
            f"signals and returns must have identical columns in the same order. "
            f"signals={list(signals.columns)}, returns={list(returns.columns)}."
        )
    if not signals.index.equals(returns.index):
        raise ValueError(
            "signals.index and returns.index must be identical "
            "(same length, same timestamps, same order)."
        )
    if signals.index.has_duplicates:
        raise ValueError("signals.index has duplicates.")
    if not signals.index.is_monotonic_increasing:
        raise ValueError("signals.index must be sorted ascending.")


def _combined_heat(
    weights: np.ndarray,
    corr_matrix: np.ndarray,
    per_trade_risk: float,
) -> float:
    """Compute portfolio-level open risk via the variance formula.

    weights: signed direction array, e.g. [+1, -1] for long-short.
    corr_matrix: K x K symmetric matrix with 1.0 on the diagonal and
        floored correlations off-diagonal.
    per_trade_risk: scalar r (e.g. 0.01).

    Returns sqrt(w' (r^2 * C) w). Returns 0 if all weights are 0.
    """
    if not np.any(weights):
        return 0.0
    # variance contribution = sum_ij w_i * w_j * r^2 * corr_ij
    var = float(weights @ corr_matrix @ weights) * (per_trade_risk ** 2)
    # Numerical guard: variance must be non-negative.
    return float(np.sqrt(max(var, 0.0)))


def heat_governor(
    signals: pd.DataFrame,
    returns: pd.DataFrame,
    config: HeatConfig | None = None,
) -> HeatResult:
    """Compute per-bar position multipliers that cap portfolio open risk.

    Algorithm per bar t:
        1. Read signals[t] -> weight vector w in {-1, 0, +1}^K.
        2. Read rolling correlation matrix from returns[t-window..t-1]
           (strictly prior; no look-ahead). Floor off-diagonals at
           config.correlation_floor.
        3. Compute desired heat = sqrt(w' (r^2 * C) w).
        4. If desired_heat > cap, multiplier = cap / desired_heat for
           ALL active symbols (proportional). Else multiplier = 1.
        5. Inactive symbols (w_i = 0) get multiplier 0.

    Warm-up bars (where rolling correlation is not yet defined) use
    the identity matrix as a fallback — i.e. correlation is treated as
    zero between distinct symbols, which is the most permissive
    (least heat-inflating) assumption pre-warmup. This is intentional:
    it lets backtests start trading on bar (correlation_window) instead
    of bar (correlation_window * 2), at the cost of a slightly looser
    cap on the very first bars. For K=2 with warm-up correlations
    treated as 0, both-on heat = r*sqrt(2) ≈ 1.41%, which is still
    under the 1.5% cap, so no false binding occurs.

    Args:
        signals: Per-symbol signal panel, columns = symbols, values in
            {-1, 0, +1, NaN}. NaN is treated as 0 (no position).
        returns: Per-symbol per-bar returns (NOT prices), aligned
            identically to signals. Used only for rolling correlation.
        config: Optional HeatConfig override. Defaults to H017 settings.

    Returns:
        HeatResult with multipliers, pre/post heat series, binding flag.
    """
    if config is None:
        config = HeatConfig()
    _validate_inputs(signals, returns)

    # Treat NaN signals as 0 (flat). Cast to float for arithmetic.
    sig = signals.fillna(0.0).astype(float)
    rets = returns.astype(float)

    n_bars = len(sig)
    symbols = list(sig.columns)
    k = len(symbols)
    r = config.per_trade_risk
    cap = config.max_portfolio_heat
    floor = config.correlation_floor
    win = config.correlation_window

    # Pre-compute rolling correlations. We use returns.shift(1).rolling(...)
    # so that the correlation at bar t uses bars t-win .. t-1, NOT t.
    # This is the same no-lookahead convention as Donchian channels in
    # signals.py (prior-N-bar high/low) and vol-target in 2.1b.
    rets_prior = rets.shift(1)

    # rolling().corr() on a DataFrame returns a stacked frame: MultiIndex
    # (date, symbol) x columns=symbols. We extract per-bar K x K matrices
    # by groupby on the date level.
    rolling_corr = rets_prior.rolling(window=win, min_periods=win).corr()

    multipliers = np.zeros((n_bars, k), dtype=float)
    heat_pre = np.zeros(n_bars, dtype=float)
    heat_post = np.zeros(n_bars, dtype=float)
    binding = np.zeros(n_bars, dtype=bool)

    sig_values = sig.to_numpy()
    timestamps = sig.index

    # Identity fallback for bars where rolling correlation is undefined.
    identity = np.eye(k, dtype=float)

    for t in range(n_bars):
        w = sig_values[t]

        # Build the correlation matrix for this bar.
        ts = timestamps[t]
        try:
            block = rolling_corr.loc[ts]
            # block is a DataFrame indexed by symbols, columns by symbols.
            corr_raw = block.to_numpy()
            if np.isnan(corr_raw).any():
                # Warm-up: rolling() returns NaN until min_periods met.
                corr = identity
            else:
                corr = corr_raw.copy()
                # Floor off-diagonals; preserve diagonal at 1.0.
                np.fill_diagonal(corr, 1.0)
                off_diag_mask = ~np.eye(k, dtype=bool)
                corr[off_diag_mask] = np.maximum(corr[off_diag_mask], floor)
        except KeyError:
            corr = identity

        desired = _combined_heat(w, corr, r)
        heat_pre[t] = desired

        if desired <= 0.0:
            # No active positions; multipliers stay 0, heat stays 0.
            continue

        if desired <= cap + 1e-12:
            # Under cap: full size for active symbols.
            mult_scalar = 1.0
            heat_post[t] = desired
        else:
            # Over cap: scale proportionally.
            mult_scalar = cap / desired
            heat_post[t] = cap
            binding[t] = True

        # Apply multiplier only to active symbols (where |w_i| > 0).
        active = np.abs(w) > 0
        multipliers[t, active] = mult_scalar

    multipliers_df = pd.DataFrame(multipliers, index=sig.index, columns=symbols)
    heat_pre_s = pd.Series(heat_pre, index=sig.index, name="portfolio_heat_pre")
    heat_post_s = pd.Series(heat_post, index=sig.index, name="portfolio_heat_post")
    binding_s = pd.Series(binding, index=sig.index, name="binding")

    return HeatResult(
        multipliers=multipliers_df,
        portfolio_heat_pre=heat_pre_s,
        portfolio_heat_post=heat_post_s,
        binding=binding_s,
    )