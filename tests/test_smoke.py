"""Smoke test: proves the test runner and imports work."""


def test_python_works():
    assert 1 + 1 == 2


def test_numpy_imports():
    import numpy as np
    arr = np.array([1, 2, 3])
    assert arr.sum() == 6


def test_pandas_imports():
    import pandas as pd
    s = pd.Series([1, 2, 3])
    assert s.mean() == 2