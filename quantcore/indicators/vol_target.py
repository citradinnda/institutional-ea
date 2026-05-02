"""
Volatility-target position sizing.

WHY: H013-H014 graveyard finding — vol-targeted sizing is necessary to
keep portfolio risk constant across regimes. A naive fixed-units strategy
takes too much risk in volatile periods and not enough in quiet ones.

Sizing multiplier at bar t:
    realized_vol_t = std(returns[t-lookback .. t-1]) * sqrt(periods_per_year)
    multiplier_t   = clip(target_vol_annual / realized_vol_t, 0, max_leverage)

WHY the window is [t-lookback .. t-1] EXCLUSIVE of t: the size for bar t
is decided at the close of bar t-1 (live trading constraint). Including
return[t] in realized vol is the classic vol-targeting lookahead bug —
you would size INVERSELY to volatility you have not yet observed.

WHY clip at max_leverage: in vol-collapse regimes (target/realized -> inf)
the multiplier explodes and a single shock blows the account. Default 3.0
is a sane retail ceiling; production callers tune per asset.

Reference:
    Moskowitz, T., Ooi, Y. H., & Pedersen, L. H. (2012). Time series
    momentum. Journal of Financial Economics, 104(2), 228-250.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def vol_target_size(
    returns: pd.Series,
    target_vol_annual: float = 0.10,
    lookback: int = 20,
    periods_per_year: int = 252,
    max_leverage: float = 3.0,
) -> pd.Series:
    """
    Compute the per-bar position-size multiplier for vol-targeting.

    Parameters
    ----------
    returns : pd.Series
        Per-period returns of the underlying (NOT of the strategy).
    target_vol_annual : float, default 0.10
        Target annualized volatility. Must be > 0.
    lookback : int, default 20
        Realized-vol estimation window. Must be >= 2.
    periods_per_year : int, default 252
        Annualization factor. Must be > 0.
    max_leverage : float, default 3.0
        Upper clip on the multiplier. Must be > 0.

    Returns
    -------
    pd.Series
        Sizing multiplier aligned to returns.index, name = "vol_target_size".
        Indices [0..lookback-1] are NaN (warm-up). Indices where realized
        vol is exactly 0 produce max_leverage (clipped from inf).
    """
    if not isinstance(returns, pd.Series):
        raise TypeError("returns must be a pandas Series")
    if target_vol_annual <= 0:
        raise ValueError(f"target_vol_annual must be > 0; got {target_vol_annual}")
    if lookback < 2:
        raise ValueError(f"lookback must be >= 2; got {lookback}")
    if periods_per_year <= 0:
        raise ValueError(f"periods_per_year must be > 0; got {periods_per_year}")
    if max_leverage <= 0:
        raise ValueError(f"max_leverage must be > 0; got {max_leverage}")
    if len(returns) < lookback + 1:
        raise ValueError(
            f"returns has {len(returns)} obs but lookback={lookback} requires "
            f"at least lookback+1"
        )

    # Shift by 1 so the window at index t covers [t-lookback .. t-1].
    realized = (
        returns.shift(1)
        .rolling(lookback, min_periods=lookback)
        .std(ddof=1)
        * np.sqrt(periods_per_year)
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        raw = target_vol_annual / realized
    multiplier = raw.clip(lower=0.0, upper=max_leverage)
    multiplier.name = "vol_target_size"
    return multiplier