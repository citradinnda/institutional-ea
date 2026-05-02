from __future__ import annotations

import hashlib

import numpy as np
import pandas as pd
import pytest

from quantcore.data.checksums import (
    Checksum,
    hash_dataframe,
    hash_file,
    verify_dataframe,
    verify_file,
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _canonical_ohlcv(n: int = 50, seed: int = 0) -> pd.DataFrame:
    """Build a deterministic canonical OHLCV frame for hashing tests."""
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC", name="time")
    close = 100.0 + np.cumsum(rng.standard_normal(n) * 0.1)
    df = pd.DataFrame(
        {
            "open": close + rng.standard_normal(n) * 0.05,
            "high": close + np.abs(rng.standard_normal(n)) * 0.1,
            "low":  close - np.abs(rng.standard_normal(n)) * 0.1,
            "close": close,
            "volume": rng.integers(100, 1000, n).astype("int64"),
        },
        index=idx,
    )
    return df


# --------------------------------------------------------------------------- #
# File hashing
# --------------------------------------------------------------------------- #

def test_hash_file_matches_hashlib_reference(tmp_path):
    """Our streaming hash must equal a one-shot hashlib.sha256 of the same bytes."""
    payload = b"institutional-ea phase 1.4 checksum reference\n" * 1000
    p = tmp_path / "sample.bin"
    p.write_bytes(payload)

    expected = hashlib.sha256(payload).hexdigest()
    cs = hash_file(p)

    assert isinstance(cs, Checksum)
    assert cs.algorithm == "sha256"
    assert cs.hexdigest == expected


def test_hash_file_is_deterministic(tmp_path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"hello world")
    assert hash_file(p).hexdigest == hash_file(p).hexdigest


def test_hash_file_detects_single_byte_change(tmp_path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"hello world")
    h1 = hash_file(p).hexdigest
    p.write_bytes(b"hello worlD")  # one byte different
    h2 = hash_file(p).hexdigest
    assert h1 != h2


def test_hash_file_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        hash_file(tmp_path / "does_not_exist.bin")


def test_hash_file_handles_file_larger_than_chunk(tmp_path):
    """Files bigger than the 64KB chunk must hash the same as a one-shot."""
    payload = b"x" * (65536 * 3 + 17)  # 3 chunks + a partial
    p = tmp_path / "big.bin"
    p.write_bytes(payload)
    assert hash_file(p).hexdigest == hashlib.sha256(payload).hexdigest()


def test_verify_file_accepts_string_and_checksum(tmp_path):
    p = tmp_path / "a.txt"
    p.write_bytes(b"abc")
    cs = hash_file(p)
    assert verify_file(p, cs) is True
    assert verify_file(p, cs.hexdigest) is True
    assert verify_file(p, f"sha256:{cs.hexdigest}") is True
    assert verify_file(p, "0" * 64) is False


# --------------------------------------------------------------------------- #
# DataFrame hashing
# --------------------------------------------------------------------------- #

def test_hash_dataframe_is_deterministic():
    df = _canonical_ohlcv()
    assert hash_dataframe(df).hexdigest == hash_dataframe(df).hexdigest


def test_hash_dataframe_detects_value_change():
    df1 = _canonical_ohlcv()
    df2 = df1.copy()
    # Use label-based access instead of iloc+get_loc to avoid pandas'
    # union-typed return from get_loc that confuses static checkers.
    df2.loc[df2.index[0], "close"] += 1e-9
    assert hash_dataframe(df1).hexdigest != hash_dataframe(df2).hexdigest


def test_hash_dataframe_detects_index_change():
    df1 = _canonical_ohlcv()
    df2 = df1.copy()
    # Cast to DatetimeIndex explicitly so .shift(freq=...) is visible
    # to type checkers; the canonical OHLCV invariant guarantees this.
    assert isinstance(df2.index, pd.DatetimeIndex)
    df2.index = df2.index.shift(1, freq="h")
    assert hash_dataframe(df1).hexdigest != hash_dataframe(df2).hexdigest


def test_hash_dataframe_detects_column_reorder():
    """Canonical OHLCV has a fixed column order; reordering is a real change."""
    df1 = _canonical_ohlcv()
    df2 = df1[["close", "open", "high", "low", "volume"]]
    assert hash_dataframe(df1).hexdigest != hash_dataframe(df2).hexdigest


def test_hash_dataframe_detects_dtype_change():
    df1 = _canonical_ohlcv()
    df2 = df1.copy()
    df2["volume"] = df2["volume"].astype("float64")  # int64 -> float64
    assert hash_dataframe(df1).hexdigest != hash_dataframe(df2).hexdigest


def test_hash_dataframe_rejects_non_dataframe():
    with pytest.raises(TypeError):
        hash_dataframe([1, 2, 3])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        hash_dataframe(None)  # type: ignore[arg-type]


def test_hash_dataframe_parquet_roundtrip_is_stable(tmp_path):
    """The whole point: write to parquet, read back, hash must match.

    Without this property, every cache hit would invalidate every
    downstream model. This is the single most important checksum
    invariant for the project.
    """
    df = _canonical_ohlcv()
    h_before = hash_dataframe(df).hexdigest

    p = tmp_path / "ohlcv.parquet"
    df.to_parquet(p)
    df_back = pd.read_parquet(p)

    h_after = hash_dataframe(df_back).hexdigest
    assert h_before == h_after, "parquet roundtrip must preserve DataFrame hash"


def test_verify_dataframe_returns_false_on_mismatch():
    df = _canonical_ohlcv()
    assert verify_dataframe(df, hash_dataframe(df)) is True
    assert verify_dataframe(df, "0" * 64) is False