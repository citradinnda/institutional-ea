"""
Combinatorial Purged Cross-Validation (CPCV) with embargo.

WHY: A single backtest path (Phase 1.7 PurgedKFold) is one realization of
fold ordering. Its Sharpe ratio is a point estimate with no measure of
variance. CPCV (López de Prado AFML Ch. 12) generates many full-period
backtest paths from the SAME data by picking k of N folds as test
(C(N,k) combinations) and stitching test predictions into C(N-1, k-1)
distinct paths. The resulting Sharpe distribution feeds Probabilistic
Sharpe (1.10), Deflated Sharpe (1.10), and Reality Check (1.12).

Purge + embargo extends to non-contiguous test blocks: when k >= 2 the
test set may consist of disjoint group ranges (e.g. groups {0, 2, 4}).
We identify each contiguous run in the test set and apply purge +
embargo per run.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb
from typing import Iterator

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CPCVSplit:
    """A single (train, test) split produced by CombinatorialPurgedKFold.

    `combination` is the lexicographic index into `itertools.combinations(
    range(n_splits), n_test_splits)`. `test_groups` is the tuple of group
    ids (0..n_splits-1) that are test in this combination — needed by
    `path_assembly_matrix()` to attribute predictions to paths.
    """

    combination: int
    test_groups: tuple[int, ...]
    train_idx: np.ndarray
    test_idx: np.ndarray
    n_purged: int
    n_embargoed: int


class CombinatorialPurgedKFold:
    """Combinatorial Purged K-Fold splitter with embargo and optional t1.

    Parameters
    ----------
    n_splits : int
        Total number of equal-sized contiguous groups (N). Must be >= 2.
    n_test_splits : int
        Number of groups used as test in each combination (k). Must satisfy
        1 <= k < n_splits.
    embargo_pct : float
        Fraction of total samples dropped after each contiguous test run.
        Must be in [0, 1).
    t1 : pd.Series | None
        Optional per-label end times (see PurgedKFold for semantics).

    Notes
    -----
    Yields C(n_splits, n_test_splits) splits. The number of distinct
    backtest paths obtainable via `path_assembly_matrix()` is
    C(n_splits - 1, n_test_splits - 1).
    """

    def __init__(
        self,
        n_splits: int = 6,
        n_test_splits: int = 2,
        embargo_pct: float = 0.0,
        t1: pd.Series | None = None,
    ) -> None:
        if n_splits < 2:
            raise ValueError(f"n_splits must be >= 2, got {n_splits}")
        if n_test_splits < 1:
            raise ValueError(
                f"n_test_splits must be >= 1, got {n_test_splits}"
            )
        if n_test_splits >= n_splits:
            raise ValueError(
                f"n_test_splits ({n_test_splits}) must be < n_splits "
                f"({n_splits}); at least one group must remain for training"
            )
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
            t1_as_idx = pd.DatetimeIndex(t1.values)
            if (t1_as_idx.asi8 < t1.index.asi8).any():
                raise ValueError(
                    "t1 values must end at or after their corresponding "
                    "index (label end-time >= label start-time)"
                )

        self.n_splits = n_splits
        self.n_test_splits = n_test_splits
        self.embargo_pct = embargo_pct
        self.t1 = t1

    # ------------------------------------------------------------------ #
    # Counts                                                             #
    # ------------------------------------------------------------------ #
    def get_n_splits(
        self,
        X: pd.DataFrame | pd.Series | None = None,
        y: pd.Series | None = None,
        groups: pd.Series | None = None,
    ) -> int:
        """Number of train/test combinations: C(n_splits, n_test_splits)."""
        return comb(self.n_splits, self.n_test_splits)

    def get_n_paths(self) -> int:
        """Number of distinct backtest paths: C(n_splits - 1, n_test_splits - 1).

        Each path is a full-period out-of-sample sequence covering all groups
        exactly once.
        """
        return comb(self.n_splits - 1, self.n_test_splits - 1)

    # ------------------------------------------------------------------ #
    # Path assembly                                                      #
    # ------------------------------------------------------------------ #
    def path_assembly_matrix(self) -> np.ndarray:
        """Return (n_splits, n_paths) int matrix mapping (group, path) -> combo.

        Entry [g, p] = the combination index whose test prediction for
        group g is the p-th path's coverage of group g. Each group appears
        as test in exactly C(n_splits-1, n_test_splits-1) combinations,
        which equals n_paths — so every column ranges over n_splits
        distinct combinations and constitutes one full backtest path.

        Construction is greedy in lexicographic combination order: for each
        combination, append its test groups to the next available slot of
        each group's row. Because each group is touched exactly n_paths
        times, every row fills exactly.
        """
        n_paths = self.get_n_paths()
        matrix = np.full((self.n_splits, n_paths), -1, dtype=int)
        counts = np.zeros(self.n_splits, dtype=int)
        for combo_idx, combo in enumerate(
            combinations(range(self.n_splits), self.n_test_splits)
        ):
            for g in combo:
                matrix[g, counts[g]] = combo_idx
                counts[g] += 1
        return matrix

    def group_indices(self, n_samples: int) -> list[np.ndarray]:
        """Return list of n_splits arrays giving positional indices per group."""
        if n_samples < self.n_splits:
            raise ValueError(
                f"n_samples ({n_samples}) must be >= n_splits ({self.n_splits})"
            )
        return [
            np.asarray(g)
            for g in np.array_split(np.arange(n_samples), self.n_splits)
        ]

    # ------------------------------------------------------------------ #
    # Splitting                                                          #
    # ------------------------------------------------------------------ #
    def split(
        self,
        X: pd.DataFrame | pd.Series,
        y: pd.Series | None = None,
        groups: pd.Series | None = None,
    ) -> Iterator[CPCVSplit]:
        """Yield CPCVSplit instances in lexicographic combination order."""
        if not isinstance(X.index, pd.DatetimeIndex):
            raise TypeError("X must have a DatetimeIndex")
        if not X.index.is_monotonic_increasing:
            raise ValueError("X index must be monotonic increasing")

        n = X.shape[0]
        if n < self.n_splits:
            raise ValueError(
                f"n_samples ({n}) must be >= n_splits ({self.n_splits})"
            )

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
        groups_pos = self.group_indices(n)

        t0_ns = X.index.asi8
        if self.t1 is not None:
            t1_ns = pd.DatetimeIndex(self.t1.values).asi8
        else:
            t1_ns = t0_ns

        for combo_idx, combo in enumerate(
            combinations(range(self.n_splits), self.n_test_splits)
        ):
            test_idx = np.concatenate([groups_pos[g] for g in combo])
            test_idx.sort()

            train_mask = np.ones(n, dtype=bool)
            train_mask[test_idx] = False

            # Identify contiguous runs in the (sorted) test index. Each run
            # gets its own purge window and its own post-run embargo.
            runs = _contiguous_runs(test_idx)

            n_purged = 0
            n_embargoed = 0
            for run_start, run_end in runs:
                run_t0_ns = int(t0_ns[run_start])
                run_t1_ns = int(t1_ns[run_start : run_end + 1].max())

                # Purge: drop train samples whose [t0, t1] overlaps this run.
                overlap = (t0_ns <= run_t1_ns) & (t1_ns >= run_t0_ns)
                purge_now = train_mask & overlap
                n_purged += int(purge_now.sum())
                train_mask &= ~overlap

                # Embargo: drop the next embargo_n bars after this run, but
                # only those still in train_mask (avoid double-counting if
                # the embargo window overlaps another test run).
                if embargo_n > 0 and run_end + 1 < n:
                    emb_start = run_end + 1
                    emb_stop = min(emb_start + embargo_n, n)
                    kept = int(train_mask[emb_start:emb_stop].sum())
                    n_embargoed += kept
                    train_mask[emb_start:emb_stop] = False

            train_idx = np.flatnonzero(train_mask)

            yield CPCVSplit(
                combination=combo_idx,
                test_groups=tuple(combo),
                train_idx=train_idx,
                test_idx=test_idx,
                n_purged=n_purged,
                n_embargoed=n_embargoed,
            )


# ---------------------------------------------------------------------- #
# Helpers                                                                #
# ---------------------------------------------------------------------- #
def _contiguous_runs(sorted_positions: np.ndarray) -> list[tuple[int, int]]:
    """Return list of (start, end) inclusive runs of consecutive integers.

    Example: [0, 1, 2, 5, 6, 9] -> [(0, 2), (5, 6), (9, 9)]
    """
    if sorted_positions.size == 0:
        return []
    runs: list[tuple[int, int]] = []
    start = int(sorted_positions[0])
    prev = int(sorted_positions[0])
    for p in sorted_positions[1:]:
        p_int = int(p)
        if p_int != prev + 1:
            runs.append((start, prev))
            start = p_int
        prev = p_int
    runs.append((start, prev))
    return runs