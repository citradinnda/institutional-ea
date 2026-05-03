"""Tests for quantcore.data.histdata_loader.

The real HistData CSV files are under /data/raw/ and are gitignored, so these
tests use tiny synthetic CSV files written to tmp_path.
"""
from __future__ import annotations

from pathlib import Path

import dataclasses

import pandas as pd
import pytest

from quantcore.data.histdata_loader import (
    HistDataM1LoadResult,
    load_histdata_m1_csv,
)


def _write_histdata_csv(path: Path, rows: list[str]) -> None:
    """Write a tiny observed HistData M1 no-header CSV file."""

    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def test_load_histdata_m1_csv_returns_result(tmp_path: Path) -> None:
    csv = tmp_path / "USDJPY_2021_2025_Raw_HistData.csv"
    _write_histdata_csv(
        csv,
        [
            "2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0",
            "2021.01.03,17:01,103.161000,103.161000,103.160000,103.161000,0",
        ],
    )

    result = load_histdata_m1_csv(csv)

    assert isinstance(result, HistDataM1LoadResult)
    assert result.n_input_rows == 2
    assert result.n_bars == 2


def test_load_histdata_m1_csv_outputs_canonical_columns_and_utc_index(
    tmp_path: Path,
) -> None:
    csv = tmp_path / "x.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0"],
    )

    result = load_histdata_m1_csv(csv)

    assert list(result.bars.columns) == ["open", "high", "low", "close", "volume"]
    assert result.bars.index[0] == pd.Timestamp("2021-01-03 17:00:00", tz="UTC")
    assert str(result.bars.index.tz) == "UTC"


def test_load_histdata_m1_csv_metadata_matches_data(tmp_path: Path) -> None:
    csv = tmp_path / "x.csv"
    _write_histdata_csv(
        csv,
        [
            "2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0",
            "2021.01.03,17:01,103.161000,103.161000,103.160000,103.161000,0",
        ],
    )

    result = load_histdata_m1_csv(csv)

    assert result.earliest_utc == pd.Timestamp("2021-01-03 17:00:00", tz="UTC")
    assert result.latest_utc == pd.Timestamp("2021-01-03 17:01:00", tz="UTC")
    assert result.source_tz == "UTC"
    assert result.n_missing_minutes == 0
    assert result.missing_minutes == ()


def test_load_histdata_m1_csv_converts_explicit_source_timezone_to_utc(
    tmp_path: Path,
) -> None:
    csv = tmp_path / "x.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0"],
    )

    result = load_histdata_m1_csv(csv, source_tz="Etc/GMT-2")

    assert result.earliest_utc == pd.Timestamp("2021-01-03 15:00:00", tz="UTC")
    assert result.latest_utc == pd.Timestamp("2021-01-03 15:00:00", tz="UTC")
    assert result.source_tz == "Etc/GMT-2"


def test_load_histdata_m1_csv_rejects_wrong_column_count(tmp_path: Path) -> None:
    csv = tmp_path / "broken.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000"],
    )

    with pytest.raises(ValueError, match="expected 7 columns"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_rejects_bad_timestamp_format(tmp_path: Path) -> None:
    csv = tmp_path / "bad_timestamp.csv"
    _write_histdata_csv(
        csv,
        ["2021-01-03,17:00,103.097000,103.160000,103.097000,103.160000,0"],
    )

    with pytest.raises(ValueError, match="timestamps that do not match"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_rejects_duplicate_timestamps(tmp_path: Path) -> None:
    csv = tmp_path / "duplicate.csv"
    _write_histdata_csv(
        csv,
        [
            "2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0",
            "2021.01.03,17:00,103.161000,103.161000,103.160000,103.161000,0",
        ],
    )

    with pytest.raises(ValueError, match="duplicate timestamps"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_rejects_non_monotonic_timestamps(
    tmp_path: Path,
) -> None:
    csv = tmp_path / "unsorted.csv"
    _write_histdata_csv(
        csv,
        [
            "2021.01.03,17:01,103.161000,103.161000,103.160000,103.161000,0",
            "2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0",
        ],
    )

    with pytest.raises(ValueError, match="non-monotonic timestamps"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_rejects_bad_ohlc_rows(tmp_path: Path) -> None:
    csv = tmp_path / "bad_ohlc.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,103.097000,103.000000,103.097000,103.160000,0"],
    )

    with pytest.raises(ValueError, match="bad OHLC"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_rejects_non_positive_prices(tmp_path: Path) -> None:
    csv = tmp_path / "bad_price.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,0.000000,103.160000,103.097000,103.160000,0"],
    )

    with pytest.raises(ValueError, match="non-positive OHLC prices"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_rejects_non_numeric_ohlcv(tmp_path: Path) -> None:
    csv = tmp_path / "bad_numeric.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,not-a-price,103.160000,103.097000,103.160000,0"],
    )

    with pytest.raises(ValueError, match="non-numeric values"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_rejects_negative_volume(tmp_path: Path) -> None:
    csv = tmp_path / "bad_volume.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,-1"],
    )

    with pytest.raises(ValueError, match="negative volume"):
        load_histdata_m1_csv(csv)


def test_load_histdata_m1_csv_allows_zero_volume(tmp_path: Path) -> None:
    csv = tmp_path / "zero_volume.csv"
    _write_histdata_csv(
        csv,
        ["2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0"],
    )

    result = load_histdata_m1_csv(csv)

    assert result.bars["volume"].iloc[0] == 0.0


def test_load_histdata_m1_csv_reports_missing_minutes_without_failing(
    tmp_path: Path,
) -> None:
    csv = tmp_path / "gap.csv"
    _write_histdata_csv(
        csv,
        [
            "2021.01.03,17:00,103.097000,103.160000,103.097000,103.160000,0",
            "2021.01.03,17:02,103.161000,103.161000,103.160000,103.161000,0",
        ],
    )

    result = load_histdata_m1_csv(csv)

    assert result.n_missing_minutes == 1
    assert result.missing_minutes == (
        pd.Timestamp("2021-01-03 17:01:00", tz="UTC"),
    )


def test_histdata_m1_load_result_is_frozen() -> None:
    result = HistDataM1LoadResult(
        bars=pd.DataFrame(),
        n_bars=0,
        n_input_rows=0,
        earliest_utc=pd.Timestamp("2021-01-01", tz="UTC"),
        latest_utc=pd.Timestamp("2021-01-01", tz="UTC"),
        source_tz="UTC",
        n_missing_minutes=0,
        missing_minutes=(),
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        result.n_bars = 999  # type: ignore[misc]
