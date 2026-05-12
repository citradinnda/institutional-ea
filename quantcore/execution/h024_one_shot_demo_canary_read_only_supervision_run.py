from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


DEFAULT_OUTPUT_PATH = Path("reports/h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl")


@dataclass(frozen=True)
class SupervisionStage:
    name: str
    command: tuple[str, ...]
    description: str
    mt5_access: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_stages() -> tuple[SupervisionStage, ...]:
    return (
        SupervisionStage(
            name="build_monitor",
            command=(sys.executable, "scripts/build_h024_one_shot_demo_canary_monitor_jsonl.py"),
            description="Refresh the read-only broker monitor packet.",
            mt5_access="read_only_via_monitor_script",
        ),
        SupervisionStage(
            name="verify_monitor",
            command=(
                sys.executable,
                "scripts/verify_h024_one_shot_demo_canary_monitor_jsonl.py",
                "reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl",
                "--require-pass",
            ),
            description="Verify the read-only broker monitor packet.",
            mt5_access="none",
        ),
        SupervisionStage(
            name="build_lifecycle_decision",
            command=(sys.executable, "scripts/build_h024_one_shot_demo_canary_lifecycle_decision_jsonl.py"),
            description="Refresh the continue-hold lifecycle decision from the monitor packet.",
            mt5_access="none",
        ),
        SupervisionStage(
            name="verify_lifecycle_decision",
            command=(
                sys.executable,
                "scripts/verify_h024_one_shot_demo_canary_lifecycle_decision_jsonl.py",
                "reports/h024_standard_demo_one_shot_demo_canary_lifecycle_decision.jsonl",
                "--require-pass",
            ),
            description="Verify the lifecycle decision packet.",
            mt5_access="none",
        ),
        SupervisionStage(
            name="build_observation_analysis",
            command=(sys.executable, "scripts/build_h024_one_shot_demo_canary_observation_analysis_jsonl.py"),
            description="Refresh the durable post-canary observation analysis packet.",
            mt5_access="none",
        ),
        SupervisionStage(
            name="verify_observation_analysis",
            command=(
                sys.executable,
                "scripts/verify_h024_one_shot_demo_canary_observation_analysis_jsonl.py",
                "reports/h024_standard_demo_one_shot_demo_canary_observation_analysis.jsonl",
                "--require-pass",
            ),
            description="Verify the observation analysis packet.",
            mt5_access="none",
        ),
        SupervisionStage(
            name="build_supervisory_state",
            command=(sys.executable, "scripts/build_h024_one_shot_demo_canary_supervisory_state_jsonl.py"),
            description="Refresh the top-level read-only supervisory state packet.",
            mt5_access="none",
        ),
        SupervisionStage(
            name="verify_supervisory_state",
            command=(
                sys.executable,
                "scripts/verify_h024_one_shot_demo_canary_supervisory_state_jsonl.py",
                "reports/h024_standard_demo_one_shot_demo_canary_supervisory_state.jsonl",
                "--require-pass",
            ),
            description="Verify the top-level supervisory state packet.",
            mt5_access="none",
        ),
    )


def _safe_command_tokens(command: tuple[str, ...]) -> list[str]:
    return [str(token) for token in command]


def _command_text(command: tuple[str, ...]) -> str:
    return " ".join(_safe_command_tokens(command))


def assert_stage_commands_are_read_only(stages: tuple[SupervisionStage, ...]) -> list[str]:
    violations: list[str] = []
    forbidden_fragments = [
        "--send",
        "run_h024_one_shot_demo_canary.py",
        "order_send",
        "order_check",
        "close_position",
        "position_close",
        "modify_position",
        "order_modify",
        "trade_loop",
        "trading_loop",
    ]

    for stage in stages:
        command_text = _command_text(stage.command).lower()
        for fragment in forbidden_fragments:
            if fragment.lower() in command_text:
                violations.append(f"{stage.name} command contains forbidden fragment {fragment!r}: {command_text}")

    return violations


def write_jsonl(path: str | Path, records: list[dict[str, Any]]) -> None:
    candidate = Path(path)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in records)
    candidate.write_text(payload, encoding="utf-8")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    candidate = Path(path)
    if not candidate.exists():
        return []

    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(candidate.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        loaded = json.loads(stripped)
        if not isinstance(loaded, dict):
            raise ValueError(f"{candidate}:{line_number} is not a JSON object")
        records.append(loaded)
    return records


def _default_command_runner(command: tuple[str, ...], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def run_read_only_supervision(
    *,
    repo_root: str | Path = ".",
    stages: tuple[SupervisionStage, ...] | None = None,
    command_runner: Callable[[tuple[str, ...], Path], Any] = _default_command_runner,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    repo_root_path = Path(repo_root)
    stage_plan = stages if stages is not None else default_stages()
    preflight_violations = assert_stage_commands_are_read_only(stage_plan)

    stage_records: list[dict[str, Any]] = []
    first_failed_stage: str | None = None

    if not preflight_violations:
        for stage in stage_plan:
            completed = command_runner(stage.command, repo_root_path)
            returncode = int(getattr(completed, "returncode", 1))
            stdout = getattr(completed, "stdout", "")
            stderr = getattr(completed, "stderr", "")

            stage_record = {
                "name": stage.name,
                "description": stage.description,
                "command": _safe_command_tokens(stage.command),
                "mt5_access": stage.mt5_access,
                "returncode": returncode,
                "stdout": stdout,
                "stderr": stderr,
                "passed": returncode == 0,
            }
            stage_records.append(stage_record)

            if returncode != 0:
                first_failed_stage = stage.name
                break

    completed_count = sum(1 for stage in stage_records if stage["passed"])
    all_stages_passed = not preflight_violations and len(stage_records) == len(stage_plan) and all(
        stage["passed"] for stage in stage_records
    )

    violations: list[str] = list(preflight_violations)
    if first_failed_stage is not None:
        violations.append(f"stage failed: {first_failed_stage}")
    if not preflight_violations and len(stage_records) != len(stage_plan):
        violations.append(f"supervision stopped after {len(stage_records)} of {len(stage_plan)} stages")

    verdict = "PASS" if all_stages_passed and not violations else "FAIL"

    return {
        "schema_version": 1,
        "record_type": "h024_one_shot_demo_canary_read_only_supervision_run",
        "generated_at_utc": generated_at_utc or utc_now_iso(),
        "strategy": "H024",
        "verdict": verdict,
        "violations": violations,
        "stage_count": len(stage_plan),
        "completed_stage_count": completed_count,
        "first_failed_stage": first_failed_stage,
        "stages": stage_records,
        "broker_mutation_authorized": False,
        "mt5_mutation_authorized": False,
        "entry_authorized": False,
        "close_authorized": False,
        "modify_authorized": False,
        "live_deployment_authorized": False,
        "trading_loop_authorized": False,
        "edge_inference_authorized": False,
        "operator_next_action": (
            "read_supervisory_state_and_continue_observation"
            if verdict == "PASS"
            else "stop_and_investigate_failed_read_only_stage_no_broker_mutation"
        ),
        "output_artifacts": {
            "monitor": "reports/h024_standard_demo_one_shot_demo_canary_monitor.jsonl",
            "lifecycle_decision": "reports/h024_standard_demo_one_shot_demo_canary_lifecycle_decision.jsonl",
            "observation_analysis": "reports/h024_standard_demo_one_shot_demo_canary_observation_analysis.jsonl",
            "supervisory_state": "reports/h024_standard_demo_one_shot_demo_canary_supervisory_state.jsonl",
        },
        "automation_boundary": {
            "read_only_stack_automated": True,
            "broker_mutation_automated": False,
            "usd_jpy_automated": False,
            "usd_jpy_requires_separate_readiness": True,
            "kill_switches_required_before_trading_loop": True,
            "black_swan_guards_required_before_trading_loop": True,
        },
    }


def verify_supervision_run_record(record: dict[str, Any], *, require_pass: bool = False) -> list[str]:
    violations: list[str] = []

    if record.get("record_type") != "h024_one_shot_demo_canary_read_only_supervision_run":
        violations.append(f"unexpected record_type: {record.get('record_type')!r}")

    embedded = record.get("violations")
    if not isinstance(embedded, list):
        violations.append("violations must be a list")
    elif embedded:
        violations.extend(f"embedded violation: {item}" for item in embedded)

    for field in [
        "broker_mutation_authorized",
        "mt5_mutation_authorized",
        "entry_authorized",
        "close_authorized",
        "modify_authorized",
        "live_deployment_authorized",
        "trading_loop_authorized",
        "edge_inference_authorized",
    ]:
        if record.get(field) is not False:
            violations.append(f"{field} must be False")

    stages = record.get("stages")
    if not isinstance(stages, list):
        violations.append("stages must be a list")
    else:
        for stage in stages:
            if not isinstance(stage, dict):
                violations.append("each stage must be an object")
                continue
            command = stage.get("command", [])
            if not isinstance(command, list):
                violations.append(f"stage {stage.get('name')!r} command must be a list")
                continue
            command_text = " ".join(str(token) for token in command).lower()
            for forbidden in ["--send", "run_h024_one_shot_demo_canary.py", "order_send", "close_position", "trading_loop"]:
                if forbidden in command_text:
                    violations.append(f"stage {stage.get('name')!r} command contains forbidden fragment {forbidden!r}")
            if require_pass and stage.get("passed") is not True:
                violations.append(f"stage {stage.get('name')!r} must pass")

    boundary = record.get("automation_boundary", {})
    if not isinstance(boundary, dict):
        violations.append("automation_boundary must be an object")
    else:
        if boundary.get("read_only_stack_automated") is not True:
            violations.append("read_only_stack_automated must be True")
        if boundary.get("broker_mutation_automated") is not False:
            violations.append("broker_mutation_automated must be False")
        if boundary.get("usd_jpy_requires_separate_readiness") is not True:
            violations.append("usd_jpy_requires_separate_readiness must be True")
        if boundary.get("kill_switches_required_before_trading_loop") is not True:
            violations.append("kill_switches_required_before_trading_loop must be True")
        if boundary.get("black_swan_guards_required_before_trading_loop") is not True:
            violations.append("black_swan_guards_required_before_trading_loop must be True")

    if require_pass and record.get("verdict") != "PASS":
        violations.append(f"verdict must be PASS, observed {record.get('verdict')!r}")

    return violations
