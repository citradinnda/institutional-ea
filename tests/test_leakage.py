from __future__ import annotations

"""Tests for quantcore.data.leakage.

Why these tests exist
---------------------
Phase 2.6b discovered that the Exness export had ~3 years of D1 bars
mislabeled as H4. The detector that found this is now a library module;
these tests pin its behavior so future refactors can't silently regress.
"""

import pandas as pd
import pytest

from quantcore.data.leakage import (
    MIN_H4_BARS_PER_ACTIVE_DAY,
    LeakageScan,
    detect_d1_leakage,
    trim_to_common_start,
)


def _make_h4_frame(
    start_utc: str,
    n_d1_dates: int,
    n_h4_dates: int,
) -> pd.DataFrame:
    """Build a canonical OHLCV frame with `n_d1_dates` D1-disguised
    dates followed by `n_h4_dates` real H4 dates.

    D1-disguised dates: 1 bar/day. Real H4 dates: 6 bars/day. Bars are
    placed on UTC midnight + 4-hour increments. Prices are deterministic
    (constant 100.0) since the leakage detector only cares about
    timestamp density, not values.
    """
    rows: list[dict] = []
    cur = pd.Timestamp(start_utc, tz="UTC")
    # D1-disguised region: one bar per UTC date.
    for _ in range(n_d1_dates):
        rows.append(
            {"ts": cur, "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0}
        )
        cur = cur + pd.Timedelta(days=1)
    # Real H4 region: six bars per UTC date at 0/4/8/12/16/20.
    for _ in range(n_h4_dates):
        for h in (0, 4, 8, 12, 16, 20):
            ts = cur.normalize() + pd.Timedelta(hours=h)
            rows.append(
                {"ts": ts, "open": 100.0, "high": 100.0, "low": 100.0, "close": 100.0, "volume": 1.0}
            )
        cur = cur + pd.Timedelta(days=1)
    df = pd.DataFrame(rows).set_index("ts").sort_index()
    return df


def test_default_threshold_is_four() -> None:
    """The module-level constant must remain 4; downstream callers
    depend on it (Phase 2.6b script, future Phase 3 backtest)."""
    assert MIN_H4_BARS_PER_ACTIVE_DAY == 4


def test_detects_pure_d1_leakage_at_start() -> None:
    """5 D1-disguised dates followed by 10 real H4 dates should yield
    leaked_dates=5 and first_reliable_date == first H4 date."""
    df = _make_h4_frame("2024-01-01", n_d1_dates=5, n_h4_dates=10)
    scan = detect_d1_leakage(df, broker_tz="Europe/Athens")
    assert isinstance(scan, LeakageScan)
    assert scan.leaked_dates == 5
    assert scan.total_dates == 15
    # first_reliable_date is broker-local (Athens). With UTC midnight
    # bars in winter (UTC+2), 2024-01-06 00:00 UTC -> 2024-01-06 02:00
    # Athens, still calendar date 2024-01-06.
    assert scan.first_reliable_date.date() == pd.Timestamp("2024-01-06").date()
    assert scan.broker_tz == "Europe/Athens"


def test_no_leakage_when_all_h4() -> None:
    """If every date already meets the threshold, leaked_dates == 0
    and weekend_dates == 0 (no off-days in this synthetic frame)."""
    df = _make_h4_frame("2024-03-01", n_d1_dates=0, n_h4_dates=10)
    scan = detect_d1_leakage(df, broker_tz="Europe/Athens")
    assert scan.leaked_dates == 0
    assert scan.weekend_dates == 0
    assert scan.total_dates == 10


def test_raises_on_empty_frame() -> None:
    """An empty frame is a programmer error, not a silent zero result.
    The validator-style 'fail loud' convention applies here too."""
    empty = pd.DataFrame(
        columns=["open", "high", "low", "close", "volume"],
        index=pd.DatetimeIndex([], tz="UTC"),
    )
    with pytest.raises(ValueError, match="empty"):
        detect_d1_leakage(empty, broker_tz="Europe/Athens")


def test_raises_when_no_date_meets_threshold() -> None:
    """A fully D1-disguised export is unrecoverable; the detector must
    refuse to silently return a meaningless first_reliable_date."""
    df = _make_h4_frame("2024-01-01", n_d1_dates=20, n_h4_dates=0)
    with pytest.raises(ValueError, match="entire dataset"):
        detect_d1_leakage(df, broker_tz="Europe/Athens")


def test_trim_to_common_start_aligns_both_frames() -> None:
    """Both frames must drop bars strictly before the cutoff; bars at
    the exact cutoff are kept."""
    a = _make_h4_frame("2024-01-01", n_d1_dates=0, n_h4_dates=10)
    b = _make_h4_frame("2024-01-01", n_d1_dates=0, n_h4_dates=10)
    cutoff = pd.Timestamp("2024-01-05", tz="UTC")
    a_trim, b_trim = trim_to_common_start(a, b, cutoff)
    assert (a_trim.index >= cutoff).all()
    assert (b_trim.index >= cutoff).all()
    assert a_trim.index[0] == cutoff
    assert b_trim.index[0] == cutoff


def test_trim_rejects_naive_timestamp() -> None:
    """A tz-naive cutoff would silently misalign bars (one of the
    repo's recurring footguns); reject loudly."""
    a = _make_h4_frame("2024-01-01", n_d1_dates=0, n_h4_dates=5)
    b = _make_h4_frame("2024-01-01", n_d1_dates=0, n_h4_dates=5)
    naive = pd.Timestamp("2024-01-03")  # no tz
    with pytest.raises(ValueError, match="tz-aware"):
        trim_to_common_start(a, b, naive)