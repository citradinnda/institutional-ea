"""Read-only H024 USDJPY broker-readiness packet.

This module intentionally performs no broker mutation. It may be used by a
script that imports MetaTrader5, but the only MT5 calls expected here are
read-only account, symbol, tick, rates, positions, and orders queries.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping


STRATEGY = "H024"
PACKET_TYPE = "h024_usdjpy_broker_readiness"
SCHEMA_VERSION = "1.0"

ALLOWED_DEMO_SERVER = "Exness-MT5Trial6"
EXPECTED_ACCOUNT_CURRENCY = "USD"
MODEL_SYMBOL = "USDJPY"
RUNTIME_SYMBOL = "USDJPYm"
MAGIC = 240024

CANARY_VOLUME_FLOOR_LOT = 0.01
MIN_H4_BARS = 50
MIN_M1_BARS = 200
MAX_SPREAD_POINTS = 250.0


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return str(value)
        return value
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "item"):
        try:
            return _json_safe(value.item())
        except Exception:
            pass
    if hasattr(value, "_asdict"):
        return {str(k): _json_safe(v) for k, v in value._asdict().items()}
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "__dict__"):
        return {
            str(k): _json_safe(v)
            for k, v in vars(value).items()
            if not str(k).startswith("_")
        }
    return str(value)


def _object_to_dict(value: Any) -> dict[str, Any]:
    safe = _json_safe(value)
    if isinstance(safe, dict):
        return safe
    return {"value": safe}


def _sequence_to_dicts(value: Any) -> list[dict[str, Any]] | None:
    if value is None:
        return None
    safe = _json_safe(value)
    if isinstance(safe, list):
        return [item if isinstance(item, dict) else {"value": item} for item in safe]
    return [{"value": safe}]


def _rate_count(value: Any) -> int:
    if value is None:
        return 0
    try:
        return len(value)
    except TypeError:
        return 0


def _latest_rate_time(value: Any) -> Any:
    if _rate_count(value) <= 0:
        return None
    try:
        latest = value[-1]
    except Exception:
        return None
    latest_safe = _json_safe(latest)
    if isinstance(latest_safe, dict):
        return latest_safe.get("time")
    return None


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def _decimal(value: Any) -> Decimal | None:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None


def _volume_aligned(value: Any, minimum: Any, step: Any) -> bool:
    value_d = _decimal(value)
    minimum_d = _decimal(minimum)
    step_d = _decimal(step)
    if value_d is None or minimum_d is None or step_d is None or step_d <= 0:
        return False
    quotient = (value_d - minimum_d) / step_d
    return quotient == quotient.to_integral_value()


def _has_magic(item: Mapping[str, Any], magic: int) -> bool:
    return str(item.get("magic")) == str(magic)


def _build_base_record(generated_at_utc: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "generated_at_utc": generated_at_utc or utc_now_iso(),
        "allowed_demo_server": ALLOWED_DEMO_SERVER,
        "expected_account_currency": EXPECTED_ACCOUNT_CURRENCY,
        "model_symbol": MODEL_SYMBOL,
        "runtime_symbol": RUNTIME_SYMBOL,
        "magic": MAGIC,
        "read_only": True,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "usd_jpy_order_authorized": False,
        "trading_loop_authorized": False,
        "requires_separate_canary_governance": True,
        "violations": [],
        "observations": {},
        "verdict": "FAIL",
    }


def build_h024_usdjpy_broker_readiness_record(
    mt5: Any,
    *,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    """Build a read-only USDJPY readiness packet from an MT5-like module."""

    record = _build_base_record(generated_at_utc)
    violations: list[str] = record["violations"]

    initialized = False
    try:
        initialized = bool(mt5.initialize())
        record["observations"]["mt5_initialized"] = initialized
        if not initialized:
            violations.append("mt5_initialize_failed")
            record["verdict"] = "FAIL"
            return record

        account_info_raw = mt5.account_info()
        account_info = _object_to_dict(account_info_raw) if account_info_raw is not None else {}
        record["account"] = account_info

        if not account_info:
            violations.append("account_info_unavailable")
        if account_info.get("server") != ALLOWED_DEMO_SERVER:
            violations.append("unexpected_account_server")
        if account_info.get("currency") != EXPECTED_ACCOUNT_CURRENCY:
            violations.append("unexpected_account_currency")

        symbol_info_raw = mt5.symbol_info(RUNTIME_SYMBOL)
        symbol_info = _object_to_dict(symbol_info_raw) if symbol_info_raw is not None else {}
        record["symbol_info"] = symbol_info

        if not symbol_info:
            violations.append("symbol_info_unavailable")
        else:
            if symbol_info.get("name") not in (None, RUNTIME_SYMBOL):
                violations.append("unexpected_symbol_name")
            if symbol_info.get("visible") is False:
                violations.append("runtime_symbol_not_visible")
            if symbol_info.get("trade_mode") == 0:
                violations.append("runtime_symbol_trade_disabled")

            point = _as_float(symbol_info.get("point"))
            tick_size = _as_float(symbol_info.get("trade_tick_size"))
            contract_size = _as_float(symbol_info.get("trade_contract_size"))
            volume_min = _as_float(symbol_info.get("volume_min"))
            volume_step = _as_float(symbol_info.get("volume_step"))
            volume_max = _as_float(symbol_info.get("volume_max"))

            if point is None or point <= 0:
                violations.append("invalid_symbol_point")
            if tick_size is not None and tick_size <= 0:
                violations.append("invalid_trade_tick_size")
            if contract_size is not None and contract_size <= 0:
                violations.append("invalid_trade_contract_size")
            if volume_min is None or volume_min <= 0:
                violations.append("invalid_volume_min")
            if volume_step is None or volume_step <= 0:
                violations.append("invalid_volume_step")
            if volume_max is None or volume_max < (volume_min or 0):
                violations.append("invalid_volume_max")

        tick_raw = mt5.symbol_info_tick(RUNTIME_SYMBOL)
        tick = _object_to_dict(tick_raw) if tick_raw is not None else {}
        record["tick"] = tick

        bid = _as_float(tick.get("bid"))
        ask = _as_float(tick.get("ask"))
        point = _as_float(symbol_info.get("point")) if symbol_info else None
        spread_price = None
        spread_points = None

        if not tick:
            violations.append("symbol_tick_unavailable")
        elif bid is None or ask is None or bid <= 0 or ask <= 0:
            violations.append("invalid_tick_bid_ask")
        elif ask < bid:
            violations.append("crossed_tick_bid_ask")
        elif point is None or point <= 0:
            violations.append("spread_points_unavailable_due_invalid_point")
        else:
            spread_price = ask - bid
            spread_points = spread_price / point
            if spread_price <= 0:
                violations.append("non_positive_spread")
            if spread_points > MAX_SPREAD_POINTS:
                violations.append("spread_points_exceeds_sanity_limit")

        record["spread_sanity"] = {
            "bid": bid,
            "ask": ask,
            "spread_price": spread_price,
            "spread_points": spread_points,
            "max_spread_points": MAX_SPREAD_POINTS,
        }

        timeframe_h4 = getattr(mt5, "TIMEFRAME_H4", 16388)
        timeframe_m1 = getattr(mt5, "TIMEFRAME_M1", 1)
        h4_rates = mt5.copy_rates_from_pos(RUNTIME_SYMBOL, timeframe_h4, 0, MIN_H4_BARS)
        m1_rates = mt5.copy_rates_from_pos(RUNTIME_SYMBOL, timeframe_m1, 0, MIN_M1_BARS)

        h4_count = _rate_count(h4_rates)
        m1_count = _rate_count(m1_rates)
        record["broker_native_data"] = {
            "h4": {
                "runtime_symbol": RUNTIME_SYMBOL,
                "timeframe": "H4",
                "minimum_bars_required": MIN_H4_BARS,
                "bars_observed": h4_count,
                "latest_rate_time": _latest_rate_time(h4_rates),
            },
            "m1": {
                "runtime_symbol": RUNTIME_SYMBOL,
                "timeframe": "M1",
                "minimum_bars_required": MIN_M1_BARS,
                "bars_observed": m1_count,
                "latest_rate_time": _latest_rate_time(m1_rates),
            },
        }

        if h4_count < MIN_H4_BARS:
            violations.append("insufficient_broker_native_h4_bars")
        if m1_count < MIN_M1_BARS:
            violations.append("insufficient_broker_native_m1_bars")

        volume_min = symbol_info.get("volume_min") if symbol_info else None
        volume_step = symbol_info.get("volume_step") if symbol_info else None
        volume_max = symbol_info.get("volume_max") if symbol_info else None

        min_lot_feasible = False
        if volume_min is not None and volume_step is not None and volume_max is not None:
            floor = _decimal(CANARY_VOLUME_FLOOR_LOT)
            min_d = _decimal(volume_min)
            max_d = _decimal(volume_max)
            min_lot_feasible = (
                floor is not None
                and min_d is not None
                and max_d is not None
                and min_d <= floor <= max_d
                and _volume_aligned(CANARY_VOLUME_FLOOR_LOT, volume_min, volume_step)
            )

        record["h020_sizing_feasibility"] = {
            "uses_h020_contract": True,
            "manual_lot_reconstruction_authorized": False,
            "candidate_floor_lot_for_future_canary": CANARY_VOLUME_FLOOR_LOT,
            "volume_min": volume_min,
            "volume_step": volume_step,
            "volume_max": volume_max,
            "candidate_floor_lot_feasible": min_lot_feasible,
        }

        if not min_lot_feasible:
            violations.append("h020_min_lot_feasibility_failed")

        positions_raw = mt5.positions_get(symbol=RUNTIME_SYMBOL)
        orders_raw = mt5.orders_get(symbol=RUNTIME_SYMBOL)
        positions = _sequence_to_dicts(positions_raw)
        orders = _sequence_to_dicts(orders_raw)

        record["open_positions"] = {
            "query_symbol": RUNTIME_SYMBOL,
            "positions_get_returned_none": positions is None,
            "count": None if positions is None else len(positions),
            "h024_magic_count": None if positions is None else sum(1 for item in positions if _has_magic(item, MAGIC)),
            "h024_magic_positions": [] if positions is None else [item for item in positions if _has_magic(item, MAGIC)],
        }
        record["pending_orders"] = {
            "query_symbol": RUNTIME_SYMBOL,
            "orders_get_returned_none": orders is None,
            "count": None if orders is None else len(orders),
            "h024_magic_count": None if orders is None else sum(1 for item in orders if _has_magic(item, MAGIC)),
            "h024_magic_orders": [] if orders is None else [item for item in orders if _has_magic(item, MAGIC)],
        }

        if positions is None:
            violations.append("positions_get_unavailable")
        elif any(_has_magic(item, MAGIC) for item in positions):
            violations.append("unexpected_h024_usdjpy_position_exists")

        if orders is None:
            violations.append("orders_get_unavailable")
        elif any(_has_magic(item, MAGIC) for item in orders):
            violations.append("unexpected_h024_usdjpy_pending_order_exists")

        record["request_shape_implications"] = {
            "status": "read_only_constraints_only",
            "runtime_symbol": RUNTIME_SYMBOL,
            "model_symbol": MODEL_SYMBOL,
            "strategy": STRATEGY,
            "magic": MAGIC,
            "future_request_must_be_separately_governed": True,
            "future_request_must_use_h020_sizing": True,
            "future_request_must_have_separate_usdjpy_acknowledgement": True,
            "future_request_must_have_separate_idempotency_ledger": True,
            "future_request_must_have_post_order_audit": True,
            "order_check_authorized_now": False,
            "order_send_authorized_now": False,
            "close_or_modify_authorized_now": False,
            "trading_loop_authorized_now": False,
        }

    except Exception as exc:
        violations.append("read_only_broker_readiness_exception")
        record["exception"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        if initialized:
            try:
                mt5.shutdown()
                record["observations"]["mt5_shutdown_called"] = True
            except Exception as exc:
                violations.append("mt5_shutdown_failed")
                record["observations"]["mt5_shutdown_exception"] = {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }

    record["verdict"] = "PASS" if not violations else "FAIL"
    return _json_safe(record)


def write_jsonl(record: Mapping[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(_json_safe(record), sort_keys=True, separators=(",", ":")) + "\n")
    return path


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def verify_h024_usdjpy_broker_readiness_records(
    records: Iterable[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    loaded = [dict(record) for record in records]
    violations: list[str] = []

    if len(loaded) != 1:
        violations.append("expected_exactly_one_readiness_record")

    record = loaded[0] if loaded else {}

    expected_fields = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "allowed_demo_server": ALLOWED_DEMO_SERVER,
        "expected_account_currency": EXPECTED_ACCOUNT_CURRENCY,
        "model_symbol": MODEL_SYMBOL,
        "runtime_symbol": RUNTIME_SYMBOL,
        "magic": MAGIC,
    }
    for key, expected in expected_fields.items():
        if record.get(key) != expected:
            violations.append(f"unexpected_{key}")

    false_fields = [
        "broker_mutation_authorized",
        "order_check_authorized",
        "order_send_authorized",
        "usd_jpy_order_authorized",
        "trading_loop_authorized",
    ]
    for key in false_fields:
        if record.get(key) is not False:
            violations.append(f"{key}_must_be_false")

    if record.get("read_only") is not True:
        violations.append("read_only_must_be_true")

    if record.get("requires_separate_canary_governance") is not True:
        violations.append("requires_separate_canary_governance_must_be_true")

    request_shape = record.get("request_shape_implications")
    if not isinstance(request_shape, Mapping):
        violations.append("request_shape_implications_missing")
    else:
        if request_shape.get("order_check_authorized_now") is not False:
            violations.append("request_shape_order_check_authorized_now_must_be_false")
        if request_shape.get("order_send_authorized_now") is not False:
            violations.append("request_shape_order_send_authorized_now_must_be_false")
        if request_shape.get("trading_loop_authorized_now") is not False:
            violations.append("request_shape_trading_loop_authorized_now_must_be_false")
        if request_shape.get("future_request_must_be_separately_governed") is not True:
            violations.append("future_request_must_be_separately_governed_missing")

    embedded_violations = record.get("violations", [])
    if not isinstance(embedded_violations, list):
        violations.append("embedded_violations_not_list")
        embedded_violations = []

    if require_pass and record.get("verdict") != "PASS":
        violations.append("record_verdict_not_pass")
    if require_pass and embedded_violations:
        violations.append("record_contains_embedded_violations")

    return {
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "record_count": len(loaded),
        "embedded_violations": embedded_violations,
        "record_verdict": record.get("verdict"),
        "broker_mutation_authorized": record.get("broker_mutation_authorized"),
        "order_check_authorized": record.get("order_check_authorized"),
        "order_send_authorized": record.get("order_send_authorized"),
        "usd_jpy_order_authorized": record.get("usd_jpy_order_authorized"),
        "trading_loop_authorized": record.get("trading_loop_authorized"),
    }