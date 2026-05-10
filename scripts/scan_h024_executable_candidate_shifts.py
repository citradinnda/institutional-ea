"""Scan H024 historical H4 rows for executable dry-run candidate shifts.

Research only. No demo/live/Phase 4 approval.
Pure Python. Broker-native H4 CSV read only.
No MT5 access. No order execution.

This scanner answers a narrow question:

    Does the current H024 + H020 sizing bridge contain any historical H4
    decision row that remains executable at the requested balance/risk settings?

It deliberately does not use the older M1 accepted-window guard because the
purpose here is only to locate candidate closed-H4 replay shifts for log-only
runtime reconstruction. Any candidate found here still requires separate runtime
CSV replay and dry-run reconciliation before execution work may proceed.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Mapping

import pandas as pd

from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h020 import H020SizingConfig, generate_h020_intent_panel
from quantcore.strategy.h024 import generate_h024_signals
from quantcore.strategy.h024_runner import (
    H024BridgeConfig,
    _common_h4_index,
    _require_h4_frame,
    _validate_h024_bridge_config,
    _wilder_atr,
    run_h024_bridge_shim,
)
from scripts.run_h020_strict_event_real import USDJPY_H4_PATH, XAUUSD_H4_PATH


DEFAULT_OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "reports"
    / "h024_executable_candidate_shifts.csv"
)


@dataclass(frozen=True)
class ExecutableCandidateShift:
    symbol: str
    side: str
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    ea_closed_shift_from_latest_common_h4: int
    signal_signed_risk_fraction: float
    final_signed_risk_fraction: float
    entry_price: float
    stop_price: float
    stop_distance: float


@dataclass(frozen=True)
class H024ExecutableCandidateScanInputs:
    index: pd.DatetimeIndex
    h4_by_symbol: Mapping[str, pd.DataFrame]
    positions: pd.DataFrame
    signals: pd.DataFrame
    stops_long: pd.DataFrame
    stops_short: pd.DataFrame
    sizing_config: H020SizingConfig


def _finite_nonzero(value: object) -> bool:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(numeric) and not math.isclose(numeric, 0.0, abs_tol=1e-15)


def scan_bridge_result_for_executable_shifts(
    *,
    bridge_result: object,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
) -> list[ExecutableCandidateShift]:
    positions = bridge_result.positions
    signals = bridge_result.signals
    stops_long = bridge_result.stops_long
    stops_short = bridge_result.stops_short

    h4_by_symbol = {
        "USDJPY": usdjpy_h4.reindex(positions.index),
        "XAUUSD": xauusd_h4.reindex(positions.index),
    }

    candidates: list[ExecutableCandidateShift] = []
    index = list(pd.DatetimeIndex(positions.index))

    # H020 bridge opens at t+1, so the final row cannot produce an entry row.
    for row_number, decision_time in enumerate(index[:-1]):
        entry_time = index[row_number + 1]
        ea_closed_shift = len(index) - row_number

        for symbol in ("USDJPY", "XAUUSD"):
            final_signed_risk = positions.at[decision_time, symbol]
            if not _finite_nonzero(final_signed_risk):
                continue

            signal_signed_risk = float(signals.at[decision_time, symbol])
            side = "buy" if float(final_signed_risk) > 0 else "sell"
            stop_price = (
                float(stops_long.at[decision_time, symbol])
                if side == "buy"
                else float(stops_short.at[decision_time, symbol])
            )
            entry_price = float(h4_by_symbol[symbol].at[entry_time, "open"])
            stop_distance = abs(entry_price - stop_price)

            if not all(
                math.isfinite(value) and value > 0
                for value in (entry_price, stop_price, stop_distance)
            ):
                continue

            candidates.append(
                ExecutableCandidateShift(
                    symbol=symbol,
                    side=side,
                    decision_time=pd.Timestamp(decision_time),
                    entry_time=pd.Timestamp(entry_time),
                    ea_closed_shift_from_latest_common_h4=ea_closed_shift,
                    signal_signed_risk_fraction=signal_signed_risk,
                    final_signed_risk_fraction=float(final_signed_risk),
                    entry_price=entry_price,
                    stop_price=stop_price,
                    stop_distance=stop_distance,
                )
            )

    return candidates


def build_h024_executable_candidate_scan_inputs(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    config: H024BridgeConfig | None = None,
) -> H024ExecutableCandidateScanInputs:
    """Build reusable H024 signal/stop geometry for repeated H020 sizing scans."""

    cfg = config or H024BridgeConfig()
    _validate_h024_bridge_config(cfg)

    raw_h4_by_symbol = {
        "USDJPY": _require_h4_frame(usdjpy_h4, "USDJPY"),
        "XAUUSD": _require_h4_frame(xauusd_h4, "XAUUSD"),
    }
    common_index = _common_h4_index(raw_h4_by_symbol)

    h4_by_symbol = {
        symbol: frame.reindex(common_index).copy()
        for symbol, frame in raw_h4_by_symbol.items()
    }

    positions = pd.DataFrame(0.0, index=common_index, columns=["USDJPY", "XAUUSD"])
    signals = pd.DataFrame(0.0, index=common_index, columns=["USDJPY", "XAUUSD"])
    stops_long = pd.DataFrame(float("nan"), index=common_index, columns=["USDJPY", "XAUUSD"])
    stops_short = pd.DataFrame(float("nan"), index=common_index, columns=["USDJPY", "XAUUSD"])

    for symbol, raw_frame in raw_h4_by_symbol.items():
        raw_signals = generate_h024_signals(raw_frame, config=cfg.signal_config)
        signed_signals = raw_signals.astype(float) * float(cfg.signed_risk_fraction)
        aligned_signals = signed_signals.reindex(common_index).fillna(0.0)

        signals[symbol] = aligned_signals
        positions[symbol] = aligned_signals

        atr = _wilder_atr(raw_frame, cfg.atr_window).reindex(common_index)
        stop_distance = atr * float(cfg.stop_atr_multiple)
        close = h4_by_symbol[symbol]["close"].astype(float)

        stops_long[symbol] = close - stop_distance
        stops_short[symbol] = close + stop_distance

    return H024ExecutableCandidateScanInputs(
        index=common_index,
        h4_by_symbol=h4_by_symbol,
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
        sizing_config=cfg.sizing_config,
    )


def scan_h024_candidate_inputs_for_executable_shifts(
    *,
    scan_inputs: H024ExecutableCandidateScanInputs,
    balance: float,
) -> list[ExecutableCandidateShift]:
    """Scan precomputed H024 geometry through H020 sizing at one balance."""

    if balance <= 0:
        raise ValueError("balance must be positive")

    panels = generate_h020_intent_panel(
        positions=scan_inputs.positions,
        stops_long=scan_inputs.stops_long,
        stops_short=scan_inputs.stops_short,
        h4_by_symbol=scan_inputs.h4_by_symbol,
        equity_usd=float(balance),
        config=scan_inputs.sizing_config,
    )

    row_by_decision = {
        pd.Timestamp(timestamp): row_number
        for row_number, timestamp in enumerate(scan_inputs.index[:-1])
    }

    candidates: list[ExecutableCandidateShift] = []
    for panel in panels:
        row_number = row_by_decision.get(pd.Timestamp(panel.decision_time))
        if row_number is None:
            continue

        ea_closed_shift = len(scan_inputs.index) - row_number

        for symbol in ("USDJPY", "XAUUSD"):
            intent = panel.intents.get(symbol)
            if intent is None or intent.suppressed or intent.side is None:
                continue

            entry_price = float(intent.entry_raw_price)
            stop_price = float(intent.stop_price)
            stop_distance = float(intent.raw_stop_distance)

            if not all(
                math.isfinite(value) and value > 0.0
                for value in (entry_price, stop_price, stop_distance)
            ):
                continue

            candidates.append(
                ExecutableCandidateShift(
                    symbol=symbol,
                    side=intent.side,
                    decision_time=pd.Timestamp(panel.decision_time),
                    entry_time=pd.Timestamp(panel.entry_time),
                    ea_closed_shift_from_latest_common_h4=ea_closed_shift,
                    signal_signed_risk_fraction=float(intent.signed_risk_fraction),
                    final_signed_risk_fraction=float(intent.final_signed_risk_fraction),
                    entry_price=entry_price,
                    stop_price=stop_price,
                    stop_distance=stop_distance,
                )
            )

    return candidates


def build_real_h4_executable_candidate_provider(
    *,
    risk_fraction: float,
) -> Callable[[float], list[ExecutableCandidateShift]]:
    """Load broker-native H4 once and return a balance -> candidates provider."""

    if risk_fraction <= 0 or risk_fraction > 1:
        raise ValueError("risk_fraction must be in (0, 1]")

    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH],
        label="broker-native MT5 H4 exports",
    )

    usdjpy_h4 = load_mt5_csv(USDJPY_H4_PATH).bars
    xauusd_h4 = load_mt5_csv(XAUUSD_H4_PATH).bars
    scan_inputs = build_h024_executable_candidate_scan_inputs(
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        config=H024BridgeConfig(signed_risk_fraction=float(risk_fraction)),
    )

    cache: dict[float, list[ExecutableCandidateShift]] = {}

    def provider(balance: float) -> list[ExecutableCandidateShift]:
        if balance <= 0:
            raise ValueError("balance must be positive")
        key = float(balance)
        if key not in cache:
            cache[key] = scan_h024_candidate_inputs_for_executable_shifts(
                scan_inputs=scan_inputs,
                balance=key,
            )
        return cache[key]

    return provider


def scan_real_h4_exports(
    *,
    balance: float,
    risk_fraction: float,
) -> list[ExecutableCandidateShift]:
    provider = build_real_h4_executable_candidate_provider(
        risk_fraction=float(risk_fraction),
    )
    return provider(float(balance))


def write_candidates_csv(
    *,
    candidates: Iterable[ExecutableCandidateShift],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(candidates)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "symbol",
                "side",
                "decision_time",
                "entry_time",
                "ea_closed_shift_from_latest_common_h4",
                "signal_signed_risk_fraction",
                "final_signed_risk_fraction",
                "entry_price",
                "stop_price",
                "stop_distance",
            ],
        )
        writer.writeheader()
        for candidate in rows:
            writer.writerow(
                {
                    "symbol": candidate.symbol,
                    "side": candidate.side,
                    "decision_time": candidate.decision_time.isoformat(),
                    "entry_time": candidate.entry_time.isoformat(),
                    "ea_closed_shift_from_latest_common_h4": (
                        candidate.ea_closed_shift_from_latest_common_h4
                    ),
                    "signal_signed_risk_fraction": (
                        f"{candidate.signal_signed_risk_fraction:.12f}"
                    ),
                    "final_signed_risk_fraction": (
                        f"{candidate.final_signed_risk_fraction:.12f}"
                    ),
                    "entry_price": f"{candidate.entry_price:.10f}",
                    "stop_price": f"{candidate.stop_price:.10f}",
                    "stop_distance": f"{candidate.stop_distance:.10f}",
                }
            )


def print_summary(
    *,
    candidates: list[ExecutableCandidateShift],
    balance: float,
    risk_fraction: float,
    output_path: Path,
    max_rows: int,
) -> int:
    print("H024 executable candidate shift scan")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("Pure Python. Broker-native H4 CSV read only.")
    print("No MT5 access. No order execution.")
    print()
    print(f"balance: {balance:.2f}")
    print(f"risk_fraction: {risk_fraction:.6f}")
    print(f"executable_candidate_rows: {len(candidates)}")
    print(f"wrote: {output_path}")
    print()

    if not candidates:
        print("Verdict: PASS")
        print("Scan completed; no executable candidate shifts found at these settings.")
        return 0

    print("First candidate rows:")
    for candidate in candidates[:max_rows]:
        print(
            f"{candidate.symbol} {candidate.side} | "
            f"decision={candidate.decision_time} "
            f"entry={candidate.entry_time} "
            f"ea_closed_shift={candidate.ea_closed_shift_from_latest_common_h4} "
            f"final_risk={candidate.final_signed_risk_fraction:.12f} "
            f"entry_price={candidate.entry_price:.10f} "
            f"stop_price={candidate.stop_price:.10f}"
        )

    print()
    print("Verdict: PASS")
    print("Candidates found only for replay planning; no execution approval implied.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--balance", type=float, required=True)
    parser.add_argument("--risk-fraction", type=float, required=True)
    parser.add_argument("--output-csv", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--max-rows", type=int, default=20)
    args = parser.parse_args()

    candidates = scan_real_h4_exports(
        balance=args.balance,
        risk_fraction=args.risk_fraction,
    )
    write_candidates_csv(candidates=candidates, output_path=args.output_csv)

    return print_summary(
        candidates=candidates,
        balance=args.balance,
        risk_fraction=args.risk_fraction,
        output_path=args.output_csv,
        max_rows=args.max_rows,
    )


if __name__ == "__main__":
    raise SystemExit(main())
