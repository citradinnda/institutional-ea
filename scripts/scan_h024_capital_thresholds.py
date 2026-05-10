"""Find exact H024 capital thresholds for executable candidate shifts.

Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from scripts.scan_h024_executable_candidate_shifts import (
    ExecutableCandidateShift,
    scan_real_h4_exports,
)


@dataclass(frozen=True)
class CapitalThresholdResult:
    label: str
    balance_usd: int
    total_candidates: int
    usdjpy_candidates: int
    xauusd_candidates: int
    first_matching_candidate: ExecutableCandidateShift


def count_candidates(
    candidates: list[ExecutableCandidateShift],
    symbol: str | None,
) -> int:
    if symbol is None:
        return len(candidates)
    return sum(1 for candidate in candidates if candidate.symbol == symbol)


def expand_high_boundary_until_candidate(
    *,
    low_exclusive: int,
    high_inclusive: int,
    symbol: str | None,
    candidate_provider: Callable[[int], list[ExecutableCandidateShift]],
    max_high: int,
    high_growth_factor: int = 2,
) -> int:
    """Expand high_inclusive until it brackets at least one matching candidate.

    This keeps the exact threshold scanner usable across risk fractions instead
    of assuming the original 1 percent risk brackets.
    """

    if low_exclusive < 0:
        raise ValueError("low_exclusive must be non-negative")
    if high_inclusive <= low_exclusive:
        raise ValueError("high_inclusive must be greater than low_exclusive")
    if max_high < high_inclusive:
        raise ValueError("max_high must be greater than or equal to high_inclusive")
    if high_growth_factor < 2:
        raise ValueError("high_growth_factor must be at least 2")

    low_count = count_candidates(candidate_provider(low_exclusive), symbol)
    if low_count != 0:
        raise ValueError(
            f"low boundary must have zero candidates for {symbol or 'ANY'}; "
            f"observed {low_count}"
        )

    high = high_inclusive
    while True:
        high_count = count_candidates(candidate_provider(high), symbol)
        if high_count > 0:
            return high

        if high >= max_high:
            raise ValueError(
                f"could not find high boundary with at least one candidate for "
                f"{symbol or 'ANY'} up to max_high={max_high}; observed 0"
            )

        high = min(max_high, max(high + 1, high * high_growth_factor))


def find_first_balance_with_candidate(
    *,
    low_exclusive: int,
    high_inclusive: int,
    symbol: str | None,
    candidate_provider: Callable[[int], list[ExecutableCandidateShift]],
) -> int:
    if low_exclusive < 0:
        raise ValueError("low_exclusive must be non-negative")
    if high_inclusive <= low_exclusive:
        raise ValueError("high_inclusive must be greater than low_exclusive")

    low_count = count_candidates(candidate_provider(low_exclusive), symbol)
    high_count = count_candidates(candidate_provider(high_inclusive), symbol)

    if low_count != 0:
        raise ValueError(
            f"low boundary must have zero candidates for {symbol or 'ANY'}; "
            f"observed {low_count}"
        )
    if high_count <= 0:
        raise ValueError(
            f"high boundary must have at least one candidate for {symbol or 'ANY'}; "
            f"observed {high_count}"
        )

    low = low_exclusive
    high = high_inclusive

    while high - low > 1:
        mid = (low + high) // 2
        if count_candidates(candidate_provider(mid), symbol) > 0:
            high = mid
        else:
            low = mid

    return high


def summarize_threshold(
    *,
    label: str,
    symbol: str | None,
    low_exclusive: int,
    high_inclusive: int,
    candidate_provider: Callable[[int], list[ExecutableCandidateShift]],
    auto_expand_high: bool = False,
    max_high: int = 100_000,
    high_growth_factor: int = 2,
) -> CapitalThresholdResult:
    if auto_expand_high:
        high_inclusive = expand_high_boundary_until_candidate(
            low_exclusive=low_exclusive,
            high_inclusive=high_inclusive,
            symbol=symbol,
            candidate_provider=candidate_provider,
            max_high=max_high,
            high_growth_factor=high_growth_factor,
        )

    balance = find_first_balance_with_candidate(
        low_exclusive=low_exclusive,
        high_inclusive=high_inclusive,
        symbol=symbol,
        candidate_provider=candidate_provider,
    )
    candidates = candidate_provider(balance)
    counts = Counter(candidate.symbol for candidate in candidates)

    if symbol is None:
        first = candidates[0]
    else:
        first = next(candidate for candidate in candidates if candidate.symbol == symbol)

    return CapitalThresholdResult(
        label=label,
        balance_usd=balance,
        total_candidates=len(candidates),
        usdjpy_candidates=counts.get("USDJPY", 0),
        xauusd_candidates=counts.get("XAUUSD", 0),
        first_matching_candidate=first,
    )


def print_result(result: CapitalThresholdResult, risk_fraction: float) -> None:
    candidate = result.first_matching_candidate

    print(f"{result.label} threshold balance: {result.balance_usd} USD at {risk_fraction:.2%} risk")
    print(f"  total_candidates: {result.total_candidates}")
    print(f"  USDJPY: {result.usdjpy_candidates}")
    print(f"  XAUUSD: {result.xauusd_candidates}")
    print(
        "  first_matching_candidate: "
        f"{candidate.symbol} {candidate.side} "
        f"decision={candidate.decision_time.isoformat()} "
        f"entry={candidate.entry_time.isoformat()} "
        f"shift={candidate.ea_closed_shift_from_latest_common_h4} "
        f"final_risk={candidate.final_signed_risk_fraction:.12f} "
        f"entry_price={candidate.entry_price:.10f} "
        f"stop_price={candidate.stop_price:.10f} "
        f"stop_distance={candidate.stop_distance:.10f}"
    )
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--risk-fraction", type=float, default=0.01)
    parser.add_argument("--any-low", type=int, default=0)
    parser.add_argument("--any-high", type=int, default=250)
    parser.add_argument("--usdjpy-low", type=int, default=0)
    parser.add_argument("--usdjpy-high", type=int, default=250)
    parser.add_argument("--xauusd-low", type=int, default=0)
    parser.add_argument("--xauusd-high", type=int, default=1000)
    parser.add_argument("--max-high", type=int, default=100_000)
    parser.add_argument("--high-growth-factor", type=int, default=2)
    parser.add_argument(
        "--no-auto-expand-high",
        action="store_true",
        help="Disable automatic high-boundary expansion.",
    )
    args = parser.parse_args()

    if args.risk_fraction <= 0:
        raise ValueError("--risk-fraction must be positive")

    cache: dict[int, list[ExecutableCandidateShift]] = {}

    def provider(balance: int) -> list[ExecutableCandidateShift]:
        if balance <= 0:
            return []
        if balance not in cache:
            cache[balance] = scan_real_h4_exports(
                balance=float(balance),
                risk_fraction=float(args.risk_fraction),
            )
        return cache[balance]

    print("H024 exact capital threshold scan")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("Pure Python. Broker-native H4 CSV read only.")
    print("No MT5 access. No order execution.")
    print()

    auto_expand_high = not args.no_auto_expand_high

    results = [
        summarize_threshold(
            label="ANY",
            symbol=None,
            low_exclusive=args.any_low,
            high_inclusive=args.any_high,
            candidate_provider=provider,
            auto_expand_high=auto_expand_high,
            max_high=args.max_high,
            high_growth_factor=args.high_growth_factor,
        ),
        summarize_threshold(
            label="USDJPY",
            symbol="USDJPY",
            low_exclusive=args.usdjpy_low,
            high_inclusive=args.usdjpy_high,
            candidate_provider=provider,
            auto_expand_high=auto_expand_high,
            max_high=args.max_high,
            high_growth_factor=args.high_growth_factor,
        ),
        summarize_threshold(
            label="XAUUSD",
            symbol="XAUUSD",
            low_exclusive=args.xauusd_low,
            high_inclusive=args.xauusd_high,
            candidate_provider=provider,
            auto_expand_high=auto_expand_high,
            max_high=args.max_high,
            high_growth_factor=args.high_growth_factor,
        ),
    ]

    for result in results:
        print_result(result, risk_fraction=float(args.risk_fraction))

    print("Boundary checks:")
    for result, symbol in [
        (results[0], None),
        (results[1], "USDJPY"),
        (results[2], "XAUUSD"),
    ]:
        before = result.balance_usd - 1
        for balance in [before, result.balance_usd]:
            candidates = provider(balance)
            counts = Counter(candidate.symbol for candidate in candidates)
            matching = count_candidates(candidates, symbol)
            print(
                f"  {result.label} balance={balance}: "
                f"matching={matching} total={len(candidates)} "
                f"USDJPY={counts.get('USDJPY', 0)} "
                f"XAUUSD={counts.get('XAUUSD', 0)}"
            )

    print()
    print("Verdict: PASS")
    print("Thresholds quantified only; no higher-balance approval or execution approval implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
