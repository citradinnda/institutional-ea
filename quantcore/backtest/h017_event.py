from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import pandas as pd

from quantcore.backtest.cost_model import price_with_execution_costs
from quantcore.backtest.fill_engine import Fill, simulate_bracket_trade
from quantcore.backtest.portfolio import (
    PortfolioResult,
    build_portfolio_result,
    fill_pnl_usd,
    get_default_instrument_spec,
    size_position_from_risk,
)
from quantcore.strategy.h017 import H017Config, H017Result, run_h017

_SYMBOLS: tuple[str, str] = ("USDJPY", "XAUUSD")
_REQUIRED_H4_COLUMNS = ("open", "high", "low", "close")


@dataclass(frozen=True)
class H017EventBacktestResult:
    """Event-driven H017 backtest output.

    H017 produces desired risk exposure. The event backtest converts that
    desired exposure into broker-sized fills, applies execution costs, and then
    builds an account-level USD equity curve.

    This result deliberately keeps the original ``h017`` object because later
    diagnostics need to explain not just what the account equity did, but what
    H017 believed at each decision timestamp.
    """

    h017: H017Result
    portfolio: PortfolioResult
    fills: tuple[Fill, ...]
    n_bars: int
    symbols: tuple[str, ...]


class H017EventInsolvencyError(RuntimeError):
    """Raised when an H017 event interval drives account equity non-positive.

    This is a fail-closed validation state. The backtest should identify the
    interval that caused ruin instead of continuing until a later, less
    informative positive-equity validation fails during position sizing.
    """

    def __init__(
        self,
        *,
        decision_time: pd.Timestamp,
        entry_time: pd.Timestamp,
        forced_exit_time: pd.Timestamp,
        interval_start_equity_usd: float,
        interval_pnl_usd: float,
        ending_equity_usd: float,
        interval_fills: Sequence[Fill],
    ) -> None:
        self.decision_time = pd.Timestamp(decision_time)
        self.entry_time = pd.Timestamp(entry_time)
        self.forced_exit_time = pd.Timestamp(forced_exit_time)
        self.interval_start_equity_usd = float(interval_start_equity_usd)
        self.interval_pnl_usd = float(interval_pnl_usd)
        self.ending_equity_usd = float(ending_equity_usd)
        self.interval_fills = tuple(interval_fills)

        symbols = ", ".join(fill.symbol for fill in self.interval_fills) or "none"
        super().__init__(
            "H017 event backtest insolvency: "
            f"decision_time={self.decision_time}, "
            f"entry_time={self.entry_time}, "
            f"forced_exit_time={self.forced_exit_time}, "
            f"interval_start_equity_usd={self.interval_start_equity_usd:.2f}, "
            f"interval_pnl_usd={self.interval_pnl_usd:.2f}, "
            f"ending_equity_usd={self.ending_equity_usd:.2f}, "
            f"interval_fills={len(self.interval_fills)} [{symbols}]"
        )


def backtest_h017_event_driven(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    config: H017Config | None = None,
    starting_equity_usd: float = 10_000.0,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
) -> H017EventBacktestResult:
    """Run H017, then execute its positions with M1 intrabar simulation.

    This is the Phase 3 replacement path for the Phase 2.5 zero-cost return
    summation. Strategy decisions still come from ``run_h017``. Execution is now
    handled separately by the backtest package so that Phase 4 live trading can
    reuse the strategy layer without importing historical backtest machinery.
    """

    h017_result = run_h017(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=config,
    )

    return backtest_h017_event_from_result(
        h017_result=h017_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        starting_equity_usd=starting_equity_usd,
        slippage_atr_by_symbol=slippage_atr_by_symbol,
    )


def backtest_h017_event_from_result(
    *,
    h017_result: H017Result,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    starting_equity_usd: float = 10_000.0,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None = None,
) -> H017EventBacktestResult:
    """Execute an already-built H017 result with H4 timing and M1 fills.

    This function exists so tests can focus on execution mechanics without
    re-testing the H017 signal generator. The public ``backtest_h017_event_driven``
    wrapper still calls ``run_h017`` for real usage.

    Timing convention:
    - H017 decides at H4 close/open-label timestamp ``t``.
    - The trade opens on the next H4 bar open ``t+1``.
    - M1 bars inside ``[t+1, t+2)`` decide whether the stop is hit intrabar.
    - If no stop is hit, the segment closes at ``t+2`` open.

    The segment-close behavior is intentional for this bridge layer. H017's
    output is a per-bar target risk exposure, not a broker order ticket. Phase
    3.4 therefore treats each H4 interval as the executable account exposure
    implied by the prior H017 decision.
    """

    _validate_positive("starting_equity_usd", starting_equity_usd)

    h4_by_symbol = {
        "USDJPY": _validate_h4_frame("USDJPY", usdjpy_h4),
        "XAUUSD": _validate_h4_frame("XAUUSD", xauusd_h4),
    }
    m1_by_symbol = {
        "USDJPY": usdjpy_m1,
        "XAUUSD": xauusd_m1,
    }

    _validate_h017_panels(h017_result)

    index = _validate_decision_index(h017_result.positions.index)
    fills: list[Fill] = []
    current_equity = float(starting_equity_usd)

    if len(index) < 3:
        portfolio = build_portfolio_result(
            fills=(),
            starting_equity_usd=starting_equity_usd,
        )
        return H017EventBacktestResult(
            h017=h017_result,
            portfolio=portfolio,
            fills=(),
            n_bars=len(index),
            symbols=_SYMBOLS,
        )

    for i in range(1, len(index) - 1):
        decision_time = pd.Timestamp(index[i - 1])
        entry_time = pd.Timestamp(index[i])
        forced_exit_time = pd.Timestamp(index[i + 1])
        interval_start_equity = current_equity
        interval_pnl_usd = 0.0
        interval_fills: list[Fill] = []

        for symbol in _SYMBOLS:
            maybe_fill = _build_symbol_interval_fill(
                symbol=symbol,
                h017_result=h017_result,
                h4_bars=h4_by_symbol[symbol],
                m1_bars=m1_by_symbol[symbol],
                decision_time=decision_time,
                entry_time=entry_time,
                forced_exit_time=forced_exit_time,
                equity_usd=interval_start_equity,
                slippage_atr_by_symbol=slippage_atr_by_symbol,
            )

            if maybe_fill is None:
                continue

            fills.append(maybe_fill)
            interval_fills.append(maybe_fill)
            interval_pnl_usd += fill_pnl_usd(fill=maybe_fill)

        current_equity += interval_pnl_usd

        if current_equity <= 0.0:
            raise H017EventInsolvencyError(
                decision_time=decision_time,
                entry_time=entry_time,
                forced_exit_time=forced_exit_time,
                interval_start_equity_usd=interval_start_equity,
                interval_pnl_usd=interval_pnl_usd,
                ending_equity_usd=current_equity,
                interval_fills=interval_fills,
            )

    sorted_fills = tuple(sorted(fills, key=lambda fill: fill.exit_time_utc))
    portfolio = build_portfolio_result(
        fills=sorted_fills,
        starting_equity_usd=starting_equity_usd,
    )

    return H017EventBacktestResult(
        h017=h017_result,
        portfolio=portfolio,
        fills=sorted_fills,
        n_bars=len(index),
        symbols=_SYMBOLS,
    )


def _build_symbol_interval_fill(
    *,
    symbol: str,
    h017_result: H017Result,
    h4_bars: pd.DataFrame,
    m1_bars: pd.DataFrame,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    forced_exit_time: pd.Timestamp,
    equity_usd: float,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None,
) -> Fill | None:
    signed_risk_fraction = float(h017_result.positions.at[decision_time, symbol])

    if pd.isna(signed_risk_fraction) or signed_risk_fraction == 0.0:
        return None

    side = "buy" if signed_risk_fraction > 0.0 else "sell"
    stop_panel = h017_result.stops_long if side == "buy" else h017_result.stops_short
    stop_price = float(stop_panel.at[decision_time, symbol])

    if pd.isna(stop_price):
        return None

    entry_raw_price = float(h4_bars.at[entry_time, "open"])
    forced_exit_raw_price = float(h4_bars.at[forced_exit_time, "open"])
    stop_distance_price = abs(entry_raw_price - stop_price)

    if stop_distance_price <= 0.0:
        return None

    instrument_spec = get_default_instrument_spec(symbol)
    position_size = size_position_from_risk(
        symbol=symbol,
        signed_risk_fraction=signed_risk_fraction,
        equity_usd=equity_usd,
        entry_price=entry_raw_price,
        stop_distance_price=stop_distance_price,
        instrument_spec=instrument_spec,
    )

    if position_size.lots == 0.0:
        return None

    entry_cost = price_with_execution_costs(
        symbol=symbol,
        side=side,
        action="entry",
        raw_price=entry_raw_price,
        lots=position_size.lots,
    )

    raw_fill = simulate_bracket_trade(
        symbol=symbol,
        side=side,
        entry_time_utc=entry_time,
        entry_price=entry_cost.fill_price,
        lots=position_size.lots,
        m1_bars=m1_bars,
        stop_price=stop_price,
        take_profit_price=None,
        forced_exit_time_utc=forced_exit_time,
        forced_exit_price=forced_exit_raw_price,
        contract_size=instrument_spec.contract_size,
        commission=0.0,
        stop_slippage=0.0,
    )

    atr_for_slippage = _atr_for_slippage(
        symbol=symbol,
        decision_time=decision_time,
        stop_distance_price=stop_distance_price,
        slippage_atr_by_symbol=slippage_atr_by_symbol,
    )

    exit_cost = price_with_execution_costs(
        symbol=symbol,
        side=side,
        action="exit",
        raw_price=raw_fill.exit_price,
        lots=position_size.lots,
        exit_reason=raw_fill.exit_reason,
        atr=atr_for_slippage,
    )

    commission = entry_cost.commission_usd + exit_cost.commission_usd
    pnl_quote = _pnl_quote(
        side=side,
        entry_price=entry_cost.fill_price,
        exit_price=exit_cost.fill_price,
        lots=position_size.lots,
        contract_size=instrument_spec.contract_size,
    )

    return Fill(
        symbol=symbol,
        side=side,
        entry_time_utc=entry_time,
        entry_price=entry_cost.fill_price,
        exit_time_utc=raw_fill.exit_time_utc,
        exit_price=exit_cost.fill_price,
        lots=position_size.lots,
        pnl_quote=pnl_quote,
        commission=commission,
        slippage=exit_cost.slippage_price,
        exit_reason=raw_fill.exit_reason,
    )


def _validate_h017_panels(h017_result: H017Result) -> None:
    panels = {
        "positions": h017_result.positions,
        "stops_long": h017_result.stops_long,
        "stops_short": h017_result.stops_short,
    }

    for name, panel in panels.items():
        missing = [symbol for symbol in _SYMBOLS if symbol not in panel.columns]
        if missing:
            raise ValueError(f"{name} missing required symbols: {missing}")


def _validate_h4_frame(symbol: str, bars: pd.DataFrame) -> pd.DataFrame:
    missing = [column for column in _REQUIRED_H4_COLUMNS if column not in bars.columns]
    if missing:
        raise ValueError(f"{symbol} H4 bars missing required columns: {missing}")

    if not isinstance(bars.index, pd.DatetimeIndex):
        raise ValueError(f"{symbol} H4 bars must use a DatetimeIndex")

    if bars.index.tz is None:
        raise ValueError(f"{symbol} H4 bars index must be timezone-aware UTC")

    index_utc = bars.index.tz_convert("UTC")
    if not index_utc.is_monotonic_increasing:
        raise ValueError(f"{symbol} H4 bars index must be sorted ascending")

    if index_utc.has_duplicates:
        raise ValueError(f"{symbol} H4 bars index must not contain duplicates")

    canonical = bars.copy()
    canonical.index = index_utc
    return canonical


def _validate_decision_index(index: pd.Index) -> pd.DatetimeIndex:
    if not isinstance(index, pd.DatetimeIndex):
        raise ValueError("H017 positions must use a DatetimeIndex")

    if index.tz is None:
        raise ValueError("H017 positions index must be timezone-aware UTC")

    index_utc = index.tz_convert("UTC")
    if not index_utc.is_monotonic_increasing:
        raise ValueError("H017 positions index must be sorted ascending")

    if index_utc.has_duplicates:
        raise ValueError("H017 positions index must not contain duplicates")

    return index_utc


def _atr_for_slippage(
    *,
    symbol: str,
    decision_time: pd.Timestamp,
    stop_distance_price: float,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None,
) -> float | None:
    if slippage_atr_by_symbol is None:
        return stop_distance_price

    if symbol not in slippage_atr_by_symbol:
        return stop_distance_price

    atr_series = slippage_atr_by_symbol[symbol]
    if decision_time not in atr_series.index:
        return stop_distance_price

    atr = float(atr_series.at[decision_time])
    if pd.isna(atr) or atr <= 0.0:
        return stop_distance_price

    return atr


def _pnl_quote(
    *,
    side: str,
    entry_price: float,
    exit_price: float,
    lots: float,
    contract_size: float,
) -> float:
    direction = 1.0 if side == "buy" else -1.0
    return direction * (exit_price - entry_price) * lots * contract_size


def _validate_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0.0")
