from __future__ import annotations

import argparse
import importlib
import json
import math
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
    collect_h024_runtime_safety_heartbeat,
)
from quantcore.execution.h024_runtime_tick_spread_safety_supervisor import (
    PACKET_TYPE as TICK_SPREAD_PACKET_TYPE,
    collect_h024_runtime_tick_spread_safety_supervisor,
)

STRATEGY_ID = "H024"
PACKET_TYPE = "H024_RUNTIME_EXPOSURE_INVENTORY_SAFETY_SUPERVISOR"
SCHEMA_VERSION = 1

H024_MAGIC = 240024
CANARY_RUNTIME_SYMBOL = "XAUUSDm"
CANARY_MODEL_SYMBOL = "XAUUSD"
CANARY_TICKET_IDENTIFIER = 4413054432
CANARY_VOLUME = 0.01
CANARY_SIDE = "sell"
CANARY_POSITION_TYPE = 1

USDJPY_RUNTIME_SYMBOL = "USDJPYm"
USDJPY_MODEL_SYMBOL = "USDJPY"

LOCKOUT_READER_MODULE = "quantcore.execution.h024_runtime_safety_lockout"
HEARTBEAT_MODULE = "quantcore.execution.h024_runtime_safety_heartbeat"
TICK_SPREAD_MODULE = "quantcore.execution.h024_runtime_tick_spread_safety_supervisor"

DEFAULT_OUTPUT_PATH = Path("reports") / "h024_runtime_exposure_inventory_safety_supervisor.jsonl"


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _plain(value: Any) -> Any:
    if value is None or isinstance(value, str | int | float | bool):
        if isinstance(value, float) and not math.isfinite(value):
            return repr(value)
        return value
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "_asdict"):
        return {str(k): _plain(v) for k, v in value._asdict().items()}
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_plain(v) for v in value]
    if hasattr(value, "__dict__"):
        return {str(k): _plain(v) for k, v in vars(value).items() if not str(k).startswith("_")}
    return repr(value)


def _field(value: Any, name: str) -> Any:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return value.get(name)
    return getattr(value, name, None)


def _coerce_int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _coerce_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        result = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(result):
        return None
    return result


def _false_authorizations() -> dict[str, bool]:
    return {key: False for key in FORBIDDEN_AUTHORIZATION_KEYS}


def _authorization_violations(authorizations: Mapping[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for key in FORBIDDEN_AUTHORIZATION_KEYS:
        if key not in authorizations:
            violations.append(
                {
                    "code": "MISSING_AUTHORIZATION_KEY",
                    "message": f"Required authorization key is missing: {key}",
                    "field": key,
                    "fail_closed": True,
                }
            )
        elif authorizations[key] is not False:
            violations.append(
                {
                    "code": "UNSAFE_AUTHORIZATION_TRUE",
                    "message": f"Forbidden runtime authorization is not false: {key}",
                    "field": key,
                    "observed": _plain(authorizations[key]),
                    "fail_closed": True,
                }
            )
    return violations


def _safe_call(client: Any, method_name: str, *args: Any) -> tuple[Any, str | None]:
    method = getattr(client, method_name, None)
    if method is None:
        return None, f"missing method: {method_name}"
    try:
        return method(*args), None
    except Exception as exc:  # pragma: no cover - defensive runtime boundary
        return None, repr(exc)


def _module_reference(module_name: str) -> dict[str, Any]:
    reference: dict[str, Any] = {
        "module": module_name,
        "module_importable": False,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
    }
    try:
        module = importlib.import_module(module_name)
        reference["module_importable"] = True
        reference["module_file"] = getattr(module, "__file__", None)
    except Exception as exc:
        reference["module_error"] = repr(exc)
    return reference


def _is_h024_inventory(item: Any) -> bool:
    magic = _coerce_int(_field(item, "magic"))
    comment = str(_field(item, "comment") or "")
    ticket = _coerce_int(_field(item, "ticket"))
    identifier = _coerce_int(_field(item, "identifier"))
    return (
        magic == H024_MAGIC
        or "H024" in comment.upper()
        or ticket == CANARY_TICKET_IDENTIFIER
        or identifier == CANARY_TICKET_IDENTIFIER
    )


def _iterable_records(value: Any) -> list[Any] | None:
    if value is None:
        return None
    if isinstance(value, str | bytes | Mapping):
        return None
    if isinstance(value, Iterable):
        return list(value)
    return None


def _position_model_symbol(runtime_symbol: str | None) -> str | None:
    if runtime_symbol == CANARY_RUNTIME_SYMBOL:
        return CANARY_MODEL_SYMBOL
    if runtime_symbol == USDJPY_RUNTIME_SYMBOL:
        return USDJPY_MODEL_SYMBOL
    return None


def _order_volume(order: Any) -> float | None:
    for field_name in ("volume_current", "volume_initial", "volume"):
        volume = _coerce_float(_field(order, field_name))
        if volume is not None:
            return volume
    return None


def _evaluate_h024_position(position: Any) -> dict[str, Any]:
    runtime_symbol = str(_field(position, "symbol") or "")
    model_symbol = _position_model_symbol(runtime_symbol)
    ticket = _coerce_int(_field(position, "ticket"))
    identifier = _coerce_int(_field(position, "identifier"))
    magic = _coerce_int(_field(position, "magic"))
    volume = _coerce_float(_field(position, "volume"))
    position_type = _coerce_int(_field(position, "type"))

    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "passed": bool(passed),
                "detail": _plain(detail),
                "fail_closed_on_failure": True,
            }
        )
        if not passed:
            violations.append(
                {
                    "code": name.upper(),
                    "message": f"H024 position inventory check failed: {name}",
                    "runtime_symbol": runtime_symbol,
                    "ticket": ticket,
                    "identifier": identifier,
                    "fail_closed": True,
                    "detail": _plain(detail),
                }
            )

    add_check(
        "position_symbol_mapping_known",
        model_symbol in {CANARY_MODEL_SYMBOL, USDJPY_MODEL_SYMBOL},
        {"runtime_symbol": runtime_symbol, "model_symbol": model_symbol},
    )

    add_check(
        "position_not_usdjpy_h024",
        runtime_symbol != USDJPY_RUNTIME_SYMBOL and model_symbol != USDJPY_MODEL_SYMBOL,
        {"runtime_symbol": runtime_symbol, "model_symbol": model_symbol},
    )

    is_exact_canary = (
        runtime_symbol == CANARY_RUNTIME_SYMBOL
        and model_symbol == CANARY_MODEL_SYMBOL
        and magic == H024_MAGIC
        and volume == CANARY_VOLUME
        and position_type == CANARY_POSITION_TYPE
        and (
            ticket == CANARY_TICKET_IDENTIFIER
            or identifier == CANARY_TICKET_IDENTIFIER
        )
        and ticket in {None, CANARY_TICKET_IDENTIFIER}
        and identifier in {None, CANARY_TICKET_IDENTIFIER}
    )

    add_check(
        "xauusd_h024_position_is_exact_known_canary_if_present",
        is_exact_canary,
        {
            "expected_runtime_symbol": CANARY_RUNTIME_SYMBOL,
            "expected_model_symbol": CANARY_MODEL_SYMBOL,
            "expected_ticket_or_identifier": CANARY_TICKET_IDENTIFIER,
            "expected_magic": H024_MAGIC,
            "expected_volume": CANARY_VOLUME,
            "expected_position_type": CANARY_POSITION_TYPE,
            "observed_ticket": ticket,
            "observed_identifier": identifier,
            "observed_magic": magic,
            "observed_volume": volume,
            "observed_position_type": position_type,
        },
    )

    return {
        "kind": "position",
        "runtime_symbol": runtime_symbol,
        "model_symbol": model_symbol,
        "ticket": ticket,
        "identifier": identifier,
        "magic": magic,
        "volume": volume,
        "position_type": position_type,
        "side": CANARY_SIDE if position_type == CANARY_POSITION_TYPE else None,
        "raw": _plain(position),
        "checks": checks,
        "violations": violations,
        "verdict": "PASS" if not violations else "FAIL",
    }


def _evaluate_h024_order(order: Any) -> dict[str, Any]:
    runtime_symbol = str(_field(order, "symbol") or "")
    model_symbol = _position_model_symbol(runtime_symbol)
    ticket = _coerce_int(_field(order, "ticket"))
    magic = _coerce_int(_field(order, "magic"))
    volume = _order_volume(order)
    order_type = _coerce_int(_field(order, "type"))

    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "passed": bool(passed),
                "detail": _plain(detail),
                "fail_closed_on_failure": True,
            }
        )
        if not passed:
            violations.append(
                {
                    "code": name.upper(),
                    "message": f"H024 order inventory check failed: {name}",
                    "runtime_symbol": runtime_symbol,
                    "ticket": ticket,
                    "fail_closed": True,
                    "detail": _plain(detail),
                }
            )

    add_check(
        "h024_orders_absent",
        False,
        {
            "reason": "No H024 pending/open orders are authorized by this supervisor.",
            "runtime_symbol": runtime_symbol,
            "model_symbol": model_symbol,
            "ticket": ticket,
            "magic": magic,
            "volume": volume,
            "order_type": order_type,
        },
    )

    add_check(
        "order_not_usdjpy_h024",
        runtime_symbol != USDJPY_RUNTIME_SYMBOL and model_symbol != USDJPY_MODEL_SYMBOL,
        {"runtime_symbol": runtime_symbol, "model_symbol": model_symbol},
    )

    return {
        "kind": "order",
        "runtime_symbol": runtime_symbol,
        "model_symbol": model_symbol,
        "ticket": ticket,
        "identifier": _coerce_int(_field(order, "identifier")),
        "magic": magic,
        "volume": volume,
        "order_type": order_type,
        "raw": _plain(order),
        "checks": checks,
        "violations": violations,
        "verdict": "FAIL",
    }


def collect_h024_runtime_exposure_inventory_safety_supervisor(
    *,
    mt5_client: Any | None = None,
    expected_server: str = EXPECTED_SERVER,
    expected_currency: str = EXPECTED_ACCOUNT_CURRENCY,
) -> dict[str, Any]:
    """Collect a read-only H024 exposure/inventory safety supervisor packet.

    This packet reads MT5 positions and orders. It never calls order_check,
    order_send, symbol_select, entry, close, modify, or a trading loop.
    """

    observed_at_utc = _utc_now_iso()
    checks: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []

    def add_check(name: str, passed: bool, detail: Any = None) -> None:
        checks.append(
            {
                "name": name,
                "status": "PASS" if passed else "FAIL",
                "passed": bool(passed),
                "detail": _plain(detail),
                "fail_closed_on_failure": True,
            }
        )
        if not passed:
            violations.append(
                {
                    "code": name.upper(),
                    "message": f"Exposure/inventory supervisor check failed: {name}",
                    "detail": _plain(detail),
                    "fail_closed": True,
                }
            )

    if mt5_client is None:
        try:
            mt5_client = importlib.import_module("MetaTrader5")
            add_check("mt5_module_importable", True, {"module": "MetaTrader5"})
        except Exception as exc:
            mt5_client = None
            add_check("mt5_module_importable", False, {"error": repr(exc)})
    else:
        add_check("mt5_client_injected", True, {"client_type": type(mt5_client).__name__})

    heartbeat_record = collect_h024_runtime_safety_heartbeat(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )
    heartbeat_passed = heartbeat_record.get("verdict") == "PASS"

    tick_spread_record = collect_h024_runtime_tick_spread_safety_supervisor(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )
    tick_spread_passed = tick_spread_record.get("verdict") == "PASS"

    add_check(
        "runtime_safety_heartbeat_passed",
        heartbeat_passed,
        {
            "heartbeat_verdict": heartbeat_record.get("verdict"),
            "heartbeat_operator_state": heartbeat_record.get("operator_state"),
            "heartbeat_violation_count": len(heartbeat_record.get("violations", [])),
        },
    )
    add_check(
        "runtime_tick_spread_supervisor_passed",
        tick_spread_passed,
        {
            "tick_spread_packet_type": tick_spread_record.get("packet_type"),
            "tick_spread_verdict": tick_spread_record.get("verdict"),
            "tick_spread_operator_state": tick_spread_record.get("operator_state"),
            "tick_spread_violation_count": len(tick_spread_record.get("violations", [])),
        },
    )

    lockout_reference = _module_reference(LOCKOUT_READER_MODULE)
    heartbeat_reference = _module_reference(HEARTBEAT_MODULE)
    tick_spread_reference = _module_reference(TICK_SPREAD_MODULE)

    add_check("runtime_lockout_reader_referenced", lockout_reference.get("module_importable") is True, lockout_reference)
    add_check("runtime_heartbeat_packet_referenced", heartbeat_reference.get("module_importable") is True, heartbeat_reference)
    add_check("runtime_tick_spread_packet_referenced", tick_spread_reference.get("module_importable") is True, tick_spread_reference)

    positions_raw = None
    positions_error = "not attempted"
    orders_raw = None
    orders_error = "not attempted"

    if mt5_client is not None and heartbeat_passed:
        positions_raw, positions_error = _safe_call(mt5_client, "positions_get")
        orders_raw, orders_error = _safe_call(mt5_client, "orders_get")

    positions = _iterable_records(positions_raw)
    orders = _iterable_records(orders_raw)

    add_check(
        "positions_get_available",
        positions is not None and positions_error is None,
        {"error": positions_error, "raw_type": type(positions_raw).__name__, "raw": _plain(positions_raw)},
    )
    add_check(
        "orders_get_available",
        orders is not None and orders_error is None,
        {"error": orders_error, "raw_type": type(orders_raw).__name__, "raw": _plain(orders_raw)},
    )

    h024_positions: list[dict[str, Any]] = []
    h024_orders: list[dict[str, Any]] = []

    if positions is not None:
        for position in positions:
            if _is_h024_inventory(position):
                evaluated_position = _evaluate_h024_position(position)
                h024_positions.append(evaluated_position)
                violations.extend(evaluated_position["violations"])

    if orders is not None:
        for order in orders:
            if _is_h024_inventory(order):
                evaluated_order = _evaluate_h024_order(order)
                h024_orders.append(evaluated_order)
                violations.extend(evaluated_order["violations"])

    canary_positions = [
        position
        for position in h024_positions
        if position.get("runtime_symbol") == CANARY_RUNTIME_SYMBOL
        and position.get("ticket") in {None, CANARY_TICKET_IDENTIFIER}
        and position.get("identifier") in {None, CANARY_TICKET_IDENTIFIER}
        and (
            position.get("ticket") == CANARY_TICKET_IDENTIFIER
            or position.get("identifier") == CANARY_TICKET_IDENTIFIER
        )
    ]

    add_check(
        "h024_position_count_allowed",
        len(h024_positions) <= 1,
        {"h024_position_count": len(h024_positions), "allowed_max": 1},
    )
    add_check(
        "h024_canary_position_count_allowed",
        len(canary_positions) <= 1,
        {"h024_canary_position_count": len(canary_positions), "allowed_max": 1},
    )
    add_check(
        "h024_orders_absent",
        len(h024_orders) == 0,
        {"h024_order_count": len(h024_orders), "allowed_max": 0},
    )
    if h024_orders:
        violations.append(
            {
                "code": "H024_ORDERS_PRESENT",
                "message": "No H024 pending/open orders are authorized.",
                "observed": len(h024_orders),
                "fail_closed": True,
            }
        )
    add_check(
        "usdjpy_h024_positions_absent",
        all(position.get("runtime_symbol") != USDJPY_RUNTIME_SYMBOL for position in h024_positions),
        {"runtime_symbol": USDJPY_RUNTIME_SYMBOL},
    )
    add_check(
        "usdjpy_h024_orders_absent",
        all(order.get("runtime_symbol") != USDJPY_RUNTIME_SYMBOL for order in h024_orders),
        {"runtime_symbol": USDJPY_RUNTIME_SYMBOL},
    )

    canary_state = "NOT_OBSERVED"
    if len(canary_positions) == 1:
        canary_state = "OBSERVED_EXACT_KNOWN_CANARY"
    elif h024_positions:
        canary_state = "UNEXPECTED_H024_POSITION_BLOCKED"

    authorizations = _false_authorizations()
    authorization_violations = _authorization_violations(authorizations)
    violations.extend(authorization_violations)
    add_check("all_runtime_authorizations_false", not authorization_violations, authorizations)

    verdict = "PASS" if not violations else "FAIL"
    operator_state = (
        "EXPOSURE_INVENTORY_OK_BUT_TRADING_NOT_AUTHORIZED"
        if verdict == "PASS"
        else "FAIL_CLOSED_EXPOSURE_INVENTORY_BLOCKED"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "server": expected_server,
            "account_currency": expected_currency,
            "allowed_canary": {
                "runtime_symbol": CANARY_RUNTIME_SYMBOL,
                "model_symbol": CANARY_MODEL_SYMBOL,
                "ticket_or_identifier": CANARY_TICKET_IDENTIFIER,
                "magic": H024_MAGIC,
                "volume": CANARY_VOLUME,
                "side": CANARY_SIDE,
                "position_type": CANARY_POSITION_TYPE,
            },
            "forbidden": {
                "usdjpy_runtime_symbol": USDJPY_RUNTIME_SYMBOL,
                "usdjpy_model_symbol": USDJPY_MODEL_SYMBOL,
                "h024_orders": "all",
                "unexpected_h024_positions": "all",
            },
        },
        "upstream": {
            "heartbeat_record": _plain(heartbeat_record),
            "tick_spread_packet_type": TICK_SPREAD_PACKET_TYPE,
            "tick_spread_record": _plain(tick_spread_record),
            "lockout_reader_reference": lockout_reference,
            "heartbeat_reference": heartbeat_reference,
            "tick_spread_reference": tick_spread_reference,
        },
        "observed": {
            "positions_get_error": positions_error,
            "orders_get_error": orders_error,
            "raw_positions": _plain(positions),
            "raw_orders": _plain(orders),
            "h024_position_count": len(h024_positions),
            "h024_order_count": len(h024_orders),
            "canary_state": canary_state,
        },
        "h024_positions": h024_positions,
        "h024_orders": h024_orders,
        "checks": checks,
        "authorizations": authorizations,
        "effective_new_entries_blocked": True,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "xauusd_order_authorized": False,
        "usdjpy_order_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
        "operator_state": operator_state,
        "violations": violations,
        "verdict": verdict,
    }


def verify_h024_runtime_exposure_inventory_safety_supervisor_records(
    records: list[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    verification_violations: list[dict[str, Any]] = []

    if not records:
        verification_violations.append(
            {
                "code": "NO_RECORDS",
                "message": "No H024 exposure/inventory safety supervisor records were found.",
                "fail_closed": True,
            }
        )

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_SCHEMA_VERSION",
                    "message": "Exposure/inventory record has an unexpected schema version.",
                    "record_index": index,
                    "observed": _plain(record.get("schema_version")),
                    "expected": SCHEMA_VERSION,
                    "fail_closed": True,
                }
            )

        if record.get("strategy") != STRATEGY_ID:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_STRATEGY",
                    "message": "Exposure/inventory record has an unexpected strategy.",
                    "record_index": index,
                    "observed": _plain(record.get("strategy")),
                    "expected": STRATEGY_ID,
                    "fail_closed": True,
                }
            )

        if record.get("packet_type") != PACKET_TYPE:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_PACKET_TYPE",
                    "message": "Exposure/inventory record has an unexpected packet type.",
                    "record_index": index,
                    "observed": _plain(record.get("packet_type")),
                    "expected": PACKET_TYPE,
                    "fail_closed": True,
                }
            )

        authorization_map = record.get("authorizations")
        if not isinstance(authorization_map, Mapping):
            verification_violations.append(
                {
                    "code": "AUTHORIZATIONS_NOT_OBJECT",
                    "message": "Exposure/inventory authorizations field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            for violation in _authorization_violations(authorization_map):
                violation["record_index"] = index
                verification_violations.append(violation)

        for key in FORBIDDEN_AUTHORIZATION_KEYS:
            if record.get(key) is not False:
                verification_violations.append(
                    {
                        "code": "TOP_LEVEL_UNSAFE_AUTHORIZATION",
                        "message": f"Top-level forbidden authorization is not false: {key}",
                        "record_index": index,
                        "field": key,
                        "observed": _plain(record.get(key)),
                        "fail_closed": True,
                    }
                )

        if record.get("effective_new_entries_blocked") is not True:
            verification_violations.append(
                {
                    "code": "NEW_ENTRIES_NOT_EFFECTIVELY_BLOCKED",
                    "message": "Exposure/inventory supervisor must keep effective_new_entries_blocked true.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        upstream = record.get("upstream")
        if not isinstance(upstream, Mapping):
            verification_violations.append(
                {
                    "code": "UPSTREAM_NOT_OBJECT",
                    "message": "Exposure/inventory upstream field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            heartbeat = upstream.get("heartbeat_record")
            tick_spread = upstream.get("tick_spread_record")
            if not isinstance(heartbeat, Mapping):
                verification_violations.append(
                    {
                        "code": "HEARTBEAT_RECORD_MISSING",
                        "message": "Exposure/inventory supervisor must embed or consume a heartbeat record.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            elif require_pass and heartbeat.get("verdict") != "PASS":
                verification_violations.append(
                    {
                        "code": "HEARTBEAT_VERDICT_NOT_PASS",
                        "message": "Exposure/inventory require-pass mode requires upstream heartbeat PASS.",
                        "record_index": index,
                        "observed": _plain(heartbeat.get("verdict")),
                        "fail_closed": True,
                    }
                )

            if not isinstance(tick_spread, Mapping):
                verification_violations.append(
                    {
                        "code": "TICK_SPREAD_RECORD_MISSING",
                        "message": "Exposure/inventory supervisor must embed or consume a tick/spread supervisor record.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            elif tick_spread.get("packet_type") != TICK_SPREAD_PACKET_TYPE:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_TICK_SPREAD_PACKET_TYPE",
                        "message": "Exposure/inventory supervisor references an unexpected tick/spread packet type.",
                        "record_index": index,
                        "observed": _plain(tick_spread.get("packet_type")),
                        "expected": TICK_SPREAD_PACKET_TYPE,
                        "fail_closed": True,
                    }
                )
            elif require_pass and tick_spread.get("verdict") != "PASS":
                verification_violations.append(
                    {
                        "code": "TICK_SPREAD_VERDICT_NOT_PASS",
                        "message": "Exposure/inventory require-pass mode requires upstream tick/spread PASS.",
                        "record_index": index,
                        "observed": _plain(tick_spread.get("verdict")),
                        "fail_closed": True,
                    }
                )

        h024_positions = record.get("h024_positions")
        h024_orders = record.get("h024_orders")

        if not isinstance(h024_positions, list):
            verification_violations.append(
                {
                    "code": "H024_POSITIONS_NOT_LIST",
                    "message": "h024_positions must be a list.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            if len(h024_positions) > 1:
                verification_violations.append(
                    {
                        "code": "TOO_MANY_H024_POSITIONS",
                        "message": "At most one H024 position is allowed: the exact known XAUUSDm canary.",
                        "record_index": index,
                        "observed": len(h024_positions),
                        "fail_closed": True,
                    }
                )
            for position_index, position in enumerate(h024_positions):
                if not isinstance(position, Mapping):
                    verification_violations.append(
                        {
                            "code": "H024_POSITION_NOT_OBJECT",
                            "message": "H024 position record is not an object.",
                            "record_index": index,
                            "position_index": position_index,
                            "fail_closed": True,
                        }
                    )
                    continue
                if require_pass and position.get("verdict") != "PASS":
                    verification_violations.append(
                        {
                            "code": "H024_POSITION_VERDICT_NOT_PASS",
                            "message": "Every observed H024 position must be the exact known canary.",
                            "record_index": index,
                            "position_index": position_index,
                            "observed": _plain(position.get("verdict")),
                            "fail_closed": True,
                        }
                    )
                if position.get("runtime_symbol") == USDJPY_RUNTIME_SYMBOL:
                    verification_violations.append(
                        {
                            "code": "USDJPY_H024_POSITION_PRESENT",
                            "message": "USDJPY H024 exposure is forbidden.",
                            "record_index": index,
                            "position_index": position_index,
                            "fail_closed": True,
                        }
                    )

        if not isinstance(h024_orders, list):
            verification_violations.append(
                {
                    "code": "H024_ORDERS_NOT_LIST",
                    "message": "h024_orders must be a list.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            if h024_orders:
                verification_violations.append(
                    {
                        "code": "H024_ORDERS_PRESENT",
                        "message": "No H024 pending/open orders are authorized.",
                        "record_index": index,
                        "observed": len(h024_orders),
                        "fail_closed": True,
                    }
                )
            for order_index, order in enumerate(h024_orders):
                if isinstance(order, Mapping) and order.get("runtime_symbol") == USDJPY_RUNTIME_SYMBOL:
                    verification_violations.append(
                        {
                            "code": "USDJPY_H024_ORDER_PRESENT",
                            "message": "USDJPY H024 orders are forbidden.",
                            "record_index": index,
                            "order_index": order_index,
                            "fail_closed": True,
                        }
                    )

        embedded_violations = record.get("violations", [])
        if record.get("verdict") == "PASS" and embedded_violations:
            verification_violations.append(
                {
                    "code": "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS",
                    "message": "Exposure/inventory record verdict is PASS but embedded violations are present.",
                    "record_index": index,
                    "embedded_violation_count": len(embedded_violations),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("verdict") != "PASS":
            verification_violations.append(
                {
                    "code": "RECORD_VERDICT_NOT_PASS",
                    "message": "Exposure/inventory record verdict is not PASS.",
                    "record_index": index,
                    "observed": _plain(record.get("verdict")),
                    "fail_closed": True,
                }
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": f"{PACKET_TYPE}_VERIFICATION",
        "record_count": len(records),
        "require_pass": require_pass,
        "verification_violations": verification_violations,
        "verifier_verdict": "PASS" if not verification_violations else "FAIL",
    }


def write_jsonl(path: str | Path, records: list[Mapping[str, Any]]) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Malformed JSONL at line {line_number}: {exc}") from exc
    return records


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or verify H024 runtime exposure/inventory safety supervisor JSONL.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    return parser


__all__ = [
    "CANARY_POSITION_TYPE",
    "CANARY_RUNTIME_SYMBOL",
    "CANARY_TICKET_IDENTIFIER",
    "CANARY_VOLUME",
    "DEFAULT_OUTPUT_PATH",
    "H024_MAGIC",
    "PACKET_TYPE",
    "SCHEMA_VERSION",
    "STRATEGY_ID",
    "USDJPY_RUNTIME_SYMBOL",
    "collect_h024_runtime_exposure_inventory_safety_supervisor",
    "read_jsonl",
    "verify_h024_runtime_exposure_inventory_safety_supervisor_records",
    "write_jsonl",
]