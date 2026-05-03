"""Tests for quantcore.data.dukascopy_loader.

The real Dukascopy sample CSVs are under /data/raw/ and are gitignored, so
these tests use tiny synthetic CSV files written to tmp_path.
"""
from __future__ import annotations

from pathlib import Path

import dataclasses

import pandas as pd
import pytest

from quantcore.data.dukascopy_loader import (
    DukascopyLoadResult,
    load_dukascopy_csv,
)


_DUKASCOPY_HEADER = "UTC,Open,High,Low,Close,Volume"


def _write_dukascopy_csv(path: Path, rows: list[str], *, header: str = _DUKASCOPY_HEADER) -> None:
    """Write a tiny Dukascopy-format CSV file."""

    path.write_text(header + "\n" + "\n".join(rows) + "\n", encoding="utf-8")


def test_load_dukascopy_csv_returns_result(tmp_path: Path) -> None:
    csv = tmp_path / "USD-JPY_Minute_2024-01-03_UTC.csv"
    _write_dukascopy_csv(
        csv,
        [
            "03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,123",
            "03.01.2024 00:01:00.000 UTC,142.050,142.200,142.000,142.150,124",
        ],
    )

    result = load_dukascopy_csv(csv)

    assert isinstance(result, DukascopyLoadResult)
    assert result.n_input_rows == 2
    assert result.n_bars == 2


def test_load_dukascopy_csv_outputs_canonical_columns_and_utc_index(tmp_path: Path) -> None:
    csv = tmp_path / "x.csv"
    _write_dukascopy_csv(
        csv,
        ["03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,123"],
    )

    result = load_dukascopy_csv(csv)

    assert list(result.bars.columns) == ["open", "high", "low", "close", "volume"]
    assert result.bars.index[0] == pd.Timestamp("2024-01-03 00:00:00", tz="UTC")
    assert str(result.bars.index.tz) == "UTC"


def test_load_dukascopy_csv_metadata_matches_data(tmp_path: Path) -> None:
    csv = tmp_path / "x.csv"
    _write_dukascopy_csv(
        csv,
        [
            "03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,123",
            "03.01.2024 00:01:00.000 UTC,142.050,142.200,142.000,142.150,124",
        ],
    )

    result = load_dukascopy_csv(csv)

    assert result.earliest_utc == pd.Timestamp("2024-01-03 00:00:00", tz="UTC")
    assert result.latest_utc == pd.Timestamp("2024-01-03 00:01:00", tz="UTC")
    assert result.n_missing_minutes == 0
    assert result.missing_minutes == ()


def test_load_dukascopy_csv_rejects_missing_required_column(tmp_path: Path) -> None:
    csv = tmp_path / "broken.csv"
    bad_header = "UTC,Open,High,Low,Close"
    _write_dukascopy_csv(
        csv,
        ["03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050"],
        header=bad_header,
    )

    with pytest.raises(ValueError, match="missing required columns"):
        load_dukascopy_csv(csv)


def test_load_dukascopy_csv_rejects_duplicate_timestamps(tmp_path: Path) -> None:
    csv = tmp_path / "duplicate.csv"
    _write_dukascopy_csv(
        csv,
        [
            "03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,123",
            "03.01.2024 00:00:00.000 UTC,142.050,142.200,142.000,142.150,124",
        ],
    )

    with pytest.raises(ValueError, match="duplicate timestamps"):
        load_dukascopy_csv(csv)


def test_load_dukascopy_csv_rejects_non_monotonic_timestamps(tmp_path: Path) -> None:
    csv = tmp_path / "unsorted.csv"
    _write_dukascopy_csv(
        csv,
        [
            "03.01.2024 00:01:00.000 UTC,142.050,142.200,142.000,142.150,124",
            "03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,123",
        ],
    )

    with pytest.raises(ValueError, match="non-monotonic timestamps"):
        load_dukascopy_csv(csv)


def test_load_dukascopy_csv_rejects_bad_ohlc_rows(tmp_path: Path) -> None:
    csv = tmp_path / "bad_ohlc.csv"
    _write_dukascopy_csv(
        csv,
        ["03.01.2024 00:00:00.000 UTC,142.000,141.000,141.900,142.050,123"],
    )

    with pytest.raises(ValueError, match="bad OHLC"):
        load_dukascopy_csv(csv)


def test_load_dukascopy_csv_rejects_non_positive_prices(tmp_path: Path) -> None:
    csv = tmp_path / "bad_price.csv"
    _write_dukascopy_csv(
        csv,
        ["03.01.2024 00:00:00.000 UTC,0.000,142.100,141.900,142.050,123"],
    )

    with pytest.raises(ValueError, match="non-positive OHLC prices"):
        load_dukascopy_csv(csv)


def test_load_dukascopy_csv_rejects_negative_volume(tmp_path: Path) -> None:
    csv = tmp_path / "bad_volume.csv"
    _write_dukascopy_csv(
        csv,
        ["03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,-1"],
    )

    with pytest.raises(ValueError, match="negative volume"):
        load_dukascopy_csv(csv)


def test_load_dukascopy_csv_allows_zero_volume(tmp_path: Path) -> None:
    csv = tmp_path / "zero_volume.csv"
    _write_dukascopy_csv(
        csv,
        ["03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,0"],
    )

    result = load_dukascopy_csv(csv)

    assert result.bars["volume"].iloc[0] == 0.0


def test_load_dukascopy_csv_reports_missing_minutes_without_failing(tmp_path: Path) -> None:
    csv = tmp_path / "gap.csv"
    _write_dukascopy_csv(
        csv,
        [
            "03.01.2024 00:00:00.000 UTC,142.000,142.100,141.900,142.050,123",
            "03.01.2024 00:02:00.000 UTC,142.050,142.200,142.000,142.150,124",
        ],
    )

    result = load_dukascopy_csv(csv)

    assert result.n_missing_minutes == 1
    assert result.missing_minutes == (
        pd.Timestamp("2024-01-03 00:01:00", tz="UTC"),
    )


def test_dukascopy_load_result_is_frozen() -> None:
    result = DukascopyLoadResult(
        bars=pd.DataFrame(),
        n_bars=0,
        n_input_rows=0,
        earliest_utc=pd.Timestamp("2024-01-01", tz="UTC"),
        latest_utc=pd.Timestamp("2024-01-01", tz="UTC"),
        n_missing_minutes=0,
        missing_minutes=(),
    )

    with pytest.raises(dataclasses.FrozenInstanceError):
        result.n_bars = 999  # type: ignore[misc]
