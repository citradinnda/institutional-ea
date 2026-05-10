from types import SimpleNamespace

import pandas as pd

from quantcore.strategy.h020 import H020SizingConfig
from scripts.scan_h024_executable_candidate_shifts import (
    H024ExecutableCandidateScanInputs,
    scan_bridge_result_for_executable_shifts,
    scan_h024_candidate_inputs_for_executable_shifts,
)


def _h4_frame(index: pd.DatetimeIndex, opens: list[float]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": opens,
            "high": [value + 1.0 for value in opens],
            "low": [value - 1.0 for value in opens],
            "close": [value + 0.5 for value in opens],
        },
        index=index,
    )


def test_scan_returns_only_nonzero_sized_positions():
    index = pd.date_range("2026-01-01", periods=4, freq="4h")
    positions = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    signals = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_long = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_short = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])

    positions.at[index[1], "USDJPY"] = 0.009
    signals.at[index[1], "USDJPY"] = 0.01
    stops_long.at[index[1], "USDJPY"] = 154.0

    result = SimpleNamespace(
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    candidates = scan_bridge_result_for_executable_shifts(
        bridge_result=result,
        usdjpy_h4=_h4_frame(index, [150.0, 151.0, 156.0, 157.0]),
        xauusd_h4=_h4_frame(index, [2000.0, 2001.0, 2002.0, 2003.0]),
    )

    assert len(candidates) == 1
    assert candidates[0].symbol == "USDJPY"
    assert candidates[0].side == "buy"
    assert candidates[0].decision_time == index[1]
    assert candidates[0].entry_time == index[2]
    assert candidates[0].ea_closed_shift_from_latest_common_h4 == 3
    assert candidates[0].entry_price == 156.0
    assert candidates[0].stop_price == 154.0
    assert candidates[0].stop_distance == 2.0


def test_scan_ignores_signal_rows_that_sizing_suppressed_to_zero():
    index = pd.date_range("2026-01-01", periods=3, freq="4h")
    positions = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    signals = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_long = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_short = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])

    signals.at[index[1], "USDJPY"] = 0.01
    stops_long.at[index[1], "USDJPY"] = 154.0

    result = SimpleNamespace(
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    candidates = scan_bridge_result_for_executable_shifts(
        bridge_result=result,
        usdjpy_h4=_h4_frame(index, [150.0, 151.0, 156.0]),
        xauusd_h4=_h4_frame(index, [2000.0, 2001.0, 2002.0]),
    )

    assert candidates == []


def test_scan_handles_short_candidates_with_short_stop():
    index = pd.date_range("2026-01-01", periods=4, freq="4h")
    positions = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    signals = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_long = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_short = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])

    positions.at[index[2], "XAUUSD"] = -0.008
    signals.at[index[2], "XAUUSD"] = -0.01
    stops_short.at[index[2], "XAUUSD"] = 2050.0

    result = SimpleNamespace(
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
    )

    candidates = scan_bridge_result_for_executable_shifts(
        bridge_result=result,
        usdjpy_h4=_h4_frame(index, [150.0, 151.0, 152.0, 153.0]),
        xauusd_h4=_h4_frame(index, [2000.0, 2001.0, 2002.0, 2010.0]),
    )

    assert len(candidates) == 1
    assert candidates[0].symbol == "XAUUSD"
    assert candidates[0].side == "sell"
    assert candidates[0].decision_time == index[2]
    assert candidates[0].entry_time == index[3]
    assert candidates[0].ea_closed_shift_from_latest_common_h4 == 2
    assert candidates[0].entry_price == 2010.0
    assert candidates[0].stop_price == 2050.0
    assert candidates[0].stop_distance == 40.0

def test_precomputed_scan_inputs_reuse_h024_geometry_but_keep_h020_sizing() -> None:
    index = pd.date_range("2026-01-01", periods=4, freq="4h")
    positions = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    signals = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_long = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_short = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])

    positions.at[index[1], "USDJPY"] = 0.01
    signals.at[index[1], "USDJPY"] = 0.01
    stops_long.at[index[1], "USDJPY"] = 154.0

    scan_inputs = H024ExecutableCandidateScanInputs(
        index=index,
        h4_by_symbol={
            "USDJPY": _h4_frame(index, [150.0, 151.0, 156.0, 157.0]),
            "XAUUSD": _h4_frame(index, [2000.0, 2001.0, 2002.0, 2003.0]),
        },
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
        sizing_config=H020SizingConfig(),
    )

    executable = scan_h024_candidate_inputs_for_executable_shifts(
        scan_inputs=scan_inputs,
        balance=10_000.0,
    )
    below_minimum = scan_h024_candidate_inputs_for_executable_shifts(
        scan_inputs=scan_inputs,
        balance=100.0,
    )

    assert len(executable) == 1
    assert executable[0].symbol == "USDJPY"
    assert executable[0].side == "buy"
    assert executable[0].decision_time == index[1]
    assert executable[0].entry_time == index[2]
    assert executable[0].ea_closed_shift_from_latest_common_h4 == 3
    assert executable[0].signal_signed_risk_fraction == 0.01
    assert executable[0].final_signed_risk_fraction > 0.0
    assert executable[0].entry_price == 156.0
    assert executable[0].stop_price == 154.0
    assert executable[0].stop_distance == 2.0
    assert below_minimum == []
