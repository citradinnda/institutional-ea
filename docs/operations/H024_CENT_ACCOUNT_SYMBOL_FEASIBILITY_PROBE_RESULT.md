# H024 Cent Account Symbol Feasibility Probe Result

Research only. No demo/live/Phase 4 approval.

## Summary

A read-only MT5 probe was run against the user's Exness Standard Cent account.

No order execution was used.

The probe used:

- `mt5.account_info()`
- `mt5.symbol_info()`
- `mt5.order_calc_profit()`

It did not use:

- OrderSend
- OrderSendAsync
- OrderCheck
- CTrade
- MqlTradeRequest
- MqlTradeResult
- Any execution adapter

## Account Snapshot

Observed account:

- Server: Exness-MT5Real25
- Currency: USC
- Balance: 0.0
- Equity: 0.0
- Leverage: 2000

The account was not funded at probe time.

## Symbol Universe

Available deployment symbols on this account:

| Symbol | Found | Trade Mode | Contract Size | Min Volume | Volume Step | Spread |
|---|---:|---:|---:|---:|---:|---:|
| USDJPYc | yes | 4 | 1000.0 | 0.01 | 0.01 | 18 |
| XAUUSDc | yes | 4 | 1.0 | 0.01 | 0.01 | 360 |
| USDJPYm | no | - | - | - | - | - |
| XAUUSDm | no | - | - | - | - | - |
| USDJPY | no | - | - | - | - | - |
| XAUUSD | no | - | - | - | - | - |

This means the earlier standard-symbol `USDJPYm` / `XAUUSDm` feasibility scans are not the final deployment authority for this cent account.

## Read-Only Sizing Probe

Probe assumptions:

- Target balance: 10000 USC
- Risk fraction: 1%
- Risk budget: 100 USC
- Profit/loss calculator: MT5 `order_calc_profit`
- No order execution

### USDJPYc Probe

Candidate borrowed from the prior standard-symbol threshold scan:

- Symbol: USDJPYc
- Side: sell
- Entry: 110.015
- Stop: 110.2840593855
- Contract size: 1000.0
- Volume min: 0.01
- Volume step: 0.01

Observed MT5 calculation:

- Loss per 1 lot at stop: 171.730000 USC
- Loss per min lot at stop: 1.720000 USC
- Raw lots for 1% risk: 0.582309
- Final lots after step: 0.580000
- Final loss at stop: 99.600000 USC
- Final risk fraction: 0.0099600000
- Verdict: WOULD_BE_EXECUTABLE_BY_SIZE

### XAUUSDc Probe

Candidate borrowed from the prior standard-symbol threshold scan:

- Symbol: XAUUSDc
- Side: sell
- Entry: 1913.59
- Stop: 1922.9379866787
- Contract size: 1.0
- Volume min: 0.01
- Volume step: 0.01

Observed MT5 calculation:

- Loss per 1 lot at stop: 934.800000 USC
- Loss per min lot at stop: 9.300000 USC
- Raw lots for 1% risk: 0.106975
- Final lots after step: 0.100000
- Final loss at stop: 93.500000 USC
- Final risk fraction: 0.0093500000
- Verdict: WOULD_BE_EXECUTABLE_BY_SIZE

## Interpretation

This is a major feasibility improvement compared with the prior standard-symbol result.

The prior standard-symbol result showed that 100 USD / 1% was mechanically blocked by broker minimum volume on `USDJPYm` / `XAUUSDm`.

This cent-account probe shows that at 10000 USC / 1% risk, representative USDJPYc and XAUUSDc stop scenarios are mechanically executable by size according to MT5's own read-only profit calculator.

This does not yet prove full H024 deployment readiness.

It does prove that the cent account must be evaluated as its own symbol-spec universe rather than treated as equivalent to the prior standard-symbol scans.

## Remaining Gates

Still missing:

- Funded 10000 USC account state
- Full cent-symbol H024 feasibility scan
- Cent-symbol log-only EA/runtime replay
- Executable runtime dry-run request from cent-symbol runtime CSV
- Execution safety review
- Demo adapter
- Demo order-behavior evidence
- Live approval

Still forbidden:

- OrderSend
- OrderSendAsync
- OrderCheck
- CTrade
- MqlTradeRequest
- MqlTradeResult
- Execution adapter work
- Demo deployment
- Live deployment
- Phase 4 approval

## Current Verdict

The cent-account path is mechanically plausible by size, but H024 is still research-only.

The next safe step is to build or run a full cent-symbol feasibility scan using the actual `USDJPYc` and `XAUUSDc` symbol specs.
