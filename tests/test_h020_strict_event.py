from unittest.mock import MagicMock, patch
import pandas as pd
from quantcore.backtest.h020_strict_event import backtest_h020_strict_event

@patch("quantcore.backtest.h020_strict_event.backtest_h017_strict_event_from_result")
@patch("quantcore.backtest.h020_strict_event.run_h020_bridge_shim")
def test_backtest_h020_strict_event(mock_run_shim, mock_backtest):
    mock_run_shim.return_value = MagicMock()
    mock_backtest.return_value = MagicMock()
    
    df = pd.DataFrame()
    result = backtest_h020_strict_event(
        usdjpy_h4=df,
        xauusd_h4=df,
        usdjpy_m1=df,
        xauusd_m1=df,
        accepted_entry_times=[]
    )
    
    mock_run_shim.assert_called_once()
    mock_backtest.assert_called_once()
    assert result is not None
