from unittest.mock import MagicMock, patch
from scripts.run_h020_strict_event_real import main

@patch("scripts.run_h020_strict_event_real.backtest_h020_strict_event")
@patch("scripts.run_h020_strict_event_real.assess_common_complete_h4_m1_windows")
@patch("scripts.run_h020_strict_event_real.load_mt5_csv")
@patch("scripts.run_h020_strict_event_real.require_existing_files")
def test_run_h020_strict_event_real_routes(mock_req, mock_load, mock_assess, mock_backtest):
    mock_assess.return_value = MagicMock(accepted_count=5476)
    
    main()
    
    mock_req.assert_called_once()
    mock_backtest.assert_called_once()
