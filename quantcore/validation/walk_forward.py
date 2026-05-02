from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Literal

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class WalkForwardSplit:
    """A single train/test split produced by WalkForward.

    Why a dataclass: callers need both the positional indices (for slicing
    feature/label arrays) AND the timestamps (for logging, plotting, and
    sanity checks against the data). A bare tuple loses field names and
    forces every caller to remember the order — error-prone.
    """

    fold_id: int
    train_idx: np.ndarray
    test_idx: np.ndarray
    train_start: pd.Timestamp
    train_end: pd.Timestamp
    test_start: pd.Timestamp
    test_end: pd.Timestamp


class WalkForward:
    """Walk-forward cross-validation in rolling or anchored mode.

    Why this exists: K-fold (even purged K-fold) shuffles temporal order
    across folds. That is fine for IID labels but inappropriate when
    simulating live trading, where the model is refit and redeployed as
    time moves forward. Walk-forward preserves causality: every test fold
    lies strictly AFTER its training data.

    Modes
    -----
    'rolling'
        Fixed-size training window slides forward by `step_size` each fold.
        Adapts to regime change but discards old history.
    'anchored'
        Training starts at index 0 and GROWS each fold; only the test
        window slides. Uses all available history.

    Purging and embargo
    -------------------
    Consistent with PurgedKFold/CPCV so the validation suite behaves
    uniformly:
      * `embargo_pct` inserts a gap of `int(embargo_pct * n)` bars between
        the end of train and the start of test. Prevents label leakage
        when labels depend on bars beyond their own timestamp.
      * Optional `t1` (per-label end times) drops any training sample
        whose label end time reaches into the test window.

    Parameters
    ----------
    mode : 'rolling' or 'anchored'
    train_size : int
        Number of bars in the (initial) training window. For 'anchored'
        this is the size of the FIRST fold's training window; subsequent
        folds grow it by `step_size`.
    test_size : int
        Number of bars in each test window.
    step_size : int, optional
        Bars to advance between folds. Defaults to `test_size`, which
        produces non-overlapping test windows — the canonical walk-forward
        setup.
    embargo_pct : float, default 0.0
        Embargo gap as a fraction of total index length. Must be in [0, 1).
    t1 : pd.Series, optional
        Per-label end times indexed by the same DatetimeIndex as the data.
        If omitted, only `embargo_pct` applies (sufficient when the label
        horizon is <= the embargo gap).
    """

    def __init__(
        self,
        mode: Literal["rolling", "anchored"],
        train_size: int,
        test_size: int,
        step_size: int | None = None,
        embargo_pct: float = 0.0,
        t1: pd.Series | None = None,
    ) -> None:
        if mode not in ("rolling", "anchored"):
            raise ValueError(
                f"mode must be 'rolling' or 'anchored', got {mode!r}"
            )
        if train_size <= 0:
            raise ValueError(f"train_size must be positive, got {train_size}")
        if test_size <= 0:
            raise ValueError(f"test_size must be positive, got {test_size}")
        if step_size is not None and step_size <= 0:
            raise ValueError(f"step_size must be positive, got {step_size}")
        if not (0.0 <= embargo_pct < 1.0):
            raise ValueError(
                f"embargo_pct must be in [0, 1), got {embargo_pct}"
            )

        self.mode = mode
        self.train_size = train_size
        self.test_size = test_size
        self.step_size = step_size if step_size is not None else test_size
        self.embargo_pct = embargo_pct
        self.t1 = t1

    def get_n_splits(self, index: pd.DatetimeIndex) -> int:
        """Return the number of folds this splitter will produce.

        Why we count by iteration rather than a closed-form expression:
        when `t1` is provided, some folds may be skipped (purged training
        set becomes empty). Counting by iteration is always correct.
        """
        return sum(1 for _ in self.split(index))

    def split(self, index: pd.DatetimeIndex) -> Iterator[WalkForwardSplit]:
        """Yield successive WalkForwardSplit instances.

        Why we iterate by positional offset (not by timestamp slicing):
        pandas timestamp slicing is closed-on-both-ends and ambiguous when
        the requested boundary falls between bars. Positional integer
        slicing is exact and unambiguous, which matters for reproducibility.
        """
        n = len(index)
        if n == 0:
            raise ValueError("index is empty")
        if not index.is_monotonic_increasing:
            raise ValueError("index must be monotonically increasing")
        if self.t1 is not None and len(self.t1) != n:
            raise ValueError(
                f"t1 length {len(self.t1)} does not match index length {n}"
            )

        embargo_gap = int(self.embargo_pct * n)
        fold_id = 0
        offset = 0

        while True:
            if self.mode == "rolling":
                train_start_pos = offset
                train_end_pos = offset + self.train_size
            else:  # anchored
                train_start_pos = 0
                train_end_pos = self.train_size + offset

            test_start_pos = train_end_pos + embargo_gap
            test_end_pos = test_start_pos + self.test_size

            # Stop when the test window would run off the end of the data.
            if test_end_pos > n:
                break
            # Defensive: training must be non-empty before purging.
            if train_end_pos <= train_start_pos:
                break

            train_idx = np.arange(train_start_pos, train_end_pos)
            test_idx = np.arange(test_start_pos, test_end_pos)

            # Apply t1 purge if provided: drop training samples whose label
            # end time reaches at or past the test window's start. We use
            # strict-less-than so a label ending exactly at the test_start
            # bar (which would be observed at the same time as the test
            # signal forms) is purged.
            #
            # Why .iloc on the Series rather than .values: pandas .values on
            # a tz-aware datetime Series strips the timezone (returning a
            # tz-naive numpy.datetime64 array), which then refuses to
            # compare against the tz-aware scalar from `index[...]`.
            # Working on the Series preserves tz semantics.
            if self.t1 is not None:
                test_start_ts = index[test_start_pos]
                train_t1 = self.t1.iloc[train_idx]
                keep_mask = (train_t1 < test_start_ts).to_numpy()
                train_idx = train_idx[keep_mask]

            if len(train_idx) == 0:
                # All of train was purged — skip this fold instead of
                # yielding a degenerate split.
                offset += self.step_size
                continue

            yield WalkForwardSplit(
                fold_id=fold_id,
                train_idx=train_idx,
                test_idx=test_idx,
                train_start=index[train_idx[0]],
                train_end=index[train_idx[-1]],
                test_start=index[test_idx[0]],
                test_end=index[test_idx[-1]],
            )
            fold_id += 1
            offset += self.step_size