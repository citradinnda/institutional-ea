from __future__ import annotations

import hashlib
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import pandas as pd
from pandas.util import hash_pandas_object

# 64 KB chunks: large enough to amortize syscall overhead,
# small enough that we never hold a meaningful fraction of
# a Kaggle kernel's RAM (16 GB) for hashing alone.
_CHUNK_SIZE = 65536


@dataclass(frozen=True)
class Checksum:
    """Immutable fingerprint of a file or DataFrame.

    Why a dataclass instead of returning a bare hex string:
    we want the algorithm name to travel WITH the digest so a
    stored checksum is self-describing. A bare 'abc123...' loses
    that context the moment it leaves the function.
    """

    algorithm: str
    hexdigest: str

    def __str__(self) -> str:  # "sha256:abc123..."
        return f"{self.algorithm}:{self.hexdigest}"


def _normalize_expected(expected: Union[str, Checksum]) -> str:
    """Accept either a Checksum object or a 'sha256:abc...' / 'abc...' string."""
    if isinstance(expected, Checksum):
        return expected.hexdigest
    if isinstance(expected, str):
        return expected.split(":", 1)[-1].strip().lower()
    raise TypeError(
        f"expected must be Checksum or str, got {type(expected).__name__}"
    )


def hash_file(path: Union[str, Path], *, algorithm: str = "sha256") -> Checksum:
    """Stream a file from disk and return its cryptographic hash.

    Why streaming: raw HistData CSVs and parquet caches can reach
    multi-GB. Loading them into memory just to hash would crash
    a Kaggle kernel and is gratuitous on a laptop.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Not a regular file: {p}")

    h = hashlib.new(algorithm)
    with p.open("rb") as f:
        while True:
            chunk = f.read(_CHUNK_SIZE)
            if not chunk:
                break
            h.update(chunk)
    return Checksum(algorithm=algorithm, hexdigest=h.hexdigest())


def hash_dataframe(df: pd.DataFrame, *, algorithm: str = "sha256") -> Checksum:
    """Deterministic hash of a DataFrame's *logical* contents.

    Two DataFrames hash identically iff they have:
      - the same column names in the same order,
      - the same per-column dtypes,
      - the same index name, dtype, and values,
      - the same cell values (bit-exact for floats).

    DataFrame.attrs and memory layout are intentionally NOT hashed:
    they are researcher metadata, not data.

    Why we hash schema separately from values: pandas'
    hash_pandas_object hashes per-row values and the index, but
    column NAMES and dtypes are not always part of its output
    across versions. Mixing the schema header in explicitly makes
    'rename a column' or 'cast int->float' detectable, which is
    what we want for reproducibility audits.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df).__name__}")

    h = hashlib.new(algorithm)

    # --- Header: schema (column names + dtypes) and index metadata ---
    schema_parts = [f"{name}:{dtype}" for name, dtype in df.dtypes.items()]
    h.update("|".join(schema_parts).encode("utf-8"))
    h.update(b"\x00")
    h.update(f"index_name={df.index.name}".encode("utf-8"))
    h.update(b"\x00")
    h.update(f"index_dtype={df.index.dtype}".encode("utf-8"))
    h.update(b"\x00")

    # --- Body: per-row hash including the index ---
    # hash_pandas_object returns a uint64 Series. We force a numpy view
    # via np.asarray so static type checkers see a concrete ndarray
    # rather than the ExtensionArray | ndarray union pandas declares.
    row_hashes = hash_pandas_object(df, index=True)
    h.update(np.asarray(row_hashes, dtype=np.uint64).tobytes())

    return Checksum(algorithm=algorithm, hexdigest=h.hexdigest())


def verify_file(
    path: Union[str, Path],
    expected: Union[str, Checksum],
    *,
    algorithm: str = "sha256",
) -> bool:
    """Return True iff the file at `path` matches `expected`."""
    return hash_file(path, algorithm=algorithm).hexdigest == _normalize_expected(expected)


def verify_dataframe(
    df: pd.DataFrame,
    expected: Union[str, Checksum],
    *,
    algorithm: str = "sha256",
) -> bool:
    """Return True iff the DataFrame matches `expected`."""
    return hash_dataframe(df, algorithm=algorithm).hexdigest == _normalize_expected(expected)