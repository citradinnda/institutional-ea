from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = [
    "generated_at_server",
    "run_label",
    "event",
    "kill_switch_blocked",
    "symbol",
    "account_company",
    "account_server",
    "account_currency",
    "account_balance",
    "account_equity",
    "account_leverage",
    "account_trade_allowed",
    "account_trade_expert",
    "terminal_connected",
    "terminal_trade_allowed",
    "mql_trade_allowed",
    "bid",
    "ask",
    "spread_points",
    "volume_min",
    "volume_max",
    "volume_step",
    "stops_level",
    "freeze_level",
    "point",
    "digits",
    "detail",
]

ALLOWED_EVENTS = {"INIT", "TICK", "INTENT", "DEINIT"}
ALLOWED_INTENT_ACTIONS = {"NO_ACTION", "BLOCKED", "WOULD_OPEN"}
ALLOWED_SYMBOLS = {"USDJPYm", "XAUUSDm"}
EXPECTED_RUN_LABEL = "H024_LOG_ONLY_PREFLIGHT"


@dataclass(frozen=True)
class VerificationResult:
    rows: int
    violations: list[str]

    @property
    def passed(self) -> bool:
        return not self.violations


def _is_float(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def _is_int(value: str) -> bool:
    try:
        int(value)
    except ValueError:
        return False
    return True


def _intent_action(detail: str) -> str:
    return detail.split(":", 1)[0]


def verify_h024_ea_preflight_log(path: Path) -> VerificationResult:
    violations: list[str] = []

    if not path.exists():
        return VerificationResult(rows=0, violations=[f"missing log file: {path}"])

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []

        missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
        extra_columns = [column for column in fieldnames if column not in REQUIRED_COLUMNS]

        if missing_columns:
            violations.append(f"missing columns: {missing_columns}")
        if extra_columns:
            violations.append(f"unexpected columns: {extra_columns}")

        rows = list(reader)

    if not rows:
        violations.append("log has no data rows")
        return VerificationResult(rows=0, violations=violations)

    init_count = 0
    symbols_seen: set[str] = set()

    for index, row in enumerate(rows, start=2):
        event = row.get("event", "")
        symbol = row.get("symbol", "")

        if row.get("run_label") != EXPECTED_RUN_LABEL:
            violations.append(f"row {index}: unexpected run_label {row.get('run_label')!r}")

        if event not in ALLOWED_EVENTS:
            violations.append(f"row {index}: unexpected event {event!r}")

        if event == "INIT":
            init_count += 1

        if event == "INTENT":
            detail = row.get("detail", "")
            action = _intent_action(detail)
            if action not in ALLOWED_INTENT_ACTIONS:
                violations.append(f"row {index}: unexpected intent action {action!r}")
            if action != "NO_ACTION":
                violations.append(f"row {index}: EA runtime preflight may only emit NO_ACTION intent rows")

        if row.get("kill_switch_blocked") != "true":
            violations.append(f"row {index}: kill_switch_blocked must be true")

        if symbol not in ALLOWED_SYMBOLS:
            violations.append(f"row {index}: unexpected symbol {symbol!r}")
        else:
            symbols_seen.add(symbol)

        for bool_column in [
            "account_trade_allowed",
            "account_trade_expert",
            "terminal_connected",
            "terminal_trade_allowed",
            "mql_trade_allowed",
        ]:
            if row.get(bool_column) not in {"true", "false"}:
                violations.append(f"row {index}: {bool_column} must be true or false")

        for int_column in ["account_leverage", "spread_points", "stops_level", "freeze_level", "digits"]:
            if not _is_int(row.get(int_column, "")):
                violations.append(f"row {index}: {int_column} must be an integer")

        for float_column in ["account_balance", "account_equity", "volume_min", "volume_max", "volume_step", "point"]:
            if not _is_float(row.get(float_column, "")):
                violations.append(f"row {index}: {float_column} must be numeric")

        bid = row.get("bid", "")
        ask = row.get("ask", "")
        if bid and not _is_float(bid):
            violations.append(f"row {index}: bid must be blank or numeric")
        if ask and not _is_float(ask):
            violations.append(f"row {index}: ask must be blank or numeric")

    if init_count < 1:
        violations.append("log must include at least one INIT row")

    missing_symbols = sorted(ALLOWED_SYMBOLS - symbols_seen)
    if missing_symbols:
        violations.append(f"log missing required symbols: {missing_symbols}")

    return VerificationResult(rows=len(rows), violations=violations)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify H024 log-only EA runtime preflight CSV.")
    parser.add_argument("path", type=Path, help="Path to h024_ea_log_only_preflight.csv")
    args = parser.parse_args()

    result = verify_h024_ea_preflight_log(args.path)

    print("H024 log-only EA runtime preflight verification")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print()
    print(f"Rows: {result.rows}")
    print(f"Violations: {len(result.violations)}")

    for violation in result.violations:
        print(f"- {violation}")

    print()
    print(f"Verdict: {'PASS' if result.passed else 'FAIL'}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
