from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APPROVAL_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_check_operator_approval.json"
OUTPUT_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_check.jsonl"

EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"
EXPECTED_SYMBOL = "XAUUSDm"
EXPECTED_POSITION_SIDE = "sell"
EXPECTED_CLOSE_SIDE = "buy"
EXPECTED_VOLUME = 0.01
EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_MAGIC = 240024
EXPECTED_INTENT = "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_ONLY"

APPROVAL_SCHEMA = "h025_exact_ticket_canary_close_order_check_approval.v1"
REPORT_SCHEMA = "h025_exact_ticket_canary_close_order_check.v1"


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
        "expires_at_utc": iso_utc(now + timedelta(minutes=15)),
        "intent": EXPECTED_INTENT,
        "operator_approved": False,
        "order_check_authorized": False,
        "operator_attestation": "I approve H025 order_check only for exact ticket 4413054432. I do not approve order_send.",
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "symbol": EXPECTED_SYMBOL,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side": EXPECTED_CLOSE_SIDE,
        "order_send_authorized": False,
        "close_all_authorized": False,
        "entry_authorized": False,
        "live_money_authorized": False,
    }


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


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


def validate_approval(approval: dict[str, Any] | None, now: datetime) -> list[dict[str, str]]:
    if approval is None:
        return [{
            "code": "operator_approval_missing_or_malformed",
            "severity": "ERROR",
            "message": "operator approval artifact is missing or malformed",
        }]

    violations: list[dict[str, str]] = []
    expected_fields = {
        "schema": APPROVAL_SCHEMA,
        "intent": EXPECTED_INTENT,
        "operator_approved": True,
        "order_check_authorized": True,
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "symbol": EXPECTED_SYMBOL,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side": EXPECTED_CLOSE_SIDE,
        "order_send_authorized": False,
        "close_all_authorized": False,
        "entry_authorized": False,
        "live_money_authorized": False,
    }

    for field, expected in expected_fields.items():
        actual = approval.get(field)
        if actual != expected:
            violations.append({
                "code": f"approval_{field}_unexpected",
                "severity": "ERROR",
                "message": f"approval field {field!r} must be {expected!r}; got {actual!r}",
            })

    attestation = approval.get("operator_attestation")
    if not isinstance(attestation, str):
        violations.append({
            "code": "operator_attestation_missing",
            "severity": "ERROR",
            "message": "operator_attestation must be a string",
        })
    else:
        lowered = attestation.lower()
        if "order_check only" not in lowered or "do not approve order_send" not in lowered:
            violations.append({
                "code": "operator_attestation_ambiguous",
                "severity": "ERROR",
                "message": "operator_attestation must approve order_check only and reject order_send",
            })

    expires_at = parse_utc(approval.get("expires_at_utc"))
    if expires_at is None:
        violations.append({
            "code": "approval_expiry_missing_or_malformed",
            "severity": "ERROR",
            "message": "expires_at_utc must be timezone-aware ISO-8601",
        })
    elif expires_at <= now:
        violations.append({
            "code": "approval_expired",
            "severity": "ERROR",
            "message": "operator approval artifact has expired",
        })

    return violations


def base_record(stage: str, approval_path: Path, violations: list[dict[str, str]]) -> dict[str, Any]:
    verdict = "PASS" if not violations else "FAIL_CLOSED"
    return {
        "schema": REPORT_SCHEMA,
        "generated_at_utc": iso_utc(utc_now()),
        "stage": stage,
        "verdict": verdict,
        "operator_state": (
            "H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_COMPLETED_NO_CLOSE_SENT"
            if verdict == "PASS"
            else "FAIL_CLOSED_H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_BLOCKED"
        ),
        "operator_next_action": (
            "REVIEW_ORDER_CHECK_RESULT_THEN_SEPARATELY_AUTHORIZE_STAGE_4_ORDER_SEND_IF_ACCEPTABLE"
            if verdict == "PASS"
            else "FIX_VIOLATIONS_BEFORE_ANY_ORDER_CHECK_OR_ORDER_SEND"
        ),
        "violations": violations,
        "approval_path": str(approval_path),
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "symbol": EXPECTED_SYMBOL,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side_checked": EXPECTED_CLOSE_SIDE,
        "demo_account_only": True,
        "order_check_authorized": verdict == "PASS",
        "order_check_executed": False,
        "order_send_authorized": False,
        "order_send_executed": False,
        "symbol_select_authorized": False,
        "symbol_select_executed": False,
        "broker_mutation_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "close_all_authorized": False,
        "unattended_loop_authorized": False,
        "live_money_authorized": False,
    }


def write_report(record: dict[str, Any]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def fail_closed(stage: str, approval_path: Path, violations: list[dict[str, str]]) -> int:
    record = base_record(stage, approval_path, violations)
    write_report(record)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(violations)}")
    print(f"Operator state: {record['operator_state']}")
    print(f"order_check_executed: {record['order_check_executed']}")
    print(f"order_send_executed: {record['order_send_executed']}")
    return 1


def write_approval_template(path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(approval_template(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote approval template: {path}")
    print("Template is disabled by default.")
    return 0


def run_order_check(approval_path: Path) -> int:
    approval = read_json(approval_path)
    approval_violations = validate_approval(approval, utc_now())
    if approval_violations:
        return fail_closed("H025_STAGE_3_APPROVAL_VALIDATION", approval_path, approval_violations)

    import MetaTrader5 as mt5  # type: ignore[import-not-found]

    initialized = False
    try:
        initialized = bool(mt5.initialize())
        if not initialized:
            return fail_closed("H025_STAGE_3_MT5_INITIALIZE", approval_path, [{
                "code": "mt5_initialize_failed",
                "severity": "ERROR",
                "message": f"mt5.initialize failed: {mt5.last_error()}",
            }])

        account = as_dict(mt5.account_info())
        if account.get("server") != EXPECTED_ACCOUNT_SERVER:
            return fail_closed("H025_STAGE_3_ACCOUNT_CHECK", approval_path, [{
                "code": "account_server_unexpected",
                "severity": "ERROR",
                "message": f"expected {EXPECTED_ACCOUNT_SERVER}; got {account.get('server')!r}",
            }])

        positions = list(mt5.positions_get(ticket=EXPECTED_TICKET) or [])
        if len(positions) != 1:
            return fail_closed("H025_STAGE_3_EXACT_POSITION_CHECK", approval_path, [{
                "code": "exact_ticket_position_count_unexpected",
                "severity": "ERROR",
                "message": f"expected one position for ticket {EXPECTED_TICKET}; got {len(positions)}",
            }])

        position = as_dict(positions[0])
        position_violations: list[dict[str, str]] = []

        if position.get("identifier") != EXPECTED_IDENTIFIER:
            position_violations.append({"code": "position_identifier_unexpected", "severity": "ERROR", "message": str(position.get("identifier"))})
        if position.get("symbol") != EXPECTED_SYMBOL:
            position_violations.append({"code": "position_symbol_unexpected", "severity": "ERROR", "message": str(position.get("symbol"))})
        if position.get("magic") != EXPECTED_MAGIC:
            position_violations.append({"code": "position_magic_unexpected", "severity": "ERROR", "message": str(position.get("magic"))})
        if abs(float(position.get("volume", -1.0)) - EXPECTED_VOLUME) > 0.0000001:
            position_violations.append({"code": "position_volume_unexpected", "severity": "ERROR", "message": str(position.get("volume"))})
        if position.get("type") != mt5.POSITION_TYPE_SELL:
            position_violations.append({"code": "position_type_unexpected", "severity": "ERROR", "message": str(position.get("type"))})

        h024_positions = [
            as_dict(item)
            for item in list(mt5.positions_get(symbol=EXPECTED_SYMBOL) or [])
            if as_dict(item).get("magic") == EXPECTED_MAGIC
        ]
        if len(h024_positions) != 1:
            position_violations.append({
                "code": "h024_position_count_unexpected",
                "severity": "ERROR",
                "message": f"expected one H024 position on {EXPECTED_SYMBOL}; got {len(h024_positions)}",
            })

        h024_orders = [
            as_dict(item)
            for item in list(mt5.orders_get(symbol=EXPECTED_SYMBOL) or [])
            if as_dict(item).get("magic") == EXPECTED_MAGIC
        ]
        if h024_orders:
            position_violations.append({
                "code": "h024_pending_order_count_unexpected",
                "severity": "ERROR",
                "message": f"expected zero H024 pending orders on {EXPECTED_SYMBOL}; got {len(h024_orders)}",
            })

        if position_violations:
            return fail_closed("H025_STAGE_3_EXACT_POSITION_CHECK", approval_path, position_violations)

        tick = as_dict(mt5.symbol_info_tick(EXPECTED_SYMBOL))
        ask = tick.get("ask")
        if ask is None or float(ask) <= 0.0:
            return fail_closed("H025_STAGE_3_TICK_CHECK", approval_path, [{
                "code": "tick_ask_missing_or_invalid",
                "severity": "ERROR",
                "message": f"missing/invalid ask for {EXPECTED_SYMBOL}",
            }])

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": EXPECTED_SYMBOL,
            "volume": EXPECTED_VOLUME,
            "type": mt5.ORDER_TYPE_BUY,
            "position": EXPECTED_TICKET,
            "price": float(ask),
            "deviation": 50,
            "magic": EXPECTED_MAGIC,
            "comment": "H025_CLOSE_CHECK",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        check_result = mt5.order_check(request)
        check = as_dict(check_result)

        violations: list[dict[str, str]] = []
        if check_result is None:
            violations.append({
                "code": "order_check_returned_none",
                "severity": "ERROR",
                "message": f"mt5.order_check returned None: {mt5.last_error()}",
            })
        elif check.get("retcode") not in (0,):
            violations.append({
                "code": "order_check_retcode_not_clear",
                "severity": "ERROR",
                "message": f"retcode={check.get('retcode')!r}; comment={check.get('comment')!r}",
            })

        record = base_record("H025_STAGE_3_EXACT_TICKET_CLOSE_ORDER_CHECK", approval_path, violations)
        record["order_check_executed"] = True
        record["order_check_result"] = check
        record["mt5_last_error_after_order_check"] = mt5.last_error()
        record["position_snapshot"] = position
        record["account_snapshot"] = account
        record["tick_snapshot"] = tick
        record["request_checked"] = request
        record["order_send_authorized"] = False
        record["order_send_executed"] = False
        record["broker_mutation_authorized"] = False
        record["close_modify_authorized"] = False

        if violations:
            record["verdict"] = "FAIL_CLOSED"
            record["operator_state"] = "FAIL_CLOSED_H025_EXACT_TICKET_CANARY_CLOSE_ORDER_CHECK_REJECTED"
            record["operator_next_action"] = "OPERATOR_REVIEW_REQUIRED_NO_ORDER_SEND_AUTHORIZED"

        write_report(record)

        print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
        print(f"Verdict: {record['verdict']}")
        print(f"Operator state: {record['operator_state']}")
        print(f"Exact ticket: {EXPECTED_TICKET}")
        print(f"Exact identifier: {EXPECTED_IDENTIFIER}")
        print(f"order_check_executed: {record['order_check_executed']}")
        print(f"order_send_authorized: {record['order_send_authorized']}")
        print(f"order_send_executed: {record['order_send_executed']}")
        print(f"broker_mutation_authorized: {record['broker_mutation_authorized']}")
        print(f"retcode: {check.get('retcode')!r}")
        print(f"comment: {check.get('comment')!r}")

        return 0 if record["verdict"] == "PASS" else 1
    finally:
        if initialized:
            mt5.shutdown()


def main() -> int:
    parser = argparse.ArgumentParser(description="H025 exact-ticket canary close order_check only; no order_send.")
    parser.add_argument("--approval-json", type=Path, default=DEFAULT_APPROVAL_PATH)
    parser.add_argument("--write-approval-template", type=Path)
    args = parser.parse_args()

    if args.write_approval_template:
        return write_approval_template(args.write_approval_template)

    return run_order_check(args.approval_json)


if __name__ == "__main__":
    raise SystemExit(main())

