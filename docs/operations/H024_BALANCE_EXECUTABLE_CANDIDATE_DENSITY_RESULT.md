# H024 Balance Executable Candidate Density Result

Research only. No demo/live/Phase 4 approval.

## Summary

This document preserves the balance-density scan performed after HANDOFF_83.

The scan tested H024 executable historical candidate counts at fixed 1% risk across selected balances.

No MT5 access was used.
No order execution was used.
No demo/live approval is implied.

## Result Table

| Balance | Risk Fraction | Executable Candidate Rows | Interpretation |
|---:|---:|---:|---|
| 100 USD | 1.00% | 0 | Current intended setting remains mechanically non-executable. |
| 120 USD | 1.00% | 0 | Still mechanically non-executable. |
| 123 USD | 1.00% | 0 | 123 USD is only relevant as the 2% ANY/USDJPY threshold, not as a 1% threshold. |
| 164 USD | 1.00% | 0 | Still mechanically non-executable at 1%. |
| 245 USD | 1.00% | 1 | First ANY/USDJPY executable historical candidate. This is only a threshold blip, not meaningful density. |
| 327 USD | 1.00% | 16 | Thin USDJPY executable feasibility. |
| 490 USD | 1.00% | 174 | Meaningful USDJPY executable candidate density begins. |
| 550 USD | 1.00% | 215 | Stronger USDJPY executable candidate density. |
| 935 USD | 1.00% | 569 | XAUUSD threshold begins; dual-symbol feasibility starts. |
| 1000 USD | 1.00% | 595 | Dual-symbol feasibility becomes more realistic, but still research-only. |

## First Candidate Observations

At 245 USD / 1% risk, the first executable candidate was:

- Symbol: USDJPY
- Side: sell
- Decision time: 2021-07-17 21:00:00+00:00
- Entry time: 2021-07-18 17:00:00+00:00
- EA closed shift: 7697
- Final signed risk fraction: -0.009982289447
- Entry price: 110.0150000000
- Stop price: 110.2840593855

At 327 USD / 1% risk, executable rows increased to 16.

At 490 USD / 1% risk, executable rows increased to 174.

At 550 USD / 1% risk, executable rows increased to 215.

At 935 USD / 1% risk, executable rows increased to 569 and XAUUSD feasibility begins according to the prior exact threshold result.

At 1000 USD / 1% risk, executable rows increased to 595.

## Interpretation

The current intended account setting remains blocked:

- Balance: 100 USD
- Risk fraction: 1%
- Executable candidate rows: 0

The first 1% executable threshold at 245 USD is not a practical deployment point because it produces only one historical executable row.

A more meaningful USDJPY executable-density region appears around 490 to 550 USD at 1% risk.

XAUUSD does not become mechanically executable until roughly 935 USD at 1% risk.

This result strengthens the conclusion that the blocker is economic / broker minimum-volume feasibility, not a known H024 signal-code malfunction.

## Deployment Boundary

This result does not approve:

- Demo deployment
- Live deployment
- Phase 4
- OrderSend
- OrderCheck
- CTrade
- MqlTradeRequest
- Execution adapter work
- Raising risk to force execution
- Treating 245 USD as sufficient deployment capital

The next safe work remains research-only.

Before any execution work, the project still needs an executable runtime dry-run request and separate execution safety review.

## Current Verdict

H024 is closer to having a quantified deployment envelope, but it is still not deployable at the current 100 USD / 1% setting.

For 100 USD / 1%, deployment readiness remains zero.

For larger-balance research, the evidence now suggests:

- 245 USD: first executable USDJPY threshold only
- 490 to 550 USD: meaningful USDJPY feasibility begins
- 935 to 1000 USD: dual-symbol feasibility begins
