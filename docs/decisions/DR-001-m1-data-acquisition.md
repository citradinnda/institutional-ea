# Decision Record 001: Research-Grade M1 Data Acquisition Path

Date: 2026-05-03

Status: Accepted

## Context

The project is building a USDJPY + XAUUSD MetaTrader 5 expert advisor with infrastructure-first discipline.

The current strategy candidate is H017.

H017 is alive, but it is not promotable.

The latest realistic event-driven backtest pipeline works, but current available M1 history is too short for research-grade validation.

The current verified event-smoke state after Phase 3.8 is:

- Full test anchor: 482 passed.
- Latest code commit before this decision path: `e79158c Phase 3.8: add event smoke data preflight checks`.
- Handoff commit after Phase 3.8: `d7239f4 Add handoff document #15 after Phase 3.8 preflight hardening`.
- Realistic event pipeline status: operational smoke passed.
- Research validation status: insufficient.

The current M1 common clean event window is approximately:

- Start: 2026-01-26 03:09:00 UTC.
- End: 2026-04-29 09:00:00 UTC.
- Common H4 bars: 411.

The required research-grade minimum is currently:

- Desired M1 start: 2021-07-02 00:00:00 UTC.
- Minimum H4 bars: 1512.

Therefore current M1 coverage fails both requirements:

- It does not start at or before 2021-07-02.
- It does not contain at least 1512 common H4 bars.

## Decision

The next infrastructure-first priority is to obtain enough clean M1 data for USDJPY and XAUUSD before treating any realistic event-driven H017 result as research-grade.

We will not promote H017 to live trading, tune parameters, broaden symbols, or add machine learning until the data coverage blocker is resolved or explicitly deferred in a later decision record.

## Required Data

The project needs M1 data for both:

- USDJPY
- XAUUSD

The target historical window is:

- Start at or before: 2021-07-02 00:00:00 UTC.
- End: as recent as practical.

The data must support reconstruction of H4 event fills using M1 intrabar bars.

Required columns after loading are canonical OHLCV:

- timestamp
- open
- high
- low
- close
- volume

The current MT5 loader expects MetaTrader 5 History Center CSV columns:

- `<DATE>`
- `<TIME>`
- `<OPEN>`
- `<HIGH>`
- `<LOW>`
- `<CLOSE>`
- `<TICKVOL>`
- `<VOL>`
- `<SPREAD>`

The loader maps:

- `<TICKVOL>` to `volume`

The loader drops:

- `<VOL>`
- `<SPREAD>`

The broker timezone assumption is:

- Europe/Athens
- Winter UTC+2
- Summer UTC+3
- DST-aware

## Accepted Acquisition Path

The preferred path is to first attempt a broker-native MT5 export because it is closest to the final execution environment.

Accepted first source:

- Exness MetaTrader 5 History Center export.

Accepted export format:

- CSV from MT5 History Center.
- One file per symbol and timeframe.
- M1 files must be placed locally under:

```text
C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
```

The raw data directory must remain gitignored.

Do not commit raw market data.

## Validation Requirements After Acquisition

After replacing or extending M1 files, run the real event smoke script:

```powershell
python scripts\run_h017_event_real.py
```

The output must be checked for:

1. H4 leakage scan.
2. Clean common event window.
3. M1 coverage guard.
4. Event-driven backtest summary.
5. H017 claim summary.
6. Operational verdict.

The key required improvement is:

```text
RESEARCH VALIDATION SUFFICIENT: True
```

If the pipeline passes but research validation remains false, then the data acquisition is operationally useful but still not research-grade.

## Rejected Options

### Rejected: Promote H017 using current short M1 window

Reason:

The current event-driven result uses only a short 2026 window.

The current short-window result showed high return, but that is not enough evidence.

The observed drawdown was also severe.

Promoting based on this would repeat the core mistake of earlier failed strategies: trusting attractive backtest output without enough validation depth.

### Rejected: Tune H017 parameters before fixing M1 coverage

Reason:

Tuning before solving data coverage risks overfitting to the short available M1 window.

Overfitting means adapting parameters to historical noise instead of durable edge.

### Rejected: Add machine learning now

Reason:

Machine learning would add complexity while the current blocker is data sufficiency.

The project history already shows that ML cannot compensate for weak validation, fictional fills, or poor risk control.

### Rejected: Broaden to more symbols now

Reason:

Adding instruments before solving M1 coverage for the core two-symbol portfolio would increase operational complexity.

H015 already showed that diversification into negative-edge instruments can destroy the portfolio.

### Rejected: Switch silently to a different vendor

Reason:

Vendor changes affect timestamps, sessions, spreads, missing bars, and symbol conventions.

Any non-MT5 or non-Exness source must be introduced through a separate decision record and loader validation phase.

## Operational Rules

1. Keep raw data out of Git.
2. Keep `/data/` root-anchored in `.gitignore`.
3. Do not change `.gitignore` from `/data/` to unanchored `data/`.
4. Do not treat smoke success as research sufficiency.
5. Do not treat short-window profit as validated edge.
6. Do not start Phase 4 live-execution code until the research blocker is explicitly resolved or deferred.
7. Preserve the current event-driven timing convention:
   - H017 decides at H4 timestamp `t`.
   - Trade opens on next H4 bar open `t+1`.
   - M1 bars inside `[t+1, t+2)` resolve stops.
   - If no stop is hit, exposure closes at `t+2` open as `signal_flip`.
8. Preserve the conservative fill rule:
   - If stop and take-profit are both touched inside the same M1 bar, stop wins.

## Next Operational Step

Attempt to obtain longer MT5 M1 exports for both USDJPY and XAUUSD.

After placing the files locally, rerun:

```powershell
python scripts\run_h017_event_real.py
```

Then inspect whether:

```text
RESEARCH VALIDATION SUFFICIENT: True
```

If true, continue with deeper event-driven validation.

If false, record why the available M1 history is still insufficient and decide whether to:

1. Seek another validated data source.
2. Lower the research threshold with justification.
3. Defer H017 promotion.
4. Continue engine hardening without claiming research-grade validation.
