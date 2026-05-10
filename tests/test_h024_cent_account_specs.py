import pandas as pd
import pytest

from scripts.scan_h024_executable_candidate_shifts import (
    CENT_ACCOUNT_USC_INSTRUMENT_SPECS,
    H024ExecutableCandidateScanInputs,
    scan_h024_candidate_inputs_for_executable_shifts,
)
from quantcore.strategy.h020 import H020SizingConfig


def _canonical_candidate_inputs() -> H024ExecutableCandidateScanInputs:
    decision_time = pd.Timestamp("2021-07-17T21:00:00+00:00")
    entry_time = pd.Timestamp("2021-07-18T17:00:00+00:00")
    index = pd.DatetimeIndex([decision_time, entry_time])

    usdjpy = pd.DataFrame(
        {
            "open": [110.000, 110.015],
            "high": [110.100, 110.100],
            "low": [109.900, 109.900],
            "close": [110.000, 110.015],
        },
        index=index,
    )
    xauusd = pd.DataFrame(
        {
            "open": [1913.000, 1913.590],
            "high": [1914.000, 1914.000],
            "low": [1912.000, 1912.000],
            "close": [1913.000, 1913.590],
        },
        index=index,
    )

    positions = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    signals = pd.DataFrame(0.0, index=index, columns=["USDJPY", "XAUUSD"])
    stops_long = pd.DataFrame(float("nan"), index=index, columns=["USDJPY", "XAUUSD"])
    stops_short = pd.DataFrame(float("nan"), index=index, columns=["USDJPY", "XAUUSD"])

    positions.at[decision_time, "USDJPY"] = -0.01
    signals.at[decision_time, "USDJPY"] = -0.01
    stops_short.at[decision_time, "USDJPY"] = 110.2840593855

    positions.at[decision_time, "XAUUSD"] = -0.01
    signals.at[decision_time, "XAUUSD"] = -0.01
    stops_short.at[decision_time, "XAUUSD"] = 1922.9379866787

    return H024ExecutableCandidateScanInputs(
        index=index,
        h4_by_symbol={"USDJPY": usdjpy, "XAUUSD": xauusd},
        positions=positions,
        signals=signals,
        stops_long=stops_long,
        stops_short=stops_short,
        sizing_config=H020SizingConfig(),
    )


def test_canonical_rows_remain_blocked_with_default_specs_at_100_usd() -> None:
    candidates = scan_h024_candidate_inputs_for_executable_shifts(
        scan_inputs=_canonical_candidate_inputs(),
        balance=100.0,
    )

    assert candidates == []


def test_cent_usc_specs_make_canonical_rows_executable_at_10000_usc() -> None:
    candidates = scan_h024_candidate_inputs_for_executable_shifts(
        scan_inputs=_canonical_candidate_inputs(),
        balance=10_000.0,
        instrument_specs=CENT_ACCOUNT_USC_INSTRUMENT_SPECS,
    )

    by_symbol = {candidate.symbol: candidate for candidate in candidates}

    assert set(by_symbol) == {"USDJPY", "XAUUSD"}

    assert by_symbol["USDJPY"].side == "sell"
    assert by_symbol["USDJPY"].entry_price == pytest.approx(110.015)
    assert by_symbol["USDJPY"].stop_price == pytest.approx(110.2840593855)
    assert abs(by_symbol["USDJPY"].final_signed_risk_fraction) <= 0.01
    assert abs(by_symbol["USDJPY"].final_signed_risk_fraction) > 0.009

    assert by_symbol["XAUUSD"].side == "sell"
    assert by_symbol["XAUUSD"].entry_price == pytest.approx(1913.590)
    assert by_symbol["XAUUSD"].stop_price == pytest.approx(1922.9379866787)
    assert abs(by_symbol["XAUUSD"].final_signed_risk_fraction) <= 0.01
    assert abs(by_symbol["XAUUSD"].final_signed_risk_fraction) > 0.009


def test_cent_usc_specs_document_observed_cent_contract_accounting() -> None:
    assert CENT_ACCOUNT_USC_INSTRUMENT_SPECS["USDJPY"].contract_size == 100_000.0
    assert CENT_ACCOUNT_USC_INSTRUMENT_SPECS["USDJPY"].quote_currency == "JPY"
    assert CENT_ACCOUNT_USC_INSTRUMENT_SPECS["XAUUSD"].contract_size == 100.0
    assert CENT_ACCOUNT_USC_INSTRUMENT_SPECS["XAUUSD"].quote_currency == "USD"
