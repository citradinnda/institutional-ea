from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = [
    "generated_at_server",
    "schema_version",
    "ea_version",
    "source_version",
    "timer_seconds",
    "runtime_mode",
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

ALLOWED_EVENTS = {
    "INIT",
    "TICK",
    "INTENT",
    "MARKET_STATE",
    "BAR_OBSERVATION",
    "H024_STATE_OBSERVATION",
    "H024_INTENDED_ACTION_HEADER",
    "H024_INTENDED_ACTION_ROW",
    "DEINIT",
}

INTENDED_ACTION_EVENTS = {"H024_INTENDED_ACTION_HEADER", "H024_INTENDED_ACTION_ROW"}

INTENDED_ACTION_LOG_HEADER_FIELDS = [
    "timestamp",
    "schema_version",
    "ea_version",
    "symbol",
    "normalized_symbol",
    "timeframe",
    "decision",
    "direction",
    "entry_price",
    "stop_price",
    "stop_distance_price",
    "tick_size",
    "tick_value_usd_per_lot",
    "account_balance_usd",
    "risk_fraction",
    "risk_usd",
    "raw_lots",
    "lots",
    "min_volume",
    "max_volume",
    "volume_step",
    "volume_digits",
    "reason",
]

INTENDED_ACTION_LOG_ROW_FIELDS = INTENDED_ACTION_LOG_HEADER_FIELDS[1:]


def _extra_csv_fields(row: dict) -> list[str]:
    extra = row.get(None)
    if extra is None:
        return []
    return [str(value) for value in extra]


def _append_numeric_violation(
    violations: list[str],
    index: int,
    fields: dict[str, str],
    field_name: str,
) -> None:
    try:
        float(fields[field_name])
    except (KeyError, TypeError, ValueError):
        violations.append(f"row {index}: invalid intended-action numeric field {field_name!r}")


def _validate_intended_action_payload(index: int, event: str, row: dict, violations: list[str]) -> None:
    payload = _extra_csv_fields(row)

    if event == "H024_INTENDED_ACTION_HEADER":
        if row.get("detail") != "timestamp":
            violations.append(f"row {index}: intended-action header detail must be 'timestamp'")
        if payload != INTENDED_ACTION_LOG_ROW_FIELDS:
            violations.append(f"row {index}: intended-action header fields do not match frozen contract")
        return

    if event != "H024_INTENDED_ACTION_ROW":
        return

    if len(payload) != len(INTENDED_ACTION_LOG_ROW_FIELDS):
        violations.append(
            f"row {index}: intended-action row has {len(payload)} payload fields, "
            f"expected {len(INTENDED_ACTION_LOG_ROW_FIELDS)}"
        )
        return

    fields = dict(zip(INTENDED_ACTION_LOG_ROW_FIELDS, payload))

    if fields.get("schema_version") != "h024_intended_action_log_v1":
        violations.append(f"row {index}: invalid intended-action schema_version {fields.get('schema_version')!r}")

    if fields.get("timeframe") != "H4":
        violations.append(f"row {index}: invalid intended-action timeframe {fields.get('timeframe')!r}")

    if fields.get("symbol") != row.get("symbol"):
        violations.append(f"row {index}: intended-action symbol does not match preflight symbol")

    if fields.get("normalized_symbol") not in {"USDJPY", "XAUUSD"}:
        violations.append(
            f"row {index}: invalid intended-action normalized_symbol {fields.get('normalized_symbol')!r}"
        )

    decision = fields.get("decision")
    direction = fields.get("direction")

    if decision not in {"WOULD_OPEN", "BLOCKED", "NO_ACTION"}:
        violations.append(f"row {index}: invalid intended-action decision {decision!r}")

    if decision == "WOULD_OPEN" and direction not in {"long", "short"}:
        violations.append(f"row {index}: WOULD_OPEN intended-action row must have long/short direction")

    if decision in {"BLOCKED", "NO_ACTION"} and direction not in {"", "long", "short"}:
        violations.append(f"row {index}: invalid intended-action direction {direction!r}")

    for field_name in [
        "entry_price",
        "stop_price",
        "stop_distance_price",
        "tick_size",
        "tick_value_usd_per_lot",
        "account_balance_usd",
        "risk_fraction",
        "risk_usd",
        "raw_lots",
        "lots",
        "min_volume",
        "max_volume",
        "volume_step",
    ]:
        _append_numeric_violation(violations, index, fields, field_name)

    try:
        int(fields["volume_digits"])
    except (KeyError, TypeError, ValueError):
        violations.append(f"row {index}: invalid intended-action volume_digits")

    if not fields.get("reason"):
        violations.append(f"row {index}: intended-action reason must be non-empty")

ALLOWED_INTENT_ACTIONS = {"NO_ACTION", "BLOCKED", "WOULD_OPEN"}
ALLOWED_SYMBOLS = {"USDJPYm", "XAUUSDm"}
EXPECTED_RUN_LABEL = "H024_LOG_ONLY_PREFLIGHT"
EXPECTED_SCHEMA_VERSION = "h024_ea_log_only_preflight_v2"
EXPECTED_EA_VERSION = "0.6"
EXPECTED_RUNTIME_MODE = "log_only_preflight"


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

        if row.get("schema_version") != EXPECTED_SCHEMA_VERSION:
            violations.append(f"row {index}: unexpected schema_version {row.get('schema_version')!r}")

        if row.get("ea_version") != EXPECTED_EA_VERSION:
            violations.append(f"row {index}: unexpected ea_version {row.get('ea_version')!r}")

        if not row.get("source_version"):
            violations.append(f"row {index}: source_version must be populated")

        if row.get("runtime_mode") != EXPECTED_RUNTIME_MODE:
            violations.append(f"row {index}: unexpected runtime_mode {row.get('runtime_mode')!r}")

        if not _is_int(row.get("timer_seconds", "")):
            violations.append(f"row {index}: timer_seconds must be an integer")

        if row.get("run_label") != EXPECTED_RUN_LABEL:
            violations.append(f"row {index}: unexpected run_label {row.get('run_label')!r}")

        if event not in ALLOWED_EVENTS:
            violations.append(f"row {index}: unexpected event {event!r}")

        if event in INTENDED_ACTION_EVENTS:
            _validate_intended_action_payload(index, event, row, violations)
            continue

        if event == "INIT":
            init_count += 1

        if event == "INTENT":
            detail = row.get("detail", "")
            action = _intent_action(detail)
            if action not in ALLOWED_INTENT_ACTIONS:
                violations.append(f"row {index}: unexpected intent action {action!r}")
            if action == "WOULD_OPEN":
                if row.get("kill_switch_blocked") != "true":
                    violations.append(f"row {index}: WOULD_OPEN intent rows require kill_switch_blocked=true")
                if "mode=log_only_no_execution" not in detail:
                    violations.append(f"row {index}: WOULD_OPEN intent rows must be log-only no-execution observations")
                if "side=long" not in detail and "side=short" not in detail:
                    violations.append(f"row {index}: WOULD_OPEN intent rows must include side=long or side=short")
            elif action != "NO_ACTION":
                violations.append(f"row {index}: EA runtime preflight may only emit NO_ACTION or constrained WOULD_OPEN intent rows")

        if event == "MARKET_STATE":
            detail = row.get("detail", "")
            if "H4:" not in detail or "M1:" not in detail:
                violations.append(f"row {index}: MARKET_STATE detail must include H4 and M1 observations")

        if event == "BAR_OBSERVATION":
            detail = row.get("detail", "")
            if "H4_closed:" not in detail or "M1_closed:" not in detail:
                violations.append(f"row {index}: BAR_OBSERVATION detail must include closed H4 and M1 observations")

        if event == "H024_STATE_OBSERVATION":
            detail = row.get("detail", "")
            required_fragments = [
                "closed_h4_time=",
                "slow_window=5",
                "slope_lag=2",
                "atr_window=3",
                "pullback_window=3",
                "trend_up=",
                "trend_down=",
                "long_signal_observed=",
                "short_signal_observed=",
                "action=NO_ACTION:state_observation_only",
            ]
            if not (
                detail.startswith("unavailable:")
                or all(fragment in detail for fragment in required_fragments)
            ):
                violations.append(
                    f"row {index}: H024_STATE_OBSERVATION detail must include frozen H024 state fields"
                )

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
