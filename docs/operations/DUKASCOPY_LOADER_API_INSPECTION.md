# Dukascopy Loader API Inspection Notes

Phase: 3.19 - Inspect existing loader APIs before designing a Dukascopy loader

Date: 2026-05-03

## Purpose

Record the actual loader APIs and project conventions observed before designing
a Dukascopy CSV loader.

This inspection prevents implementation from relying on stale handoff memory or
guessed function names.

## Scope

Files inspected:

- `quantcore/data/loaders.py`
- `tests/test_loaders.py`
- `quantcore/data/preflight.py`
- `tests/test_preflight.py`
- `quantcore/data/coverage.py`
- `tests/test_coverage.py`
- `quantcore/data/mt5_loader.py`
- `tests/test_mt5_loader.py`

## Actual loader module layout

The generic canonical loader utilities live in:

- `quantcore/data/loaders.py`

The MT5-specific loader lives in:

- `quantcore/data/mt5_loader.py`

Important correction:

- `load_mt5_csv` is not in `quantcore.data.loaders`.
- `MT5LoadResult` is not in `quantcore.data.loaders`.
- Both are in `quantcore.data.mt5_loader`.

## Canonical OHLCV convention

The project canonical OHLCV shape is:

- columns: `open`, `high`, `low`, `close`, `volume`
- column names are lowercase
- index is a pandas `DatetimeIndex`
- index is timezone-aware UTC
- rows are sorted ascending by timestamp

The current canonical helper is:

- `ensure_canonical(df: pd.DataFrame) -> pd.DataFrame`

Current behavior:

- lowercases columns
- validates required canonical columns
- converts or localizes index to UTC
- drops duplicate timestamps, keeping the first
- sorts ascending

Important design warning:

`ensure_canonical` silently drops duplicate timestamps. That behavior is
acceptable for the existing MT5 loader because the current MT5 tests document
duplicate collapse as expected behavior. However, a future Dukascopy acceptance
loader should probably reject duplicate timestamps before calling
`ensure_canonical`, because vendor-data validation should not hide duplicate
rows.

## MT5 loader API observed

Actual public function:

- `load_mt5_csv(path: str | Path, broker_tz: str = "Europe/Athens") -> MT5LoadResult`

Actual result dataclass fields:

- `bars`
- `n_bars`
- `n_input_rows`
- `earliest_utc`
- `latest_utc`
- `broker_tz`

The MT5 loader lives in:

- `quantcore.data.mt5_loader`

The MT5 loader does not live in:

- `quantcore.data.loaders`

## MT5 loader behavior observed

The MT5 loader:

- reads tab-separated MT5 History Center CSV files
- requires MT5 columns such as `<DATE>`, `<TIME>`, `<OPEN>`, `<HIGH>`, `<LOW>`, `<CLOSE>`, and `<TICKVOL>`
- treats raw MT5 timestamps as broker wall-clock time
- defaults broker timezone to `Europe/Athens`
- converts broker-local timestamps to UTC
- maps `<TICKVOL>` to canonical `volume`
- drops `<VOL>` and `<SPREAD>` from canonical output
- calls `ensure_canonical`
- reports `n_input_rows` before canonicalization
- reports `n_bars` after canonicalization

## Dukascopy implications

The observed Dukascopy sample schema is:

- `UTC`
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`

The observed timestamp format is:

- `%d.%m.%Y %H:%M:%S.%f UTC`

Example:

- `03.01.2024 00:00:00.000 UTC`

Dukascopy timestamps are explicitly labeled UTC in the sample files. Therefore,
a future Dukascopy loader should not use broker timezone localization.

Likely future module:

- `quantcore/data/dukascopy_loader.py`

Likely future test file:

- `tests/test_dukascopy_loader.py`

## Candidate Dukascopy loader rules for a future phase

A future Dukascopy loader should likely:

1. Read comma-separated CSV files with the observed schema:
   `UTC,Open,High,Low,Close,Volume`.
2. Validate required columns before transforming data.
3. Parse timestamps using the observed UTC timestamp format.
4. Produce canonical columns:
   `open`, `high`, `low`, `close`, `volume`.
5. Return a UTC timezone-aware `DatetimeIndex`.
6. Validate numeric OHLCV columns.
7. Reject duplicate timestamps before calling `ensure_canonical`.
8. Reject non-monotonic timestamps, unless a future explicit decision allows sorting.
9. Reject bad OHLC rows where high is below open, low, or close, or low is above open, high, or close.
10. Reject non-positive OHLC prices.
11. Reject negative volume.
12. Report missing minutes, but not automatically fail on missing minutes.

Reason for rule 12:

The tiny XAUUSD sample from 2024-01-03 had 60 missing minutes beginning at
22:00 UTC. This may be a normal daily metals trading break, but that is not yet
proven. Missing minutes should therefore be measured and reported before any
acceptance decision.

## Non-acceptance reminder

This inspection does not accept Dukascopy as a research source.

Dukascopy remains only the first external M1 source candidate under evaluation.

Do not use Dukascopy data as H017 validation evidence until a tested loader,
multi-day coverage inspection, provenance notes, and mismatch risks are
documented.
