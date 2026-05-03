from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

Side = Literal["buy", "sell"]
ExitReason = Literal["stop", "tp", "signal_flip", "end_of_data"]

_REQUIRED_M1_COLUMNS = ("open", "high", "low", "close")


@dataclass(frozen=True)
class Fill:
    """A completed trade fill.

    The fill engine records execution facts separately from strategy decisions
    because Phase 4 live trading will need the same distinction: the strategy
    says what it wants, while the broker/execution layer says what actually
    happened.

    ``pnl_quote`` is before commission and is expressed in the instrument's
    quote currency units after applying ``contract_size``. For XAUUSD this is
    USD. For USDJPY this is JPY, which Phase 3.3 portfolio accounting will
    convert into account currency.
    """

    symbol: str
    side: Side
    entry_time_utc: pd.Timestamp
    entry_price: float
    exit_time_utc: pd.Timestamp
    exit_price: float
    lots: float
    pnl_quote: float
    commission: float
    slippage: float
    exit_reason: ExitReason


def simulate_bracket_trade(
    *,
    symbol: str,
    side: Side,
    entry_time_utc: pd.Timestamp,
    entry_price: float,
    lots: float,
    m1_bars: pd.DataFrame,
    stop_price: float | None = None,
    take_profit_price: float | None = None,
    forced_exit_time_utc: pd.Timestamp | None = None,
    forced_exit_price: float | None = None,
    contract_size: float = 1.0,
    commission: float = 0.0,
    stop_slippage: float = 0.0,
) -> Fill:
    """Resolve one bracket-style trade using M1 bars.

    This function is intentionally small and deterministic. It answers one
    execution question: after a position is opened, which event happens first
    inside the available M1 path - stop, take-profit, forced signal exit, or
    end of data?

    If both stop and take-profit are touched inside the same M1 candle, the
    stop wins. M1 OHLC does not reveal the tick order inside that minute, and
    assuming the take-profit filled first would systematically overstate
    strategy quality. This conservative rule directly addresses H001's lesson:
    intrabar fill assumptions can turn a backtest into fiction.

    Parameters
    ----------
    symbol:
        Instrument label, for example ``"USDJPY"`` or ``"XAUUSD"``.
    side:
        ``"buy"`` for long trades, ``"sell"`` for short trades.
    entry_time_utc:
        Time the trade is considered live. Must be timezone-aware UTC.
    entry_price:
        Executed entry price before Phase 3.2 costs.
    lots:
        Position size in broker lots. Phase 3.3 will calculate this from H017's
        target risk fraction and live equity.
    m1_bars:
        Canonical M1 OHLC bars with a timezone-aware UTC DatetimeIndex.
    stop_price:
        Stop-loss price. Optional because some tests and future exit modes may
        use forced exits only.
    take_profit_price:
        Take-profit price. Optional because H017 currently uses ATR/chandelier
        exits rather than a fixed TP.
    forced_exit_time_utc:
        Optional forced exit time, used for signal flips or portfolio rebalances.
        Stops and take-profits are checked strictly before this timestamp.
    forced_exit_price:
        Executed forced-exit price. If omitted, the function uses the latest M1
        close available up to the forced exit time.
    contract_size:
        Quote-currency units per lot per 1.0 price move. Kept explicit so tests
        can stay simple while Phase 3.3 later supplies broker-specific values.
    commission:
        Commission in account currency. Stored on the Fill but not subtracted
        from ``pnl_quote`` because ``pnl_quote`` may not yet be account currency.
    stop_slippage:
        Price-unit slippage applied only to stop exits. Positive values always
        worsen the stop fill.
    """

    _validate_side(side)
    entry_time = _require_utc_timestamp("entry_time_utc", entry_time_utc)
    forced_exit_time = (
        _require_utc_timestamp("forced_exit_time_utc", forced_exit_time_utc)
        if forced_exit_time_utc is not None
        else None
    )

    if forced_exit_time is not None and forced_exit_time <= entry_time:
        raise ValueError("forced_exit_time_utc must be after entry_time_utc")

    _validate_positive_number("entry_price", entry_price)
    _validate_positive_number("lots", lots)
    _validate_positive_number("contract_size", contract_size)

    if commission < 0.0:
        raise ValueError("commission must be >= 0.0")
    if stop_slippage < 0.0:
        raise ValueError("stop_slippage must be >= 0.0")

    if stop_price is not None:
        _validate_positive_number("stop_price", stop_price)
    if take_profit_price is not None:
        _validate_positive_number("take_profit_price", take_profit_price)
    if forced_exit_price is not None:
        _validate_positive_number("forced_exit_price", forced_exit_price)

    bars = _validate_m1_bars(m1_bars)

    scan_bars = _select_scan_window(
        bars=bars,
        entry_time_utc=entry_time,
        forced_exit_time_utc=forced_exit_time,
    )

    for timestamp, row in scan_bars.iterrows():
        high = float(row["high"])
        low = float(row["low"])

        if _stop_hit(side=side, low=low, high=high, stop_price=stop_price):
            raw_exit_price = float(stop_price)
            exit_price = _apply_stop_slippage(
                side=side,
                stop_price=raw_exit_price,
                stop_slippage=stop_slippage,
            )
            return _build_fill(
                symbol=symbol,
                side=side,
                entry_time_utc=entry_time,
                entry_price=entry_price,
                exit_time_utc=pd.Timestamp(timestamp),
                exit_price=exit_price,
                lots=lots,
                contract_size=contract_size,
                commission=commission,
                slippage=stop_slippage,
                exit_reason="stop",
            )

        if _take_profit_hit(
            side=side,
            low=low,
            high=high,
            take_profit_price=take_profit_price,
        ):
            raw_exit_price = float(take_profit_price)
            return _build_fill(
                symbol=symbol,
                side=side,
                entry_time_utc=entry_time,
                entry_price=entry_price,
                exit_time_utc=pd.Timestamp(timestamp),
                exit_price=raw_exit_price,
                lots=lots,
                contract_size=contract_size,
                commission=commission,
                slippage=0.0,
                exit_reason="tp",
            )

    if forced_exit_time is not None:
        exit_price = _forced_exit_price(
            bars=bars,
            entry_time_utc=entry_time,
            forced_exit_time_utc=forced_exit_time,
            forced_exit_price=forced_exit_price,
        )
        return _build_fill(
            symbol=symbol,
            side=side,
            entry_time_utc=entry_time,
            entry_price=entry_price,
            exit_time_utc=forced_exit_time,
            exit_price=exit_price,
            lots=lots,
            contract_size=contract_size,
            commission=commission,
            slippage=0.0,
            exit_reason="signal_flip",
        )

    end_bars = bars.loc[bars.index >= entry_time]
    if end_bars.empty:
        raise ValueError("m1_bars contains no bars at or after entry_time_utc")

    exit_time = pd.Timestamp(end_bars.index[-1])
    exit_price = float(end_bars.iloc[-1]["close"])

    return _build_fill(
        symbol=symbol,
        side=side,
        entry_time_utc=entry_time,
        entry_price=entry_price,
        exit_time_utc=exit_time,
        exit_price=exit_price,
        lots=lots,
        contract_size=contract_size,
        commission=commission,
        slippage=0.0,
        exit_reason="end_of_data",
    )


def _validate_side(side: Side) -> None:
    if side not in ("buy", "sell"):
        raise ValueError("side must be 'buy' or 'sell'")


def _require_utc_timestamp(name: str, timestamp: pd.Timestamp) -> pd.Timestamp:
    ts = pd.Timestamp(timestamp)

    if ts.tz is None:
        raise ValueError(f"{name} must be timezone-aware UTC")

    ts_utc = ts.tz_convert("UTC")
    if str(ts_utc.tz) != "UTC":
        raise ValueError(f"{name} must convert cleanly to UTC")

    return ts_utc


def _validate_positive_number(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0.0")


def _validate_m1_bars(m1_bars: pd.DataFrame) -> pd.DataFrame:
    missing = [column for column in _REQUIRED_M1_COLUMNS if column not in m1_bars.columns]
    if missing:
        raise ValueError(f"m1_bars missing required columns: {missing}")

    if not isinstance(m1_bars.index, pd.DatetimeIndex):
        raise ValueError("m1_bars must use a DatetimeIndex")

    if m1_bars.index.tz is None:
        raise ValueError("m1_bars index must be timezone-aware UTC")

    index_utc = m1_bars.index.tz_convert("UTC")
    if not index_utc.is_monotonic_increasing:
        raise ValueError("m1_bars index must be sorted ascending")

    if index_utc.has_duplicates:
        raise ValueError("m1_bars index must not contain duplicates")

    bars = m1_bars.copy()
    bars.index = index_utc
    return bars


def _select_scan_window(
    *,
    bars: pd.DataFrame,
    entry_time_utc: pd.Timestamp,
    forced_exit_time_utc: pd.Timestamp | None,
) -> pd.DataFrame:
    if forced_exit_time_utc is None:
        scan_bars = bars.loc[bars.index >= entry_time_utc]
    else:
        scan_bars = bars.loc[
            (bars.index >= entry_time_utc)
            & (bars.index < forced_exit_time_utc)
        ]

    if scan_bars.empty:
        raise ValueError("m1_bars contains no bars in the trade scan window")

    return scan_bars


def _stop_hit(
    *,
    side: Side,
    low: float,
    high: float,
    stop_price: float | None,
) -> bool:
    if stop_price is None:
        return False

    if side == "buy":
        return low <= stop_price

    return high >= stop_price


def _take_profit_hit(
    *,
    side: Side,
    low: float,
    high: float,
    take_profit_price: float | None,
) -> bool:
    if take_profit_price is None:
        return False

    if side == "buy":
        return high >= take_profit_price

    return low <= take_profit_price


def _apply_stop_slippage(
    *,
    side: Side,
    stop_price: float,
    stop_slippage: float,
) -> float:
    if side == "buy":
        return stop_price - stop_slippage

    return stop_price + stop_slippage


def _forced_exit_price(
    *,
    bars: pd.DataFrame,
    entry_time_utc: pd.Timestamp,
    forced_exit_time_utc: pd.Timestamp,
    forced_exit_price: float | None,
) -> float:
    if forced_exit_price is not None:
        return float(forced_exit_price)

    eligible = bars.loc[
        (bars.index >= entry_time_utc)
        & (bars.index <= forced_exit_time_utc)
    ]
    if eligible.empty:
        raise ValueError("cannot infer forced exit price without eligible M1 bars")

    return float(eligible.iloc[-1]["close"])


def _build_fill(
    *,
    symbol: str,
    side: Side,
    entry_time_utc: pd.Timestamp,
    entry_price: float,
    exit_time_utc: pd.Timestamp,
    exit_price: float,
    lots: float,
    contract_size: float,
    commission: float,
    slippage: float,
    exit_reason: ExitReason,
) -> Fill:
    pnl_quote = _pnl_quote(
        side=side,
        entry_price=entry_price,
        exit_price=exit_price,
        lots=lots,
        contract_size=contract_size,
    )

    return Fill(
        symbol=symbol,
        side=side,
        entry_time_utc=entry_time_utc,
        entry_price=float(entry_price),
        exit_time_utc=exit_time_utc,
        exit_price=float(exit_price),
        lots=float(lots),
        pnl_quote=pnl_quote,
        commission=float(commission),
        slippage=float(slippage),
        exit_reason=exit_reason,
    )


def _pnl_quote(
    *,
    side: Side,
    entry_price: float,
    exit_price: float,
    lots: float,
    contract_size: float,
) -> float:
    direction = 1.0 if side == "buy" else -1.0
    return direction * (exit_price - entry_price) * lots * contract_size
