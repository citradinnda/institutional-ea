from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

from quantcore.execution.h024_phase4_readiness_review import (
    BROKER_METADATA_PREFLIGHT_ARTIFACT,
    DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT,
    DEMO_ORDER_PLANS_ARTIFACT,
    DRY_RUN_REQUESTS_ARTIFACT,
    MANUAL_APPROVAL_CHECKPOINT_ARTIFACT,
    ORDER_INTENT_SIMULATION_ARTIFACT,
    build_h024_phase4_readiness_review,
)


DEFAULT_PATHS = {
    DRY_RUN_REQUESTS_ARTIFACT: Path("reports/h024_standard_demo_dry_run_requests.jsonl"),
    DEMO_ORDER_PLANS_ARTIFACT: Path("reports/h024_standard_demo_demo_order_plans.jsonl"),
    BROKER_METADATA_PREFLIGHT_ARTIFACT: Path("reports/h024_standard_demo_broker_metadata_preflight.jsonl"),
    ORDER_INTENT_SIMULATION_ARTIFACT: Path("reports/h024_standard_demo_order_intent_simulation.jsonl"),
    MANUAL_APPROVAL_CHECKPOINT_ARTIFACT: Path("reports/h024_standard_demo_manual_approval_checkpoint.jsonl"),
    DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT: Path("reports/h024_standard_demo_demo_execution_adapter_design.jsonl"),
}

VERIFIER_SPECS = {
    DRY_RUN_REQUESTS_ARTIFACT: (
        "scripts/verify_h024_dry_run_request_jsonl.py",
        ("--require-request", "--require-dry-run-request", "--require-dry-run"),
    ),
    DEMO_ORDER_PLANS_ARTIFACT: (
        "scripts/verify_h024_demo_order_plan_jsonl.py",
        ("--require-plan", "--require-demo-order-plan"),
    ),
    BROKER_METADATA_PREFLIGHT_ARTIFACT: (
        "scripts/verify_h024_broker_metadata_preflight_jsonl.py",
        ("--require-preflight", "--require-broker-metadata-preflight"),
    ),
    ORDER_INTENT_SIMULATION_ARTIFACT: (
        "scripts/verify_h024_order_intent_simulation_jsonl.py",
        ("--require-intent", "--require-order-intent"),
    ),
    MANUAL_APPROVAL_CHECKPOINT_ARTIFACT: (
        "scripts/verify_h024_manual_approval_checkpoint_jsonl.py",
        ("--require-checkpoint", "--require-manual-approval-checkpoint"),
    ),
    DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT: (
        "scripts/verify_h024_demo_execution_adapter_design_jsonl.py",
        ("--require-design", "--require-demo-execution-adapter-design"),
    ),
}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON in {path} on line {line_number}: {exc}") from exc
            if not isinstance(value, dict):
                raise SystemExit(f"JSONL line {line_number} in {path} is not an object")
            records.append(value)
    return records


def _tail_lines(value: str, limit: int = 12) -> list[str]:
    lines = [line.rstrip() for line in value.splitlines() if line.rstrip()]
    return lines[-limit:]


def _run_help(script_path: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    return f"{result.stdout}\n{result.stderr}"


def _run_verifier(
    *,
    repo_root: Path,
    artifact_key: str,
    jsonl_path: Path,
    allowed_demo_servers: list[str],
    expected_account_currency: str,
    max_risk_fraction: str,
) -> dict[str, Any]:
    script_relative, require_flag_candidates = VERIFIER_SPECS[artifact_key]
    script_path = repo_root / script_relative
    help_text = _run_help(script_path)

    command = [sys.executable, str(script_path), str(jsonl_path)]

    if "--allowed-demo-server" in help_text:
        for server in allowed_demo_servers:
            command.extend(["--allowed-demo-server", server])
    if "--expected-account-currency" in help_text:
        command.extend(["--expected-account-currency", expected_account_currency])
    if "--max-risk-fraction" in help_text:
        command.extend(["--max-risk-fraction", max_risk_fraction])

    for flag in require_flag_candidates:
        if flag in help_text:
            command.append(flag)
            break

    result = subprocess.run(command, check=False, capture_output=True, text=True)
    return {
        "artifact": artifact_key,
        "verifier": script_relative,
        "command": " ".join(shlex.quote(part) for part in command),
        "return_code": result.returncode,
        "verdict": "PASS" if result.returncode == 0 else "FAIL",
        "record_count": None,
        "violations": [] if result.returncode == 0 else ["independent_verifier_returned_nonzero"],
        "stdout_tail": _tail_lines(result.stdout),
        "stderr_tail": _tail_lines(result.stderr),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build H024 Phase 4 readiness review-request JSONL.")
    parser.add_argument("--dry-run-request-jsonl", type=Path, default=DEFAULT_PATHS[DRY_RUN_REQUESTS_ARTIFACT])
    parser.add_argument("--demo-order-plan-jsonl", type=Path, default=DEFAULT_PATHS[DEMO_ORDER_PLANS_ARTIFACT])
    parser.add_argument(
        "--broker-metadata-preflight-jsonl",
        type=Path,
        default=DEFAULT_PATHS[BROKER_METADATA_PREFLIGHT_ARTIFACT],
    )
    parser.add_argument(
        "--order-intent-simulation-jsonl",
        type=Path,
        default=DEFAULT_PATHS[ORDER_INTENT_SIMULATION_ARTIFACT],
    )
    parser.add_argument(
        "--manual-approval-checkpoint-jsonl",
        type=Path,
        default=DEFAULT_PATHS[MANUAL_APPROVAL_CHECKPOINT_ARTIFACT],
    )
    parser.add_argument(
        "--demo-execution-adapter-design-jsonl",
        type=Path,
        default=DEFAULT_PATHS[DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/h024_standard_demo_phase4_readiness_review.jsonl"),
    )
    parser.add_argument("--allowed-demo-server", action="append", required=True)
    parser.add_argument("--expected-account-currency", default="USD")
    parser.add_argument("--max-risk-fraction", default="0.01")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    artifact_paths = {
        DRY_RUN_REQUESTS_ARTIFACT: args.dry_run_request_jsonl,
        DEMO_ORDER_PLANS_ARTIFACT: args.demo_order_plan_jsonl,
        BROKER_METADATA_PREFLIGHT_ARTIFACT: args.broker_metadata_preflight_jsonl,
        ORDER_INTENT_SIMULATION_ARTIFACT: args.order_intent_simulation_jsonl,
        MANUAL_APPROVAL_CHECKPOINT_ARTIFACT: args.manual_approval_checkpoint_jsonl,
        DEMO_EXECUTION_ADAPTER_DESIGN_ARTIFACT: args.demo_execution_adapter_design_jsonl,
    }

    artifacts: dict[str, list[dict[str, Any]]] = {}
    verifications: dict[str, dict[str, Any]] = {}

    for artifact_key, path in artifact_paths.items():
        records = _read_jsonl(path)
        artifacts[artifact_key] = records
        verification = _run_verifier(
            repo_root=repo_root,
            artifact_key=artifact_key,
            jsonl_path=path,
            allowed_demo_servers=args.allowed_demo_server,
            expected_account_currency=args.expected_account_currency,
            max_risk_fraction=args.max_risk_fraction,
        )
        verification["record_count"] = len(records)
        verifications[artifact_key] = verification

    record = build_h024_phase4_readiness_review(
        artifacts,
        artifact_verifications=verifications,
        allowed_demo_servers=args.allowed_demo_server,
        expected_account_currency=args.expected_account_currency,
        max_risk_fraction=args.max_risk_fraction,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(record, handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")

    print(f"Output Phase 4 readiness review JSONL: {args.output}")
    print(f"Review records: 1")
    print(f"Violations: {len(record.get('violations', []))}")
    for violation in record.get("violations", []):
        print(f"- {violation}")
    print(f"Review request status: {record.get('review_request_status')}")
    print(f"Phase 4 approved: {record.get('phase4_approved')}")
    print(f"Demo order placement approved: {record.get('demo_order_placement_approved')}")
    print(f"Live order placement approved: {record.get('live_order_placement_approved')}")
    print(f"Execution approved: {record.get('execution_approved')}")
    print(f"Verdict: {record.get('verdict')}")

    return 0 if record.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())