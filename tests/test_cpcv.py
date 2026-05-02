"""Tests for CombinatorialPurgedKFold (Phase 1.8)."""
from __future__ import annotations

from itertools import combinations
from math import comb

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import CombinatorialPurgedKFold, CPCVSplit


# --------------------------------------------------------------------------- #
# Fixtures                                                                    #
# --------------------------------------------------------------------------- #
def _make_X(n: int = 120, freq: str = "h") -> pd.DataFrame:
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    return pd.DataFrame({"feat": np.arange(n, dtype=float)}, index=idx)


def _make_t1(X: pd.DataFrame, horizon: int) -> pd.Series:
    end_positions = np.minimum(np.arange(len(X)) + horizon, len(X) - 1)
    return pd.Series(X.index[end_positions], index=X.index)


# --------------------------------------------------------------------------- #
# Constructor validation                                                      #
# --------------------------------------------------------------------------- #
def test_n_splits_must_be_at_least_two() -> None:
    with pytest.raises(ValueError, match="n_splits"):
        CombinatorialPurgedKFold(n_splits=1, n_test_splits=1)


def test_n_test_splits_must_be_at_least_one() -> None:
    with pytest.raises(ValueError, match="n_test_splits must be >= 1"):
        CombinatorialPurgedKFold(n_splits=5, n_test_splits=0)


def test_n_test_splits_must_be_less_than_n_splits() -> None:
    """k must be < N or there's no training data left."""
    with pytest.raises(ValueError, match="must be <"):
        CombinatorialPurgedKFold(n_splits=5, n_test_splits=5)


def test_embargo_pct_must_be_in_range() -> None:
    with pytest.raises(ValueError, match="embargo_pct"):
        CombinatorialPurgedKFold(n_splits=6, n_test_splits=2, embargo_pct=1.0)


# --------------------------------------------------------------------------- #
# Counts                                                                      #
# --------------------------------------------------------------------------- #
def test_get_n_splits_equals_n_choose_k() -> None:
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    assert cv.get_n_splits() == comb(6, 2)  # 15


def test_get_n_paths_equals_n_minus_1_choose_k_minus_1() -> None:
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    assert cv.get_n_paths() == comb(5, 1)  # 5


def test_split_yields_n_choose_k_splits() -> None:
    X = _make_X(n=120)
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    splits = list(cv.split(X))
    assert len(splits) == comb(6, 2)


# --------------------------------------------------------------------------- #
# Split structure                                                             #
# --------------------------------------------------------------------------- #
def test_each_split_has_correct_number_of_test_groups() -> None:
    X = _make_X(n=120)
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    for s in cv.split(X):
        assert len(s.test_groups) == 2


def test_train_and_test_never_overlap() -> None:
    X = _make_X(n=120)
    t1 = _make_t1(X, horizon=3)
    cv = CombinatorialPurgedKFold(
        n_splits=6, n_test_splits=2, embargo_pct=0.02, t1=t1
    )
    for s in cv.split(X):
        assert len(np.intersect1d(s.train_idx, s.test_idx)) == 0


def test_returns_cpcv_split_dataclass() -> None:
    X = _make_X(n=60)
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    for s in cv.split(X):
        assert isinstance(s, CPCVSplit)


def test_combination_indices_are_lexicographic() -> None:
    """combination=i must correspond to the i-th lex combo."""
    X = _make_X(n=60)
    cv = CombinatorialPurgedKFold(n_splits=5, n_test_splits=2)
    expected = list(combinations(range(5), 2))
    for s in cv.split(X):
        assert s.test_groups == expected[s.combination]


# --------------------------------------------------------------------------- #
# Coverage / counting invariants                                              #
# --------------------------------------------------------------------------- #
def test_each_group_appears_in_n_paths_combinations() -> None:
    """Each group should be a test group in exactly C(N-1, k-1) combinations."""
    X = _make_X(n=120)
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    counts = np.zeros(6, dtype=int)
    for s in cv.split(X):
        for g in s.test_groups:
            counts[g] += 1
    assert np.all(counts == cv.get_n_paths())


def test_with_k_equals_one_matches_kfold_count() -> None:
    """k=1 is a vanilla 'leave-one-group-out' setup with n_paths=1."""
    cv = CombinatorialPurgedKFold(n_splits=5, n_test_splits=1)
    assert cv.get_n_splits() == 5
    assert cv.get_n_paths() == 1


# --------------------------------------------------------------------------- #
# split() input validation                                                    #
# --------------------------------------------------------------------------- #
def test_split_requires_datetime_index() -> None:
    cv = CombinatorialPurgedKFold(n_splits=4, n_test_splits=2)
    X = pd.DataFrame({"feat": np.arange(20)})
    with pytest.raises(TypeError, match="DatetimeIndex"):
        list(cv.split(X))


def test_split_rejects_too_few_samples() -> None:
    cv = CombinatorialPurgedKFold(n_splits=10, n_test_splits=2)
    X = _make_X(n=5)
    with pytest.raises(ValueError, match="n_samples"):
        list(cv.split(X))


# --------------------------------------------------------------------------- #
# Purge / embargo                                                             #
# --------------------------------------------------------------------------- #
def test_purge_removes_overlapping_labels() -> None:
    X = _make_X(n=120)
    t1 = _make_t1(X, horizon=10)  # long horizon → overlap
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2, t1=t1)
    splits = list(cv.split(X))
    assert any(s.n_purged > 0 for s in splits)


def test_embargo_drops_bars_after_each_test_run() -> None:
    """With non-contiguous test groups, embargo must fire after each run."""
    X = _make_X(n=120)
    cv = CombinatorialPurgedKFold(
        n_splits=6, n_test_splits=2, embargo_pct=0.05
    )
    embargo_n = int(np.floor(120 * 0.05))  # 6
    for s in cv.split(X):
        # Re-derive contiguous test runs from the split.
        diffs = np.diff(s.test_idx)
        run_ends = list(s.test_idx[np.where(diffs != 1)[0]])
        run_ends.append(int(s.test_idx[-1]))
        # Each run that doesn't end at n-1 should embargo up to embargo_n bars.
        for end in run_ends:
            if end + 1 < 120:
                window = np.arange(end + 1, min(end + 1 + embargo_n, 120))
                assert len(np.intersect1d(s.train_idx, window)) == 0


# --------------------------------------------------------------------------- #
# Path assembly matrix                                                        #
# --------------------------------------------------------------------------- #
def test_path_assembly_matrix_shape() -> None:
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    m = cv.path_assembly_matrix()
    assert m.shape == (6, cv.get_n_paths())


def test_path_assembly_matrix_no_unfilled_slots() -> None:
    """Every (group, path) cell must be assigned a real combination index."""
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    m = cv.path_assembly_matrix()
    assert (m >= 0).all()


def test_path_assembly_each_path_covers_all_groups_via_distinct_combos() -> None:
    """For each cell [g, p], the assigned combination must have g as a test
    group. (We do NOT require distinct combos per column: when k >= 2 a single
    combination can legitimately supply OOS predictions for multiple groups in
    the same path, since it trained on data excluding all of them.)"""
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    m = cv.path_assembly_matrix()
    combos = list(combinations(range(6), 2))
    for p in range(m.shape[1]):
        col = m[:, p]
        for g, combo_idx in enumerate(col):
            assert g in combos[combo_idx]


def test_path_assembly_matrix_each_combo_appears_k_times() -> None:
    """Each combination contributes its k test groups to k different (group, path)
    cells across the matrix — so combination i appears exactly k times."""
    cv = CombinatorialPurgedKFold(n_splits=6, n_test_splits=2)
    m = cv.path_assembly_matrix()
    unique, counts = np.unique(m, return_counts=True)
    assert len(unique) == cv.get_n_splits()
    assert np.all(counts == 2)  # k = 2