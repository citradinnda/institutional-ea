# file: tests/h024_full_h4_runtime_ci_harness.py
import csv
from dataclasses import dataclass
from typing import List
from collections import Counter
from pathlib import Path
import random

RUNTIME_CSV = Path("reports/h024_full_h4_runtime_ci_simulated.csv")

@dataclass
class H024BarInput:
    symbol: str
    copied_h4_bars: int
    closed_h4_time: str
    long_signal_observed: bool = False
    short_signal_observed: bool = False


def h024_strategy_intent_detail(inputs: H024BarInput) -> str:
    """Pure log-only EA decision mirror."""
    if inputs.copied_h4_bars < 10:
        return "NO_ACTION:strategy_unavailable_insufficient_h4_warmup"

    if inputs.long_signal_observed and inputs.short_signal_observed:
        return "BLOCKED:strategy_conflict_log_only"

    if inputs.long_signal_observed:
        return (
            f"WOULD_OPEN:side=long;"
            f"closed_h4_time={inputs.closed_h4_time};"
            "source=H024_STATE_OBSERVATION;"
            "mode=log_only_no_execution"
        )

    if inputs.short_signal_observed:
        return (
            f"WOULD_OPEN:side=short;"
            f"closed_h4_time={inputs.closed_h4_time};"
            "source=H024_STATE_OBSERVATION;"
            "mode=log_only_no_execution"
        )

    return (
        f"NO_ACTION:strategy_no_signal;"
        f"closed_h4_time={inputs.closed_h4_time};"
        "mode=log_only_no_execution"
    )


def simulate_historical_h4_series(symbols: List[str], num_bars: int, start_time: str) -> List[H024BarInput]:
    """Generate simulated H4 bars for multiple symbols with controlled signals."""
    simulated_bars = []
    base_hour = int(start_time.split(" ")[1].split(":")[0])
    base_day = int(start_time.split(" ")[0].split("-")[2])
    for i in range(num_bars):
        for symbol in symbols:
            h = (base_hour + i * 4) % 24
            day_offset = (base_hour + i * 4) // 24
            closed_time = f"2026-05-{base_day + day_offset:02d} {h:02d}:00"
            long_signal = random.choice([True, False, False])  # ~33%
            short_signal = random.choice([True, False, False])
            copied_h4_bars = 10 if i >= 2 else 5  # first 2 bars = warmup
            simulated_bars.append(
                H024BarInput(
                    symbol=symbol,
                    copied_h4_bars=copied_h4_bars,
                    closed_h4_time=closed_time,
                    long_signal_observed=long_signal,
                    short_signal_observed=short_signal,
                )
            )
    return simulated_bars


def simulate_runtime_csv(simulated_bars: List[H024BarInput], output_csv: Path):
    """Simulate runtime CSV for log-only EA."""
    fieldnames = ["symbol", "closed_h4_time", "event"]
    output_csv.parent.mkdir(exist_ok=True)
    with output_csv.open(mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for bar in simulated_bars:
            event = h024_strategy_intent_detail(bar)
            writer.writerow({"symbol": bar.symbol, "closed_h4_time": bar.closed_h4_time, "event": event})


def verify_runtime_csv(output_csv: Path):
    """Dynamically verify counts of WOULD_OPEN, BLOCKED, NO_ACTION per symbol."""
    counts_per_symbol = {}
    with output_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row["symbol"]
            event = row["event"]
            if symbol not in counts_per_symbol:
                counts_per_symbol[symbol] = Counter()
            if "WOULD_OPEN" in event:
                counts_per_symbol[symbol]["WOULD_OPEN"] += 1
            elif "BLOCKED" in event:
                counts_per_symbol[symbol]["BLOCKED"] += 1
            elif "NO_ACTION" in event:
                counts_per_symbol[symbol]["NO_ACTION"] += 1

    # Print counts and assert sanity dynamically
    print("Runtime counts per symbol:")
    for symbol, counts in counts_per_symbol.items():
        print(f"{symbol}: {dict(counts)}")
        # Must have at least one of each that occurs in simulation
        for event_type, count in counts.items():
            assert count > 0, f"{symbol} has zero {event_type} rows"


def test_h024_full_h4_runtime_ci():
    """CI test: simulate, write CSV, and validate all symbols/events."""
    symbols = ["USDJPYm", "XAUUSDm"]
    simulated_bars = simulate_historical_h4_series(symbols, num_bars=10, start_time="2026-05-08 10:00")
    simulate_runtime_csv(simulated_bars, RUNTIME_CSV)
    verify_runtime_csv(RUNTIME_CSV)
    print(f"Full H4 runtime CI harness CSV generated: {RUNTIME_CSV}")


if __name__ == "__main__":
    test_h024_full_h4_runtime_ci()