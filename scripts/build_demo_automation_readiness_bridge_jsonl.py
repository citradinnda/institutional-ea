"""Build DEMO_AUTOMATION_READINESS_BRIDGE packet.

This is an operational bridge, not a strategy hypothesis.

It consumes H024 post-close operational completion and opens the next practical
track toward controlled demo automation:

INERT_DEMO_ENTRY_REQUEST_PREVIEW

This bridge does not authorize trading, broker mutation, executable request
construction, order checks, order sends, symbol selection, new entries, loops,
or live-money support.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "demo_automation_readiness_bridge.v1"
STAGE = "DEMO_AUTOMATION_READINESS_BRIDGE"

ACCOUNT_SERVER = "Exness-MT5Trial6"
EXPECTED_POST_CLOSE_STATE = "NO OPEN CANARY - INTENTIONALLY CLOSED BY H025"

ALLOWED_DEMO_SYMBOLS = ["USDJPYm", "XAUUSDm"]
BANNED_SYMBOLS = ["EURUSDm", "GBPUSDm", "US500m"]

MAX_RISK_PER_TRADE_PCT = 0.5
MAX_PORTFOLIO_HEAT_PCT = 1.0

DEFAULT_COMPLETION_REPORT = Path("reports/h024_post_close_operational_completion.jsonl")
DEFAULT_OUTPUT_JSONL = Path("reports/demo_automation_readiness_bridge.jsonl")
DEFAULT_OUTPUT_TEXT = Path("reports/demo_automation_readiness_bridge.txt")


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


def build_packet(completion_report_path: Path) -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    completion: dict[str, Any] | None = None

    packet: dict[str, Any] = {
        "schema": SCHEMA,
        "stage": STAGE,
        "generated_at_utc": utc_now_iso(),
        "account_server": ACCOUNT_SERVER,
        "completion_report_path": str(completion_report_path),
        "operational_bridge_only": True,
        "strategy_hypothesis_id_allocated": False,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "entry_authorized": False,
        "close_all_authorized": False,
        "live_money_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "symbol_select_authorized": False,
        "unattended_loop_authorized": False,
        "executable_trade_request_authorized": False,
        "allowed_demo_symbols": ALLOWED_DEMO_SYMBOLS,
        "banned_symbols": BANNED_SYMBOLS,
        "max_risk_per_trade_pct": MAX_RISK_PER_TRADE_PCT,
        "max_portfolio_heat_pct": MAX_PORTFOLIO_HEAT_PCT,
        "next_target": "INERT_DEMO_ENTRY_REQUEST_PREVIEW",
        "operator_next_action": "BUILD_INERT_DEMO_ENTRY_REQUEST_PREVIEW_NO_TRADING_AUTHORIZED",
    }

    try:
        completion = read_last_jsonl(completion_report_path, "H024 post-close completion")
    except Exception as exc:
        violations.append(
            {
                "code": "completion_report_unreadable",
                "severity": "ERROR",
                "message": str(exc),
            }
        )

    if completion is None:
        packet.update(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_DEMO_AUTOMATION_BRIDGE_COMPLETION_EVIDENCE_UNAVAILABLE",
                "demo_automation_bridge_state": "UNVERIFIED",
                "ready_for_inert_demo_entry_preview": False,
                "violations": violations,
            }
        )
        return packet

    packet.update(
        {
            "completion_verdict": completion.get("verdict"),
            "completion_operator_state": completion.get("operator_state"),
            "post_close_operational_state": completion.get("post_close_operational_state"),
            "completion_transition_allowed": completion.get("demo_automation_readiness_transition_allowed"),
            "completion_next_target": completion.get("demo_automation_next_target"),
            "exact_ticket_open": completion.get("exact_ticket_open"),
            "h024_position_count": completion.get("h024_position_count"),
            "h024_order_count": completion.get("h024_order_count"),
            "completion_trading_authorized": completion.get("trading_authorized"),
            "completion_broker_mutation_authorized": completion.get("broker_mutation_authorized"),
        }
    )

    expected_pairs = [
        ("completion_verdict_not_pass", completion.get("verdict"), "PASS"),
        (
            "completion_operator_state_unexpected",
            completion.get("operator_state"),
            "H024_POST_CLOSE_OPERATIONAL_COMPLETION_ACCEPTED",
        ),
        (
            "post_close_operational_state_unexpected",
            completion.get("post_close_operational_state"),
            EXPECTED_POST_CLOSE_STATE,
        ),
        (
            "completion_transition_not_allowed",
            completion.get("demo_automation_readiness_transition_allowed"),
            True,
        ),
        (
            "completion_next_target_unexpected",
            completion.get("demo_automation_next_target"),
            "DEMO_AUTOMATION_READINESS_BRIDGE",
        ),
        ("exact_ticket_open_not_false", completion.get("exact_ticket_open"), False),
        ("h024_position_count_not_zero", completion.get("h024_position_count"), 0),
        ("h024_order_count_not_zero", completion.get("h024_order_count"), 0),
        ("completion_trading_authorized_not_false", completion.get("trading_authorized"), False),
        ("completion_broker_mutation_authorized_not_false", completion.get("broker_mutation_authorized"), False),
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
                "operator_state": "FAIL_CLOSED_DEMO_AUTOMATION_BRIDGE_UNVERIFIED",
                "demo_automation_bridge_state": "UNVERIFIED",
                "ready_for_inert_demo_entry_preview": False,
                "violations": violations,
            }
        )
        return packet

    packet.update(
        {
            "verdict": "PASS",
            "operator_state": "DEMO_AUTOMATION_READINESS_BRIDGE_ACCEPTED",
            "demo_automation_bridge_state": "READY_FOR_INERT_DEMO_ENTRY_REQUEST_PREVIEW",
            "ready_for_inert_demo_entry_preview": True,
            "controlled_demo_automation_track_open": True,
            "first_order_capable_step_authorized": False,
            "required_inert_preview_fields": [
                "account_server",
                "symbol",
                "model_symbol",
                "strategy_signal_source",
                "model_artifact_manifest",
                "live_candle_parity_snapshot",
                "entry_side_preview",
                "volume_preview",
                "risk_per_trade_pct_preview",
                "portfolio_heat_pct_preview",
                "atr_stop_distance_preview",
                "spread_snapshot",
                "slippage_assumption",
                "kill_switch_state",
                "operator_approval_required_for_any_future_order_check",
            ],
            "required_pre_demo_execution_gates": [
                "model artifact manifest loads",
                "live candle schema matches training schema",
                "strategy signal source produces one deterministic signal snapshot",
                "risk engine dry-run returns valid stop distance and position size",
                "portfolio heat dry-run is within configured cap",
                "spread and tick-age snapshot are logged",
                "kill-switch is present and defaults to block",
                "operator approval artifact exists before any future order-capable step",
            ],
            "operator_next_action": "IMPLEMENT_INERT_DEMO_ENTRY_REQUEST_PREVIEW_NO_TRADING_AUTHORIZED",
            "violations": [],
        }
    )
    return packet


def write_outputs(packet: dict[str, Any], output_jsonl: Path, output_text: Path) -> None:
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_text.parent.mkdir(parents=True, exist_ok=True)

    output_jsonl.write_text(json.dumps(packet, sort_keys=True) + "\n", encoding="utf-8")

    preview_fields = packet.get("required_inert_preview_fields", [])
    gates = packet.get("required_pre_demo_execution_gates", [])

    if not isinstance(preview_fields, list):
        preview_fields = []
    if not isinstance(gates, list):
        gates = []

    lines = [
        "DEMO_AUTOMATION_READINESS_BRIDGE",
        f"Verdict: {packet.get('verdict')}",
        f"Operator state: {packet.get('operator_state')}",
        f"Bridge state: {packet.get('demo_automation_bridge_state')}",
        f"Ready for inert demo entry preview: {packet.get('ready_for_inert_demo_entry_preview')}",
        f"Controlled demo automation track open: {packet.get('controlled_demo_automation_track_open')}",
        f"Next target: {packet.get('next_target')}",
        f"Allowed demo symbols: {', '.join(packet.get('allowed_demo_symbols', []))}",
        f"Banned symbols: {', '.join(packet.get('banned_symbols', []))}",
        f"Max risk per trade pct: {packet.get('max_risk_per_trade_pct')}",
        f"Max portfolio heat pct: {packet.get('max_portfolio_heat_pct')}",
        f"Trading authorized: {packet.get('trading_authorized')}",
        f"Broker mutation authorized: {packet.get('broker_mutation_authorized')}",
        f"Order check authorized: {packet.get('order_check_authorized')}",
        f"Order send authorized: {packet.get('order_send_authorized')}",
        f"Symbol select authorized: {packet.get('symbol_select_authorized')}",
        f"Violations: {len(packet.get('violations', []))}",
        "",
        "Required inert preview fields:",
    ]

    if preview_fields:
        lines.extend(f"- {field}" for field in preview_fields)
    else:
        lines.append("- unavailable until bridge PASS")

    lines.append("")
    lines.append("Required pre-demo execution gates:")

    if gates:
        lines.extend(f"- {gate}" for gate in gates)
    else:
        lines.append("- unavailable until bridge PASS")

    output_text.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--completion-report", type=Path, default=DEFAULT_COMPLETION_REPORT)
    parser.add_argument("--output-jsonl", type=Path, default=DEFAULT_OUTPUT_JSONL)
    parser.add_argument("--output-text", type=Path, default=DEFAULT_OUTPUT_TEXT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_packet(args.completion_report)
    write_outputs(packet, args.output_jsonl, args.output_text)

    print(f"DEMO_AUTOMATION_READINESS_BRIDGE verdict: {packet['verdict']}")
    print(f"Operator state: {packet['operator_state']}")
    print(f"Bridge state: {packet['demo_automation_bridge_state']}")
    print(f"Ready for inert demo entry preview: {packet['ready_for_inert_demo_entry_preview']}")
    print(f"Controlled demo automation track open: {packet.get('controlled_demo_automation_track_open')}")
    print(f"Next target: {packet['next_target']}")
    print(f"Allowed demo symbols: {packet['allowed_demo_symbols']}")
    print(f"Banned symbols: {packet['banned_symbols']}")
    print(f"Max risk per trade pct: {packet['max_risk_per_trade_pct']}")
    print(f"Max portfolio heat pct: {packet['max_portfolio_heat_pct']}")
    print(f"Trading authorized: {packet['trading_authorized']}")
    print(f"Broker mutation authorized: {packet['broker_mutation_authorized']}")
    print(f"Order check authorized: {packet['order_check_authorized']}")
    print(f"Order send authorized: {packet['order_send_authorized']}")
    print(f"Symbol select authorized: {packet['symbol_select_authorized']}")
    print(f"Violations: {len(packet.get('violations', []))}")

    return 0 if packet["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
