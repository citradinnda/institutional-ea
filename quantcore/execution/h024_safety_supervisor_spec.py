"""H024 safety supervisor / kill-switch specification.

This module is intentionally specification-only and read-only. It imports no
MetaTrader5 package, performs no broker reads or writes, and authorizes no
entry, close, modify, order_check, order_send, or trading loop.

The purpose is to define the mandatory safety supervisor contract that must be
implemented before any automated H024 trading loop can exist.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


STRATEGY = "H024"
PACKET_TYPE = "h024_safety_supervisor_spec"
SCHEMA_VERSION = "1.0"

MODEL_SYMBOLS = ("XAUUSD", "USDJPY")
RUNTIME_SYMBOLS = {
    "XAUUSD": "XAUUSDm",
    "USDJPY": "USDJPYm",
}

REQUIRED_GLOBAL_GUARDS = (
    "global_no_new_entry_switch",
    "manual_override_lockout_file",
    "daily_loss_lockout",
    "max_floating_loss_lockout",
    "spread_shock_guard",
    "stale_tick_guard",
    "disconnected_terminal_guard",
    "margin_compression_guard",
    "volatility_expansion_black_swan_guard",
    "unexpected_position_order_lockout",
)

REQUIRED_SYMBOL_CIRCUIT_BREAKERS = (
    "symbol_no_new_entry_breaker",
    "symbol_max_floating_loss_breaker",
    "symbol_spread_shock_breaker",
    "symbol_stale_tick_breaker",
    "symbol_volatility_expansion_black_swan_breaker",
    "symbol_unexpected_position_order_breaker",
)

MUST_BE_FALSE_FIELDS = (
    "broker_mutation_authorized",
    "order_check_authorized",
    "order_send_authorized",
    "entry_authorized",
    "close_modify_authorized",
    "xauusd_order_authorized",
    "usdjpy_order_authorized",
    "trading_loop_authorized",
    "automatic_execution_authorized",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _guard(
    *,
    name: str,
    category: str,
    scope: str,
    trigger_source: str,
    required_runtime_inputs: list[str],
    fail_closed_condition: str,
    operator_action: str,
    blocks: list[str],
    configuration_required: bool = True,
) -> dict[str, Any]:
    return {
        "name": name,
        "category": category,
        "scope": scope,
        "status": "specified_not_runtime_enforced",
        "required_before_trading_loop": True,
        "configuration_required": configuration_required,
        "trigger_source": trigger_source,
        "required_runtime_inputs": required_runtime_inputs,
        "fail_closed_default": True,
        "fail_closed_condition": fail_closed_condition,
        "operator_action": operator_action,
        "blocks": blocks,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
    }


def _symbol_breaker(
    *,
    model_symbol: str,
    runtime_symbol: str,
    breaker_name: str,
    category: str,
    trigger_source: str,
    required_runtime_inputs: list[str],
    fail_closed_condition: str,
    blocks: list[str],
) -> dict[str, Any]:
    return {
        "name": breaker_name,
        "model_symbol": model_symbol,
        "runtime_symbol": runtime_symbol,
        "category": category,
        "scope": f"symbol:{model_symbol}",
        "status": "specified_not_runtime_enforced",
        "required_before_trading_loop": True,
        "trigger_source": trigger_source,
        "required_runtime_inputs": required_runtime_inputs,
        "fail_closed_default": True,
        "fail_closed_condition": fail_closed_condition,
        "blocks": blocks,
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
    }


def build_h024_safety_supervisor_spec_record(*, generated_at_utc: str | None = None) -> dict[str, Any]:
    """Build the read-only H024 safety supervisor specification record."""

    guards = {
        "global_no_new_entry_switch": _guard(
            name="global_no_new_entry_switch",
            category="operator_lockout",
            scope="global",
            trigger_source="lockout file or config flag",
            required_runtime_inputs=[
                "runtime lockout path",
                "operator acknowledgement state",
                "supervisor config",
            ],
            fail_closed_condition="missing config, unreadable lockout path, or active no-new-entry lock",
            operator_action="clear only through explicit governed operator action",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "manual_override_lockout_file": _guard(
            name="manual_override_lockout_file",
            category="operator_lockout",
            scope="global",
            trigger_source="manual override lock file",
            required_runtime_inputs=[
                "manual override lock path",
                "file existence state",
                "file contents",
            ],
            fail_closed_condition="manual lock file exists, is unreadable, malformed, or stale in an unsafe way",
            operator_action="inspect manual lock file and resolve with explicit operator note",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "daily_loss_lockout": _guard(
            name="daily_loss_lockout",
            category="loss_limit",
            scope="global",
            trigger_source="account equity and realized/unrealized daily P/L ledger",
            required_runtime_inputs=[
                "start-of-day equity",
                "current equity",
                "closed P/L since broker day start",
                "floating P/L",
                "configured daily loss threshold",
            ],
            fail_closed_condition="daily loss threshold breached or required P/L inputs unavailable",
            operator_action="stop new entries until next governed reset window",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "max_floating_loss_lockout": _guard(
            name="max_floating_loss_lockout",
            category="loss_limit",
            scope="global",
            trigger_source="aggregate open-position mark-to-market",
            required_runtime_inputs=[
                "open positions",
                "current symbol ticks",
                "aggregate floating P/L",
                "configured max floating loss threshold",
            ],
            fail_closed_condition="aggregate floating loss threshold breached or mark-to-market unavailable",
            operator_action="block all new entries and inspect exposure",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "spread_shock_guard": _guard(
            name="spread_shock_guard",
            category="market_quality",
            scope="global",
            trigger_source="per-symbol bid/ask spread state",
            required_runtime_inputs=[
                "bid",
                "ask",
                "point",
                "rolling spread baseline",
                "configured spread multiplier or hard cap",
            ],
            fail_closed_condition="spread exceeds hard cap, spread exceeds shock multiplier, or spread cannot be computed",
            operator_action="wait for spread normalization before permitting any entry review",
            blocks=["all_new_entries", "all_order_check", "all_order_send"],
        ),
        "stale_tick_guard": _guard(
            name="stale_tick_guard",
            category="market_quality",
            scope="global",
            trigger_source="latest tick timestamp",
            required_runtime_inputs=[
                "terminal time",
                "latest tick time per runtime symbol",
                "configured max tick age seconds",
            ],
            fail_closed_condition="latest tick is older than allowed age or timestamp is unavailable",
            operator_action="verify terminal connectivity and symbol subscription",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "disconnected_terminal_guard": _guard(
            name="disconnected_terminal_guard",
            category="platform_state",
            scope="global",
            trigger_source="MT5 terminal/account connectivity state",
            required_runtime_inputs=[
                "mt5.initialize result",
                "account_info",
                "terminal_info when available",
                "last successful read-only heartbeat",
            ],
            fail_closed_condition="terminal cannot initialize, account_info unavailable, or heartbeat stale",
            operator_action="restore terminal connectivity before any automation resumes",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "margin_compression_guard": _guard(
            name="margin_compression_guard",
            category="account_risk",
            scope="global",
            trigger_source="account margin state",
            required_runtime_inputs=[
                "equity",
                "margin",
                "margin_free",
                "margin_level",
                "configured margin floor",
                "configured free-margin floor",
            ],
            fail_closed_condition="margin level/free margin breaches configured floor or account margin state unavailable",
            operator_action="block entries and inspect account risk",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "volatility_expansion_black_swan_guard": _guard(
            name="volatility_expansion_black_swan_guard",
            category="market_regime_risk",
            scope="global",
            trigger_source="broker-native H4/M1 range and ATR expansion state",
            required_runtime_inputs=[
                "broker-native H4 bars",
                "broker-native M1 bars",
                "rolling ATR baseline",
                "latest range shock metric",
                "configured expansion threshold",
            ],
            fail_closed_condition="volatility expansion exceeds configured threshold or broker-native data unavailable",
            operator_action="block entries until volatility regime normalizes or new governance is approved",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
        "unexpected_position_order_lockout": _guard(
            name="unexpected_position_order_lockout",
            category="position_order_integrity",
            scope="global",
            trigger_source="positions_get and orders_get read-only reconciliation",
            required_runtime_inputs=[
                "open positions",
                "pending orders",
                "known governed tickets",
                "known governed magics",
                "strategy ledgers",
            ],
            fail_closed_condition="unexpected H024 position/order, unknown magic, duplicate canary, or ledger mismatch detected",
            operator_action="stop automation and reconcile broker state against ledgers",
            blocks=["all_new_entries", "all_order_check", "all_order_send", "trading_loop"],
        ),
    }

    symbol_circuit_breakers: dict[str, Any] = {}
    for model_symbol in MODEL_SYMBOLS:
        runtime_symbol = RUNTIME_SYMBOLS[model_symbol]
        symbol_circuit_breakers[model_symbol] = {
            "model_symbol": model_symbol,
            "runtime_symbol": runtime_symbol,
            "required_before_trading_loop": True,
            "broker_mutation_authorized": False,
            "order_check_authorized": False,
            "order_send_authorized": False,
            "entry_authorized": False,
            "close_modify_authorized": False,
            "trading_loop_authorized": False,
            "breakers": {
                "symbol_no_new_entry_breaker": _symbol_breaker(
                    model_symbol=model_symbol,
                    runtime_symbol=runtime_symbol,
                    breaker_name="symbol_no_new_entry_breaker",
                    category="symbol_lockout",
                    trigger_source="per-symbol lockout file or config flag",
                    required_runtime_inputs=[
                        "symbol lockout path",
                        "symbol config",
                        "operator acknowledgement state",
                    ],
                    fail_closed_condition="symbol lock active, missing, unreadable, or malformed",
                    blocks=["symbol_new_entries", "symbol_order_check", "symbol_order_send"],
                ),
                "symbol_max_floating_loss_breaker": _symbol_breaker(
                    model_symbol=model_symbol,
                    runtime_symbol=runtime_symbol,
                    breaker_name="symbol_max_floating_loss_breaker",
                    category="symbol_loss_limit",
                    trigger_source="per-symbol open-position mark-to-market",
                    required_runtime_inputs=[
                        "symbol open positions",
                        "symbol current tick",
                        "symbol floating P/L",
                        "configured symbol max floating loss",
                    ],
                    fail_closed_condition="symbol floating loss threshold breached or symbol mark-to-market unavailable",
                    blocks=["symbol_new_entries", "symbol_order_check", "symbol_order_send"],
                ),
                "symbol_spread_shock_breaker": _symbol_breaker(
                    model_symbol=model_symbol,
                    runtime_symbol=runtime_symbol,
                    breaker_name="symbol_spread_shock_breaker",
                    category="symbol_market_quality",
                    trigger_source="symbol bid/ask spread state",
                    required_runtime_inputs=[
                        "symbol bid",
                        "symbol ask",
                        "symbol point",
                        "symbol spread baseline",
                        "symbol spread shock threshold",
                    ],
                    fail_closed_condition="symbol spread exceeds threshold or cannot be computed",
                    blocks=["symbol_new_entries", "symbol_order_check", "symbol_order_send"],
                ),
                "symbol_stale_tick_breaker": _symbol_breaker(
                    model_symbol=model_symbol,
                    runtime_symbol=runtime_symbol,
                    breaker_name="symbol_stale_tick_breaker",
                    category="symbol_market_quality",
                    trigger_source="symbol latest tick timestamp",
                    required_runtime_inputs=[
                        "terminal time",
                        "symbol latest tick time",
                        "configured max symbol tick age seconds",
                    ],
                    fail_closed_condition="symbol tick age exceeds threshold or timestamp unavailable",
                    blocks=["symbol_new_entries", "symbol_order_check", "symbol_order_send"],
                ),
                "symbol_volatility_expansion_black_swan_breaker": _symbol_breaker(
                    model_symbol=model_symbol,
                    runtime_symbol=runtime_symbol,
                    breaker_name="symbol_volatility_expansion_black_swan_breaker",
                    category="symbol_regime_risk",
                    trigger_source="symbol broker-native H4/M1 range and ATR expansion",
                    required_runtime_inputs=[
                        "symbol broker-native H4 bars",
                        "symbol broker-native M1 bars",
                        "symbol ATR baseline",
                        "symbol latest range shock metric",
                        "configured symbol volatility threshold",
                    ],
                    fail_closed_condition="symbol volatility expansion exceeds threshold or broker-native data unavailable",
                    blocks=["symbol_new_entries", "symbol_order_check", "symbol_order_send"],
                ),
                "symbol_unexpected_position_order_breaker": _symbol_breaker(
                    model_symbol=model_symbol,
                    runtime_symbol=runtime_symbol,
                    breaker_name="symbol_unexpected_position_order_breaker",
                    category="symbol_position_order_integrity",
                    trigger_source="symbol positions_get and orders_get reconciliation",
                    required_runtime_inputs=[
                        "symbol open positions",
                        "symbol pending orders",
                        "known governed symbol tickets",
                        "known governed symbol magics",
                        "symbol ledgers",
                    ],
                    fail_closed_condition="unexpected symbol position/order, duplicate governed exposure, or ledger mismatch detected",
                    blocks=["symbol_new_entries", "symbol_order_check", "symbol_order_send", "trading_loop"],
                ),
            },
        }

    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "strategy": STRATEGY,
        "packet_type": PACKET_TYPE,
        "generated_at_utc": generated_at_utc or utc_now_iso(),
        "read_only": True,
        "specification_only": True,
        "implementation_status": "specified_not_runtime_enforced",
        "model_symbols": list(MODEL_SYMBOLS),
        "runtime_symbols": dict(RUNTIME_SYMBOLS),
        "broker_mutation_authorized": False,
        "order_check_authorized": False,
        "order_send_authorized": False,
        "entry_authorized": False,
        "close_modify_authorized": False,
        "xauusd_order_authorized": False,
        "usdjpy_order_authorized": False,
        "trading_loop_authorized": False,
        "automatic_execution_authorized": False,
        "guards_required_before_trading_loop": True,
        "black_swan_guards_required_before_trading_loop": True,
        "global_guards": guards,
        "symbol_circuit_breakers": symbol_circuit_breakers,
        "integration_requirements": [
            "All future H024 entry preview, request-shape, canary, and loop code must consume this supervisor state or its runtime successor.",
            "Any unreadable, missing, stale, or malformed guard input must fail closed.",
            "Any unexpected H024 position or pending order must block new entries and the trading loop.",
            "A manual lockout must override signal quality, sizing feasibility, and broker readiness.",
            "USDJPY must remain separately governed from the existing XAUUSDm canary.",
            "No trading loop can be implemented until these guards have runtime enforcement and tests.",
        ],
        "minimum_next_runtime_layers": [
            "configuration schema for thresholds and lockout paths",
            "read-only lockout file reader",
            "read-only account and terminal state heartbeat",
            "read-only per-symbol tick freshness and spread supervisor",
            "read-only margin and floating-P/L supervisor",
            "read-only broker-native volatility expansion supervisor",
            "read-only position/order reconciliation supervisor",
            "fail-closed aggregate supervisor verifier",
        ],
        "violations": [],
        "verdict": "PASS",
    }
    return record


def _walk_mappings(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _walk_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_mappings(child)


def _verify_false_authorizations(record: Mapping[str, Any], violations: list[str]) -> None:
    for mapping in _walk_mappings(record):
        name = mapping.get("name") or mapping.get("packet_type") or mapping.get("model_symbol") or "mapping"
        for field in MUST_BE_FALSE_FIELDS:
            if field in mapping and mapping.get(field) is not False:
                violations.append(f"{name}.{field}_must_be_false")


def verify_h024_safety_supervisor_spec_records(
    records: Iterable[Mapping[str, Any]],
    *,
    require_pass: bool = False,
) -> dict[str, Any]:
    loaded = [dict(record) for record in records]
    violations: list[str] = []

    if len(loaded) != 1:
        violations.append("expected_exactly_one_safety_supervisor_spec_record")

    record = loaded[0] if loaded else {}

    if record.get("schema_version") != SCHEMA_VERSION:
        violations.append("unexpected_schema_version")
    if record.get("strategy") != STRATEGY:
        violations.append("unexpected_strategy")
    if record.get("packet_type") != PACKET_TYPE:
        violations.append("unexpected_packet_type")
    if record.get("read_only") is not True:
        violations.append("read_only_must_be_true")
    if record.get("specification_only") is not True:
        violations.append("specification_only_must_be_true")
    if record.get("guards_required_before_trading_loop") is not True:
        violations.append("guards_required_before_trading_loop_must_be_true")
    if record.get("black_swan_guards_required_before_trading_loop") is not True:
        violations.append("black_swan_guards_required_before_trading_loop_must_be_true")

    if tuple(record.get("model_symbols", [])) != MODEL_SYMBOLS:
        violations.append("unexpected_model_symbols")
    if record.get("runtime_symbols") != RUNTIME_SYMBOLS:
        violations.append("unexpected_runtime_symbols")

    _verify_false_authorizations(record, violations)

    global_guards = record.get("global_guards")
    if not isinstance(global_guards, Mapping):
        violations.append("global_guards_missing")
        global_guards = {}

    for guard_name in REQUIRED_GLOBAL_GUARDS:
        guard = global_guards.get(guard_name)
        if not isinstance(guard, Mapping):
            violations.append(f"missing_global_guard_{guard_name}")
            continue
        if guard.get("required_before_trading_loop") is not True:
            violations.append(f"{guard_name}_not_required_before_trading_loop")
        if guard.get("fail_closed_default") is not True:
            violations.append(f"{guard_name}_must_fail_closed")
        if guard.get("status") != "specified_not_runtime_enforced":
            violations.append(f"{guard_name}_unexpected_status")
        if not guard.get("required_runtime_inputs"):
            violations.append(f"{guard_name}_missing_required_runtime_inputs")
        if not guard.get("fail_closed_condition"):
            violations.append(f"{guard_name}_missing_fail_closed_condition")
        if not guard.get("blocks"):
            violations.append(f"{guard_name}_missing_blocks")

    circuit_breakers = record.get("symbol_circuit_breakers")
    if not isinstance(circuit_breakers, Mapping):
        violations.append("symbol_circuit_breakers_missing")
        circuit_breakers = {}

    for model_symbol in MODEL_SYMBOLS:
        symbol_block = circuit_breakers.get(model_symbol)
        if not isinstance(symbol_block, Mapping):
            violations.append(f"missing_symbol_circuit_breakers_{model_symbol}")
            continue
        if symbol_block.get("runtime_symbol") != RUNTIME_SYMBOLS[model_symbol]:
            violations.append(f"{model_symbol}_unexpected_runtime_symbol")
        if symbol_block.get("required_before_trading_loop") is not True:
            violations.append(f"{model_symbol}_breakers_not_required_before_trading_loop")
        breakers = symbol_block.get("breakers")
        if not isinstance(breakers, Mapping):
            violations.append(f"{model_symbol}_breakers_missing")
            breakers = {}
        for breaker_name in REQUIRED_SYMBOL_CIRCUIT_BREAKERS:
            breaker = breakers.get(breaker_name)
            if not isinstance(breaker, Mapping):
                violations.append(f"missing_{model_symbol}_{breaker_name}")
                continue
            if breaker.get("model_symbol") != model_symbol:
                violations.append(f"{model_symbol}_{breaker_name}_unexpected_model_symbol")
            if breaker.get("runtime_symbol") != RUNTIME_SYMBOLS[model_symbol]:
                violations.append(f"{model_symbol}_{breaker_name}_unexpected_runtime_symbol")
            if breaker.get("required_before_trading_loop") is not True:
                violations.append(f"{model_symbol}_{breaker_name}_not_required_before_trading_loop")
            if breaker.get("fail_closed_default") is not True:
                violations.append(f"{model_symbol}_{breaker_name}_must_fail_closed")
            if not breaker.get("required_runtime_inputs"):
                violations.append(f"{model_symbol}_{breaker_name}_missing_required_runtime_inputs")
            if not breaker.get("fail_closed_condition"):
                violations.append(f"{model_symbol}_{breaker_name}_missing_fail_closed_condition")
            if not breaker.get("blocks"):
                violations.append(f"{model_symbol}_{breaker_name}_missing_blocks")

    embedded_violations = record.get("violations", [])
    if not isinstance(embedded_violations, list):
        violations.append("embedded_violations_not_list")
        embedded_violations = []

    if require_pass and record.get("verdict") != "PASS":
        violations.append("record_verdict_not_pass")
    if require_pass and embedded_violations:
        violations.append("record_contains_embedded_violations")

    return {
        "verdict": "PASS" if not violations else "FAIL",
        "violations": violations,
        "record_count": len(loaded),
        "record_verdict": record.get("verdict"),
        "embedded_violations": embedded_violations,
        "broker_mutation_authorized": record.get("broker_mutation_authorized"),
        "order_check_authorized": record.get("order_check_authorized"),
        "order_send_authorized": record.get("order_send_authorized"),
        "entry_authorized": record.get("entry_authorized"),
        "close_modify_authorized": record.get("close_modify_authorized"),
        "xauusd_order_authorized": record.get("xauusd_order_authorized"),
        "usdjpy_order_authorized": record.get("usdjpy_order_authorized"),
        "trading_loop_authorized": record.get("trading_loop_authorized"),
        "automatic_execution_authorized": record.get("automatic_execution_authorized"),
        "global_guard_count": len(global_guards),
        "symbol_count": len(circuit_breakers),
    }


def write_jsonl(record: Mapping[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    return path


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records