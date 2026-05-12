from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "h024_one_shot_demo_canary_monitor.v1"
STRATEGY = "H024"
EXPECTED_SERVER = "Exness-MT5Trial6"
EXPECTED_CURRENCY = "USD"
EXPECTED_SYMBOL = "XAUUSDm"
EXPECTED_MAGIC = 240024
EXPECTED_VOLUME = 0.01
EXPECTED_POSITION_TICKET = 4413054432
EXPECTED_ORDER_TICKET = 4413054432
EXPECTED_ENTRY_DEAL = 3788869526
EXPECTED_TYPE = 1
EXPECTED_PRICE_OPEN = 4728.4490000000005
EXPECTED_SL = 4817.394
EXPECTED_COMMENT_PREFIX = "H024_ONE_SHOT_DE"
FLOAT_TOLERANCE = 1e-6

READ_ONLY_MT5_CALLS = [
    "mt5.initialize",
    "mt5.account_info",
    "mt5.positions_get",
    "mt5.orders_get",
    "mt5.history_deals_get",
    "mt5.shutdown",
]

FORBIDDEN_MT5_CALLS = [
    "mt5.order_check",
    "mt5.order_send",
    "close",
    "modify",
    "gui_automation",
    "chart_attach",
    "chart_detach",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def expected_canary() -> dict[str, Any]:
    return {
        "server": EXPECTED_SERVER,
        "currency": EXPECTED_CURRENCY,
        "strategy": STRATEGY,
        "symbol": EXPECTED_SYMBOL,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "position_ticket": EXPECTED_POSITION_TICKET,
        "order_ticket": EXPECTED_ORDER_TICKET,
        "entry_deal": EXPECTED_ENTRY_DEAL,
        "type": EXPECTED_TYPE,
        "side": "sell",
        "price_open": EXPECTED_PRICE_OPEN,
        "sl": EXPECTED_SL,
        "comment_prefix": EXPECTED_COMMENT_PREFIX,
    }


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if hasattr(value, "_asdict"):
        return _json_safe(value._asdict())
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if hasattr(value, "__dict__"):
        return _json_safe(vars(value))
    return str(value)


def normalize_mt5_object(value: Any) -> dict[str, Any]:
    normalized = _json_safe(value)
    if normalized is None:
        return {}
    if not isinstance(normalized, dict):
        raise TypeError(f"Expected MT5 object to normalize to dict, got {type(normalized)!r}")
    return normalized


def normalize_mt5_objects(values: Iterable[Any] | None) -> list[dict[str, Any]]:
    if values is None:
        return []
    return [normalize_mt5_object(value) for value in values]


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL in {path} line {line_number}: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"Invalid JSONL in {path} line {line_number}: record is not an object")
            records.append(record)
    return records


def write_jsonl(path: str | Path, records: Iterable[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(_json_safe(record), sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def _as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _float_equal(left: Any, right: float, tolerance: float = FLOAT_TOLERANCE) -> bool:
    left_float = _as_float(left)
    return left_float is not None and abs(left_float - right) <= tolerance


def _deal_id(row: dict[str, Any]) -> int | None:
    for key in ("deal", "ticket", "id"):
        value = _as_int(row.get(key))
        if value is not None:
            return value
    return None


def _position_identity(row: dict[str, Any]) -> set[int]:
    identities: set[int] = set()
    for key in ("ticket", "identifier", "position_id", "position", "order"):
        value = _as_int(row.get(key))
        if value is not None:
            identities.add(value)
    return identities


def _is_expected_symbol_magic(row: dict[str, Any]) -> bool:
    return row.get("symbol") == EXPECTED_SYMBOL and _as_int(row.get("magic")) == EXPECTED_MAGIC


def _is_h024_row(row: dict[str, Any]) -> bool:
    comment = str(row.get("comment", "") or "")
    return _is_expected_symbol_magic(row) or comment.startswith("H024_ONE_SHOT") or comment.startswith(EXPECTED_COMMENT_PREFIX)


def _expected_position_violations(position: dict[str, Any]) -> list[dict[str, Any]]:
    checks = [
        (position.get("symbol") == EXPECTED_SYMBOL, "position_symbol_mismatch", position.get("symbol")),
        (_as_int(position.get("magic")) == EXPECTED_MAGIC, "position_magic_mismatch", position.get("magic")),
        (_as_int(position.get("type")) == EXPECTED_TYPE, "position_type_mismatch", position.get("type")),
        (_float_equal(position.get("volume"), EXPECTED_VOLUME), "position_volume_mismatch", position.get("volume")),
        (_float_equal(position.get("price_open"), EXPECTED_PRICE_OPEN), "position_open_price_mismatch", position.get("price_open")),
        (_float_equal(position.get("sl"), EXPECTED_SL), "position_sl_mismatch", position.get("sl")),
        (EXPECTED_POSITION_TICKET in _position_identity(position), "position_ticket_mismatch", {"ticket": position.get("ticket"), "identifier": position.get("identifier")}),
        (str(position.get("comment", "") or "").startswith(EXPECTED_COMMENT_PREFIX), "position_comment_prefix_mismatch", position.get("comment")),
    ]
    return [
        {"code": code, "detail": {"observed": observed, "expected_canary": expected_canary()}}
        for passed, code, observed in checks
        if not passed
    ]


def _is_exact_expected_position(position: dict[str, Any]) -> bool:
    return not _expected_position_violations(position)


def _entry_kind(value: Any) -> str | None:
    if value is None or value == "":
        return None
    text = str(value).strip().lower()
    if text in {"0", "in", "deal_entry_in"}:
        return "in"
    if text in {"1", "out", "deal_entry_out"}:
        return "out"
    if text in {"2", "inout", "deal_entry_inout"}:
        return "inout"
    if text in {"3", "out_by", "deal_entry_out_by"}:
        return "out"
    return text


def _is_entry_deal(deal: dict[str, Any]) -> bool:
    if not _is_expected_symbol_magic(deal):
        return False
    deal_id = _deal_id(deal)
    if deal_id == EXPECTED_ENTRY_DEAL:
        return True
    entry = _entry_kind(deal.get("entry"))
    return entry in {"in", "inout"}


def _is_matching_close_deal(deal: dict[str, Any]) -> bool:
    if not _is_expected_symbol_magic(deal):
        return False
    if not _float_equal(deal.get("volume"), EXPECTED_VOLUME):
        return False
    if EXPECTED_POSITION_TICKET not in _position_identity(deal):
        return False
    if _deal_id(deal) == EXPECTED_ENTRY_DEAL:
        return False
    entry = _entry_kind(deal.get("entry"))
    if entry in {"out", "inout"}:
        return True
    deal_type = _as_int(deal.get("type"))
    return deal_type == 0


def _ledger_success_records(ledger_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in ledger_records if record.get("attempt_stage") == "send_succeeded"]


def _validate_ledger(ledger_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    successes = _ledger_success_records(ledger_records)
    if len(successes) != 1:
        violations.append({"code": "ledger_success_count_mismatch", "detail": {"observed": len(successes), "expected": 1}})
        return violations
    success = successes[0]
    send = success.get("order_send_result") or {}
    request = success.get("request") or {}
    checks = [
        (success.get("allowed_demo_server") == EXPECTED_SERVER, "ledger_server_mismatch", success.get("allowed_demo_server")),
        (success.get("symbol") == EXPECTED_SYMBOL, "ledger_symbol_mismatch", success.get("symbol")),
        (_as_int(send.get("order")) == EXPECTED_ORDER_TICKET, "ledger_order_mismatch", send.get("order")),
        (_as_int(send.get("deal")) == EXPECTED_ENTRY_DEAL, "ledger_deal_mismatch", send.get("deal")),
        (_as_int(send.get("retcode")) == 10009, "ledger_send_retcode_mismatch", send.get("retcode")),
        (_as_int(request.get("magic")) == EXPECTED_MAGIC, "ledger_magic_mismatch", request.get("magic")),
        (_float_equal(request.get("volume"), EXPECTED_VOLUME), "ledger_volume_mismatch", request.get("volume")),
        (_as_int(request.get("type")) == EXPECTED_TYPE, "ledger_type_mismatch", request.get("type")),
        (_float_equal(request.get("sl"), EXPECTED_SL), "ledger_sl_mismatch", request.get("sl")),
    ]
    for passed, code, observed in checks:
        if not passed:
            violations.append({"code": code, "detail": {"observed": observed, "expected_canary": expected_canary()}})
    return violations


def build_monitor_record(
    *,
    generated_at_utc: str,
    account: dict[str, Any],
    positions: list[dict[str, Any]],
    pending_orders: list[dict[str, Any]],
    history_deals: list[dict[str, Any]],
    ledger_records: list[dict[str, Any]],
) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []

    if account.get("server") != EXPECTED_SERVER:
        violations.append({"code": "account_server_mismatch", "detail": {"observed": account.get("server"), "expected": EXPECTED_SERVER}})
    if account.get("currency") != EXPECTED_CURRENCY:
        violations.append({"code": "account_currency_mismatch", "detail": {"observed": account.get("currency"), "expected": EXPECTED_CURRENCY}})
    trade_mode = _as_int(account.get("trade_mode"))
    if trade_mode is not None and trade_mode != 0:
        violations.append({"code": "account_trade_mode_not_demo", "detail": {"observed": account.get("trade_mode"), "expected_demo_trade_mode": 0}})

    h024_positions = [position for position in positions if _is_h024_row(position)]
    exact_positions = [position for position in h024_positions if _is_exact_expected_position(position)]
    extra_positions = [position for position in h024_positions if not _is_exact_expected_position(position)]
    pending_h024_orders = [order for order in pending_orders if _is_h024_row(order)]
    h024_history_deals = [deal for deal in history_deals if _is_expected_symbol_magic(deal)]
    second_entry_deals = [deal for deal in h024_history_deals if _is_entry_deal(deal) and _deal_id(deal) != EXPECTED_ENTRY_DEAL]
    matching_close_deals = [deal for deal in h024_history_deals if _is_matching_close_deal(deal)]

    if len(exact_positions) > 1:
        violations.append({"code": "duplicate_exact_canary_positions", "detail": {"observed": len(exact_positions), "expected": 1}})
    if extra_positions:
        violations.append({"code": "unexpected_h024_positions", "detail": {"count": len(extra_positions), "positions": extra_positions}})
    if pending_h024_orders:
        violations.append({"code": "unexpected_h024_pending_orders", "detail": {"count": len(pending_h024_orders), "orders": pending_h024_orders}})
    if second_entry_deals:
        violations.append({"code": "second_h024_entry_deal_detected", "detail": {"count": len(second_entry_deals), "deals": second_entry_deals}})

    lifecycle_state = "unknown"
    open_canary_position = exact_positions[0] if len(exact_positions) == 1 else None
    if len(exact_positions) == 1 and not extra_positions:
        lifecycle_state = "open"
    elif not h024_positions and matching_close_deals:
        lifecycle_state = "closed_explained"
    elif not h024_positions:
        lifecycle_state = "no_open_position_without_matching_close_history"
        violations.append({"code": "no_open_position_without_matching_close_history", "detail": {"history_deal_count": len(h024_history_deals)}})
    else:
        lifecycle_state = "position_mismatch"

    violations.extend(_validate_ledger(ledger_records))

    latest_known = {
        "price_current": open_canary_position.get("price_current") if open_canary_position else None,
        "profit": open_canary_position.get("profit") if open_canary_position else None,
        "swap": open_canary_position.get("swap") if open_canary_position else None,
        "equity": account.get("equity"),
        "margin": account.get("margin"),
        "margin_free": account.get("margin_free"),
        "margin_level": account.get("margin_level"),
        "balance": account.get("balance"),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": generated_at_utc,
        "strategy": STRATEGY,
        "expected_canary": expected_canary(),
        "lifecycle_state": lifecycle_state,
        "verdict": "FAIL" if violations else "PASS",
        "violations": violations,
        "account": {
            "login": account.get("login"),
            "server": account.get("server"),
            "currency": account.get("currency"),
            "trade_mode": account.get("trade_mode"),
            "balance": account.get("balance"),
            "equity": account.get("equity"),
            "margin": account.get("margin"),
            "margin_free": account.get("margin_free"),
            "margin_level": account.get("margin_level"),
        },
        "observed": {
            "total_symbol_positions": len(positions),
            "h024_position_count": len(h024_positions),
            "exact_canary_position_count": len(exact_positions),
            "unexpected_h024_pending_order_count": len(pending_h024_orders),
            "h024_history_deal_count": len(h024_history_deals),
            "matching_close_deal_count": len(matching_close_deals),
            "second_entry_deal_count": len(second_entry_deals),
            "ledger_record_count": len(ledger_records),
            "ledger_success_count": len(_ledger_success_records(ledger_records)),
        },
        "open_canary_position": open_canary_position,
        "matching_close_deals": matching_close_deals,
        "latest_known": latest_known,
        "mt5_read_only_calls_allowed": READ_ONLY_MT5_CALLS,
        "mt5_mutating_calls_declared_forbidden": FORBIDDEN_MT5_CALLS,
    }


def verify_monitor_records(records: list[dict[str, Any]], *, require_pass: bool = False) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if len(records) != 1:
        violations.append({"code": "monitor_record_count_mismatch", "detail": {"observed": len(records), "expected": 1}})
        return violations
    record = records[0]
    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append({"code": "schema_version_mismatch", "detail": {"observed": record.get("schema_version"), "expected": SCHEMA_VERSION}})
    if record.get("strategy") != STRATEGY:
        violations.append({"code": "strategy_mismatch", "detail": {"observed": record.get("strategy"), "expected": STRATEGY}})
    if record.get("expected_canary") != expected_canary():
        violations.append({"code": "expected_canary_mismatch", "detail": {"observed": record.get("expected_canary"), "expected": expected_canary()}})
    if record.get("mt5_read_only_calls_allowed") != READ_ONLY_MT5_CALLS:
        violations.append({"code": "read_only_call_contract_mismatch", "detail": record.get("mt5_read_only_calls_allowed")})
    if record.get("lifecycle_state") not in {"open", "closed_explained"}:
        violations.append({"code": "lifecycle_state_not_accepted", "detail": {"observed": record.get("lifecycle_state"), "accepted": ["open", "closed_explained"]}})
    embedded_violations = record.get("violations") or []
    if embedded_violations:
        violations.append({"code": "monitor_embedded_violations_present", "detail": embedded_violations})
    if record.get("verdict") != ("FAIL" if embedded_violations else "PASS"):
        violations.append({"code": "monitor_verdict_inconsistent", "detail": {"verdict": record.get("verdict"), "embedded_violations": embedded_violations}})
    if require_pass and record.get("verdict") != "PASS":
        violations.append({"code": "monitor_verdict_not_pass", "detail": {"observed": record.get("verdict"), "expected": "PASS"}})
    return violations