from __future__ import annotations

import argparse

from quantcore.execution.h024_one_shot_demo_canary_supervisory_state import (
    DEFAULT_LIFECYCLE_DECISION_PATH,
    DEFAULT_MONITOR_PATH,
    DEFAULT_OBSERVATION_ANALYSIS_PATH,
    DEFAULT_OUTPUT_PATH,
    build_supervisory_state,
    write_jsonl,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the H024 canary supervisory state JSONL packet.")
    parser.add_argument("--monitor", default=str(DEFAULT_MONITOR_PATH))
    parser.add_argument("--lifecycle-decision", default=str(DEFAULT_LIFECYCLE_DECISION_PATH))
    parser.add_argument("--observation-analysis", default=str(DEFAULT_OBSERVATION_ANALYSIS_PATH))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_PATH))
    parser.add_argument("--manual-review-loss-usd", type=float, default=40.0)
    parser.add_argument("--manual-review-adverse-price-move", type=float, default=45.0)
    args = parser.parse_args()

    record = build_supervisory_state(
        monitor_path=args.monitor,
        lifecycle_decision_path=args.lifecycle_decision,
        observation_analysis_path=args.observation_analysis,
        manual_review_loss_usd=args.manual_review_loss_usd,
        manual_review_adverse_price_move=args.manual_review_adverse_price_move,
    )
    write_jsonl(args.output, [record])

    mtm = record["latest_mark_to_market"]

    print(f"Wrote {args.output}")
    print(f"Supervisory verdict: {record['supervisory_verdict']}")
    print(f"Supervisory state: {record['supervisory_state']}")
    print(f"Operator next action: {record['operator_next_action']}")
    print(f"Violations: {len(record['violations'])}")
    print(f"Human review recommended: {record['human_review_recommended']}")
    print(f"Review triggers: {len(record['review_triggers'])}")
    print(f"Monitor lifecycle state: {record['state_inputs']['monitor_lifecycle_state']}")
    print(f"Lifecycle decision: {record['state_inputs']['lifecycle_decision']}")
    print(f"Current price: {mtm['current_price']}")
    print(f"Floating P/L: {mtm['floating_pl']}")
    print(f"Swap: {mtm['swap']}")
    print(f"Adverse move from fill: {mtm['adverse_price_move_from_fill']}")
    print(f"Adverse move fraction of stop: {mtm['adverse_move_fraction_of_stop']}")
    print(f"Broker mutation authorized: {record['broker_mutation_authorized']}")
    print(f"Trading loop authorized: {record['trading_loop_authorized']}")
    print(f"USDJPY separate readiness required: {record['automation_boundary']['usd_jpy_requires_separate_broker_readiness']}")

    return 0 if record["supervisory_verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
