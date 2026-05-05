from unittest.mock import MagicMock, patch
import pandas as pd
from quantcore.strategy.h020_runner import run_h020_bridge_shim

@patch("quantcore.strategy.h020_runner.generate_h020_intent_panel")
@patch("quantcore.strategy.h020_runner.run_h019")
def test_run_h020_bridge_shim(mock_run_h019, mock_generate):
    mock_result = MagicMock()
    mock_result.positions = pd.DataFrame()
    mock_run_h019.return_value = mock_result
    mock_generate.return_value = []
    
    df = pd.DataFrame()
    result = run_h020_bridge_shim(usdjpy_ohlcv=df, xauusd_ohlcv=df)
    
    mock_run_h019.assert_called_once()
    mock_generate.assert_called_once()
    assert result.positions is not None
