from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"

PATH_MAP_REPORT = REPORTS_DIR / "h024_standard_demo_existing_path_map.jsonl"
REPLAY_JSONL = REPORTS_DIR / "h024_standard_demo_existing_path_replay.jsonl"
REPLAY_TXT = REPORTS_DIR / "h024_standard_demo_existing_path_replay.txt"

STAGE = "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY"

EXPECTED_PATH_MAP_FIELDS: dict[str, Any] = {
    "verdict": "PASS",
    "operator_state": "H024_STANDARD_DEMO_EXISTING_PATH_MAP_ACCEPTED",
    "existing_path_map_state": "REAL_H024_STANDARD_DEMO_PATH_IDENTIFIED",
    "ready_for_existing_path_replay": True,
    "ready_for_demo_order_check_gate": False,
    "trading_authorized": False,
    "broker_mutation_authorized": False,
    "order_check_authorized": False,
    "order_send_authorized": False,
    "symbol_select_authorized": False,
    "executable_trade_request_constructed": False,
}

EXISTING_PATH_SEQUENCE = [
    "quantcore/execution/h024_order_intent_simulation.py",
    "quantcore/execution/h024_dry_run.py",
    "quantcore/execution/h024_dry_run_log.py",
    "quantcore/execution/h024_runtime_safety_lockout.py",
    "quantcore/execution/h024_runtime_tick_spread_safety_supervisor.py",
    "quantcore/execution/h024_runtime_exposure_inventory_safety_supervisor.py",
    "quantcore/execution/h024_safety_supervisor_spec.py",
    "quantcore/execution/h024_manual_approval_checkpoint.py",
    "quantcore/execution/h024_broker_request_draft_envelope.py",
]

STANDARD_DEMO_RESULT_DOCS = [
    "docs/operations/H024_STANDARD_DEMO_ORDER_INTENT_SIMULATION_RESULT.md",
    "docs/operations/H024_STANDARD_DEMO_ORDER_READINESS_PACKET_RESULT.md",
    "docs/operations/H024_STANDARD_DEMO_MANUAL_APPROVAL_CHECKPOINT_RESULT.md",
    "docs/operations/H024_STANDARD_DEMO_BROKER_REQUEST_DRAFT_ENVELOPE_RESULT.md",
    "docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md",
    "docs/operations/H024_STANDARD_DEMO_ORDER_CANARY_HUMAN_APPROVAL_RESULT.md",
]

LATEST_EXISTING_ARTIFACT_BEFORE_BROKER_MUTATION = (
    "docs/operations/H024_STANDARD_DEMO_MT5_REQUEST_SHAPE_PREVIEW_ENVELOPE_RESULT.md"
)

FOCUSED_EXISTING_TEST_TARGETS = [
    "tests/test_h024_order_intent_simulation.py",
    "tests/test_h024_dry_run_execution.py",
    "tests/test_h024_dry_run_log.py",
    "tests/test_h024_dry_run_action_verifier.py",
    "tests/test_h024_manual_approval_checkpoint.py",
    "tests/test_h024_runtime_safety_lockout.py",
    "tests/test_h024_runtime_tick_spread_safety_supervisor.py",
    "tests/test_h024_runtime_exposure_inventory_safety_supervisor.py",
    "tests/test_h024_safety_supervisor_spec.py",
]

ALLOWED_DEMO_SYMBOLS = ["USDJPYm", "XAUUSDm"]
BANNED_SYMBOLS = ["EURUSDm", "GBPUSDm", "US500m"]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _violation(code: str, message: str, severity: str = "ERROR") -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message}


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


def _collect_existing_files(root: Path, rel_paths: list[str]) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []
    for rel_path in rel_paths:
        if _rel_exists(root, rel_path):
            present.append(rel_path)
        else:
            missing.append(rel_path)
    return present, missing


def _run_existing_tests(root: Path, targets: list[str]) -> dict[str, Any]:
    present_targets = [target for target in targets if _rel_exists(root, target)]

    if not present_targets:
        return {
            "executed": False,
            "returncode": None,
            "targets": [],
            "stdout_tail": "",
            "stderr_tail": "",
            "reason": "no_existing_test_targets_found",
        }

    completed = subprocess.run(
        [sys.executable, "-m", "pytest", *present_targets, "-q"],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )

    return {
        "executed": True,
        "returncode": completed.returncode,
        "targets": present_targets,
        "stdout_tail": "\n".join(completed.stdout.splitlines()[-80:]),
        "stderr_tail": "\n".join(completed.stderr.splitlines()[-80:]),
        "reason": None,
    }


def build_replay_packet(
    *,
    root: Path = ROOT,
    path_map_report: Path = PATH_MAP_REPORT,
    run_existing_tests: bool = False,
) -> dict[str, Any]:
    violations: list[dict[str, str]] = []

    path_map_record: dict[str, Any] | None
    try:
        path_map_record = _latest_jsonl_record(path_map_report)
    except ValueError as exc:
        path_map_record = None
        violations.append(
            _violation(
                "path_map_report_malformed",
                f"Path-map report is malformed: {exc}",
            )
        )

    if path_map_record is None:
        violations.append(
            _violation(
                "path_map_report_missing",
                f"Required path-map report is missing or empty: {path_map_report}",
            )
        )
    else:
        for field, expected in EXPECTED_PATH_MAP_FIELDS.items():
            observed = path_map_record.get(field)
            if observed != expected:
                violations.append(
                    _violation(
                        f"path_map_{field}_unexpected",
                        f"Path-map field {field!r} must be {expected!r}; got {observed!r}.",
                    )
                )

    path_sequence_present, path_sequence_missing = _collect_existing_files(root, EXISTING_PATH_SEQUENCE)
    for rel_path in path_sequence_missing:
        violations.append(
            _violation(
                "existing_path_file_missing",
                f"Existing H024 standard-demo replay path file is missing: {rel_path}",
            )
        )

    docs_present, docs_missing = _collect_existing_files(root, STANDARD_DEMO_RESULT_DOCS)
    for rel_path in docs_missing:
        violations.append(
            _violation(
                "standard_demo_result_doc_missing",
                f"Existing H024 standard-demo result document is missing: {rel_path}",
            )
        )

    tests_present, tests_missing = _collect_existing_files(root, FOCUSED_EXISTING_TEST_TARGETS)
    if not tests_present:
        violations.append(
            _violation(
                "existing_h024_tests_missing",
                "No existing H024 replay-relevant tests were found.",
            )
        )

    latest_artifact_exists = _rel_exists(root, LATEST_EXISTING_ARTIFACT_BEFORE_BROKER_MUTATION)
    if not latest_artifact_exists:
        violations.append(
            _violation(
                "latest_pre_broker_mutation_artifact_missing",
                (
                    "Latest existing artifact before broker mutation is missing: "
                    f"{LATEST_EXISTING_ARTIFACT_BEFORE_BROKER_MUTATION}"
                ),
            )
        )

    existing_tests_result = {
        "executed": False,
        "returncode": None,
        "targets": tests_present,
        "stdout_tail": "",
        "stderr_tail": "",
        "reason": "not_requested",
    }
    if run_existing_tests:
        existing_tests_result = _run_existing_tests(root, FOCUSED_EXISTING_TEST_TARGETS)
        if not existing_tests_result["executed"]:
            violations.append(
                _violation(
                    "existing_h024_tests_not_executed",
                    "Existing H024 tests were requested but no replay-relevant test targets were found.",
                )
            )
        elif existing_tests_result["returncode"] != 0:
            violations.append(
                _violation(
                    "existing_h024_tests_failed",
                    (
                        "Existing H024 replay-relevant tests failed with return code "
                        f"{existing_tests_result['returncode']}."
                    ),
                )
            )

    verdict = "PASS" if not violations else "FAIL_CLOSED"
    accepted = verdict == "PASS"

    packet: dict[str, Any] = {
        "verdict": verdict,
        "stage": STAGE,
        "operator_state": (
            "H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_ACCEPTED"
            if accepted
            else "FAIL_CLOSED_H024_STANDARD_DEMO_EXISTING_PATH_REPLAY_UNVERIFIED"
        ),
        "existing_path_replay_state": (
            "REAL_H024_STANDARD_DEMO_PATH_REPLAYED_READ_ONLY"
            if accepted
            else "REAL_H024_STANDARD_DEMO_PATH_REPLAY_BLOCKED"
        ),
        "operator_next_action": (
            "PROCEED_TO_H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN_READ_ONLY"
            if accepted
            else "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"
        ),
        "generated_at_utc": _utc_now_iso(),
        "consumed_path_map_report": str(path_map_report.relative_to(root)) if path_map_report.is_relative_to(root) else str(path_map_report),
        "path_map_verdict": None if path_map_record is None else path_map_record.get("verdict"),
        "path_map_operator_state": None if path_map_record is None else path_map_record.get("operator_state"),
        "path_map_existing_path_map_state": None
        if path_map_record is None
        else path_map_record.get("existing_path_map_state"),
        "existing_path_sequence": EXISTING_PATH_SEQUENCE,
        "existing_path_sequence_present": path_sequence_present,
        "existing_path_sequence_missing": path_sequence_missing,
        "standard_demo_result_docs_present": docs_present,
        "standard_demo_result_docs_missing": docs_missing,
        "latest_existing_artifact_before_broker_mutation": LATEST_EXISTING_ARTIFACT_BEFORE_BROKER_MUTATION,
        "latest_existing_artifact_before_broker_mutation_exists": latest_artifact_exists,
        "focused_existing_test_targets_present": tests_present,
        "focused_existing_test_targets_missing": tests_missing,
        "existing_tests": existing_tests_result,
        "allowed_demo_symbols": ALLOWED_DEMO_SYMBOLS,
        "banned_symbols": BANNED_SYMBOLS,
        "max_risk_per_trade_pct": 0.5,
        "max_portfolio_heat_pct": 1.0,
        "ready_for_existing_path_replay": accepted,
        "ready_for_demo_order_check_gate": False,
        "ready_for_demo_order_check_gate_design": accepted,
        "next_target": "H024_STANDARD_DEMO_ORDER_CHECK_GATE_DESIGN",
        "trading_authorized": False,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "symbol_select_authorized": False,
        "executable_trade_request_constructed": False,
        "new_entry_authorized": False,
        "close_modify_authorized": False,
        "live_money_supported": False,
        "read_only_replay_only": True,
        "violations": violations,
        "violation_count": len(violations),
    }

    return packet


def render_text(packet: dict[str, Any]) -> str:
    lines = [
        "H024 standard-demo existing path replay summary",
        "",
        f"verdict                                           : {packet['verdict']}",
        f"stage                                             : {packet['stage']}",
        f"operator_state                                    : {packet['operator_state']}",
        f"existing_path_replay_state                        : {packet['existing_path_replay_state']}",
        f"operator_next_action                              : {packet['operator_next_action']}",
        f"consumed_path_map_report                          : {packet['consumed_path_map_report']}",
        f"path_map_verdict                                  : {packet['path_map_verdict']}",
        f"path_map_operator_state                           : {packet['path_map_operator_state']}",
        f"path_map_existing_path_map_state                  : {packet['path_map_existing_path_map_state']}",
        f"latest_existing_artifact_before_broker_mutation   : {packet['latest_existing_artifact_before_broker_mutation']}",
        f"latest_existing_artifact_exists                   : {packet['latest_existing_artifact_before_broker_mutation_exists']}",
        f"ready_for_existing_path_replay                    : {packet['ready_for_existing_path_replay']}",
        f"ready_for_demo_order_check_gate                   : {packet['ready_for_demo_order_check_gate']}",
        f"ready_for_demo_order_check_gate_design            : {packet['ready_for_demo_order_check_gate_design']}",
        f"next_target                                       : {packet['next_target']}",
        f"trading_authorized                                : {packet['trading_authorized']}",
        f"broker_mutation_authorized                        : {packet['broker_mutation_authorized']}",
        f"order_check_authorized                            : {packet['order_check_authorized']}",
        f"order_send_authorized                             : {packet['order_send_authorized']}",
        f"symbol_select_authorized                          : {packet['symbol_select_authorized']}",
        f"executable_trade_request_constructed             : {packet['executable_trade_request_constructed']}",
        f"new_entry_authorized                              : {packet['new_entry_authorized']}",
        f"close_modify_authorized                           : {packet['close_modify_authorized']}",
        f"read_only_replay_only                             : {packet['read_only_replay_only']}",
        f"violation_count                                   : {packet['violation_count']}",
        "",
        "Existing path sequence:",
    ]

    for rel_path in packet["existing_path_sequence"]:
        lines.append(f"- {rel_path}")

    lines.extend(["", "Existing replay-relevant tests present:"])
    for rel_path in packet["focused_existing_test_targets_present"]:
        lines.append(f"- {rel_path}")

    lines.extend(["", "Existing standard-demo result docs present:"])
    for rel_path in packet["standard_demo_result_docs_present"]:
        lines.append(f"- {rel_path}")

    lines.extend(["", "Existing tests execution:"])
    existing_tests = packet["existing_tests"]
    lines.append(f"executed   : {existing_tests['executed']}")
    lines.append(f"returncode : {existing_tests['returncode']}")
    lines.append(f"reason     : {existing_tests['reason']}")

    if existing_tests.get("stdout_tail"):
        lines.extend(["", "Existing tests stdout tail:", existing_tests["stdout_tail"]])

    if existing_tests.get("stderr_tail"):
        lines.extend(["", "Existing tests stderr tail:", existing_tests["stderr_tail"]])

    lines.extend(["", "Violations:"])
    if packet["violations"]:
        for violation in packet["violations"]:
            lines.append(f"- {violation['severity']} {violation['code']}: {violation['message']}")
    else:
        lines.append("- none")

    return "\n".join(lines) + "\n"


def write_reports(packet: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with REPLAY_JSONL.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(packet, sort_keys=True) + "\n")
    REPLAY_TXT.write_text(render_text(packet), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the H024 standard-demo existing path replay packet.")
    parser.add_argument(
        "--run-existing-tests",
        action="store_true",
        help="Run replay-relevant existing H024 tests as part of the read-only replay evidence.",
    )
    args = parser.parse_args()

    packet = build_replay_packet(run_existing_tests=args.run_existing_tests)
    write_reports(packet)
    print(render_text(packet), end="")
    return 0 if packet["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
