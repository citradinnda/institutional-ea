"""Build H024 post-close operational completion packet.

This is intentionally thin. It confirms that the H024 post-close observer and
dashboard/readiness adapters agree that the old canary absence is intentional.

It also emits the next operational target: move from post-close observer work to
demo automation readiness work, without reopening the old canary and without
performing broker mutation here.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "h024_post_close_operational_completion.v1"
STAGE = "H024_POST_CLOSE_OPERATIONAL_COMPLETION"

ACCOUNT_SERVER = "Exness-MT5Trial6"
SYMBOL = "XAUUSDm"
MODEL_SYMBOL = "XAUUSD"
EXACT_TICKET = 4413054432
EXACT_IDENTIFIER = 4413054432
MAGIC = 240024
VOLUME = 0.01

EXPECTED_STATE = "NO OPEN CANARY - INTENTIONALLY CLOSED BY H025"

DEFAULT_STATE_REPORT = Path("reports/h024_post_close_no_open_canary_state.jsonl")
DEFAULT_ADAPTER_REPORT = Path("reports/h024_post_close_dashboard_readiness_adapter.jsonl")
DEFAULT_OUTPUT_JSONL = Path("reports/h024_post_close_operational_completion.jsonl")
DEFAULT_OUTPUT_TEXT = Path("reports/h024_post_close_operational_completion.txt")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_last_jsonl(path: Path, label: str) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing {label} report: {path}")

    last_line = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            last_line = stripped

    if not last_line:
        raise ValueError(f"empty {label} report: {path}")

    parsed = json.loads(last_line)
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} JSONL record must be an object")

    return parsed


def build_packet(state_report_path: Path, adapter_report_path: Path) -> dict[str, Any]:
    violations: list[dict[str, str]] = []

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
        "state_report_path": str(state_report_path),
        "adapter_report_path": str(adapter_report_path),
        "read_only_completion_only": True,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "entry_authorized": False,
        "close_all_authorized": False,
        "live_money_authorized": False,
        "operator_next_action": "MOVE_TO_DEMO_AUTOMATION_READINESS_NO_TRADING_AUTHORIZED_BY_THIS_PACKET",
    }

    evidence: dict[str, dict[str, Any]] = {}

    for label, path in [
        ("state", state_report_path),
        ("adapter", adapter_report_path),
    ]:
        try:
            evidence[label] = read_last_jsonl(path, label)
        except Exception as exc:
            violations.append(
                {
                    "code": f"{label}_report_unreadable",
                    "severity": "ERROR",
                    "message": str(exc),
                }
            )

    if violations:
        packet.update(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_H024_POST_CLOSE_COMPLETION_EVIDENCE_UNAVAILABLE",
                "post_close_operational_state": "UNVERIFIED",
                "demo_automation_readiness_transition_allowed": False,
                "violations": violations,
            }
        )
        return packet

    state = evidence["state"]
    adapter = evidence["adapter"]

    packet.update(
        {
            "state_verdict": state.get("verdict"),
            "state_canary_absence_classification": state.get("canary_absence_classification"),
            "state_dashboard_wording": state.get("dashboard_wording"),
            "state_readiness_wording": state.get("readiness_wording"),
            "adapter_verdict": adapter.get("verdict"),
            "adapter_dashboard_state": adapter.get("dashboard_state"),
            "adapter_readiness_state": adapter.get("readiness_state"),
            "adapter_dashboard_compatible": adapter.get("h024_dashboard_compatible"),
            "adapter_readiness_compatible": adapter.get("h024_readiness_compatible"),
            "adapter_legacy_open_canary_required": adapter.get("legacy_open_canary_required"),
            "adapter_post_close_no_open_canary_accepted": adapter.get("post_close_no_open_canary_accepted"),
            "exact_ticket_open": state.get("exact_ticket_open"),
            "h024_position_count": state.get("h024_position_count"),
            "h024_order_count": state.get("h024_order_count"),
        }
    )

    expected_pairs = [
        ("state_verdict_not_pass", state.get("verdict"), "PASS"),
        ("state_absence_not_intentionally_closed", state.get("canary_absence_classification"), "INTENTIONALLY_CLOSED_BY_H025"),
        ("state_dashboard_wording_unexpected", state.get("dashboard_wording"), EXPECTED_STATE),
        ("state_readiness_wording_unexpected", state.get("readiness_wording"), EXPECTED_STATE),
        ("state_exact_ticket_open_not_false", state.get("exact_ticket_open"), False),
        ("state_h024_position_count_not_zero", state.get("h024_position_count"), 0),
        ("state_h024_order_count_not_zero", state.get("h024_order_count"), 0),
        ("adapter_verdict_not_pass", adapter.get("verdict"), "PASS"),
        ("adapter_dashboard_state_unexpected", adapter.get("dashboard_state"), EXPECTED_STATE),
        ("adapter_readiness_state_unexpected", adapter.get("readiness_state"), EXPECTED_STATE),
        ("adapter_dashboard_not_compatible", adapter.get("h024_dashboard_compatible"), True),
        ("adapter_readiness_not_compatible", adapter.get("h024_readiness_compatible"), True),
        ("adapter_legacy_open_canary_required_not_false", adapter.get("legacy_open_canary_required"), False),
        ("adapter_post_close_not_accepted", adapter.get("post_close_no_open_canary_accepted"), True),
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

    for label, record in evidence.items():
        if record.get("trading_authorized") is not False:
            violations.append(
                {
                    "code": f"{label}_trading_authorized_not_false",
                    "severity": "ERROR",
                    "message": f"{label} must not authorize trading.",
                }
            )
        if record.get("broker_mutation_authorized") is not False:
            violations.append(
                {
                    "code": f"{label}_broker_mutation_authorized_not_false",
                    "severity": "ERROR",
                    "message": f"{label} must not authorize broker mutation.",
                }
            )

    if violations:
        packet.update(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_H024_POST_CLOSE_OPERATIONAL_COMPLETION_UNVERIFIED",
                "post_close_operational_state": "UNVERIFIED",
                "demo_automation_readiness_transition_allowed": False,
                "violations": violations,
            }
        )
        return packet

    packet.update(
        {
            "verdict": "PASS",
            "operator_state": "H024_POST_CLOSE_OPERATIONAL_COMPLETION_ACCEPTED",
            "post_close_operational_state": EXPECTED_STATE,
            "dashboard_state": EXPECTED_STATE,
            "readiness_state": EXPECTED_STATE,
            "legacy_open_canary_required": False,
            "post_close_no_open_canary_accepted": True,
            "demo_automation_readiness_transition_allowed": True,
            "demo_automation_next_target": "DEMO_AUTOMATION_READINESS_BRIDGE",
            "demo_automation_blockers_remaining": [
                "define one-shot demo entry authorization scope",
                "define exact symbols allowed for demo automation",
                "define strategy signal source and model artifact checks",
                "define deterministic risk engine checks",
                "define portfolio heat limits",
                "define spread/slippage/pre-trade condition logging",
                "define kill-switch and fail-closed behavior",
                "define operator approval artifact for first controlled demo entry",
            ],
            "operator_next_action": "BUILD_DEMO_AUTOMATION_READINESS_BRIDGE_NO_TRADING_AUTHORIZED_YET",
            "violations": [],
        }
    )
    return packet


def write_outputs(packet: dict[str, Any], output_jsonl: Path, output_text: Path) -> None:
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_text.parent.mkdir(parents=True, exist_ok=True)

    output_jsonl.write_text(json.dumps(packet, sort_keys=True) + "\n", encoding="utf-8")

    blockers = packet.get("demo_automation_blockers_remaining", [])
    if not isinstance(blockers, list):
        blockers = []

    lines = [
        "H024 post-close operational completion",
        f"Verdict: {packet.get('verdict')}",
        f"Operator state: {packet.get('operator_state')}",
        f"Post-close operational state: {packet.get('post_close_operational_state')}",
        f"Dashboard state: {packet.get('dashboard_state')}",
        f"Readiness state: {packet.get('readiness_state')}",
        f"Exact ticket open: {packet.get('exact_ticket_open')}",
        f"H024 position count: {packet.get('h024_position_count')}",
        f"H024 order count: {packet.get('h024_order_count')}",
        f"Trading authorized: {packet.get('trading_authorized')}",
        f"Broker mutation authorized: {packet.get('broker_mutation_authorized')}",
        f"Demo automation readiness transition allowed: {packet.get('demo_automation_readiness_transition_allowed')}",
        f"Demo automation next target: {packet.get('demo_automation_next_target')}",
        f"Violations: {len(packet.get('violations', []))}",
        "",
        "Remaining demo automation blockers:",
    ]

    if blockers:
        lines.extend(f"- {blocker}" for blocker in blockers)
    else:
        lines.append("- unavailable until packet PASS")

    output_text.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-report", type=Path, default=DEFAULT_STATE_REPORT)
    parser.add_argument("--adapter-report", type=Path, default=DEFAULT_ADAPTER_REPORT)
    parser.add_argument("--output-jsonl", type=Path, default=DEFAULT_OUTPUT_JSONL)
    parser.add_argument("--output-text", type=Path, default=DEFAULT_OUTPUT_TEXT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_packet(args.state_report, args.adapter_report)
    write_outputs(packet, args.output_jsonl, args.output_text)

    print(f"H024 post-close operational completion verdict: {packet['verdict']}")
    print(f"Operator state: {packet['operator_state']}")
    print(f"Post-close operational state: {packet['post_close_operational_state']}")
    print(f"Dashboard state: {packet.get('dashboard_state')}")
    print(f"Readiness state: {packet.get('readiness_state')}")
    print(f"Exact ticket open: {packet.get('exact_ticket_open')}")
    print(f"H024 position count: {packet.get('h024_position_count')}")
    print(f"H024 order count: {packet.get('h024_order_count')}")
    print(f"Trading authorized: {packet['trading_authorized']}")
    print(f"Broker mutation authorized: {packet['broker_mutation_authorized']}")
    print(f"Demo automation transition allowed: {packet['demo_automation_readiness_transition_allowed']}")
    print(f"Demo automation next target: {packet.get('demo_automation_next_target')}")
    print(f"Violations: {len(packet.get('violations', []))}")

    return 0 if packet["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
