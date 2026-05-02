"""
Purged K-Fold cross-validation with embargo for time-series ML.

WHY: Standard K-Fold leaks information across train/test boundaries when
labels span multiple bars (overlapping observations) or when serial
correlation in features carries info from train into test. López de Prado
(AFML Ch. 7) introduces two corrections that we implement here:

  1. PURGE: Remove training samples whose label time-spans [t0, t1] overlap
     the test fold's time window. Without this, a training label can
     literally encode information about a test-period bar.

  2. EMBARGO: After every test fold, drop a buffer of training samples
     whose features may be autocorrelated with features inside the test
     fold. Purge alone does not handle this — it operates on labels, not
     features.

Design choice: `t1` (per-label end times) is OPTIONAL. Fixed-horizon
strategies just pass `embargo_pct`; triple-barrier / variable-horizon
strategies pass `t1` as well. This is the canonical AFML design.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PurgedSplit:
    """A single (train, test) split produced by PurgedKFold.

    Indices are integer POSITIONAL (not label-based) to match sklearn's
    `split()` convention, so callers can do `X.iloc[train_idx]`.

    `n_purged` and `n_embargoed` are diagnostic counts — useful for asserting
    that purge/embargo actually fired during CV, or for logging how much
    training data each fold loses to leakage protection.
    """

    fold: int
    train_idx: np.ndarray
    test_idx: np.ndarray
    n_purged: int
    n_embargoed: int


class PurgedKFold:
    """Purged K-Fold splitter with embargo and optional per-label end-times.

    Parameters
    ----------
    n_splits : int
        Number of folds. Must be >= 2.
    embargo_pct : float
        Fraction of total samples to drop AFTER each test fold (autocorrelation
        buffer). Must be in [0, 1). Default 0.0 (no embargo).
    t1 : pd.Series | None
        Optional per-label end times. Index = label START time (must equal
        `X.index` at split-time). Values = label END time (must be >= the
        corresponding index). If None, only the embargo applies — appropriate
        for fixed-horizon labels.

    Notes
    -----
    Folds are contiguous, equal-sized blocks of the time-ordered dataset
    (`np.array_split` semantics — last fold absorbs any remainder).
    `X.index` must be a monotonic-increasing DatetimeIndex.
    """

    def __init__(
        self,
        n_splits: int = 5,
        embargo_pct: float = 0.0,
        t1: pd.Series | None = None,
    ) -> None:
        if n_splits < 2:
            raise ValueError(f"n_splits must be >= 2, got {n_splits}")
        if not (0.0 <= embargo_pct < 1.0):
            raise ValueError(
                f"embargo_pct must be in [0, 1), got {embargo_pct}"
            )
        if t1 is not None:
            if not isinstance(t1, pd.Series):
                raise TypeError(
                    f"t1 must be a pandas Series, got {type(t1).__name__}"
                )
            if not isinstance(t1.index, pd.DatetimeIndex):
                raise TypeError("t1 must have a DatetimeIndex")
            if not t1.index.is_monotonic_increasing:
                raise ValueError("t1 index must be monotonic increasing")
            # Each label must end at or after it starts.
            t1_as_idx = pd.DatetimeIndex(t1.values)
            if (t1_as_idx.asi8 < t1.index.asi8).any():
                raise ValueError(
                    "t1 values must end at or after their corresponding "
                    "index (label end-time >= label start-time)"
                )

        self.n_splits = n_splits
        self.embargo_pct = embargo_pct
        self.t1 = t1

    def get_n_splits(
        self,
        X: pd.DataFrame | pd.Series | None = None,
        y: pd.Series | None = None,
        groups: pd.Series | None = None,
    ) -> int:
        """Return the number of splits. sklearn-compatible signature."""
        return self.n_splits

    def split(
        self,
        X: pd.DataFrame | pd.Series,
        y: pd.Series | None = None,
        groups: pd.Series | None = None,
    ) -> Iterator[PurgedSplit]:
        """Yield PurgedSplit instances with integer positional indices.

        Parameters
        ----------
        X : pd.DataFrame | pd.Series
            Must have a monotonic-increasing DatetimeIndex. If `t1` was
            provided to the constructor, `X.index` must match `t1.index`
            exactly (same length, same values, same timezone).
        y, groups : ignored
            Accepted for sklearn-compatibility only.
        """
        if not isinstance(X.index, pd.DatetimeIndex):
            raise TypeError("X must have a DatetimeIndex")
        if not X.index.is_monotonic_increasing:
            raise ValueError("X index must be monotonic increasing")

        n = X.shape[0]
        if n < self.n_splits:
            raise ValueError(
                f"n_samples ({n}) must be >= n_splits ({self.n_splits})"
            )

        # Validate t1 alignment with X.
        if self.t1 is not None:
            if len(self.t1) != n:
                raise ValueError(
                    f"t1 length ({len(self.t1)}) must equal X length ({n})"
                )
            if not self.t1.index.equals(X.index):
                raise ValueError(
                    "t1.index must equal X.index exactly (same values, "
                    "same timezone, same order)"
                )

        embargo_n = int(np.floor(n * self.embargo_pct))

        # Build per-sample [t0, t1] spans as int64 nanoseconds for fast
        # interval-overlap checks. If no t1 was provided, t1 = t0
        # (a label that ends the same instant it starts has no overlap by
        # itself, so purge becomes a no-op and embargo carries the load).
        t0_ns = X.index.asi8
        if self.t1 is not None:
            t1_ns = pd.DatetimeIndex(self.t1.values).asi8
        else:
            t1_ns = t0_ns

        all_positions = np.arange(n)
        fold_bounds = np.array_split(all_positions, self.n_splits)

        for fold_i, test_idx in enumerate(fold_bounds):
            test_start_pos = int(test_idx[0])
            test_end_pos = int(test_idx[-1])

            # Test window in time: from t0 of the first test sample
            # to the MAX t1 across all test samples (handles labels that
            # extend past the fold's last bar).
            test_t0_ns = int(t0_ns[test_start_pos])
            test_t1_ns = int(t1_ns[test_start_pos : test_end_pos + 1].max())

            # Candidate train positions: everything outside the test fold.
            train_mask = np.ones(n, dtype=bool)
            train_mask[test_start_pos : test_end_pos + 1] = False

            # --- PURGE ---------------------------------------------------
            # A training sample [t0_i, t1_i] overlaps the test window
            # [test_t0, test_t1] iff t0_i <= test_t1 AND t1_i >= test_t0.
            # Drop any training sample whose label span overlaps.
            overlap_mask = (t0_ns <= test_t1_ns) & (t1_ns >= test_t0_ns)
            purge_mask = train_mask & overlap_mask
            n_purged = int(purge_mask.sum())
            train_mask &= ~overlap_mask

            # --- EMBARGO -------------------------------------------------
            # Drop the next `embargo_n` positions after the test fold.
            # (No embargo on the LEFT side: by construction, training data
            # to the left already lies before the test window in time, and
            # purge has already handled any label spans that reach into it.)
            n_embargoed = 0
            if embargo_n > 0 and test_end_pos + 1 < n:
                embargo_start = test_end_pos + 1
                embargo_stop = min(embargo_start + embargo_n, n)
                pre_embargo_kept = int(
                    train_mask[embargo_start:embargo_stop].sum()
                )
                train_mask[embargo_start:embargo_stop] = False
                n_embargoed = pre_embargo_kept

            train_idx = all_positions[train_mask]

            yield PurgedSplit(
                fold=fold_i,
                train_idx=train_idx,
                test_idx=np.asarray(test_idx),
                n_purged=n_purged,
                n_embargoed=n_embargoed,
            )