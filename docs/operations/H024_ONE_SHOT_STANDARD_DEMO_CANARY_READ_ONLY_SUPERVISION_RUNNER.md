# H024 One-Shot Standard-Demo Canary Read-Only Supervision Runner

## Purpose

This runner automates the full read-only post-canary supervision stack.

It runs these stages in order:

1. build monitor
2. verify monitor
3. build lifecycle decision
4. verify lifecycle decision
5. build observation analysis
6. verify observation analysis
7. build supervisory state
8. verify supervisory state

The runner stops at the first failed stage and records a fail-closed summary.

## Command

```powershell
python scripts\run_h024_one_shot_demo_canary_read_only_supervision.py
python scripts\verify_h024_one_shot_demo_canary_read_only_supervision_jsonl.py reports\h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl --require-pass
Output

Local runtime output:

reports/h024_standard_demo_one_shot_demo_canary_read_only_supervision_run.jsonl

This file must not be committed.

Automation boundary

This is read-only automation.

It does not authorize:

a second H024 entry
live trading
a trading loop
scaling
additional symbols
close
modify
strategy-edge inference

The monitor stage may use MT5 read-only calls through the existing monitor script. The runner itself does not import MetaTrader5 and does not issue trade requests.

USDJPY

USDJPY is part of the intended H024 universe, but this runner does not automate USDJPY.

USDJPY requires a separate readiness and governance path for:

broker-native runtime symbol USDJPYm
symbol properties
spread and tick sanity
H020 sizing
request-shape preview
separate demo canary approval if later justified
Safety roadmap

Before any trading loop exists, the project still needs:

exact-ticket controlled close governance
global no-new-entry kill switch
manual override lockout file
daily loss lockout
max floating loss lockout
spread shock guard
stale tick guard
disconnected terminal guard
margin compression guard
volatility expansion / black-swan guard
unexpected position/order lockout
per-symbol circuit breakers for XAUUSD and USDJPY
