from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_SCHEMA_VERSION = "h024_dry_run_execution_request_v1"
EXPECTED_REQUEST_KIND = "DRY_RUN_MARKET_OPEN"
EXPECTED_SOURCE_SCHEMA_VERSION = "h024_intended_action_log_v1"
ALLOWED_NORMALIZED_SYMBOLS = {"USDJPY", "XAUUSD"}
ALLOWED_TIMEFRAMES = {"H4"}
ALLOWED_SIDES = {"BUY", "SELL"}


@dataclass(frozen=True)
class VerificationResult:
    requests: int
    violations: list[str]

    @property
    def passed(self) -> bool:
        return not self.violations


def _load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    violations: list[str] = []
    rows: list[dict[str, Any]] = []

    if not path.exists():
        return [], [f"missing JSONL file: {path}"]

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            violations.append(f"line {line_number}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            violations.append(f"line {line_number}: JSONL value must be an object")
            continue
        rows.append(value)

    return rows, violations


def _is_positive_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _validate_request(index: int, row: dict[str, Any], violations: list[str]) -> None:
    expected_strings = {
        "schema_version": EXPECTED_SCHEMA_VERSION,
        "request_kind": EXPECTED_REQUEST_KIND,
        "source_schema_version": EXPECTED_SOURCE_SCHEMA_VERSION,
        "timeframe": "H4",
    }
    for field, expected in expected_strings.items():
        if row.get(field) != expected:
            violations.append(f"request {index}: {field} expected {expected!r}, got {row.get(field)!r}")

    symbol = row.get("symbol")
    normalized_symbol = row.get("normalized_symbol")
    side = row.get("side")

    if normalized_symbol not in ALLOWED_NORMALIZED_SYMBOLS:
        violations.append(f"request {index}: invalid normalized_symbol {normalized_symbol!r}")

    if symbol not in {"USDJPYm", "XAUUSDm", "USDJPYc", "XAUUSDc"}:
        violations.append(f"request {index}: invalid symbol {symbol!r}")

    if isinstance(symbol, str):
        if symbol.startswith("USDJPY") and normalized_symbol != "USDJPY":
            violations.append(f"request {index}: USDJPY broker symbol must normalize to USDJPY")
        if symbol.startswith("XAUUSD") and normalized_symbol != "XAUUSD":
            violations.append(f"request {index}: XAUUSD broker symbol must normalize to XAUUSD")

    if side not in ALLOWED_SIDES:
        violations.append(f"request {index}: invalid side {side!r}")

    for field in ("entry_price", "stop_loss", "risk_usd", "volume_lots"):
        if not _is_positive_number(row.get(field)):
            violations.append(f"request {index}: {field} must be a positive number")

    entry = row.get("entry_price")
    stop = row.get("stop_loss")
    if isinstance(entry, (int, float)) and isinstance(stop, (int, float)):
        if side == "BUY" and not stop < entry:
            violations.append(f"request {index}: BUY request stop_loss must be below entry_price")
        if side == "SELL" and not stop > entry:
            violations.append(f"request {index}: SELL request stop_loss must be above entry_price")

    reason = row.get("source_reason")
    if not isinstance(reason, str) or not reason:
        violations.append(f"request {index}: source_reason must be non-empty")
    else:
        for fragment in ("WOULD_OPEN:", "mode=log_only_no_execution"):
            if fragment not in reason:
                violations.append(f"request {index}: source_reason missing {fragment!r}")

    timestamp = row.get("timestamp")
    if not isinstance(timestamp, str) or not timestamp:
        violations.append(f"request {index}: timestamp must be non-empty")

    forbidden_key_fragments = ("order", "ticket", "position", "deal")
    forbidden_keys = [
        key
        for key in row
        if any(fragment in key.lower() for fragment in forbidden_key_fragments)
    ]
    if forbidden_keys:
        violations.append(f"request {index}: contains execution-like keys {forbidden_keys}")


def verify_h024_dry_run_request_jsonl(path: Path, *, require_request: bool = False) -> VerificationResult:
    rows, violations = _load_jsonl(path)

    if require_request and not rows:
        violations.append("JSONL must contain at least one dry-run request")

    for index, row in enumerate(rows, start=1):
        _validate_request(index, row, violations)

    return VerificationResult(requests=len(rows), violations=violations)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify H024 dry-run execution request JSONL.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--require-request", action="store_true")
    args = parser.parse_args()

    result = verify_h024_dry_run_request_jsonl(args.path, require_request=args.require_request)

    print("H024 dry-run execution request JSONL verification")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("JSONL read only. No MT5 access. No order execution.")
    print()
    print(f"JSONL: {args.path}")
    print(f"Requests: {result.requests}")
    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"- {violation}")
    print()
    print(f"Verdict: {'PASS' if result.passed else 'FAIL'}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
