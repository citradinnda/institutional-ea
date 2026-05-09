import pandas as pd
import pytest

from scripts.audit_h024_broker_symbol_specs import (
    REQUIRED_COLUMNS,
    audit_mt5_symbol_specs,
    format_symbol_spec_audit_report,
    load_mt5_symbol_specs,
)


def _matching_specs() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "symbol": "USDJPY",
                "contract_size": 100_000.0,
                "quote_currency": "JPY",
                "lot_step": 0.01,
                "min_lot": 0.01,
                "spread_price": 0.01,
                "commission_usd_per_lot_per_fill": 7.0,
                "stop_slippage_atr_fraction": 0.05,
            },
            {
                "symbol": "XAUUSD",
                "contract_size": 100.0,
                "quote_currency": "USD",
                "lot_step": 0.01,
                "min_lot": 0.01,
                "spread_price": 0.30,
                "commission_usd_per_lot_per_fill": 10.0,
                "stop_slippage_atr_fraction": 0.05,
            },
        ]
    )


def test_required_columns_are_stable():
    assert REQUIRED_COLUMNS == (
        "symbol",
        "contract_size",
        "quote_currency",
        "lot_step",
        "min_lot",
        "spread_price",
        "commission_usd_per_lot_per_fill",
    )


def test_audit_mt5_symbol_specs_passes_matching_specs():
    rows = audit_mt5_symbol_specs(_matching_specs())

    assert rows
    assert all(row.status == "ok" for row in rows)

    report = format_symbol_spec_audit_report(rows)
    assert "Verdict: PASS" in report
    assert "No demo/live/Phase 4 approval." in report


def test_audit_mt5_symbol_specs_flags_mismatch():
    specs = _matching_specs()
    specs.loc[specs["symbol"] == "XAUUSD", "contract_size"] = 1.0

    rows = audit_mt5_symbol_specs(specs)

    mismatches = [row for row in rows if row.status == "mismatch"]
    assert len(mismatches) == 1
    assert mismatches[0].symbol == "XAUUSD"
    assert mismatches[0].field == "contract_size"

    report = format_symbol_spec_audit_report(rows)
    assert "Verdict: FAIL" in report


def test_audit_rejects_missing_required_column():
    specs = _matching_specs().drop(columns=["spread_price"])

    with pytest.raises(ValueError, match="missing required columns"):
        audit_mt5_symbol_specs(specs)


def test_load_mt5_symbol_specs_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match="MT5 symbol spec CSV not found"):
        load_mt5_symbol_specs(tmp_path / "missing.csv")


def test_load_mt5_symbol_specs_validates_symbols_and_duplicates(tmp_path):
    path = tmp_path / "specs.csv"
    _matching_specs().to_csv(path, index=False)

    loaded = load_mt5_symbol_specs(path)
    assert set(loaded["symbol"]) == {"USDJPY", "XAUUSD"}

    duplicate = pd.concat([_matching_specs(), _matching_specs().iloc[[0]]], ignore_index=True)
    duplicate_path = tmp_path / "duplicate.csv"
    duplicate.to_csv(duplicate_path, index=False)

    with pytest.raises(ValueError, match="duplicate symbol rows"):
        load_mt5_symbol_specs(duplicate_path)

    missing = _matching_specs().loc[lambda frame: frame["symbol"] == "USDJPY"]
    missing_path = tmp_path / "missing_symbol.csv"
    missing.to_csv(missing_path, index=False)

    with pytest.raises(ValueError, match="missing supported symbols"):
        load_mt5_symbol_specs(missing_path)
