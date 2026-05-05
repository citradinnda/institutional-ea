import pandas as pd
from quantcore.backtest.h017_strict_event import backtest_h017_strict_event_from_result
from quantcore.strategy.h020 import H020SizingConfig
from quantcore.strategy.h020_runner import run_h020_bridge_shim

def backtest_h020_strict_event(
    *,
    usdjpy_h4: pd.DataFrame,
    xauusd_h4: pd.DataFrame,
    usdjpy_m1: pd.DataFrame,
    xauusd_m1: pd.DataFrame,
    accepted_entry_times: list[pd.Timestamp],
    starting_equity_usd: float = 10000.0,
    config: H020SizingConfig | None = None,
):
    """Run strict event validation for H020."""
    shim_result = run_h020_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4,
        xauusd_ohlcv=xauusd_h4,
        config=config,
    )
    
    return backtest_h017_strict_event_from_result(
        h017_result=shim_result,
        usdjpy_h4=usdjpy_h4,
        xauusd_h4=xauusd_h4,
        usdjpy_m1=usdjpy_m1,
        xauusd_m1=xauusd_m1,
        accepted_entry_times=accepted_entry_times,
        starting_equity_usd=starting_equity_usd,
    )
