from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
import hashlib
import json

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


_CACHE_SCHEMA_VERSION = 1


def build_common_complete_bridge_window_cache_key(
    *,
    source_paths: Mapping[str, str | Path],
    expected_m1_bars_per_h4: int = 240,
    expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
) -> str:
    """Build a deterministic cache key from strict bridge-window inputs.

    The key intentionally uses source file path, byte size, and mtime_ns instead
    of hashing large broker CSVs. This keeps the check cheap while invalidating
    when MT5 exports are replaced or edited.
    """
    source_fingerprints = []
    for label, raw_path in sorted(source_paths.items()):
        path = Path(raw_path).resolve()
        stat = path.stat()
        source_fingerprints.append(
            {
                "label": label,
                "path": str(path),
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        )

    payload = {
        "schema_version": _CACHE_SCHEMA_VERSION,
        "source_fingerprints": source_fingerprints,
        "expected_m1_bars_per_h4": int(expected_m1_bars_per_h4),
        "expected_h4_delta_seconds": float(expected_h4_delta.total_seconds()),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_common_complete_bridge_window_assessment_cache(
    *,
    cache_path: str | Path,
    cache_key: str,
) -> CommonCompleteBridgeWindowAssessment | None:
    """Load a cached strict bridge-window assessment, or return None on miss.

    Corrupt, stale, or schema-mismatched caches are treated as misses so callers
    recompute from broker-native data instead of trusting ambiguous state.
    """
    path = Path(cache_path)
    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != _CACHE_SCHEMA_VERSION:
            return None
        if payload.get("cache_key") != cache_key:
            return None

        assessment_payload = payload["assessment"]
        accepted_timestamps = pd.DatetimeIndex(
            [pd.Timestamp(value).tz_convert("UTC") for value in assessment_payload["accepted_timestamps"]],
            tz="UTC",
        )
        rejection_counts = tuple(
            BridgeWindowRejectionCount(
                reason=str(item["reason"]),
                count=int(item["count"]),
            )
            for item in assessment_payload["rejection_counts"]
        )

        first_accepted_timestamp = (
            accepted_timestamps[0] if len(accepted_timestamps) else None
        )
        last_accepted_timestamp = (
            accepted_timestamps[-1] if len(accepted_timestamps) else None
        )

        return CommonCompleteBridgeWindowAssessment(
            accepted_timestamps=accepted_timestamps,
            accepted_count=int(assessment_payload["accepted_count"]),
            first_accepted_timestamp=first_accepted_timestamp,
            last_accepted_timestamp=last_accepted_timestamp,
            candidate_common_h4_count=int(assessment_payload["candidate_common_h4_count"]),
            usdjpy_complete_count=int(assessment_payload["usdjpy_complete_count"]),
            xauusd_complete_count=int(assessment_payload["xauusd_complete_count"]),
            common_complete_count=int(assessment_payload["common_complete_count"]),
            usdjpy_only_complete_count=int(assessment_payload["usdjpy_only_complete_count"]),
            xauusd_only_complete_count=int(assessment_payload["xauusd_only_complete_count"]),
            rejected_count=int(assessment_payload["rejected_count"]),
            rejection_counts=rejection_counts,
        )
    except Exception:
        return None


def write_common_complete_bridge_window_assessment_cache(
    *,
    cache_path: str | Path,
    cache_key: str,
    assessment: CommonCompleteBridgeWindowAssessment,
) -> None:
    """Atomically write a strict bridge-window assessment cache as JSON."""
    path = Path(cache_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": _CACHE_SCHEMA_VERSION,
        "cache_key": cache_key,
        "assessment": {
            "accepted_timestamps": [
                pd.Timestamp(timestamp).tz_convert("UTC").isoformat()
                for timestamp in assessment.accepted_timestamps
            ],
            "accepted_count": assessment.accepted_count,
            "candidate_common_h4_count": assessment.candidate_common_h4_count,
            "usdjpy_complete_count": assessment.usdjpy_complete_count,
            "xauusd_complete_count": assessment.xauusd_complete_count,
            "common_complete_count": assessment.common_complete_count,
            "usdjpy_only_complete_count": assessment.usdjpy_only_complete_count,
            "xauusd_only_complete_count": assessment.xauusd_only_complete_count,
            "rejected_count": assessment.rejected_count,
            "rejection_counts": [
                {"reason": item.reason, "count": item.count}
                for item in assessment.rejection_counts
            ],
        },
    }

    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(path)


def assess_common_complete_h4_m1_windows_cached(
    *,
    cache_path: str | Path,
    cache_key: str,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    expected_m1_bars_per_h4: int = 240,
    expected_h4_delta: pd.Timedelta = pd.Timedelta(hours=4),
) -> CommonCompleteBridgeWindowAssessment:
    """Load cached strict bridge-window assessment or compute and persist it."""
    cached = load_common_complete_bridge_window_assessment_cache(
        cache_path=cache_path,
        cache_key=cache_key,
    )
    if cached is not None:
        return cached

    assessment = assess_common_complete_h4_m1_windows(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        expected_m1_bars_per_h4=expected_m1_bars_per_h4,
        expected_h4_delta=expected_h4_delta,
    )
    write_common_complete_bridge_window_assessment_cache(
        cache_path=cache_path,
        cache_key=cache_key,
        assessment=assessment,
    )
    return assessment
