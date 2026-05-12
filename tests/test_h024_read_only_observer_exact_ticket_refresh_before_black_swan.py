from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[1]
OBSERVER = REPO_ROOT / "scripts" / "run_h024_read_only_vps_observer_once.ps1"

EXACT_TICKET_BUILDERS = [
    "build_h024_exact_ticket_canary_close_modify_governance_jsonl.py",
    "build_h024_exact_ticket_canary_close_modify_decision_artifact_jsonl.py",
    "build_h024_exact_ticket_canary_close_modify_pre_action_evidence_aggregate_jsonl.py",
    "build_h024_exact_ticket_canary_close_modify_bar_age_exit_condition_evidence_jsonl.py",
    "build_h024_exact_ticket_canary_close_modify_manual_approval_gate_preview_jsonl.py",
    "build_h024_exact_ticket_canary_close_modify_operator_decision_v2_preview_jsonl.py",
    "build_h024_exact_ticket_canary_close_modify_execution_readiness_dry_run_schema_preview_jsonl.py",
]

BLACK_SWAN_BUILDER = "build_h024_read_only_black_swan_guard_jsonl.py"


def _observer_text() -> str:
    assert OBSERVER.exists(), f"missing observer script: {OBSERVER}"
    return OBSERVER.read_text(encoding="utf-8")


def test_exact_ticket_read_only_evidence_refreshes_before_black_swan_guard() -> None:
    text = _observer_text()

    black_swan_index = text.find(BLACK_SWAN_BUILDER)
    assert black_swan_index >= 0, "black-swan guard builder is missing from observer"

    for builder in EXACT_TICKET_BUILDERS:
        builder_index = text.find(builder)
        assert builder_index >= 0, f"{builder} is missing from observer"
        assert builder_index < black_swan_index, (
            f"{builder} must run before {BLACK_SWAN_BUILDER}"
        )


def test_observer_declares_refresh_is_read_only_and_non_authorizing() -> None:
    text = _observer_text()

    assert "exact-ticket read-only evidence refresh" in text.lower()
    assert "does not authorize trading" in text.lower()
    assert "H024 remains read-only" in text


def test_h024_observer_still_has_no_order_capable_calls() -> None:
    text = _observer_text()

    forbidden_patterns = [
        r"\border_send\s*\(",
        r"\.order_send\s*\(",
        r"\border_check\s*\(",
        r"\.order_check\s*\(",
        r"\bsymbol_select\s*\(",
        r"\.symbol_select\s*\(",
        r"\bTRADE_ACTION\b",
        r"\bORDER_TYPE_BUY\b",
        r"\bORDER_TYPE_SELL\b",
        r"\bMqlTradeRequest\b",
    ]

    for pattern in forbidden_patterns:
        assert re.search(pattern, text) is None, f"forbidden H024 pattern found: {pattern}"
