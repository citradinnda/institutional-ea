import pandas as pd
import pytest

from quantcore.strategy.h024 import H024SignalConfig, generate_h024_signals


def test_h024_generates_long_pullback_continuation_signal():
    frame = pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104, 105, 106, 105, 107],
            "high": [101, 102, 103, 104, 105, 106, 107, 106, 109],
            "low": [99, 100, 101, 102, 103, 104, 105, 104, 106],
            "close": [101, 102, 103, 104, 105, 106, 106.5, 104.5, 108],
        }
    )

    signals = generate_h024_signals(frame)

    assert signals.iloc[-1] == 1
    assert signals.iloc[:-1].eq(0).all()


def test_h024_generates_short_pullback_continuation_signal():
    frame = pd.DataFrame(
        {
            "open": [110, 109, 108, 107, 106, 105, 104, 105, 103],
            "high": [111, 110, 109, 108, 107, 106, 105, 106, 104],
            "low": [109, 108, 107, 106, 105, 104, 103, 104, 101],
            "close": [109, 108, 107, 106, 105, 104, 103.5, 105.5, 102],
        }
    )

    signals = generate_h024_signals(frame)

    assert signals.iloc[-1] == -1
    assert signals.iloc[:-1].eq(0).all()


def test_h024_requires_pullback_before_resumption():
    frame = pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104, 105, 106, 107, 108],
            "high": [101, 102, 103, 104, 105, 106, 107, 108, 110],
            "low": [99, 100, 101, 102, 103, 104, 105, 106, 107],
            "close": [101, 102, 103, 104, 105, 106, 107, 108, 109],
        }
    )

    signals = generate_h024_signals(frame)

    assert signals.eq(0).all()


def test_h024_returns_flat_until_indicators_are_warmed_up():
    frame = pd.DataFrame(
        {
            "open": [100, 101, 102],
            "high": [101, 102, 103],
            "low": [99, 100, 101],
            "close": [101, 102, 103],
        }
    )

    signals = generate_h024_signals(frame)

    assert list(signals) == [0, 0, 0]


def test_h024_rejects_missing_ohlc_columns():
    frame = pd.DataFrame({"close": [1, 2, 3]})

    with pytest.raises(ValueError, match="missing required OHLC columns"):
        generate_h024_signals(frame)


def test_h024_rejects_invalid_config():
    frame = pd.DataFrame(
        {
            "open": [1, 2, 3],
            "high": [2, 3, 4],
            "low": [0, 1, 2],
            "close": [1, 2, 3],
        }
    )

    with pytest.raises(ValueError, match="slow_window must be >= 2"):
        generate_h024_signals(frame, H024SignalConfig(slow_window=1))
