from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA = "h024_demo_adapter_boundary_static_verifier_v1"
KIND = "DEMO_ADAPTER_BOUNDARY_STATIC_VERIFIER"
STATUS = "ADAPTER_IMPLEMENTATION_BOUNDARY_STATIC_VERIFIED"
DECISION = "ALLOW_IMPLEMENTATION_SURFACE_REVIEW_ONLY_NO_EXECUTION"

DEFAULT_ADAPTER_BOUNDARY_TARGETS = (
    "quantcore/execution/h024_demo_execution_adapter_skeleton.py",
    "quantcore/execution/h024_demo_adapter_intent_refusal_audit.py",
    "scripts/build_h024_demo_execution_adapter_skeleton_jsonl.py",
    "scripts/verify_h024_demo_execution_adapter_skeleton_jsonl.py",
    "scripts/build_h024_demo_adapter_intent_refusal_audit_jsonl.py",
    "scripts/verify_h024_demo_adapter_intent_refusal_audit_jsonl.py",
)

PROHIBITED_PATTERNS: tuple[tuple[str, str], ...] = (
    ("metatrader5_import", r"^\s*(?:import\s+MetaTrader5\b|from\s+MetaTrader5\b)"),
    ("python_mt5_execution_call", r"\bmt5\s*\.\s*(?:initialize|login|shutdown|order_send|order_check)\b"),
    ("python_order_send_call", r"\border_send\s*\("),
    ("python_order_check_call", r"\border_check\s*\("),
    ("mql_trade_include", r"#\s*include\s*<\s*Trade(?:/|\\|\.|>)"),
    (
        "mql_execution_symbol",
        r"\b(?:OrderSend|OrderSendAsync|OrderCheck|CTrade|MqlTradeRequest|MqlTradeResult|"
        r"PositionOpen|PositionClose|PositionModify)\b",
    ),
    (
        "mql_pending_order_helper",
        r"\b(?:BuyStop|SellStop|BuyLimit|SellLimit|BuyStopLimit|SellStopLimit)\b",
    ),
)

FALSE_AUTHORITY_FLAGS = (
    "execution_adapter_use_approved",
    "execution_adapter_approved",
    "broker_request_approved",
    "mt5_execution_approved",
    "terminal_mutation_approved",
    "demo_order_placement_approved",
    "live_order_placement_approved",
    "execution_approved",
    "broker_request_constructed",
    "mt5_request_constructed",
    "order_payload_constructed",
    "dispatch_attempted",
    "terminal_mutated",
    "broker_state_mutated",
)


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(p.read_text(encoding="utf-8-sig").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{p}:{line_number}: invalid JSONL: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{p}:{line_number}: expected JSON object, got {type(value).__name__}")
        records.append(value)
    return records


def write_jsonl(path: str | Path, records: Sequence[Mapping[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _line_excerpt(line: str, limit: int = 160) -> str:
    normalized = line.strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def _scan_text_for_prohibited_patterns(text: str, *, path: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    compiled = [
        (pattern_id, re.compile(pattern, flags=re.IGNORECASE | re.MULTILINE))
        for pattern_id, pattern in PROHIBITED_PATTERNS
    ]

    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern_id, pattern in compiled:
            match = pattern.search(line)
            if match:
                findings.append(
                    {
                        "path": path,
                        "line": line_number,
                        "pattern_id": pattern_id,
                        "matched_text": match.group(0),
                        "line_excerpt": _line_excerpt(line),
                    }
                )

    return findings


def scan_adapter_boundary_targets(
    targets: Sequence[str | Path] | None = None,
    *,
    root: str | Path = ".",
) -> list[dict[str, Any]]:
    repo_root = Path(root)
    target_values = tuple(targets) if targets is not None else DEFAULT_ADAPTER_BOUNDARY_TARGETS
    results: list[dict[str, Any]] = []

    for target in target_values:
        target_path = Path(target)
        path = target_path if target_path.is_absolute() else repo_root / target_path
        display_path = _display_path(path, repo_root)

        if not path.exists():
            results.append(
                {
                    "path": display_path,
                    "exists": False,
                    "line_count": 0,
                    "findings": [
                        {
                            "path": display_path,
                            "line": None,
                            "pattern_id": "target_missing",
                            "matched_text": "",
                            "line_excerpt": "",
                        }
                    ],
                }
            )
            continue

        text = path.read_text(encoding="utf-8-sig")
        results.append(
            {
                "path": display_path,
                "exists": True,
                "line_count": len(text.splitlines()),
                "findings": _scan_text_for_prohibited_patterns(text, path=display_path),
            }
        )

    return results


def build_static_verifier_record(
    targets: Sequence[str | Path] | None = None,
    *,
    root: str | Path = ".",
) -> dict[str, Any]:
    target_results = scan_adapter_boundary_targets(targets, root=root)
    findings = [finding for result in target_results for finding in result["findings"]]

    record: dict[str, Any] = {
        "schema": SCHEMA,
        "kind": KIND,
        "status": STATUS,
        "decision": DECISION,
        "phase4_approved": True,
        "demo_execution_adapter_implementation_approved": True,
        "execution_adapter_implementation_approved": True,
        "execution_adapter_use_approved": False,
        "execution_adapter_approved": False,
        "broker_request_approved": False,
        "mt5_execution_approved": False,
        "terminal_mutation_approved": False,
        "demo_order_placement_approved": False,
        "live_order_placement_approved": False,
        "execution_approved": False,
        "broker_request_constructed": False,
        "mt5_request_constructed": False,
        "order_payload_constructed": False,
        "dispatch_attempted": False,
        "terminal_mutated": False,
        "broker_state_mutated": False,
        "adapter_boundary_static_verified": not findings,
        "target_count": len(target_results),
        "prohibited_finding_count": len(findings),
        "target_files": target_results,
        "violations": [f"{finding['path']}:{finding['line']}:{finding['pattern_id']}" for finding in findings],
    }
    record["verdict"] = "PASS" if not findings else "FAIL"
    return record


def build_static_verifier_records(
    targets: Sequence[str | Path] | None = None,
    *,
    root: str | Path = ".",
) -> list[dict[str, Any]]:
    return [build_static_verifier_record(targets, root=root)]


def verify_static_verifier_records(
    records: Sequence[Mapping[str, Any]],
    *,
    require_pass: bool = True,
) -> list[str]:
    violations: list[str] = []

    if not records:
        return ["no_records"]
    if len(records) != 1:
        violations.append(f"expected_one_record_got_{len(records)}")

    for index, record in enumerate(records):
        prefix = f"record_{index}"

        expected_values = {
            "schema": SCHEMA,
            "kind": KIND,
            "status": STATUS,
            "decision": DECISION,
        }
        if require_pass:
            expected_values["verdict"] = "PASS"

        for key, expected in expected_values.items():
            if record.get(key) != expected:
                violations.append(f"{prefix}_{key}_mismatch")

        for key in (
            "phase4_approved",
            "demo_execution_adapter_implementation_approved",
            "execution_adapter_implementation_approved",
        ):
            if record.get(key) is not True:
                violations.append(f"{prefix}_{key}_not_true")

        for key in FALSE_AUTHORITY_FLAGS:
            if record.get(key) is not False:
                violations.append(f"{prefix}_{key}_not_false")

        if record.get("adapter_boundary_static_verified") is not True:
            violations.append(f"{prefix}_adapter_boundary_static_verified_not_true")

        target_count = record.get("target_count")
        if not isinstance(target_count, int) or target_count <= 0:
            violations.append(f"{prefix}_target_count_invalid")

        prohibited_count = record.get("prohibited_finding_count")
        if prohibited_count != 0:
            violations.append(f"{prefix}_prohibited_finding_count_nonzero")

        builder_violations = record.get("violations")
        if builder_violations:
            violations.append(f"{prefix}_builder_violations_present")

        target_files = record.get("target_files")
        if not isinstance(target_files, list) or not target_files:
            violations.append(f"{prefix}_target_files_missing")
        else:
            for target_index, target in enumerate(target_files):
                if not isinstance(target, Mapping):
                    violations.append(f"{prefix}_target_{target_index}_not_object")
                    continue
                if target.get("exists") is not True:
                    violations.append(f"{prefix}_target_{target_index}_missing")
                if target.get("findings"):
                    violations.append(f"{prefix}_target_{target_index}_findings_present")

    return violations


def format_verification_summary(records: Sequence[Mapping[str, Any]], violations: Sequence[str]) -> str:
    target_count = records[0].get("target_count", 0) if records else 0
    finding_count = records[0].get("prohibited_finding_count", 0) if records else 0
    lines = [
        f"H024 demo adapter boundary static verifier records: {len(records)}",
        f"Scanned adapter-boundary files: {target_count}",
        f"Prohibited findings: {finding_count}",
        f"Violations: {len(violations)}",
    ]
    if violations:
        lines.extend(f"- {violation}" for violation in violations)
    lines.append(f"Verdict: {'PASS' if not violations else 'FAIL'}")
    return "\n".join(lines)