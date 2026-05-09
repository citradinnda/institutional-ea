from __future__ import annotations

import argparse
import re
from pathlib import Path


DEFAULT_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")

FORBIDDEN_PATTERNS: tuple[tuple[str, str], ...] = (
    ("OrderSend", r"\bOrderSend\b"),
    ("OrderSendAsync", r"\bOrderSendAsync\b"),
    ("OrderCheck", r"\bOrderCheck\b"),
    ("CTrade", r"\bCTrade\b"),
    ("Trade include", r"#\s*include\s*[<\"].*Trade.*[>\"]"),
    ("PositionOpen", r"\bPositionOpen\b"),
    ("PositionClose", r"\bPositionClose\b"),
    ("PositionModify", r"\bPositionModify\b"),
    ("Buy helper", r"\bBuy\s*\("),
    ("Sell helper", r"\bSell\s*\("),
    ("BuyStop helper", r"\bBuyStop\s*\("),
    ("SellStop helper", r"\bSellStop\s*\("),
    ("BuyLimit helper", r"\bBuyLimit\s*\("),
    ("SellLimit helper", r"\bSellLimit\s*\("),
    ("OrderDelete", r"\bOrderDelete\b"),
    ("OrderModify", r"\bOrderModify\b"),
    ("TRADE_ACTION_DEAL", r"\bTRADE_ACTION_DEAL\b"),
    ("TRADE_ACTION_PENDING", r"\bTRADE_ACTION_PENDING\b"),
    ("TRADE_ACTION_SLTP", r"\bTRADE_ACTION_SLTP\b"),
    ("MqlTradeRequest", r"\bMqlTradeRequest\b"),
    ("MqlTradeResult", r"\bMqlTradeResult\b"),
)

REQUIRED_PATTERNS: tuple[tuple[str, str], ...] = (
    ("OnInit hook", r"\bint\s+OnInit\s*\("),
    ("OnTick hook", r"\bvoid\s+OnTick\s*\("),
    ("OnDeinit hook", r"\bvoid\s+OnDeinit\s*\("),
    ("kill switch default blocked", r"\bInpKillSwitchBlocked\s*=\s*true\b"),
    ("log file name", r"h024_ea_log_only_preflight\.csv"),
)


def _strip_comments(source: str) -> str:
    without_block = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    return re.sub(r"//.*", "", without_block)


def verify_source(path: Path) -> list[str]:
    violations: list[str] = []

    if not path.exists():
        return [f"missing source file: {path}"]

    raw = path.read_text(encoding="utf-8")
    searchable = _strip_comments(raw)

    for label, pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, searchable, flags=re.IGNORECASE):
            violations.append(f"forbidden execution surface present: {label}")

    for label, pattern in REQUIRED_PATTERNS:
        if not re.search(pattern, searchable, flags=re.IGNORECASE):
            violations.append(f"required log-only invariant missing: {label}")

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify H024 MQL5 log-only EA source has no execution surface."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=str(DEFAULT_SOURCE),
        help="Path to H024_LogOnly_Preflight.mq5",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    violations = verify_source(source_path)

    print("H024 MQL5 EA source static verification")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print()
    print(f"Source: {source_path}")
    print(f"Violations: {len(violations)}")

    for violation in violations:
        print(f"- {violation}")

    print()
    print("Verdict: PASS" if not violations else "Verdict: FAIL")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
