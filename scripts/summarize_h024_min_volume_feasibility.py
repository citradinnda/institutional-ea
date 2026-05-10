"""Summarize H024 minimum-volume feasibility.

Research only. No demo/live/Phase 4 approval.
Pure Python. No MT5 access. No order execution.

This tool quantifies whether an observed H024 signal can reach broker minimum
volume under a given balance and risk fraction. It does NOT recommend raising
risk; it only reports the feasibility math.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class FeasibilityResult:
    symbol: str
    action: str
    balance: float
    risk_fraction: float
    risk_usd: float
    raw_lots: float
    min_volume: float
    loss_per_1_lot_usd: float
    minimum_risk_usd_for_min_volume: float
    minimum_balance_at_same_risk_fraction: float
    minimum_risk_fraction_at_same_balance: float
    feasible_at_current_settings: bool
    observation_count: int = 1


def _positive_float(value: object, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric, got {value!r}") from exc
    if not math.isfinite(result) or result <= 0:
        raise ValueError(f"{name} must be finite and positive, got {value!r}")
    return result


def compute_feasibility(
    *,
    symbol: str,
    action: str = "UNKNOWN",
    balance: float,
    risk_fraction: float,
    raw_lots: float,
    min_volume: float,
) -> FeasibilityResult:
    balance = _positive_float(balance, "balance")
    risk_fraction = _positive_float(risk_fraction, "risk_fraction")
    raw_lots = _positive_float(raw_lots, "raw_lots")
    min_volume = _positive_float(min_volume, "min_volume")

    risk_usd = balance * risk_fraction
    loss_per_1_lot_usd = risk_usd / raw_lots
    minimum_risk_usd = loss_per_1_lot_usd * min_volume
    minimum_balance = minimum_risk_usd / risk_fraction
    minimum_risk_fraction = minimum_risk_usd / balance

    return FeasibilityResult(
        symbol=symbol,
        action=action,
        balance=balance,
        risk_fraction=risk_fraction,
        risk_usd=risk_usd,
        raw_lots=raw_lots,
        min_volume=min_volume,
        loss_per_1_lot_usd=loss_per_1_lot_usd,
        minimum_risk_usd_for_min_volume=minimum_risk_usd,
        minimum_balance_at_same_risk_fraction=minimum_balance,
        minimum_risk_fraction_at_same_balance=minimum_risk_fraction,
        feasible_at_current_settings=raw_lots >= min_volume,
    )


ALIASES = {
    "symbol": ("symbol", "broker_symbol", "mt5_symbol"),
    "normalized_symbol": ("normalized_symbol", "model_symbol"),
    "action": ("action", "intended_action", "decision"),
    "raw_lots": ("raw_lots", "raw_volume", "raw_volume_lots", "computed_raw_lots"),
    "min_volume": ("min_volume", "volume_min", "broker_min_volume"),
}


def _get(row: dict[str, str], logical_name: str) -> str | None:
    for key in ALIASES[logical_name]:
        if key in row and row[key] not in ("", None):
            return row[key]
    return None


def parse_runtime_csv(path: Path) -> list[dict[str, str]]:
    """Parse mixed-schema H024 runtime CSV and return intended-action rows.

    The runtime CSV can contain short preflight rows and longer intended-action
    rows, so this intentionally avoids pandas and tracks repeated header rows.
    """

    rows: list[dict[str, str]] = []
    current_header: list[str] | None = None

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        for physical_row in reader:
            if not physical_row:
                continue

            lowered = [cell.strip().lower() for cell in physical_row]
            has_action = any(name in lowered for name in ALIASES["action"])
            has_raw_lots = any(name in lowered for name in ALIASES["raw_lots"])
            has_min_volume = any(name in lowered for name in ALIASES["min_volume"])

            if has_action and has_raw_lots and has_min_volume:
                current_header = lowered
                continue

            if current_header is None:
                continue

            if len(physical_row) != len(current_header):
                continue

            mapped = {
                key: value.strip()
                for key, value in zip(current_header, physical_row, strict=True)
            }

            raw_lots = _get(mapped, "raw_lots")
            min_volume = _get(mapped, "min_volume")
            action = _get(mapped, "action")

            if raw_lots and min_volume and action:
                try:
                    if float(raw_lots) > 0 and float(min_volume) > 0:
                        rows.append(mapped)
                except ValueError:
                    continue

    return rows


def compute_from_runtime_csv(
    *,
    path: Path,
    balance: float,
    risk_fraction: float,
) -> list[FeasibilityResult]:
    by_key: dict[tuple[str, str, float, float], FeasibilityResult] = {}

    for row in parse_runtime_csv(path):
        symbol = (
            _get(row, "normalized_symbol")
            or _get(row, "symbol")
            or "UNKNOWN"
        )
        action = _get(row, "action") or "UNKNOWN"
        raw_lots = _get(row, "raw_lots")
        min_volume = _get(row, "min_volume")

        if raw_lots is None or min_volume is None:
            continue

        result = compute_feasibility(
            symbol=symbol,
            action=action,
            balance=balance,
            risk_fraction=risk_fraction,
            raw_lots=float(raw_lots),
            min_volume=float(min_volume),
        )
        key = (
            result.symbol,
            result.action,
            round(result.raw_lots, 10),
            round(result.min_volume, 10),
        )

        if key in by_key:
            by_key[key] = replace(
                by_key[key],
                observation_count=by_key[key].observation_count + 1,
            )
        else:
            by_key[key] = result

    return list(by_key.values())

def print_results(results: Iterable[FeasibilityResult]) -> int:
    materialized = list(results)

    print("H024 minimum-volume feasibility summary")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("Pure Python. No MT5 access. No order execution.")
    print()

    if not materialized:
        print("No positive raw-lot rows found.")
        print()
        print("Verdict: FAIL")
        return 1

    for result in materialized:
        verdict = "FEASIBLE" if result.feasible_at_current_settings else "BELOW_MIN_VOLUME"
        print(
            f"{result.symbol} | {result.action} | {verdict} | "
            f"observations={result.observation_count} "
            f"raw_lots={result.raw_lots:.10f} min_volume={result.min_volume:.10f}"
        )
        print(f"  balance: {result.balance:.2f}")
        print(f"  risk_fraction: {result.risk_fraction:.6f}")
        print(f"  current_risk_usd: {result.risk_usd:.6f}")
        print(f"  implied_loss_per_1_lot_usd: {result.loss_per_1_lot_usd:.6f}")
        print(
            "  minimum_risk_usd_for_min_volume: "
            f"{result.minimum_risk_usd_for_min_volume:.6f}"
        )
        print(
            "  minimum_balance_at_same_risk_fraction: "
            f"{result.minimum_balance_at_same_risk_fraction:.2f}"
        )
        print(
            "  minimum_risk_fraction_at_same_balance: "
            f"{result.minimum_risk_fraction_at_same_balance:.6f}"
        )
        print()

    print("Verdict: PASS")
    print("Feasibility quantified only; no risk increase or execution approval implied.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--symbol")
    parser.add_argument("--action", default="MANUAL")
    parser.add_argument("--balance", type=float, required=True)
    parser.add_argument("--risk-fraction", type=float, required=True)
    parser.add_argument("--raw-lots", type=float)
    parser.add_argument("--min-volume", type=float)

    args = parser.parse_args()

    if args.csv:
        results = compute_from_runtime_csv(
            path=args.csv,
            balance=args.balance,
            risk_fraction=args.risk_fraction,
        )
    else:
        if args.symbol is None or args.raw_lots is None or args.min_volume is None:
            parser.error("manual mode requires --symbol, --raw-lots, and --min-volume")

        results = [
            compute_feasibility(
                symbol=args.symbol,
                action=args.action,
                balance=args.balance,
                risk_fraction=args.risk_fraction,
                raw_lots=args.raw_lots,
                min_volume=args.min_volume,
            )
        ]

    return print_results(results)


if __name__ == "__main__":
    raise SystemExit(main())
