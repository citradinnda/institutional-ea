# H020 Hypothesis Seed

## Status

H020 is a new hypothesis seed.

No H020 code exists yet.

H020 is not validated.

H020 is not promotable.

H020 is not live-approved.

Phase 4 execution is not approved.

Live trading is not approved.

## Reason H020 Exists

H019 failed strict broker-native event validation because the strategy produced a trade whose USD gross notional exposure exceeded the H018 maximum per-trade leverage guard.

First H019 failure:

- symbol: `USDJPY`
- side: `buy`
- decision_time: `2021-07-05 21:00:00+00:00`
- entry_time: `2021-07-06 01:00:00+00:00`
- gross_leverage: `12.154432565`
- maximum allowed: `10.000000000`

The next hypothesis must address the sizing/leverage contract directly.

## H020 Core Question

Can a Donchian-entry plus stateful-Chandelier-exit strategy remain viable when position sizing is explicitly constrained by both:

1. target risk from stop distance, and
2. maximum USD gross notional leverage?

## H020 Proposed Identity

H020 should be a strategy-sizing hypothesis, not a guard patch.

Working name:

- H020: stateful Chandelier lifecycle with notional-aware sizing contract

Starting point:

- Keep H019 lifecycle semantics.
- Keep same-side Chandelier stops.
- Keep H018 guards.
- Add an explicit pre-trade sizing contract that prevents impossible gross leverage before event validation.

## Proposed H020 Sizing Principle

For each candidate trade, calculate both:

1. risk-based lots, derived from:
   - equity,
   - risk fraction,
   - stop distance,
   - contract size,
   - quote currency conversion,
   - lot step,
   - min lot;

2. max-notional lots, derived from:
   - equity,
   - maximum allowed gross leverage,
   - entry price,
   - contract size,
   - quote currency conversion,
   - lot step,
   - min lot.

Then the strategy-sized lot ceiling is:

- `allowed_lots = min(risk_based_lots, max_notional_lots)`

Open design question:

- If `allowed_lots` is below broker minimum lot, should the strategy emit zero exposure?
- If yes, this is not a silent skip; it becomes explicit strategy sizing semantics.
- If no, H020 will keep failing guards for small-equity or tight-stop cases.

## Important Distinction

H018 guard behavior must remain fail-closed.

H020 should not weaken guards.

Instead, H020 should define strategy outputs that are already compatible with the guards under normal conditions.

A guard failure after H020 would still mean the implementation or assumptions are wrong.

## H020 Design Choices To Lock Before Code

Before coding H020, decide these explicitly:

1. Per-trade notional cap:
   - use the existing H018 10x equity cap,
   - or choose a lower strategy cap below the hard guard?

2. Portfolio notional cap:
   - use the existing H018 10x portfolio gross cap,
   - or choose a lower strategy cap below the hard guard?

3. Lot clipping semantics:
   - Is reducing risk-based lots to the notional cap an approved strategy behavior?
   - This is not the same as the event engine silently clipping a violation.
   - It must be visible in strategy output or diagnostics.

4. Minimum-lot semantics:
   - If capped lots fall below min lot, should H020 emit flat?
   - This likely reduces trade frequency and may create missed signals.

5. Risk accounting:
   - Should H020 positions continue to be represented as signed risk fraction?
   - Or should the strategy/event bridge move toward explicit lot-intent objects?

6. Heat governor interaction:
   - Should heat be applied before notional cap?
   - after notional cap?
   - or both through a portfolio allocation step?

7. Diagnostic requirement:
   - Before strict validation, run an H020 guard scan across accepted windows.
   - The scan should count invalid stops, minimum stop distance failures, per-trade leverage failures, and portfolio leverage failures.

## Recommended H020 Development Path

Step 1:

- Build an H019/H020 diagnostic scan first.
- Confirm how many H019 guard violations remain across all accepted windows.
- Do not rely only on the first failure.

Step 2:

- Decide whether H020 should be:
  - risk-fraction output with notional-aware pre-scaling, or
  - explicit lot-intent output.

Step 3:

- Implement synthetic tests only.
- Prove no silent guard weakening.
- Prove capped sizing is visible and deterministic.

Step 4:

- Run focused tests.
- Run full pytest.
- Commit and push.

Step 5:

- Only after explicit authorization, run strict H020 broker-native validation.

## What H020 Must Not Do

H020 must not:

- weaken H018 guards,
- bypass guard checks,
- silently skip violating trades in the event engine,
- silently clip lots in the event engine,
- change cost model casually,
- change broker specs casually,
- change raw versus executable entry sizing silently,
- use HistData,
- use incomplete windows,
- impute M1 bars,
- approve live trading.

## Current Recommendation

Start H020 by creating an H019 guard diagnostic scanner first.

Reason:

H019 failed at the first per-trade leverage violation, but we need the full distribution before choosing H020 sizing semantics.

The diagnostic should answer:

- Are invalid directional stops now near zero?
- How many per-trade leverage violations remain?
- How many portfolio leverage violations remain?
- How many minimum stop-distance violations remain?
- Which symbols and sides dominate the failures?
- Are failures mostly tight-stop sizing, overlapping exposure, or both?

Only then should H020 sizing semantics be locked.
