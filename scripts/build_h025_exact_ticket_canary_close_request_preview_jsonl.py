from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_request_preview.jsonl"

EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"
EXPECTED_SYMBOL = "XAUUSDm"
EXPECTED_POSITION_SIDE = "sell"
EXPECTED_CLOSE_SIDE = "buy"
EXPECTED_VOLUME = 0.01
EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_MAGIC = 240024

SCHEMA_NAME = "h025_exact_ticket_canary_close_request_preview.v1"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_preview_record() -> dict[str, Any]:
    violations: list[dict[str, str]] = []

    close_request_preview = {
        "shape_kind": "INERT_EXACT_TICKET_CLOSE_REQUEST_PREVIEW_ONLY",
        "not_submitable_to_mt5": True,
        "account_server_required": EXPECTED_ACCOUNT_SERVER,
        "symbol_required": EXPECTED_SYMBOL,
        "position_ticket_required": EXPECTED_TICKET,
        "position_identifier_required": EXPECTED_IDENTIFIER,
        "magic_required": EXPECTED_MAGIC,
        "position_side_to_close": EXPECTED_POSITION_SIDE,
        "close_side_preview": EXPECTED_CLOSE_SIDE,
        "volume_required": EXPECTED_VOLUME,
        "comment_preview": "H025 exact-ticket canary close preview only",
        "manual_operator_approval_required_before_order_check": True,
        "manual_operator_confirmation_required_before_order_send": True,
    }

    if close_request_preview["position_ticket_required"] != EXPECTED_TICKET:
        violations.append(
            {
                "code": "unexpected_ticket",
                "severity": "ERROR",
                "message": "close preview is not constrained to the exact canary ticket",
            }
        )

    if close_request_preview["position_identifier_required"] != EXPECTED_IDENTIFIER:
        violations.append(
            {
                "code": "unexpected_identifier",
                "severity": "ERROR",
                "message": "close preview is not constrained to the exact canary identifier",
            }
        )

    if close_request_preview["account_server_required"] != EXPECTED_ACCOUNT_SERVER:
        violations.append(
            {
                "code": "unexpected_account_server",
                "severity": "ERROR",
                "message": "close preview is not constrained to the expected demo server",
            }
        )

    if close_request_preview["symbol_required"] != EXPECTED_SYMBOL:
        violations.append(
            {
                "code": "unexpected_symbol",
                "severity": "ERROR",
                "message": "close preview is not constrained to XAUUSDm",
            }
        )

    if close_request_preview["magic_required"] != EXPECTED_MAGIC:
        violations.append(
            {
                "code": "unexpected_magic",
                "severity": "ERROR",
                "message": "close preview is not constrained to magic 240024",
            }
        )

    if close_request_preview["volume_required"] != EXPECTED_VOLUME:
        violations.append(
            {
                "code": "unexpected_volume",
                "severity": "ERROR",
                "message": "close preview is not constrained to 0.01 lots",
            }
        )

    verdict = "PASS" if not violations else "FAIL_CLOSED"

    return {
        "schema": SCHEMA_NAME,
        "generated_at_utc": _utc_now_iso(),
        "stage": "H025_STAGE_2_EXACT_TICKET_CLOSE_REQUEST_PREVIEW",
        "verdict": verdict,
        "operator_state": (
            "H025_EXACT_TICKET_CLOSE_REQUEST_PREVIEW_READY_BUT_NOT_SUBMITTED"
            if verdict == "PASS"
            else "FAIL_CLOSED_H025_EXACT_TICKET_CLOSE_REQUEST_PREVIEW_INVALID"
        ),
        "operator_next_action": (
            "REVIEW_PREVIEW_THEN_SEPARATELY_AUTHORIZE_STAGE_3_ORDER_CHECK_IF_ACCEPTABLE"
            if verdict == "PASS"
            else "FIX_PREVIEW_BEFORE_ANY_ORDER_CHECK_OR_ORDER_SEND"
        ),
        "violations": violations,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "symbol": EXPECTED_SYMBOL,
        "side_to_close": EXPECTED_POSITION_SIDE,
        "close_side_preview": EXPECTED_CLOSE_SIDE,
        "volume": EXPECTED_VOLUME,
        "magic": EXPECTED_MAGIC,
        "preview_only": True,
        "inert_close_request_shape_constructed": True,
        "live_mt5_request_constructed": False,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "unattended_loop_authorized": False,
        "close_all_authorized": False,
        "live_money_authorized": False,
        "close_request_preview": close_request_preview,
    }


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = build_preview_record()
    OUTPUT_PATH.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Verdict: {record['verdict']}")
    print(f"Operator state: {record['operator_state']}")
    print(f"Exact ticket: {record['exact_ticket']}")
    print(f"Exact identifier: {record['exact_identifier']}")
    print(f"Preview only: {record['preview_only']}")
    print(f"Broker mutation authorized: {record['broker_mutation_authorized']}")
    print(f"order_check_authorized: {record['order_check_authorized']}")
    print(f"order_send_authorized: {record['order_send_authorized']}")

    return 0 if record["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
