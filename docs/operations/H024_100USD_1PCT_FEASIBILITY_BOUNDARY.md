# H024 100 USD / 1 Percent Risk Feasibility Boundary

Status: research-only / pre-deployment.

H024 is not demo-approved, not live-approved, and not Phase 4-approved.

## Boundary Result

At the current intended setting:

- Balance: 100 USD
- Risk fraction: 1 percent

H024 has no executable historical candidate shifts.

The current blocker is economic / broker minimum-volume feasibility, not a known strategy-code malfunction.

## Exact Thresholds at 1 Percent Risk

Reusable capital threshold scanning found:

| Scope | First executable balance |
|---|---:|
| ANY H024 candidate | 245 USD |
| USDJPY | 245 USD |
| XAUUSD | 935 USD |

These thresholds quantify mechanical feasibility only.

They do not approve:

- Increasing account balance
- Increasing risk
- Demo trading
- Live trading
- Phase 4 execution
- OrderSend / OrderCheck / CTrade / MqlTradeRequest
- Execution adapter work

## Current Deployment Gate

At 100 USD / 1 percent risk, H024 cannot yet pass the required path:

runtime CSV -> executable dry-run request -> execution-safety review

because no executable dry-run request exists at the current setting.

BLOCKED rows with positive sizing diagnostics remain non-executable and must not become dry-run requests.

## Allowed Next Work

Safe next work remains limited to:

- Log-only runtime replay
- CSV-read-only reconciliation
- Parameterized threshold reporting
- Research-level stop / symbol / sizing investigation
- Documentation that prevents deployment-boundary confusion

Do not proceed to execution adapter or demo trading from this result.
