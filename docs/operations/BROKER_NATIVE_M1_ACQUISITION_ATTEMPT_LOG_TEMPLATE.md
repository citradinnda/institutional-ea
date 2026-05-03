# Broker-Native M1 Acquisition Attempt Log Template

Phase: 3.26-aa  
Status: template only  
Date: 2026-05-03

## Purpose

This template defines how to record manual attempts to acquire longer broker-native M1 data.

The goal is to make every acquisition attempt auditable before any raw inventory, parser work, source-acceptance diagnostic, or H017 validation is considered.

This document is a template only.

It does not approve:

1. H017 validation.
2. H017 validation on newly acquired data.
3. H017 validation on HistData.
4. Source acceptance.
5. Raw data commits.
6. Derived data generation.
7. Strategy tuning.
8. Live trading.

## Current Validation State

Accepted H4 reference for broker-aligned diagnostics:

- Broker-native H4.

Accepted M1 source for broker-only short-window diagnostics:

- Broker-native M1.

Accepted long-history M1 validation source:

- None.

Accepted H017 validation source:

- None.

HistData status:

- Rejected for H017 validation under current evidence.
- Not accepted as a research source.
- Diagnostic-reference only.

H017 status:

- Alive.
- Not promotable.
- Not ready for live trading.

Research validation status:

- Blocked pending acceptable long-history M1 data.

## How To Use This Template

For each acquisition attempt, copy the relevant section into a future documented acquisition log.

Do not paste broker credentials, account numbers, passwords, API keys, or private personal information into the repository.

It is acceptable to document:

- broker name,
- server name if not sensitive,
- account type,
- symbol names,
- export method,
- timestamp ranges,
- observed data behavior,
- support answers with private details removed.

It is not acceptable to commit:

- raw CSV data,
- screenshots with account identifiers,
- credentials,
- account balances,
- personal identity documents,
- broker portal private URLs.

## Attempt Record Template

### Attempt ID

Example:

- `BROKER-M1-ATTEMPT-001`

### Attempt Date

Example:

- `YYYY-MM-DD`

### Operator

Example:

- `local user`

Avoid using sensitive personal identity information.

### Objective

Example:

- Acquire deeper broker-native M1 history for USDJPY and XAUUSD from the current MT5 broker environment.

### Broker Environment

Record if known:

1. Broker name:
2. MT5 server name:
3. Account type:
4. MT5 terminal build:
5. Operating system:
6. Was MT5 connected during export:
7. Was this the intended trading server:
8. Notes:

### Symbol Identification

Record exact symbol names as shown in MT5.

USDJPY:

1. Exact symbol name:
2. Any prefix:
3. Any suffix:
4. Contract or symbol specification notes:

XAUUSD:

1. Exact symbol name:
2. Any prefix:
3. Any suffix:
4. Contract or symbol specification notes:

### MT5 History Settings

Record:

1. Max bars in chart setting:
2. Max bars in history setting:
3. Were settings changed before export:
4. Was MT5 restarted after settings changes:
5. Was history manually scrolled back:
6. Was any History Center or download function used:
7. Notes:

### Export Method

Record:

1. Manual chart export:
2. History center export:
3. Copy from MT5 data folder:
4. Scripted export:
5. Other:
6. Exact steps used:

### Intended Raw File Paths

Raw data must stay under the root gitignored data folder.

Suggested path pattern:

- `C:\Users\equin\Documents\institutional-ea\data\raw\broker_native_candidate\YYYYMMDD\USDJPY\M1.csv`
- `C:\Users\equin\Documents\institutional-ea\data\raw\broker_native_candidate\YYYYMMDD\XAUUSD\M1.csv`

Record actual paths:

USDJPY M1 raw path:

- 

XAUUSD M1 raw path:

- 

### Raw File Handling Confirmation

Confirm:

1. Raw files were not edited:
2. Raw files were not opened and resaved in Excel:
3. Raw rows were not manually deleted:
4. Raw columns were not manually renamed:
5. Raw files remain under `/data/`:
6. Raw files were not committed:
7. No derived files were written:
8. Notes:

### Visible Date Range Before Export

USDJPY M1:

1. Earliest visible timestamp:
2. Latest visible timestamp:
3. Timezone as displayed by MT5:

XAUUSD M1:

1. Earliest visible timestamp:
2. Latest visible timestamp:
3. Timezone as displayed by MT5:

### Exported Date Range Observed Manually

Do not compute formal inventory here unless a later inventory phase is explicitly authorized.

If visible from the exported file without modifying it, record:

USDJPY M1:

1. First observed row timestamp:
2. Last observed row timestamp:
3. Approximate row count if easily visible:
4. Notes:

XAUUSD M1:

1. First observed row timestamp:
2. Last observed row timestamp:
3. Approximate row count if easily visible:
4. Notes:

### Problems Encountered

Record any issues:

1. Export failed:
2. Export truncated:
3. MT5 stopped loading older data:
4. Symbol unavailable:
5. Server disconnected:
6. Data gaps obvious by visual inspection:
7. XAUUSD behaved differently from USDJPY:
8. Timestamp timezone unclear:
9. Other:

### Immediate Classification

Choose one:

1. Acquisition failed.
2. Acquisition partially succeeded.
3. Acquisition succeeded but source is not accepted.
4. Acquisition succeeded and awaits raw inventory.

Important:

Even if acquisition succeeds, the source remains unaccepted until formal diagnostics are completed.

### Required Next Step If Files Exist

If new raw files exist, the next allowed project phase is a read-only raw inventory phase.

That phase should document:

1. File paths.
2. File sizes.
3. SHA-256 hashes.
4. Line counts.
5. First observed rows.
6. Last observed rows.
7. Symbol coverage.
8. Whether files are raw original exports.

That phase must not:

1. Run H017.
2. Validate H017.
3. Write derived data.
4. Modify raw files.
5. Commit raw files.
6. Accept the source automatically.

## Broker Support Contact Log Template

### Support Contact ID

Example:

- `BROKER-SUPPORT-M1-001`

### Contact Date

Example:

- `YYYY-MM-DD`

### Contact Method

Choose one:

1. Email.
2. Broker ticket.
3. Live chat.
4. Phone.
5. Other.

### Question Summary

Record what was asked, without private account details.

### Broker Reply Summary

Record the reply, with private account details removed.

### Claims Made By Broker

Record each claim separately.

Example:

1. Broker claims M1 history is available from:
2. Broker claims server timezone is:
3. Broker claims XAUUSD daily break is:
4. Broker claims Sunday open is:
5. Broker claims Friday close is:
6. Broker claims data type is bid/ask/mid/other:
7. Broker claims bulk export is/is not available:
8. Broker claims licensing allows private research:
9. Other:

### Evidence Quality

Choose one:

1. Written formal documentation.
2. Written support reply.
3. Informal chat reply.
4. Verbal phone claim.
5. Unknown.

### Contradictions Or Open Questions

Record:

1. Claims that conflict with observed data:
2. Missing answers:
3. Ambiguous answers:
4. Follow-up needed:

### Support Reply Handling

Confirm:

1. No private credentials committed:
2. No account number committed:
3. No personal identity information committed:
4. Reply preserved outside repo if needed:
5. Sanitized summary may be documented later:
6. Notes:

## External Source Inquiry Template

Use only if broker-native acquisition fails or is insufficient.

### External Source Candidate

Record:

1. Vendor/source name:
2. Instrument names:
3. Available years:
4. Data type:
5. Timezone:
6. DST handling:
7. Session schedule:
8. XAUUSD daily break:
9. Duplicate policy if documented:
10. File format:
11. License:
12. Cost:
13. Can raw files be preserved:
14. Is overlap available with broker-native H4/M1:
15. Notes:

### Preliminary Rejection Triggers

Reject or pause the source if any of these are true:

1. Timezone is undocumented.
2. Session schedule is undocumented.
3. XAUUSD break behavior is undocumented.
4. Data type is unclear.
5. License does not permit private research use.
6. Raw files cannot be preserved.
7. Format is proprietary with no audit path.
8. No overlap exists for broker compatibility checks.
9. Vendor encourages silent cleaned data without audit metadata.
10. Source cannot explain duplicates, gaps, or corrections.

## Final Reminder

Longer data is not automatically better data.

A longer M1 source can still be invalid for H017 if it has incompatible sessions, unexplained gaps, bad timestamp handling, vendor-specific repairs, or poor broker H4 boundary compatibility.

The project remains blocked until an acceptable long-history M1 validation source is acquired and accepted through documented diagnostics.
