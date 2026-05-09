from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"
EXPECTED_ACCOUNT_COMPANY = "Exness Technologies Ltd"
EXPECTED_ACCOUNT_CURRENCY = "USD"
EXPECTED_EA_NAME = "H024_LogOnly_Preflight"
EXPECTED_SCHEMA_VERSION = "h024_ea_log_only_preflight_v2"
EXPECTED_EA_VERSION = "0.4"
EXPECTED_RUNTIME_MODE = "log_only_preflight"
EXPECTED_SYMBOLS = {"USDJPYm", "XAUUSDm"}
EXPECTED_TIMEFRAME = "H4"


@dataclass(frozen=True)
class PlanValidationResult:
    violations: list[str]

    @property
    def passed(self) -> bool:
        return not self.violations


def _load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.exists():
        return None, [f"missing plan file: {path}"]

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: {exc}"]

    if not isinstance(payload, dict):
        return None, ["plan root must be a JSON object"]

    return payload, []


def _require_string(payload: dict[str, Any], key: str, violations: list[str]) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        violations.append(f"{key} must be a non-empty string")
        return ""
    return value


def _require_bool(payload: dict[str, Any], key: str, violations: list[str]) -> bool | None:
    value = payload.get(key)
    if not isinstance(value, bool):
        violations.append(f"{key} must be a boolean")
        return None
    return value


def validate_plan_payload(payload: dict[str, Any]) -> PlanValidationResult:
    violations: list[str] = []

    terminal_data_dir = _require_string(payload, "terminal_data_dir", violations)
    if terminal_data_dir:
        terminal_path = Path(terminal_data_dir)
        if not terminal_path.exists():
            violations.append(f"terminal_data_dir does not exist: {terminal_data_dir}")
        if not (terminal_path / "MQL5" / "Experts").exists():
            violations.append(f"terminal Experts dir does not exist: {terminal_path / 'MQL5' / 'Experts'}")
        if not (terminal_path / "MQL5" / "Files").exists():
            violations.append(f"terminal Files dir does not exist: {terminal_path / 'MQL5' / 'Files'}")

    if _require_string(payload, "account_server", violations) != EXPECTED_ACCOUNT_SERVER:
        violations.append("account_server does not match expected Exness demo server")

    if _require_string(payload, "account_company", violations) != EXPECTED_ACCOUNT_COMPANY:
        violations.append("account_company does not match expected broker company")

    if _require_string(payload, "account_currency", violations) != EXPECTED_ACCOUNT_CURRENCY:
        violations.append("account_currency must be USD")

    if _require_string(payload, "ea_name", violations) != EXPECTED_EA_NAME:
        violations.append("ea_name does not match expected log-only EA")

    if _require_string(payload, "schema_version", violations) != EXPECTED_SCHEMA_VERSION:
        violations.append("schema_version does not match expected runtime CSV schema")

    if _require_string(payload, "ea_version", violations) != EXPECTED_EA_VERSION:
        violations.append("ea_version does not match expected EA version")

    if _require_string(payload, "runtime_mode", violations) != EXPECTED_RUNTIME_MODE:
        violations.append("runtime_mode must remain log_only_preflight")

    kill_switch = _require_bool(payload, "kill_switch_blocked", violations)
    if kill_switch is not True:
        violations.append("kill_switch_blocked must be true")

    attach_detach = _require_bool(payload, "attach_detach_enabled", violations)
    if attach_detach is not False:
        violations.append("attach_detach_enabled must be false until explicitly approved")

    order_send = _require_bool(payload, "order_send_enabled", violations)
    if order_send is not False:
        violations.append("order_send_enabled must be false")

    gui_automation = _require_bool(payload, "gui_automation_enabled", violations)
    if gui_automation is not False:
        violations.append("gui_automation_enabled must be false")

    charts = payload.get("charts")
    if not isinstance(charts, list) or not charts:
        violations.append("charts must be a non-empty list")
    else:
        seen_symbols: set[str] = set()
        for index, chart in enumerate(charts, start=1):
            if not isinstance(chart, dict):
                violations.append(f"chart {index}: must be an object")
                continue

            symbol = chart.get("symbol")
            timeframe = chart.get("timeframe")
            ea_name = chart.get("ea_name")
            inputs = chart.get("inputs")

            if symbol not in EXPECTED_SYMBOLS:
                violations.append(f"chart {index}: unexpected symbol {symbol!r}")
            else:
                seen_symbols.add(symbol)

            if timeframe != EXPECTED_TIMEFRAME:
                violations.append(f"chart {index}: timeframe must be {EXPECTED_TIMEFRAME}")

            if ea_name != EXPECTED_EA_NAME:
                violations.append(f"chart {index}: ea_name does not match expected log-only EA")

            if not isinstance(inputs, dict):
                violations.append(f"chart {index}: inputs must be an object")
                continue

            if inputs.get("InpKillSwitchBlocked") is not True:
                violations.append(f"chart {index}: InpKillSwitchBlocked must be true")

            if inputs.get("InpSchemaVersion") != EXPECTED_SCHEMA_VERSION:
                violations.append(f"chart {index}: InpSchemaVersion mismatch")

            if inputs.get("InpEaVersion") != EXPECTED_EA_VERSION:
                violations.append(f"chart {index}: InpEaVersion mismatch")

            if inputs.get("InpRuntimeMode") != EXPECTED_RUNTIME_MODE:
                violations.append(f"chart {index}: InpRuntimeMode mismatch")

        missing_symbols = sorted(EXPECTED_SYMBOLS - seen_symbols)
        if missing_symbols:
            violations.append(f"charts missing required symbols: {missing_symbols}")

    return PlanValidationResult(violations=violations)


def validate_plan_file(path: Path) -> PlanValidationResult:
    payload, violations = _load_json(path)
    if payload is None:
        return PlanValidationResult(violations=violations)
    return validate_plan_payload(payload)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a proposed H024 MT5 profile/template automation plan. "
            "This is read-only and does not launch MT5, attach/detach EAs, place orders, "
            "modify orders, close orders, or call MT5 trade APIs."
        )
    )
    parser.add_argument("plan", type=Path, help="Path to inert JSON automation plan.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = validate_plan_file(args.plan)

    print("H024 MT5 profile/template automation plan validation")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("Read-only plan validation. No MT5 launch, GUI automation, attach/detach, or order-send.")
    print()
    print(f"Plan: {args.plan}")
    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"- {violation}")
    print()
    print("Verdict: PASS" if result.passed else "Verdict: FAIL")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
