"""Build H024_STANDARD_DEMO_EXISTING_PATH_MAP.

This is a read-only repository inspection packet.

Purpose:
- Rejoin the existing H024 standard-demo execution path.
- Identify the shortest existing route toward controlled demo order_check/order_send.
- Avoid building parallel standalone scaffolding.
- Avoid broker mutation, broker imports, symbol selection, executable request construction,
  order checks, and order sends.

This script inspects tracked source/docs/tests by path and by static text only.
It writes local reports under reports/.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "h024_standard_demo_existing_path_map.v1"
STAGE = "H024_STANDARD_DEMO_EXISTING_PATH_MAP"

DEFAULT_OUTPUT_JSONL = Path("reports/h024_standard_demo_existing_path_map.jsonl")
DEFAULT_OUTPUT_TEXT = Path("reports/h024_standard_demo_existing_path_map.txt")

# Constructed this way so the read-only self-test can search for the actual
# forbidden source snippets without matching the marker list itself.
FORBIDDEN_SELF_SNIPPETS = [
    "import " + "MetaTrader5",
    "from " + "MetaTrader5",
    "mt5" + ".",
    "order_" + "check(",
    "order_" + "send(",
    "symbol_" + "select(",
    "TRADE_" + "ACTION_DEAL",
    "TRADE_" + "ACTION_PENDING",
    "ORDER_" + "TYPE_BUY",
    "ORDER_" + "TYPE_SELL",
]

EXPECTED_ALLOWED_MODEL_SYMBOLS = ["USDJPY", "XAUUSD"]
EXPECTED_ALLOWED_RUNTIME_SYMBOLS = ["USDJPYm", "XAUUSDm"]

CORE_SOURCE_COMPONENTS = [
    {
        "id": "strategy_source",
        "path": "quantcore/strategy/h020.py",
        "role": "Existing strategy/entry-source module feeding H024 intent research path.",
        "required_keywords": ["get_default_cost_spec"],
        "order": 10,
    },
    {
        "id": "order_intent_simulation",
        "path": "quantcore/execution/h024_order_intent_simulation.py",
        "role": "Existing H024 order-intent simulation and action-intent validation layer.",
        "required_keywords": ["SUPPORTED_NORMALIZED_SYMBOLS", "normalized_symbol", "symbol_normalization_mismatch"],
        "order": 20,
    },
    {
        "id": "dry_run",
        "path": "quantcore/execution/h024_dry_run.py",
        "role": "Existing broker-aware dry-run candidate conversion layer.",
        "required_keywords": ["SYMBOL_MAPPING", "model_symbol", "broker_symbol"],
        "order": 30,
    },
    {
        "id": "dry_run_log",
        "path": "quantcore/execution/h024_dry_run_log.py",
        "role": "Existing dry-run action export/log layer.",
        "required_keywords": ["model_symbol", "broker_symbol"],
        "order": 40,
    },
    {
        "id": "manual_approval_checkpoint",
        "path": "quantcore/execution/h024_manual_approval_checkpoint.py",
        "role": "Existing manual/operator approval checkpoint before any order-capable transition.",
        "required_keywords": ["USDJPY", "XAUUSD", "approval"],
        "order": 50,
    },
    {
        "id": "broker_request_draft_envelope",
        "path": "quantcore/execution/h024_broker_request_draft_envelope.py",
        "role": "Existing broker request draft/envelope layer before MT5 request-shape preview.",
        "required_keywords": ["preview_envelope", "normalized_symbol", "model_symbol"],
        "order": 60,
    },
]

SAFETY_SOURCE_COMPONENTS = [
    {
        "id": "runtime_safety_lockout",
        "path": "quantcore/execution/h024_runtime_safety_lockout.py",
        "role": "Existing runtime lockout reader/checker.",
        "required_keywords": ["MODEL_SYMBOLS", "XAUUSD", "USDJPY"],
    },
    {
        "id": "runtime_tick_spread_safety",
        "path": "quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py",
        "role": "Existing tick/spread safety supervisor.",
        "required_keywords": ["model_symbol", "XAUUSD", "USDJPY"],
    },
    {
        "id": "runtime_exposure_inventory_safety",
        "path": "quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py",
        "role": "Existing exposure inventory safety supervisor.",
        "required_keywords": ["model_symbol", "runtime_symbol"],
    },
    {
        "id": "safety_supervisor_spec",
        "path": "quantcore/execution/h024_safety_supervisor_spec.py",
        "role": "Existing H024 safety-supervisor specification.",
        "required_keywords": ["MODEL_SYMBOLS", "RUNTIME_SYMBOLS", "circuit_breakers"],
    },
]

STANDARD_DEMO_DOC_COMPONENTS = [
    {
        "id": "demo_adapter_design",
        "path": "docs/operations/H024_DEMO_EXECUTION_ADAPTER_DESIGN_SPEC.md",
        "role": "Existing demo execution adapter design spec.",
    },
    {
        "id": "standard_demo_order_intent_simulation_result",
        "path": "docs/operations/H024_STANDARD_DEMO_ORDER_INTENT_SIMULATION_RESULT.md",
        "role": "Existing standard-demo order-intent simulation result.",
    },
    {
        "id": "standard_demo_order_readiness_packet_result",
        "path": "docs/operations/H024_STANDARD_DEMO_ORDER_READINESS_PACKET_RESULT.md",
        "role": "Existing standard-demo order-readiness packet result.",
    },
    {
        "id": "standard_demo_manual_approval_checkpoint_result",
        "path": "docs/operations/H024_STANDARD_DEMO_MANUAL_APPROVAL_CHECKPOINT_RESULT.md",
        "role": "Existing standard-demo manual approval checkpoint result.",
    },
    {
        "id": "standard_demo_broker_request_draft_envelope_result",
        "path": "docs/operations/H024_STANDARD_DEMO_BROKER_REQUEST_DRAFT_ENVELOPE_RESULT.md",
        "role": "Existing standard-demo broker request draft envelope result.",
    },
    {
        "id": "standard_demo_mt5_request_shape_preview_envelope_result",
        "path": "docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md",
        "role": "Existing standard-demo MT5 request-shape preview envelope result.",
    },
    {
        "id": "standard_demo_order_canary_human_approval_result",
        "path": "docs/operations/H024_STANDARD_DEMO_ORDER_CANARY_HUMAN_APPROVAL_RESULT.md",
        "role": "Existing standard-demo order canary human approval result.",
    },
]

TEST_COMPONENTS = [
    {
        "id": "test_order_intent_simulation",
        "path": "tests/test_h024_order_intent_simulation.py",
        "role": "Tests for H024 order-intent simulation.",
    },
    {
        "id": "test_dry_run_execution",
        "path": "tests/test_h024_dry_run_execution.py",
        "role": "Tests for H024 dry-run execution semantics.",
    },
    {
        "id": "test_dry_run_log",
        "path": "tests/test_h024_dry_run_log.py",
        "role": "Tests for H024 dry-run log/export behavior.",
    },
    {
        "id": "test_dry_run_action_verifier",
        "path": "tests/test_h024_dry_run_action_verifier.py",
        "role": "Tests for H024 dry-run action verifier.",
    },
    {
        "id": "test_manual_approval_checkpoint",
        "path": "tests/test_h024_manual_approval_checkpoint.py",
        "role": "Tests for H024 manual approval checkpoint.",
    },
    {
        "id": "test_runtime_safety_lockout",
        "path": "tests/test_h024_runtime_safety_lockout.py",
        "role": "Tests for H024 runtime safety lockout.",
    },
    {
        "id": "test_runtime_tick_spread_safety",
        "path": "tests/test_h024_runtime_tick_spread_safety_supervisor.py",
        "role": "Tests for H024 runtime tick/spread safety supervisor.",
    },
    {
        "id": "test_runtime_exposure_inventory_safety",
        "path": "tests/test_h024_runtime_exposure_inventory_safety_supervisor.py",
        "role": "Tests for H024 runtime exposure inventory safety supervisor.",
    },
    {
        "id": "test_safety_supervisor_spec",
        "path": "tests/test_h024_safety_supervisor_spec.py",
        "role": "Tests for H024 safety supervisor spec.",
    },
]


@dataclass(frozen=True)
class ComponentResult:
    id: str
    path: str
    role: str
    exists: bool
    required_keywords: list[str]
    missing_keywords: list[str]
    order: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "path": self.path,
            "role": self.role,
            "exists": self.exists,
            "required_keywords": self.required_keywords,
            "missing_keywords": self.missing_keywords,
            "order": self.order,
        }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_repo_path(repo_root: Path, relative_path: str) -> Path:
    return repo_root / relative_path


def read_text_or_empty(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def inspect_component(spec: dict[str, Any], repo_root: Path) -> ComponentResult:
    relative_path = str(spec["path"])
    absolute_path = resolve_repo_path(repo_root, relative_path)
    required_keywords = list(spec.get("required_keywords", []))
    text = read_text_or_empty(absolute_path)
    missing_keywords = [keyword for keyword in required_keywords if keyword not in text]

    return ComponentResult(
        id=str(spec["id"]),
        path=relative_path,
        role=str(spec["role"]),
        exists=absolute_path.exists(),
        required_keywords=required_keywords,
        missing_keywords=missing_keywords,
        order=spec.get("order"),
    )


def component_violations(prefix: str, components: list[ComponentResult]) -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []

    for component in components:
        if not component.exists:
            violations.append(
                {
                    "code": f"{prefix}_{component.id}_missing",
                    "severity": "ERROR",
                    "message": f"Required component is missing: {component.path}",
                }
            )
        if component.missing_keywords:
            violations.append(
                {
                    "code": f"{prefix}_{component.id}_keywords_missing",
                    "severity": "ERROR",
                    "message": f"{component.path} missing static markers: {component.missing_keywords}",
                }
            )

    return violations


def static_forbidden_hits(path: Path, forbidden: list[str]) -> list[str]:
    text = read_text_or_empty(path)
    return [snippet for snippet in forbidden if snippet in text]


def build_packet(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    violations: list[dict[str, str]] = []

    core_components = [inspect_component(spec, repo_root) for spec in CORE_SOURCE_COMPONENTS]
    safety_components = [inspect_component(spec, repo_root) for spec in SAFETY_SOURCE_COMPONENTS]
    standard_demo_docs = [inspect_component(spec, repo_root) for spec in STANDARD_DEMO_DOC_COMPONENTS]
    tests = [inspect_component(spec, repo_root) for spec in TEST_COMPONENTS]

    violations.extend(component_violations("core", core_components))
    violations.extend(component_violations("safety", safety_components))
    violations.extend(component_violations("standard_demo_doc", standard_demo_docs))
    violations.extend(component_violations("test", tests))

    self_path = Path(__file__)
    self_forbidden_hits = static_forbidden_hits(self_path, FORBIDDEN_SELF_SNIPPETS)
    if self_forbidden_hits:
        violations.append(
            {
                "code": "path_map_script_contains_broker_execution_api",
                "severity": "ERROR",
                "message": f"This read-only path map script contains forbidden snippets: {self_forbidden_hits}",
            }
        )

    shortest_existing_route = [
        {
            "step": 1,
            "name": "order_intent_simulation",
            "source": "quantcore/execution/h024_order_intent_simulation.py",
            "purpose": "Produce/validate H024 standard-demo action intent using normalized symbols.",
            "mutation": False,
        },
        {
            "step": 2,
            "name": "dry_run",
            "source": "quantcore/execution/h024_dry_run.py",
            "purpose": "Convert valid model-symbol intent into broker-aware dry-run candidate facts.",
            "mutation": False,
        },
        {
            "step": 3,
            "name": "dry_run_log_and_verifier",
            "source": "quantcore/execution/h024_dry_run_log.py",
            "purpose": "Export and verify dry-run action evidence.",
            "mutation": False,
        },
        {
            "step": 4,
            "name": "runtime_safety_supervisors",
            "source": "quantcore/execution/h024_runtime_*_safety_supervisor.py",
            "purpose": "Check lockout, tick/spread, exposure, account/risk/margin, and safety-spec gates.",
            "mutation": False,
        },
        {
            "step": 5,
            "name": "manual_approval_checkpoint",
            "source": "quantcore/execution/h024_manual_approval_checkpoint.py",
            "purpose": "Require explicit operator checkpoint before any order-capable transition.",
            "mutation": False,
        },
        {
            "step": 6,
            "name": "broker_request_draft_envelope",
            "source": "quantcore/execution/h024_broker_request_draft_envelope.py",
            "purpose": "Produce request-like draft/envelope for review without broker mutation.",
            "mutation": False,
        },
        {
            "step": 7,
            "name": "mt5_request_shape_preview",
            "source": "docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md",
            "purpose": "Validate MT5 request shape semantics before any order-capable gate.",
            "mutation": False,
        },
        {
            "step": 8,
            "name": "future_demo_order_check_gate",
            "source": "not implemented by this packet",
            "purpose": "Next future order-capable step: demo-only order_check behind fresh explicit operator approval.",
            "mutation": "future_only_requires_new_explicit_operator_authorization",
        },
        {
            "step": 9,
            "name": "future_one_shot_demo_order_send_gate",
            "source": "not implemented by this packet",
            "purpose": "Later future step: one-shot demo order_send behind separate explicit operator approval.",
            "mutation": "future_only_requires_new_explicit_operator_authorization",
        },
    ]

    packet: dict[str, Any] = {
        "schema": SCHEMA,
        "stage": STAGE,
        "generated_at_utc": utc_now_iso(),
        "repo_root": str(repo_root),
        "read_only_path_map_only": True,
        "standalone_scaffold_rejected": True,
        "strategy_hypothesis_id_allocated": False,
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "entry_authorized": False,
        "close_all_authorized": False,
        "live_money_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "symbol_select_authorized": False,
        "executable_trade_request_authorized": False,
        "executable_trade_request_constructed": False,
        "allowed_model_symbols": EXPECTED_ALLOWED_MODEL_SYMBOLS,
        "allowed_runtime_symbols": EXPECTED_ALLOWED_RUNTIME_SYMBOLS,
        "core_components": [component.to_dict() for component in core_components],
        "safety_components": [component.to_dict() for component in safety_components],
        "standard_demo_docs": [component.to_dict() for component in standard_demo_docs],
        "tests": [component.to_dict() for component in tests],
        "shortest_existing_route_to_controlled_demo_order_check_order_send": shortest_existing_route,
        "next_target": "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY",
        "operator_next_action": "RUN_EXISTING_H024_STANDARD_DEMO_PATH_REPLAY_BEFORE_ANY_ORDER_CAPABLE_STEP",
        "demo_order_check_gate_requires_new_explicit_operator_approval": True,
        "demo_order_send_gate_requires_separate_future_operator_approval": True,
        "violations": violations,
    }

    if violations:
        packet.update(
            {
                "verdict": "FAIL_CLOSED",
                "operator_state": "FAIL_CLOSED_H024_STANDARD_DEMO_EXISTING_PATH_MAP_INCOMPLETE",
                "existing_path_map_state": "INCOMPLETE",
                "ready_for_existing_path_replay": False,
                "ready_for_demo_order_check_gate": False,
            }
        )
        return packet

    packet.update(
        {
            "verdict": "PASS",
            "operator_state": "H024_STANDARD_DEMO_EXISTING_PATH_MAP_ACCEPTED",
            "existing_path_map_state": "REAL_H024_STANDARD_DEMO_PATH_IDENTIFIED",
            "ready_for_existing_path_replay": True,
            "ready_for_demo_order_check_gate": False,
        }
    )
    return packet


def write_outputs(packet: dict[str, Any], output_jsonl: Path, output_text: Path) -> None:
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    output_text.parent.mkdir(parents=True, exist_ok=True)

    output_jsonl.write_text(json.dumps(packet, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "H024_STANDARD_DEMO_EXISTING_PATH_MAP",
        f"Verdict: {packet.get('verdict')}",
        f"Operator state: {packet.get('operator_state')}",
        f"Existing path map state: {packet.get('existing_path_map_state')}",
        f"Ready for existing path replay: {packet.get('ready_for_existing_path_replay')}",
        f"Ready for demo order_check gate: {packet.get('ready_for_demo_order_check_gate')}",
        f"Next target: {packet.get('next_target')}",
        f"Trading authorized: {packet.get('trading_authorized')}",
        f"Broker mutation authorized: {packet.get('broker_mutation_authorized')}",
        f"Order check authorized: {packet.get('order_check_authorized')}",
        f"Order send authorized: {packet.get('order_send_authorized')}",
        f"Symbol select authorized: {packet.get('symbol_select_authorized')}",
        f"Executable trade request constructed: {packet.get('executable_trade_request_constructed')}",
        f"Violations: {len(packet.get('violations', []))}",
        "",
        "Shortest existing route:",
    ]

    route = packet.get("shortest_existing_route_to_controlled_demo_order_check_order_send", [])
    if isinstance(route, list):
        for step in route:
            if isinstance(step, dict):
                lines.append(
                    f"{step.get('step')}. {step.get('name')} -> {step.get('source')} :: {step.get('purpose')}"
                )

    lines.append("")
    lines.append("Core components:")
    for component in packet.get("core_components", []):
        if isinstance(component, dict):
            lines.append(f"- {component.get('id')}: {component.get('path')} exists={component.get('exists')}")

    lines.append("")
    lines.append("Safety components:")
    for component in packet.get("safety_components", []):
        if isinstance(component, dict):
            lines.append(f"- {component.get('id')}: {component.get('path')} exists={component.get('exists')}")

    lines.append("")
    lines.append("Standard-demo docs:")
    for component in packet.get("standard_demo_docs", []):
        if isinstance(component, dict):
            lines.append(f"- {component.get('id')}: {component.get('path')} exists={component.get('exists')}")

    output_text.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-jsonl", type=Path, default=DEFAULT_OUTPUT_JSONL)
    parser.add_argument("--output-text", type=Path, default=DEFAULT_OUTPUT_TEXT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    packet = build_packet(args.repo_root)
    write_outputs(packet, args.output_jsonl, args.output_text)

    print(f"H024_STANDARD_DEMO_EXISTING_PATH_MAP verdict: {packet['verdict']}")
    print(f"Operator state: {packet['operator_state']}")
    print(f"Existing path map state: {packet['existing_path_map_state']}")
    print(f"Ready for existing path replay: {packet['ready_for_existing_path_replay']}")
    print(f"Ready for demo order_check gate: {packet['ready_for_demo_order_check_gate']}")
    print(f"Next target: {packet['next_target']}")
    print(f"Trading authorized: {packet['trading_authorized']}")
    print(f"Broker mutation authorized: {packet['broker_mutation_authorized']}")
    print(f"Order check authorized: {packet['order_check_authorized']}")
    print(f"Order send authorized: {packet['order_send_authorized']}")
    print(f"Symbol select authorized: {packet['symbol_select_authorized']}")
    print(f"Executable trade request constructed: {packet['executable_trade_request_constructed']}")
    print(f"Violations: {len(packet.get('violations', []))}")

    return 0 if packet["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

