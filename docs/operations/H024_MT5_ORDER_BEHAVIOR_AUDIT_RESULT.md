# H024 MT5 Order Behavior Audit Result

Research only. No demo trading is approved. No live trading is approved. Phase 4 is not approved.

## Purpose

Reconcile static MT5 order-behavior facts for the Exness symbols used by H024 before any dry-run/log-only EA work.

This audit does not place orders.

This audit does not approve:

- demo trading
- live trading
- Phase 4
- EA execution
- dry-run/log-only deployment

## Command

```powershell
python .\scripts\audit_h024_mt5_order_behavior.py
Input

Local CSV, not committed:

reports\h024_mt5_order_behavior.csv

Exported from the user's Exness MT5 terminal using the Python MetaTrader5 API.

Observed Rows
{'symbol': 'USDJPYm', 'trade_mode': 4, 'execution_mode': 2, 'order_filling_modes': 3, 'order_modes': 127, 'volume_min': 0.01, 'volume_max': 300.0, 'volume_step': 0.01, 'stops_level_points': 0, 'freeze_level_points': 0, 'point': 0.001, 'digits': 3, 'spread_float': True}
{'symbol': 'XAUUSDm', 'trade_mode': 4, 'execution_mode': 2, 'order_filling_modes': 3, 'order_modes': 127, 'volume_min': 0.01, 'volume_max': 200.0, 'volume_step': 0.01, 'stops_level_points': 0, 'freeze_level_points': 0, 'point': 0.001, 'digits': 3, 'spread_float': True}
Normalization

The model symbols remain:

USDJPY
XAUUSD

Observed Exness MT5 symbols normalize as:

USDJPYm -> USDJPY
XAUUSDm -> XAUUSD
Audit Result
Symbol    Field    Expected    Observed    Status
USDJPY    trade_mode    FULL / SYMBOL_TRADE_MODE_FULL / 4    4    ok
USDJPY    execution_mode    non-empty    2    ok
USDJPY    order_filling_modes    non-empty    3    ok
USDJPY    order_modes    non-empty    127    ok
USDJPY    volume_min    <= 0.01    0.01    ok
USDJPY    volume_max    >= 0.01    300    ok
USDJPY    volume_step    0.01    0.01    ok
USDJPY    stops_level_points    >= 0    0    ok
USDJPY    freeze_level_points    >= 0    0    ok
USDJPY    point    0.001    0.001    ok
USDJPY    digits    3    3    ok
USDJPY    spread_float    true/false/0/1    True    ok
XAUUSD    trade_mode    FULL / SYMBOL_TRADE_MODE_FULL / 4    4    ok
XAUUSD    execution_mode    non-empty    2    ok
XAUUSD    order_filling_modes    non-empty    3    ok
XAUUSD    order_modes    non-empty    127    ok
XAUUSD    volume_min    <= 0.01    0.01    ok
XAUUSD    volume_max    >= 0.01    200    ok
XAUUSD    volume_step    0.01    0.01    ok
XAUUSD    stops_level_points    >= 0    0    ok
XAUUSD    freeze_level_points    >= 0    0    ok
XAUUSD    point    0.001    0.001    ok
XAUUSD    digits    3    3    ok
XAUUSD    spread_float    true/false/0/1    True    ok

Mismatch count: 0

Verdict: PASS

Interpretation

Static MT5 order-behavior facts are reconciled for USDJPYm and XAUUSDm.

This improves execution-readiness evidence because the audit confirms:

both symbols are trade-enabled
both symbols expose non-empty execution mode metadata
both symbols expose non-empty filling-mode metadata
both symbols expose non-empty order-mode metadata
volume minimum is compatible with model assumptions
volume step is compatible with model assumptions
exported stop level is 0 points
exported freeze level is 0 points
point and digits match the broker symbol-spec audit
spread is floating

This does not test actual order placement, rejection behavior, requotes, slippage, market-hours behavior, or modification behavior.

Deployment Boundary

This result does not approve:

demo trading
live trading
Phase 4
EA execution
dry-run/log-only deployment

The next gate should be a no-order dry-run EA path or a separate explicit order-check design, depending on whether the user authorizes Phase 4 preparation work.
