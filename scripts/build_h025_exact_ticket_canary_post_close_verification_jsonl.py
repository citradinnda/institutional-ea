from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

STAGE4_REPORT_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_close_order_send.jsonl"
OUTPUT_JSONL_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_post_close_verification.jsonl"
OUTPUT_TEXT_PATH = REPO_ROOT / "reports" / "h025_exact_ticket_canary_post_close_verification.txt"

EXPECTED_ACCOUNT_SERVER = "Exness-MT5Trial6"
EXPECTED_SYMBOL = "XAUUSDm"
EXPECTED_VOLUME = 0.01
EXPECTED_TICKET = 4413054432
EXPECTED_IDENTIFIER = 4413054432
EXPECTED_MAGIC = 240024

REPORT_SCHEMA = "h025_exact_ticket_canary_post_close_verification.v2"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def as_dict(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "_asdict"):
        return dict(value._asdict())
    return {
        name: getattr(value, name)
        for name in dir(value)
        if not name.startswith("_") and not callable(getattr(value, name))
    }


def read_first_jsonl(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            return None
        return value if isinstance(value, dict) else None

    return None


def violation(code: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": "ERROR", "message": message}


def summarize_stage4_runtime_report(stage4: dict[str, Any] | None) -> dict[str, Any]:
    """Summarize volatile Stage 4 runtime evidence without making it a hard gate.

    reports/ is intentionally untracked and can be overwritten by tests or fail-closed previews.
    Stage 5's authoritative verification is the current open positions/orders state.
    """

    if stage4 is None:
        return {
            "present": False,
            "usable_pass_evidence": False,
            "note": "Stage 4 runtime report is missing or malformed; not used as hard gate.",
        }

    return {
        "present": True,
        "usable_pass_evidence": (
            stage4.get("verdict") == "PASS"
            and stage4.get("stage") == "H025_STAGE_4_EXACT_TICKET_CLOSE_ORDER_SEND"
            and stage4.get("exact_ticket") == EXPECTED_TICKET
            and stage4.get("exact_identifier") == EXPECTED_IDENTIFIER
            and stage4.get("order_send_executed") is True
            and stage4.get("post_send_exact_ticket_open") is False
            and stage4.get("post_send_h024_position_count") == 0
            and stage4.get("post_send_h024_order_count") == 0
        ),
        "verdict": stage4.get("verdict"),
        "stage": stage4.get("stage"),
        "exact_ticket": stage4.get("exact_ticket"),
        "exact_identifier": stage4.get("exact_identifier"),
        "order_send_executed": stage4.get("order_send_executed"),
        "post_send_exact_ticket_open": stage4.get("post_send_exact_ticket_open"),
        "post_send_h024_position_count": stage4.get("post_send_h024_position_count"),
        "post_send_h024_order_count": stage4.get("post_send_h024_order_count"),
        "note": "Stage 4 report is volatile runtime context only; current MT5 exposure state is authoritative.",
    }


def build_record(
    *,
    account: dict[str, Any],
    exact_positions: list[dict[str, Any]],
    h024_positions: list[dict[str, Any]],
    h024_orders: list[dict[str, Any]],
    history_deal_matches: list[dict[str, Any]],
    stage4_summary: dict[str, Any],
    history_start: datetime,
    history_end: datetime,
) -> dict[str, Any]:
    verification_violations: list[dict[str, str]] = []

    if account.get("server") != EXPECTED_ACCOUNT_SERVER:
        verification_violations.append(
            violation(
                "account_server_unexpected",
                f"expected {EXPECTED_ACCOUNT_SERVER}; got {account.get('server')!r}.",
            )
        )

    exact_ticket_open = len(exact_positions) > 0
    open_canary_trade_exists = bool(h024_positions)

    if exact_ticket_open:
        verification_violations.append(
            violation("exact_ticket_still_open", f"ticket {EXPECTED_TICKET} is still open.")
        )

    if h024_positions:
        verification_violations.append(
            violation(
                "h024_positions_remain",
                f"expected zero H024 {EXPECTED_SYMBOL} magic {EXPECTED_MAGIC} positions; got {len(h024_positions)}.",
            )
        )

    if h024_orders:
        verification_violations.append(
            violation(
                "h024_orders_remain",
                f"expected zero H024 {EXPECTED_SYMBOL} magic {EXPECTED_MAGIC} pending orders; got {len(h024_orders)}.",
            )
        )

    verdict = "PASS" if not verification_violations else "FAIL_CLOSED"

    return {
        "schema": REPORT_SCHEMA,
        "generated_at_utc": iso_utc(utc_now()),
        "stage": "H025_STAGE_5_POST_CLOSE_VERIFICATION",
        "verdict": verdict,
        "operator_state": (
            "H025_EXACT_TICKET_CANARY_POST_CLOSE_VERIFIED_NO_OPEN_CANARY"
            if verdict == "PASS"
            else "FAIL_CLOSED_H025_EXACT_TICKET_CANARY_POST_CLOSE_UNVERIFIED"
        ),
        "operator_next_action": (
            "DOCUMENT_NO_OPEN_CANARY_TRADE_AND_DO_NOT_REOPEN_TO_SATISFY_H024"
            if verdict == "PASS"
            else "OPERATOR_REVIEW_REQUIRED_NO_NEW_ENTRIES_AUTHORIZED"
        ),
        "violations": verification_violations,
        "stage4_report_path": str(STAGE4_REPORT_PATH),
        "stage4_runtime_report_summary": stage4_summary,
        "account_server": EXPECTED_ACCOUNT_SERVER,
        "account_snapshot": account,
        "symbol": EXPECTED_SYMBOL,
        "exact_ticket": EXPECTED_TICKET,
        "exact_identifier": EXPECTED_IDENTIFIER,
        "magic": EXPECTED_MAGIC,
        "volume": EXPECTED_VOLUME,
        "read_only_verification_only": True,
        "order_check_executed": False,
        "order_send_executed": False,
        "symbol_select_executed": False,
        "broker_mutation_authorized": False,
        "entry_authorized": False,
        "close_all_authorized": False,
        "unattended_loop_authorized": False,
        "live_money_authorized": False,
        "post_close_verified": verdict == "PASS",
        "open_canary_trade_exists": open_canary_trade_exists,
        "exact_ticket_open": exact_ticket_open,
        "exact_ticket_positions": exact_positions,
        "h024_position_count": len(h024_positions),
        "h024_positions": h024_positions,
        "h024_order_count": len(h024_orders),
        "h024_orders": h024_orders,
        "history_query_start_utc": iso_utc(history_start),
        "history_query_end_utc": iso_utc(history_end),
        "history_deal_match_count": len(history_deal_matches),
        "history_deal_matches": history_deal_matches[:10],
    }


def write_outputs(record: dict[str, Any]) -> None:
    OUTPUT_JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSONL_PATH.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "H025 exact-ticket canary post-close verification",
        f"verdict: {record['verdict']}",
        f"operator_state: {record['operator_state']}",
        f"exact_ticket: {record['exact_ticket']}",
        f"exact_identifier: {record['exact_identifier']}",
        f"symbol: {record['symbol']}",
        f"magic: {record['magic']}",
        f"post_close_verified: {record['post_close_verified']}",
        f"open_canary_trade_exists: {record['open_canary_trade_exists']}",
        f"exact_ticket_open: {record['exact_ticket_open']}",
        f"h024_position_count: {record['h024_position_count']}",
        f"h024_order_count: {record['h024_order_count']}",
        f"history_deal_match_count: {record['history_deal_match_count']}",
        f"violations: {len(record['violations'])}",
        "Stage 4 report is volatile runtime context only; current open positions/orders are authoritative.",
        "No order_check, order_send, symbol_select, new entry, close-all, loop, or live-money execution is authorized by this packet.",
    ]
    OUTPUT_TEXT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_post_close_verification() -> int:
    import MetaTrader5 as mt5  # type: ignore[import-not-found]

    initialized = False
    try:
        initialized = bool(mt5.initialize())
        if not initialized:
            record = build_record(
                account={},
                exact_positions=[],
                h024_positions=[],
                h024_orders=[],
                history_deal_matches=[],
                stage4_summary=summarize_stage4_runtime_report(read_first_jsonl(STAGE4_REPORT_PATH)),
                history_start=utc_now(),
                history_end=utc_now(),
            )
            record["verdict"] = "FAIL_CLOSED"
            record["post_close_verified"] = False
            record["operator_state"] = "FAIL_CLOSED_H025_EXACT_TICKET_CANARY_POST_CLOSE_UNVERIFIED"
            record["operator_next_action"] = "OPERATOR_REVIEW_REQUIRED_NO_NEW_ENTRIES_AUTHORIZED"
            record["violations"] = [violation("mt5_initialize_failed", f"mt5.initialize failed: {mt5.last_error()}")]
            write_outputs(record)
            print(f"H025 exact-ticket canary post-close verification verdict: {record['verdict']}")
            print(f"Operator state: {record['operator_state']}")
            print(f"Violations: {len(record['violations'])}")
            print(f"JSON: {OUTPUT_JSONL_PATH}")
            print(f"Text: {OUTPUT_TEXT_PATH}")
            return 1

        account = as_dict(mt5.account_info())

        exact_positions = [as_dict(item) for item in list(mt5.positions_get(ticket=EXPECTED_TICKET) or [])]
        h024_positions = [
            as_dict(item)
            for item in list(mt5.positions_get(symbol=EXPECTED_SYMBOL) or [])
            if as_dict(item).get("magic") == EXPECTED_MAGIC
        ]
        h024_orders = [
            as_dict(item)
            for item in list(mt5.orders_get(symbol=EXPECTED_SYMBOL) or [])
            if as_dict(item).get("magic") == EXPECTED_MAGIC
        ]

        history_start = utc_now() - timedelta(days=14)
        history_end = utc_now() + timedelta(minutes=1)
        history_deals_raw = mt5.history_deals_get(history_start, history_end)
        history_deals = [as_dict(item) for item in list(history_deals_raw or [])]

        history_deal_matches = [
            deal
            for deal in history_deals
            if deal.get("position_id") == EXPECTED_IDENTIFIER
            or deal.get("order") == 4421682057
            or deal.get("ticket") == 3796464680
        ]

        record = build_record(
            account=account,
            exact_positions=exact_positions,
            h024_positions=h024_positions,
            h024_orders=h024_orders,
            history_deal_matches=history_deal_matches,
            stage4_summary=summarize_stage4_runtime_report(read_first_jsonl(STAGE4_REPORT_PATH)),
            history_start=history_start,
            history_end=history_end,
        )

        write_outputs(record)

        print(f"H025 exact-ticket canary post-close verification verdict: {record['verdict']}")
        print(f"Operator state: {record['operator_state']}")
        print(f"Violations: {len(record['violations'])}")
        print(f"Exact ticket: {EXPECTED_TICKET}")
        print(f"Exact identifier: {EXPECTED_IDENTIFIER}")
        print(f"post_close_verified: {record['post_close_verified']}")
        print(f"open_canary_trade_exists: {record['open_canary_trade_exists']}")
        print(f"exact_ticket_open: {record['exact_ticket_open']}")
        print(f"h024_position_count: {record['h024_position_count']}")
        print(f"h024_order_count: {record['h024_order_count']}")
        print(f"history_deal_match_count: {record['history_deal_match_count']}")
        print(f"stage4_runtime_report_usable_pass_evidence: {record['stage4_runtime_report_summary']['usable_pass_evidence']}")
        print(f"JSON: {OUTPUT_JSONL_PATH}")
        print(f"Text: {OUTPUT_TEXT_PATH}")

        return 0 if record["verdict"] == "PASS" else 1

    finally:
        if initialized:
            mt5.shutdown()


def main() -> int:
    return run_post_close_verification()


if __name__ == "__main__":
    raise SystemExit(main())
