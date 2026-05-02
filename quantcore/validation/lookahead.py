from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence, Union

import numpy as np
import pandas as pd

# A feature function takes an OHLCV DataFrame and returns either a
# Series (single feature) or a DataFrame (multiple features) aligned
# to the input's index. We accept both because realistic feature
# pipelines emit bundles, not just one column at a time.
FeatureOutput = Union[pd.Series, pd.DataFrame]
FeatureFn = Callable[[pd.DataFrame], FeatureOutput]


@dataclass(frozen=True)
class LookaheadViolation:
    """A single point where past values changed when future data was withheld.

    Why we record per-violation context: when a feature fails, the
    researcher needs to know WHICH column, at WHICH index, by HOW
    MUCH. 'It failed' is not actionable. 'Column ema_20 at row 14
    changed by 3.7e-3 when bars 15+ were withheld' is actionable
    and points straight at the offending operation.
    """

    truncation_length: int   # we ran f on df[:truncation_length]
    column: str              # which output column drifted ("" for unnamed Series)
    position: int            # row index (positional, 0-based) where drift was found
    full_value: float        # value when f saw the whole series
    truncated_value: float   # value when f saw only the prefix
    abs_diff: float          # absolute difference


@dataclass(frozen=True)
class LookaheadReport:
    """Result of a lookahead audit.

    `clean` is the gate. `violations` is for diagnosis. `n_checks`
    documents how thoroughly we audited so reviewers can judge
    whether absence of violations is meaningful or just under-tested.
    """

    clean: bool
    n_checks: int
    truncation_lengths: tuple[int, ...]
    violations: tuple[LookaheadViolation, ...] = field(default_factory=tuple)

    def summary(self) -> str:
        if self.clean:
            return (
                f"LOOKAHEAD CLEAN across {self.n_checks} truncation(s): "
                f"{self.truncation_lengths}"
            )
        first = self.violations[0]
        return (
            f"LOOKAHEAD VIOLATION: {len(self.violations)} drift(s) found. "
            f"First: column={first.column!r} pos={first.position} "
            f"trunc_len={first.truncation_length} "
            f"full={first.full_value!r} trunc={first.truncated_value!r} "
            f"abs_diff={first.abs_diff:.3e}"
        )


def _to_dataframe(out: FeatureOutput, fallback_name: str = "feature") -> pd.DataFrame:
    """Normalize feature output to a DataFrame so comparison logic is uniform."""
    if isinstance(out, pd.DataFrame):
        return out
    if isinstance(out, pd.Series):
        name = out.name if out.name is not None else fallback_name
        return out.to_frame(name=name)
    raise TypeError(
        f"Feature function must return Series or DataFrame, got {type(out).__name__}"
    )


def _default_truncations(n: int) -> list[int]:
    """Pick a reasonable spread of truncation lengths for an n-row input.

    Why these specific points: we want to test EARLY (where many
    features are still warming up and most likely to misbehave),
    MIDDLE (steady state), and LATE (just before the end, where
    off-by-one shift bugs hide). Three points is the minimum
    that triangulates all three regimes; the caller can pass more.
    """
    if n < 4:
        # Pathologically small — only test what makes sense.
        return [max(2, n - 1)]
    candidates = sorted(
        {
            max(2, n // 4),       # early
            n // 2,               # middle
            max(2, (3 * n) // 4), # late
            n - 1,                # last possible truncation
        }
    )
    return [c for c in candidates if 2 <= c < n]


def assert_no_lookahead(
    feature_fn: FeatureFn,
    df: pd.DataFrame,
    *,
    truncation_lengths: Sequence[int] | None = None,
    atol: float = 1e-10,
    rtol: float = 0.0,
    raise_on_violation: bool = True,
) -> LookaheadReport:
    """Verify that `feature_fn` does not use future information.

    The contract:
      1. Run `feature_fn(df)` on the full input. Call this F.
      2. For each k in `truncation_lengths`, run `feature_fn(df.iloc[:k])`.
         Call this F_k.
      3. Assert that F.iloc[:k] equals F_k, cell-by-cell, within tolerance.
         NaNs in matching positions are treated as equal (NaN is the
         CORRECT output for a warmup bar).

    Why NaN==NaN here: features like rolling means legitimately produce
    NaN for the first `window-1` bars. Treating NaN!=NaN (the IEEE
    default) would falsely flag every well-behaved warmup region as
    a violation. We only flag a violation when one side is NaN and
    the other is a real number, OR when both are real and differ.

    Why `atol=1e-10` default and not stricter: pandas/numpy can
    produce bit-level differences in floating point depending on
    chunk boundaries (e.g. summation order in rolling ops). 1e-10
    is far below any economically meaningful price movement on
    USDJPY or XAUUSD and far above floating-point noise.

    Args:
        feature_fn: a function df -> Series or DataFrame.
        df: canonical OHLCV input (or any DataFrame with a meaningful index).
        truncation_lengths: which prefix lengths to test. Defaults to
            an early/middle/late spread.
        atol: absolute tolerance for value comparison.
        rtol: relative tolerance (added to atol * abs(reference)).
        raise_on_violation: if True (default), raise AssertionError
            on first violation set so test suites fail loudly. If False,
            return the report regardless — useful for CI dashboards
            that want to enumerate all problems at once.

    Returns:
        LookaheadReport. Always, unless raise_on_violation triggers.

    Raises:
        AssertionError: if violations are found and raise_on_violation=True.
        TypeError: if feature_fn returns the wrong type.
        ValueError: if df is empty or truncation_lengths are invalid.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"df must be a pandas DataFrame, got {type(df).__name__}")
    n = len(df)
    if n < 2:
        raise ValueError(f"df must have at least 2 rows for a lookahead test, got {n}")

    trunc_list = (
        list(truncation_lengths)
        if truncation_lengths is not None
        else _default_truncations(n)
    )
    for k in trunc_list:
        if not isinstance(k, (int, np.integer)):
            raise ValueError(f"truncation length must be int, got {type(k).__name__}")
        if k < 2 or k >= n:
            raise ValueError(
                f"truncation length {k} out of range; must satisfy 2 <= k < {n}"
            )

    # --- Reference run on full input ---
    full_out = _to_dataframe(feature_fn(df))
    if len(full_out) != n:
        raise ValueError(
            f"feature_fn output length {len(full_out)} != input length {n}; "
            "feature functions must preserve the index."
        )

    violations: list[LookaheadViolation] = []

    for k in trunc_list:
        trunc_out = _to_dataframe(feature_fn(df.iloc[:k]))
        if len(trunc_out) != k:
            raise ValueError(
                f"feature_fn on truncated input of length {k} returned "
                f"length {len(trunc_out)}; must equal input length."
            )

        # Align columns (the truncated run must produce the same schema)
        if list(trunc_out.columns) != list(full_out.columns):
            raise ValueError(
                "feature_fn produced different columns on truncated input. "
                f"Full: {list(full_out.columns)}, Truncated@{k}: {list(trunc_out.columns)}"
            )

        full_prefix = full_out.iloc[:k]

        for col in full_out.columns:
            a = full_prefix[col].to_numpy()
            b = trunc_out[col].to_numpy()

            # NaN-aware comparison.
            a_nan = pd.isna(a)
            b_nan = pd.isna(b)

            # Mismatch in NaN-ness is always a violation.
            nan_mismatch = a_nan ^ b_nan
            if nan_mismatch.any():
                for pos in np.where(nan_mismatch)[0]:
                    violations.append(
                        LookaheadViolation(
                            truncation_length=k,
                            column=str(col),
                            position=int(pos),
                            full_value=float(a[pos]) if not a_nan[pos] else float("nan"),
                            truncated_value=float(b[pos]) if not b_nan[pos] else float("nan"),
                            abs_diff=float("inf"),
                        )
                    )

            # For positions where both are real, compare numerically.
            both_real = ~(a_nan | b_nan)
            if both_real.any():
                a_r = a[both_real].astype(float, copy=False)
                b_r = b[both_real].astype(float, copy=False)
                diff = np.abs(a_r - b_r)
                tol = atol + rtol * np.abs(a_r)
                bad = diff > tol
                if bad.any():
                    real_positions = np.where(both_real)[0]
                    for local_idx in np.where(bad)[0]:
                        pos = int(real_positions[local_idx])
                        violations.append(
                            LookaheadViolation(
                                truncation_length=k,
                                column=str(col),
                                position=pos,
                                full_value=float(a[pos]),
                                truncated_value=float(b[pos]),
                                abs_diff=float(diff[local_idx]),
                            )
                        )

    report = LookaheadReport(
        clean=(len(violations) == 0),
        n_checks=len(trunc_list) * len(full_out.columns),
        truncation_lengths=tuple(trunc_list),
        violations=tuple(violations),
    )

    if not report.clean and raise_on_violation:
        raise AssertionError(report.summary())

    return report