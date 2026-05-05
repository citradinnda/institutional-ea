from __future__ import annotations

"""H019 stateful Donchian + Chandelier lifecycle.

H019 is a new hypothesis identity, not a patch to H017.

Core semantic change from H017:
    H017 holds Donchian direction continuously until an opposite breakout.
    H019 treats Donchian as an entry/flip trigger and Chandelier as an
    active same-side exit/flatline condition.

First implementation scope:
    - Pure H4 state machine.
    - Close-based stop-state flattening.
    - No M1 intrabar fill simulation here.
    - No event-engine changes here.
    - No real-data validation here.

Entry rule:
    Enter only when the held Donchian signal changes into a nonzero side:
        0 -> +1, 0 -> -1, -1 -> +1, +1 -> -1.

Exit rule:
    If long and close <= long Chandelier stop, flatten.
    If short and close >= short Chandelier stop, flatten.

Re-entry rule:
    After stop-out, do not re-enter from the same stale held Donchian
    direction. Re-entry requires a fresh visible Donchian side change.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class H019LifecycleResult:
    """Output from the H019 single-symbol lifecycle state machine."""

    signals: pd.Series
    selected_stops: pd.Series
    entries: pd.Series
    exits: pd.Series


def _validate_aligned_series(
    *,
    held_signal: pd.Series,
    close: pd.Series,
    stops_long: pd.Series,
    stops_short: pd.Series,
) -> None:
    if not isinstance(held_signal, pd.Series):
        raise TypeError("held_signal must be a pandas Series.")
    if not isinstance(close, pd.Series):
        raise TypeError("close must be a pandas Series.")
    if not isinstance(stops_long, pd.Series):
        raise TypeError("stops_long must be a pandas Series.")
    if not isinstance(stops_short, pd.Series):
        raise TypeError("stops_short must be a pandas Series.")

    if not isinstance(held_signal.index, pd.DatetimeIndex):
        raise TypeError("held_signal.index must be a DatetimeIndex.")
    if not held_signal.index.equals(close.index):
        raise ValueError("close.index must equal held_signal.index.")
    if not held_signal.index.equals(stops_long.index):
        raise ValueError("stops_long.index must equal held_signal.index.")
    if not held_signal.index.equals(stops_short.index):
        raise ValueError("stops_short.index must equal held_signal.index.")

    if held_signal.index.has_duplicates:
        raise ValueError("held_signal.index has duplicates.")
    if not held_signal.index.is_monotonic_increasing:
        raise ValueError("held_signal.index must be sorted ascending.")


def apply_h019_chandelier_lifecycle(
    *,
    held_signal: pd.Series,
    close: pd.Series,
    stops_long: pd.Series,
    stops_short: pd.Series,
) -> H019LifecycleResult:
    """Apply H019 stateful same-side Chandelier exit semantics.

    Args:
        held_signal: Existing Donchian held signal in {-1, 0, +1, NaN}.
            NaN is treated as warm-up/flat for state transitions.
        close: H4 close prices aligned to held_signal.
        stops_long: Long-side Chandelier stop panel aligned to held_signal.
        stops_short: Short-side Chandelier stop panel aligned to held_signal.

    Returns:
        H019LifecycleResult:
            signals:
                Stateful H019 active side in {-1.0, 0.0, +1.0}.
            selected_stops:
                Same-side active stop while in position, else NaN.
            entries:
                True on bars where H019 enters/flips into a nonzero side.
            exits:
                True on bars where H019 flattens because the active
                same-side Chandelier stop was breached at H4 close.

    Notes:
        This function intentionally does not use the opposite stop panel
        to rescue invalid same-side stop geometry.
    """
    _validate_aligned_series(
        held_signal=held_signal,
        close=close,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    index = held_signal.index
    out_signal = pd.Series(0.0, index=index, name="h019_signal", dtype="float64")
    selected_stops = pd.Series(np.nan, index=index, name="h019_selected_stop")
    entries = pd.Series(False, index=index, name="h019_entry")
    exits = pd.Series(False, index=index, name="h019_exit")

    active_side = 0
    previous_observed_signal = 0

    for ts in index:
        raw_value = held_signal.at[ts]
        observed_signal = 0 if pd.isna(raw_value) else int(np.sign(raw_value))

        if observed_signal not in (-1, 0, 1):
            raise ValueError(
                f"held_signal contains unsupported value {raw_value!r} at {ts}."
            )

        # Exit existing state first using same-side stop only.
        if active_side == 1:
            stop = stops_long.at[ts]
            price = close.at[ts]
            if not pd.isna(stop) and not pd.isna(price) and price <= stop:
                active_side = 0
                exits.at[ts] = True
        elif active_side == -1:
            stop = stops_short.at[ts]
            price = close.at[ts]
            if not pd.isna(stop) and not pd.isna(price) and price >= stop:
                active_side = 0
                exits.at[ts] = True

        # Enter only on a fresh visible Donchian side change.
        signal_changed = observed_signal != previous_observed_signal
        fresh_nonzero_side = observed_signal in (-1, 1) and signal_changed

        if fresh_nonzero_side:
            active_side = observed_signal
            entries.at[ts] = True

        out_signal.at[ts] = float(active_side)

        if active_side == 1:
            selected_stops.at[ts] = stops_long.at[ts]
        elif active_side == -1:
            selected_stops.at[ts] = stops_short.at[ts]

        previous_observed_signal = observed_signal

    return H019LifecycleResult(
        signals=out_signal,
        selected_stops=selected_stops,
        entries=entries,
        exits=exits,
    )