from __future__ import annotations

"""Per-symbol strategy signal generators.

Phase 2.2: deterministic Donchian-breakout signal generators for
USDJPY and XAUUSD. Per H006/H007 graveyard, signals are deterministic
rules — ML is explicitly forbidden at this layer.

Public API:
    - SignalConfig: frozen dataclass holding lookback + optional ATR floor
    - usdjpy_trend_signal: Donchian breakout, no ATR floor by default
    - xauusd_trend_signal: Donchian breakout with ATR-percent floor
    - donchian_signal: shared underlying engine (exposed for testing)
"""

from quantcore.strategy.signals import (
    SignalConfig,
    donchian_signal,
    usdjpy_trend_signal,
    xauusd_trend_signal,
)

__all__ = [
    "SignalConfig",
    "donchian_signal",
    "usdjpy_trend_signal",
    "xauusd_trend_signal",
]