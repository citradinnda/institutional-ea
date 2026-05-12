from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from quantcore.execution.h024_one_shot_demo_canary_monitor import load_jsonl, write_jsonl

SCHEMA_VERSION = "h024_one_shot_demo_canary_lifecycle_decision.v1"
EXPECTED_MONITOR_SCHEMA_VERSION = "h024_one_shot_demo_canary_monitor.v1"
STRATEGY = "H024"
DECISION_CONTINUE_HOLD = "continue_hold"
ALLOWED_DECISIONS = [DECISION_CONTINUE_HOLD]

FORBIDDEN_ACTIONS = [
    "second_h024_entry_order",
    "live_order",
    "automatic_trading_loop",
    "scale_volume",
    "add_symbol",
    "close_position_without_separate_locked_governance",
    "modify_sl_tp_without_separate_locked_governance",
    "manual_ledger_tampering",
    "commit_reports",
]

REQUIRED_MONITOR_OBSERVED_COUNTS = {
    "exact_canary_position_count": 1,
    "unexpected_h024_pending_order_count": 0,
    "second_entry_deal_count": 0,
    "ledger_success_count": 1,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _observed_count(monitor_record: dict[str, Any], key: str) -> Any:
    observed = monitor_record.get("observed")
    if not isinstance(observed, dict):
        return None
    return observed.get(key)


def _latest_known(monitor_record: dict[str, Any]) -> dict[str, Any]:
    latest = monitor_record.get("latest_known")
    return latest if isinstance(latest, dict) else {}


def _expected_canary(monitor_record: dict[str, Any]) -> dict[str, Any]:
    expected = monitor_record.get("expected_canary")
    return expected if isinstance(expected, dict) else {}


def build_lifecycle_decision_record(
    *,
    generated_at_utc: str,
    monitor_record: dict[str, Any],
    decision: str = DECISION_CONTINUE_HOLD,
) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []

    if decision not in ALLOWED_DECISIONS:
        violations.append(
            {
                "code": "decision_not_allowed",
                "detail": {"observed": decision, "allowed": ALLOWED_DECISIONS},
            }
        )

    if monitor_record.get("schema_version") != EXPECTED_MONITOR_SCHEMA_VERSION:
        violations.append(
            {
                "code": "monitor_schema_version_mismatch",
                "detail": {
                    "observed": monitor_record.get("schema_version"),
                    "expected": EXPECTED_MONITOR_SCHEMA_VERSION,
                },
            }
        )

    if monitor_record.get("strategy") != STRATEGY:
        violations.append(
            {
                "code": "monitor_strategy_mismatch",
                "detail": {"observed": monitor_record.get("strategy"), "expected": STRATEGY},
            }
        )

    if monitor_record.get("verdict") != "PASS":
        violations.append(
            {
                "code": "monitor_verdict_not_pass",
                "detail": {"observed": monitor_record.get("verdict"), "expected": "PASS"},
            }
        )

    if monitor_record.get("lifecycle_state") != "open":
        violations.append(
            {
                "code": "monitor_lifecycle_state_not_open_for_hold",
                "detail": {"observed": monitor_record.get("lifecycle_state"), "expected": "open"},
            }
        )

    embedded_violations = monitor_record.get("violations")
    if embedded_violations:
        violations.append(
            {
                "code": "monitor_embedded_violations_present",
                "detail": embedded_violations,
            }
        )

    for key, expected_value in REQUIRED_MONITOR_OBSERVED_COUNTS.items():
        observed_value = _observed_count(monitor_record, key)
        if observed_value != expected_value:
            violations.append(
                {
                    "code": f"monitor_{key}_mismatch",
                    "detail": {"observed": observed_value, "expected": expected_value},
                }
            )

    latest_known = _latest_known(monitor_record)
    expected_canary = _expected_canary(monitor_record)

    record = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": generated_at_utc,
        "strategy": STRATEGY,
        "decision": decision,
        "verdict": "FAIL" if violations else "PASS",
        "violations": violations,
        "source_monitor": {
            "schema_version": monitor_record.get("schema_version"),
            "generated_at_utc": monitor_record.get("generated_at_utc"),
            "verdict": monitor_record.get("verdict"),
            "lifecycle_state": monitor_record.get("lifecycle_state"),
            "observed": monitor_record.get("observed"),
        },
        "expected_canary": {
            "server": expected_canary.get("server"),
            "currency": expected_canary.get("currency"),
            "symbol": expected_canary.get("symbol"),
            "side": expected_canary.get("side"),
            "magic": expected_canary.get("magic"),
            "volume": expected_canary.get("volume"),
            "position_ticket": expected_canary.get("position_ticket"),
            "entry_deal": expected_canary.get("entry_deal"),
            "price_open": expected_canary.get("price_open"),
            "sl": expected_canary.get("sl"),
        },
        "latest_known": {
            "price_current": latest_known.get("price_current"),
            "profit": latest_known.get("profit"),
            "swap": latest_known.get("swap"),
            "equity": latest_known.get("equity"),
            "margin": latest_known.get("margin"),
            "margin_free": latest_known.get("margin_free"),
            "margin_level": latest_known.get("margin_level"),
            "balance": latest_known.get("balance"),
        },
        "safety_contract": {
            "broker_mutation_authorized": False,
            "mt5_call_authorized": False,
            "close_authorized": False,
            "modify_authorized": False,
            "entry_authorized": False,
            "live_deployment_authorized": False,
            "allowed_action": "continue_read_only_observation",
            "forbidden_actions": FORBIDDEN_ACTIONS,
        },
        "rationale": [
            "The latest read-only monitor passed.",
            "Exactly one expected H024 canary position remains open.",
            "No unexpected H024 pending orders were observed.",
            "No second H024 entry deal was observed.",
            "The ledger contains exactly one successful canary record.",
            "This decision records hold/observe status only and authorizes no broker mutation.",
        ],
    }
    return record


def verify_lifecycle_decision_records(
    records: list[dict[str, Any]],
    *,
    require_pass: bool = False,
) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []

    if len(records) != 1:
        return [
            {
                "code": "lifecycle_decision_record_count_mismatch",
                "detail": {"observed": len(records), "expected": 1},
            }
        ]

    record = records[0]

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append(
            {
                "code": "schema_version_mismatch",
                "detail": {"observed": record.get("schema_version"), "expected": SCHEMA_VERSION},
            }
        )

    if record.get("strategy") != STRATEGY:
        violations.append(
            {
                "code": "strategy_mismatch",
                "detail": {"observed": record.get("strategy"), "expected": STRATEGY},
            }
        )

    if record.get("decision") != DECISION_CONTINUE_HOLD:
        violations.append(
            {
                "code": "decision_mismatch",
                "detail": {"observed": record.get("decision"), "expected": DECISION_CONTINUE_HOLD},
            }
        )

    safety_contract = record.get("safety_contract")
    if not isinstance(safety_contract, dict):
        violations.append({"code": "safety_contract_missing", "detail": safety_contract})
    else:
        false_required_fields = [
            "broker_mutation_authorized",
            "mt5_call_authorized",
            "close_authorized",
            "modify_authorized",
            "entry_authorized",
            "live_deployment_authorized",
        ]
        for field in false_required_fields:
            if safety_contract.get(field) is not False:
                violations.append(
                    {
                        "code": f"safety_contract_{field}_not_false",
                        "detail": {"observed": safety_contract.get(field), "expected": False},
                    }
                )

    embedded_violations = record.get("violations") or []
    if embedded_violations:
        violations.append(
            {
                "code": "lifecycle_decision_embedded_violations_present",
                "detail": embedded_violations,
            }
        )

    expected_verdict = "FAIL" if embedded_violations else "PASS"
    if record.get("verdict") != expected_verdict:
        violations.append(
            {
                "code": "lifecycle_decision_verdict_inconsistent",
                "detail": {"observed": record.get("verdict"), "expected": expected_verdict},
            }
        )

    if require_pass and record.get("verdict") != "PASS":
        violations.append(
            {
                "code": "lifecycle_decision_verdict_not_pass",
                "detail": {"observed": record.get("verdict"), "expected": "PASS"},
            }
        )

    return violations


def build_from_monitor_jsonl(
    *,
    monitor_path: str | Path,
    output_path: str | Path,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    monitor_records = load_jsonl(monitor_path)
    if len(monitor_records) != 1:
        record = {
            "schema_version": SCHEMA_VERSION,
            "generated_at_utc": generated_at_utc or utc_now_iso(),
            "strategy": STRATEGY,
            "decision": DECISION_CONTINUE_HOLD,
            "verdict": "FAIL",
            "violations": [
                {
                    "code": "monitor_record_count_mismatch",
                    "detail": {"observed": len(monitor_records), "expected": 1},
                }
            ],
            "source_monitor": None,
            "safety_contract": {
                "broker_mutation_authorized": False,
                "mt5_call_authorized": False,
                "close_authorized": False,
                "modify_authorized": False,
                "entry_authorized": False,
                "live_deployment_authorized": False,
                "allowed_action": "none_until_monitor_is_valid",
                "forbidden_actions": FORBIDDEN_ACTIONS,
            },
        }
    else:
        record = build_lifecycle_decision_record(
            generated_at_utc=generated_at_utc or utc_now_iso(),
            monitor_record=monitor_records[0],
            decision=DECISION_CONTINUE_HOLD,
        )

    write_jsonl(output_path, [record])
    return record