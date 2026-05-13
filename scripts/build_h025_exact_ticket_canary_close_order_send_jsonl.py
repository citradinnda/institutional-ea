from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_APPROVAL_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_send_operator_approval.json"
STAGE3_REPORT_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_check.jsonl"
OUTPUT_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_send.jsonl"

EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"
EXPECTED_SYMBOL = "XAUUSDm"
EXPECTED_POSITION_SIDE = "sell"
EXPECTED_CLOSE_SIDE = "buy"
EXPECTED_VOLUME = 0.01
EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_MAGIC = 240024
EXPECTED_INTENT = "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_ONE_SHOT"

APPROVAL_SCHEMA = "h025_exact_ticket_canary_close_order_send_approval.v1"
REPORT_SCHEMA = "h025_exact_ticket_canary_close_order_send.v1"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def approval_template() -> dict[str, Any]:
    now = utc_now()
    return {
        "schema": APPROVAL_SCHEMA,
        "created_at_utc": iso_utc(now),
        "expires_at_utc": iso_utc(now + timedelta(minutes=10)),
        "intent": EXPECTED_INTENT,
        "operator_approved": False,
        "order_send_authorized": False,
        "operator_attestation": (
            "I approve H025 one-shot demo order_send only to close exact ticket 4413054432. "
            "I do not approve new entries, close-all, symbol_select, loops, or live-money execution."
        ),
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "symbol": EXPECTED_SYMBOL,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side": EXPECTED_CLOSE_SIDE,
        "stage3_order_check_required": True,
        "pre_send_order_check_required": True,
        "order_check_authorized": True,
        "close_all_authorized": False,
        "entry_authorized": False,
        "symbol_select_authorized": False,
        "live_money_authorized": False,
        "unattended_loop_authorized": False,
    }


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def read_first_jsonl(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                return None
            return value if isinstance(value, dict) else None
    return None


def as_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "_asdict"):
        return dict(value._asdict())
    return {
        name: getattr(value, name)
        for name in dir(value)
        if not name.startswith("_") and not callable(getattr(value, name))
    }


def violation(code: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": "ERROR", "message": message}


def validate_stage3_report(stage3: dict[str, Any] | None) -> list[dict[str, str]]:
    if stage3 is None:
        return [violation("stage3_order_check_report_missing_or_malformed", "Stage 3 order_check report is missing or malformed")]

    violations: list[dict[str, str]] = []
    expected = {
        "verdict": "PASS",
        "stage": "H025_STAGE_3_EXACT_TICKET_CLOSE_ORDER_CHECK",
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "symbol": EXPECTED_SYMBOL,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side_checked": EXPECTED_CLOSE_SIDE,
        "order_check_executed": True,
        "order_send_authorized": False,
        "order_send_executed": False,
        "broker_mutation_authorized": False,
    }

    for field, expected_value in expected.items():
        actual = stage3.get(field)
        if actual != expected_value:
            violations.append(violation(
                f"stage3_{field}_unexpected",
                f"Stage 3 field {field!r} must be {expected_value!r}; got {actual!r}",
            ))

    order_check_result = stage3.get("order_check_result")
    if not isinstance(order_check_result, dict) or order_check_result.get("retcode") != 0:
        violations.append(violation("stage3_order_check_retcode_not_clear", "Stage 3 order_check_result.retcode must be 0"))

    return violations


def validate_approval(approval: dict[str, Any] | None, now: datetime) -> list[dict[str, str]]:
    if approval is None:
        return [violation("operator_approval_missing_or_malformed", "operator approval artifact is missing or malformed")]

    violations: list[dict[str, str]] = []
    expected = {
        "schema": APPROVAL_SCHEMA,
        "intent": EXPECTED_INTENT,
        "operator_approved": True,
        "order_send_authorized": True,
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "symbol": EXPECTED_SYMBOL,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side": EXPECTED_CLOSE_SIDE,
        "stage3_order_check_required": True,
        "pre_send_order_check_required": True,
        "order_check_authorized": True,
        "close_all_authorized": False,
        "entry_authorized": False,
        "symbol_select_authorized": False,
        "live_money_authorized": False,
        "unattended_loop_authorized": False,
    }

    for field, expected_value in expected.items():
        actual = approval.get(field)
        if actual != expected_value:
            violations.append(violation(
                f"approval_{field}_unexpected",
                f"approval field {field!r} must be {expected_value!r}; got {actual!r}",
            ))

    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, str):
        violations.append(violation("operator_attestation_missing", "operator_attestation must be a string"))
    else:
        lowered = attestation.lower()
        required_phrases = [
            "one-shot demo order_send only",
            "close exact ticket 4413054432",
            "do not approve new entries",
            "close-all",
            "symbol_select",
            "loops",
            "live-money",
        ]
        for phrase in required_phrases:
            if phrase not in lowered:
                violations.append(violation("operator_attestation_incomplete", f"operator_attestation missing phrase: {phrase}"))

    expires_at = parse_utc(approval.get("expires_at_utc"))
    if expires_at is None:
        violations.append(violation("approval_expiry_missing_or_malformed", "expires_at_utc must be timezone-aware ISO-8601"))
    elif expires_at <= now:
        violations.append(violation("approval_expired", "operator approval artifact has expired"))

    return violations


def base_record(stage: str, approval_path: Path, violations: list[dict[str, str]]) -> dict[str, Any]:
    verdict = "PASS" if not violations else "FAIL_CLOSED"
    return {
        "schema": REPORT_SCHEMA,
        "generated_at_utc": iso_utc(utc_now()),
        "stage": stage,
        "verdict": verdict,
        "operator_state": (
            "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_COMPLETED_AND_VERIFIED"
            if verdict == "PASS"
            else "FAIL_CLOSED_H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_BLOCKED"
        ),
        "operator_next_action": (
            "VERIFY_NO_EXTRA_H024_POSITIONS_OR_ORDERS_AND_STOP_NO_LOOP"
            if verdict == "PASS"
            else "OPERATOR_REVIEW_REQUIRED_NO_ADDITIONAL_ORDER_SEND_AUTHORIZED"
        ),
        "violations": violations,
        "approval_path": str(approval_path),
        "stage3_report_path": str(STAGE3_REPORT_PATH),
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "symbol": EXPECTED_SYMBOL,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side_sent": EXPECTED_CLOSE_SIDE,
        "demo_account_only": True,
        "order_check_executed": False,
        "order_send_authorized": verdict == "PASS",
        "order_send_executed": False,
        "symbol_select_authorized": False,
        "symbol_select_executed": False,
        "broker_mutation_authorized": verdict == "PASS",
        "entry_authorized": False,
        "close_modify_authorized": verdict == "PASS",
        "close_all_authorized": False,
        "unattended_loop_authorized": False,
        "live_money_authorized": False,
        "post_send_exact_ticket_open": None,
        "post_send_h024_position_count": None,
        "post_send_h024_order_count": None,
    }


def write_report(record: dict[str, Any]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def fail_closed(stage: str, approval_path: Path, violations: list[dict[str, str]]) -> int:
    record = base_record(stage, approval_path, violations)
    record["order_send_authorized"] = False
    record["broker_mutation_authorized"] = False
    record["close_modify_authorized"] = False
    write_report(record)

    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(violations)}")
    print(f"Operator state: {record['operator_state']}")
    print(f"order_check_executed: {record['order_check_executed']}")
    print(f"order_send_authorized: {record['order_send_authorized']}")
    print(f"order_send_executed: {record['order_send_executed']}")
    return 1


def write_approval_template(path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(approval_template(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote approval template: {path}")
    print("Template is disabled by default.")
    return 0


def h024_symbol_magic_positions(mt5: Any) -> list[dict[str, Any]]:
    return [
        as_dict(item)
        for item in list(mt5.positions_get(symbol=EXPECTED_SYMBOL) or [])
        if as_dict(item).get("magic") == EXPECTED_MAGIC
    ]


def h024_symbol_magic_orders(mt5: Any) -> list[dict[str, Any]]:
    return [
        as_dict(item)
        for item in list(mt5.orders_get(symbol=EXPECTED_SYMBOL) or [])
        if as_dict(item).get("magic") == EXPECTED_MAGIC
    ]


def run_order_send(approval_path: Path) -> int:
    stage3 = read_first_jsonl(STAGE3_REPORT_PATH)
    stage3_violations = validate_stage3_report(stage3)
    if stage3_violations:
        return fail_closed("H025_STAGE_4_STAGE3_PREFLIGHT_VALIDATION", approval_path, stage3_violations)

    approval = read_json(approval_path)
    approval_violations = validate_approval(approval, utc_now())
    if approval_violations:
        return fail_closed("H025_STAGE_4_APPROVAL_VALIDATION", approval_path, approval_violations)

    import MetaTrader5 as mt5  # type: ignore[import-not-found]

    initialized = False
    try:
        initialized = bool(mt5.initialize())
        if not initialized:
            return fail_closed("H025_STAGE_4_MT5_INITIALIZE", approval_path, [
                violation("mt5_initialize_failed", f"mt5.initialize failed: {mt5.last_error()}")
            ])

        account = as_dict(mt5.account_info())
        if account.get("server") != EXPECTED_ACCOUNT_SERVER:
            return fail_closed("H025_STAGE_4_ACCOUNT_CHECK", approval_path, [
                violation("account_server_unexpected", f"expected {EXPECTED_ACCOUNT_SERVER}; got {account.get('server')!r}")
            ])

        positions = list(mt5.positions_get(ticket=EXPECTED_TICKET) or [])
        if len(positions) != 1:
            return fail_closed("H025_STAGE_4_EXACT_POSITION_CHECK", approval_path, [
                violation("exact_ticket_position_count_unexpected", f"expected one position for ticket {EXPECTED_TICKET}; got {len(positions)}")
            ])

        position = as_dict(positions[0])
        position_violations: list[dict[str, str]] = []

        if position.get("identifier") != EXPECTED_IDENTIFIER:
            position_violations.append(violation("position_identifier_unexpected", str(position.get("identifier"))))
        if position.get("symbol") != EXPECTED_SYMBOL:
            position_violations.append(violation("position_symbol_unexpected", str(position.get("symbol"))))
        if position.get("magic") != EXPECTED_MAGIC:
            position_violations.append(violation("position_magic_unexpected", str(position.get("magic"))))
        if abs(float(position.get("volume", -1.0)) - EXPECTED_VOLUME) > 0.0000001:
            position_violations.append(violation("position_volume_unexpected", str(position.get("volume"))))
        if position.get("type") != mt5.POSITION_TYPE_SELL:
            position_violations.append(violation("position_type_unexpected", str(position.get("type"))))

        h024_positions_before = h024_symbol_magic_positions(mt5)
        h024_orders_before = h024_symbol_magic_orders(mt5)

        if len(h024_positions_before) != 1:
            position_violations.append(violation(
                "h024_position_count_unexpected",
                f"expected one H024 position on {EXPECTED_SYMBOL}; got {len(h024_positions_before)}",
            ))
        if h024_orders_before:
            position_violations.append(violation(
                "h024_pending_order_count_unexpected",
                f"expected zero H024 pending orders on {EXPECTED_SYMBOL}; got {len(h024_orders_before)}",
            ))

        if position_violations:
            return fail_closed("H025_STAGE_4_EXACT_POSITION_CHECK", approval_path, position_violations)

        tick = as_dict(mt5.symbol_info_tick(EXPECTED_SYMBOL))
        ask = tick.get("ask")
        if ask is None or float(ask) <= 0.0:
            return fail_closed("H025_STAGE_4_TICK_CHECK", approval_path, [
                violation("tick_ask_missing_or_invalid", f"missing/invalid ask for {EXPECTED_SYMBOL}")
            ])

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": EXPECTED_SYMBOL,
            "volume": EXPECTED_VOLUME,
            "type": mt5.ORDER_TYPE_BUY,
            "position": EXPECTED_TICKET,
            "price": float(ask),
            "deviation": 50,
            "magic": EXPECTED_MAGIC,
            "comment": "H025_CLOSE_SEND",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        pre_send_check_result = mt5.order_check(request)
        pre_send_check = as_dict(pre_send_check_result)

        if pre_send_check_result is None:
            return fail_closed("H025_STAGE_4_PRE_SEND_ORDER_CHECK", approval_path, [
                violation("pre_send_order_check_returned_none", f"mt5.order_check returned None: {mt5.last_error()}")
            ])

        if pre_send_check.get("retcode") != 0:
            return fail_closed("H025_STAGE_4_PRE_SEND_ORDER_CHECK", approval_path, [
                violation("pre_send_order_check_retcode_not_clear", f"retcode={pre_send_check.get('retcode')!r}; comment={pre_send_check.get('comment')!r}")
            ])

        send_result = mt5.order_send(request)
        send = as_dict(send_result)

        send_violations: list[dict[str, str]] = []
        if send_result is None:
            send_violations.append(violation("order_send_returned_none", f"mt5.order_send returned None: {mt5.last_error()}"))
        elif send.get("retcode") != mt5.TRADE_RETCODE_DONE:
            send_violations.append(violation("order_send_retcode_not_done", f"retcode={send.get('retcode')!r}; comment={send.get('comment')!r}"))

        post_exact_positions = list(mt5.positions_get(ticket=EXPECTED_TICKET) or [])
        post_h024_positions = h024_symbol_magic_positions(mt5)
        post_h024_orders = h024_symbol_magic_orders(mt5)

        if post_exact_positions:
            send_violations.append(violation("post_send_exact_ticket_still_open", f"ticket {EXPECTED_TICKET} still open after order_send"))

        if post_h024_orders:
            send_violations.append(violation("post_send_h024_pending_orders_exist", f"H024 pending orders remain: {len(post_h024_orders)}"))

        remaining_same_ticket = [
            item for item in post_h024_positions
            if item.get("ticket") == EXPECTED_TICKET or item.get("identifier") == EXPECTED_IDENTIFIER
        ]
        if remaining_same_ticket:
            send_violations.append(violation("post_send_same_identifier_position_remains", "same ticket/identifier still present after order_send"))

        record = base_record("H025_STAGE_4_EXACT_TICKET_CLOSE_ORDER_SEND", approval_path, send_violations)
        record.update({
            "order_check_executed": True,
            "pre_send_order_check_result": pre_send_check,
            "order_send_authorized": True,
            "order_send_executed": True,
            "broker_mutation_authorized": True,
            "close_modify_authorized": True,
            "order_send_result": send,
            "mt5_last_error_after_order_send": mt5.last_error(),
            "position_snapshot_before_send": position,
            "account_snapshot_before_send": account,
            "tick_snapshot_before_send": tick,
            "request_sent": request,
            "h024_positions_before_send": h024_positions_before,
            "h024_orders_before_send": h024_orders_before,
            "post_send_exact_ticket_open": bool(post_exact_positions),
            "post_send_exact_ticket_positions": [as_dict(item) for item in post_exact_positions],
            "post_send_h024_position_count": len(post_h024_positions),
            "post_send_h024_positions": post_h024_positions,
            "post_send_h024_order_count": len(post_h024_orders),
            "post_send_h024_orders": post_h024_orders,
        })

        if send_violations:
            record["verdict"] = "FAIL_CLOSED"
            record["operator_state"] = "FAIL_CLOSED_H025_EXACT_TICKET_CANARY_CLOSE_ORDER_SEND_UNVERIFIED"
            record["operator_next_action"] = "OPERATOR_REVIEW_REQUIRED_NO_ADDITIONAL_ORDER_SEND_AUTHORIZED"

        write_report(record)

        print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
        print(f"Verdict: {record['verdict']}")
        print(f"Operator state: {record['operator_state']}")
        print(f"Exact ticket: {EXPECTED_TICKET}")
        print(f"Exact identifier: {EXPECTED_IDENTIFIER}")
        print(f"order_check_executed: {record['order_check_executed']}")
        print(f"order_send_executed: {record['order_send_executed']}")
        print(f"broker_mutation_authorized: {record['broker_mutation_authorized']}")
        print(f"send_retcode: {send.get('retcode')!r}")
        print(f"send_comment: {send.get('comment')!r}")
        print(f"post_send_exact_ticket_open: {record['post_send_exact_ticket_open']}")
        print(f"post_send_h024_position_count: {record['post_send_h024_position_count']}")
        print(f"post_send_h024_order_count: {record['post_send_h024_order_count']}")

        return 0 if record["verdict"] == "PASS" else 1

    finally:
        if initialized:
            mt5.shutdown()


def main() -> int:
    parser = argparse.ArgumentParser(description="H025 exact-ticket canary close order_send one-shot; no loop.")
    parser.add_argument("--approval-json", type=Path, default=DEFAULT_APPROVAL_PATH)
    parser.add_argument("--write-approval-template", type=Path)
    args = parser.parse_args()

    if args.write_approval_template:
        return write_approval_template(args.write_approval_template)

    return run_order_send(args.approval_json)


if __name__ == "__main__":
    raise SystemExit(main())
