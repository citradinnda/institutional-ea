# MT5 M1 Export Checklist

## Purpose

This checklist explains how to obtain longer MetaTrader 5 M1 exports for the local event-driven H017 research pipeline.

M1 means 1-minute bars. These bars are needed because the event-driven backtest uses M1 candles inside each H4 candle to decide whether a stop loss was touched before the planned H4 exit.

This checklist is operational documentation only. It does not promote H017, change strategy logic, change risk rules, or approve live trading.

## Current Research Status

H017 is currently:

1. Alive.
2. Not promotable.
3. Not ready for live trading.
4. Blocked by insufficient M1 history for research-grade event validation.

The realistic event-driven pipeline can run, but the current common M1 window is too short.

Current required validation marker:

    RESEARCH VALIDATION SUFFICIENT: True

If the script still prints:

    RESEARCH VALIDATION SUFFICIENT: False

then the pipeline may work, but research validation is still insufficient.

## Required Local File Locations

Place the exported CSV files at these exact paths:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

The existing H4 files should remain here:

    C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
    C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv

Do not rename the files unless the loader or smoke script is deliberately updated in a separate code phase.

## Git Safety Rule

Do not commit raw data.

The `data` folder is intentionally ignored by Git through this root-anchored `.gitignore` rule:

    /data/

This is correct.

Do not change it to:

    data/

The unanchored form can accidentally ignore source-code folders such as:

    C:\Users\equin\Documents\institutional-ea\quantcore\data

## Broker and Timezone Assumption

The current broker timezone assumption is:

    Europe/Athens

This matters because MetaTrader 5 CSV timestamps are broker wall-clock timestamps, not UTC timestamps.

Wall-clock timestamp means the time shown by the broker platform. The loader converts that time to UTC before research.

## MT5 Export Checklist

Use the Exness MetaTrader 5 terminal first.

For each symbol:

1. Open MetaTrader 5.
2. Log into the same Exness environment used for the existing exports.
3. Open History Center.
4. Select the symbol:
   - `USDJPY`
   - `XAUUSD`
5. Select timeframe:
   - `M1`
6. Download or load as much M1 history as the broker provides.
7. Export the data to CSV.
8. Save the exported files to the required local paths:

       C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
       C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv

## Expected MT5 CSV Columns

The expected MT5 History Center columns are:

    <DATE> <TIME> <OPEN> <HIGH> <LOW> <CLOSE> <TICKVOL> <VOL> <SPREAD>

The loader maps:

    <TICKVOL> -> volume

The loader drops:

    <VOL>
    <SPREAD>

Reason:

1. OTC FX real volume is often zero or unreliable.
2. Spread is modeled separately through the backtest cost model.

## Coverage Goal

The preferred M1 start date is:

    2021-07-02 00:00:00 UTC

Reason:

The existing H4 exports contain early daily bars disguised as H4 bars. The current reliable H4 start is:

    2021-07-02

The goal is to obtain M1 data far enough back to cover the reliable H4 period.

## Validation Command

After replacing or extending the M1 files, run:

    cd C:\Users\equin\Documents\institutional-ea
    .\.venv\Scripts\Activate.ps1
    python scripts\run_h017_event_real.py

## Success Marker

The desired output is:

    RESEARCH VALIDATION SUFFICIENT: True

This means the M1 coverage guard passed.

It does not automatically mean H017 is promotable. It only means the data coverage is sufficient for research-grade event validation.

## If Validation Is Still False

If the output still says:

    RESEARCH VALIDATION SUFFICIENT: False

then:

    Pipeline may work, but research validation is still insufficient.

Do not treat short-window returns as validated edge.

Do not promote H017 to live trading.

Do not tune strategy parameters to fit the short M1 window.

## After Exporting Data

After exporting new M1 data, record the observed output from:

    python scripts\run_h017_event_real.py

Important fields to record:

1. Earliest USDJPY M1 timestamp.
2. Earliest XAUUSD M1 timestamp.
3. Latest USDJPY M1 timestamp.
4. Latest XAUUSD M1 timestamp.
5. Clean common event window start.
6. Clean common event window end.
7. Common H4 bar count.
8. Fill count.
9. Ending equity.
10. Maximum drawdown.
11. Sharpe.
12. `RESEARCH VALIDATION SUFFICIENT`.

## Decision Discipline

If Exness cannot provide sufficient M1 history, do not silently switch vendors.

A new data vendor requires a separate decision record and a loader-validation phase.

The next decision must document:

1. Vendor name.
2. Symbols.
3. Timezone convention.
4. Column schema.
5. Data quality checks.
6. Missing-bar checks.
7. Duplicate-timestamp checks.
8. Cost or licensing constraints.
9. Whether redistribution or committing is forbidden.
10. How the new data was compared against the broker-native MT5 exports.
