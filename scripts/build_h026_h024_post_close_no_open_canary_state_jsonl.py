"""Build H026/H024-post-close read-only no-open-canary observer state.

This packet intentionally treats the old H024 canary absence as acceptable only
when H025 Stage 5 has already verified the exact ticket is closed and there are
zero H024 positions/orders.

This module is read-only. It consumes H025 Stage 5 evidence and writes a local
operator packet. It uses only local JSON evidence and writes local operator packets. It performs no broker
mutation.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "h026_h024_post_close_no_open_canary_state.v1"
STAGE = "H026_H024_POST_CLOSE_NO_OPEN_CANARY_OBSERVER_STATE"

ACCOUNT_SERVER = "Exness-MT5Trial6"
SYMBOL = "XAUUSDm"
MODEL_SYMBOL = "XAUUSD"
EXACT_TICKET = 4413054432
EXACT_IDENTIFIER = 4413054432
MAGIC = 240024
VOLUME = 0.01
EXPECTED_DASHBOARD_WORDING = "NO OPEN CANARY - INTENTIONALLY CLOSED BY H025"

DEFAULT_STAGE5_REPORT = Path("reports/h025_exact_ticket_canary_post_close_verification.jsonl")
DEFAULT_OUTPUT_JSONL = Path("reports/h026_h024_post_close_no_open_canary_state.jsonl")
DEFAULT_OUTPUT_TEXT = Path("reports/h026_h024_post_close_no_open_canary_state.txt")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_last_jsonl(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing Stage 5 report: {path}")

    last_line = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            last_line = stripped

    if not last_line:
        raise ValueError(f"empty Stage 5 report: {path}")

    parsed = json.loads(last_line)
    if not isinstance(parsed, dict):
        raise ValueError("Stage 5 report JSONL record must be an object")

    return parsed


def as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def build_packet(stage5_report_path: Path) -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    stage5: dict[str, Any] | None = None

    packet: dict[str, Any] = {
        "schema": SCHEMA,
        "stage": STAGE,
        "generated_at_utc": utc_now_iso(),
        "account_server": ACCOUNT_SERVER,
        "symbol": SYMBOL,
        "model_symbol": MODEL_SYMBOL,
        "exact_ticket": EXACT_TICKET,
        "exact_identifier": EXACT_IDENTIFIER,
        "magic": MAGIC,
        "volume": VOLUME,
        "stage5_report_path": str(stage5_report_path),
        "read_only_observer_state_only": True,
        "broker_mutation_authorized": False,
        "trading_authorized": False,
        "entry_authorized": False,
        "close_all_authorized": False,
        "live_money_authorized": False,
        "h024_post_close_observer_enabled": True,
        "dashboard_wording": EXPECTED_DASHBOARD_WORDING,
        "readiness_wording": EXPECTED_DASHBOARD_WORDING,
        "operator_next_action": "OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED",
    }

    try:
        stage5 = read_last_jsonl(stage5_report_path)
    except Exception as exc:
        violations.append(
            {
                "code": "stage5_report_unreadable",
                "severity": "ERROR",
                "message": str(exc),
            }
        )

    if stage5 is None:
        packet.update(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_H026_STAGE5_POST_CLOSE_EVIDENCE_UNAVAILABLE",
                "canary_absence_classification": "UNEXPECTED_MISSING_CANARY_OR_STAGE5_UNVERIFIED",
                "post_close_verified": False,
                "open_canary_trade_exists": None,
                "exact_ticket_open": None,
                "h024_position_count": None,
                "h024_order_count": None,
                "violations": violations,
            }
        )
        return packet

    stage5_verdict = stage5.get("verdict")
    post_close_verified = as_bool(stage5.get("post_close_verified"))
    open_canary_trade_exists = as_bool(stage5.get("open_canary_trade_exists"))
    exact_ticket_open = as_bool(stage5.get("exact_ticket_open"))
    h024_position_count = as_int(stage5.get("h024_position_count"))
    h024_order_count = as_int(stage5.get("h024_order_count"))

    packet.update(
        {
            "stage5_verdict": stage5_verdict,
            "post_close_verified": post_close_verified,
            "open_canary_trade_exists": open_canary_trade_exists,
            "exact_ticket_open": exact_ticket_open,
            "h024_position_count": h024_position_count,
            "h024_order_count": h024_order_count,
            "stage5_operator_state": stage5.get("operator_state"),
            "stage5_stage": stage5.get("stage"),
            "history_deal_match_count": stage5.get("history_deal_match_count"),
        }
    )

    expected_pairs = [
        ("stage5_verdict_not_pass", stage5_verdict, "PASS"),
        ("post_close_not_verified", post_close_verified, True),
        ("open_canary_trade_exists_unexpected", open_canary_trade_exists, False),
        ("exact_ticket_still_open", exact_ticket_open, False),
        ("h024_position_count_not_zero", h024_position_count, 0),
        ("h024_order_count_not_zero", h024_order_count, 0),
    ]

    for code, actual, expected in expected_pairs:
        if actual != expected:
            violations.append(
                {
                    "code": code,
                    "severity": "ERROR",
                    "message": f"Expected {expected!r}; got {actual!r}.",
                }
            )

    if violations:
        packet.update(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_H026_NO_OPEN_CANARY_NOT_INTENTIONALLY_VERIFIED",
                "canary_absence_classification": "UNEXPECTED_MISSING_CANARY_OR_STAGE5_UNVERIFIED",
                "violations": violations,
            }
        )
        return packet

    packet.update(
        {
            "verdict": "PASS",
            "operator_state": "H026_H024_POST_CLOSE_NO_OPEN_CANARY_INTENTIONALLY_CLOSED_BY_H025",
            "canary_absence_classification": "INTENTIONALLY_CLOSED_BY_H025",
            "h024_observer_state": "POST_CLOSE_NO_OPEN_CANARY_ACCEPTED",
            "dashboard_state": EXPECTED_DASHBOARD_WORDING,
            "readiness_state": EXPECTED_DASHBOARD_WORDING,
            "operator_next_action": "NO_OPEN_CANARY_ACCEPTED_READ_ONLY_OBSERVER_CONTINUATION",
            "violations": [],
        }
    )
    return packet


def write_outputs(packet: dict[str, Any], output_jsonl: Path, output_text: Path) -> None:
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_text.parent.mkdir(parents=True, exist_ok=True)

    output_jsonl.write_text(json.dumps(packet, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "H026/H024 post-close no-open-canary observer state",
        f"Verdict: {packet.get('verdict')}",
        f"Operator state: {packet.get('operator_state')}",
        f"Canary absence classification: {packet.get('canary_absence_classification')}",
        f"Dashboard wording: {packet.get('dashboard_wording')}",
        f"Readiness wording: {packet.get('readiness_wording')}",
        f"Exact ticket open: {packet.get('exact_ticket_open')}",
        f"H024 position count: {packet.get('h024_position_count')}",
        f"H024 order count: {packet.get('h024_order_count')}",
        f"Trading authorized: {packet.get('trading_authorized')}",
        f"Broker mutation authorized: {packet.get('broker_mutation_authorized')}",
        f"Violations: {len(packet.get('violations', []))}",
    ]
    output_text.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage5-report", type=Path, default=DEFAULT_STAGE5_REPORT)
    parser.add_argument("--output-jsonl", type=Path, default=DEFAULT_OUTPUT_JSONL)
    parser.add_argument("--output-text", type=Path, default=DEFAULT_OUTPUT_TEXT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_packet(args.stage5_report)
    write_outputs(packet, args.output_jsonl, args.output_text)

    print(f"H026/H024 post-close no-open-canary observer state verdict: {packet['verdict']}")
    print(f"Operator state: {packet['operator_state']}")
    print(f"Canary absence classification: {packet['canary_absence_classification']}")
    print(f"Dashboard wording: {packet['dashboard_wording']}")
    print(f"Readiness wording: {packet['readiness_wording']}")
    print(f"Exact ticket open: {packet.get('exact_ticket_open')}")
    print(f"H024 position count: {packet.get('h024_position_count')}")
    print(f"H024 order count: {packet.get('h024_order_count')}")
    print(f"Trading authorized: {packet['trading_authorized']}")
    print(f"Broker mutation authorized: {packet['broker_mutation_authorized']}")
    print(f"Violations: {len(packet.get('violations', []))}")

    return 0 if packet["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

