"""Verify the local H024 MT5 terminal/account preflight JSON report.

Research-only verifier.

This is not:
- demo approval,
- live approval,
- Phase 4 approval,
- EA execution approval.

Expected input:

    reports/h024_mt5_terminal_preflight.json

The JSON is produced by scripts/log_h024_mt5_terminal_preflight.py and must
remain local. Do not commit the JSON report.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

DEFAULT_INPUT_PATH = (
    Path(__file__).resolve().parents[1] / "reports" / "h024_mt5_terminal_preflight.json"
)

EXPECTED_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")
EXPECTED_BROKER_SYMBOLS: Mapping[str, str] = {
    "USDJPY": "USDJPYm",
    "XAUUSD": "XAUUSDm",
}
EXPECTED_POINT_BY_SYMBOL: Mapping[str, float] = {
    "USDJPY": 0.001,
    "XAUUSD": 0.001,
}
EXPECTED_DIGITS_BY_SYMBOL: Mapping[str, int] = {
    "USDJPY": 3,
    "XAUUSD": 3,
}
EXPECTED_VOLUME_STEP_BY_SYMBOL: Mapping[str, float] = {
    "USDJPY": 0.01,
    "XAUUSD": 0.01,
}
MAXIMUM_EXPECTED_VOLUME_MIN_BY_SYMBOL: Mapping[str, float] = {
    "USDJPY": 0.01,
    "XAUUSD": 0.01,
}
FORBIDDEN_CALLS: tuple[str, ...] = (
    "order_send",
    "order_check",
    "order_calc_margin",
    "order_calc_profit",
    "positions_get",
    "orders_get",
    "history_orders_get",
    "history_deals_get",
)


@dataclass(frozen=True)
class PreflightCheck:
    section: str
    field: str
    expected: str
    observed: str
    status: str


@dataclass(frozen=True)
class PreflightVerification:
    checks: tuple[PreflightCheck, ...]
    violation_count: int

    @property
    def passed(self) -> bool:
        return self.violation_count == 0


def load_preflight_report(path: Path) -> dict[str, Any]:
    """Load a terminal preflight JSON report."""

    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict):
        raise ValueError("terminal preflight JSON root must be an object")

    return payload


def verify_preflight_report(payload: Mapping[str, Any]) -> PreflightVerification:
    """Verify local terminal preflight report shape and safety fields."""

    checks: list[PreflightCheck] = []

    checks.extend(
        [
            _check_bool(payload, section="root", field="research_only", expected=True),
            _check_bool(payload, section="root", field="passed", expected=True),
            _check_bool(payload, section="root", field="mt5_initialized", expected=True),
            _check_text_contains(
                payload,
                section="root",
                field="approval_boundary",
                expected_text="No demo/live/Phase 4 approval.",
            ),
            _check_empty_list(payload, section="root", field="forbidden_call_attempts"),
            _check_forbidden_calls_checked(payload),
        ]
    )

    terminal = _mapping_field(payload, "terminal")
    account = _mapping_field(payload, "account")

    checks.extend(
        [
            _check_bool(terminal, section="terminal", field="connected", expected=True),
            _check_bool(terminal, section="terminal", field="tradeapi_disabled", expected=False),
            _check_text(account, section="account", field="currency", expected="USD"),
            _check_bool(account, section="account", field="trade_allowed", expected=True),
            _check_bool(account, section="account", field="trade_expert", expected=True),
        ]
    )

    checks.extend(_verify_symbols(payload))

    violation_count = sum(1 for check in checks if check.status != "ok")
    return PreflightVerification(checks=tuple(checks), violation_count=violation_count)


def format_preflight_verification(verification: PreflightVerification) -> str:
    """Format terminal preflight verification output."""

    lines = [
        "H024 MT5 terminal/account preflight verification",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        "section | field | expected | observed | status",
    ]

    for check in verification.checks:
        lines.append(
            " | ".join(
                [
                    check.section,
                    check.field,
                    check.expected,
                    check.observed,
                    check.status,
                ]
            )
        )

    lines.extend(
        [
            "",
            f"Violations: {verification.violation_count}",
            "",
            f"Verdict: {'PASS' if verification.passed else 'FAIL'}",
            "",
            "Safety boundary:",
            "- This verifier does not approve demo trading, live trading, or Phase 4.",
            "- This verifier only checks the local terminal preflight report shape and safety fields.",
        ]
    )

    return "\n".join(lines)


def _verify_symbols(payload: Mapping[str, Any]) -> tuple[PreflightCheck, ...]:
    symbols = payload.get("symbols")
    if not isinstance(symbols, list):
        return (
            PreflightCheck(
                section="symbols",
                field="symbols",
                expected="list",
                observed=type(symbols).__name__,
                status="violation",
            ),
        )

    by_symbol: dict[str, Mapping[str, Any]] = {}
    checks: list[PreflightCheck] = []

    for row in symbols:
        if not isinstance(row, Mapping):
            checks.append(
                PreflightCheck(
                    section="symbols",
                    field="row",
                    expected="object",
                    observed=type(row).__name__,
                    status="violation",
                )
            )
            continue

        model_symbol = str(row.get("model_symbol", ""))
        if model_symbol in by_symbol:
            checks.append(
                PreflightCheck(
                    section=model_symbol,
                    field="model_symbol",
                    expected="one row",
                    observed="duplicate",
                    status="violation",
                )
            )
            continue

        by_symbol[model_symbol] = row

    for symbol in EXPECTED_SYMBOLS:
        row = by_symbol.get(symbol)
        if row is None:
            checks.append(
                PreflightCheck(
                    section=symbol,
                    field="model_symbol",
                    expected="present",
                    observed="missing",
                    status="violation",
                )
            )
            continue

        checks.extend(_verify_symbol_row(symbol=symbol, row=row))

    return tuple(checks)


def _verify_symbol_row(*, symbol: str, row: Mapping[str, Any]) -> tuple[PreflightCheck, ...]:
    return (
        _check_text(row, section=symbol, field="broker_symbol", expected=EXPECTED_BROKER_SYMBOLS[symbol]),
        _check_text(row, section=symbol, field="status", expected="ok"),
        _check_bool(row, section=symbol, field="selected", expected=True),
        _check_bool(row, section=symbol, field="visible_after_select", expected=True),
        _check_positive_float(row, section=symbol, field="bid"),
        _check_positive_float(row, section=symbol, field="ask"),
        _check_non_negative_float(row, section=symbol, field="spread"),
        _check_text_set(row, section=symbol, field="trade_mode", allowed={"4", "FULL", "SYMBOL_TRADE_MODE_FULL"}),
        _check_non_empty(row, section=symbol, field="execution_mode"),
        _check_non_empty(row, section=symbol, field="order_filling_modes"),
        _check_non_empty(row, section=symbol, field="order_modes"),
        _check_float_at_most(
            row,
            section=symbol,
            field="volume_min",
            threshold=MAXIMUM_EXPECTED_VOLUME_MIN_BY_SYMBOL[symbol],
        ),
        _check_float_at_least(row, section=symbol, field="volume_max", threshold=0.01),
        _check_float_equal(
            row,
            section=symbol,
            field="volume_step",
            expected=EXPECTED_VOLUME_STEP_BY_SYMBOL[symbol],
        ),
        _check_float_equal(row, section=symbol, field="point", expected=EXPECTED_POINT_BY_SYMBOL[symbol]),
        _check_int_equal(row, section=symbol, field="digits", expected=EXPECTED_DIGITS_BY_SYMBOL[symbol]),
        _check_non_negative_float(row, section=symbol, field="stops_level_points"),
        _check_non_negative_float(row, section=symbol, field="freeze_level_points"),
    )


def _mapping_field(payload: Mapping[str, Any], field: str) -> Mapping[str, Any]:
    value = payload.get(field)
    if isinstance(value, Mapping):
        return value
    return {}


def _check_forbidden_calls_checked(payload: Mapping[str, Any]) -> PreflightCheck:
    value = payload.get("forbidden_calls_checked")
    if not isinstance(value, list):
        return PreflightCheck(
            section="root",
            field="forbidden_calls_checked",
            expected=str(list(FORBIDDEN_CALLS)),
            observed=type(value).__name__,
            status="violation",
        )

    missing = [name for name in FORBIDDEN_CALLS if name not in value]
    return PreflightCheck(
        section="root",
        field="forbidden_calls_checked",
        expected="all forbidden MT5 call names present",
        observed=f"missing={missing}",
        status="ok" if not missing else "violation",
    )


def _check_bool(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    expected: bool,
) -> PreflightCheck:
    value = payload.get(field)
    return PreflightCheck(
        section=section,
        field=field,
        expected=str(expected),
        observed=str(value),
        status="ok" if value is expected else "violation",
    )


def _check_empty_list(payload: Mapping[str, Any], *, section: str, field: str) -> PreflightCheck:
    value = payload.get(field)
    return PreflightCheck(
        section=section,
        field=field,
        expected="[]",
        observed=str(value),
        status="ok" if value == [] else "violation",
    )


def _check_text(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    expected: str,
) -> PreflightCheck:
    value = str(payload.get(field, ""))
    return PreflightCheck(
        section=section,
        field=field,
        expected=expected,
        observed=value,
        status="ok" if value == expected else "violation",
    )


def _check_text_contains(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    expected_text: str,
) -> PreflightCheck:
    value = str(payload.get(field, ""))
    return PreflightCheck(
        section=section,
        field=field,
        expected=f"contains {expected_text}",
        observed=value,
        status="ok" if expected_text in value else "violation",
    )


def _check_text_set(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    allowed: set[str],
) -> PreflightCheck:
    value = str(payload.get(field, "")).strip().upper()
    return PreflightCheck(
        section=section,
        field=field,
        expected=str(sorted(allowed)),
        observed=str(payload.get(field, "")),
        status="ok" if value in allowed else "violation",
    )


def _check_non_empty(payload: Mapping[str, Any], *, section: str, field: str) -> PreflightCheck:
    value = str(payload.get(field, "")).strip()
    return PreflightCheck(
        section=section,
        field=field,
        expected="non-empty",
        observed=value,
        status="ok" if value else "violation",
    )


def _check_positive_float(payload: Mapping[str, Any], *, section: str, field: str) -> PreflightCheck:
    value = _float_value(payload, field)
    return PreflightCheck(
        section=section,
        field=field,
        expected="> 0",
        observed=str(payload.get(field)),
        status="ok" if value is not None and value > 0.0 else "violation",
    )


def _check_non_negative_float(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
) -> PreflightCheck:
    value = _float_value(payload, field)
    return PreflightCheck(
        section=section,
        field=field,
        expected=">= 0",
        observed=str(payload.get(field)),
        status="ok" if value is not None and value >= 0.0 else "violation",
    )


def _check_float_equal(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    expected: float,
) -> PreflightCheck:
    value = _float_value(payload, field)
    return PreflightCheck(
        section=section,
        field=field,
        expected=f"{expected:.10g}",
        observed=str(payload.get(field)),
        status=(
            "ok"
            if value is not None and abs(value - expected) <= 1e-12
            else "violation"
        ),
    )


def _check_float_at_most(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    threshold: float,
) -> PreflightCheck:
    value = _float_value(payload, field)
    return PreflightCheck(
        section=section,
        field=field,
        expected=f"<= {threshold:.10g}",
        observed=str(payload.get(field)),
        status="ok" if value is not None and value <= threshold else "violation",
    )


def _check_float_at_least(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    threshold: float,
) -> PreflightCheck:
    value = _float_value(payload, field)
    return PreflightCheck(
        section=section,
        field=field,
        expected=f">= {threshold:.10g}",
        observed=str(payload.get(field)),
        status="ok" if value is not None and value >= threshold else "violation",
    )


def _check_int_equal(
    payload: Mapping[str, Any],
    *,
    section: str,
    field: str,
    expected: int,
) -> PreflightCheck:
    value = _int_value(payload, field)
    return PreflightCheck(
        section=section,
        field=field,
        expected=str(expected),
        observed=str(payload.get(field)),
        status="ok" if value == expected else "violation",
    )


def _float_value(payload: Mapping[str, Any], field: str) -> float | None:
    try:
        return float(payload[field])
    except (KeyError, TypeError, ValueError):
        return None


def _int_value(payload: Mapping[str, Any], field: str) -> int | None:
    try:
        return int(payload[field])
    except (KeyError, TypeError, ValueError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Path to local MT5 terminal preflight JSON report.",
    )
    args = parser.parse_args()

    payload = load_preflight_report(args.input)
    verification = verify_preflight_report(payload)
    print(format_preflight_verification(verification))

    if not verification.passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
