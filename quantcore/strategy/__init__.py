from __future__ import annotations

"""Per-symbol strategy signal generators and portfolio heat governor.

Phase 2.2: deterministic Donchian-breakout signal generators for
USDJPY and XAUUSD. Per H006/H007 graveyard, signals are deterministic
rules — ML is explicitly forbidden at this layer.

Phase 2.3: portfolio heat governor (the H017 fix). Caps simultaneous
open risk at the portfolio level and accounts for correlation.

Public API:
    Signals (2.2):
        - SignalConfig
        - donchian_signal
        - usdjpy_trend_signal
        - xauusd_trend_signal
    Heat governor (2.3):
        - HeatConfig
        - HeatResult
        - heat_governor
"""

from quantcore.strategy.heat_governor import (
    HeatConfig,
    HeatResult,
    heat_governor,
)
from quantcore.strategy.signals import (
    SignalConfig,
    donchian_signal,
    usdjpy_trend_signal,
    xauusd_trend_signal,
)

__all__ = [
    "HeatConfig",
    "HeatResult",
    "SignalConfig",
    "donchian_signal",
    "heat_governor",
    "usdjpy_trend_signal",
    "xauusd_trend_signal",
]