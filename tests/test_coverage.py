from __future__ import annotations

import pandas as pd
import pytest

from quantcore.data.coverage import CoverageAssessment, assess_m1_research_coverage


def test_assess_m1_research_coverage_flags_short_recent_sample() -> None:
    result = assess_m1_research_coverage(
        desired_m1_start_utc=pd.Timestamp("2021-07-02 00:00:00", tz="UTC"),
        actual_common_start_utc=pd.Timestamp("2026-01-26 03:09:00", tz="UTC"),
        actual_common_end_utc=pd.Timestamp("2026-04-29 09:00:00", tz="UTC"),
        n_common_h4_bars=411,
        minimum_research_h4_bars=1512,
    )

    assert isinstance(result, CoverageAssessment)
    assert result.meets_desired_m1_start is False
    assert result.has_minimum_h4_bars is False
    assert result.research_sufficient is False
    assert len(result.reasons) == 2
    assert "M1 common start is later" in result.reasons[0]
    assert "Common H4 sample is shorter" in result.reasons[1]


def test_assess_m1_research_coverage_passes_when_start_and_bars_are_sufficient() -> None:
    result = assess_m1_research_coverage(
        desired_m1_start_utc=pd.Timestamp("2021-07-02 00:00:00", tz="UTC"),
        actual_common_start_utc=pd.Timestamp("2021-07-02 00:00:00", tz="UTC"),
        actual_common_end_utc=pd.Timestamp("2026-04-29 09:00:00", tz="UTC"),
        n_common_h4_bars=7719,
        minimum_research_h4_bars=1512,
    )

    assert result.meets_desired_m1_start is True
    assert result.has_minimum_h4_bars is True
    assert result.research_sufficient is True
    assert result.reasons == (
        "M1 coverage is sufficient for a first research-grade event validation pass.",
    )


def test_assess_m1_research_coverage_allows_early_m1_start() -> None:
    result = assess_m1_research_coverage(
        desired_m1_start_utc=pd.Timestamp("2021-07-02 00:00:00", tz="UTC"),
        actual_common_start_utc=pd.Timestamp("2020-01-01 00:00:00", tz="UTC"),
        actual_common_end_utc=pd.Timestamp("2026-04-29 09:00:00", tz="UTC"),
        n_common_h4_bars=9000,
        minimum_research_h4_bars=1512,
    )

    assert result.meets_desired_m1_start is True
    assert result.research_sufficient is True


def test_assess_m1_research_coverage_localizes_naive_timestamps_to_utc() -> None:
    result = assess_m1_research_coverage(
        desired_m1_start_utc="2021-07-02 00:00:00",
        actual_common_start_utc="2021-07-02 00:00:00",
        actual_common_end_utc="2022-07-02 00:00:00",
        n_common_h4_bars=1512,
        minimum_research_h4_bars=1512,
    )

    assert str(result.desired_m1_start_utc.tz) == "UTC"
    assert str(result.actual_common_start_utc.tz) == "UTC"
    assert str(result.actual_common_end_utc.tz) == "UTC"


def test_assess_m1_research_coverage_converts_aware_timestamps_to_utc() -> None:
    result = assess_m1_research_coverage(
        desired_m1_start_utc=pd.Timestamp("2021-07-02 03:00:00", tz="Europe/Athens"),
        actual_common_start_utc=pd.Timestamp("2021-07-02 03:00:00", tz="Europe/Athens"),
        actual_common_end_utc=pd.Timestamp("2022-07-02 03:00:00", tz="Europe/Athens"),
        n_common_h4_bars=1512,
        minimum_research_h4_bars=1512,
    )

    assert result.desired_m1_start_utc == pd.Timestamp("2021-07-02 00:00:00", tz="UTC")
    assert result.actual_common_start_utc == pd.Timestamp("2021-07-02 00:00:00", tz="UTC")


def test_assess_m1_research_coverage_rejects_negative_bar_count() -> None:
    with pytest.raises(ValueError, match="n_common_h4_bars must be >= 0"):
        assess_m1_research_coverage(
            desired_m1_start_utc=pd.Timestamp("2021-07-02 00:00:00", tz="UTC"),
            actual_common_start_utc=pd.Timestamp("2021-07-02 00:00:00", tz="UTC"),
            actual_common_end_utc=pd.Timestamp("2022-07-02 00:00:00", tz="UTC"),
            n_common_h4_bars=-1,
            minimum_research_h4_bars=1512,
        )


def test_assess_m1_research_coverage_rejects_empty_or_reversed_window() -> None:
    with pytest.raises(ValueError, match="must be earlier"):
        assess_m1_research_coverage(
            desired_m1_start_utc=pd.Timestamp("2021-07-02 00:00:00", tz="UTC"),
            actual_common_start_utc=pd.Timestamp("2022-07-02 00:00:00", tz="UTC"),
            actual_common_end_utc=pd.Timestamp("2022-07-02 00:00:00", tz="UTC"),
            n_common_h4_bars=1512,
            minimum_research_h4_bars=1512,
        )
