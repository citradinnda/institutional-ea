from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import pandas as pd

from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, load_mt5_csv
from quantcore.strategy.h024 import H024SignalConfig, _wilder_atr
from scripts.run_h020_strict_event_real import USDJPY_H4_PATH, XAUUSD_H4_PATH


BROKER_TO_MODEL_SYMBOL = {
    "USDJPYm": "USDJPY",
    "XAUUSDm": "XAUUSD",
}

FLOAT_FIELDS = (
    "slow_ma",
    "slow_ma_lag",
    "atr",
    "previous_atr",
    "slope",
    "slope_threshold",
    "recent_high_before_signal",
    "recent_low_before_signal",
    "long_pullback_depth_atr",
    "short_pullback_depth_atr",
)

BOOL_FIELDS = (
    "trend_up",
    "trend_down",
    "previous_bearish",
    "previous_bullish",
    "long_pullback_ok",
    "short_pullback_ok",
    "long_resumption",
    "short_resumption",
    "long_signal_observed",
    "short_signal_observed",
)

INT_FIELDS = (
    "h4_warmup_bars",
    "slow_window",
    "slope_lag",
    "atr_window",
    "pullback_window",
)

DEFAULT_FLOAT_TOLERANCE = 1e-8


@dataclass(frozen=True)
class StateObservationParityResult:
    rows_checked: int
    comparisons: int
    violations: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.violations


def parse_h024_state_detail(detail: str) -> dict[str, str]:
    if detail.startswith("unavailable:"):
        raise ValueError(f"state observation unavailable: {detail}")

    parsed: dict[str, str] = {}
    for part in detail.split(";"):
        if not part:
            continue
        if "=" not in part:
            raise ValueError(f"malformed detail fragment: {part!r}")
        key, value = part.split("=", 1)
        parsed[key] = value

    return parsed


def mt5_server_time_to_utc(value: str, broker_tz: str = DEFAULT_BROKER_TZ) -> pd.Timestamp:
    naive = pd.to_datetime(value, format="%Y.%m.%d %H:%M:%S")
    index = pd.DatetimeIndex([naive])
    if broker_tz == "UTC":
        return index.tz_localize("UTC")[0]
    return index.tz_localize(
        broker_tz,
        ambiguous=False,
        nonexistent="shift_forward",
    ).tz_convert("UTC")[0]


def compute_h024_state_for_closed_bar(
    bars: pd.DataFrame,
    closed_h4_time_utc: pd.Timestamp,
    *,
    h4_warmup_bars: int,
    config: H024SignalConfig | None = None,
) -> dict[str, float | bool | int]:
    if h4_warmup_bars <= 0:
        raise ValueError("h4_warmup_bars must be positive")
    if not isinstance(bars.index, pd.DatetimeIndex):
        raise ValueError("bars must use a DatetimeIndex")
    if bars.index.tz is None:
        raise ValueError("bars index must be timezone-aware UTC")

    resolved = config or H024SignalConfig()
    window = bars.loc[bars.index <= closed_h4_time_utc].tail(h4_warmup_bars)
    if window.empty or window.index[-1] != closed_h4_time_utc:
        earliest = bars.index.min() if not bars.empty else "<empty>"
        latest = bars.index.max() if not bars.empty else "<empty>"
        raise ValueError(
            "closed H4 timestamp not found in bars: "
            f"{closed_h4_time_utc}; available range: {earliest} to {latest}"
        )

    open_ = window["open"].astype(float)
    high = window["high"].astype(float)
    low = window["low"].astype(float)
    close = window["close"].astype(float)

    slow_ma = close.rolling(
        resolved.slow_window,
        min_periods=resolved.slow_window,
    ).mean()
    atr = _wilder_atr(window, resolved.atr_window)

    slope = slow_ma - slow_ma.shift(resolved.slope_lag)
    slope_threshold = atr * resolved.min_slope_atr

    trend_up = (close > slow_ma) & (slope > slope_threshold)
    trend_down = (close < slow_ma) & (slope < -slope_threshold)

    previous_bearish = close.shift(1) < open_.shift(1)
    previous_bullish = close.shift(1) > open_.shift(1)

    recent_high_before_signal = high.shift(1).rolling(
        resolved.pullback_window,
        min_periods=resolved.pullback_window,
    ).max()
    recent_low_before_signal = low.shift(1).rolling(
        resolved.pullback_window,
        min_periods=resolved.pullback_window,
    ).min()

    long_pullback_depth_atr = (recent_high_before_signal - low.shift(1)) / atr.shift(1)
    short_pullback_depth_atr = (high.shift(1) - recent_low_before_signal) / atr.shift(1)

    long_pullback_ok = long_pullback_depth_atr.between(
        resolved.min_pullback_atr,
        resolved.max_pullback_atr,
        inclusive="both",
    )
    short_pullback_ok = short_pullback_depth_atr.between(
        resolved.min_pullback_atr,
        resolved.max_pullback_atr,
        inclusive="both",
    )

    long_resumption = close > high.shift(1)
    short_resumption = close < low.shift(1)

    long_signal = trend_up & previous_bearish & long_pullback_ok & long_resumption
    short_signal = trend_down & previous_bullish & short_pullback_ok & short_resumption

    last = window.index[-1]
    previous = window.index[-2] if len(window) >= 2 else last

    return {
        "h4_warmup_bars": h4_warmup_bars,
        "slow_window": resolved.slow_window,
        "slope_lag": resolved.slope_lag,
        "atr_window": resolved.atr_window,
        "pullback_window": resolved.pullback_window,
        "slow_ma": float(slow_ma.loc[last]),
        "slow_ma_lag": float(slow_ma.shift(resolved.slope_lag).loc[last]),
        "atr": float(atr.loc[last]),
        "previous_atr": float(atr.loc[previous]),
        "slope": float(slope.loc[last]),
        "slope_threshold": float(slope_threshold.loc[last]),
        "trend_up": bool(trend_up.loc[last]),
        "trend_down": bool(trend_down.loc[last]),
        "previous_bearish": bool(previous_bearish.loc[last]),
        "previous_bullish": bool(previous_bullish.loc[last]),
        "recent_high_before_signal": float(recent_high_before_signal.loc[last]),
        "recent_low_before_signal": float(recent_low_before_signal.loc[last]),
        "long_pullback_depth_atr": float(long_pullback_depth_atr.loc[last]),
        "short_pullback_depth_atr": float(short_pullback_depth_atr.loc[last]),
        "long_pullback_ok": bool(long_pullback_ok.loc[last]),
        "short_pullback_ok": bool(short_pullback_ok.loc[last]),
        "long_resumption": bool(long_resumption.loc[last]),
        "short_resumption": bool(short_resumption.loc[last]),
        "long_signal_observed": bool(long_signal.loc[last]),
        "short_signal_observed": bool(short_signal.loc[last]),
    }


def verify_h024_ea_state_observation_parity(
    log_path: Path,
    *,
    h4_bars_by_symbol: Mapping[str, pd.DataFrame],
    tolerance: float = DEFAULT_FLOAT_TOLERANCE,
) -> StateObservationParityResult:
    violations: list[str] = []
    rows_checked = 0
    comparisons = 0

    if not log_path.exists():
        return StateObservationParityResult(
            rows_checked=0,
            comparisons=0,
            violations=(f"missing log file: {log_path}",),
        )

    with log_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row_number, row in enumerate(reader, start=2):
            if row.get("event") != "H024_STATE_OBSERVATION":
                continue

            rows_checked += 1
            broker_symbol = row.get("symbol", "")
            model_symbol = BROKER_TO_MODEL_SYMBOL.get(broker_symbol)
            if model_symbol is None:
                violations.append(f"row {row_number}: unexpected broker symbol {broker_symbol!r}")
                continue
            if model_symbol not in h4_bars_by_symbol:
                violations.append(f"row {row_number}: missing H4 bars for {model_symbol}")
                continue

            try:
                detail = parse_h024_state_detail(row.get("detail", ""))
                closed_time = mt5_server_time_to_utc(detail["closed_h4_time"])
                warmup_bars = int(detail["h4_warmup_bars"])
                expected = compute_h024_state_for_closed_bar(
                    h4_bars_by_symbol[model_symbol],
                    closed_time,
                    h4_warmup_bars=warmup_bars,
                )
            except Exception as exc:
                violations.append(f"row {row_number}: failed to compute expected state: {exc}")
                continue

            for field in INT_FIELDS:
                comparisons += 1
                actual = int(detail[field])
                if actual != expected[field]:
                    violations.append(
                        f"row {row_number} {model_symbol} {field}: actual {actual} != expected {expected[field]}"
                    )

            for field in FLOAT_FIELDS:
                comparisons += 1
                actual = float(detail[field])
                expected_value = float(expected[field])
                if abs(actual - expected_value) > tolerance:
                    violations.append(
                        f"row {row_number} {model_symbol} {field}: "
                        f"actual {actual:.12f} != expected {expected_value:.12f}"
                    )

            for field in BOOL_FIELDS:
                comparisons += 1
                actual = detail[field].lower()
                expected_value = "true" if expected[field] else "false"
                if actual != expected_value:
                    violations.append(
                        f"row {row_number} {model_symbol} {field}: actual {actual!r} != expected {expected_value!r}"
                    )

    if rows_checked == 0:
        violations.append("log has no H024_STATE_OBSERVATION rows")

    return StateObservationParityResult(
        rows_checked=rows_checked,
        comparisons=comparisons,
        violations=tuple(violations),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify parity between EA H024_STATE_OBSERVATION rows and Python H024 state calculations."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to h024_ea_log_only_preflight.csv",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_FLOAT_TOLERANCE,
        help="Absolute tolerance for numeric state fields.",
    )
    args = parser.parse_args()

    usdjpy_h4 = load_mt5_csv(USDJPY_H4_PATH)
    xauusd_h4 = load_mt5_csv(XAUUSD_H4_PATH)

    result = verify_h024_ea_state_observation_parity(
        args.path,
        h4_bars_by_symbol={
            "USDJPY": usdjpy_h4.bars,
            "XAUUSD": xauusd_h4.bars,
        },
        tolerance=args.tolerance,
    )

    print("H024 EA state observation parity verifier")
    print("=" * 72)
    print(f"Rows checked: {result.rows_checked}")
    print(f"Comparisons: {result.comparisons}")
    print(f"Violations: {len(result.violations)}")
    for violation in result.violations:
        print(f"- {violation}")
    print()
    print(f"Verdict: {'PASS' if result.passed else 'FAIL'}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
