from __future__ import annotations

import argparse
import importlib
import json
import math
from collections.abc import Iterable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor import (
    CANARY_RUNTIME_SYMBOL,
    CANARY_TICKET_IDENTIFIER,
    CANARY_VOLUME,
    H024_MAGIC,
    PACKET_TYPE as EXPOSURE_INVENTORY_PACKET_TYPE,
    USDJPY_RUNTIME_SYMBOL,
    collect_h024_runtime_exposure_inventory_safety_supervisor,
)
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
PACKET_TYPE = "H024_RUNTIME_ACCOUNT_RISK_MARGIN_SAFETY_SUPERVISOR"
SCHEMA_VERSION = 1

LOCKOUT_READER_MODULE = "quantcore.execution.h024_runtime_safety_lockout"
HEARTBEAT_MODULE = "quantcore.execution.h024_runtime_safety_heartbeat"
TICK_SPREAD_MODULE = "quantcore.execution.h024_runtime_tick_spread_safety_supervisor"
EXPOSURE_INVENTORY_MODULE = "quantcore.execution.h024_runtime_exposure_inventory_safety_supervisor"

DEFAULT_OUTPUT_PATH = Path("reports") / "h024_runtime_account_risk_margin_safety_supervisor.jsonl"

DEFAULT_THRESHOLDS: dict[str, float] = {
    "min_balance_usd": 0.0,
    "min_equity_usd": 0.0,
    "min_free_margin_usd": 0.0,
    "min_margin_level_percent_when_margin_used": 300.0,
    "max_total_margin_used_fraction": 0.50,
    "max_account_identity_diff_usd": 0.10,
    "max_canary_volume": CANARY_VOLUME,
    "max_h024_position_count": 1.0,
    "max_h024_order_count": 0.0,
}


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


def _coerce_int(value: Any) -> int | None:
    try:
        if value is None:
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


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


def _iterable_records(value: Any) -> list[Any] | None:
    if value is None:
        return None
    if isinstance(value, str | bytes | Mapping):
        return None
    if isinstance(value, Iterable):
        return list(value)
    return None


def _position_profit_sum(raw_positions: Any) -> tuple[float | None, str]:
    positions = _iterable_records(raw_positions)
    if positions is None:
        return None, "raw positions unavailable or not iterable"

    total = 0.0
    for position in positions:
        profit = _coerce_float(_field(position, "profit"))
        if profit is None:
            return None, "at least one position profit field is unavailable"
        total += profit
    return total, "all position profit fields available"


def collect_h024_runtime_account_risk_margin_safety_supervisor(
    *,
    mt5_client: Any | None = None,
    expected_server: str = EXPECTED_SERVER,
    expected_currency: str = EXPECTED_ACCOUNT_CURRENCY,
    thresholds: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Collect a read-only H024 account risk and margin safety supervisor packet.

    This packet reads account_info and consumes read-only upstream runtime
    safety packets. It never calls order_check, order_send, symbol_select,
    entry, close, modify, or any trading loop.
    """

    observed_at_utc = _utc_now_iso()
    threshold_map = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        threshold_map.update({str(key): float(value) for key, value in thresholds.items()})

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
                    "message": f"Account risk/margin supervisor check failed: {name}",
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
    tick_spread_record = collect_h024_runtime_tick_spread_safety_supervisor(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )
    exposure_inventory_record = collect_h024_runtime_exposure_inventory_safety_supervisor(
        mt5_client=mt5_client,
        expected_server=expected_server,
        expected_currency=expected_currency,
    )

    heartbeat_passed = heartbeat_record.get("verdict") == "PASS"
    tick_spread_passed = tick_spread_record.get("verdict") == "PASS"
    exposure_inventory_passed = exposure_inventory_record.get("verdict") == "PASS"

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
    add_check(
        "runtime_exposure_inventory_supervisor_passed",
        exposure_inventory_passed,
        {
            "exposure_inventory_packet_type": exposure_inventory_record.get("packet_type"),
            "exposure_inventory_verdict": exposure_inventory_record.get("verdict"),
            "exposure_inventory_operator_state": exposure_inventory_record.get("operator_state"),
            "exposure_inventory_violation_count": len(exposure_inventory_record.get("violations", [])),
        },
    )

    lockout_reference = _module_reference(LOCKOUT_READER_MODULE)
    heartbeat_reference = _module_reference(HEARTBEAT_MODULE)
    tick_spread_reference = _module_reference(TICK_SPREAD_MODULE)
    exposure_inventory_reference = _module_reference(EXPOSURE_INVENTORY_MODULE)

    add_check("runtime_lockout_reader_referenced", lockout_reference.get("module_importable") is True, lockout_reference)
    add_check("runtime_heartbeat_packet_referenced", heartbeat_reference.get("module_importable") is True, heartbeat_reference)
    add_check("runtime_tick_spread_packet_referenced", tick_spread_reference.get("module_importable") is True, tick_spread_reference)
    add_check(
        "runtime_exposure_inventory_packet_referenced",
        exposure_inventory_reference.get("module_importable") is True,
        exposure_inventory_reference,
    )

    account_info = None
    account_info_error = "not attempted"
    if mt5_client is not None:
        account_info, account_info_error = _safe_call(mt5_client, "account_info")

    account_plain = _plain(account_info)

    server = _field(account_info, "server")
    currency = _field(account_info, "currency")
    balance = _coerce_float(_field(account_info, "balance"))
    equity = _coerce_float(_field(account_info, "equity"))
    margin = _coerce_float(_field(account_info, "margin"))
    margin_free = _coerce_float(_field(account_info, "margin_free"))
    if margin_free is None:
        margin_free = _coerce_float(_field(account_info, "free_margin"))
    margin_level = _coerce_float(_field(account_info, "margin_level"))
    profit = _coerce_float(_field(account_info, "profit"))
    credit = _coerce_float(_field(account_info, "credit")) or 0.0

    add_check(
        "account_info_available",
        account_info is not None and account_info_error is None,
        {"error": account_info_error, "account": account_plain},
    )
    add_check(
        "account_server_expected",
        account_info is not None and server == expected_server,
        {"expected": expected_server, "observed": server},
    )
    add_check(
        "account_currency_expected",
        account_info is not None and currency == expected_currency,
        {"expected": expected_currency, "observed": currency},
    )
    add_check("balance_finite_and_non_negative", balance is not None and balance >= threshold_map["min_balance_usd"], {"balance": balance})
    add_check("equity_finite_and_non_negative", equity is not None and equity >= threshold_map["min_equity_usd"], {"equity": equity})
    add_check("margin_finite_and_non_negative", margin is not None and margin >= 0.0, {"margin": margin})
    add_check(
        "free_margin_finite_and_non_negative",
        margin_free is not None and margin_free >= threshold_map["min_free_margin_usd"],
        {"margin_free": margin_free},
    )

    margin_used_fraction = None
    if equity is not None and equity > 0 and margin is not None:
        margin_used_fraction = margin / equity

    add_check(
        "total_margin_used_fraction_bounded",
        margin_used_fraction is not None and margin_used_fraction <= threshold_map["max_total_margin_used_fraction"],
        {
            "margin": margin,
            "equity": equity,
            "margin_used_fraction": margin_used_fraction,
            "max_total_margin_used_fraction": threshold_map["max_total_margin_used_fraction"],
        },
    )

    free_margin_identity_diff = None
    if equity is not None and margin is not None and margin_free is not None:
        free_margin_identity_diff = abs(margin_free - (equity - margin))

    add_check(
        "free_margin_identity_consistent",
        free_margin_identity_diff is not None and free_margin_identity_diff <= threshold_map["max_account_identity_diff_usd"],
        {
            "equity": equity,
            "margin": margin,
            "margin_free": margin_free,
            "identity": "margin_free ~= equity - margin",
            "diff": free_margin_identity_diff,
            "max_diff_usd": threshold_map["max_account_identity_diff_usd"],
        },
    )

    profit_field_available = profit is not None
    add_check(
        "profit_finite_where_available",
        profit is None or math.isfinite(profit),
        {"profit": profit, "profit_field_available": profit_field_available},
    )

    equity_profit_identity_diff = None
    if balance is not None and equity is not None and profit is not None:
        equity_profit_identity_diff = abs(equity - (balance + credit + profit))

    add_check(
        "equity_balance_profit_identity_consistent_where_available",
        profit is None
        or (
            equity_profit_identity_diff is not None
            and equity_profit_identity_diff <= threshold_map["max_account_identity_diff_usd"]
        ),
        {
            "balance": balance,
            "credit": credit,
            "profit": profit,
            "equity": equity,
            "identity": "equity ~= balance + credit + profit",
            "diff": equity_profit_identity_diff,
            "max_diff_usd": threshold_map["max_account_identity_diff_usd"],
        },
    )

    raw_positions = None
    if isinstance(exposure_inventory_record.get("observed"), Mapping):
        raw_positions = exposure_inventory_record["observed"].get("raw_positions")
    position_profit_sum, position_profit_sum_status = _position_profit_sum(raw_positions)
    position_profit_diff = None
    if profit is not None and position_profit_sum is not None:
        position_profit_diff = abs(profit - position_profit_sum)

    add_check(
        "floating_pnl_consistent_with_positions_where_available",
        profit is None
        or position_profit_sum is None
        or (
            position_profit_diff is not None
            and position_profit_diff <= threshold_map["max_account_identity_diff_usd"]
        ),
        {
            "account_profit": profit,
            "position_profit_sum": position_profit_sum,
            "position_profit_sum_status": position_profit_sum_status,
            "diff": position_profit_diff,
            "max_diff_usd": threshold_map["max_account_identity_diff_usd"],
        },
    )

    margin_level_expected = None
    margin_level_diff = None
    margin_is_used = margin is not None and margin > 0.0
    if margin_is_used and equity is not None:
        margin_level_expected = (equity / margin) * 100.0
    if margin_level is not None and margin_level_expected is not None:
        margin_level_diff = abs(margin_level - margin_level_expected)

    add_check(
        "margin_level_sane_where_available",
        (
            margin_is_used
            and margin_level is not None
            and margin_level > 0.0
            and margin_level >= threshold_map["min_margin_level_percent_when_margin_used"]
        )
        or (
            not margin_is_used
            and (margin_level is None or margin_level >= 0.0)
        ),
        {
            "margin": margin,
            "equity": equity,
            "margin_level": margin_level,
            "min_margin_level_percent_when_margin_used": threshold_map["min_margin_level_percent_when_margin_used"],
        },
    )

    add_check(
        "margin_level_identity_consistent_where_available",
        (
            not margin_is_used
            or margin_level is None
            or margin_level_expected is None
            or margin_level_diff <= max(1.0, threshold_map["max_account_identity_diff_usd"] * 100.0)
        ),
        {
            "margin_level": margin_level,
            "expected_margin_level": margin_level_expected,
            "diff": margin_level_diff,
            "identity": "margin_level ~= equity / margin * 100 when margin is used",
        },
    )

    observed_exposure = exposure_inventory_record.get("observed", {})
    h024_position_count = None
    h024_order_count = None
    canary_state = None
    if isinstance(observed_exposure, Mapping):
        h024_position_count = _coerce_int(observed_exposure.get("h024_position_count"))
        h024_order_count = _coerce_int(observed_exposure.get("h024_order_count"))
        canary_state = observed_exposure.get("canary_state")

    h024_positions = exposure_inventory_record.get("h024_positions", [])
    canary_position = None
    if isinstance(h024_positions, list) and h024_positions:
        canary_position = h024_positions[0] if isinstance(h024_positions[0], Mapping) else None

    canary_volume = _coerce_float(canary_position.get("volume")) if isinstance(canary_position, Mapping) else 0.0
    canary_ticket = _coerce_int(canary_position.get("ticket")) if isinstance(canary_position, Mapping) else None
    canary_identifier = _coerce_int(canary_position.get("identifier")) if isinstance(canary_position, Mapping) else None
    canary_magic = _coerce_int(canary_position.get("magic")) if isinstance(canary_position, Mapping) else None
    canary_symbol = canary_position.get("runtime_symbol") if isinstance(canary_position, Mapping) else None

    add_check(
        "h024_position_count_bounded",
        h024_position_count is not None and h024_position_count <= int(threshold_map["max_h024_position_count"]),
        {"h024_position_count": h024_position_count, "max_h024_position_count": threshold_map["max_h024_position_count"]},
    )
    add_check(
        "h024_order_count_zero",
        h024_order_count is not None and h024_order_count == int(threshold_map["max_h024_order_count"]),
        {"h024_order_count": h024_order_count, "max_h024_order_count": threshold_map["max_h024_order_count"]},
    )
    add_check(
        "canary_state_allowed",
        canary_state in {"OBSERVED_EXACT_KNOWN_CANARY", "NOT_OBSERVED"},
        {"canary_state": canary_state},
    )
    add_check(
        "canary_exposure_volume_bounded",
        canary_volume is not None and canary_volume <= threshold_map["max_canary_volume"],
        {"canary_volume": canary_volume, "max_canary_volume": threshold_map["max_canary_volume"]},
    )
    add_check(
        "canary_identity_consistent_when_observed",
        canary_state != "OBSERVED_EXACT_KNOWN_CANARY"
        or (
            canary_symbol == CANARY_RUNTIME_SYMBOL
            and canary_magic == H024_MAGIC
            and canary_volume == CANARY_VOLUME
            and (
                canary_ticket == CANARY_TICKET_IDENTIFIER
                or canary_identifier == CANARY_TICKET_IDENTIFIER
            )
        ),
        {
            "canary_state": canary_state,
            "runtime_symbol": canary_symbol,
            "ticket": canary_ticket,
            "identifier": canary_identifier,
            "magic": canary_magic,
            "volume": canary_volume,
            "expected_runtime_symbol": CANARY_RUNTIME_SYMBOL,
            "expected_ticket_or_identifier": CANARY_TICKET_IDENTIFIER,
            "expected_magic": H024_MAGIC,
            "expected_volume": CANARY_VOLUME,
        },
    )
    add_check(
        "usdjpy_h024_exposure_absent",
        all(
            not isinstance(position, Mapping) or position.get("runtime_symbol") != USDJPY_RUNTIME_SYMBOL
            for position in (h024_positions if isinstance(h024_positions, list) else [])
        ),
        {"forbidden_runtime_symbol": USDJPY_RUNTIME_SYMBOL},
    )

    authorizations = _false_authorizations()
    authorization_violations = _authorization_violations(authorizations)
    violations.extend(authorization_violations)
    add_check("all_runtime_authorizations_false", not authorization_violations, authorizations)

    verdict = "PASS" if not violations else "FAIL"
    operator_state = (
        "ACCOUNT_RISK_MARGIN_OK_BUT_TRADING_NOT_AUTHORIZED"
        if verdict == "PASS"
        else "FAIL_CLOSED_ACCOUNT_RISK_MARGIN_BLOCKED"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "server": expected_server,
            "account_currency": expected_currency,
            "thresholds": _plain(threshold_map),
            "allowed_canary": {
                "runtime_symbol": CANARY_RUNTIME_SYMBOL,
                "ticket_or_identifier": CANARY_TICKET_IDENTIFIER,
                "magic": H024_MAGIC,
                "volume": CANARY_VOLUME,
            },
        },
        "upstream": {
            "heartbeat_record": _plain(heartbeat_record),
            "tick_spread_packet_type": TICK_SPREAD_PACKET_TYPE,
            "tick_spread_record": _plain(tick_spread_record),
            "exposure_inventory_packet_type": EXPOSURE_INVENTORY_PACKET_TYPE,
            "exposure_inventory_record": _plain(exposure_inventory_record),
            "lockout_reader_reference": lockout_reference,
            "heartbeat_reference": heartbeat_reference,
            "tick_spread_reference": tick_spread_reference,
            "exposure_inventory_reference": exposure_inventory_reference,
        },
        "observed": {
            "account_info_error": account_info_error,
            "account": account_plain,
            "server": server,
            "currency": currency,
            "balance": balance,
            "equity": equity,
            "credit": credit,
            "profit": profit,
            "margin": margin,
            "margin_free": margin_free,
            "margin_level": margin_level,
            "margin_used_fraction": margin_used_fraction,
            "free_margin_identity_diff": free_margin_identity_diff,
            "equity_profit_identity_diff": equity_profit_identity_diff,
            "position_profit_sum": position_profit_sum,
            "position_profit_sum_status": position_profit_sum_status,
            "position_profit_diff": position_profit_diff,
            "margin_level_expected": margin_level_expected,
            "margin_level_diff": margin_level_diff,
            "h024_position_count": h024_position_count,
            "h024_order_count": h024_order_count,
            "canary_state": canary_state,
            "canary_volume": canary_volume,
        },
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


def verify_h024_runtime_account_risk_margin_safety_supervisor_records(
    records: list[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    verification_violations: list[dict[str, Any]] = []

    if not records:
        verification_violations.append(
            {
                "code": "NO_RECORDS",
                "message": "No H024 account risk/margin safety supervisor records were found.",
                "fail_closed": True,
            }
        )

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_SCHEMA_VERSION",
                    "message": "Account risk/margin record has an unexpected schema version.",
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
                    "message": "Account risk/margin record has an unexpected strategy.",
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
                    "message": "Account risk/margin record has an unexpected packet type.",
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
                    "message": "Account risk/margin authorizations field is not an object.",
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
                    "message": "Account risk/margin supervisor must keep effective_new_entries_blocked true.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        upstream = record.get("upstream")
        if not isinstance(upstream, Mapping):
            verification_violations.append(
                {
                    "code": "UPSTREAM_NOT_OBJECT",
                    "message": "Account risk/margin upstream field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            heartbeat = upstream.get("heartbeat_record")
            tick_spread = upstream.get("tick_spread_record")
            exposure_inventory = upstream.get("exposure_inventory_record")

            if not isinstance(heartbeat, Mapping):
                verification_violations.append(
                    {
                        "code": "HEARTBEAT_RECORD_MISSING",
                        "message": "Account risk/margin supervisor must embed or consume a heartbeat record.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            elif require_pass and heartbeat.get("verdict") != "PASS":
                verification_violations.append(
                    {
                        "code": "HEARTBEAT_VERDICT_NOT_PASS",
                        "message": "Account risk/margin require-pass mode requires upstream heartbeat PASS.",
                        "record_index": index,
                        "observed": _plain(heartbeat.get("verdict")),
                        "fail_closed": True,
                    }
                )

            if not isinstance(tick_spread, Mapping):
                verification_violations.append(
                    {
                        "code": "TICK_SPREAD_RECORD_MISSING",
                        "message": "Account risk/margin supervisor must embed or consume a tick/spread record.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            elif tick_spread.get("packet_type") != TICK_SPREAD_PACKET_TYPE:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_TICK_SPREAD_PACKET_TYPE",
                        "message": "Account risk/margin supervisor references an unexpected tick/spread packet type.",
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
                        "message": "Account risk/margin require-pass mode requires upstream tick/spread PASS.",
                        "record_index": index,
                        "observed": _plain(tick_spread.get("verdict")),
                        "fail_closed": True,
                    }
                )

            if not isinstance(exposure_inventory, Mapping):
                verification_violations.append(
                    {
                        "code": "EXPOSURE_INVENTORY_RECORD_MISSING",
                        "message": "Account risk/margin supervisor must embed or consume an exposure/inventory record.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            elif exposure_inventory.get("packet_type") != EXPOSURE_INVENTORY_PACKET_TYPE:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_EXPOSURE_INVENTORY_PACKET_TYPE",
                        "message": "Account risk/margin supervisor references an unexpected exposure/inventory packet type.",
                        "record_index": index,
                        "observed": _plain(exposure_inventory.get("packet_type")),
                        "expected": EXPOSURE_INVENTORY_PACKET_TYPE,
                        "fail_closed": True,
                    }
                )
            elif require_pass and exposure_inventory.get("verdict") != "PASS":
                verification_violations.append(
                    {
                        "code": "EXPOSURE_INVENTORY_VERDICT_NOT_PASS",
                        "message": "Account risk/margin require-pass mode requires upstream exposure/inventory PASS.",
                        "record_index": index,
                        "observed": _plain(exposure_inventory.get("verdict")),
                        "fail_closed": True,
                    }
                )

        observed = record.get("observed")
        if not isinstance(observed, Mapping):
            verification_violations.append(
                {
                    "code": "OBSERVED_NOT_OBJECT",
                    "message": "Account risk/margin observed field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            if observed.get("currency") != EXPECTED_ACCOUNT_CURRENCY:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_ACCOUNT_CURRENCY",
                        "message": "Account risk/margin record observed an unexpected account currency.",
                        "record_index": index,
                        "observed": _plain(observed.get("currency")),
                        "expected": EXPECTED_ACCOUNT_CURRENCY,
                        "fail_closed": True,
                    }
                )
            if require_pass and observed.get("margin_used_fraction") is not None:
                margin_used_fraction = _coerce_float(observed.get("margin_used_fraction"))
                if margin_used_fraction is None or margin_used_fraction > DEFAULT_THRESHOLDS["max_total_margin_used_fraction"]:
                    verification_violations.append(
                        {
                            "code": "MARGIN_USED_FRACTION_UNSAFE",
                            "message": "Observed margin used fraction is missing or above threshold.",
                            "record_index": index,
                            "observed": _plain(observed.get("margin_used_fraction")),
                            "threshold": DEFAULT_THRESHOLDS["max_total_margin_used_fraction"],
                            "fail_closed": True,
                        }
                    )

        embedded_violations = record.get("violations", [])
        if record.get("verdict") == "PASS" and embedded_violations:
            verification_violations.append(
                {
                    "code": "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS",
                    "message": "Account risk/margin record verdict is PASS but embedded violations are present.",
                    "record_index": index,
                    "embedded_violation_count": len(embedded_violations),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("verdict") != "PASS":
            verification_violations.append(
                {
                    "code": "RECORD_VERDICT_NOT_PASS",
                    "message": "Account risk/margin record verdict is not PASS.",
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
    parser = argparse.ArgumentParser(description="Build or verify H024 runtime account risk/margin safety supervisor JSONL.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    return parser


__all__ = [
    "DEFAULT_OUTPUT_PATH",
    "DEFAULT_THRESHOLDS",
    "PACKET_TYPE",
    "SCHEMA_VERSION",
    "STRATEGY_ID",
    "collect_h024_runtime_account_risk_margin_safety_supervisor",
    "read_jsonl",
    "verify_h024_runtime_account_risk_margin_safety_supervisor_records",
    "write_jsonl",
]