from __future__ import annotations

import ast
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
    "quantcore/execution/h024_demo_adapter_noop_transport_contract.py",
    "scripts/build_h024_demo_adapter_noop_transport_contract_jsonl.py",
    "scripts/verify_h024_demo_adapter_noop_transport_contract_jsonl.py",
    "quantcore/execution/h024_demo_adapter_noop_use_approval.py",
    "scripts/build_h024_demo_adapter_noop_use_approval_jsonl.py",
    "scripts/verify_h024_demo_adapter_noop_use_approval_jsonl.py",
    "quantcore/execution/h024_demo_adapter_noop_use_invocation_audit.py",
    "scripts/build_h024_demo_adapter_noop_use_invocation_audit_jsonl.py",
    "scripts/verify_h024_demo_adapter_noop_use_invocation_audit_jsonl.py",
    "quantcore/execution/h024_broker_request_construction_readiness_packet.py",
    "scripts/build_h024_broker_request_construction_readiness_packet_jsonl.py",
    "scripts/verify_h024_broker_request_construction_readiness_packet_jsonl.py",
    "quantcore/execution/h024_broker_request_preview_envelope.py",
    "scripts/build_h024_broker_request_preview_construction_approval_jsonl.py",
    "scripts/verify_h024_broker_request_preview_construction_approval_jsonl.py",
    "scripts/build_h024_broker_request_preview_envelope_jsonl.py",
    "scripts/verify_h024_broker_request_preview_envelope_jsonl.py",
'quantcore/execution/h024_broker_request_draft_construction_approval.py'
'quantcore/execution/h024_broker_request_draft_envelope.py'
'scripts/build_h024_broker_request_draft_construction_approval_jsonl.py'
'scripts/verify_h024_broker_request_draft_construction_approval_jsonl.py'
'scripts/build_h024_broker_request_draft_envelope_jsonl.py'
'scripts/verify_h024_broker_request_draft_envelope_jsonl.py'
)

PYTHON_PROHIBITED_IMPORT_ROOTS = frozenset({"MetaTrader5"})

PYTHON_PROHIBITED_ATTR_CALLS = frozenset(
    {
        "order_send",
        "order_check",
    }
)

PYTHON_PROHIBITED_MT5_SESSION_ATTR_CALLS = frozenset(
    {
        "initialize",
        "login",
        "shutdown",
    }
)

PYTHON_PROHIBITED_DIRECT_CALLS = frozenset(
    {
        "order_send",
        "order_check",
        "OrderSend",
        "OrderSendAsync",
        "OrderCheck",
        "CTrade",
        "MqlTradeRequest",
        "MqlTradeResult",
        "PositionOpen",
        "PositionClose",
        "PositionModify",
        "BuyStop",
        "SellStop",
        "BuyLimit",
        "SellLimit",
        "BuyStopLimit",
        "SellStopLimit",
    }
)

MQL_PROHIBITED_TEXT_PATTERNS: tuple[tuple[str, str], ...] = (
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


def _line_excerpt(lines: Sequence[str], line_number: int | None, limit: int = 160) -> str:
    if line_number is None or line_number < 1 or line_number > len(lines):
        return ""
    normalized = lines[line_number - 1].strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def _finding(
    *,
    path: str,
    line: int | None,
    pattern_id: str,
    matched_text: str,
    lines: Sequence[str],
) -> dict[str, Any]:
    return {
        "path": path,
        "line": line,
        "pattern_id": pattern_id,
        "matched_text": matched_text,
        "line_excerpt": _line_excerpt(lines, line),
    }


def _root_name(node: ast.AST) -> str | None:
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    if isinstance(current, ast.Name):
        return current.id
    return None


def _call_name(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return node.__class__.__name__


def _scan_python_ast_for_prohibited_patterns(text: str, *, path: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    findings: list[dict[str, Any]] = []

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        findings.append(
            _finding(
                path=path,
                line=exc.lineno,
                pattern_id="python_syntax_error",
                matched_text=exc.msg,
                lines=lines,
            )
        )
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in PYTHON_PROHIBITED_IMPORT_ROOTS:
                    findings.append(
                        _finding(
                            path=path,
                            line=node.lineno,
                            pattern_id="metatrader5_import",
                            matched_text=alias.name,
                            lines=lines,
                        )
                    )

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".", 1)[0]
            if root in PYTHON_PROHIBITED_IMPORT_ROOTS:
                findings.append(
                    _finding(
                        path=path,
                        line=node.lineno,
                        pattern_id="metatrader5_import",
                        matched_text=module,
                        lines=lines,
                    )
                )

        elif isinstance(node, ast.Call):
            func = node.func

            if isinstance(func, ast.Attribute):
                attr = func.attr
                root = _root_name(func.value)
                if attr in PYTHON_PROHIBITED_ATTR_CALLS:
                    findings.append(
                        _finding(
                            path=path,
                            line=node.lineno,
                            pattern_id="python_execution_attr_call",
                            matched_text=_call_name(func),
                            lines=lines,
                        )
                    )
                elif (
                    attr in PYTHON_PROHIBITED_MT5_SESSION_ATTR_CALLS
                    and root in {"mt5", "MetaTrader5"}
                ):
                    findings.append(
                        _finding(
                            path=path,
                            line=node.lineno,
                            pattern_id="python_mt5_session_call",
                            matched_text=_call_name(func),
                            lines=lines,
                        )
                    )

            elif isinstance(func, ast.Name) and func.id in PYTHON_PROHIBITED_DIRECT_CALLS:
                findings.append(
                    _finding(
                        path=path,
                        line=node.lineno,
                        pattern_id="python_execution_direct_call",
                        matched_text=func.id,
                        lines=lines,
                    )
                )

    return findings


def _scan_mql_text_for_prohibited_patterns(text: str, *, path: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    findings: list[dict[str, Any]] = []
    compiled = [
        (pattern_id, re.compile(pattern, flags=re.IGNORECASE | re.MULTILINE))
        for pattern_id, pattern in MQL_PROHIBITED_TEXT_PATTERNS
    ]

    for line_number, line in enumerate(lines, start=1):
        for pattern_id, pattern in compiled:
            match = pattern.search(line)
            if match:
                findings.append(
                    _finding(
                        path=path,
                        line=line_number,
                        pattern_id=pattern_id,
                        matched_text=match.group(0),
                        lines=lines,
                    )
                )

    return findings


def _scan_text_for_prohibited_patterns(text: str, *, path: str) -> list[dict[str, Any]]:
    suffix = Path(path).suffix.lower()
    if suffix == ".py":
        return _scan_python_ast_for_prohibited_patterns(text, path=path)
    if suffix in {".mq5", ".mqh", ".mq4"}:
        return _scan_mql_text_for_prohibited_patterns(text, path=path)
    return []


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
