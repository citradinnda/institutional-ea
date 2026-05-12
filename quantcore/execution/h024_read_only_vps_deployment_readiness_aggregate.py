from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = "1.0.0"
STRATEGY = "H024"
PACKET_TYPE = "h024_read_only_vps_deployment_readiness_aggregate"

EXPECTED_SERVER = "Exness-MT5Trial6"
EXPECTED_ACCOUNT_CURRENCY = "USD"
EXPECTED_RUNTIME_SYMBOL = "XAUUSDm"
EXPECTED_MODEL_SYMBOL = "XAUUSD"
EXPECTED_MAGIC = 240024
EXPECTED_VOLUME = 0.01
EXPECTED_POSITION_TYPE = 1
EXPECTED_EXACT_TICKET = 4413054432
EXPECTED_EXACT_IDENTIFIER = 4413054432

PASS_VERDICT = "PASS"
FAIL_VERDICT = "FAIL_CLOSED"

PASS_OPERATOR_STATE = "READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED"
PASS_OPERATOR_NEXT_ACTION = "RUN_READ_ONLY_OBSERVER_WORKFLOW_NO_TRADING_AUTHORIZED"

FAIL_OPERATOR_STATE = "FAIL_CLOSED_READ_ONLY_VPS_OBSERVER_DEPLOYMENT_READINESS_UNVERIFIED_NO_TRADING_AUTHORIZED"
FAIL_OPERATOR_NEXT_ACTION = "FAIL_CLOSED_OPERATOR_REVIEW_REQUIRED_NO_TRADING_AUTHORIZED"

REPORT_PATH = Path("reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl")
RUNNER_PATH = Path("scripts/run_h024_read_only_vps_observer_once.ps1")

AUTHORIZATION_FIELDS = (
    "broker_mutation_authorized",
    "order_check_authorized",
    "order_send_authorized",
    "entry_authorized",
    "close_modify_authorized",
    "xauusd_order_authorized",
    "usdjpy_order_authorized",
    "trading_loop_authorized",
    "automatic_execution_authorized",
)

CONSTRUCTION_FIELDS = (
    "live_broker_request_constructed",
    "executable_trade_request_constructed",
    "mt5_request_dictionary_constructed",
)

TIMESTAMP_KEYS = (
    "observed_at_utc",
    "generated_at_utc",
    "created_at_utc",
    "evaluated_at_utc",
    "built_at_utc",
    "timestamp_utc",
    "timestamp",
)

FORBIDDEN_RUNBOOK_TOKENS = (
    "order_send",
    "order_check",
    "symbol_select",
    "trade_action",
    "one_shot_demo_canary",
    "run_h024_one_shot_demo_canary",
    "h024_one_shot_demo_canary",
    "close_position",
    "modify_position",
)

REQUEST_OBJECT_KEY_FRAGMENTS = (
    "live_broker_request",
    "executable_trade_request",
    "mt5_request_dictionary",
    "order_check_request",
    "order_send_request",
)


@dataclass(frozen=True)
class UpstreamSpec:
    name: str
    path_candidates: tuple[str, ...]


UPSTREAM_SPECS: tuple[UpstreamSpec, ...] = (
    UpstreamSpec("runtime_heartbeat", (
        "reports/h024_runtime_safety_heartbeat.jsonl",
        "reports/h024_runtime_heartbeat.jsonl",
    )),
    UpstreamSpec("runtime_lockout_reader", (
        "reports/h024_runtime_safety_lockout.jsonl",
    )),
    UpstreamSpec("tick_spread_supervisor", (
        "reports/h024_runtime_tick_spread_safety_supervisor.jsonl",
        "reports/h024_runtime_tick_spread_supervisor.jsonl",
    )),
    UpstreamSpec("exposure_inventory_supervisor", (
        "reports/h024_runtime_exposure_inventory_safety_supervisor.jsonl",
        "reports/h024_exposure_inventory_safety_supervisor.jsonl",
    )),
    UpstreamSpec("account_risk_margin_supervisor", (
        "reports/h024_runtime_account_risk_margin_safety_supervisor.jsonl",
        "reports/h024_account_risk_margin_safety_supervisor.jsonl",
    )),
    UpstreamSpec("runtime_safety_aggregate", (
        "reports/h024_runtime_safety_aggregate_supervisor.jsonl",
        "reports/h024_runtime_safety_aggregate.jsonl",
    )),
    UpstreamSpec("unified_read_only_runtime_supervision", (
        "reports/h024_unified_read_only_post_canary_runtime_supervision.jsonl",
        "reports/h024_unified_read_only_runtime_supervision.jsonl",
        "reports/h024_unified_post_canary_runtime_supervision.jsonl",
    )),
    UpstreamSpec("runtime_no_mutation_safety_gate", (
        "reports/h024_runtime_no_mutation_safety_gate.jsonl",
    )),
    UpstreamSpec("exact_ticket_close_modify_governance", (
        "reports/h024_exact_ticket_canary_close_modify_governance.jsonl",
        "reports/h024_exact_ticket_canary_close_modify_governance_spec.jsonl",
        "reports/h024_exact_ticket_close_modify_governance.jsonl",
        "reports/h024_exact_ticket_close_modify_governance_spec.jsonl",
    )),
    UpstreamSpec("exact_ticket_decision_artifact_validator", (
        "reports/h024_exact_ticket_canary_close_modify_decision_artifact.jsonl",
        "reports/h024_exact_ticket_canary_close_modify_decision_artifact_validator.jsonl",
        "reports/h024_exact_ticket_close_modify_decision_artifact.jsonl",
        "reports/h024_exact_ticket_close_modify_decision_artifact_validator.jsonl",
    )),
    UpstreamSpec("exact_ticket_pre_action_evidence_aggregate", (
        "reports/h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate.jsonl",
    )),
    UpstreamSpec("exact_ticket_bar_age_exit_condition_evidence", (
        "reports/h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence.jsonl",
    )),
    UpstreamSpec("exact_ticket_manual_approval_gate_preview", (
        "reports/h024_exact_ticket_canary_close_modify_manual_approval_gate_preview.jsonl",
    )),
    UpstreamSpec("exact_ticket_operator_decision_v2_preview", (
        "reports/h024_exact_ticket_canary_close_modify_operator_decision_v2_preview.jsonl",
    )),
    UpstreamSpec("execution_readiness_dry_run_schema_preview", (
        "reports/h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview.jsonl",
    )),
    UpstreamSpec("read_only_black_swan_guard", (
        "reports/h024_read_only_black_swan_guard.jsonl",
    )),
)


MISSING = object()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def deep_find_value(obj: Any, key: str) -> Any:
    if isinstance(obj, Mapping):
        if key in obj:
            return obj[key]
        for value in obj.values():
            found = deep_find_value(value, key)
            if found is not MISSING:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = deep_find_value(item, key)
            if found is not MISSING:
                return found
    return MISSING


def upstream_timestamp_value(record: Mapping[str, Any]) -> Any:
    for key in TIMESTAMP_KEYS:
        found = deep_find_value(record, key)
        if found is not MISSING:
            return found
    return MISSING


def read_latest_jsonl_record(path: Path) -> Mapping[str, Any]:
    if not path.exists():
        raise ValueError(f"missing upstream report: {path}")
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError(f"empty upstream report: {path}")
    try:
        record = json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed upstream JSONL in {path}: {exc}") from exc
    if not isinstance(record, Mapping):
        raise ValueError(f"latest upstream record is not an object: {path}")
    return record


def resolve_existing_path(base_dir: Path, candidates: Sequence[str]) -> Path:
    for candidate in candidates:
        path = base_dir / candidate
        if path.exists():
            return path
    return base_dir / candidates[0]


def iter_suspicious_request_objects(obj: Any, path: str = "$") -> Iterable[str]:
    """Find actual executable/live request-like payloads, not safety-check booleans."""
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            key_text = str(key).lower()
            child_path = f"{path}.{key}"

            request_key = any(fragment in key_text for fragment in REQUEST_OBJECT_KEY_FRAGMENTS)
            safety_check_key = (
                key_text.endswith("_absent")
                or key_text.endswith("_blocked")
                or key_text.endswith("_constructed")
                or key_text.endswith("_authorized")
            )

            if request_key and not safety_check_key:
                if isinstance(value, Mapping) and value:
                    yield child_path
                elif isinstance(value, list) and value:
                    yield child_path
                elif isinstance(value, str) and value.strip():
                    yield child_path

            yield from iter_suspicious_request_objects(value, child_path)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            yield from iter_suspicious_request_objects(item, f"{path}[{index}]")


def bool_value(record: Mapping[str, Any], field: str) -> Any:
    direct = record.get(field, MISSING)
    if direct is not MISSING:
        return direct
    authorizations = record.get("authorizations")
    if isinstance(authorizations, Mapping) and field in authorizations:
        return authorizations[field]
    observed = record.get("observed")
    if isinstance(observed, Mapping) and field in observed:
        return observed[field]
    checks = record.get("checks")
    if isinstance(checks, Mapping) and field in checks:
        return checks[field]
    return deep_find_value(record, field)


def validate_upstream_record(
    *,
    spec: UpstreamSpec,
    path: Path,
    record: Mapping[str, Any],
    now_utc: datetime,
    max_age_minutes: int,
) -> tuple[dict[str, Any], list[str]]:
    violations: list[str] = []

    verdict = record.get("verdict")
    operator_state = record.get("operator_state")
    operator_next_action = record.get("operator_next_action")

    if record.get("strategy") not in (STRATEGY, None):
        violations.append(f"{spec.name}: wrong strategy {record.get('strategy')!r}")

    if verdict != PASS_VERDICT:
        violations.append(f"{spec.name}: upstream verdict is not PASS: {verdict!r}")

    upstream_violations = record.get("violations")
    if upstream_violations not in (None, []):
        violations.append(f"{spec.name}: upstream has embedded violations")

    raw_timestamp = upstream_timestamp_value(record)
    parsed_timestamp = parse_timestamp(raw_timestamp)
    age_seconds: float | None = None
    if parsed_timestamp is None:
        violations.append(f"{spec.name}: missing or malformed upstream timestamp")
        observed_timestamp = None
    else:
        observed_timestamp = isoformat_utc(parsed_timestamp)
        age_seconds = max(0.0, (now_utc - parsed_timestamp).total_seconds())
        if parsed_timestamp > now_utc + timedelta(minutes=2):
            violations.append(f"{spec.name}: upstream timestamp is in the future")
        if age_seconds > max_age_minutes * 60:
            violations.append(
                f"{spec.name}: upstream evidence stale at {int(age_seconds)} seconds "
                f"(max {max_age_minutes * 60} seconds)"
            )

    effective_blocked = bool_value(record, "effective_new_entries_blocked")
    if effective_blocked is not True:
        violations.append(f"{spec.name}: effective_new_entries_blocked is not true")

    for field in AUTHORIZATION_FIELDS:
        value = bool_value(record, field)
        if value is MISSING:
            violations.append(f"{spec.name}: missing authorization field {field}")
        elif value is not False:
            violations.append(f"{spec.name}: unsafe authorization field {field}={value!r}")

    for field in CONSTRUCTION_FIELDS:
        value = bool_value(record, field)
        if value is MISSING:
            continue
        if value is not False:
            violations.append(f"{spec.name}: unsafe construction field {field}={value!r}")

    for request_path in iter_suspicious_request_objects(record):
        violations.append(f"{spec.name}: executable/live request object present at {request_path}")

    if spec.name == "read_only_black_swan_guard":
        exact_ticket = deep_find_value(record, "exact_ticket")
        exact_identifier = deep_find_value(record, "exact_identifier")
        black_swan_clear = deep_find_value(record, "black_swan_guard_clear")
        black_swan_triggered = deep_find_value(record, "black_swan_guard_triggered")
        if exact_ticket != EXPECTED_EXACT_TICKET:
            violations.append(f"{spec.name}: exact_ticket mismatch {exact_ticket!r}")
        if exact_identifier != EXPECTED_EXACT_IDENTIFIER:
            violations.append(f"{spec.name}: exact_identifier mismatch {exact_identifier!r}")
        if black_swan_clear is not True:
            violations.append(f"{spec.name}: black_swan_guard_clear is not true")
        if black_swan_triggered is not False:
            violations.append(f"{spec.name}: black_swan_guard_triggered is not false")

    summary = {
        "name": spec.name,
        "path": str(path),
        "verdict": verdict,
        "operator_state": operator_state,
        "operator_next_action": operator_next_action,
        "observed_timestamp_utc": observed_timestamp,
        "age_seconds": age_seconds,
    }
    return summary, violations


def reports_dir_writable(reports_dir: Path) -> tuple[bool, str | None]:
    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=reports_dir,
            prefix=".h024_readiness_write_check_",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write("read-only observer report path check\n")
            temp_path = Path(handle.name)
        temp_path.unlink(missing_ok=True)
        return True, None
    except Exception as exc:  # pragma: no cover - platform-specific exception details
        return False, str(exc)


def check_environment(
    *,
    base_dir: Path,
    reports_dir: Path,
    require_venv: bool,
    require_mt5_package: bool,
) -> tuple[dict[str, Any], list[str]]:
    violations: list[str] = []

    venv_env = os.environ.get("VIRTUAL_ENV")
    executable_parts = tuple(part.lower() for part in Path(sys.executable).parts)
    venv_active = bool(venv_env) or ".venv" in executable_parts

    mt5_spec = importlib.util.find_spec("MetaTrader5")
    mt5_package_available = mt5_spec is not None

    writable, write_error = reports_dir_writable(reports_dir)

    checks = {
        "base_dir": str(base_dir),
        "base_dir_exists": base_dir.exists(),
        "python_executable": sys.executable,
        "virtual_env": venv_env,
        "venv_active_or_venv_python": venv_active,
        "require_venv": require_venv,
        "platform": platform.platform(),
        "system": platform.system(),
        "reports_dir": str(reports_dir),
        "reports_dir_exists": reports_dir.exists(),
        "reports_dir_writable": writable,
        "reports_dir_write_error": write_error,
        "mt5_package_available": mt5_package_available,
        "require_mt5_package": require_mt5_package,
        "mt5_check_scope": "package-availability-only; runtime MT5/account checks are consumed from read-only heartbeat upstream",
    }

    if not base_dir.exists():
        violations.append(f"base directory does not exist: {base_dir}")
    if require_venv and not venv_active:
        violations.append("Python virtual environment is not active and sys.executable is not under .venv")
    if not writable:
        violations.append(f"reports/ is not writable: {write_error}")
    if require_mt5_package and not mt5_package_available:
        violations.append("MetaTrader5 package is not importable for read-only VPS observer environment")

    return checks, violations


def operator_runbook_commands(base_dir: Path) -> list[dict[str, Any]]:
    repo = str(base_dir)
    runner = str((base_dir / RUNNER_PATH).resolve())
    return [
        {
            "name": "enter_repo",
            "operator_command": f"cd {repo}",
            "execution_role": "operator_manual_setup",
        },
        {
            "name": "activate_venv",
            "operator_command": r".\.venv\Scripts\Activate.ps1",
            "execution_role": "operator_manual_setup",
        },
        {
            "name": "run_read_only_observer_once",
            "operator_command": r"powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_h024_read_only_vps_observer_once.ps1",
            "execution_role": "read_only_observer_packet_generation",
        },
        {
            "name": "verify_deployment_readiness_report",
            "operator_command": r"python scripts\verify_h024_read_only_vps_deployment_readiness_aggregate_jsonl.py reports\h024_read_only_vps_deployment_readiness_aggregate.jsonl --require-pass",
            "execution_role": "read_only_report_verification",
        },
        {
            "name": "scheduled_task_preview_operator_review_only",
            "operator_command": (
                'schtasks /Create /SC MINUTE /MO 5 /TN H024ReadOnlyObserver '
                f'/TR "powershell -NoProfile -ExecutionPolicy Bypass -File {runner}"'
            ),
            "execution_role": "preview_only_not_executed_by_packet",
        },
    ]


def validate_runbook_commands(commands: Sequence[Mapping[str, Any]]) -> list[str]:
    violations: list[str] = []
    for command in commands:
        command_text = str(command.get("operator_command", "")).lower()
        name = str(command.get("name", "unnamed"))
        for forbidden in FORBIDDEN_RUNBOOK_TOKENS:
            if forbidden in command_text:
                violations.append(f"runbook command {name!r} contains forbidden token {forbidden!r}")
        if not command_text.strip():
            violations.append(f"runbook command {name!r} is empty")
    return violations


def blocked_authorizations() -> dict[str, bool]:
    return {field: False for field in AUTHORIZATION_FIELDS}


def blocked_construction_flags() -> dict[str, bool]:
    return {field: False for field in CONSTRUCTION_FIELDS}


def build_readiness_aggregate(
    *,
    base_dir: Path,
    max_age_minutes: int = 60,
    require_venv: bool = True,
    require_mt5_package: bool = True,
    now_utc: datetime | None = None,
) -> dict[str, Any]:
    now = now_utc or utc_now()
    base_dir = base_dir.resolve()
    reports_dir = base_dir / "reports"

    violations: list[str] = []
    upstream_summaries: list[dict[str, Any]] = []
    consumed_upstreams: dict[str, str] = {}

    for spec in UPSTREAM_SPECS:
        path = resolve_existing_path(base_dir, spec.path_candidates)
        consumed_upstreams[spec.name] = str(path)
        try:
            record = read_latest_jsonl_record(path)
        except ValueError as exc:
            upstream_summaries.append({
                "name": spec.name,
                "path": str(path),
                "verdict": None,
                "operator_state": None,
                "operator_next_action": None,
                "observed_timestamp_utc": None,
                "age_seconds": None,
            })
            violations.append(f"{spec.name}: {exc}")
            continue
        summary, upstream_violations = validate_upstream_record(
            spec=spec,
            path=path,
            record=record,
            now_utc=now,
            max_age_minutes=max_age_minutes,
        )
        upstream_summaries.append(summary)
        violations.extend(upstream_violations)

    environment, environment_violations = check_environment(
        base_dir=base_dir,
        reports_dir=reports_dir,
        require_venv=require_venv,
        require_mt5_package=require_mt5_package,
    )
    violations.extend(environment_violations)

    commands = operator_runbook_commands(base_dir)
    violations.extend(validate_runbook_commands(commands))

    runner_exists = (base_dir / RUNNER_PATH).exists()
    if not runner_exists:
        violations.append(f"read-only observer runner is missing: {RUNNER_PATH}")

    verdict = PASS_VERDICT if not violations else FAIL_VERDICT

    checks = {
        "read_only_observer_mode_declared": True,
        "vps_read_only_observer_deployment_ready_for_operator_review": verdict == PASS_VERDICT,
        "observer_runner_path": str(RUNNER_PATH),
        "observer_runner_exists": runner_exists,
        "all_required_upstreams_consumed": len(upstream_summaries) == len(UPSTREAM_SPECS),
        "upstream_count": len(upstream_summaries),
        "max_upstream_age_minutes": max_age_minutes,
        "reports_path_checked": True,
        "environment_checked": True,
        "operator_runbook_commands_checked": True,
        "mt5_runtime_check_source": "runtime_heartbeat_upstream",
        "mt5_package_availability_checked_locally": True,
        "black_swan_guard_consumed": "read_only_black_swan_guard" in consumed_upstreams,
        "exact_canary_identity_locked": True,
        "scheduled_command_preview_only": True,
        "deployment_readiness_authorizes_trading": False,
        "deployment_readiness_authorizes_close_modify": False,
        "read_only_observer_runner_authorizes_trading_loop": False,
        "read_only_observer_runner_authorizes_broker_mutation": False,
    }

    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "observed_at_utc": isoformat_utc(now),
        "expected": {
            "server": EXPECTED_SERVER,
            "account_currency": EXPECTED_ACCOUNT_CURRENCY,
            "runtime_symbol": EXPECTED_RUNTIME_SYMBOL,
            "model_symbol": EXPECTED_MODEL_SYMBOL,
            "magic": EXPECTED_MAGIC,
            "volume": EXPECTED_VOLUME,
            "position_type": EXPECTED_POSITION_TYPE,
            "exact_ticket": EXPECTED_EXACT_TICKET,
            "exact_identifier": EXPECTED_EXACT_IDENTIFIER,
            "mode": "read_only_vps_observer",
        },
        "observed": {
            "base_dir": str(base_dir),
            "reports_dir": str(reports_dir),
            "runner_path": str(base_dir / RUNNER_PATH),
            "upstream_reports": consumed_upstreams,
        },
        "environment": environment,
        "upstream_summaries": upstream_summaries,
        "operator_runbook": {
            "commands": commands,
            "expected_report_outputs": [
                "reports/h024_runtime_safety_heartbeat.jsonl",
                "reports/h024_runtime_safety_lockout.jsonl",
                "reports/h024_runtime_tick_spread_safety_supervisor.jsonl",
                "reports/h024_runtime_exposure_inventory_safety_supervisor.jsonl",
                "reports/h024_runtime_account_risk_margin_safety_supervisor.jsonl",
                "reports/h024_runtime_safety_aggregate_supervisor.jsonl",
                "reports/h024_unified_read_only_runtime_supervision.jsonl",
                "reports/h024_runtime_no_mutation_safety_gate.jsonl",
                "reports/h024_read_only_black_swan_guard.jsonl",
                "reports/h024_read_only_vps_deployment_readiness_aggregate.jsonl",
            ],
            "operator_notes": [
                "This runner is read-only packet generation only.",
                "PASS means VPS read-only observer readiness is coherent for operator review.",
                "PASS does not authorize trading, close/modify, order_check, order_send, symbol_select, or broker mutation.",
                "The scheduled task command is a preview for operator review and is not executed by this packet.",
            ],
        },
        "checks": checks,
        "authorizations": {
            "effective_new_entries_blocked": True,
            **blocked_authorizations(),
            **blocked_construction_flags(),
            "symbol_select_authorized": False,
            "read_only_observer_workflow_authorized_for_operator_review": verdict == PASS_VERDICT,
            "vps_deployment_readiness_authorizes_trading": False,
        },
        "effective_new_entries_blocked": True,
        **blocked_authorizations(),
        **blocked_construction_flags(),
        "symbol_select_authorized": False,
        "read_only_observer_workflow_authorized_for_operator_review": verdict == PASS_VERDICT,
        "vps_deployment_readiness_authorizes_trading": False,
        "operator_state": PASS_OPERATOR_STATE if verdict == PASS_VERDICT else FAIL_OPERATOR_STATE,
        "operator_next_action": PASS_OPERATOR_NEXT_ACTION if verdict == PASS_VERDICT else FAIL_OPERATOR_NEXT_ACTION,
        "violations": violations,
        "verdict": verdict,
    }
    return record


def write_jsonl_record(path: Path, record: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")


def load_jsonl_records(path: Path) -> list[Mapping[str, Any]]:
    if not path.exists():
        raise ValueError(f"missing JSONL file: {path}")
    records: list[Mapping[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"malformed JSONL at line {line_number}: {exc}") from exc
        if not isinstance(parsed, Mapping):
            raise ValueError(f"record at line {line_number} is not an object")
        records.append(parsed)
    if not records:
        raise ValueError(f"no records found in {path}")
    return records


def validate_readiness_record(record: Mapping[str, Any], *, require_pass: bool = False, record_number: int = 1) -> list[str]:
    prefix = f"record {record_number}"
    violations: list[str] = []

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append(f"{prefix}: wrong schema_version {record.get('schema_version')!r}")
    if record.get("strategy") != STRATEGY:
        violations.append(f"{prefix}: wrong strategy {record.get('strategy')!r}")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append(f"{prefix}: wrong packet_type {record.get('packet_type')!r}")

    verdict = record.get("verdict")
    embedded_violations = record.get("violations")
    if verdict not in (PASS_VERDICT, FAIL_VERDICT):
        violations.append(f"{prefix}: invalid verdict {verdict!r}")
    if require_pass and verdict != PASS_VERDICT:
        violations.append(f"{prefix}: --require-pass rejects verdict {verdict}")
    if verdict == PASS_VERDICT and embedded_violations not in ([], None):
        violations.append(f"{prefix}: PASS record contains embedded violations")

    timestamp = parse_timestamp(record.get("observed_at_utc"))
    if timestamp is None:
        violations.append(f"{prefix}: missing or malformed observed_at_utc")

    if record.get("effective_new_entries_blocked") is not True:
        violations.append(f"{prefix}: effective_new_entries_blocked is not true")

    for field in AUTHORIZATION_FIELDS:
        value = bool_value(record, field)
        if value is MISSING:
            violations.append(f"{prefix}: missing authorization field {field}")
        elif value is not False:
            violations.append(f"{prefix}: unsafe authorization field {field}={value!r}")

    for field in CONSTRUCTION_FIELDS:
        value = bool_value(record, field)
        if value is MISSING:
            violations.append(f"{prefix}: missing construction field {field}")
        elif value is not False:
            violations.append(f"{prefix}: unsafe construction field {field}={value!r}")

    symbol_select = bool_value(record, "symbol_select_authorized")
    if symbol_select is MISSING:
        violations.append(f"{prefix}: missing symbol_select_authorized")
    elif symbol_select is not False:
        violations.append(f"{prefix}: symbol_select_authorized is not false")

    trading_auth = bool_value(record, "vps_deployment_readiness_authorizes_trading")
    if trading_auth is not False:
        violations.append(f"{prefix}: vps_deployment_readiness_authorizes_trading is not false")

    expected = record.get("expected")
    if not isinstance(expected, Mapping):
        violations.append(f"{prefix}: missing expected object")
    else:
        if expected.get("exact_ticket") != EXPECTED_EXACT_TICKET:
            violations.append(f"{prefix}: expected exact_ticket mismatch")
        if expected.get("exact_identifier") != EXPECTED_EXACT_IDENTIFIER:
            violations.append(f"{prefix}: expected exact_identifier mismatch")
        if expected.get("mode") != "read_only_vps_observer":
            violations.append(f"{prefix}: expected mode is not read_only_vps_observer")

    upstream_summaries = record.get("upstream_summaries")
    if not isinstance(upstream_summaries, list) or len(upstream_summaries) != len(UPSTREAM_SPECS):
        violations.append(f"{prefix}: upstream_summaries missing or wrong length")

    runbook = record.get("operator_runbook")
    if not isinstance(runbook, Mapping):
        violations.append(f"{prefix}: missing operator_runbook")
    else:
        commands = runbook.get("commands")
        if not isinstance(commands, list) or not commands:
            violations.append(f"{prefix}: missing operator runbook commands")
        else:
            violations.extend(f"{prefix}: {message}" for message in validate_runbook_commands(commands))

    for request_path in iter_suspicious_request_objects(record):
        violations.append(f"{prefix}: executable/live request object present at {request_path}")

    return violations


def validate_records(records: Sequence[Mapping[str, Any]], *, require_pass: bool = False) -> list[str]:
    violations: list[str] = []
    for index, record in enumerate(records, start=1):
        violations.extend(validate_readiness_record(record, require_pass=require_pass, record_number=index))
    return violations


def summarize_record(record: Mapping[str, Any]) -> str:
    lines = [
        f"Record verdict: {record.get('verdict')}",
        f"Operator state: {record.get('operator_state')}",
        f"Operator next action: {record.get('operator_next_action')}",
        f"Exact ticket: {deep_find_value(record, 'exact_ticket')}",
        f"Exact identifier: {deep_find_value(record, 'exact_identifier')}",
        f"read_only_observer_workflow_authorized_for_operator_review: {bool_value(record, 'read_only_observer_workflow_authorized_for_operator_review')}",
        f"effective_new_entries_blocked: {bool_value(record, 'effective_new_entries_blocked')}",
    ]
    for field in AUTHORIZATION_FIELDS:
        lines.append(f"{field}: {bool_value(record, field)}")
    for field in CONSTRUCTION_FIELDS:
        lines.append(f"{field}: {bool_value(record, field)}")
    lines.append(f"symbol_select_authorized: {bool_value(record, 'symbol_select_authorized')}")
    lines.append(f"vps_deployment_readiness_authorizes_trading: {bool_value(record, 'vps_deployment_readiness_authorizes_trading')}")
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build/verify H024 read-only VPS deployment readiness aggregate.")
    parser.add_argument("--base-dir", default=".", help="Repository base directory.")
    parser.add_argument("--output", default=str(REPORT_PATH), help="Output JSONL path.")
    parser.add_argument("--max-age-minutes", type=int, default=60, help="Maximum upstream report age.")
    parser.add_argument("--allow-non-venv", action="store_true", help="Do not fail closed when not running under .venv.")
    parser.add_argument("--allow-missing-mt5-package", action="store_true", help="Do not fail closed when MetaTrader5 is not importable.")
    parser.add_argument("--require-pass", action="store_true", help="Verifier mode: require PASS records.")
    parser.add_argument("jsonl", nargs="?", help="Verifier mode JSONL path.")
    return parser


def main_build(argv: Sequence[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    record = build_readiness_aggregate(
        base_dir=Path(args.base_dir),
        max_age_minutes=args.max_age_minutes,
        require_venv=not args.allow_non_venv,
        require_mt5_package=not args.allow_missing_mt5_package,
    )
    output = Path(args.output)
    write_jsonl_record(output, record)
    print(f"Wrote {output}")
    print(f"Verdict: {record['verdict']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Operator state: {record['operator_state']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Exact ticket: {record['expected']['exact_ticket']}")
    print(f"Exact identifier: {record['expected']['exact_identifier']}")
    print(f"read_only_observer_workflow_authorized_for_operator_review: {record['read_only_observer_workflow_authorized_for_operator_review']}")
    print(f"effective_new_entries_blocked: {record['effective_new_entries_blocked']}")
    for field in AUTHORIZATION_FIELDS:
        label = field.replace("_", " ")
        print(f"{label}: {record[field]}")
    for field in CONSTRUCTION_FIELDS:
        print(f"{field}: {record[field]}")
    print(f"symbol_select_authorized: {record['symbol_select_authorized']}")
    print(f"vps_deployment_readiness_authorizes_trading: {record['vps_deployment_readiness_authorizes_trading']}")
    if record["violations"]:
        for violation in record["violations"]:
            print(f"VIOLATION: {violation}")
    return 0


def main_verify(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify H024 read-only VPS deployment readiness aggregate JSONL.")
    parser.add_argument("jsonl", help="JSONL report path.")
    parser.add_argument("--require-pass", action="store_true", help="Require all records to be PASS.")
    args = parser.parse_args(argv)

    try:
        records = load_jsonl_records(Path(args.jsonl))
    except ValueError as exc:
        print(f"H024 read-only VPS deployment readiness records: 0")
        print(f"Violations: 1")
        print("Verifier verdict: FAIL")
        print(f"VIOLATION: {exc}")
        return 1

    violations = validate_records(records, require_pass=args.require_pass)
    print(f"H024 read-only VPS deployment readiness records: {len(records)}")
    print(f"Violations: {len(violations)}")
    print(f"Verifier verdict: {'PASS' if not violations else 'FAIL'}")
    print(summarize_record(records[-1]))
    for violation in violations:
        print(f"VIOLATION: {violation}")
    return 0 if not violations else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main_build())