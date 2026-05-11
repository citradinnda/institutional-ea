from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

SCHEMA = "h024_phase4_review_packet_v1"
KIND = "PHASE4_REVIEW_PACKET_REVIEW_ONLY"
READY_STATUS = "READY_FOR_HUMAN_PHASE4_REVIEW"

PHASE4_REVIEW_READY_STATUS = "READY_FOR_PHASE4_REVIEW_REQUEST"
SAFETY_DESIGN_STATUS = "SAFETY_CONTROLS_DESIGN_SPEC_ONLY_NOT_IMPLEMENTED"
DEFAULT_BLOCK_DECISION = "BLOCK"
DEFAULT_BLOCK_REASON = "missing_kill_switch_state"
ALLOW_DECISION = "PASS_REVIEW_ONLY_NOT_EXECUTION_APPROVAL"

APPROVAL_FLAG_KEYS = {
    "phase4_approved",
    "demo_order_placement_approved",
    "live_order_placement_approved",
    "execution_adapter_approved",
    "adapter_implementation_approved",
    "demo_execution_adapter_implementation_approved",
    "manual_approval_granted",
    "execution_approved",
}

FORBIDDEN_EXECUTION_FIELD_NAMES = {
    "ordersend",
    "order_send",
    "ordersendasync",
    "order_send_async",
    "ordercheck",
    "order_check",
    "ctrade",
    "c_trade",
    "mqltraderequest",
    "mql_trade_request",
    "mqltraderesult",
    "mql_trade_result",
    "mt5_request",
    "broker_request",
    "trade_request",
    "order_request",
    "position_open",
    "position_close",
    "position_modify",
    "pending_order_request",
}


class Phase4ReviewPacketError(ValueError):
    """Raised when Phase 4 review-packet evidence violates review-only boundaries."""


@dataclass(frozen=True)
class Phase4ReviewPacketPaths:
    phase4_readiness_review_jsonl: Path
    execution_safety_controls_design_jsonl: Path
    default_blocked_safety_preflight_jsonl: Path
    operator_control_state_snapshot_json: Path
    allow_state_safety_preflight_jsonl: Path

    @classmethod
    def standard_demo_reports(cls, reports_dir: str | Path = "reports") -> "Phase4ReviewPacketPaths":
        reports = Path(reports_dir)
        return cls(
            phase4_readiness_review_jsonl=reports / "h024_standard_demo_phase4_readiness_review.jsonl",
            execution_safety_controls_design_jsonl=reports / "h024_standard_demo_execution_safety_controls_design.jsonl",
            default_blocked_safety_preflight_jsonl=reports / "h024_standard_demo_execution_safety_controls_default_blocked_preflight.jsonl",
            operator_control_state_snapshot_json=reports / "h024_standard_demo_operator_control_state_snapshot.json",
            allow_state_safety_preflight_jsonl=reports / "h024_standard_demo_execution_safety_controls_allow_state_preflight.jsonl",
        )


@dataclass(frozen=True)
class ArtifactRecord:
    label: str
    path: Path
    payload: dict[str, Any]
    record_count: int | None


def read_jsonl_records(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    records: list[dict[str, Any]] = []
    for line_no, raw_line in enumerate(source.read_text(encoding="utf-8-sig").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise Phase4ReviewPacketError(f"{source}:{line_no}: invalid JSONL: {exc}") from exc
        if not isinstance(payload, dict):
            raise Phase4ReviewPacketError(f"{source}:{line_no}: JSONL record must be an object")
        records.append(payload)
    return records


def read_json_object(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise Phase4ReviewPacketError(f"{source}: invalid JSON object: {exc}") from exc
    if not isinstance(payload, dict):
        raise Phase4ReviewPacketError(f"{source}: JSON payload must be an object")
    return payload


def write_jsonl_record(path: str | Path, record: dict[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def _walk(payload: Any, prefix: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_path = (*prefix, str(key))
            yield key_path, value
            yield from _walk(value, key_path)
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            yield from _walk(value, (*prefix, str(index)))


def _first(payload: Any, key_names: Sequence[str]) -> Any | None:
    wanted = {key.lower() for key in key_names}
    for key_path, value in _walk(payload):
        if key_path and key_path[-1].lower() in wanted:
            return value
    return None


def _all_values(payload: Any, key_names: Sequence[str]) -> list[Any]:
    wanted = {key.lower() for key in key_names}
    return [value for key_path, value in _walk(payload) if key_path and key_path[-1].lower() in wanted]


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


def _as_text(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _flatten_reasons(values: Sequence[Any]) -> list[str]:
    reasons: list[str] = []
    for value in values:
        if value is None:
            continue
        if isinstance(value, (list, tuple)):
            reasons.extend(str(item) for item in value if str(item).strip())
        else:
            text = str(value).strip()
            if text:
                reasons.append(text)
    return reasons


def _server(payload: dict[str, Any]) -> str | None:
    return _as_text(_first(payload, ("server", "account_server", "broker_server", "demo_server", "allowed_demo_server")))


def _assert_one_jsonl(label: str, path: Path) -> ArtifactRecord:
    records = read_jsonl_records(path)
    if len(records) != 1:
        raise Phase4ReviewPacketError(f"{label}: expected exactly 1 JSONL record at {path}, found {len(records)}")
    return ArtifactRecord(label=label, path=path, payload=records[0], record_count=1)


def _assert_json(label: str, path: Path) -> ArtifactRecord:
    return ArtifactRecord(label=label, path=path, payload=read_json_object(path), record_count=None)


def _boundary_violations(label: str, payload: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for key_path, value in _walk(payload):
        if not key_path:
            continue
        key = key_path[-1].lower()
        if key in APPROVAL_FLAG_KEYS and _as_bool(value) is True:
            violations.append(f"{label}: approval flag {'.'.join(key_path)} is true")
        if key in FORBIDDEN_EXECUTION_FIELD_NAMES:
            violations.append(f"{label}: forbidden execution-like field {'.'.join(key_path)} is present")
    return violations


def load_required_artifacts(paths: Phase4ReviewPacketPaths) -> dict[str, ArtifactRecord]:
    return {
        "phase4_readiness_review": _assert_one_jsonl("phase4_readiness_review", paths.phase4_readiness_review_jsonl),
        "execution_safety_controls_design": _assert_one_jsonl("execution_safety_controls_design", paths.execution_safety_controls_design_jsonl),
        "default_blocked_safety_preflight": _assert_one_jsonl("default_blocked_safety_preflight", paths.default_blocked_safety_preflight_jsonl),
        "operator_control_state_snapshot": _assert_json("operator_control_state_snapshot", paths.operator_control_state_snapshot_json),
        "allow_state_safety_preflight": _assert_one_jsonl("allow_state_safety_preflight", paths.allow_state_safety_preflight_jsonl),
    }


def validate_required_artifacts(
    artifacts: dict[str, ArtifactRecord], *, allowed_demo_server: str | None = None
) -> list[str]:
    violations: list[str] = []
    required = {
        "phase4_readiness_review",
        "execution_safety_controls_design",
        "default_blocked_safety_preflight",
        "operator_control_state_snapshot",
        "allow_state_safety_preflight",
    }
    missing = required - set(artifacts)
    if missing:
        return [f"missing required artifacts: {sorted(missing)}"]

    for artifact in artifacts.values():
        violations.extend(_boundary_violations(artifact.label, artifact.payload))
        artifact_server = _server(artifact.payload)
        if allowed_demo_server and artifact_server is not None and artifact_server != allowed_demo_server:
            violations.append(f"{artifact.label}: server {artifact_server!r} does not match allowed demo server {allowed_demo_server!r}")

    phase4_status = _as_text(_first(artifacts["phase4_readiness_review"].payload, ("review_request_status",)) or _first(artifacts["phase4_readiness_review"].payload, ("status",)))
    if phase4_status != PHASE4_REVIEW_READY_STATUS:
        violations.append(f"phase4_readiness_review: expected {PHASE4_REVIEW_READY_STATUS!r}, found {phase4_status!r}")

    design_status = _as_text(_first(artifacts["execution_safety_controls_design"].payload, ("design_status",)) or _first(artifacts["execution_safety_controls_design"].payload, ("status",)))
    if design_status != SAFETY_DESIGN_STATUS:
        violations.append(f"execution_safety_controls_design: expected {SAFETY_DESIGN_STATUS!r}, found {design_status!r}")

    default_payload = artifacts["default_blocked_safety_preflight"].payload
    default_decision = _as_text(_first(default_payload, ("control_decision",)))
    default_reasons = _flatten_reasons(_all_values(default_payload, ("blocked_reason", "blocked_reasons")))
    if default_decision != DEFAULT_BLOCK_DECISION:
        violations.append(f"default_blocked_safety_preflight: expected control_decision {DEFAULT_BLOCK_DECISION!r}, found {default_decision!r}")
    if DEFAULT_BLOCK_REASON not in default_reasons:
        violations.append(f"default_blocked_safety_preflight: expected blocked reason {DEFAULT_BLOCK_REASON!r}, found {default_reasons!r}")

    operator_payload = artifacts["operator_control_state_snapshot"].payload
    snapshot_status = _as_text(_first(operator_payload, ("snapshot_status",)) or _first(operator_payload, ("status",)))
    if snapshot_status != "ALLOW_STATE_REVIEW_ONLY_NOT_EXECUTION_APPROVAL":
        violations.append(f"operator_control_state_snapshot: expected 'ALLOW_STATE_REVIEW_ONLY_NOT_EXECUTION_APPROVAL', found {snapshot_status!r}")
    stable_intent_id = _as_text(_first(operator_payload, ("stable_intent_id", "intent_id")))
    if not stable_intent_id:
        violations.append("operator_control_state_snapshot: missing stable intent id")

    allow_payload = artifacts["allow_state_safety_preflight"].payload
    allow_decision = _as_text(_first(allow_payload, ("control_decision",)))
    allow_reasons = _flatten_reasons(_all_values(allow_payload, ("blocked_reason", "blocked_reasons")))
    if allow_decision != ALLOW_DECISION:
        violations.append(f"allow_state_safety_preflight: expected control_decision {ALLOW_DECISION!r}, found {allow_decision!r}")
    if allow_reasons:
        violations.append(f"allow_state_safety_preflight: expected no blocked reasons, found {allow_reasons!r}")

    return violations


def independent_verifier_commands(paths: Phase4ReviewPacketPaths, *, allowed_demo_server: str) -> list[list[str]]:
    return [
        [sys.executable, "scripts/verify_h024_phase4_readiness_review_jsonl.py", str(paths.phase4_readiness_review_jsonl), "--allowed-demo-server", allowed_demo_server, "--require-review"],
        [sys.executable, "scripts/verify_h024_execution_safety_controls_design_jsonl.py", str(paths.execution_safety_controls_design_jsonl), "--allowed-demo-server", allowed_demo_server, "--require-design"],
        [sys.executable, "scripts/verify_h024_execution_safety_controls_preflight_jsonl.py", str(paths.default_blocked_safety_preflight_jsonl), "--allowed-demo-server", allowed_demo_server, "--require-preflight", "--require-blocked"],
        [sys.executable, "scripts/verify_h024_operator_control_state_snapshot.py", str(paths.operator_control_state_snapshot_json), "--allowed-demo-server", allowed_demo_server],
        [sys.executable, "scripts/verify_h024_execution_safety_controls_preflight_jsonl.py", str(paths.allow_state_safety_preflight_jsonl), "--allowed-demo-server", allowed_demo_server, "--require-preflight"],
    ]


def run_independent_verifiers(
    paths: Phase4ReviewPacketPaths,
    *,
    allowed_demo_server: str,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for command in independent_verifier_commands(paths, allowed_demo_server=allowed_demo_server):
        completed = runner(command, capture_output=True, text=True)
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        results.append(
            {
                "command": command,
                "returncode": completed.returncode,
                "passed": completed.returncode == 0 and "Verdict: PASS" in stdout,
                "stdout_tail": "\n".join(stdout.splitlines()[-12:]),
                "stderr_tail": "\n".join(stderr.splitlines()[-12:]),
            }
        )
    return results


def _artifact_summary(artifact: ArtifactRecord) -> dict[str, Any]:
    payload = artifact.payload
    summary: dict[str, Any] = {
        "label": artifact.label,
        "path": str(artifact.path),
        "record_count": artifact.record_count,
        "schema": _as_text(_first(payload, ("schema",))),
        "kind": _as_text(_first(payload, ("kind",))),
        "server": _server(payload),
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "execution_approved": False,
    }
    for key in ("review_request_status", "design_status", "snapshot_status", "control_status", "control_decision", "stable_intent_id"):
        value = _first(payload, (key,))
        if value is not None:
            summary[key] = value
    reasons = _flatten_reasons(_all_values(payload, ("blocked_reason", "blocked_reasons")))
    if reasons:
        summary["blocked_reasons"] = reasons
    return summary


def build_phase4_review_packet(
    paths: Phase4ReviewPacketPaths,
    *,
    allowed_demo_server: str = "Exness-MT5Trial6",
    created_utc: str | None = None,
    upstream_verifier_results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    artifacts = load_required_artifacts(paths)
    violations = validate_required_artifacts(artifacts, allowed_demo_server=allowed_demo_server)

    verifier_results = upstream_verifier_results or []
    for result in verifier_results:
        if not result.get("passed", False):
            violations.append(f"independent verifier failed: {' '.join(result.get('command', []))}")

    if violations:
        raise Phase4ReviewPacketError("Phase 4 review packet input violations: " + "; ".join(violations))

    stable_intent_id = _as_text(_first(artifacts["operator_control_state_snapshot"].payload, ("stable_intent_id", "intent_id")))
    created = created_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    packet = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": READY_STATUS,
        "created_utc": created,
        "strategy_id": "H024",
        "environment": "standard_demo_review_only",
        "allowed_demo_server": allowed_demo_server,
        "stable_intent_id": stable_intent_id,
        "human_review_required": True,
        "phase4_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_adapter_approved": False,
        "execution_approved": False,
        "execution_boundary": {
            "mt5_access_approved": False,
            "broker_request_construction_approved": False,
            "demo_order_placement_approved": False,
            "live_order_placement_approved": False,
            "execution_adapter_approved": False,
            "order_send_approved": False,
            "order_check_approved": False,
            "explicit_allow_state_is_execution_approval": False,
        },
        "required_artifacts": [_artifact_summary(artifacts[label]) for label in sorted(artifacts)],
        "gate_checks": {
            "phase4_readiness_review_ready": True,
            "execution_safety_controls_design_verified": True,
            "default_missing_kill_switch_blocks": True,
            "operator_control_state_snapshot_verified": True,
            "explicit_allow_state_preflight_passes_review_only": True,
            "all_approval_flags_false": True,
            "no_execution_like_fields_present": True,
            "independent_upstream_verifiers_passed": all(result.get("passed", False) for result in verifier_results) if verifier_results else None,
        },
        "upstream_verifier_results": verifier_results,
        "review_boundary_statement": (
            "Ready to request human Phase 4 review only. This packet does not approve Phase 4, "
            "demo order placement, live order placement, execution adapter implementation, MT5 request "
            "construction, broker request construction, OrderSend, OrderCheck, CTrade, or execution."
        ),
    }

    packet_violations = validate_phase4_review_packet_record(packet, require_ready=True, allowed_demo_server=allowed_demo_server)
    if packet_violations:
        raise Phase4ReviewPacketError("Built packet is invalid: " + "; ".join(packet_violations))
    return packet


def validate_phase4_review_packet_record(
    record: dict[str, Any], *, require_ready: bool = False, allowed_demo_server: str | None = None
) -> list[str]:
    violations: list[str] = []
    if record.get("schema") != SCHEMA:
        violations.append(f"expected schema {SCHEMA!r}, found {record.get('schema')!r}")
    if record.get("kind") != KIND:
        violations.append(f"expected kind {KIND!r}, found {record.get('kind')!r}")
    if require_ready and record.get("status") != READY_STATUS:
        violations.append(f"expected status {READY_STATUS!r}, found {record.get('status')!r}")
    if allowed_demo_server and record.get("allowed_demo_server") != allowed_demo_server:
        violations.append(f"expected allowed_demo_server {allowed_demo_server!r}, found {record.get('allowed_demo_server')!r}")
    if record.get("human_review_required") is not True:
        violations.append("human_review_required must be true")
    for key in ("phase4_approved", "demo_order_placement_approved", "live_order_placement_approved", "execution_adapter_approved", "execution_approved"):
        if record.get(key) is not False:
            violations.append(f"{key} must be false")

    boundary = record.get("execution_boundary")
    if not isinstance(boundary, dict):
        violations.append("execution_boundary must be an object")
    else:
        for key in (
            "mt5_access_approved",
            "broker_request_construction_approved",
            "demo_order_placement_approved",
            "live_order_placement_approved",
            "execution_adapter_approved",
            "order_send_approved",
            "order_check_approved",
            "explicit_allow_state_is_execution_approval",
        ):
            if boundary.get(key) is not False:
                violations.append(f"execution_boundary.{key} must be false")

    artifacts = record.get("required_artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 5:
        violations.append("required_artifacts must contain exactly 5 artifact summaries")

    checks = record.get("gate_checks")
    if not isinstance(checks, dict):
        violations.append("gate_checks must be an object")
    else:
        for key in (
            "phase4_readiness_review_ready",
            "execution_safety_controls_design_verified",
            "default_missing_kill_switch_blocks",
            "operator_control_state_snapshot_verified",
            "explicit_allow_state_preflight_passes_review_only",
            "all_approval_flags_false",
            "no_execution_like_fields_present",
        ):
            if checks.get(key) is not True:
                violations.append(f"gate_checks.{key} must be true")

    violations.extend(_boundary_violations("phase4_review_packet", record))
    return violations


def verify_phase4_review_packet_jsonl(
    path: str | Path, *, require_ready: bool = False, allowed_demo_server: str | None = None
) -> tuple[list[dict[str, Any]], list[str]]:
    records = read_jsonl_records(path)
    violations: list[str] = []
    if len(records) != 1:
        violations.append(f"expected exactly 1 Phase 4 review packet record, found {len(records)}")
    for index, record in enumerate(records, start=1):
        for violation in validate_phase4_review_packet_record(record, require_ready=require_ready, allowed_demo_server=allowed_demo_server):
            violations.append(f"record {index}: {violation}")
    return records, violations


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an H024 Phase 4 human-review packet JSONL artifact.")
    parser.add_argument("--reports-dir", default="reports")
    parser.add_argument("--output", default="reports/h024_standard_demo_phase4_review_packet.jsonl")
    parser.add_argument("--allowed-demo-server", default="Exness-MT5Trial6")
    parser.add_argument("--skip-upstream-verifiers", action="store_true")
    return parser


def main_build(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    paths = Phase4ReviewPacketPaths.standard_demo_reports(args.reports_dir)
    verifier_results: list[dict[str, Any]] = []
    if not args.skip_upstream_verifiers:
        verifier_results = run_independent_verifiers(paths, allowed_demo_server=args.allowed_demo_server)
    packet = build_phase4_review_packet(paths, allowed_demo_server=args.allowed_demo_server, upstream_verifier_results=verifier_results)
    write_jsonl_record(args.output, packet)
    print(f"Output: {args.output}")
    print("Review packet records: 1")
    print("Violations: 0")
    print("Status: READY_FOR_HUMAN_PHASE4_REVIEW")
    print("Phase 4 approved: false")
    print("Demo order placement approved: false")
    print("Live order placement approved: false")
    print("Execution adapter approved: false")
    print("Execution approved: false")
    print("Verdict: PASS")
    return 0


def verify_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify an H024 Phase 4 human-review packet JSONL artifact.")
    parser.add_argument("jsonl_path")
    parser.add_argument("--allowed-demo-server", default=None)
    parser.add_argument("--require-ready", action="store_true")
    return parser


def main_verify(argv: Sequence[str] | None = None) -> int:
    args = verify_arg_parser().parse_args(argv)
    records, violations = verify_phase4_review_packet_jsonl(args.jsonl_path, require_ready=args.require_ready, allowed_demo_server=args.allowed_demo_server)
    print(f"Input: {args.jsonl_path}")
    print(f"Review packet records: {len(records)}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    if violations:
        print("Verdict: FAIL")
        return 1
    print("Verdict: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_build())