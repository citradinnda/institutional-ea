from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

import pandas as pd

from quantcore.backtest.cost_model import get_default_cost_spec, price_with_execution_costs
from quantcore.backtest.fill_engine import Fill, simulate_bracket_trade
from quantcore.backtest.portfolio import (
    InstrumentSpec,
    PortfolioResult,
    PositionSize,
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


class H017EventInvalidStopError(RuntimeError):
    """Raised when H017 emits a stop with invalid directional geometry.

    The current H017 event bridge sizes from the raw H4 entry open. Under that
    explicit semantics, a long stop must be below the raw entry and a short
    stop must be above the raw entry. Failing closed here prevents absolute
    stop-distance sizing from hiding invalid stop geometry.
    """

    def __init__(
        self,
        *,
        symbol: str,
        side: str,
        decision_time: pd.Timestamp,
        entry_time: pd.Timestamp,
        entry_raw_price: float,
        stop_price: float,
    ) -> None:
        self.symbol = symbol
        self.side = side
        self.decision_time = pd.Timestamp(decision_time)
        self.entry_time = pd.Timestamp(entry_time)
        self.entry_raw_price = float(entry_raw_price)
        self.stop_price = float(stop_price)

        super().__init__(
            "H017 event invalid stop geometry: "
            f"symbol={self.symbol}, "
            f"side={self.side}, "
            f"decision_time={self.decision_time}, "
            f"entry_time={self.entry_time}, "
            f"entry_raw_price={self.entry_raw_price:.9f}, "
            f"stop_price={self.stop_price:.9f}"
        )



class H018MinimumStopDistanceError(RuntimeError):
    """Raised when H018 minimum raw-entry stop-distance policy is violated.

    H018 validation mode requires the raw-entry stop distance to be greater than
    or equal to one modeled spread for the symbol. Violations fail closed; they
    are not skipped, clipped, or treated as valid continuation.
    """

    def __init__(
        self,
        *,
        symbol: str,
        side: str,
        decision_time: pd.Timestamp,
        entry_time: pd.Timestamp,
        entry_raw_price: float,
        stop_price: float,
        raw_stop_distance: float,
        minimum_stop_distance: float,
    ) -> None:
        self.rule_name = "raw_stop_distance_at_least_one_modeled_spread"
        self.symbol = symbol
        self.side = side
        self.decision_time = pd.Timestamp(decision_time)
        self.entry_time = pd.Timestamp(entry_time)
        self.entry_raw_price = float(entry_raw_price)
        self.stop_price = float(stop_price)
        self.raw_stop_distance = float(raw_stop_distance)
        self.minimum_stop_distance = float(minimum_stop_distance)
        self.threshold_basis = "one_modeled_spread"
        self.validation_action = "fail_closed"

        super().__init__(
            "H018 minimum stop-distance violation: "
            f"rule_name={self.rule_name}, "
            f"symbol={self.symbol}, "
            f"side={self.side}, "
            f"decision_time={self.decision_time}, "
            f"entry_time={self.entry_time}, "
            f"entry_raw_price={self.entry_raw_price:.9f}, "
            f"stop_price={self.stop_price:.9f}, "
            f"raw_stop_distance={self.raw_stop_distance:.9f}, "
            f"minimum_stop_distance={self.minimum_stop_distance:.9f}, "
            f"threshold_basis={self.threshold_basis}, "
            f"validation_action={self.validation_action}"
        )


class H018MaximumPerTradeLeverageError(RuntimeError):
    """Raised when H018 maximum per-trade USD gross leverage policy is violated.

    H018 validation mode caps each trade's USD-converted gross notional exposure
    at 10.0 times account equity. Violations fail closed; they are not skipped,
    clipped, or treated as valid continuation.
    """

    def __init__(
        self,
        *,
        symbol: str,
        side: str,
        decision_time: pd.Timestamp,
        entry_time: pd.Timestamp,
        entry_raw_price: float,
        stop_price: float,
        raw_stop_distance: float,
        equity_usd: float,
        lots: float,
        contract_size: float,
        quote_currency: str,
        notional_quote: float,
        notional_usd: float,
        gross_leverage: float,
        maximum_gross_leverage: float,
    ) -> None:
        self.rule_name = "per_trade_usd_gross_leverage_at_or_below_10x_equity"
        self.symbol = symbol
        self.side = side
        self.decision_time = pd.Timestamp(decision_time)
        self.entry_time = pd.Timestamp(entry_time)
        self.entry_raw_price = float(entry_raw_price)
        self.stop_price = float(stop_price)
        self.raw_stop_distance = float(raw_stop_distance)
        self.equity_usd = float(equity_usd)
        self.lots = float(lots)
        self.contract_size = float(contract_size)
        self.quote_currency = quote_currency
        self.notional_quote = float(notional_quote)
        self.notional_usd = float(notional_usd)
        self.gross_leverage = float(gross_leverage)
        self.maximum_gross_leverage = float(maximum_gross_leverage)
        self.threshold_basis = "per_trade_usd_gross_notional_divided_by_equity"
        self.validation_action = "fail_closed"

        super().__init__(
            "H018 maximum per-trade leverage violation: "
            f"rule_name={self.rule_name}, "
            f"symbol={self.symbol}, "
            f"side={self.side}, "
            f"decision_time={self.decision_time}, "
            f"entry_time={self.entry_time}, "
            f"entry_raw_price={self.entry_raw_price:.9f}, "
            f"stop_price={self.stop_price:.9f}, "
            f"raw_stop_distance={self.raw_stop_distance:.9f}, "
            f"equity_usd={self.equity_usd:.2f}, "
            f"lots={self.lots:.2f}, "
            f"contract_size={self.contract_size:.9f}, "
            f"quote_currency={self.quote_currency}, "
            f"notional_quote={self.notional_quote:.9f}, "
            f"notional_usd={self.notional_usd:.9f}, "
            f"gross_leverage={self.gross_leverage:.9f}, "
            f"maximum_gross_leverage={self.maximum_gross_leverage:.9f}, "
            f"threshold_basis={self.threshold_basis}, "
            f"validation_action={self.validation_action}"
        )



class H018MaximumPortfolioGrossLeverageError(RuntimeError):
    """Raised when H018 portfolio-wide USD gross leverage policy is violated.

    H018 validation mode caps the sum of USD-converted gross notional exposure
    opened by all non-zero-lot candidate trades in one event interval at 10.0
    times interval-start account equity. Long and short notionals are summed
    gross; they are not netted.
    """

    def __init__(
        self,
        *,
        decision_time: pd.Timestamp,
        entry_time: pd.Timestamp,
        interval_start_equity_usd: float,
        symbols: Sequence[str],
        per_symbol_lots: Mapping[str, float],
        per_symbol_entry_raw_price: Mapping[str, float],
        per_symbol_notional_quote: Mapping[str, float],
        per_symbol_notional_usd: Mapping[str, float],
        portfolio_notional_usd: float,
        portfolio_gross_leverage: float,
        maximum_portfolio_gross_leverage: float,
    ) -> None:
        self.rule_name = "portfolio_usd_gross_leverage_at_or_below_10x_equity"
        self.decision_time = pd.Timestamp(decision_time)
        self.entry_time = pd.Timestamp(entry_time)
        self.interval_start_equity_usd = float(interval_start_equity_usd)
        self.symbols = tuple(symbols)
        self.per_symbol_lots = dict(per_symbol_lots)
        self.per_symbol_entry_raw_price = dict(per_symbol_entry_raw_price)
        self.per_symbol_notional_quote = dict(per_symbol_notional_quote)
        self.per_symbol_notional_usd = dict(per_symbol_notional_usd)
        self.portfolio_notional_usd = float(portfolio_notional_usd)
        self.portfolio_gross_leverage = float(portfolio_gross_leverage)
        self.maximum_portfolio_gross_leverage = float(maximum_portfolio_gross_leverage)
        self.threshold_basis = "portfolio_usd_gross_notional_divided_by_interval_start_equity"
        self.validation_action = "fail_closed"

        super().__init__(
            "H018 maximum portfolio gross leverage violation: "
            f"rule_name={self.rule_name}, "
            f"decision_time={self.decision_time}, "
            f"entry_time={self.entry_time}, "
            f"interval_start_equity_usd={self.interval_start_equity_usd:.2f}, "
            f"symbols={self.symbols}, "
            f"per_symbol_lots={self.per_symbol_lots}, "
            f"per_symbol_entry_raw_price={self.per_symbol_entry_raw_price}, "
            f"per_symbol_notional_quote={self.per_symbol_notional_quote}, "
            f"per_symbol_notional_usd={self.per_symbol_notional_usd}, "
            f"portfolio_notional_usd={self.portfolio_notional_usd:.9f}, "
            f"portfolio_gross_leverage={self.portfolio_gross_leverage:.9f}, "
            f"maximum_portfolio_gross_leverage={self.maximum_portfolio_gross_leverage:.9f}, "
            f"threshold_basis={self.threshold_basis}, "
            f"validation_action={self.validation_action}"
        )


@dataclass(frozen=True)
class _SymbolIntervalCandidate:
    symbol: str
    side: str
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    forced_exit_time: pd.Timestamp
    entry_raw_price: float
    forced_exit_raw_price: float
    stop_price: float
    raw_stop_distance: float
    instrument_spec: InstrumentSpec
    position_size: PositionSize
    notional_usd: float

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

        interval_candidates: list[_SymbolIntervalCandidate] = []

        for symbol in _SYMBOLS:
            maybe_candidate = _build_symbol_interval_candidate(
                symbol=symbol,
                h017_result=h017_result,
                h4_bars=h4_by_symbol[symbol],
                decision_time=decision_time,
                entry_time=entry_time,
                forced_exit_time=forced_exit_time,
                equity_usd=interval_start_equity,
            )

            if maybe_candidate is None:
                continue

            interval_candidates.append(maybe_candidate)

        _validate_maximum_portfolio_usd_gross_leverage(
            decision_time=decision_time,
            entry_time=entry_time,
            interval_start_equity_usd=interval_start_equity,
            candidates=interval_candidates,
        )

        for candidate in interval_candidates:
            fill = _build_symbol_interval_fill(
                candidate=candidate,
                m1_bars=m1_by_symbol[candidate.symbol],
                slippage_atr_by_symbol=slippage_atr_by_symbol,
            )

            fills.append(fill)
            interval_fills.append(fill)
            interval_pnl_usd += fill_pnl_usd(fill=fill)

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


def _build_symbol_interval_candidate(
    *,
    symbol: str,
    h017_result: H017Result,
    h4_bars: pd.DataFrame,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    forced_exit_time: pd.Timestamp,
    equity_usd: float,
) -> _SymbolIntervalCandidate | None:
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
    _validate_directional_stop(
        symbol=symbol,
        side=side,
        decision_time=decision_time,
        entry_time=entry_time,
        entry_raw_price=entry_raw_price,
        stop_price=stop_price,
    )
    stop_distance_price = abs(entry_raw_price - stop_price)
    _validate_minimum_stop_distance(
        symbol=symbol,
        side=side,
        decision_time=decision_time,
        entry_time=entry_time,
        entry_raw_price=entry_raw_price,
        stop_price=stop_price,
        raw_stop_distance=stop_distance_price,
    )

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

    _validate_maximum_per_trade_usd_gross_leverage(
        symbol=symbol,
        side=side,
        decision_time=decision_time,
        entry_time=entry_time,
        entry_raw_price=entry_raw_price,
        stop_price=stop_price,
        raw_stop_distance=stop_distance_price,
        equity_usd=equity_usd,
        position_size=position_size,
        instrument_spec=instrument_spec,
    )

    notional_usd = _position_notional_usd(
        symbol=symbol,
        entry_raw_price=entry_raw_price,
        position_size=position_size,
        instrument_spec=instrument_spec,
    )

    return _SymbolIntervalCandidate(
        symbol=symbol,
        side=side,
        decision_time=decision_time,
        entry_time=entry_time,
        forced_exit_time=forced_exit_time,
        entry_raw_price=entry_raw_price,
        forced_exit_raw_price=forced_exit_raw_price,
        stop_price=stop_price,
        raw_stop_distance=stop_distance_price,
        instrument_spec=instrument_spec,
        position_size=position_size,
        notional_usd=notional_usd,
    )


def _build_symbol_interval_fill(
    *,
    candidate: _SymbolIntervalCandidate,
    m1_bars: pd.DataFrame,
    slippage_atr_by_symbol: Mapping[str, pd.Series] | None,
) -> Fill:
    symbol = candidate.symbol
    side = candidate.side
    position_size = candidate.position_size
    instrument_spec = candidate.instrument_spec

    entry_cost = price_with_execution_costs(
        symbol=symbol,
        side=side,
        action="entry",
        raw_price=candidate.entry_raw_price,
        lots=position_size.lots,
    )

    raw_fill = simulate_bracket_trade(
        symbol=symbol,
        side=side,
        entry_time_utc=candidate.entry_time,
        entry_price=entry_cost.fill_price,
        lots=position_size.lots,
        m1_bars=m1_bars,
        stop_price=candidate.stop_price,
        take_profit_price=None,
        forced_exit_time_utc=candidate.forced_exit_time,
        forced_exit_price=candidate.forced_exit_raw_price,
        contract_size=instrument_spec.contract_size,
        commission=0.0,
        stop_slippage=0.0,
    )

    atr_for_slippage = _atr_for_slippage(
        symbol=symbol,
        decision_time=candidate.decision_time,
        stop_distance_price=candidate.raw_stop_distance,
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
        entry_time_utc=candidate.entry_time,
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


def _validate_directional_stop(
    *,
    symbol: str,
    side: str,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    entry_raw_price: float,
    stop_price: float,
) -> None:
    if side == "buy" and stop_price >= entry_raw_price:
        raise H017EventInvalidStopError(
            symbol=symbol,
            side=side,
            decision_time=decision_time,
            entry_time=entry_time,
            entry_raw_price=entry_raw_price,
            stop_price=stop_price,
        )

    if side == "sell" and stop_price <= entry_raw_price:
        raise H017EventInvalidStopError(
            symbol=symbol,
            side=side,
            decision_time=decision_time,
            entry_time=entry_time,
            entry_raw_price=entry_raw_price,
            stop_price=stop_price,
        )



def _validate_minimum_stop_distance(
    *,
    symbol: str,
    side: str,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    entry_raw_price: float,
    stop_price: float,
    raw_stop_distance: float,
) -> None:
    minimum_stop_distance = float(get_default_cost_spec(symbol).spread_price)

    if raw_stop_distance < minimum_stop_distance and not math.isclose(
        raw_stop_distance,
        minimum_stop_distance,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        raise H018MinimumStopDistanceError(
            symbol=symbol,
            side=side,
            decision_time=decision_time,
            entry_time=entry_time,
            entry_raw_price=entry_raw_price,
            stop_price=stop_price,
            raw_stop_distance=raw_stop_distance,
            minimum_stop_distance=minimum_stop_distance,
        )


_MAXIMUM_PER_TRADE_USD_GROSS_LEVERAGE = 10.0
_MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE = 10.0


def _position_notional_usd(
    *,
    symbol: str,
    entry_raw_price: float,
    position_size: PositionSize,
    instrument_spec: InstrumentSpec,
) -> float:
    if position_size.symbol.upper() != symbol.upper():
        raise ValueError("position_size symbol must match symbol")

    if instrument_spec.symbol.upper() != symbol.upper():
        raise ValueError("instrument_spec symbol must match symbol")

    quote_currency = instrument_spec.quote_currency.upper()

    if quote_currency == "USD":
        return float(position_size.notional_quote)

    if quote_currency == "JPY":
        if entry_raw_price <= 0.0:
            raise ValueError("entry_raw_price must be positive for JPY notional conversion")
        return float(position_size.notional_quote) / float(entry_raw_price)

    raise ValueError(f"unsupported quote currency {instrument_spec.quote_currency!r}")


def _validate_maximum_per_trade_usd_gross_leverage(
    *,
    symbol: str,
    side: str,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    entry_raw_price: float,
    stop_price: float,
    raw_stop_distance: float,
    equity_usd: float,
    position_size: PositionSize,
    instrument_spec: InstrumentSpec,
) -> None:
    if equity_usd <= 0.0:
        raise ValueError("equity_usd must be positive")

    notional_usd = _position_notional_usd(
        symbol=symbol,
        entry_raw_price=entry_raw_price,
        position_size=position_size,
        instrument_spec=instrument_spec,
    )
    gross_leverage = notional_usd / float(equity_usd)

    if gross_leverage > _MAXIMUM_PER_TRADE_USD_GROSS_LEVERAGE and not math.isclose(
        gross_leverage,
        _MAXIMUM_PER_TRADE_USD_GROSS_LEVERAGE,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        raise H018MaximumPerTradeLeverageError(
            symbol=symbol,
            side=side,
            decision_time=decision_time,
            entry_time=entry_time,
            entry_raw_price=entry_raw_price,
            stop_price=stop_price,
            raw_stop_distance=raw_stop_distance,
            equity_usd=equity_usd,
            lots=position_size.lots,
            contract_size=instrument_spec.contract_size,
            quote_currency=instrument_spec.quote_currency,
            notional_quote=position_size.notional_quote,
            notional_usd=notional_usd,
            gross_leverage=gross_leverage,
            maximum_gross_leverage=_MAXIMUM_PER_TRADE_USD_GROSS_LEVERAGE,
        )


def _validate_maximum_portfolio_usd_gross_leverage(
    *,
    decision_time: pd.Timestamp,
    entry_time: pd.Timestamp,
    interval_start_equity_usd: float,
    candidates: Sequence[_SymbolIntervalCandidate],
) -> None:
    if interval_start_equity_usd <= 0.0:
        raise ValueError("interval_start_equity_usd must be positive")

    if not candidates:
        return

    portfolio_notional_usd = sum(candidate.notional_usd for candidate in candidates)
    portfolio_gross_leverage = portfolio_notional_usd / float(interval_start_equity_usd)

    if portfolio_gross_leverage > _MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE and not math.isclose(
        portfolio_gross_leverage,
        _MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        raise H018MaximumPortfolioGrossLeverageError(
            decision_time=decision_time,
            entry_time=entry_time,
            interval_start_equity_usd=interval_start_equity_usd,
            symbols=tuple(candidate.symbol for candidate in candidates),
            per_symbol_lots={
                candidate.symbol: candidate.position_size.lots for candidate in candidates
            },
            per_symbol_entry_raw_price={
                candidate.symbol: candidate.entry_raw_price for candidate in candidates
            },
            per_symbol_notional_quote={
                candidate.symbol: candidate.position_size.notional_quote
                for candidate in candidates
            },
            per_symbol_notional_usd={
                candidate.symbol: candidate.notional_usd for candidate in candidates
            },
            portfolio_notional_usd=portfolio_notional_usd,
            portfolio_gross_leverage=portfolio_gross_leverage,
            maximum_portfolio_gross_leverage=_MAXIMUM_PORTFOLIO_USD_GROSS_LEVERAGE,
        )


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
