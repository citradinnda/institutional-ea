"""Log H024 MT5 terminal/account preflight facts.

Research-only terminal preflight.

This is not:
- demo approval,
- live approval,
- Phase 4 approval,
- EA execution approval.

The script reads MT5 terminal, account, and symbol metadata and writes a local
JSON report. It must not place, modify, close, or delete orders.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Protocol

DEFAULT_OUTPUT_PATH = (
    Path(__file__).resolve().parents[1] / "reports" / "h024_mt5_terminal_preflight.json"
)

BROKER_SYMBOLS_BY_MODEL: Mapping[str, str] = {
    "USDJPY": "USDJPYm",
    "XAUUSD": "XAUUSDm",
}

FORBIDDEN_MT5_CALL_NAMES: tuple[str, ...] = (
    "order_send",
    "order_check",
    "order_calc_margin",
    "order_calc_profit",
    "positions_get",
    "orders_get",
    "history_orders_get",
    "history_deals_get",
)


class Mt5Reader(Protocol):
    def initialize(self) -> bool: ...
    def shutdown(self) -> None: ...
    def last_error(self) -> object: ...
    def terminal_info(self) -> object: ...
    def account_info(self) -> object: ...
    def symbol_info(self, symbol: str) -> object: ...
    def symbol_select(self, symbol: str, enable: bool) -> bool: ...
    def symbol_info_tick(self, symbol: str) -> object: ...


class ForbiddenMt5CallError(RuntimeError):
    """Raised if preflight code tries to use forbidden MT5 functionality."""


class GuardedMt5Reader:
    """Proxy that permits read-only MT5 calls and blocks forbidden calls."""

    def __init__(self, mt5: Mt5Reader):
        self._mt5 = mt5
        self.forbidden_call_attempts: list[str] = []

    def __getattr__(self, name: str) -> object:
        if name in FORBIDDEN_MT5_CALL_NAMES:
            def _blocked(*_args: object, **_kwargs: object) -> object:
                self.forbidden_call_attempts.append(name)
                raise ForbiddenMt5CallError(f"forbidden MT5 call attempted: {name}")

            return _blocked
        return getattr(self._mt5, name)

    def initialize(self) -> bool:
        return bool(self._mt5.initialize())

    def shutdown(self) -> None:
        self._mt5.shutdown()

    def last_error(self) -> object:
        return self._mt5.last_error()

    def terminal_info(self) -> object:
        return self._mt5.terminal_info()

    def account_info(self) -> object:
        return self._mt5.account_info()

    def symbol_info(self, symbol: str) -> object:
        return self._mt5.symbol_info(symbol)

    def symbol_select(self, symbol: str, enable: bool) -> bool:
        return bool(self._mt5.symbol_select(symbol, enable))

    def symbol_info_tick(self, symbol: str) -> object:
        return self._mt5.symbol_info_tick(symbol)


@dataclass(frozen=True)
class SymbolPreflight:
    model_symbol: str
    broker_symbol: str
    visible_before_select: bool | None
    selected: bool
    visible_after_select: bool | None
    trade_mode: int | str | None
    execution_mode: int | str | None
    order_filling_modes: int | str | None
    order_modes: int | str | None
    volume_min: float | None
    volume_max: float | None
    volume_step: float | None
    stops_level_points: int | float | None
    freeze_level_points: int | float | None
    point: float | None
    digits: int | None
    spread: int | float | None
    spread_float: bool | None
    bid: float | None
    ask: float | None
    tick_time: int | None
    status: str
    reason: str


@dataclass(frozen=True)
class TerminalPreflightReport:
    generated_at_utc: str
    research_only: bool
    approval_boundary: str
    mt5_initialized: bool
    terminal: dict[str, Any]
    account: dict[str, Any]
    symbols: tuple[SymbolPreflight, ...]
    forbidden_calls_checked: tuple[str, ...]
    forbidden_call_attempts: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return (
            self.mt5_initialized
            and not self.forbidden_call_attempts
            and all(symbol.status == "ok" for symbol in self.symbols)
        )


def build_terminal_preflight_report(mt5: Mt5Reader) -> TerminalPreflightReport:
    """Read terminal/account/symbol facts without any order-send calls."""

    guarded = GuardedMt5Reader(mt5)

    initialized = bool(guarded.initialize())
    if not initialized:
        return TerminalPreflightReport(
            generated_at_utc=_utc_now_iso(),
            research_only=True,
            approval_boundary="No demo/live/Phase 4 approval.",
            mt5_initialized=False,
            terminal={"last_error": _safe_value(guarded.last_error())},
            account={},
            symbols=(),
            forbidden_calls_checked=FORBIDDEN_MT5_CALL_NAMES,
            forbidden_call_attempts=tuple(guarded.forbidden_call_attempts),
        )

    try:
        terminal = _object_to_dict(guarded.terminal_info())
        account = _object_to_dict(guarded.account_info())
        symbols = tuple(
            _read_symbol_preflight(
                mt5=guarded,
                model_symbol=model_symbol,
                broker_symbol=broker_symbol,
            )
            for model_symbol, broker_symbol in BROKER_SYMBOLS_BY_MODEL.items()
        )
        return TerminalPreflightReport(
            generated_at_utc=_utc_now_iso(),
            research_only=True,
            approval_boundary="No demo/live/Phase 4 approval.",
            mt5_initialized=True,
            terminal=terminal,
            account=account,
            symbols=symbols,
            forbidden_calls_checked=FORBIDDEN_MT5_CALL_NAMES,
            forbidden_call_attempts=tuple(guarded.forbidden_call_attempts),
        )
    finally:
        guarded.shutdown()


def write_terminal_preflight_report(report: TerminalPreflightReport, path: Path) -> None:
    """Write the terminal preflight report as JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(report)
    payload["passed"] = report.passed
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def format_terminal_preflight_report(report: TerminalPreflightReport, output_path: Path) -> str:
    """Format a compact terminal preflight summary."""

    lines = [
        "H024 MT5 terminal/account preflight",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        f"MT5 initialized: {report.mt5_initialized}",
        f"Forbidden MT5 call attempts: {len(report.forbidden_call_attempts)}",
        f"Symbols checked: {len(report.symbols)}",
    ]

    for symbol in report.symbols:
        lines.append(
            f"- {symbol.model_symbol} / {symbol.broker_symbol}: "
            f"{symbol.status} ({symbol.reason}) "
            f"bid={symbol.bid} ask={symbol.ask} spread={symbol.spread}"
        )

    lines.extend(
        [
            "",
            f"Wrote: {output_path}",
            f"Verdict: {'PASS' if report.passed else 'FAIL'}",
            "",
            "Safety boundary:",
            "- This script reads MT5 metadata only.",
            "- This script must not place, modify, close, or delete orders.",
            "- PASS does not approve demo trading, live trading, Phase 4, or EA execution.",
        ]
    )
    return "\n".join(lines)


def _read_symbol_preflight(
    *,
    mt5: Mt5Reader,
    model_symbol: str,
    broker_symbol: str,
) -> SymbolPreflight:
    before = mt5.symbol_info(broker_symbol)
    visible_before = _get_attr(before, "visible")

    selected = bool(mt5.symbol_select(broker_symbol, True))
    after = mt5.symbol_info(broker_symbol)
    tick = mt5.symbol_info_tick(broker_symbol)

    if after is None:
        return SymbolPreflight(
            model_symbol=model_symbol,
            broker_symbol=broker_symbol,
            visible_before_select=visible_before,
            selected=selected,
            visible_after_select=None,
            trade_mode=None,
            execution_mode=None,
            order_filling_modes=None,
            order_modes=None,
            volume_min=None,
            volume_max=None,
            volume_step=None,
            stops_level_points=None,
            freeze_level_points=None,
            point=None,
            digits=None,
            spread=None,
            spread_float=None,
            bid=None,
            ask=None,
            tick_time=None,
            status="fail",
            reason="symbol_info unavailable after select",
        )

    bid = _get_attr(tick, "bid")
    ask = _get_attr(tick, "ask")
    reason = "selected and tick available"
    status = "ok"

    if not selected:
        status = "fail"
        reason = "symbol_select failed"
    elif tick is None:
        status = "fail"
        reason = "symbol_info_tick unavailable"
    elif bid is None or ask is None or float(bid) <= 0.0 or float(ask) <= 0.0:
        status = "fail"
        reason = "invalid bid/ask"

    return SymbolPreflight(
        model_symbol=model_symbol,
        broker_symbol=broker_symbol,
        visible_before_select=visible_before,
        selected=selected,
        visible_after_select=_get_attr(after, "visible"),
        trade_mode=_get_attr(after, "trade_mode"),
        execution_mode=_get_attr(after, "trade_exemode"),
        order_filling_modes=_get_attr(after, "filling_mode"),
        order_modes=_get_attr(after, "order_mode"),
        volume_min=_get_attr(after, "volume_min"),
        volume_max=_get_attr(after, "volume_max"),
        volume_step=_get_attr(after, "volume_step"),
        stops_level_points=_get_attr(after, "trade_stops_level"),
        freeze_level_points=_get_attr(after, "trade_freeze_level"),
        point=_get_attr(after, "point"),
        digits=_get_attr(after, "digits"),
        spread=_get_attr(after, "spread"),
        spread_float=_get_attr(after, "spread_float"),
        bid=bid,
        ask=ask,
        tick_time=_get_attr(tick, "time"),
        status=status,
        reason=reason,
    )


def _object_to_dict(value: object) -> dict[str, Any]:
    if value is None:
        return {}
    if hasattr(value, "_asdict"):
        return {str(key): _safe_value(item) for key, item in value._asdict().items()}
    if isinstance(value, dict):
        return {str(key): _safe_value(item) for key, item in value.items()}
    if hasattr(value, "__dict__"):
        return {
            str(key): _safe_value(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return {"value": _safe_value(value)}


def _get_attr(value: object, name: str) -> Any:
    if value is None:
        return None
    if isinstance(value, dict):
        return _safe_value(value.get(name))
    return _safe_value(getattr(value, name, None))


def _safe_value(value: object) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, tuple):
        return tuple(_safe_value(item) for item in value)
    if isinstance(value, list):
        return [_safe_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _safe_value(item) for key, item in value.items()}
    return str(value)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_mt5() -> Mt5Reader:
    import MetaTrader5 as mt5  # type: ignore[import-not-found]

    return mt5


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path to write the MT5 terminal/account preflight JSON report.",
    )
    args = parser.parse_args()

    report = build_terminal_preflight_report(_load_mt5())
    write_terminal_preflight_report(report, args.output)
    print(format_terminal_preflight_report(report, args.output))

    if not report.passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
