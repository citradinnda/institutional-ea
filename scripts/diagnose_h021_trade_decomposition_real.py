"""H021 trade decomposition diagnostic.

This script is diagnostic-only. It decomposes the already guard-safe H020 strict
event fills to identify where the realized losses came from.

It is not:
- a new strategy,
- a validation pass,
- live-trading approval,
- Phase 4 approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, Sequence

import pandas as pd

from quantcore.backtest.fill_engine import Fill
from quantcore.backtest.portfolio import fill_pnl_usd
from quantcore.backtest.h020_strict_event import backtest_h020_strict_event
from quantcore.data.bridge_windows import assess_common_complete_h4_m1_windows
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)

_ALLOWED_GROUP_FIELDS = frozenset({"symbol", "side", "exit_reason"})


@dataclass(frozen=True)
class H021TradeDecompositionRow:
    group: tuple[tuple[str, str], ...]
    fill_count: int
    winning_fill_count: int
    losing_fill_count: int
    flat_fill_count: int
    win_rate: float
    total_pnl_usd: float
    mean_pnl_usd: float
    median_pnl_usd: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float


def summarize_fills_by_fields(
    fills: Iterable[Fill],
    *,
    group_fields: Sequence[str],
) -> tuple[H021TradeDecompositionRow, ...]:
    """Summarize fill P&L after costs by explicit fill fields."""
    _validate_group_fields(group_fields)

    records: list[dict[str, object]] = []
    for fill in fills:
        record = {
            "symbol": fill.symbol,
            "side": fill.side,
            "exit_reason": fill.exit_reason,
            "pnl_usd": fill_pnl_usd(fill=fill),
        }
        records.append(record)

    if not records:
        return ()

    frame = pd.DataFrame.from_records(records)
    rows: list[H021TradeDecompositionRow] = []

    groupby_key: str | list[str]
    if len(group_fields) == 1:
        groupby_key = group_fields[0]
    else:
        groupby_key = list(group_fields)

    grouped = frame.groupby(groupby_key, dropna=False, sort=True)

    for key, group in grouped:
        key_tuple = _normalize_group_key(key=key, group_fields=group_fields)
        pnl = group["pnl_usd"].astype(float)
        winning = pnl[pnl > 0.0]
        losing = pnl[pnl < 0.0]
        flat = pnl[pnl == 0.0]

        gross_profit = float(winning.sum())
        gross_loss = float(losing.sum())
        profit_factor = gross_profit / abs(gross_loss) if gross_loss < 0.0 else float("nan")

        rows.append(
            H021TradeDecompositionRow(
                group=key_tuple,
                fill_count=int(len(pnl)),
                winning_fill_count=int(len(winning)),
                losing_fill_count=int(len(losing)),
                flat_fill_count=int(len(flat)),
                win_rate=float(len(winning) / len(pnl)),
                total_pnl_usd=float(pnl.sum()),
                mean_pnl_usd=float(pnl.mean()),
                median_pnl_usd=float(pnl.median()),
                gross_profit_usd=gross_profit,
                gross_loss_usd=gross_loss,
                profit_factor=profit_factor,
            )
        )

    return tuple(rows)


def format_decomposition_table(
    rows: Sequence[H021TradeDecompositionRow],
    *,
    title: str,
) -> str:
    """Format decomposition rows as a compact console table."""
    lines = [
        title,
        "-" * len(title),
    ]

    if not rows:
        lines.append("(no fills)")
        return "\n".join(lines)

    header = (
        "group | fills | win_rate | total_pnl_usd | mean_pnl_usd | "
        "median_pnl_usd | profit_factor"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for row in rows:
        group_label = ", ".join(f"{name}={value}" for name, value in row.group)
        lines.append(
            " | ".join(
                [
                    group_label,
                    str(row.fill_count),
                    _format_percent(row.win_rate),
                    f"{row.total_pnl_usd:.2f}",
                    f"{row.mean_pnl_usd:.2f}",
                    f"{row.median_pnl_usd:.2f}",
                    _format_float(row.profit_factor),
                ]
            )
        )

    return "\n".join(lines)


def main() -> None:
    print("H021 trade decomposition diagnostic from H020 strict event fills")
    print("=" * 70)
    print("Diagnostic only. No live trading. No Phase 4.")
    print()

    require_existing_files(
        [USDJPY_H4_PATH, XAUUSD_H4_PATH, USDJPY_M1_PATH, XAUUSD_M1_PATH],
        label="broker-native MT5 exports",
    )

    print("Loading exports...")
    usdjpy_h4 = load_mt5_csv(USDJPY_H4_PATH)
    xauusd_h4 = load_mt5_csv(XAUUSD_H4_PATH)
    usdjpy_m1 = load_mt5_csv(USDJPY_M1_PATH)
    xauusd_m1 = load_mt5_csv(XAUUSD_M1_PATH)

    assessment = assess_common_complete_h4_m1_windows(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        expected_m1_bars_per_h4=EXPECTED_M1_BARS_PER_H4,
        expected_h4_delta=EXPECTED_H4_DELTA,
    )

    if assessment.accepted_count != EXPECTED_ACCEPTED_COUNT:
        raise RuntimeError(f"accepted_count mismatch: {assessment.accepted_count}")

    print(f"Strict accepted bridge-windows: {assessment.accepted_count}")
    print("Running strict H020 event backtest...")
    print()

    result = backtest_h020_strict_event(
        usdjpy_h4=usdjpy_h4.bars,
        xauusd_h4=xauusd_h4.bars,
        usdjpy_m1=usdjpy_m1.bars,
        xauusd_m1=xauusd_m1.bars,
        accepted_entry_times=assessment.accepted_timestamps,
        starting_equity_usd=10000.0,
    )

    fills = result.backtest.fills

    print(format_decomposition_table(
        summarize_fills_by_fields(fills, group_fields=("symbol",)),
        title="By symbol",
    ))
    print()
    print(format_decomposition_table(
        summarize_fills_by_fields(fills, group_fields=("side",)),
        title="By side",
    ))
    print()
    print(format_decomposition_table(
        summarize_fills_by_fields(fills, group_fields=("exit_reason",)),
        title="By exit reason",
    ))
    print()
    print(format_decomposition_table(
        summarize_fills_by_fields(fills, group_fields=("symbol", "side", "exit_reason")),
        title="By symbol / side / exit reason",
    ))
    print()
    print("Verdict reminder: decomposition is evidence gathering only.")
    print("No live trading is approved. Phase 4 is not approved.")


def _validate_group_fields(group_fields: Sequence[str]) -> None:
    if not group_fields:
        raise ValueError("group_fields must not be empty")

    unknown = [field for field in group_fields if field not in _ALLOWED_GROUP_FIELDS]
    if unknown:
        supported = ", ".join(sorted(_ALLOWED_GROUP_FIELDS))
        raise ValueError(f"unsupported group field(s): {unknown}; supported: {supported}")


def _normalize_group_key(
    *,
    key: object,
    group_fields: Sequence[str],
) -> tuple[tuple[str, str], ...]:
    if len(group_fields) == 1:
        values = (key,)
    else:
        values = tuple(key) if isinstance(key, tuple) else (key,)

    return tuple(
        (field, str(value))
        for field, value in zip(group_fields, values, strict=True)
    )


def _format_float(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.6f}"


def _format_percent(value: float) -> str:
    if isnan(value):
        return "nan"
    return f"{value:.4%}"


if __name__ == "__main__":
    main()
