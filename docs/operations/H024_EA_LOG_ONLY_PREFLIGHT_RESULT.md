# H024 EA Log-Only Runtime Preflight Result

Status: PASS

Date: 2026-05-09

Scope:

- Terminal-attached MT5 EA runtime preflight.
- Log-only EA skeleton: `ea_mt5/Experts/H024_LogOnly_Preflight.mq5`.
- Runtime CSV verifier: `scripts/verify_h024_ea_preflight_log.py`.
- Local runtime CSV: `reports/h024_ea_log_only_preflight.csv`.

Safety boundary:

- Research only.
- No demo trading approval.
- No live trading approval.
- No Phase 4 execution approval.
- No order placement.
- No order modification.
- No order closing.
- No order deletion.
- No `OrderSend` path.
- No `CTrade` path.
- Kill switch remained blocked.

Runtime symbols covered:

| Model symbol | Broker symbol | Runtime rows |
|---|---:|---:|
| USDJPY | USDJPYm | INIT + DEINIT |
| XAUUSD | XAUUSDm | INIT + DEINIT |

Observed runtime facts:

| Field | USDJPYm | XAUUSDm |
|---|---:|---:|
| account_company | Exness Technologies Ltd | Exness Technologies Ltd |
| account_server | Exness-MT5Trial6 | Exness-MT5Trial6 |
| account_currency | USD | USD |
| account_balance | 1246.45 | 1246.45 |
| account_equity | 1246.45 | 1246.45 |
| account_leverage | 2000 | 2000 |
| account_trade_allowed | true | true |
| account_trade_expert | true | true |
| terminal_connected | true | true |
| terminal_trade_allowed | false | false |
| mql_trade_allowed | true | true |
| bid | 156.676 | 4715.309 |
| ask | 156.694 | 4715.669 |
| spread_points | 18 | 360 |
| volume_min | 0.01 | 0.01 |
| volume_max | 300.00 | 200.00 |
| volume_step | 0.01 | 0.01 |
| stops_level | 0 | 0 |
| freeze_level | 0 | 0 |
| point | 0.0010000000 | 0.0010000000 |
| digits | 3 | 3 |

Verifier command:

```powershell
python .\scripts\verify_h024_ea_preflight_log.py reports\h024_ea_log_only_preflight.csv

Verifier result:

H024 log-only EA runtime preflight verification
========================================================================
Research only. No demo/live/Phase 4 approval.

Rows: 4
Violations: 0

Verdict: PASS

Interpretation:

The terminal-attached log-only EA runtime preflight passed for both required H024 broker symbols.

This verifies:

EA can attach to MT5 charts.
EA can write runtime preflight logs from the MT5 terminal context.
Runtime account, terminal, and symbol metadata are available to the EA.
Kill switch default remained blocked.
The Python verifier accepted the runtime CSV shape and required both symbols.
The log-only runtime path did not require any order-send capability.

Important limitation:

This does not approve demo trading, live trading, Phase 4 execution, order placement, order modification, or order closing.

The observed terminal_trade_allowed=false condition remains important. It did not block this read-only runtime preflight, but it must be understood before any later execution gate.

Next allowed work:

Add a stricter static verifier for the EA source if needed.
Add a no-order dry-run intent log representation inside EA runtime.
Add a verifier for intended-action runtime logs.

Still not allowed:

Demo order placement.
Live order placement.
Execution adapter.
OrderSend.
CTrade.
Phase 4 execution.

## Versioned Runtime Schema Recheck - 2026-05-09

After commit `e043de5 Version H024 EA runtime preflight schema`, the log-only EA was copied, compiled, runtime log was reset, manually attached to both required broker symbols, removed, collected, and verified.

Command family:

```text
python .\scripts\verify_h024_ea_source_static.py
python .\scripts\run_h024_mt5_log_only_preflight_local.py --terminal-data-dir <local-terminal-data-dir> --metaeditor <local-metaeditor-path> --reset-runtime-log
python .\scripts\run_h024_mt5_log_only_preflight_local.py --terminal-data-dir <local-terminal-data-dir> --collect

Static source verifier:

Violations: 0
Verdict: PASS

Compile/reset result:

Runtime CSV reset: removed existing file
MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Collected runtime CSV verifier:

Rows: 17
Violations: 0
Verdict: PASS

Runtime grouped rows:

Schema version    EA version    Runtime mode    Symbol    Event    Count
h024_ea_log_only_preflight_v2    0.2    log_only_preflight    XAUUSDm    INIT    1
h024_ea_log_only_preflight_v2    0.2    log_only_preflight    XAUUSDm    INTENT    6
h024_ea_log_only_preflight_v2    0.2    log_only_preflight    XAUUSDm    DEINIT    1
h024_ea_log_only_preflight_v2    0.2    log_only_preflight    USDJPYm    INIT    1
h024_ea_log_only_preflight_v2    0.2    log_only_preflight    USDJPYm    INTENT    7
h024_ea_log_only_preflight_v2    0.2    log_only_preflight    USDJPYm    DEINIT    1

Interpretation:

Fresh terminal-attached runtime evidence now uses explicit schema metadata.
The verifier accepted the v2 runtime CSV.
Both required H024 broker symbols were covered.
The EA emitted timer-driven INTENT rows without requiring market ticks.
Kill switch remained blocked.
This remains log-only preflight evidence.
This does not approve demo trading, live trading, Phase 4 execution, order placement, order modification, or order closing.

## Runtime Market-State Recheck - 2026-05-09

After commit `e611d62 Add H024 EA market-state preflight rows`, the log-only EA was copied, compiled, runtime log was reset, manually attached to both required broker symbols, removed, collected, and verified.

Static source verifier:

```text id="ddf501"
Violations: 0
Verdict: PASS

Compile/reset result:

Runtime CSV reset: removed existing file
MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Collected runtime CSV verifier:

Rows: 22
Violations: 0
Verdict: PASS

Runtime grouped rows:

Schema version    EA version    Runtime mode    Symbol    Event    Count
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    USDJPYm    INIT    1
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    USDJPYm    INTENT    4
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    USDJPYm    MARKET_STATE    4
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    USDJPYm    DEINIT    1
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    XAUUSDm    INIT    1
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    XAUUSDm    INTENT    5
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    XAUUSDm    MARKET_STATE    5
h024_ea_log_only_preflight_v2    0.3    log_only_preflight    XAUUSDm    DEINIT    1

Observed market-state examples:

USDJPYm:
H4:time=2026.05.08 20:00:00;open=156.726;high=156.754;low=156.647;close=156.676;tick_volume=1028
M1:time=2026.05.08 20:58:00;open=156.691;high=156.695;low=156.670;close=156.676;tick_volume=19

XAUUSDm:
H4:time=2026.05.08 20:00:00;open=4723.858;high=4724.334;low=4714.357;close=4715.309;tick_volume=4458
M1:time=2026.05.08 20:57:00;open=4715.503;high=4715.503;low=4715.002;close=4715.309;tick_volume=42

Interpretation:

Fresh terminal-attached runtime evidence now includes no-order H4/M1 market-state observations.
The verifier accepted the EA 0.3 runtime CSV.
Both required H024 broker symbols were covered.
The EA emitted timer-driven INTENT and MARKET_STATE rows without requiring market ticks.
Runtime H4 and M1 data access from EA context is confirmed for both symbols.
Kill switch remained blocked.
This remains log-only preflight evidence.
This does not approve demo trading, live trading, Phase 4 execution, order placement, order modification, or order closing.

## H024 EA 0.4 Closed-Bar Observation Runtime Preflight

Result date: 2026-05-09

Purpose:

Validate that the log-only MT5 EA can emit closed-bar observation rows from terminal runtime context for both required H024 broker symbols without adding any order-send surface.

Safety boundary:

- Research only.
- No demo approval.
- No live approval.
- No Phase 4 approval.
- No attach/detach automation approval.
- No GUI automation approval.
- No order placement, modification, closing, or deletion.
- Kill switch remained blocked.

Commands:

```powershell
python .\scripts\verify_h024_ea_source_static.py

python .\scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --metaeditor "C:\Program Files\MetaTrader 5\MetaEditor64.exe" `
  --automation-target-preflight `
  --reset-runtime-log

python .\scripts\run_h024_mt5_log_only_preflight_local.py `
  --terminal-data-dir "C:\Users\equin\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075" `
  --collect

Static source verifier:

Violations: 0
Verdict: PASS

Automation target preflight:

expected_schema_version: h024_ea_log_only_preflight_v2
expected_ea_version: 0.4
expected_symbols: USDJPYm, XAUUSDm
Violations: 0
Verdict: PASS

Compile/reset:

Runtime CSV reset: removed existing file
MetaEditor compile return code: 1
EX5 refreshed: True
Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.

Runtime collection/verifier:

Rows: 52
Violations: 0
Verdict: PASS

Runtime grouped rows:

h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, XAUUSDm, INIT                1
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, XAUUSDm, INTENT              8
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, XAUUSDm, MARKET_STATE        8
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, XAUUSDm, BAR_OBSERVATION     8
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, XAUUSDm, DEINIT              1
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, USDJPYm, INIT                1
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, USDJPYm, INTENT              8
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, USDJPYm, MARKET_STATE        8
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, USDJPYm, BAR_OBSERVATION     8
h024_ea_log_only_preflight_v2, 0.4, log_only_preflight, USDJPYm, DEINIT              1

Observed BAR_OBSERVATION example:

symbol: XAUUSDm
event: BAR_OBSERVATION
detail: H4_closed:time=2026.05.08 16:00:00;open=4706.9830000000;high=4729.0040000000;low=4705.5030000000;close=4723.7890000000;tick_volume=29031|M1_closed:time=2026.05.08 20:56:00;open=4715.1460000000;high=4715.6100000000;low=4714.9540000000;close=4715.5580000000;tick_volume=67

Interpretation:

The EA 0.4 terminal-attached log-only runtime preflight passed.

The runtime now emits closed-bar BAR_OBSERVATION rows for both required H024 broker symbols. This confirms that the EA can read latest completed H4 and M1 bars from MT5 runtime context and write them into the versioned preflight CSV.

This is a necessary runtime-ingestion preparation step only. It does not compute H024 strategy state, does not emit strategy-derived WOULD_OPEN rows, and does not approve demo trading, live trading, Phase 4, attach/detach automation, GUI automation, or order-send code.
