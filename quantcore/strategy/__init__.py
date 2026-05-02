from __future__ import annotations

"""Per-symbol signal generators, heat governor, and H017 integration.

Phase 2.2: deterministic Donchian-breakout signals (USDJPY + XAUUSD).
Phase 2.3: portfolio heat governor (the H017 fix).
Phase 2.4: H017 strategy integration glueing 2.1-2.3 together.

Public API:
    Signals:        SignalConfig, donchian_signal,
                    usdjpy_trend_signal, xauusd_trend_signal
    Heat governor:  HeatConfig, HeatResult, heat_governor
    H017 strategy:  H017Config, H017Result, run_h017
"""

from quantcore.strategy.h017 import H017Config, H017Result, run_h017
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
    "H017Config",
    "H017Result",
    "HeatConfig",
    "HeatResult",
    "SignalConfig",
    "donchian_signal",
    "heat_governor",
    "run_h017",
    "usdjpy_trend_signal",
    "xauusd_trend_signal",
]