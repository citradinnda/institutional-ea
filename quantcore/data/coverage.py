from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CoverageAssessment:
    """Make data sufficiency explicit so a short smoke run is never mistaken for validation."""

    desired_m1_start_utc: pd.Timestamp
    actual_common_start_utc: pd.Timestamp
    actual_common_end_utc: pd.Timestamp
    n_common_h4_bars: int
    minimum_research_h4_bars: int
    meets_desired_m1_start: bool
    has_minimum_h4_bars: bool
    research_sufficient: bool
    reasons: tuple[str, ...]


def _as_utc_timestamp(value: object, *, field_name: str) -> pd.Timestamp:
    """Normalize user-facing timestamps because coverage comparisons must be timezone-safe."""

    timestamp = pd.Timestamp(value)
    if pd.isna(timestamp):
        raise ValueError(f"{field_name} must be a valid timestamp, got {value!r}.")

    if timestamp.tzinfo is None:
        return timestamp.tz_localize("UTC")

    return timestamp.tz_convert("UTC")


def assess_m1_research_coverage(
    *,
    desired_m1_start_utc: object,
    actual_common_start_utc: object,
    actual_common_end_utc: object,
    n_common_h4_bars: int,
    minimum_research_h4_bars: int,
) -> CoverageAssessment:
    """Separate an operational M1 smoke pass from enough history for research validation."""

    if n_common_h4_bars < 0:
        raise ValueError(f"n_common_h4_bars must be >= 0, got {n_common_h4_bars}.")
    if minimum_research_h4_bars <= 0:
        raise ValueError(
            f"minimum_research_h4_bars must be > 0, got {minimum_research_h4_bars}."
        )

    desired_start = _as_utc_timestamp(
        desired_m1_start_utc,
        field_name="desired_m1_start_utc",
    )
    actual_start = _as_utc_timestamp(
        actual_common_start_utc,
        field_name="actual_common_start_utc",
    )
    actual_end = _as_utc_timestamp(
        actual_common_end_utc,
        field_name="actual_common_end_utc",
    )

    if actual_start >= actual_end:
        raise ValueError(
            "actual_common_start_utc must be earlier than actual_common_end_utc. "
            f"start={actual_start}, end={actual_end}"
        )

    meets_desired_m1_start = actual_start <= desired_start
    has_minimum_h4_bars = n_common_h4_bars >= minimum_research_h4_bars

    reasons: list[str] = []
    if not meets_desired_m1_start:
        reasons.append(
            "M1 common start is later than the desired clean H4 start. "
            f"desired={desired_start}, actual={actual_start}"
        )
    if not has_minimum_h4_bars:
        reasons.append(
            "Common H4 sample is shorter than one approximate H4 trading year. "
            f"minimum={minimum_research_h4_bars}, actual={n_common_h4_bars}"
        )

    research_sufficient = meets_desired_m1_start and has_minimum_h4_bars

    if research_sufficient:
        reasons.append("M1 coverage is sufficient for a first research-grade event validation pass.")

    return CoverageAssessment(
        desired_m1_start_utc=desired_start,
        actual_common_start_utc=actual_start,
        actual_common_end_utc=actual_end,
        n_common_h4_bars=n_common_h4_bars,
        minimum_research_h4_bars=minimum_research_h4_bars,
        meets_desired_m1_start=meets_desired_m1_start,
        has_minimum_h4_bars=has_minimum_h4_bars,
        research_sufficient=research_sufficient,
        reasons=tuple(reasons),
    )
