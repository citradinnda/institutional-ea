"""
Phase 2.1 indicator helpers.

WHY a separate package: indicators will accumulate (ATR, chandelier exit,
vol-target sizing in 2.1; later RSI / momentum / regime filters). Keeping
them in their own package preserves clean import boundaries.

All indicators follow the canonical OHLCV input convention from Phase 1.1:
lowercase columns ('open', 'high', 'low', 'close', optionally 'volume')
and a DatetimeIndex (UTC by convention).
"""
from __future__ import annotations

from quantcore.indicators.atr import average_true_range
from quantcore.indicators.chandelier import chandelier_exit
from quantcore.indicators.vol_target import vol_target_size

__all__ = ["average_true_range", "chandelier_exit", "vol_target_size"]