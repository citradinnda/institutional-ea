"""H024 broker symbol/spec audit.

Research diagnostic only.

This is not:
- a deployable strategy,
- demo approval,
- live approval,
- Phase 4 approval.

Purpose:
- compare MT5-exported symbol facts against current backtest assumptions,
- fail loudly on contract-size, quote-currency, lot-step, min-lot, spread, or
  commission mismatches,
- keep broker/execution realism separate from alpha logic.

Expected input CSV:

reports/h024_mt5_symbol_specs.csv

Required columns:
- symbol
- contract_size
- quote_currency
- lot_step
- min_lot
- spread_price
- commission_usd_per_lot_per_fill

Optional columns:
- stop_slippage_atr_fraction
- max_lot
- stops_level_points
- freeze_level_points
- point
- digits
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from quantcore.backtest.cost_model import get_default_cost_spec
from quantcore.backtest.portfolio import get_default_instrument_spec

DEFAULT_MT5_SPEC_PATH = (
    Path(__file__).resolve().parents[1]
    / "reports"
    / "h024_mt5_symbol_specs.csv"
)

REQUIRED_COLUMNS: tuple[str, ...] = (
    "symbol",
    "contract_size",
    "quote_currency",
    "lot_step",
    "min_lot",
    "spread_price",
    "commission_usd_per_lot_per_fill",
)

OPTIONAL_COLUMNS: tuple[str, ...] = (
    "stop_slippage_atr_fraction",
    "max_lot",
    "stops_level_points",
    "freeze_level_points",
    "point",
    "digits",
)

_SUPPORTED_SYMBOLS: tuple[str, ...] = ("USDJPY", "XAUUSD")


@dataclass(frozen=True)
class SymbolSpecAuditRow:
    symbol: str
    field: str
    expected: str
    observed: str
    status: str


def load_mt5_symbol_specs(path: Path = DEFAULT_MT5_SPEC_PATH) -> pd.DataFrame:
    """Load MT5 symbol specs from the required audit CSV."""

    if not path.exists():
        raise FileNotFoundError(
            f"MT5 symbol spec CSV not found: {path}. "
            "Create reports\\h024_mt5_symbol_specs.csv with the required columns."
        )

    frame = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"MT5 symbol spec CSV missing required columns: {missing}")

    frame = frame.copy()
    frame["symbol"] = frame["symbol"].astype(str).str.upper()

    duplicates = frame.loc[frame["symbol"].duplicated(), "symbol"].tolist()
    if duplicates:
        raise ValueError(f"duplicate symbol rows in MT5 symbol spec CSV: {duplicates}")

    missing_symbols = [symbol for symbol in _SUPPORTED_SYMBOLS if symbol not in set(frame["symbol"])]
    if missing_symbols:
        raise ValueError(f"MT5 symbol spec CSV missing supported symbols: {missing_symbols}")

    return frame


def audit_mt5_symbol_specs(frame: pd.DataFrame) -> tuple[SymbolSpecAuditRow, ...]:
    """Compare observed MT5 symbol facts with current backtest assumptions."""

    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"spec frame missing required columns: {missing}")

    specs = frame.copy()
    specs["symbol"] = specs["symbol"].astype(str).str.upper()
    rows: list[SymbolSpecAuditRow] = []

    for symbol in _SUPPORTED_SYMBOLS:
        observed_rows = specs.loc[specs["symbol"] == symbol]
        if len(observed_rows) != 1:
            raise ValueError(f"expected exactly one row for {symbol}, got {len(observed_rows)}")

        observed = observed_rows.iloc[0]
        instrument = get_default_instrument_spec(symbol)
        cost = get_default_cost_spec(symbol)

        rows.extend(
            [
                _compare_float(
                    symbol=symbol,
                    field="contract_size",
                    expected=instrument.contract_size,
                    observed=observed["contract_size"],
                ),
                _compare_text(
                    symbol=symbol,
                    field="quote_currency",
                    expected=instrument.quote_currency,
                    observed=observed["quote_currency"],
                ),
                _compare_float(
                    symbol=symbol,
                    field="lot_step",
                    expected=instrument.lot_step,
                    observed=observed["lot_step"],
                ),
                _compare_float(
                    symbol=symbol,
                    field="min_lot",
                    expected=instrument.min_lot,
                    observed=observed["min_lot"],
                ),
                _compare_float(
                    symbol=symbol,
                    field="spread_price",
                    expected=cost.spread_price,
                    observed=observed["spread_price"],
                ),
                _compare_float(
                    symbol=symbol,
                    field="commission_usd_per_lot_per_fill",
                    expected=cost.commission_usd_per_lot_per_fill,
                    observed=observed["commission_usd_per_lot_per_fill"],
                ),
            ]
        )

        if "stop_slippage_atr_fraction" in specs.columns:
            rows.append(
                _compare_float(
                    symbol=symbol,
                    field="stop_slippage_atr_fraction",
                    expected=cost.stop_slippage_atr_fraction,
                    observed=observed["stop_slippage_atr_fraction"],
                )
            )

    return tuple(rows)


def format_symbol_spec_audit_report(rows: tuple[SymbolSpecAuditRow, ...]) -> str:
    mismatches = [row for row in rows if row.status != "ok"]

    table = pd.DataFrame([row.__dict__ for row in rows])
    sections = [
        "H024 broker symbol/spec audit",
        "=" * 72,
        "Research only. No demo/live/Phase 4 approval.",
        "",
        table.to_string(index=False) if not table.empty else "(no rows)",
        "",
        f"Mismatch count: {len(mismatches)}",
    ]

    if mismatches:
        sections.extend(
            [
                "",
                "Verdict: FAIL",
                "Backtest broker assumptions do not match the supplied MT5 symbol facts.",
            ]
        )
    else:
        sections.extend(
            [
                "",
                "Verdict: PASS",
                "Supplied MT5 symbol facts match the current backtest assumptions.",
            ]
        )

    sections.extend(
        [
            "",
            "This audit only checks static symbol/cost assumptions.",
            "It does not approve demo/live/Phase 4.",
        ]
    )
    return "\n".join(sections)


def main() -> None:
    print("H024 broker symbol/spec audit")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print()

    specs = load_mt5_symbol_specs(DEFAULT_MT5_SPEC_PATH)
    rows = audit_mt5_symbol_specs(specs)
    print(format_symbol_spec_audit_report(rows))

    if any(row.status != "ok" for row in rows):
        raise SystemExit(1)


def _compare_float(
    *,
    symbol: str,
    field: str,
    expected: float,
    observed: object,
    tolerance: float = 1e-9,
) -> SymbolSpecAuditRow:
    observed_float = float(observed)
    expected_float = float(expected)
    status = "ok" if abs(observed_float - expected_float) <= tolerance else "mismatch"
    return SymbolSpecAuditRow(
        symbol=symbol,
        field=field,
        expected=f"{expected_float:.12g}",
        observed=f"{observed_float:.12g}",
        status=status,
    )


def _compare_text(
    *,
    symbol: str,
    field: str,
    expected: str,
    observed: object,
) -> SymbolSpecAuditRow:
    expected_text = str(expected).upper()
    observed_text = str(observed).upper()
    status = "ok" if expected_text == observed_text else "mismatch"
    return SymbolSpecAuditRow(
        symbol=symbol,
        field=field,
        expected=expected_text,
        observed=observed_text,
        status=status,
    )


if __name__ == "__main__":
    main()
