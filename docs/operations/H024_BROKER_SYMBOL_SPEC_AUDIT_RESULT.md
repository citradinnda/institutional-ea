# H024 Broker Symbol Spec Audit Result

Research diagnostic only.

This is not:
- demo approval
- live approval
- Phase 4 approval
- execution approval

## Diagnostic

Command:

```powershell
python .\scripts\audit_h024_broker_symbol_specs.py

Input CSV:

reports\h024_mt5_symbol_specs.csv

The CSV is a local broker/account artifact and should not be committed.

MT5 Symbols

The Exness MT5 symbols exported were:

USDJPYm
XAUUSDm

For audit comparison, they were normalized to model symbols:

USDJPY
XAUUSD
Result
Symbol    Field    Model expected    MT5 observed    Status
USDJPY    contract_size    100000    100000    ok
USDJPY    quote_currency    JPY    JPY    ok
USDJPY    lot_step    0.01    0.01    ok
USDJPY    min_lot    0.01    0.01    ok
USDJPY    spread_price    0.01    0.018    mismatch
USDJPY    commission_usd_per_lot_per_fill    7    0    mismatch
USDJPY    stop_slippage_atr_fraction    0.05    0.05    ok
XAUUSD    contract_size    100    100    ok
XAUUSD    quote_currency    USD    USD    ok
XAUUSD    lot_step    0.01    0.01    ok
XAUUSD    min_lot    0.01    0.01    ok
XAUUSD    spread_price    0.30    0.36    mismatch
XAUUSD    commission_usd_per_lot_per_fill    10    0    mismatch
XAUUSD    stop_slippage_atr_fraction    0.05    0.05    ok

Mismatch count: 4.

Verdict: FAIL.

Interpretation

The static instrument assumptions matched:

contract size
quote currency
lot step
minimum lot

The static cost assumptions did not match the supplied MT5 symbol facts:

USDJPY observed spread was 0.018 versus model 0.010
XAUUSD observed spread was 0.36 versus model 0.30
observed commission fields were 0.0 versus model assumptions of 7.0 and 10.0 USD per lot per fill

The commission mismatch may reflect Exness account type. A zero-commission account can still be more expensive through wider spreads. Therefore this result should not be interpreted as "costs are lower." It means the current modeled cost decomposition is not reconciled to the observed MT5 account.

Consequence

This blocks demo-readiness review until broker-cost reconciliation is completed.

Next required diagnostic:

rerun frozen H024 hold=3 under observed MT5 spread/commission assumptions
preserve H018 hard guards
do not optimize H024 parameters
do not lower costs unless justified by MT5 account facts
record whether H024 survives the observed-cost scenario
Status

H024 remains:

not demo-approved
not live-approved
not Phase 4-approved
