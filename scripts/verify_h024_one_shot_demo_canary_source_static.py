from __future__ import annotations

from pathlib import Path


REQUIRED_SNIPPETS = (
    "ACKNOWLEDGEMENT_TEXT",
    "I_ACCEPT_EXACTLY_ONE_H024_STANDARD_DEMO_CANARY_ORDER",
    "allowed_demo_server != \"Exness-MT5Trial6\"",
    "symbol != \"XAUUSDm\"",
    "max_lot_cap_must_remain_0_01",
    "sl_distance_price_must_remain_89_027",
    "ensure_no_prior_canary",
    "terminal.account_info()",
    "terminal.symbol_info(config.symbol)",
    "terminal.positions_get(symbol=config.symbol)",
    "terminal.orders_get(symbol=config.symbol)",
    "terminal.order_check(request)",
    "terminal.order_send(request)",
)


def main() -> int:
    module_path = Path("quantcore/execution/h024_one_shot_demo_canary.py")
    runner_path = Path("scripts/run_h024_one_shot_demo_canary.py")
    module_source = module_path.read_text(encoding="utf-8-sig")
    runner_source = runner_path.read_text(encoding="utf-8-sig")
    combined = module_source + "\n" + runner_source

    violations = [snippet for snippet in REQUIRED_SNIPPETS if snippet not in combined]
    if "import MetaTrader5 as mt5" not in runner_source:
        violations.append("runner_missing_runtime_mt5_import")
    if "import MetaTrader5" in module_source:
        violations.append("library_module_must_not_import_mt5_directly")
    if "--send" not in runner_source:
        violations.append("runner_missing_explicit_send_flag")

    print("H024 one-shot demo canary source static verification")
    print("=" * 72)
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")
    verdict = "PASS" if not violations else "FAIL"
    print(f"Verdict: {verdict}")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())