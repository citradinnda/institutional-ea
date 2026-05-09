import pandas as pd
import pytest

from scripts.diagnose_h024_walk_forward_real import (
    DEFAULT_H024_WALK_FORWARD_HOLD_H4_BARS,
    DEFAULT_H024_WALK_FORWARD_TEST_FRACTIONS,
    build_h024_walk_forward_folds,
    format_h024_walk_forward_summary,
    run_h024_walk_forward_validation,
)


def _index() -> pd.DatetimeIndex:
    return pd.date_range("2024-01-01 00:00", periods=12, freq="4h", tz="UTC")


def _usdjpy_h4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104, 105, 106, 105, 107, 108, 109, 110],
            "high": [101, 102, 103, 104, 105, 106, 107, 106, 109, 110, 111, 112],
            "low": [99, 100, 101, 102, 103, 104, 105, 104, 106, 107, 108, 109],
            "close": [101, 102, 103, 104, 105, 106, 106.5, 104.5, 108, 109, 110, 111],
        },
        index=_index(),
    )


def _xauusd_h4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": [110, 109, 108, 107, 106, 105, 104, 105, 103, 102, 101, 100],
            "high": [111, 110, 109, 108, 107, 106, 105, 106, 104, 103, 102, 101],
            "low": [109, 108, 107, 106, 105, 104, 103, 104, 101, 100, 99, 98],
            "close": [109, 108, 107, 106, 105, 104, 103.5, 105.5, 102, 101, 100, 99],
        },
        index=_index(),
    )


def _m1_from_h4(h4: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
            }
            for _, row in h4.iterrows()
        ],
        index=h4.index,
    )


def test_h024_walk_forward_defaults_are_fixed_candidate():
    assert DEFAULT_H024_WALK_FORWARD_HOLD_H4_BARS == 3
    assert DEFAULT_H024_WALK_FORWARD_TEST_FRACTIONS == (0.25, 0.50, 0.75)


def test_h024_walk_forward_folds_are_anchored_and_chronological():
    folds = build_h024_walk_forward_folds(tuple(_index()))

    assert [fold.label for fold in folds] == [
        "anchored_train_25%_test_rest",
        "anchored_train_50%_test_rest",
        "anchored_train_75%_test_rest",
    ]
    assert [fold.train_count for fold in folds] == [3, 6, 9]
    assert [fold.test_count for fold in folds] == [9, 6, 3]
    assert folds[0].test_start_utc == _index()[3]
    assert folds[-1].test_start_utc == _index()[9]


def test_h024_walk_forward_runs_on_synthetic_data():
    results = run_h024_walk_forward_validation(
        usdjpy_h4=_usdjpy_h4(),
        xauusd_h4=_xauusd_h4(),
        usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
        xauusd_m1=_m1_from_h4(_xauusd_h4()),
        accepted_entry_times=tuple(_index()),
        test_fractions=(0.25,),
    )

    assert len(results) == 1
    assert results[0].fold.label == "anchored_train_25%_test_rest"
    assert results[0].run.hold_h4_bars == 3
    assert results[0].run.summary.accepted_entry_count == 9


def test_h024_walk_forward_summary_is_stable():
    results = run_h024_walk_forward_validation(
        usdjpy_h4=_usdjpy_h4(),
        xauusd_h4=_xauusd_h4(),
        usdjpy_m1=_m1_from_h4(_usdjpy_h4()),
        xauusd_m1=_m1_from_h4(_xauusd_h4()),
        accepted_entry_times=tuple(_index()),
        test_fractions=(0.25,),
    )

    report = format_h024_walk_forward_summary(results)

    assert "H024 hold=3 chronological validation summary" in report
    assert "fold | train_count | test_count" in report
    assert "anchored_train_25%_test_rest" in report
    assert "No demo trading is approved. No live trading is approved. Phase 4 is not approved." in report


def test_h024_walk_forward_rejects_bad_folds():
    with pytest.raises(ValueError, match="at least 4 timestamps"):
        build_h024_walk_forward_folds(tuple(_index()[:3]))

    with pytest.raises(ValueError, match="test_fractions must be non-empty"):
        build_h024_walk_forward_folds(tuple(_index()), test_fractions=())

    with pytest.raises(ValueError, match="between 0 and 1"):
        build_h024_walk_forward_folds(tuple(_index()), test_fractions=(1.0,))

    with pytest.raises(ValueError, match="strictly increasing"):
        build_h024_walk_forward_folds(tuple(_index()), test_fractions=(0.5, 0.25))


def test_h024_walk_forward_script_has_main_entrypoint():
    import scripts.diagnose_h024_walk_forward_real as module

    assert callable(module.main)
