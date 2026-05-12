from __future__ import annotations

import argparse
import importlib
import json
import math
import time
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from quantcore.execution.h024_runtime_safety_heartbeat import (
    EXPECTED_ACCOUNT_CURRENCY,
    EXPECTED_SERVER,
    FORBIDDEN_AUTHORIZATION_KEYS,
    PACKET_TYPE as HEARTBEAT_PACKET_TYPE,
    collect_h024_runtime_safety_heartbeat,
)

STRATEGY_ID = "H024"
PACKET_TYPE = "H024_RUNTIME_TICK_SPREAD_SAFETY_SUPERVISOR"
SCHEMA_VERSION = 1

DEFAULT_SYMBOL_CONFIGS: dict[str, dict[str, Any]] = {
    "XAUUSDm": {
        "model_symbol": "XAUUSD",
        "max_spread_points": 5000.0,
        "max_tick_age_seconds": 3600.0,
    },
    "USDJPYm": {
        "model_symbol": "USDJPY",
        "max_spread_points": 500.0,
        "max_tick_age_seconds": 3600.0,
    },
}

LOCKOUT_READER_MODULE = "quantcore.execution.h024_runtime_safety_lockout"
HEARTBEAT_MODULE = "quantcore.execution.h024_runtime_safety_heartbeat"
DEFAULT_OUTPUT_PATH = Path("reports") / "h024_runtime_tick_spread_safety_supervisor.jsonl"


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


def _coerce_finite_float(value: Any) -> float | None:
    try:
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


def _symbol_checks(
    *,
    mt5_client: Any,
    runtime_symbol: str,
    config: Mapping[str, Any],
    now_epoch_seconds: float,
) -> dict[str, Any]:
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
                    "message": f"Symbol safety check failed for {runtime_symbol}: {name}",
                    "runtime_symbol": runtime_symbol,
                    "detail": _plain(detail),
                    "fail_closed": True,
                }
            )

    model_symbol = str(config.get("model_symbol", ""))
    max_spread_points = _coerce_finite_float(config.get("max_spread_points"))
    max_tick_age_seconds = _coerce_finite_float(config.get("max_tick_age_seconds"))

    add_check("model_symbol_configured", model_symbol in {"XAUUSD", "USDJPY"}, {"model_symbol": model_symbol})
    add_check(
        "max_spread_points_configured",
        max_spread_points is not None and max_spread_points > 0,
        {"max_spread_points": config.get("max_spread_points")},
    )
    add_check(
        "max_tick_age_seconds_configured",
        max_tick_age_seconds is not None and max_tick_age_seconds > 0,
        {"max_tick_age_seconds": config.get("max_tick_age_seconds")},
    )

    symbol_info, symbol_info_error = _safe_call(mt5_client, "symbol_info", runtime_symbol)
    tick_info, tick_info_error = _safe_call(mt5_client, "symbol_info_tick", runtime_symbol)

    symbol_info_plain = _plain(symbol_info)
    tick_info_plain = _plain(tick_info)

    add_check(
        "symbol_info_available",
        symbol_info is not None and symbol_info_error is None,
        {"error": symbol_info_error, "symbol_info": symbol_info_plain},
    )
    add_check(
        "tick_available",
        tick_info is not None and tick_info_error is None,
        {"error": tick_info_error, "tick": tick_info_plain},
    )

    visible = _field(symbol_info, "visible")
    add_check(
        "symbol_visible_selection_ready",
        symbol_info is not None and visible is True,
        {
            "visible": visible,
            "symbol_select_authorized": False,
            "symbol_select_called": False,
            "interpretation": "symbol must already be visible/readable; supervisor does not call symbol_select",
        },
    )

    point = _coerce_finite_float(_field(symbol_info, "point"))
    add_check("symbol_point_positive", point is not None and point > 0, {"point": _field(symbol_info, "point")})

    bid = _coerce_finite_float(_field(tick_info, "bid"))
    ask = _coerce_finite_float(_field(tick_info, "ask"))

    add_check("bid_positive_finite", bid is not None and bid > 0, {"bid": _field(tick_info, "bid")})
    add_check("ask_positive_finite", ask is not None and ask > 0, {"ask": _field(tick_info, "ask")})
    add_check("ask_above_bid", bid is not None and ask is not None and ask > bid, {"bid": bid, "ask": ask})

    spread_price = None
    spread_points = None
    if bid is not None and ask is not None:
        spread_price = ask - bid
        if point is not None and point > 0:
            spread_points = spread_price / point

    add_check(
        "spread_price_positive",
        spread_price is not None and spread_price > 0,
        {"spread_price": spread_price, "bid": bid, "ask": ask},
    )
    add_check(
        "spread_points_positive",
        spread_points is not None and spread_points > 0,
        {"spread_points": spread_points, "point": point},
    )
    add_check(
        "spread_points_within_threshold",
        spread_points is not None and max_spread_points is not None and spread_points <= max_spread_points,
        {"spread_points": spread_points, "max_spread_points": max_spread_points},
    )

    tick_time_msc = _coerce_finite_float(_field(tick_info, "time_msc"))
    tick_time = _coerce_finite_float(_field(tick_info, "time"))
    tick_epoch_seconds = None
    if tick_time_msc is not None and tick_time_msc > 0:
        tick_epoch_seconds = tick_time_msc / 1000.0
    elif tick_time is not None and tick_time > 0:
        tick_epoch_seconds = tick_time

    tick_age_seconds = None
    if tick_epoch_seconds is not None:
        tick_age_seconds = now_epoch_seconds - tick_epoch_seconds

    add_check(
        "tick_timestamp_available",
        tick_epoch_seconds is not None,
        {"time_msc": _field(tick_info, "time_msc"), "time": _field(tick_info, "time")},
    )
    add_check(
        "tick_fresh_within_threshold",
        tick_age_seconds is not None
        and max_tick_age_seconds is not None
        and -60.0 <= tick_age_seconds <= max_tick_age_seconds,
        {
            "tick_epoch_seconds": tick_epoch_seconds,
            "now_epoch_seconds": now_epoch_seconds,
            "tick_age_seconds": tick_age_seconds,
            "max_tick_age_seconds": max_tick_age_seconds,
            "future_tick_tolerance_seconds": 60.0,
        },
    )

    return {
        "runtime_symbol": runtime_symbol,
        "model_symbol": model_symbol,
        "symbol_select_authorized": False,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
        "configured_thresholds": {
            "max_spread_points": max_spread_points,
            "max_tick_age_seconds": max_tick_age_seconds,
        },
        "observed": {
            "symbol_info": symbol_info_plain,
            "tick": tick_info_plain,
            "point": point,
            "bid": bid,
            "ask": ask,
            "spread_price": spread_price,
            "spread_points": spread_points,
            "tick_epoch_seconds": tick_epoch_seconds,
            "tick_age_seconds": tick_age_seconds,
        },
        "checks": checks,
        "violations": violations,
        "verdict": "PASS" if not violations else "FAIL",
    }


def collect_h024_runtime_tick_spread_safety_supervisor(
    *,
    mt5_client: Any | None = None,
    symbol_configs: Mapping[str, Mapping[str, Any]] | None = None,
    expected_server: str = EXPECTED_SERVER,
    expected_currency: str = EXPECTED_ACCOUNT_CURRENCY,
    now_epoch_seconds: float | None = None,
) -> dict[str, Any]:
    """Collect a read-only H024 runtime tick and spread safety supervisor packet.

    This packet may read MT5 account, terminal, symbol_info, and symbol_info_tick.
    It never calls symbol_select, order_check, order_send, entry, close, modify,
    or any trading loop.
    """

    observed_at_utc = _utc_now_iso()
    now_epoch = float(time.time() if now_epoch_seconds is None else now_epoch_seconds)
    configs = dict(symbol_configs or DEFAULT_SYMBOL_CONFIGS)

    violations: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []

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
                    "message": f"Tick/spread supervisor check failed: {name}",
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
    add_check(
        "runtime_safety_heartbeat_passed",
        heartbeat_passed,
        {
            "heartbeat_packet_type": heartbeat_record.get("packet_type"),
            "heartbeat_verdict": heartbeat_record.get("verdict"),
            "heartbeat_operator_state": heartbeat_record.get("operator_state"),
            "heartbeat_violation_count": len(heartbeat_record.get("violations", [])),
        },
    )

    lockout_reference = _module_reference(LOCKOUT_READER_MODULE)
    heartbeat_reference = _module_reference(HEARTBEAT_MODULE)
    add_check("runtime_lockout_reader_referenced", lockout_reference.get("module_importable") is True, lockout_reference)
    add_check("runtime_heartbeat_packet_referenced", heartbeat_reference.get("module_importable") is True, heartbeat_reference)

    required_symbols = {"XAUUSDm", "USDJPYm"}
    configured_symbols = set(configs)
    add_check(
        "required_symbols_configured",
        configured_symbols == required_symbols,
        {"required_symbols": sorted(required_symbols), "configured_symbols": sorted(configured_symbols)},
    )

    symbol_records: list[dict[str, Any]] = []
    if mt5_client is not None and heartbeat_passed:
        for runtime_symbol in sorted(required_symbols):
            config = configs.get(runtime_symbol, {})
            symbol_record = _symbol_checks(
                mt5_client=mt5_client,
                runtime_symbol=runtime_symbol,
                config=config,
                now_epoch_seconds=now_epoch,
            )
            symbol_records.append(symbol_record)
            for violation in symbol_record["violations"]:
                violations.append(violation)
    else:
        for runtime_symbol in sorted(required_symbols):
            symbol_records.append(
                {
                    "runtime_symbol": runtime_symbol,
                    "model_symbol": str(configs.get(runtime_symbol, {}).get("model_symbol", "")),
                    "symbol_select_authorized": False,
                    "broker_mutation_authorized": False,
                    "order_check_authorized": False,
                    "order_send_authorized": False,
                    "entry_authorized": False,
                    "close_modify_authorized": False,
                    "trading_loop_authorized": False,
                    "configured_thresholds": _plain(configs.get(runtime_symbol, {})),
                    "observed": {},
                    "checks": [],
                    "violations": [
                        {
                            "code": "SYMBOL_CHECKS_SKIPPED_HEARTBEAT_BLOCKED",
                            "message": "Symbol checks skipped because runtime heartbeat failed or MT5 client was unavailable.",
                            "runtime_symbol": runtime_symbol,
                            "fail_closed": True,
                        }
                    ],
                    "verdict": "FAIL",
                }
            )
        violations.append(
            {
                "code": "SYMBOL_CHECKS_SKIPPED_HEARTBEAT_BLOCKED",
                "message": "Tick/spread checks cannot run safely without a passing runtime heartbeat.",
                "fail_closed": True,
            }
        )

    authorizations = _false_authorizations()
    authorization_violations = _authorization_violations(authorizations)
    violations.extend(authorization_violations)
    add_check("all_runtime_authorizations_false", not authorization_violations, authorizations)

    verdict = "PASS" if not violations else "FAIL"
    operator_state = (
        "TICK_SPREAD_SUPERVISOR_OK_BUT_TRADING_NOT_AUTHORIZED"
        if verdict == "PASS"
        else "FAIL_CLOSED_TICK_SPREAD_SUPERVISOR_BLOCKED"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY_ID,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": observed_at_utc,
        "expected": {
            "server": expected_server,
            "account_currency": expected_currency,
            "symbols": _plain(configs),
        },
        "upstream": {
            "heartbeat_packet_type": HEARTBEAT_PACKET_TYPE,
            "heartbeat_record": _plain(heartbeat_record),
            "heartbeat_reference": heartbeat_reference,
            "lockout_reader_reference": lockout_reference,
        },
        "symbols": symbol_records,
        "checks": checks,
        "authorizations": authorizations,
        "effective_new_entries_blocked": True,
        "symbol_select_authorized": False,
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


def verify_h024_runtime_tick_spread_safety_supervisor_records(
    records: list[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    verification_violations: list[dict[str, Any]] = []

    if not records:
        verification_violations.append(
            {
                "code": "NO_RECORDS",
                "message": "No H024 runtime tick/spread supervisor records were found.",
                "fail_closed": True,
            }
        )

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            verification_violations.append(
                {
                    "code": "UNEXPECTED_SCHEMA_VERSION",
                    "message": "Tick/spread supervisor record has an unexpected schema version.",
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
                    "message": "Tick/spread supervisor record has an unexpected strategy.",
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
                    "message": "Tick/spread supervisor record has an unexpected packet type.",
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
                    "message": "Tick/spread supervisor authorizations field is not an object.",
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

        if record.get("symbol_select_authorized") is not False:
            verification_violations.append(
                {
                    "code": "SYMBOL_SELECT_AUTHORIZED",
                    "message": "symbol_select must not be authorized by this supervisor.",
                    "record_index": index,
                    "observed": _plain(record.get("symbol_select_authorized")),
                    "fail_closed": True,
                }
            )

        if record.get("effective_new_entries_blocked") is not True:
            verification_violations.append(
                {
                    "code": "NEW_ENTRIES_NOT_EFFECTIVELY_BLOCKED",
                    "message": "Tick/spread supervisor must keep effective_new_entries_blocked true.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )

        upstream = record.get("upstream")
        if not isinstance(upstream, Mapping):
            verification_violations.append(
                {
                    "code": "UPSTREAM_NOT_OBJECT",
                    "message": "Tick/spread supervisor upstream field is not an object.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            heartbeat = upstream.get("heartbeat_record")
            if not isinstance(heartbeat, Mapping):
                verification_violations.append(
                    {
                        "code": "HEARTBEAT_RECORD_MISSING",
                        "message": "Tick/spread supervisor must embed or consume a heartbeat record.",
                        "record_index": index,
                        "fail_closed": True,
                    }
                )
            elif heartbeat.get("packet_type") != HEARTBEAT_PACKET_TYPE:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_HEARTBEAT_PACKET_TYPE",
                        "message": "Tick/spread supervisor references an unexpected heartbeat packet type.",
                        "record_index": index,
                        "observed": _plain(heartbeat.get("packet_type")),
                        "expected": HEARTBEAT_PACKET_TYPE,
                        "fail_closed": True,
                    }
                )
            elif require_pass and heartbeat.get("verdict") != "PASS":
                verification_violations.append(
                    {
                        "code": "HEARTBEAT_VERDICT_NOT_PASS",
                        "message": "Tick/spread supervisor require-pass mode requires upstream heartbeat PASS.",
                        "record_index": index,
                        "observed": _plain(heartbeat.get("verdict")),
                        "fail_closed": True,
                    }
                )

        symbol_records = record.get("symbols")
        if not isinstance(symbol_records, list):
            verification_violations.append(
                {
                    "code": "SYMBOLS_NOT_LIST",
                    "message": "Tick/spread supervisor symbols field is not a list.",
                    "record_index": index,
                    "fail_closed": True,
                }
            )
        else:
            observed_symbols = {item.get("runtime_symbol") for item in symbol_records if isinstance(item, Mapping)}
            if observed_symbols != {"XAUUSDm", "USDJPYm"}:
                verification_violations.append(
                    {
                        "code": "UNEXPECTED_SYMBOL_SET",
                        "message": "Tick/spread supervisor must cover exactly XAUUSDm and USDJPYm.",
                        "record_index": index,
                        "observed": sorted(str(symbol) for symbol in observed_symbols),
                        "expected": ["USDJPYm", "XAUUSDm"],
                        "fail_closed": True,
                    }
                )
            for symbol_index, symbol_record in enumerate(symbol_records):
                if not isinstance(symbol_record, Mapping):
                    verification_violations.append(
                        {
                            "code": "SYMBOL_RECORD_NOT_OBJECT",
                            "message": "Symbol record is not an object.",
                            "record_index": index,
                            "symbol_index": symbol_index,
                            "fail_closed": True,
                        }
                    )
                    continue
                if symbol_record.get("symbol_select_authorized") is not False:
                    verification_violations.append(
                        {
                            "code": "SYMBOL_RECORD_SELECT_AUTHORIZED",
                            "message": "Symbol record must not authorize symbol_select.",
                            "record_index": index,
                            "symbol_index": symbol_index,
                            "runtime_symbol": _plain(symbol_record.get("runtime_symbol")),
                            "fail_closed": True,
                        }
                    )
                for key in (
                    "broker_mutation_authorized",
                    "order_check_authorized",
                    "order_send_authorized",
                    "entry_authorized",
                    "close_modify_authorized",
                    "trading_loop_authorized",
                ):
                    if symbol_record.get(key) is not False:
                        verification_violations.append(
                            {
                                "code": "SYMBOL_RECORD_UNSAFE_AUTHORIZATION",
                                "message": f"Symbol record forbidden authorization is not false: {key}",
                                "record_index": index,
                                "symbol_index": symbol_index,
                                "runtime_symbol": _plain(symbol_record.get("runtime_symbol")),
                                "field": key,
                                "observed": _plain(symbol_record.get(key)),
                                "fail_closed": True,
                            }
                        )
                if require_pass and symbol_record.get("verdict") != "PASS":
                    verification_violations.append(
                        {
                            "code": "SYMBOL_RECORD_VERDICT_NOT_PASS",
                            "message": "Tick/spread supervisor require-pass mode requires every symbol record PASS.",
                            "record_index": index,
                            "symbol_index": symbol_index,
                            "runtime_symbol": _plain(symbol_record.get("runtime_symbol")),
                            "observed": _plain(symbol_record.get("verdict")),
                            "fail_closed": True,
                        }
                    )

        embedded_violations = record.get("violations", [])
        if record.get("verdict") == "PASS" and embedded_violations:
            verification_violations.append(
                {
                    "code": "PASS_RECORD_HAS_EMBEDDED_VIOLATIONS",
                    "message": "Tick/spread supervisor record verdict is PASS but embedded violations are present.",
                    "record_index": index,
                    "embedded_violation_count": len(embedded_violations),
                    "fail_closed": True,
                }
            )

        if require_pass and record.get("verdict") != "PASS":
            verification_violations.append(
                {
                    "code": "RECORD_VERDICT_NOT_PASS",
                    "message": "Tick/spread supervisor record verdict is not PASS.",
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
    parser = argparse.ArgumentParser(description="Build or verify H024 runtime tick/spread safety supervisor JSONL.")
    parser.add_argument("path", nargs="?", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--require-pass", action="store_true")
    return parser


__all__ = [
    "DEFAULT_OUTPUT_PATH",
    "DEFAULT_SYMBOL_CONFIGS",
    "PACKET_TYPE",
    "SCHEMA_VERSION",
    "STRATEGY_ID",
    "collect_h024_runtime_tick_spread_safety_supervisor",
    "read_jsonl",
    "verify_h024_runtime_tick_spread_safety_supervisor_records",
    "write_jsonl",
]