"""One-shot H024 standard-demo canary execution path.

This module is execution-capable only when called by an explicit runner with a
terminal transport object. It is hard-locked for one standard-demo canary and is
designed to be unit-tested with fake transports.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Protocol

FINAL_AUDIT_SCHEMA_VERSION = "h024_final_pre_dispatch_audit_packet_v1"
FINAL_AUDIT_DECISION = "COMPLETE_FINAL_INERT_PRE_DISPATCH_AUDIT_FOR_ONE_DEMO_CANARY_NO_DISPATCH"

ACKNOWLEDGEMENT_TEXT = "I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER"
CANARY_COMMENT = "H024_ONE_SHOT_DEMO_CANARY"
CANARY_MAGIC = 240024
TRADE_RETCODE_CLIENT_DISABLES_AT = 10027


class CanaryExecutionRefusal(RuntimeError):
    """Raised when a hard control blocks canary execution."""


class TerminalTransport(Protocol):
    TRADE_ACTION_DEAL: int
    ORDER_TYPE_BUY: int
    ORDER_TYPE_SELL: int
    ORDER_TIME_GTC: int
    ORDER_FILLING_IOC: int
    TRADE_RETCODE_DONE: int
    ACCOUNT_TRADE_MODE_DEMO: int

    def account_info(self) -> Any: ...
    def symbol_info(self, symbol: str) -> Any: ...
    def symbol_info_tick(self, symbol: str) -> Any: ...
    def positions_get(self, symbol: str | None = None) -> Any: ...
    def orders_get(self, symbol: str | None = None) -> Any: ...
    def order_check(self, request: dict[str, Any]) -> Any: ...
    def order_send(self, request: dict[str, Any]) -> Any: ...


@dataclass(frozen=True)
class OneShotDemoCanaryConfig:
    allowed_demo_server: str = "Exness-MT5Trial6"
    account_currency: str = "USD"
    symbol: str = "XAUUSDm"
    side: str = "sell"
    volume: float = 0.01
    max_lot_cap: float = 0.01
    sl_distance_price: float = 89.027
    deviation_points: int = 50
    acknowledgement: str = ""
    send: bool = False


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_single_jsonl_record(path: Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if not isinstance(value, dict):
                raise CanaryExecutionRefusal(f"{path}:{line_number} is not a JSON object")
            records.append(value)
    if len(records) != 1:
        raise CanaryExecutionRefusal(f"expected exactly one JSONL record in {path}, found {len(records)}")
    return records[0]


def append_jsonl_record(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
        handle.write("\n")


def object_to_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "_asdict"):
        return dict(value._asdict())
    if isinstance(value, SimpleNamespace):
        return dict(vars(value))
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    return {"value": value}


def validate_final_audit_packet(record: dict[str, Any], config: OneShotDemoCanaryConfig) -> list[str]:
    violations: list[str] = []

    if record.get("schema_version") != FINAL_AUDIT_SCHEMA_VERSION:
        violations.append("unexpected_final_audit_schema_version")
    if record.get("decision") != FINAL_AUDIT_DECISION:
        violations.append("unexpected_final_audit_decision")
    if record.get("verdict") != "PASS":
        violations.append("final_audit_verdict_not_pass")
    if record.get("pre_dispatch_audit_passed") is not True:
        violations.append("pre_dispatch_audit_not_passed")
    if record.get("allowed_demo_server") != config.allowed_demo_server:
        violations.append("allowed_demo_server_mismatch")
    if record.get("expected_runtime_symbol") != config.symbol:
        violations.append("expected_runtime_symbol_mismatch")
    if float(record.get("max_lot_cap", -1.0)) != float(config.max_lot_cap):
        violations.append("max_lot_cap_mismatch")

    authority = record.get("authority")
    if not isinstance(authority, dict):
        violations.append("authority_missing_or_not_mapping")
        authority = {}
    if authority.get("one_shot_execution_capable_demo_path_implementation_allowed") is not True:
        violations.append("one_shot_execution_path_not_allowed_by_final_audit")
    if authority.get("max_approved_canary_orders") != 1:
        violations.append("max_approved_canary_orders_not_one")
    if authority.get("live_order_placement_approved") is not False:
        violations.append("live_order_placement_approved_not_false")

    controls = record.get("verified_controls")
    if not isinstance(controls, dict):
        violations.append("verified_controls_missing_or_not_mapping")
        controls = {}
    expected_controls: dict[str, Any] = {
        "allowed_demo_server_lock": config.allowed_demo_server,
        "account_currency_lock": config.account_currency,
        "account_context_lock": "standard_demo_only",
        "runtime_symbol_lock": config.symbol,
        "kill_switch_allow_state_required": True,
        "idempotency_ledger_required": True,
        "single_canary_order_limit": 1,
        "max_lot_cap": float(config.max_lot_cap),
        "pre_dispatch_final_audit_required": True,
        "post_order_audit_required_if_later_approved": True,
        "live_order_forbidden": True,
    }
    for key, expected in expected_controls.items():
        if controls.get(key) != expected:
            violations.append(f"{key}_mismatch")

    return violations


def validate_config(config: OneShotDemoCanaryConfig) -> list[str]:
    violations: list[str] = []
    if config.allowed_demo_server != "Exness-MT5Trial6":
        violations.append("allowed_demo_server_must_remain_Exness_MT5Trial6")
    if config.account_currency != "USD":
        violations.append("account_currency_must_remain_USD")
    if config.symbol != "XAUUSDm":
        violations.append("symbol_must_remain_XAUUSDm")
    if config.side not in {"buy", "sell"}:
        violations.append("side_must_be_buy_or_sell")
    if float(config.volume) <= 0:
        violations.append("volume_must_be_positive")
    if float(config.volume) > float(config.max_lot_cap):
        violations.append("volume_exceeds_max_lot_cap")
    if float(config.max_lot_cap) != 0.01:
        violations.append("max_lot_cap_must_remain_0_01")
    if float(config.sl_distance_price) != 89.027:
        violations.append("sl_distance_price_must_remain_89_027")
    if int(config.deviation_points) < 0:
        violations.append("deviation_points_must_not_be_negative")
    if config.send and config.acknowledgement != ACKNOWLEDGEMENT_TEXT:
        violations.append("exact_acknowledgement_required_for_send")
    return violations


def load_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if not isinstance(value, dict):
                raise CanaryExecutionRefusal(f"{path}:{line_number} is not a JSON object")
            records.append(value)
    return records


def _ledger_record_is_known_no_fill_refusal(record: dict[str, Any]) -> bool:
    send_result = record.get("order_send_result")
    if not isinstance(send_result, dict):
        return False
    return send_result.get("retcode") == TRADE_RETCODE_CLIENT_DISABLES_AT


def ensure_no_prior_canary(ledger_path: Path, config: OneShotDemoCanaryConfig) -> None:
    for record in load_ledger(ledger_path):
        if not (
            record.get("strategy") == "H024"
            and record.get("canary_comment") == CANARY_COMMENT
            and record.get("symbol") == config.symbol
            and record.get("allowed_demo_server") == config.allowed_demo_server
        ):
            continue

        stage = record.get("attempt_stage")
        if stage == "send_succeeded":
            raise CanaryExecutionRefusal("idempotency_ledger_already_contains_prior_successful_canary")

        if stage in {"send_refused_no_fill_client_autotrading_disabled", "send_attempted"}:
            if _ledger_record_is_known_no_fill_refusal(record):
                continue
            raise CanaryExecutionRefusal("idempotency_ledger_contains_prior_unknown_send_attempt")

        if stage in {"sent", "send_attempted_unknown_result", "order_check_failed"}:
            raise CanaryExecutionRefusal("idempotency_ledger_contains_prior_blocking_attempt")


def validate_terminal_environment(terminal: TerminalTransport, config: OneShotDemoCanaryConfig) -> list[str]:
    violations: list[str] = []

    account = terminal.account_info()
    account_dict = object_to_dict(account)
    if not account_dict:
        violations.append("account_info_unavailable")
        return violations

    if account_dict.get("server") != config.allowed_demo_server:
        violations.append("terminal_server_mismatch")
    if account_dict.get("currency") != config.account_currency:
        violations.append("terminal_account_currency_mismatch")

    demo_constant = getattr(terminal, "ACCOUNT_TRADE_MODE_DEMO", None)
    trade_mode = account_dict.get("trade_mode")
    if demo_constant is not None and trade_mode is not None and trade_mode != demo_constant:
        violations.append("terminal_account_is_not_demo_trade_mode")

    symbol_info = terminal.symbol_info(config.symbol)
    symbol_dict = object_to_dict(symbol_info)
    if not symbol_dict:
        violations.append("symbol_info_unavailable")
        return violations
    if symbol_dict.get("visible") is False:
        violations.append("symbol_not_visible_manual_market_watch_enable_required")

    min_volume = symbol_dict.get("volume_min")
    max_volume = symbol_dict.get("volume_max")
    step = symbol_dict.get("volume_step")
    if min_volume is not None and float(config.volume) < float(min_volume):
        violations.append("volume_below_symbol_minimum")
    if max_volume is not None and float(config.volume) > float(max_volume):
        violations.append("volume_above_symbol_maximum")
    if step not in (None, 0):
        scaled = round(float(config.volume) / float(step))
        if abs((scaled * float(step)) - float(config.volume)) > 1e-9:
            violations.append("volume_not_aligned_to_symbol_step")

    positions = terminal.positions_get(symbol=config.symbol)
    if positions not in (None, (), []):
        violations.append("existing_symbol_position_blocks_one_shot_canary")
    orders = terminal.orders_get(symbol=config.symbol)
    if orders not in (None, (), []):
        violations.append("existing_symbol_pending_order_blocks_one_shot_canary")

    tick = terminal.symbol_info_tick(config.symbol)
    tick_dict = object_to_dict(tick)
    if not tick_dict:
        violations.append("symbol_tick_unavailable")
    elif float(tick_dict.get("bid", 0.0) or 0.0) <= 0 or float(tick_dict.get("ask", 0.0) or 0.0) <= 0:
        violations.append("symbol_tick_bid_ask_invalid")

    return violations


def build_market_canary_request(terminal: TerminalTransport, config: OneShotDemoCanaryConfig) -> dict[str, Any]:
    tick = object_to_dict(terminal.symbol_info_tick(config.symbol))
    bid = float(tick.get("bid", 0.0) or 0.0)
    ask = float(tick.get("ask", 0.0) or 0.0)
    if bid <= 0 or ask <= 0:
        raise CanaryExecutionRefusal("cannot_build_request_without_valid_bid_ask")

    if config.side == "sell":
        order_type = terminal.ORDER_TYPE_SELL
        price = bid
        stop_loss = price + float(config.sl_distance_price)
    elif config.side == "buy":
        order_type = terminal.ORDER_TYPE_BUY
        price = ask
        stop_loss = price - float(config.sl_distance_price)
    else:
        raise CanaryExecutionRefusal("side_must_be_buy_or_sell")

    return {
        "action": terminal.TRADE_ACTION_DEAL,
        "symbol": config.symbol,
        "volume": float(config.volume),
        "type": order_type,
        "price": price,
        "sl": stop_loss,
        "deviation": int(config.deviation_points),
        "magic": CANARY_MAGIC,
        "comment": CANARY_COMMENT,
        "type_time": terminal.ORDER_TIME_GTC,
        "type_filling": terminal.ORDER_FILLING_IOC,
    }


def execute_one_shot_demo_canary(
    *,
    terminal: TerminalTransport,
    final_audit_packet: dict[str, Any],
    ledger_path: Path,
    config: OneShotDemoCanaryConfig,
) -> dict[str, Any]:
    violations: list[str] = []
    violations.extend(validate_config(config))
    violations.extend(validate_final_audit_packet(final_audit_packet, config))
    if violations:
        raise CanaryExecutionRefusal(";".join(violations))

    ensure_no_prior_canary(ledger_path, config)

    env_violations = validate_terminal_environment(terminal, config)
    if env_violations:
        raise CanaryExecutionRefusal(";".join(env_violations))

    request = build_market_canary_request(terminal, config)

    if not config.send:
        return {
            "strategy": "H024",
            "attempt_stage": "request_built_dry_run_no_send",
            "canary_comment": CANARY_COMMENT,
            "allowed_demo_server": config.allowed_demo_server,
            "symbol": config.symbol,
            "request": request,
            "generated_at_utc": utc_now_iso(),
        }

    check_result = terminal.order_check(request)
    check_dict = object_to_dict(check_result)
    check_retcode = check_dict.get("retcode")
    acceptable_check_retcodes = {0, getattr(terminal, "TRADE_RETCODE_DONE", None)}
    if check_retcode not in acceptable_check_retcodes:
        record = {
            "strategy": "H024",
            "attempt_stage": "order_check_failed",
            "canary_comment": CANARY_COMMENT,
            "allowed_demo_server": config.allowed_demo_server,
            "symbol": config.symbol,
            "request": request,
            "order_check_result": check_dict,
            "generated_at_utc": utc_now_iso(),
        }
        append_jsonl_record(ledger_path, record)
        raise CanaryExecutionRefusal(f"order_check_failed_retcode_{check_retcode}")

    send_result = terminal.order_send(request)
    send_dict = object_to_dict(send_result)
    send_retcode = send_dict.get("retcode")

    if send_retcode == getattr(terminal, "TRADE_RETCODE_DONE", None):
        record = {
            "strategy": "H024",
            "attempt_stage": "send_succeeded",
            "canary_comment": CANARY_COMMENT,
            "allowed_demo_server": config.allowed_demo_server,
            "symbol": config.symbol,
            "request": request,
            "order_check_result": check_dict,
            "order_send_result": send_dict,
            "generated_at_utc": utc_now_iso(),
        }
        append_jsonl_record(ledger_path, record)
        return record

    if send_retcode == TRADE_RETCODE_CLIENT_DISABLES_AT:
        record = {
            "strategy": "H024",
            "attempt_stage": "send_refused_no_fill_client_autotrading_disabled",
            "canary_comment": CANARY_COMMENT,
            "allowed_demo_server": config.allowed_demo_server,
            "symbol": config.symbol,
            "request": request,
            "order_check_result": check_dict,
            "order_send_result": send_dict,
            "generated_at_utc": utc_now_iso(),
        }
        append_jsonl_record(ledger_path, record)
        raise CanaryExecutionRefusal("order_send_failed_retcode_10027_client_autotrading_disabled_no_fill")

    record = {
        "strategy": "H024",
        "attempt_stage": "send_attempted_unknown_result",
        "canary_comment": CANARY_COMMENT,
        "allowed_demo_server": config.allowed_demo_server,
        "symbol": config.symbol,
        "request": request,
        "order_check_result": check_dict,
        "order_send_result": send_dict,
        "generated_at_utc": utc_now_iso(),
    }
    append_jsonl_record(ledger_path, record)
    raise CanaryExecutionRefusal(f"order_send_failed_retcode_{send_retcode}")


__all__ = [
    "ACKNOWLEDGEMENT_TEXT",
    "CANARY_COMMENT",
    "CANARY_MAGIC",
    "CanaryExecutionRefusal",
    "OneShotDemoCanaryConfig",
    "append_jsonl_record",
    "build_market_canary_request",
    "execute_one_shot_demo_canary",
    "read_single_jsonl_record",
    "validate_config",
    "validate_final_audit_packet",
    "validate_terminal_environment",
]