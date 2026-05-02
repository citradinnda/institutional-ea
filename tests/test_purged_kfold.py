"""Tests for PurgedKFold (Phase 1.7).

WHY each test exists is documented inline. The core invariants:
  - Train and test never overlap.
  - Every position appears in exactly one test fold across all splits.
  - Purge actually removes overlapping labels (n_purged > 0 when it should).
  - Embargo actually removes the right number of post-test bars.
  - With no t1 and zero embargo, behaves like ordered K-Fold.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import PurgedKFold, PurgedSplit


# --------------------------------------------------------------------------- #
# Fixtures                                                                    #
# --------------------------------------------------------------------------- #
def _make_X(n: int = 100, freq: str = "h") -> pd.DataFrame:
    """Deterministic time-indexed DataFrame for splitter testing."""
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    return pd.DataFrame({"feat": np.arange(n, dtype=float)}, index=idx)


def _make_t1(X: pd.DataFrame, horizon: int) -> pd.Series:
    """Per-label end-times: each label ends `horizon` bars after it starts.

    The last `horizon` labels are clipped to the final index value so we
    don't fabricate timestamps past the dataset.
    """
    end_positions = np.minimum(
        np.arange(len(X)) + horizon, len(X) - 1
    )
    return pd.Series(X.index[end_positions], index=X.index)


# --------------------------------------------------------------------------- #
# Constructor validation                                                      #
# --------------------------------------------------------------------------- #
def test_n_splits_must_be_at_least_two() -> None:
    with pytest.raises(ValueError, match="n_splits"):
        PurgedKFold(n_splits=1)


def test_embargo_pct_must_be_in_range() -> None:
    with pytest.raises(ValueError, match="embargo_pct"):
        PurgedKFold(n_splits=5, embargo_pct=-0.01)
    with pytest.raises(ValueError, match="embargo_pct"):
        PurgedKFold(n_splits=5, embargo_pct=1.0)


def test_t1_must_be_series() -> None:
    with pytest.raises(TypeError, match="t1 must be"):
        PurgedKFold(n_splits=5, t1=[1, 2, 3])  # type: ignore[arg-type]


def test_t1_must_have_datetime_index() -> None:
    bad = pd.Series([1, 2, 3])
    with pytest.raises(TypeError, match="DatetimeIndex"):
        PurgedKFold(n_splits=5, t1=bad)


def test_t1_must_be_monotonic() -> None:
    idx = pd.DatetimeIndex(
        ["2024-01-02", "2024-01-01", "2024-01-03"], tz="UTC"
    )
    bad = pd.Series(idx, index=idx)
    with pytest.raises(ValueError, match="monotonic"):
        PurgedKFold(n_splits=5, t1=bad)


def test_t1_values_must_be_after_index() -> None:
    """A label cannot END before it STARTS."""
    idx = pd.date_range("2024-01-01", periods=5, freq="D", tz="UTC")
    # End-times are one day BEFORE start-times → invalid.
    bad_values = idx - pd.Timedelta(days=1)
    bad = pd.Series(bad_values, index=idx)
    with pytest.raises(ValueError, match="end at or after"):
        PurgedKFold(n_splits=2, t1=bad)


# --------------------------------------------------------------------------- #
# split() input validation                                                    #
# --------------------------------------------------------------------------- #
def test_split_requires_datetime_index() -> None:
    splitter = PurgedKFold(n_splits=3)
    X = pd.DataFrame({"feat": np.arange(10)})  # default RangeIndex
    with pytest.raises(TypeError, match="DatetimeIndex"):
        list(splitter.split(X))


def test_split_requires_monotonic_index() -> None:
    splitter = PurgedKFold(n_splits=3)
    idx = pd.DatetimeIndex(
        ["2024-01-02", "2024-01-01", "2024-01-03"], tz="UTC"
    )
    X = pd.DataFrame({"feat": [1, 2, 3]}, index=idx)
    with pytest.raises(ValueError, match="monotonic"):
        list(splitter.split(X))


def test_split_rejects_too_few_samples() -> None:
    splitter = PurgedKFold(n_splits=10)
    X = _make_X(n=5)
    with pytest.raises(ValueError, match="n_samples"):
        list(splitter.split(X))


def test_t1_length_must_match_X() -> None:
    X = _make_X(n=100)
    t1_short = _make_t1(_make_X(n=50), horizon=2)
    splitter = PurgedKFold(n_splits=5, t1=t1_short)
    with pytest.raises(ValueError, match="t1 length"):
        list(splitter.split(X))


def test_t1_index_must_match_X_index() -> None:
    X = _make_X(n=100)
    X_other = _make_X(n=100, freq="2h")  # different timestamps
    t1 = _make_t1(X_other, horizon=2)
    splitter = PurgedKFold(n_splits=5, t1=t1)
    with pytest.raises(ValueError, match="t1.index must equal"):
        list(splitter.split(X))


# --------------------------------------------------------------------------- #
# Core split-correctness invariants                                           #
# --------------------------------------------------------------------------- #
def test_get_n_splits_returns_constructor_value() -> None:
    assert PurgedKFold(n_splits=7).get_n_splits() == 7


def test_yields_correct_number_of_splits() -> None:
    X = _make_X(n=100)
    splitter = PurgedKFold(n_splits=5)
    splits = list(splitter.split(X))
    assert len(splits) == 5


def test_train_and_test_never_overlap() -> None:
    """Hard invariant: a position is never in both train and test."""
    X = _make_X(n=200)
    t1 = _make_t1(X, horizon=5)
    splitter = PurgedKFold(n_splits=5, embargo_pct=0.02, t1=t1)
    for s in splitter.split(X):
        assert len(np.intersect1d(s.train_idx, s.test_idx)) == 0


def test_test_folds_partition_the_dataset() -> None:
    """Every position must appear in exactly one test fold."""
    X = _make_X(n=100)
    splitter = PurgedKFold(n_splits=5)
    seen = np.concatenate([s.test_idx for s in splitter.split(X)])
    assert sorted(seen.tolist()) == list(range(100))


def test_returns_purged_split_dataclass() -> None:
    X = _make_X(n=50)
    splitter = PurgedKFold(n_splits=5)
    for s in splitter.split(X):
        assert isinstance(s, PurgedSplit)


# --------------------------------------------------------------------------- #
# Behaviour without t1 / embargo (degenerate-but-valid case)                  #
# --------------------------------------------------------------------------- #
def test_no_t1_no_embargo_behaves_like_ordered_kfold() -> None:
    """With no label overlap and zero embargo, train = everything outside test."""
    X = _make_X(n=100)
    splitter = PurgedKFold(n_splits=5, embargo_pct=0.0, t1=None)
    for s in splitter.split(X):
        assert s.n_purged == 0
        assert s.n_embargoed == 0
        # train ∪ test = all positions
        union = np.union1d(s.train_idx, s.test_idx)
        assert union.tolist() == list(range(100))


# --------------------------------------------------------------------------- #
# Purge behaviour                                                             #
# --------------------------------------------------------------------------- #
def test_purge_removes_overlapping_train_labels() -> None:
    """A training label whose span reaches into the test fold must be purged."""
    X = _make_X(n=100)
    # Long horizon → labels just before each test fold reach INTO that fold.
    t1 = _make_t1(X, horizon=10)
    splitter = PurgedKFold(n_splits=5, t1=t1)
    splits = list(splitter.split(X))
    # Folds after the first should see purging on the left edge.
    assert any(s.n_purged > 0 for s in splits[1:])


def test_purge_does_nothing_when_horizon_is_zero() -> None:
    """Labels that end the same bar they start cannot overlap a later fold."""
    X = _make_X(n=100)
    t1 = _make_t1(X, horizon=0)  # t1 == index
    splitter = PurgedKFold(n_splits=5, embargo_pct=0.0, t1=t1)
    for s in splitter.split(X):
        assert s.n_purged == 0


def test_purged_train_indices_have_no_label_overlap_with_test() -> None:
    """The DEFINING property of purge: no train label spans into test window."""
    X = _make_X(n=200)
    horizon = 8
    t1 = _make_t1(X, horizon=horizon)
    t0_ns = X.index.asi8
    t1_ns = pd.DatetimeIndex(t1.values).asi8

    splitter = PurgedKFold(n_splits=5, t1=t1)
    for s in splitter.split(X):
        test_t0 = t0_ns[s.test_idx[0]]
        test_t1 = t1_ns[s.test_idx[0] : s.test_idx[-1] + 1].max()
        for ti in s.train_idx:
            overlaps = (t0_ns[ti] <= test_t1) and (t1_ns[ti] >= test_t0)
            assert not overlaps, f"train idx {ti} overlaps test window"


# --------------------------------------------------------------------------- #
# Embargo behaviour                                                           #
# --------------------------------------------------------------------------- #
def test_embargo_drops_correct_number_of_post_test_bars() -> None:
    """With 5% embargo on n=100 → 5 bars dropped after each non-final fold."""
    X = _make_X(n=100)
    splitter = PurgedKFold(n_splits=5, embargo_pct=0.05)
    splits = list(splitter.split(X))
    # All folds except the last should embargo exactly 5 bars.
    for s in splits[:-1]:
        assert s.n_embargoed == 5
    # Last fold has no bars after it → nothing to embargo.
    assert splits[-1].n_embargoed == 0


def test_embargoed_positions_are_excluded_from_train() -> None:
    """Positions inside the embargo window must not appear in train_idx."""
    X = _make_X(n=100)
    splitter = PurgedKFold(n_splits=5, embargo_pct=0.05)
    splits = list(splitter.split(X))
    for s in splits[:-1]:
        embargo_start = int(s.test_idx[-1]) + 1
        embargo_stop = embargo_start + 5
        embargoed = np.arange(embargo_start, embargo_stop)
        assert len(np.intersect1d(s.train_idx, embargoed)) == 0


def test_zero_embargo_keeps_all_post_test_bars() -> None:
    X = _make_X(n=100)
    splitter = PurgedKFold(n_splits=5, embargo_pct=0.0)
    for s in splitter.split(X):
        assert s.n_embargoed == 0