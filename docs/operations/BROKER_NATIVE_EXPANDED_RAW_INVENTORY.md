# Broker-Native Expanded Raw Inventory

Phase: 3.26-ab
Status: raw inventory only
Date: 2026-05-03

## Purpose

This document records a read-only raw inventory of newly exported broker-native MT5 CSV files.

The user reported that deeper broker-native M1 export succeeded for USDJPYm and XAUUSDm, with earliest visible M1 history reaching 2018.

The user also reported successfully exporting updated H4 files for both pairs, also starting from 2018.

This inventory does not accept the data source.

This inventory does not approve H017 validation.

This inventory does not write derived data.

## Manual Acquisition Summary

- Broker: Exness
- Server: MT5
- Account type: Demo
- MT5 terminal build: not recorded
- USDJPY exact MT5 symbol: USDJPYm
- USDJPY earliest visible M1 timestamp: 2018
- USDJPY M1 export succeeded: yes
- USDJPY M1 raw path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
- XAUUSD exact MT5 symbol: XAUUSDm
- XAUUSD earliest visible M1 timestamp: 2018
- XAUUSD M1 export succeeded: yes
- XAUUSD M1 raw path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
- Additional note: updated H4 data for both pairs was also exported to the same existing raw directories, with more data starting from 2018.

## Raw Data Handling

The inspected files are under the repository root /data/ directory.

The root /data/ directory is gitignored and raw data files must not be committed.

This phase did not modify the raw files.

This phase did not create derived datasets.

## Inventory Results

### USDJPY M1

- Symbol: USDJPYm
- Timeframe: M1
- Raw path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\M1.csv
- Exists: True
- Size bytes: 108190060
- SHA-256: 679bb6f153a24aac8fc27238ad1ba7f5fb121a759baea759c8b59ac1b18b2619
- Line count: 1785313

First observed lines:

- `<DATE>	<TIME>	<OPEN>	<HIGH>	<LOW>	<CLOSE>	<TICKVOL>	<VOL>	<SPREAD>`
- `2018.07.03	00:00:00	110.877	111.124	110.378	110.411	50944	0	0`
- `2018.07.04	00:00:00	110.410	110.549	110.274	110.499	44662	0	0`
- `2018.07.05	00:00:00	110.498	110.715	110.286	110.559	50143	0	0`
- `2018.07.06	00:00:00	110.562	110.780	110.377	110.440	40301	0	0`

Last observed lines:

- `2026.04.30	09:56:00	159.334	159.393	159.334	159.393	82	0	10`
- `2026.04.30	09:57:00	159.390	159.420	159.377	159.406	122	0	10`
- `2026.04.30	09:58:00	159.405	159.405	159.356	159.362	106	0	10`
- `2026.04.30	09:59:00	159.358	159.366	159.331	159.339	72	0	10`
- `2026.04.30	10:00:00	159.339	159.350	159.326	159.333	105	0	10`

### USDJPY H4

- Symbol: USDJPYm
- Timeframe: H4
- Raw path: C:\Users\equin\Documents\institutional-ea\data\raw\USDJPY\H4.csv
- Exists: True
- Size bytes: 548819
- SHA-256: 72a6db90e42b53338ff5a57e5362be32c77caca290c90800c8cf60ce342e7651
- Line count: 8714

First observed lines:

- `<DATE>	<TIME>	<OPEN>	<HIGH>	<LOW>	<CLOSE>	<TICKVOL>	<VOL>	<SPREAD>`
- `2018.07.03	00:00:00	110.877	111.124	110.378	110.411	50944	0	0`
- `2018.07.04	00:00:00	110.410	110.549	110.274	110.499	44662	0	0`
- `2018.07.05	00:00:00	110.498	110.715	110.286	110.559	50143	0	0`
- `2018.07.06	00:00:00	110.562	110.780	110.377	110.440	40301	0	0`

Last observed lines:

- `2026.04.29	16:00:00	160.230	160.438	160.163	160.376	14888	0	10`
- `2026.04.29	20:00:00	160.370	160.442	160.147	160.198	4909	0	10`
- `2026.04.30	00:00:00	160.196	160.422	160.068	160.418	10101	0	10`
- `2026.04.30	04:00:00	160.420	160.723	159.783	160.132	11678	0	10`
- `2026.04.30	08:00:00	160.134	160.176	155.549	156.372	100985	0	10`

### XAUUSD M1

- Symbol: XAUUSDm
- Timeframe: M1
- Raw path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\M1.csv
- Exists: True
- Size bytes: 113195272
- SHA-256: dc08ef307f9eb6566e4dfdb88cd1bcaaf473f26ab5b30724230ef2fd2b52e609
- Line count: 1704908

First observed lines:

- `<DATE>	<TIME>	<OPEN>	<HIGH>	<LOW>	<CLOSE>	<TICKVOL>	<VOL>	<SPREAD>`
- `2018.06.28	00:00:00	1252.884	1254.229	1245.910	1248.581	81353	0	0`
- `2018.06.29	00:00:00	1248.551	1255.573	1245.978	1252.533	79160	0	0`
- `2018.07.01	00:00:00	1253.020	1254.149	1252.785	1253.365	2202	0	0`
- `2018.07.02	00:00:00	1253.329	1253.576	1239.648	1242.103	75367	0	0`

Last observed lines:

- `2026.04.30	09:56:00	4625.743	4626.172	4624.509	4624.716	132	0	280`
- `2026.04.30	09:57:00	4624.631	4625.416	4624.420	4624.946	134	0	280`
- `2026.04.30	09:58:00	4624.889	4625.384	4623.375	4624.865	192	0	280`
- `2026.04.30	09:59:00	4624.779	4626.112	4624.231	4624.962	158	0	280`
- `2026.04.30	10:00:00	4625.030	4627.281	4625.030	4626.687	199	0	280`

### XAUUSD H4

- Symbol: XAUUSDm
- Timeframe: H4
- Raw path: C:\Users\equin\Documents\institutional-ea\data\raw\XAUUSD\H4.csv
- Exists: True
- Size bytes: 594386
- SHA-256: ae9280b257bedd889152392339c32eb957a8aa4549649ac343a73e2663ac8b74
- Line count: 8659

First observed lines:

- `<DATE>	<TIME>	<OPEN>	<HIGH>	<LOW>	<CLOSE>	<TICKVOL>	<VOL>	<SPREAD>`
- `2018.06.28	00:00:00	1252.884	1254.229	1245.910	1248.581	81353	0	0`
- `2018.06.29	00:00:00	1248.551	1255.573	1245.978	1252.533	79160	0	0`
- `2018.07.01	00:00:00	1253.020	1254.149	1252.785	1253.365	2202	0	0`
- `2018.07.02	00:00:00	1253.329	1253.576	1239.648	1242.103	75367	0	0`

Last observed lines:

- `2026.04.29	16:00:00	4547.794	4564.972	4517.951	4547.032	75284	0	280`
- `2026.04.29	20:00:00	4546.938	4562.086	4539.271	4561.717	22487	0	280`
- `2026.04.30	00:00:00	4561.621	4582.525	4555.500	4556.017	46829	0	280`
- `2026.04.30	04:00:00	4555.991	4605.493	4540.766	4598.212	42231	0	280`
- `2026.04.30	08:00:00	4598.271	4646.985	4597.267	4629.938	62255	0	280`

## Current Interpretation

The expanded broker-native export may materially improve the data situation because it appears to extend M1 history back to 2018.

However, the data remains unaccepted until further diagnostics are completed.

Required future diagnostics include:

1. Loader smoke test on the expanded broker-native files.
2. Timezone and timestamp-shape confirmation.
3. Duplicate timestamp check.
4. Coverage analysis by symbol, year, month, hour, and cross-symbol common window.
5. Broker H4/M1 aggregation compatibility over the expanded overlap.
6. Session-boundary analysis for Sunday opens, Friday closes, DST transitions, and XAUUSD breaks.
7. Explicit source-acceptance or source-rejection checkpoint.

## Explicit Non-Approval

This inventory does not approve:

1. H017 validation.
2. H017 validation on the expanded broker-native files.
3. HistData validation.
4. Source acceptance.
5. Derived data generation.
6. Strategy tuning.
7. Cost model changes.
8. New instruments.
9. Machine learning.
10. Phase 4 execution.
11. Live trading.

## Current State After Inventory

Accepted H4 reference for broker-aligned diagnostics:

- Broker-native H4, diagnostic reference only.

Accepted M1 source for broker-only short-window diagnostics:

- Previously exported broker-native M1 short window.

Candidate expanded broker-native M1 source:

- Newly exported broker-native M1 files, unaccepted pending diagnostics.

Accepted long-history M1 validation source:

- None.

Accepted H017 validation source:

- None.

H017 status:

- Alive but not promotable.

Research validation status:

- Still blocked pending diagnostics and explicit source acceptance.
