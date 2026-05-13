from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"

REPLAY_REPORT = REPORTS_DIR / "h024_standard_demo_existing_path_replay.jsonl"
DESIGN_JSONL = REPORTS_DIR / "h024_standard_demo_order_check_gate_design.jsonl"
DESIGN_TXT = REPORTS_DIR / "h024_standard_demo_order_check_gate_design.txt"

STAGE = "H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN"

EXPECTED_REPLAY_FIELDS: dict[str, Any] = {
    "verdict": "PASS",
    "stage": "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY",
    "operator_state": "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_ACCEPTED",
    "existing_path_replay_state": "REAL_H024_STANDARD_DEMO_PATH_REPLAYED_READ_ONLY",
    "ready_for_existing_path_replay": True,
    "ready_for_demo_order_check_gate": False,
    "ready_for_demo_order_check_gate_design": True,
    "trading_authorized": False,
    "broker_mutation_authorized": False,
    "order_check_authorized": False,
    "order_send_authorized": False,
    "symbol_select_authorized": False,
    "executable_trade_request_constructed": False,
    "new_entry_authorized": False,
    "close_modify_authorized": False,
    "read_only_replay_only": True,
}

REQUIRED_EXISTING_ARTIFACTS = [
    "scripts/build_h024_standard_demo_existing_path_replay_jsonl.py",
    "tests/test_h024_standard_demo_existing_path_replay.py",
    "docs/operations/H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_RUNBOOK.md",
    "docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md",
    "docs/operations/H024_STANDARD_DEMO_ORDER_CANARY_HUMAN_APPROVAL_RESULT.md",
    "docs/operations/H024_STANDARD_DEMO_BROKER_REQUEST_DRAFT_ENVELOPE_RESULT.md",
    "quantcore/execution/h024_broker_request_draft_envelope.py",
    "quantcore/execution/h024_manual_approval_checkpoint.py",
    "quantcore/execution/h024_runtime_safety_lockout.py",
    "quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py",
    "quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py",
    "quantcore/execution/h024_runtime_account_risk_margin_safety_supervisor.py",
    "quantcore/execution/h024_runtime_no_mutation_safety_gate.py",
    "quantcore/execution/h024_safety_supervisor_spec.py",
]

FOCUSED_DESIGN_TEST_TARGETS = [
    "tests/test_h024_standard_demo_existing_path_map.py",
    "tests/test_h024_standard_demo_existing_path_replay.py",
    "tests/test_h024_standard_demo_order_check_gate_design.py",
]

ALLOWED_DEMO_SYMBOLS = ["USDJPYm", "XAUUSDm"]
BANNED_SYMBOLS = ["EURUSDm", "GBPUSDm", "US500m"]

FUTURE_GATE_SCHEMA = {
    "schema_name": "h024_standard_demo_order_check_gate_candidate_v1",
    "purpose": "future_demo_only_order_check_preflight_after_explicit_operator_authorization",
    "required_inputs": [
        "operator_authorization_packet",
        "operator_authorization_id",
        "authorization_scope",
        "authorization_created_at_utc",
        "authorization_expires_at_utc",
        "existing_path_replay_report",
        "broker_request_draft_envelope_artifact",
        "manual_approval_checkpoint_artifact",
        "runtime_safety_lockout_artifact",
        "runtime_tick_spread_safety_artifact",
        "runtime_exposure_inventory_safety_artifact",
        "runtime_account_risk_margin_safety_artifact",
        "runtime_no_mutation_safety_gate_artifact",
        "symbol",
        "model_symbol",
        "runtime_symbol",
        "side",
        "volume",
        "demo_server",
        "account_mode",
        "max_risk_per_trade_pct",
        "max_portfolio_heat_pct",
    ],
    "required_operator_authorization_scope": "H024_STANDARD_DEMO_ORDER_CHECK_GATE_ONLY",
    "allowed_account_mode": "demo_only",
    "allowed_symbols": ALLOWED_DEMO_SYMBOLS,
    "banned_symbols": BANNED_SYMBOLS,
    "max_risk_per_trade_pct": 0.5,
    "max_portfolio_heat_pct": 1.0,
    "freshness_requirements": {
        "operator_authorization_max_age_seconds": 900,
        "runtime_safety_artifacts_max_age_seconds": 300,
        "broker_request_draft_envelope_max_age_seconds": 300,
    },
    "fail_closed_conditions": [
        "missing_or_malformed_operator_authorization_packet",
        "ambiguous_operator_authorization_scope",
        "expired_operator_authorization",
        "authorization_scope_not_exactly_h024_standard_demo_order_check_gate_only",
        "existing_path_replay_not_pass",
        "manual_approval_checkpoint_missing_or_not_pass",
        "broker_request_draft_envelope_missing_or_not_pass",
        "runtime_safety_artifact_missing_malformed_stale_or_not_pass",
        "symbol_not_in_allowed_demo_symbols",
        "symbol_in_banned_symbols",
        "account_mode_not_demo_only",
        "volume_missing_or_non_positive",
        "risk_or_heat_limit_exceeded",
        "request_contains_order_send_authorization",
        "request_contains_symbol_select_authorization",
        "request_contains_live_money_authorization",
        "request_contains_executable_trade_dispatch_authorization",
    ],
    "future_permitted_action_after_separate_authorization": (
        "single demo-only order-check preflight invocation for one fully reviewed candidate"
    ),
    "explicitly_not_permitted_by_this_design_packet": [
        "order-check invocation",
        "order-send invocation",
        "symbol selection",
        "position creation",
        "position close",
        "position modification",
        "live-money support",
        "unattended loop",
        "automatic retry",
        "automatic dispatch",
    ],
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _violation(code: str, message: str, severity: str = "ERROR") -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message}


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _latest_jsonl_record(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None

    latest: dict[str, Any] | None = None
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path} line {line_number} is not valid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{path} line {line_number} must be a JSON object")
        latest = record
    return latest


def _rel_exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).is_file()


def _collect_files(root: Path, rel_paths: list[str]) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []
    for rel_path in rel_paths:
        if _rel_exists(root, rel_path):
            present.append(rel_path)
        else:
            missing.append(rel_path)
    return present, missing


def build_order_check_gate_design_packet(
    *,
    root: Path = ROOT,
    replay_report: Path = REPLAY_REPORT,
) -> dict[str, Any]:
    violations: list[dict[str, str]] = []

    replay_record: dict[str, Any] | None
    try:
        replay_record = _latest_jsonl_record(replay_report)
    except ValueError as exc:
        replay_record = None
        violations.append(
            _violation(
                "existing_path_replay_report_malformed",
                f"Existing path replay report is malformed: {exc}",
            )
        )

    if replay_record is None:
        violations.append(
            _violation(
                "existing_path_replay_report_missing",
                f"Required existing path replay report is missing or empty: {replay_report}",
            )
        )
    else:
        for field, expected in EXPECTED_REPLAY_FIELDS.items():
            observed = replay_record.get(field)
            if observed != expected:
                violations.append(
                    _violation(
                        f"existing_path_replay_{field}_unexpected",
                        f"Replay field {field!r} must be {expected!r}; got {observed!r}.",
                    )
                )

    present_artifacts, missing_artifacts = _collect_files(root, REQUIRED_EXISTING_ARTIFACTS)
    for rel_path in missing_artifacts:
        violations.append(
            _violation(
                "required_existing_artifact_missing",
                f"Required existing artifact for order-check gate design is missing: {rel_path}",
            )
        )

    design_contract_constraints = {
        "read_only_design_only": True,
        "requires_future_explicit_operator_authorization": True,
        "authorization_scope_must_be_exact": True,
        "single_candidate_only": True,
        "demo_only": True,
        "no_live_money": True,
        "no_symbol_select": True,
        "no_order_send": True,
        "no_position_creation": True,
        "no_position_close": True,
        "no_position_modify": True,
        "no_unattended_loop": True,
        "no_automatic_retry": True,
        "fail_closed_by_default": True,
    }

    verdict = "PASS" if not violations else "FAIL_CLOSED"
    accepted = verdict == "PASS"

    packet: dict[str, Any] = {
        "verdict": verdict,
        "stage": STAGE,
        "operator_state": (
            "H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_ACCEPTED"
            if accepted
            else "FAIL_CLOSED_H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_UNVERIFIED"
        ),
        "order_check_gate_design_state": (
            "READ_ONLY_GATE_CONTRACT_DEFINED"
            if accepted
            else "READ_ONLY_GATE_CONTRACT_BLOCKED"
        ),
        "operator_next_action": (
            "PROCEED_TO_H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN"
            if accepted
            else "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
        ),
        "generated_at_utc": _utc_now_iso(),
        "consumed_existing_path_replay_report": _safe_relative(replay_report, root),
        "existing_path_replay_verdict": None if replay_record is None else replay_record.get("verdict"),
        "existing_path_replay_operator_state": None if replay_record is None else replay_record.get("operator_state"),
        "existing_path_replay_state": None if replay_record is None else replay_record.get("existing_path_replay_state"),
        "latest_existing_artifact_before_broker_mutation": None
        if replay_record is None
        else replay_record.get("latest_existing_artifact_before_broker_mutation"),
        "required_existing_artifacts_present": present_artifacts,
        "required_existing_artifacts_missing": missing_artifacts,
        "future_gate_schema": FUTURE_GATE_SCHEMA,
        "design_contract_constraints": design_contract_constraints,
        "allowed_demo_symbols": ALLOWED_DEMO_SYMBOLS,
        "banned_symbols": BANNED_SYMBOLS,
        "max_risk_per_trade_pct": 0.5,
        "max_portfolio_heat_pct": 1.0,
        "ready_for_order_check_gate_design": accepted,
        "ready_for_order_check_gate_operator_authorization_packet_design": accepted,
        "ready_for_demo_order_check_gate": False,
        "ready_for_demo_order_check_gate_implementation": False,
        "ready_for_demo_order_check_invocation": False,
        "next_target": "H024_STANDARD_DEMO_ORDER_CHECK_GATE_OPERATOR_AUTHORIZATION_PACKET_DESIGN",
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "symbol_select_authorized": False,
        "executable_trade_request_constructed": False,
        "new_entry_authorized": False,
        "close_modify_authorized": False,
        "live_money_supported": False,
        "read_only_design_only": True,
        "violations": violations,
        "violation_count": len(violations),
    }

    return packet


def render_text(packet: dict[str, Any]) -> str:
    lines = [
        "H024 standard-demo order-check gate design summary",
        "",
        f"verdict                                                : {packet['verdict']}",
        f"stage                                                  : {packet['stage']}",
        f"operator_state                                         : {packet['operator_state']}",
        f"order_check_gate_design_state                          : {packet['order_check_gate_design_state']}",
        f"operator_next_action                                   : {packet['operator_next_action']}",
        f"consumed_existing_path_replay_report                   : {packet['consumed_existing_path_replay_report']}",
        f"existing_path_replay_verdict                           : {packet['existing_path_replay_verdict']}",
        f"existing_path_replay_operator_state                    : {packet['existing_path_replay_operator_state']}",
        f"existing_path_replay_state                             : {packet['existing_path_replay_state']}",
        f"latest_existing_artifact_before_broker_mutation        : {packet['latest_existing_artifact_before_broker_mutation']}",
        f"ready_for_order_check_gate_design                      : {packet['ready_for_order_check_gate_design']}",
        f"ready_for_order_check_gate_authorization_packet_design : {packet['ready_for_order_check_gate_operator_authorization_packet_design']}",
        f"ready_for_demo_order_check_gate                        : {packet['ready_for_demo_order_check_gate']}",
        f"ready_for_demo_order_check_gate_implementation         : {packet['ready_for_demo_order_check_gate_implementation']}",
        f"ready_for_demo_order_check_invocation                  : {packet['ready_for_demo_order_check_invocation']}",
        f"next_target                                            : {packet['next_target']}",
        f"trading_authorized                                     : {packet['trading_authorized']}",
        f"broker_mutation_authorized                             : {packet['broker_mutation_authorized']}",
        f"order_check_authorized                                 : {packet['order_check_authorized']}",
        f"order_send_authorized                                  : {packet['order_send_authorized']}",
        f"symbol_select_authorized                               : {packet['symbol_select_authorized']}",
        f"executable_trade_request_constructed                  : {packet['executable_trade_request_constructed']}",
        f"new_entry_authorized                                   : {packet['new_entry_authorized']}",
        f"close_modify_authorized                                : {packet['close_modify_authorized']}",
        f"read_only_design_only                                  : {packet['read_only_design_only']}",
        f"violation_count                                        : {packet['violation_count']}",
        "",
        "Required existing artifacts present:",
    ]

    for rel_path in packet["required_existing_artifacts_present"]:
        lines.append(f"- {rel_path}")

    lines.extend(["", "Future gate required inputs:"])
    for field in packet["future_gate_schema"]["required_inputs"]:
        lines.append(f"- {field}")

    lines.extend(["", "Fail-closed conditions:"])
    for condition in packet["future_gate_schema"]["fail_closed_conditions"]:
        lines.append(f"- {condition}")

    lines.extend(["", "Explicitly not permitted by this design packet:"])
    for item in packet["future_gate_schema"]["explicitly_not_permitted_by_this_design_packet"]:
        lines.append(f"- {item}")

    lines.extend(["", "Violations:"])
    if packet["violations"]:
        for violation in packet["violations"]:
            lines.append(f"- {violation['severity']} {violation['code']}: {violation['message']}")
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"


def write_reports(packet: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with DESIGN_JSONL.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(packet, sort_keys=True) + "\n")
    DESIGN_TXT.write_text(render_text(packet), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the H024 standard-demo order-check gate design packet.")
    parser.parse_args()

    packet = build_order_check_gate_design_packet()
    write_reports(packet)
    print(render_text(packet), end="")
    return 0 if packet["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
