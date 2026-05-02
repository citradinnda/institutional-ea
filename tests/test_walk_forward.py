from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from quantcore.validation import WalkForward, WalkForwardSplit


def make_index(n: int, freq: str = "h") -> pd.DatetimeIndex:
    """A UTC hourly index of length n.

    Why hourly: freq is irrelevant to the splitter (it operates on
    positional offsets), so we pick something fast and unambiguous.
    """
    return pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")


# ---------------------------------------------------------------------------
# Rolling mode
# ---------------------------------------------------------------------------

def test_rolling_basic_split_count():
    # n=100, train=40, test=10, step=10 (default).
    # test_end_pos = offset + 50; valid offsets 0,10,...,50 → 6 splits.
    idx = make_index(100)
    wf = WalkForward(mode="rolling", train_size=40, test_size=10)
    assert len(list(wf.split(idx))) == 6


def test_rolling_train_window_constant_size():
    idx = make_index(200)
    wf = WalkForward(mode="rolling", train_size=50, test_size=20)
    for split in wf.split(idx):
        assert len(split.train_idx) == 50


def test_rolling_train_strictly_before_test():
    idx = make_index(200)
    wf = WalkForward(mode="rolling", train_size=50, test_size=20)
    for split in wf.split(idx):
        assert split.train_idx.max() < split.test_idx.min()


def test_rolling_step_size_advances_train_start():
    idx = make_index(200)
    wf = WalkForward(
        mode="rolling", train_size=50, test_size=20, step_size=15
    )
    splits = list(wf.split(idx))
    train_starts = [s.train_idx[0] for s in splits]
    assert np.all(np.diff(train_starts) == 15)


def test_rolling_default_step_size_is_test_size():
    """Non-overlapping test windows is the canonical walk-forward setup."""
    idx = make_index(200)
    wf = WalkForward(mode="rolling", train_size=50, test_size=20)
    splits = list(wf.split(idx))
    test_starts = [s.test_idx[0] for s in splits]
    assert np.all(np.diff(test_starts) == 20)


# ---------------------------------------------------------------------------
# Anchored mode
# ---------------------------------------------------------------------------

def test_anchored_basic_split_count():
    idx = make_index(100)
    wf = WalkForward(mode="anchored", train_size=40, test_size=10)
    assert len(list(wf.split(idx))) == 6


def test_anchored_train_always_starts_at_zero():
    idx = make_index(200)
    wf = WalkForward(mode="anchored", train_size=50, test_size=20)
    for split in wf.split(idx):
        assert split.train_idx[0] == 0


def test_anchored_train_grows_monotonically():
    idx = make_index(200)
    wf = WalkForward(mode="anchored", train_size=50, test_size=20)
    splits = list(wf.split(idx))
    train_lengths = [len(s.train_idx) for s in splits]
    # Anchored: each subsequent fold's training set is strictly larger.
    assert all(b > a for a, b in zip(train_lengths, train_lengths[1:]))


def test_anchored_train_strictly_before_test():
    idx = make_index(200)
    wf = WalkForward(mode="anchored", train_size=50, test_size=20)
    for split in wf.split(idx):
        assert split.train_idx.max() < split.test_idx.min()


def test_anchored_test_window_constant_size():
    idx = make_index(200)
    wf = WalkForward(mode="anchored", train_size=50, test_size=20)
    for split in wf.split(idx):
        assert len(split.test_idx) == 20


# ---------------------------------------------------------------------------
# Embargo
# ---------------------------------------------------------------------------

def test_embargo_inserts_gap_rolling():
    # n=200, embargo_pct=0.05 → gap = int(0.05 * 200) = 10.
    idx = make_index(200)
    wf = WalkForward(
        mode="rolling", train_size=50, test_size=20, embargo_pct=0.05
    )
    for split in wf.split(idx):
        gap = split.test_idx[0] - split.train_idx[-1] - 1
        assert gap == 10


def test_embargo_inserts_gap_anchored():
    idx = make_index(200)
    wf = WalkForward(
        mode="anchored", train_size=50, test_size=20, embargo_pct=0.05
    )
    for split in wf.split(idx):
        gap = split.test_idx[0] - split.train_idx[-1] - 1
        assert gap == 10


def test_zero_embargo_no_gap():
    idx = make_index(200)
    wf = WalkForward(
        mode="rolling", train_size=50, test_size=20, embargo_pct=0.0
    )
    for split in wf.split(idx):
        # train_end_pos and test_start_pos are adjacent → gap = 0.
        gap = split.test_idx[0] - split.train_idx[-1] - 1
        assert gap == 0


# ---------------------------------------------------------------------------
# t1 purge (per-label end times)
# ---------------------------------------------------------------------------

def test_t1_purges_overlapping_train_labels():
    """If a training label's end time reaches into the test window, it
    must be purged. Otherwise the model has effectively seen the future."""
    idx = make_index(100)
    # Construct t1 so the LAST training sample (pos 39) has a label that
    # ends well inside the first test window (pos 40..49).
    t1 = pd.Series(idx, index=idx)  # default: label ends at its own bar
    t1.iloc[39] = idx[45]  # label at pos 39 ends at pos 45 → overlaps test
    wf = WalkForward(mode="rolling", train_size=40, test_size=10, t1=t1)
    first = next(iter(wf.split(idx)))
    assert 39 not in first.train_idx


def test_t1_no_purge_when_labels_end_before_test():
    """If every label ends at or before its own bar, no training sample
    overlaps the test window and nothing should be purged."""
    idx = make_index(100)
    t1 = pd.Series(idx, index=idx)  # label ends at its own bar
    wf = WalkForward(mode="rolling", train_size=40, test_size=10, t1=t1)
    first = next(iter(wf.split(idx)))
    assert len(first.train_idx) == 40


def test_t1_skips_fold_when_all_train_purged():
    """If every training label reaches into the test window, the fold
    should be skipped rather than yielded with an empty training set."""
    idx = make_index(100)
    # Push every label far into the future → all training samples purged.
    far_future = pd.Timestamp("2099-01-01", tz="UTC")
    t1 = pd.Series([far_future] * 100, index=idx)
    wf = WalkForward(mode="rolling", train_size=40, test_size=10, t1=t1)
    splits = list(wf.split(idx))
    assert len(splits) == 0


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def test_invalid_mode_raises():
    with pytest.raises(ValueError, match="mode"):
        WalkForward(mode="sliding", train_size=50, test_size=20)  # type: ignore[arg-type]


def test_nonpositive_train_size_raises():
    with pytest.raises(ValueError, match="train_size"):
        WalkForward(mode="rolling", train_size=0, test_size=20)


def test_nonpositive_test_size_raises():
    with pytest.raises(ValueError, match="test_size"):
        WalkForward(mode="rolling", train_size=50, test_size=0)


def test_invalid_embargo_raises():
    with pytest.raises(ValueError, match="embargo_pct"):
        WalkForward(
            mode="rolling", train_size=50, test_size=20, embargo_pct=1.5
        )


def test_empty_index_raises():
    idx = pd.DatetimeIndex([], tz="UTC")
    wf = WalkForward(mode="rolling", train_size=50, test_size=20)
    with pytest.raises(ValueError, match="empty"):
        list(wf.split(idx))


def test_non_monotonic_index_raises():
    idx = make_index(100)
    shuffled = idx[[5, 2, 1, 3, 4] + list(range(5, 100))]
    wf = WalkForward(mode="rolling", train_size=40, test_size=10)
    with pytest.raises(ValueError, match="monotonic"):
        list(wf.split(shuffled))


# ---------------------------------------------------------------------------
# Structural / API
# ---------------------------------------------------------------------------

def test_fold_id_is_sequential():
    idx = make_index(200)
    wf = WalkForward(mode="rolling", train_size=50, test_size=20)
    splits = list(wf.split(idx))
    assert [s.fold_id for s in splits] == list(range(len(splits)))


def test_get_n_splits_matches_split_iter():
    idx = make_index(200)
    wf = WalkForward(mode="anchored", train_size=50, test_size=20)
    assert wf.get_n_splits(idx) == len(list(wf.split(idx)))


def test_timestamps_match_indices():
    """The reported start/end timestamps must equal the index values at
    the corresponding positional indices. Sanity check against off-by-one
    bugs in the dataclass construction."""
    idx = make_index(200)
    wf = WalkForward(mode="rolling", train_size=50, test_size=20)
    for split in wf.split(idx):
        assert isinstance(split, WalkForwardSplit)
        assert split.train_start == idx[split.train_idx[0]]
        assert split.train_end == idx[split.train_idx[-1]]
        assert split.test_start == idx[split.test_idx[0]]
        assert split.test_end == idx[split.test_idx[-1]]