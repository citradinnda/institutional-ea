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

## H019/H020 Guard Diagnostic Result

After the H019 strict broker-native validation failed at the first per-trade leverage violation, an H019/H020 guard diagnostic scanner was added:

- `scripts/scan_h019_guard_violations_real.py`
- `tests/test_h019_guard_scan_real_script.py`

Diagnostic command run:

- `python .\scripts\scan_h019_guard_violations_real.py`

This was diagnostic-only:

- not validation,
- not strategy promotion,
- not live-trading approval,
- not H020 implementation,
- not a guard weakening.

Strict bridge-window preflight passed exactly:

- `accepted_entry_count=5476`
- `first_accepted_timestamp=2021-07-02 13:00:00+00:00`
- `last_accepted_timestamp=2026-04-30 01:00:00+00:00`

H019/H020 guard diagnostic summary:

- `accepted_entry_count=5476`
- `executed_entry_count=5476`
- `skipped_entry_count=3176`
- `event_interval_count=8652`
- `trade_intent_count=5736`
- `candidate_count=5052`
- `skipped_intent_count=424`
- `violation_count=302`

Violation counts by guard:

- `maximum_per_trade_usd_gross_leverage`: `239`
- `maximum_portfolio_usd_gross_leverage`: `42`
- `minimum_stop_distance`: `19`
- `invalid_directional_stop`: `2`

Violation counts by symbol:

- `USDJPY`: `205`
- `XAUUSD`: `55`
- Portfolio-wide leverage violations are symbolless in the current scanner, so symbol totals do not include the `42` portfolio violations.

Violation counts by side:

- `buy`: `155`
- `sell`: `105`
- Portfolio-wide leverage violations are symbolless and sideless.

Enriched severity diagnostics:

Per-trade gross leverage violations:

- `count`: `239`
- `min`: `10.090896`
- `median`: `15.700000`
- `p95`: `79.820000`
- `max`: `429.700000`

Portfolio gross leverage violations:

- `count`: `42`
- `min`: `10.062785`
- `median`: `11.205005`
- `p95`: `15.568125`
- `max`: `16.938916`

Minimum stop-distance ratio violations, measured as raw stop distance divided by minimum modeled spread:

- `count`: `19`
- `min`: `0.114372`
- `median`: `0.571525`
- `p95`: `0.951577`
- `max`: `0.960424`

Comparison to prior H018 diagnostic:

- Prior H018 total guard violations: `2271`
- H019 total guard violations: `302`
- Prior H018 invalid directional stops: `1545`
- H019 invalid directional stops: `2`

Interpretation:

- H019 materially fixed the stale-held-signal versus stop-lifecycle mismatch.
- H019 did not become promotable.
- The dominant remaining blocker is notional/leverage sizing, especially per-trade USD gross leverage.
- H020 should focus on explicit notional-aware sizing rather than lifecycle repair.
- Per-trade leverage violations are severe, not cosmetic: median `15.70x`, p95 `79.82x`, max `429.70x`.
- H020 should also account for portfolio-wide gross exposure because `42` portfolio leverage violations remain.
- Portfolio leverage violations are milder than per-trade violations but still real: median `11.205x`, max `16.939x`.
- The `19` minimum stop-distance violations and `2` invalid directional-stop violations still require explicit handling or explanation before any strict H020 validation can be considered meaningful.
- A simple per-trade cap alone is insufficient because portfolio-wide overlap can still breach the hard guard.

## H020 Sizing Contract Decision

Decision locked after the H019/H020 guard diagnostic severity scan.

H020 will be a sizing-contract hypothesis, not a lifecycle-repair hypothesis.

H020 will keep:

- H019 Donchian entry/flip plus stateful same-side Chandelier lifecycle semantics,
- same-side Chandelier stops,
- H018 hard validation guards,
- strict broker-native complete-window validation requirements.

H020 will not weaken event-engine guards.

### H020 Pre-Trade Suppression Rules

Before sizing a candidate trade, H020 must check intended raw-entry stop geometry.

If the same-side stop is non-protective at intended raw entry:

- long/buy stop is not below raw entry, or
- short/sell stop is not above raw entry,

then H020 emits flat/no lot intent for that symbol at that decision.

If raw stop distance is below one modeled spread for the symbol, H020 emits flat/no lot intent.

This is approved strategy-level intent suppression.

It is not:

- event-engine silent skipping,
- event-engine lot clipping,
- validation pass-through,
- guard weakening.

The event engine must still fail closed if an invalid stop, sub-minimum stop distance, per-trade leverage violation, or portfolio leverage violation reaches validation.

### H020 Risk-Based Lots

For each valid candidate trade, H020 first computes risk-based lots from:

- equity,
- signed risk fraction,
- raw entry price,
- same-side stop distance,
- contract size,
- quote currency conversion,
- lot step,
- minimum lot.

The existing portfolio sizing conventions remain the starting reference.

### H020 Per-Trade Notional Cap

H020 then computes maximum per-trade lots from a strategy-level USD gross notional cap.

Decision:

- H020 strategy per-trade cap: below the H018 hard guard.
- Initial proposed cap for implementation: `9.0x` equity.
- H018 hard guard remains `10.0x` equity.

For each candidate:

- `candidate_lots = min(risk_based_lots, per_trade_notional_cap_lots)`

Lots must be rounded down to broker lot step.

If rounded lots fall below broker minimum lot, H020 emits flat/no lot intent for that symbol.

### H020 Portfolio Gross Notional Cap

H020 must also enforce a portfolio-wide strategy-level USD gross notional cap before event validation.

Decision:

- H020 strategy portfolio cap: below the H018 hard guard.
- Initial proposed cap for implementation: `9.0x` equity.
- H018 hard portfolio guard remains `10.0x` equity.

If combined candidate USD gross notional exceeds the H020 portfolio cap:

- scale all active candidate lots down proportionally,
- round down to broker lot step,
- recompute notionals after rounding,
- emit flat/no lot intent for any symbol whose rounded lots fall below minimum lot.

Long and short notionals are summed gross.

They are not netted.

### H020 Representation Decision

H020 should not pretend that signed risk fraction alone is enough to express the strategy contract.

Implementation should introduce explicit sizing diagnostics or explicit lot-intent objects.

At minimum, H020 outputs must make visible:

- raw risk-based lots,
- per-trade-cap lots,
- portfolio-scaled lots,
- final emitted lots,
- whether the symbol was suppressed,
- suppression reason if flat,
- raw stop distance,
- per-trade gross leverage estimate,
- portfolio gross leverage estimate.

The strict event bridge may need to be extended to consume explicit lots safely.

If the first implementation temporarily converts final lots back into a risk-fraction-shaped result for compatibility, that conversion must be tested and documented as a bridge shim, not as the H020 strategy truth.

### H020 Validation Expectations

Before any strict H020 broker-native validation attempt, run an H020 guard diagnostic scan across the accepted complete windows.

Expected diagnostic goal before validation:

- zero invalid directional-stop violations,
- zero minimum stop-distance violations,
- zero per-trade leverage violations,
- zero portfolio leverage violations.

Any nonzero hard-guard violation in H020 diagnostic means the H020 sizing contract or implementation is not ready for strict validation.
## H020 Design Choices To Lock Before Code

Before coding H020, decide these explicitly:

1. Per-trade notional cap:
   - Decision: use a strategy cap below the H018 hard guard.
   - Initial implementation target: `9.0x` equity.
   - H018 hard guard remains `10.0x`.

2. Portfolio notional cap:
   - Decision: use a strategy cap below the H018 hard guard.
   - Initial implementation target: `9.0x` total gross equity exposure.
   - H018 hard guard remains `10.0x`.

3. Lot clipping semantics:
   - Decision: reducing risk-based lots to the notional cap is approved H020 strategy behavior.
   - This must happen before validation.
   - It must be visible in H020 outputs or diagnostics.
   - It is not event-engine silent clipping.

4. Minimum-lot semantics:
   - Decision: if final capped/scaled lots fall below broker minimum lot, H020 emits flat/no lot intent for that symbol.

5. Risk accounting:
   - Decision: H020 should move toward explicit lot-intent or sizing-diagnostic outputs.
   - Signed risk fraction alone is insufficient as the strategy truth.

6. Heat governor interaction:
   - Decision: keep existing heat/risk-fraction logic as the starting risk budget, then apply per-trade and portfolio notional caps afterward.
   - The portfolio cap is the final gross-notional constraint before emitting lots.

7. Diagnostic requirement:
   - Decision: before strict validation, run an H020 guard scan across accepted windows.
   - Required target before validation: zero invalid stops, zero minimum stop-distance failures, zero per-trade leverage failures, and zero portfolio leverage failures.

## Recommended H020 Development Path

Step 1:

- Completed: build and run the H019/H020 diagnostic scan.
- Result: H019 has `302` guard violations across the accepted broker-native windows.
- Dominant blocker: `239` maximum per-trade USD gross leverage violations.
- Secondary blocker: `42` maximum portfolio USD gross leverage violations.

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

Do not write H020 sizing code yet.

Next, lock H020 sizing semantics from the diagnostic evidence:

- Per-trade notional-aware sizing is mandatory because `239` per-trade leverage violations remain, with p95 `79.82x` and max `429.70x`.
- Portfolio gross exposure must be considered because `42` portfolio leverage violations remain, with max `16.938916x`.
- Minimum stop-distance handling must be explicit because `19` violations remain, with median raw-distance/spread ratio `0.571525`.
- Directional stop geometry is almost fixed but not perfectly eliminated because `2` invalid directional-stop violations remain.

Recommended next engineering action:

- Inspect whether the remaining H019 violations are caused mainly by tight stops, overlapping exposure, minimum-lot constraints, or lifecycle edge cases.
- Then decide H020 sizing contract before code.
