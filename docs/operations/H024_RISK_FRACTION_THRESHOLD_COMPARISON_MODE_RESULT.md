# H024 Risk-Fraction Threshold Comparison Mode Result

Research only. No demo/live/Phase 4 approval.

This document preserves the result of adding and optimizing the one-command
risk-fraction capital threshold comparison mode for H024.

---

## 1. Verdict

PASS.

The optimized comparison mode produced the same known threshold table as the
manual repeated scans, while avoiding the earlier slow repeated full bridge
rescans per balance probe.

This is a tooling/result-preservation document only.

It does not approve:

- Higher risk
- Higher balance
- Demo trading
- Live trading
- Phase 4
- OrderSend
- OrderCheck
- CTrade
- MqlTradeRequest
- Any execution adapter

---

## 2. Relevant Commits

Feature commit:

```text
782eb16 Add H024 risk fraction threshold comparison mode

Whitespace cleanup:

b3cd189 Clean H024 threshold comparison whitespace

Optimization commit:

f0413f2 Optimize H024 threshold comparison scans

The latest expected commit before this documentation commit is:

f0413f2 Optimize H024 threshold comparison scans
3. What Changed

The capital threshold scanner now supports a single comparison command:

python scripts\scan_h024_capital_thresholds.py --risk-fractions 0.005,0.0075,0.01,0.015,0.02

The initial implementation was correct but expensive because each balance probe
could reload broker-native H4 data and rerun the H024 bridge.

The optimization added reusable H024 executable-candidate scan inputs so
broker-native H4 data and H024 signal/stop geometry can be reused while each
balance still routes through H020 sizing.

Important safety detail:

The optimization does not bypass H020 sizing.

It still preserves:

H020 risk-based lots
H020 per-trade notional caps
H020 portfolio scaling
Broker minimum-lot suppression semantics
Research-only / no-execution boundary
4. Validation Commands Run

Focused tests after optimization:

python -m pytest tests\test_h024_executable_candidate_shift_scan.py tests\test_h024_capital_threshold_scan.py -q

Observed:

15 passed in 1.96s

Full suite after optimization:

python -m pytest -q

Observed anchor from this work:

944 passed in 19.53s

Diff whitespace check after cleanup:

git diff --check

Observed:

clean
5. One-Command Comparison Result

Command:

python scripts\scan_h024_capital_thresholds.py --risk-fractions 0.005,0.0075,0.01,0.015,0.02

Observed output:

H024 risk-fraction capital threshold comparison
========================================================================
Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.

Risk fraction    ANY threshold    USDJPY threshold    XAUUSD threshold
0.50%    490 USD    490 USD    1,870 USD
0.75%    327 USD    327 USD    1,247 USD
1.00%    245 USD    245 USD    935 USD
1.50%    164 USD    164 USD    624 USD
2.00%    123 USD    123 USD    468 USD

Verdict: PASS
Thresholds quantified only; no higher-risk, no higher-balance, no demo/live, and no execution approval implied.
6. Interpretation

At the actual intended current setting:

Balance: 100 USD
Risk:    1%

H024 remains mechanically non-executable under the current broker minimum-volume
constraints.

At 2% risk, the first ANY / USDJPY executable threshold is still 123 USD.

Therefore, 100 USD remains non-executable even at 2% risk.

Approximate implied risk needed at 100 USD remains:

ANY / USDJPY: about 2.45%
XAUUSD:       about 9.35%

These are feasibility measurements only.

They are not recommendations and do not approve raising risk.

7. Current Deployment Boundary

H024 remains:

Research-only
Not demo-approved
Not live-approved
Not Phase 4-approved
Not approved for any execution adapter
Not approved for any order-send path

The current blocker remains economic / broker minimum-volume feasibility, not a
known H024 strategy-code malfunction.

No execution work should proceed from this document alone.
