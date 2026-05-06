"""H021 stop-loss precursor diagnostic.

This script is diagnostic-only. It asks whether realized stop-outs from the
H020 guard-safe strict event backtest concentrate in features known at decision
time.

It is not:
- a new strategy,
- a validation pass,
- live-trading approval,
- Phase 4 approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Iterable, Mapping, Sequence

import pandas as pd

from quantcore.backtest.cost_model import get_default_cost_spec
from quantcore.backtest.fill_engine import Fill
from quantcore.backtest.h020_strict_event import backtest_h020_strict_event
from quantcore.backtest.portfolio import (
    get_default_instrument_spec,
    fill_pnl_usd,
)
from quantcore.data.bridge_windows import assess_common_complete_h4_m1_windows
from quantcore.data.mt5_loader import load_mt5_csv
from quantcore.data.preflight import require_existing_files
from quantcore.strategy.h017 import H017Result
from quantcore.strategy.h020_runner import run_h020_bridge_shim
from scripts.run_h020_strict_event_real import (
    EXPECTED_ACCEPTED_COUNT,
    EXPECTED_H4_DELTA,
    EXPECTED_M1_BARS_PER_H4,
    USDJPY_H4_PATH,
    USDJPY_M1_PATH,
    XAUUSD_H4_PATH,
    XAUUSD_M1_PATH,
)

_ALLOWED_GROUP_FIELDS = frozenset(
    {
        "symbol",
        "side",
        "exit_reason",
        "decision_hour_utc",
        "entry_hour_utc",
        "stop_distance_spread_bucket",
        "estimated_gross_leverage_bucket",
    }
)


@dataclass(frozen=True)
class H021DecisionContext:
    symbol: str
    side: str
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_raw_price: float
    stop_price: float
    raw_stop_distance: float
    stop_distance_spread_multiple: float
    signed_risk_fraction: float


@dataclass(frozen=True)
class H021StopPrecursorRecord:
    symbol: str
    side: str
    exit_reason: str
    decision_time: pd.Timestamp
    entry_time: pd.Timestamp
    decision_hour_utc: str
    entry_hour_utc: str
    entry_raw_price: float
    stop_price: float
    raw_stop_distance: float
    stop_distance_spread_multiple: float
    stop_distance_spread_bucket: str
    signed_risk_fraction: float
    lots: float
    estimated_notional_usd: float
    estimated_gross_leverage: float
    estimated_gross_leverage_bucket: str
    pnl_usd: float


@dataclass(frozen=True)
class H021StopPrecursorSummaryRow:
    group: tuple[tuple[str, str], ...]
    fill_count: int
    stop_count: int
    stop_rate: float
    winning_fill_count: int
    losing_fill_count: int
    total_pnl_usd: float
    mean_pnl_usd: float
    median_pnl_usd: float
    gross_profit_usd: float
    gross_loss_usd: float
    profit_factor: float


def build_decision_contexts(
    *,
    h017_result: H017Result,
    h4_by_symbol: Mapping[str, pd.DataFrame],
    accepted_entry_times: Sequence[pd.Timestamp],
) -> dict[tuple[str, str, pd.Timestamp], H021DecisionContext]:
    """Reconstruct decision-time context for accepted strict entry windows."""
    contexts: dict[tuple[str, str, pd.Timestamp], H021DecisionContext] = {}
    index = pd.DatetimeIndex(h017_result.positions.index).tz_convert("UTC")
    accepted_index = pd.DatetimeIndex(accepted_entry_times).tz_convert("UTC")

    for raw_entry_time in accepted_index:
        entry_time = pd.Timestamp(raw_entry_time).tz_convert("UTC")
        if entry_time not in index:
            continue

        location = index.get_loc(entry_time)
        if not isinstance(location, int):
            raise ValueError(f"non-unique entry_time in positions index: {entry_time}")
        if location <= 0:
            continue

        decision_time = pd.Timestamp(index[location - 1]).tz_convert("UTC")

        for symbol in h017_result.positions.columns:
            signed_risk = float(h017_result.positions.at[decision_time, symbol])
            if pd.isna(signed_risk) or signed_risk == 0.0:
                continue

            side = "buy" if signed_risk > 0.0 else "sell"
            stop_panel = h017_result.stops_long if side == "buy" else h017_result.stops_short
            stop_price = float(stop_panel.at[decision_time, symbol])
            if pd.isna(stop_price):
                continue

            h4 = h4_by_symbol.get(symbol)
            if h4 is None or entry_time not in h4.index:
                continue

            entry_raw_price = float(h4.at[entry_time, "open"])
            raw_stop_distance = abs(entry_raw_price - stop_price)
            if raw_stop_distance <= 0.0:
                continue

            spread = float(get_default_cost_spec(symbol).spread_price)
            spread_multiple = raw_stop_distance / spread

            context = H021DecisionContext(
                symbol=symbol,
                side=side,
                decision_time=decision_time,
                entry_time=entry_time,
                entry_raw_price=entry_raw_price,
                stop_price=stop_price,
                raw_stop_distance=raw_stop_distance,
                stop_distance_spread_multiple=spread_multiple,
                signed_risk_fraction=signed_risk,
            )
            contexts[(symbol, side, entry_time)] = context

    return contexts


def enrich_fills_with_decision_context(
    fills: Iterable[Fill],
    contexts: Mapping[tuple[str, str, pd.Timestamp], H021DecisionContext],
    *,
    starting_equity_usd: float = 10000.0,
) -> tuple[H021StopPrecursorRecord, ...]:
    """Join realized fills to reconstructed decision-time context."""
    if starting_equity_usd <= 0.0:
        raise ValueError("starting_equity_usd must be positive")

    records: list[H021StopPrecursorRecord] = []

    for fill in fills:
        entry_time = pd.Timestamp(fill.entry_time_utc).tz_convert("UTC")
        key = (fill.symbol, fill.side, entry_time)
        if key not in contexts:
            raise ValueError(f"missing decision context for fill key={key}")

        context = contexts[key]
        notional_usd = _estimated_notional_usd(
            symbol=fill.symbol,
            lots=fill.lots,
            entry_raw_price=context.entry_raw_price,
        )
        gross_leverage = notional_usd / float(starting_equity_usd)

        records.append(
            H021StopPrecursorRecord(
                symbol=fill.symbol,
                side=fill.side,
                exit_reason=fill.exit_reason,
                decision_time=context.decision_time,
                entry_time=context.entry_time,
                decision_hour_utc=f"{context.decision_time.hour:02d}",
                entry_hour_utc=f"{context.entry_time.hour:02d}",
                entry_raw_price=context.entry_raw_price,
                stop_price=context.stop_price,
                raw_stop_distance=context.raw_stop_distance,
                stop_distance_spread_multiple=context.stop_distance_spread_multiple,
                stop_distance_spread_bucket=_stop_distance_spread_bucket(
                    context.stop_distance_spread_multiple
                ),
                signed_risk_fraction=context.signed_risk_fraction,
                lots=float(fill.lots),
                estimated_notional_usd=notional_usd,
                estimated_gross_leverage=gross_leverage,
                estimated_gross_leverage_bucket=_gross_leverage_bucket(gross_leverage),
                pnl_usd=fill_pnl_usd(fill=fill),
            )
        )

    return tuple(records)


def summarize_records_by_fields(
    records: Iterable[H021StopPrecursorRecord],
    *,
    group_fields: Sequence[str],
) -> tuple[H021StopPrecursorSummaryRow, ...]:
    """Summarize realized outcomes by decision-time observable fields."""
    _validate_group_fields(group_fields)

    raw_records = []
    for record in records:
        raw_records.append(
            {
                field: getattr(record, field)
                for field in _ALLOWED_GROUP_FIELDS
            }
            | {
                "pnl_usd": record.pnl_usd,
                "is_stop": record.exit_reason == "stop",
            }
        )

    if not raw_records:
        return ()

    frame = pd.DataFrame.from_records(raw_records)
    groupby_key: str | list[str] = group_fields[0] if len(group_fields) == 1 else list(group_fields)
    grouped = frame.groupby(groupby_key, dropna=False, sort=True)

    rows: list[H021StopPrecursorSummaryRow] = []
    for key, group in grouped:
        key_tuple = _normalize_group_key(key=key, group_fields=group_fields)
        pnl = group["pnl_usd"].astype(float)
        winning = pnl[pnl > 0.0]
        losing = pnl[pnl < 0.0]

        gross_profit = float(winning.sum())
        gross_loss = float(losing.sum())
        profit_factor = gross_profit / abs(gross_loss) if gross_loss < 0.0 else float("nan")

        rows.append(
            H021StopPrecursorSummaryRow(
                group=key_tuple,
                fill_count=int(len(group)),
                stop_count=int(group["is_stop"].sum()),
                stop_rate=float(group["is_stop"].mean()),
                winning_fill_count=int(len(winning)),
                losing_fill_count=int(len(losing)),
                total_pnl_usd=float(pnl.sum()),
                mean_pnl_usd=float(pnl.mean()),
                median_pnl_usd=float(pnl.median()),
                gross_profit_usd=gross_profit,
                gross_loss_usd=gross_loss,
                profit_factor=profit_factor,
            )
        )

    return tuple(rows)


def format_stop_precursor_table(
    rows: Sequence[H021StopPrecursorSummaryRow],
    *,
    title: str,
) -> str:
    """Format precursor summary rows as a compact console table."""
    lines = [title, "-" * len(title)]

    if not rows:
        lines.append("(no fills)")
        return "\n".join(lines)

    header = (
        "group | fills | stops | stop_rate | total_pnl_usd | mean_pnl_usd | "
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
                    str(row.stop_count),
                    _format_percent(row.stop_rate),
                    f"{row.total_pnl_usd:.2f}",
                    f"{row.mean_pnl_usd:.2f}",
                    f"{row.median_pnl_usd:.2f}",
                    _format_float(row.profit_factor),
                ]
            )
        )

    return "\n".join(lines)


def main() -> None:
    print("H021 stop-loss precursor diagnostic from H020 strict event fills")
    print("=" * 74)
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

    shim = run_h020_bridge_shim(
        usdjpy_ohlcv=usdjpy_h4.bars,
        xauusd_ohlcv=xauusd_h4.bars,
    )
    contexts = build_decision_contexts(
        h017_result=shim,
        h4_by_symbol={"USDJPY": usdjpy_h4.bars, "XAUUSD": xauusd_h4.bars},
        accepted_entry_times=assessment.accepted_timestamps,
    )
    records = enrich_fills_with_decision_context(
        result.backtest.fills,
        contexts,
        starting_equity_usd=10000.0,
    )

    print(f"Context rows reconstructed: {len(contexts)}")
    print(f"Fill rows enriched: {len(records)}")
    print()

    for title, fields in (
        ("By decision hour UTC", ("decision_hour_utc",)),
        ("By entry hour UTC", ("entry_hour_utc",)),
        ("By stop distance / spread bucket", ("stop_distance_spread_bucket",)),
        ("By estimated gross leverage bucket", ("estimated_gross_leverage_bucket",)),
        ("By symbol / side / stop distance bucket", ("symbol", "side", "stop_distance_spread_bucket")),
        ("By symbol / side / decision hour UTC", ("symbol", "side", "decision_hour_utc")),
    ):
        print(format_stop_precursor_table(
            summarize_records_by_fields(records, group_fields=fields),
            title=title,
        ))
        print()

    print("Verdict reminder: precursor decomposition is evidence gathering only.")
    print("No live trading is approved. Phase 4 is not approved.")


def _estimated_notional_usd(
    *,
    symbol: str,
    lots: float,
    entry_raw_price: float,
) -> float:
    spec = get_default_instrument_spec(symbol)

    if spec.quote_currency.upper() == "JPY":
        return float(lots) * spec.contract_size

    if spec.quote_currency.upper() == "USD":
        return float(lots) * spec.contract_size * float(entry_raw_price)

    raise ValueError(f"unsupported quote currency {spec.quote_currency!r}")


def _stop_distance_spread_bucket(spread_multiple: float) -> str:
    if spread_multiple < 2.0:
        return "<2x"
    if spread_multiple < 5.0:
        return "2-5x"
    if spread_multiple < 10.0:
        return "5-10x"
    if spread_multiple < 20.0:
        return "10-20x"
    if spread_multiple < 50.0:
        return "20-50x"
    return ">=50x"


def _gross_leverage_bucket(gross_leverage: float) -> str:
    if gross_leverage < 1.0:
        return "<1x"
    if gross_leverage < 3.0:
        return "1-3x"
    if gross_leverage < 6.0:
        return "3-6x"
    if gross_leverage < 9.0:
        return "6-9x"
    return ">=9x"


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
