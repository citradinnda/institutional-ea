from __future__ import annotations

"""Strict event routing for H019.

H019 returns an H017Result-shaped object, so this module deliberately reuses
the existing H017 strict event bridge.

Important:
    - H018 guards remain in the bridge.
    - This module does not weaken, skip, clip, or bypass guards.
    - This module does not run real-data validation by itself.
"""

from typing import Any

import pandas as pd

from quantcore.backtest.h017_strict_event import (
    backtest_h017_strict_event_from_result,
)
from quantcore.strategy.h017 import H017Config, H017Result
from quantcore.strategy.h019 import run_h019


def backtest_h019_strict_event(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    config: H017Config | None = None,
    **strict_event_kwargs: Any,
) -> Any:
    """Run H019, then route its result through the strict event bridge.

    Args:
        usdjpy_h4: Canonical USDJPY H4 OHLCV frame.
        xauusd_h4: Canonical XAUUSD H4 OHLCV frame.
        config: Optional H017Config-compatible configuration used by H019.
        strict_event_kwargs: Remaining keyword arguments forwarded to
            backtest_h017_strict_event_from_result, including M1 frames,
            accepted complete-window timestamps, equity, costs, specs, and
            optional slippage ATR panels.

    Returns:
        The existing strict event backtest result object.
    """
    h019_result = run_h019(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=config,
    )

    return backtest_h017_strict_event_from_result(
        h017_result=h019_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        **strict_event_kwargs,
    )


def backtest_h019_strict_event_from_result(
    *,
    h019_result: H017Result,
    **strict_event_kwargs: Any,
) -> Any:
    """Route a precomputed H019 result through the strict event bridge.

    This helper is useful for diagnostics and tests where the strategy output
    has already been computed. The argument name is intentionally h019_result,
    but the object remains H017Result-shaped for bridge compatibility.
    """
    return backtest_h017_strict_event_from_result(
        h017_result=h019_result,
        **strict_event_kwargs,
    )
