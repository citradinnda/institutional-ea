"""Tests for quantcore.data.mt5_loader.

WHY synthetic fixtures via tmp_path: the real MT5 CSVs are gitignored
(under /data/raw/), so tests cannot depend on them. Each test writes a
tiny tab-separated string with the exact MT5 header format, exercising
one invariant at a time.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from quantcore.data.loaders import _ensure_canonical, ensure_canonical
from quantcore.data.mt5_loader import (
    DEFAULT_BROKER_TZ,
    MT5LoadResult,
    load_mt5_csv,
)


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

_MT5_HEADER = (
    "<DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<CLOSE>\t<TICKVOL>\t<VOL>\t<SPREAD>"
)


def _write_mt5_csv(path: Path, rows: list[str]) -> None:
    """Write a tab-separated MT5-format CSV with the standard header."""
    content = _MT5_HEADER + "\n" + "\n".join(rows) + "\n"
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Public-alias sanity
# ---------------------------------------------------------------------------

def test_ensure_canonical_public_alias_is_identity():
    """Phase 2.6a promoted _ensure_canonical to public ensure_canonical."""
    assert ensure_canonical is _ensure_canonical


# ---------------------------------------------------------------------------
# 2. Result type and shape
# ---------------------------------------------------------------------------

def test_load_mt5_csv_returns_mt5_load_result(tmp_path):
    csv = tmp_path / "USDJPY_H4.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
        "2024.06.03\t04:00:00\t156.200\t156.300\t155.900\t156.000\t1100\t0\t10",
    ])
    result = load_mt5_csv(csv)
    assert isinstance(result, MT5LoadResult)
    assert result.n_bars == 2
    assert result.n_input_rows == 2


def test_load_mt5_csv_canonical_columns_only(tmp_path):
    """Output frame must have exactly the canonical OHLCV columns, in order."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
    ])
    result = load_mt5_csv(csv)
    assert list(result.bars.columns) == ["open", "high", "low", "close", "volume"]


def test_load_mt5_csv_drops_vol_and_spread(tmp_path):
    """<VOL> and <SPREAD> must NOT appear in the canonical frame."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
    ])
    result = load_mt5_csv(csv)
    assert "vol" not in result.bars.columns
    assert "spread" not in result.bars.columns
    assert "<VOL>" not in result.bars.columns
    assert "<SPREAD>" not in result.bars.columns


# ---------------------------------------------------------------------------
# 3. Volume mapping
# ---------------------------------------------------------------------------

def test_load_mt5_csv_maps_tickvol_to_volume(tmp_path):
    """<TICKVOL> values must land in the canonical 'volume' column."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1234\t0\t10",
    ])
    result = load_mt5_csv(csv)
    assert result.bars["volume"].iloc[0] == 1234.0


# ---------------------------------------------------------------------------
# 4. Timezone conversion
# ---------------------------------------------------------------------------

def test_load_mt5_csv_index_is_utc(tmp_path):
    """Index must be tz-aware UTC after loading."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
    ])
    result = load_mt5_csv(csv)
    assert result.bars.index.tz is not None
    assert str(result.bars.index.tz) == "UTC"


def test_load_mt5_csv_default_broker_tz_is_athens():
    """Default tz must be Europe/Athens (Exness convention)."""
    assert DEFAULT_BROKER_TZ == "Europe/Athens"


def test_load_mt5_csv_athens_summer_offset_is_minus_three(tmp_path):
    """A June (EEST = UTC+3) bar at broker 04:00 must land at 01:00 UTC.

    WHY: this is the load-bearing correctness check for the loader. If we
    ever revert to naive 'localize directly to UTC', this test fails by
    exactly the broker offset (3 hours in summer).
    """
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t04:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
    ])
    result = load_mt5_csv(csv)
    expected = pd.Timestamp("2024-06-03 01:00:00", tz="UTC")
    assert result.bars.index[0] == expected


def test_load_mt5_csv_athens_winter_offset_is_minus_two(tmp_path):
    """A January (EET = UTC+2) bar at broker 04:00 must land at 02:00 UTC."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.01.15\t04:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
    ])
    result = load_mt5_csv(csv)
    expected = pd.Timestamp("2024-01-15 02:00:00", tz="UTC")
    assert result.bars.index[0] == expected


def test_load_mt5_csv_explicit_utc_broker_tz_is_passthrough(tmp_path):
    """If broker_tz='UTC', wall-clock 04:00 stays at 04:00 UTC."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t04:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
    ])
    result = load_mt5_csv(csv, broker_tz="UTC")
    expected = pd.Timestamp("2024-06-03 04:00:00", tz="UTC")
    assert result.bars.index[0] == expected


# ---------------------------------------------------------------------------
# 5. Sort and dedup
# ---------------------------------------------------------------------------

def test_load_mt5_csv_sorts_ascending(tmp_path):
    """Out-of-order input rows must be sorted ascending by timestamp."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t08:00:00\t156.300\t156.400\t156.100\t156.200\t1200\t0\t10",
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
        "2024.06.03\t04:00:00\t156.200\t156.300\t155.900\t156.000\t1100\t0\t10",
    ])
    result = load_mt5_csv(csv)
    assert result.bars.index.is_monotonic_increasing
    assert result.n_bars == 3


def test_load_mt5_csv_dedups_duplicate_timestamps(tmp_path):
    """Duplicate timestamps (broker re-sync artifacts) must collapse to one row.

    n_input_rows reports the pre-dedup count; n_bars reports post-dedup.
    """
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
        "2024.06.03\t00:00:00\t156.001\t156.501\t155.801\t156.201\t1001\t0\t10",
        "2024.06.03\t04:00:00\t156.200\t156.300\t155.900\t156.000\t1100\t0\t10",
    ])
    result = load_mt5_csv(csv)
    assert result.n_input_rows == 3
    assert result.n_bars == 2


# ---------------------------------------------------------------------------
# 6. Error handling
# ---------------------------------------------------------------------------

def test_load_mt5_csv_raises_on_missing_required_column(tmp_path):
    """Missing <CLOSE> must raise ValueError, not silently produce NaN."""
    csv = tmp_path / "broken.csv"
    # Header without <CLOSE>:
    bad_header = "<DATE>\t<TIME>\t<OPEN>\t<HIGH>\t<LOW>\t<TICKVOL>\t<VOL>\t<SPREAD>"
    csv.write_text(
        bad_header + "\n"
        + "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t1000\t0\t10\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="missing required columns"):
        load_mt5_csv(csv)


# ---------------------------------------------------------------------------
# 7. Metadata fields
# ---------------------------------------------------------------------------

def test_load_mt5_csv_metadata_fields_match_data(tmp_path):
    """earliest_utc / latest_utc / broker_tz must reflect the actual frame."""
    csv = tmp_path / "x.csv"
    _write_mt5_csv(csv, [
        "2024.06.03\t00:00:00\t156.000\t156.500\t155.800\t156.200\t1000\t0\t10",
        "2024.06.03\t04:00:00\t156.200\t156.300\t155.900\t156.000\t1100\t0\t10",
        "2024.06.03\t08:00:00\t156.000\t156.400\t155.700\t156.100\t1200\t0\t10",
    ])
    result = load_mt5_csv(csv)
    # Athens summer: 00:00 -> 21:00 UTC previous day; 08:00 -> 05:00 UTC.
    assert result.earliest_utc == pd.Timestamp("2024-06-02 21:00:00", tz="UTC")
    assert result.latest_utc == pd.Timestamp("2024-06-03 05:00:00", tz="UTC")
    assert result.broker_tz == "Europe/Athens"


def test_load_mt5_csv_result_is_frozen():
    """Per §6: structured returns are @dataclass(frozen=True).

    WHY: H017Result, H017Config, H017Claim and friends are all frozen so
    callers can't accidentally mutate validation outputs. MT5LoadResult
    must follow the same convention. We verify by constructing a minimal
    instance and asserting that mutation raises FrozenInstanceError.
    """
    import dataclasses

    result = MT5LoadResult(
        bars=pd.DataFrame(),
        n_bars=0,
        n_input_rows=0,
        earliest_utc=pd.Timestamp("2024-01-01", tz="UTC"),
        latest_utc=pd.Timestamp("2024-01-01", tz="UTC"),
        broker_tz="UTC",
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.n_bars = 999  # type: ignore[misc]