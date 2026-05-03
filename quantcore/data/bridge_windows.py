from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


_REQUIRED_OHLC_COLUMNS = ("open", "high", "low", "close")


@dataclass(frozen=True)
class BridgeWindowRejectionCount:
    """Count one explicit reason strict H4/M1 bridge windows were rejected."""

    reason: str
    count: int


@dataclass(frozen=True)
class CommonCompleteBridgeWindowAssessment:
    """Audit strict common H4/M1 bridge windows before event-driven validation.

    A timestamp is accepted only when both symbols have the H4 timestamp, both
    symbols have the next H4 timestamp exactly four hours later, and both symbols
    have exactly the expected number of M1 bars in [timestamp, timestamp + 4h).
    """

    accepted_timestamps: pd.DatetimeIndex
    accepted_count: int
    first_accepted_timestamp: pd.Timestamp | None
    last_accepted_timestamp: pd.Timestamp | None
    candidate_common_h4_count: int
    usdjpy_complete_count: int
    xauusd_complete_count: int
    common_complete_count: int
    usdjpy_only_complete_count: int
    xauusd_only_complete_count: int
    rejected_count: int
    rejection_counts: tuple[BridgeWindowRejectionCount, ...]


def _require_utc_datetime_index(frame: pd.DataFrame, *, label: str) -> pd.DatetimeIndex:
    """Validate loaded OHLC data indexes before strict bridge-window filtering."""

    if not isinstance(frame, pd.DataFrame):
        raise TypeError(f"{label} must be a pandas DataFrame.")

    index = frame.index
    if not isinstance(index, pd.DatetimeIndex):
        raise TypeError(f"{label} must have a pandas DatetimeIndex.")

    if index.tz is None:
        raise ValueError(f"{label} index must be timezone-aware UTC.")

    probe = pd.Timestamp("2024-01-01 00:00:00", tz=index.tz)
    if probe.utcoffset() != pd.Timedelta(0):
        raise ValueError(f"{label} index must be UTC, got timezone {index.tz!r}.")

    if index.has_duplicates:
        raise ValueError(f"{label} index must not contain duplicate timestamps.")

    if not index.is_monotonic_increasing:
        raise ValueError(f"{label} index must be sorted ascending.")

    missing_columns = tuple(column for column in _REQUIRED_OHLC_COLUMNS if column not in frame.columns)
    if missing_columns:
        raise ValueError(
            f"{label} must contain OHLC columns {_REQUIRED_OHLC_COLUMNS}; "
            f"missing {missing_columns}."
        )

    return index


def _m1_count_in_window(
    m1_index: pd.DatetimeIndex,
    *,
    start: pd.Timestamp,
    expected_h4_delta: pd.Timedelta,
) -> int:
    """Count M1 bars in [start, start + expected_h4_delta) without imputing."""

    end = start + expected_h4_delta
    start_position = m1_index.searchsorted(start, side="left")
    end_position = m1_index.searchsorted(end, side="left")
    return int(end_position - start_position)


def _has_exact_next_h4_delta(
    h4_index: pd.DatetimeIndex,
    *,
    timestamp: pd.Timestamp,
    expected_h4_delta: pd.Timedelta,
) -> tuple[bool, str | None]:
    """Check whether the next native H4 timestamp is exactly one H4 interval later."""

    location = h4_index.get_loc(timestamp)
    if not isinstance(location, int):
        raise ValueError("H4 indexes must be unique before bridge-window assessment.")

    next_location = location + 1
    if next_location >= len(h4_index):
        return False, "missing_next_h4_timestamp"

    next_timestamp = h4_index[next_location]
    if next_timestamp - timestamp != expected_h4_delta:
        return False, "non_4h_next_h4_delta"

    return True, None


def _assess_symbol_window(
    *,
    symbol_label: str,
    h4_index: pd.DatetimeIndex,
    m1_index: pd.DatetimeIndex,
    timestamp: pd.Timestamp,
    expected_m1_bars_per_h4: int,
    expected_h4_delta: pd.Timedelta,
) -> tuple[bool, tuple[str, ...]]:
    """Assess one symbol for one candidate H4 bridge timestamp."""

    reasons: list[str] = []

    has_next_h4, h4_reason = _has_exact_next_h4_delta(
        h4_index,
        timestamp=timestamp,
        expected_h4_delta=expected_h4_delta,
    )
    if not has_next_h4 and h4_reason is not None:
        reasons.append(f"{symbol_label}_{h4_reason}")

    m1_count = _m1_count_in_window(
        m1_index,
        start=timestamp,
        expected_h4_delta=expected_h4_delta,
    )
    if m1_count != expected_m1_bars_per_h4:
        reasons.append(f"{symbol_label}_m1_count_not_expected")

    return not reasons, tuple(reasons)


def _rejection_counts(reasons: list[str]) -> tuple[BridgeWindowRejectionCount, ...]:
    """Return deterministic rejection reason counts for operational audit logs."""

    counts: dict[str, int] = {}
    for reason in reasons:
        counts[reason] = counts.get(reason, 0) + 1

    return tuple(
        BridgeWindowRejectionCount(reason=reason, count=counts[reason])
        for reason in sorted(counts)
    )


def assess_common_complete_h4_m1_windows(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    expected_m1_bars_per_h4: int = 240,
    expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
) -> CommonCompleteBridgeWindowAssessment:
    """Find strict common complete H4/M1 bridge windows for USDJPY and XAUUSD.

    This function is intentionally pure: it accepts already-loaded dataframes,
    writes no files, performs no imputation, and returns accepted timestamps plus
    diagnostics. It is a preflight/filter for future event-driven H017 validation,
    not a strategy runner.
    """

    if expected_m1_bars_per_h4 <= 0:
        raise ValueError(
            "expected_m1_bars_per_h4 must be > 0, "
            f"got {expected_m1_bars_per_h4}."
        )
    if expected_h4_delta <= pd.Timedelta(0):
        raise ValueError(
            f"expected_h4_delta must be positive, got {expected_h4_delta}."
        )

    usdjpy_h4_index = _require_utc_datetime_index(usdjpy_h4, label="usdjpy_h4")
    xauusd_h4_index = _require_utc_datetime_index(xauusd_h4, label="xauusd_h4")
    usdjpy_m1_index = _require_utc_datetime_index(usdjpy_m1, label="usdjpy_m1")
    xauusd_m1_index = _require_utc_datetime_index(xauusd_m1, label="xauusd_m1")

    candidate_common_h4 = usdjpy_h4_index.intersection(xauusd_h4_index).sort_values()

    usdjpy_complete: set[pd.Timestamp] = set()
    xauusd_complete: set[pd.Timestamp] = set()
    all_rejection_reasons: list[str] = []

    for timestamp in candidate_common_h4:
        usdjpy_is_complete, usdjpy_reasons = _assess_symbol_window(
            symbol_label="usdjpy",
            h4_index=usdjpy_h4_index,
            m1_index=usdjpy_m1_index,
            timestamp=timestamp,
            expected_m1_bars_per_h4=expected_m1_bars_per_h4,
            expected_h4_delta=expected_h4_delta,
        )
        xauusd_is_complete, xauusd_reasons = _assess_symbol_window(
            symbol_label="xauusd",
            h4_index=xauusd_h4_index,
            m1_index=xauusd_m1_index,
            timestamp=timestamp,
            expected_m1_bars_per_h4=expected_m1_bars_per_h4,
            expected_h4_delta=expected_h4_delta,
        )

        if usdjpy_is_complete:
            usdjpy_complete.add(timestamp)
        else:
            all_rejection_reasons.extend(usdjpy_reasons)

        if xauusd_is_complete:
            xauusd_complete.add(timestamp)
        else:
            all_rejection_reasons.extend(xauusd_reasons)

    accepted = sorted(usdjpy_complete.intersection(xauusd_complete))
    accepted_timestamps = pd.DatetimeIndex(accepted, tz="UTC")

    first_accepted_timestamp = (
        accepted_timestamps[0] if len(accepted_timestamps) else None
    )
    last_accepted_timestamp = (
        accepted_timestamps[-1] if len(accepted_timestamps) else None
    )

    return CommonCompleteBridgeWindowAssessment(
        accepted_timestamps=accepted_timestamps,
        accepted_count=len(accepted_timestamps),
        first_accepted_timestamp=first_accepted_timestamp,
        last_accepted_timestamp=last_accepted_timestamp,
        candidate_common_h4_count=len(candidate_common_h4),
        usdjpy_complete_count=len(usdjpy_complete),
        xauusd_complete_count=len(xauusd_complete),
        common_complete_count=len(accepted_timestamps),
        usdjpy_only_complete_count=len(usdjpy_complete - xauusd_complete),
        xauusd_only_complete_count=len(xauusd_complete - usdjpy_complete),
        rejected_count=len(candidate_common_h4) - len(accepted_timestamps),
        rejection_counts=_rejection_counts(all_rejection_reasons),
    )
