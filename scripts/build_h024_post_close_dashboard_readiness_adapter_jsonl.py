"""Build H024 post-close dashboard/readiness adapter packet.

This adapter consumes the H024 post-close no-open-canary observer state packet
and emits a dashboard/readiness-compatible summary for the closed canary state.

The module uses local evidence only and writes local reports only.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "h024_post_close_dashboard_readiness_adapter.v1"
STAGE = "H024_POST_CLOSE_DASHBOARD_READINESS_ADAPTER"

ACCOUNT_SERVER = "Exness-MT5Trial6"
SYMBOL = "XAUUSDm"
MODEL_SYMBOL = "XAUUSD"
EXACT_TICKET = 4413054432
EXACT_IDENTIFIER = 4413054432
MAGIC = 240024
VOLUME = 0.01

EXPECTED_WORDING = "NO OPEN CANARY - INTENTIONALLY CLOSED BY H025"
EXPECTED_POST_CLOSE_CLASSIFICATION = "INTENTIONALLY_CLOSED_BY_H025"

DEFAULT_POST_CLOSE_REPORT = Path("reports/h024_post_close_no_open_canary_state.jsonl")
DEFAULT_OUTPUT_JSONL = Path("reports/h024_post_close_dashboard_readiness_adapter.jsonl")
DEFAULT_OUTPUT_TEXT = Path("reports/h024_post_close_dashboard_readiness_adapter.txt")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_last_jsonl(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing H024 post-close report: {path}")

    last_line = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            last_line = stripped

    if not last_line:
        raise ValueError(f"empty H024 post-close report: {path}")

    parsed = json.loads(last_line)
    if not isinstance(parsed, dict):
        raise ValueError("H024 post-close JSONL record must be an object")

    return parsed


def build_packet(post_close_report_path: Path) -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    post_close: dict[str, Any] | None = None

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
        "post_close_report_path": str(post_close_report_path),
        "read_only_adapter_only": True,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "entry_authorized": False,
        "close_all_authorized": False,
        "live_money_authorized": False,
        "operator_next_action": "OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED",
    }

    try:
        post_close = read_last_jsonl(post_close_report_path)
    except Exception as exc:
        violations.append(
            {
                "code": "post_close_report_unreadable",
                "severity": "ERROR",
                "message": str(exc),
            }
        )

    if post_close is None:
        packet.update(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_H024_POST_CLOSE_STATE_UNAVAILABLE",
                "dashboard_state": "NO_OPEN_CANARY_UNVERIFIED",
                "readiness_state": "NO_OPEN_CANARY_UNVERIFIED",
                "h024_dashboard_compatible": False,
                "h024_readiness_compatible": False,
                "canary_absence_classification": "UNEXPECTED_MISSING_CANARY_OR_POST_CLOSE_UNVERIFIED",
                "violations": violations,
            }
        )
        return packet

    post_close_verdict = post_close.get("verdict")
    post_close_classification = post_close.get("canary_absence_classification")
    post_close_exact_ticket_open = post_close.get("exact_ticket_open")
    post_close_position_count = post_close.get("h024_position_count")
    post_close_order_count = post_close.get("h024_order_count")
    post_close_trading_authorized = post_close.get("trading_authorized")
    post_close_broker_mutation_authorized = post_close.get("broker_mutation_authorized")
    post_close_dashboard_wording = post_close.get("dashboard_wording")
    post_close_readiness_wording = post_close.get("readiness_wording")

    packet.update(
        {
            "post_close_verdict": post_close_verdict,
            "post_close_operator_state": post_close.get("operator_state"),
            "canary_absence_classification": post_close_classification,
            "exact_ticket_open": post_close_exact_ticket_open,
            "h024_position_count": post_close_position_count,
            "h024_order_count": post_close_order_count,
            "post_close_trading_authorized": post_close_trading_authorized,
            "post_close_broker_mutation_authorized": post_close_broker_mutation_authorized,
            "dashboard_wording": post_close_dashboard_wording,
            "readiness_wording": post_close_readiness_wording,
        }
    )

    expected_pairs = [
        ("post_close_verdict_not_pass", post_close_verdict, "PASS"),
        ("post_close_absence_not_intentionally_closed", post_close_classification, EXPECTED_POST_CLOSE_CLASSIFICATION),
        ("exact_ticket_open_not_false", post_close_exact_ticket_open, False),
        ("h024_position_count_not_zero", post_close_position_count, 0),
        ("h024_order_count_not_zero", post_close_order_count, 0),
        ("post_close_trading_authorized_not_false", post_close_trading_authorized, False),
        ("post_close_broker_mutation_authorized_not_false", post_close_broker_mutation_authorized, False),
        ("dashboard_wording_unexpected", post_close_dashboard_wording, EXPECTED_WORDING),
        ("readiness_wording_unexpected", post_close_readiness_wording, EXPECTED_WORDING),
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
                "operator_state": "FAIL_CLOSED_H024_POST_CLOSE_DASHBOARD_READINESS_UNVERIFIED",
                "dashboard_state": "NO_OPEN_CANARY_UNVERIFIED",
                "readiness_state": "NO_OPEN_CANARY_UNVERIFIED",
                "h024_dashboard_compatible": False,
                "h024_readiness_compatible": False,
                "violations": violations,
            }
        )
        return packet

    packet.update(
        {
            "verdict": "PASS",
            "operator_state": "H024_DASHBOARD_READINESS_ACCEPTS_H025_POST_CLOSE_NO_OPEN_CANARY",
            "dashboard_state": EXPECTED_WORDING,
            "readiness_state": EXPECTED_WORDING,
            "h024_dashboard_compatible": True,
            "h024_readiness_compatible": True,
            "legacy_open_canary_required": False,
            "post_close_no_open_canary_accepted": True,
            "operator_next_action": "H024_DASHBOARD_READINESS_CAN_SHOW_INTENTIONAL_POST_CLOSE_STATE",
            "violations": [],
        }
    )
    return packet


def write_outputs(packet: dict[str, Any], output_jsonl: Path, output_text: Path) -> None:
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_text.parent.mkdir(parents=True, exist_ok=True)

    output_jsonl.write_text(json.dumps(packet, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "H024 post-close dashboard/readiness adapter",
        f"Verdict: {packet.get('verdict')}",
        f"Operator state: {packet.get('operator_state')}",
        f"Dashboard state: {packet.get('dashboard_state')}",
        f"Readiness state: {packet.get('readiness_state')}",
        f"Dashboard compatible: {packet.get('h024_dashboard_compatible')}",
        f"Readiness compatible: {packet.get('h024_readiness_compatible')}",
        f"Legacy open canary required: {packet.get('legacy_open_canary_required')}",
        f"Post-close no-open-canary accepted: {packet.get('post_close_no_open_canary_accepted')}",
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
    parser.add_argument("--post-close-report", type=Path, default=DEFAULT_POST_CLOSE_REPORT)
    parser.add_argument("--output-jsonl", type=Path, default=DEFAULT_OUTPUT_JSONL)
    parser.add_argument("--output-text", type=Path, default=DEFAULT_OUTPUT_TEXT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_packet(args.post_close_report)
    write_outputs(packet, args.output_jsonl, args.output_text)

    print(f"H024 post-close dashboard/readiness adapter verdict: {packet['verdict']}")
    print(f"Operator state: {packet['operator_state']}")
    print(f"Dashboard state: {packet['dashboard_state']}")
    print(f"Readiness state: {packet['readiness_state']}")
    print(f"Dashboard compatible: {packet['h024_dashboard_compatible']}")
    print(f"Readiness compatible: {packet['h024_readiness_compatible']}")
    print(f"Legacy open canary required: {packet.get('legacy_open_canary_required')}")
    print(f"Post-close no-open-canary accepted: {packet.get('post_close_no_open_canary_accepted')}")
    print(f"Exact ticket open: {packet.get('exact_ticket_open')}")
    print(f"H024 position count: {packet.get('h024_position_count')}")
    print(f"H024 order count: {packet.get('h024_order_count')}")
    print(f"Trading authorized: {packet['trading_authorized']}")
    print(f"Broker mutation authorized: {packet['broker_mutation_authorized']}")
    print(f"Violations: {len(packet.get('violations', []))}")

    return 0 if packet["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
