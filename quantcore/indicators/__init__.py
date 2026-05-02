"""
Phase 2.1 indicator helpers.

WHY a separate package: indicators will accumulate (ATR, chandelier exit,
vol-target sizing in 2.1; later RSI / momentum / regime filters). Keeping
them in their own package — disjoint from `quantcore/validation/` and
`quantcore/data/` — preserves clean import boundaries and prevents the
strategy layer from accidentally pulling validation symbols into prod paths.

All indicators in this package follow the canonical OHLCV input convention
established in Phase 1.1: lowercase columns ('open', 'high', 'low', 'close',
optionally 'volume') and a DatetimeIndex (UTC by convention).
"""
from __future__ import annotations

from quantcore.indicators.atr import average_true_range

__all__ = ["average_true_range"]