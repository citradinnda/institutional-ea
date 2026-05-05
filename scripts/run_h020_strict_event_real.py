"""Run strict expanded broker-native H020 validation manually."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd

from quantcore.data.bridge_windows import assess_common_complete_h4_m1_windows
from quantcore.data.mt5_loader import DEFAULT_BROKER_TZ, MT5LoadResult, load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.backtest.h020_strict_event import backtest_h020_strict_event

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data" / "raw"

USDJPY_H4_PATH = DATA_ROOT / "USDJPY" / "H4.csv"
XAUUSD_H4_PATH = DATA_ROOT / "XAUUSD" / "H4.csv"
USDJPY_M1_PATH = DATA_ROOT / "USDJPY" / "M1.csv"
XAUUSD_M1_PATH = DATA_ROOT / "XAUUSD" / "M1.csv"

EXPECTED_ACCEPTED_COUNT = 5476
EXPECTED_M1_BARS_PER_H4 = 240
EXPECTED_H4_DELTA = pd.Timedelta(hours=4)

def main() -> None:
    print("H020 strict expanded broker-native event-driven validation")
    print("=" * 60)
    
    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="broker-native MT5 exports",
    )
    
    print("Loading exports...")
    usdjpy_h4 = load_mt5_csv(USDJPY_H4_PATH)
    xauusd_h4 = load_mt5_csv(XAUUSD_H4_PATH)
    usdjpy_m1 = load_mt5_csv(USDJPY_M1_PATH)
    xauusd_m1 = load_mt5_csv(XAUUSD_M1_PATH)
    
    assessment = assess_common_complete_h4_m1_windows(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )
    
    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(f"accepted_count mismatch: {assessment.accepted_count}")
        
    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print("Running strict event backtest (this may take a minute)...")
    
    result = backtest_h020_strict_event(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
        starting_equity_usd=10000.0,
    )
    
    print("\nValidation completed successfully WITHOUT guard violations!")

if __name__ == "__main__":
    main()
