from unittest.mock import MagicMock, patch

from scripts.scan_h020_sizing_diagnostics_real import main


@patch("scripts.scan_h020_sizing_diagnostics_real.build_h020_sizing_diagnostic")
@patch("scripts.scan_h020_sizing_diagnostics_real._load_broker_native_exports")
@patch("builtins.print")
def test_h020_sizing_diagnostic_real_script_routes(mock_print, mock_load, mock_build) -> None:
    # Setup mocks to bypass real data loading
    mock_load.return_value = MagicMock()
    
    mock_diagnostic = MagicMock()
    mock_diagnostic.bridge_window_assessment.accepted_count = 5476
    mock_diagnostic.bridge_window_assessment.accepted_timestamps = []
    mock_diagnostic.panels = []
    mock_build.return_value = mock_diagnostic

    main()

    mock_load.assert_called_once()
    mock_build.assert_called_once()
    
    # Verify interpretation guardrails were printed
    assert any("H020 VALIDATED: False" in str(call) for call in mock_print.mock_calls)
