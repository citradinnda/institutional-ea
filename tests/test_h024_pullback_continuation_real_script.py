import pandas as pd
import pytest

from quantcore.strategy.h024 import H024SignalConfig, generate_h024_signals
from scripts.diagnose_h024_pullback_continuation_real import (
    DEFAULT_H024_SYMBOLS,
    build_h024_signal_diagnostic_report,
    format_h024_signal_summary_table,
    format_h024_split_summary_table,
    summarize_h024_chronological_splits,
    summarize_h024_multi_symbol_signals,
    summarize_h024_signal_series,
    summarize_h024_signals,
)


def _utc_range(count: int) -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01 00:00", periods=count, freq="4h", tz="UTC")


def _long_signal_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104, 105, 106, 105, 107],
            "high": [101, 102, 103, 104, 105, 106, 107, 106, 109],
            "low": [99, 100, 101, 102, 103, 104, 105, 104, 106],
            "close": [101, 102, 103, 104, 105, 106, 106.5, 104.5, 108],
        },
        index=_utc_range(9),
    )


def _short_signal_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [110, 109, 108, 107, 106, 105, 104, 105, 103],
            "high": [111, 110, 109, 108, 107, 106, 105, 106, 104],
            "low": [109, 108, 107, 106, 105, 104, 103, 104, 101],
            "close": [109, 108, 107, 106, 105, 104, 103.5, 105.5, 102],
        },
        index=_utc_range(9),
    )


def test_h024_default_symbols_are_usdjpy_xauusd():
    assert DEFAULT_H024_SYMBOLS == ("USDJPY", "XAUUSD")


def test_h024_signal_summary_counts_long_signal():
    summary = summarize_h024_signals(symbol="USDJPY", h4_bars=_long_signal_frame())

    assert summary.symbol == "USDJPY"
    assert summary.bar_count == 9
    assert summary.signal_count == 1
    assert summary.long_signal_count == 1
    assert summary.short_signal_count == 0
    assert summary.flat_count == 8
    assert summary.signal_rate == pytest.approx(1 / 9)
    assert summary.long_share == pytest.approx(1.0)
    assert summary.short_share == pytest.approx(0.0)
    assert summary.first_signal_time_utc == _utc_range(9)[-1]
    assert summary.last_signal_time_utc == _utc_range(9)[-1]


def test_h024_signal_summary_counts_short_signal():
    summary = summarize_h024_signals(symbol="XAUUSD", h4_bars=_short_signal_frame())

    assert summary.symbol == "XAUUSD"
    assert summary.bar_count == 9
    assert summary.signal_count == 1
    assert summary.long_signal_count == 0
    assert summary.short_signal_count == 1
    assert summary.flat_count == 8
    assert summary.signal_rate == pytest.approx(1 / 9)
    assert summary.long_share == pytest.approx(0.0)
    assert summary.short_share == pytest.approx(1.0)


def test_h024_signal_series_summary_handles_empty_series():
    signals = pd.Series([], index=pd.DatetimeIndex([], tz="UTC"), dtype="int64")

    summary = summarize_h024_signal_series(symbol="USDJPY", signals=signals)

    assert summary.bar_count == 0
    assert summary.signal_count == 0
    assert summary.flat_count == 0
    assert str(summary.signal_rate) == "nan"
    assert summary.first_signal_time_utc is None
    assert summary.last_signal_time_utc is None


def test_h024_signal_summary_table_is_stable():
    summaries = [
        summarize_h024_signals(symbol="USDJPY", h4_bars=_long_signal_frame()),
        summarize_h024_signals(symbol="XAUUSD", h4_bars=_short_signal_frame()),
    ]

    table = format_h024_signal_summary_table(summaries)

    assert "symbol | bars | signals | long | short | flat" in table
    assert "USDJPY | 9 | 1 | 1 | 0 | 8" in table
    assert "XAUUSD | 9 | 1 | 0 | 1 | 8" in table
    assert "2024-01-02T08:00:00+00:00" in table


def test_h024_chronological_split_summary_counts_by_slice():
    signals = pd.Series([0, 1, 0, -1, 0], index=_utc_range(5), dtype="int64")

    splits = summarize_h024_chronological_splits(
        symbol="USDJPY",
        signals=signals,
        split_count=2,
    )

    assert [split.label for split in splits] == ["part_1_of_2", "part_2_of_2"]
    assert [split.bar_count for split in splits] == [3, 2]
    assert [split.signal_count for split in splits] == [1, 1]
    assert splits[0].long_signal_count == 1
    assert splits[1].short_signal_count == 1


def test_h024_split_summary_table_is_stable():
    signals = pd.Series([0, 1, 0, -1, 0], index=_utc_range(5), dtype="int64")
    splits = summarize_h024_chronological_splits(
        symbol="USDJPY",
        signals=signals,
        split_count=2,
    )

    table = format_h024_split_summary_table(splits)

    assert "label | symbol | bars | signals | long | short | signal_rate" in table
    assert "part_1_of_2 | USDJPY | 3 | 1 | 1 | 0 | 0.333333" in table
    assert "part_2_of_2 | USDJPY | 2 | 1 | 0 | 1 | 0.500000" in table


def test_h024_multi_symbol_summary_sorts_symbols():
    summaries = summarize_h024_multi_symbol_signals(
        h4_bars_by_symbol={
            "XAUUSD": _short_signal_frame(),
            "USDJPY": _long_signal_frame(),
        }
    )

    assert [summary.symbol for summary in summaries] == ["USDJPY", "XAUUSD"]


def test_h024_signal_diagnostic_report_includes_summary_and_splits():
    report = build_h024_signal_diagnostic_report(
        h4_bars_by_symbol={
            "USDJPY": _long_signal_frame(),
            "XAUUSD": _short_signal_frame(),
        }
    )

    assert "H024 signal diagnostic report" in report
    assert "Signal summary:" in report
    assert "Chronological splits:" in report
    assert "USDJPY | 9 | 1 | 1 | 0 | 8" in report
    assert "XAUUSD | 9 | 1 | 0 | 1 | 8" in report
    assert "part_1_of_2" in report
    assert "part_3_of_3" in report


def test_h024_diagnostic_rejects_bad_inputs():
    with pytest.raises(ValueError, match="symbol must be non-empty"):
        summarize_h024_signals(symbol="", h4_bars=_long_signal_frame())

    with pytest.raises(ValueError, match="h4_bars must use a DatetimeIndex"):
        summarize_h024_signals(
            symbol="USDJPY",
            h4_bars=_long_signal_frame().reset_index(drop=True),
        )

    with pytest.raises(ValueError, match="split_count must be >= 2"):
        summarize_h024_chronological_splits(
            symbol="USDJPY",
            signals=generate_h024_signals(_long_signal_frame()),
            split_count=1,
        )


def test_h024_report_accepts_explicit_signal_config():
    config = H024SignalConfig(
        slow_window=5,
        slope_lag=2,
        atr_window=3,
        pullback_window=3,
        min_pullback_atr=0.25,
        max_pullback_atr=3.0,
        min_slope_atr=0.05,
    )

    report = build_h024_signal_diagnostic_report(
        h4_bars_by_symbol={"USDJPY": _long_signal_frame()},
        config=config,
    )

    assert "USDJPY | 9 | 1 | 1 | 0 | 8" in report
