from pathlib import Path

BUILDER = Path("scripts/build_h024_free_local_read_only_demo_deployment_readiness.ps1")
VERIFIER = Path("scripts/verify_h024_free_local_read_only_demo_deployment_readiness.ps1")
RUNBOOK = Path("docs/operations/H024_FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_RUNBOOK.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_demo_readiness_files_exist():
    assert BUILDER.exists()
    assert VERIFIER.exists()
    assert RUNBOOK.exists()


def test_builder_declares_capstone_contract_and_outputs():
    text = read(BUILDER)

    assert "free_local_read_only_demo_deployment_readiness" in text
    assert "h024_free_local_read_only_demo_deployment_readiness.json" in text
    assert "h024_free_local_read_only_demo_deployment_readiness.txt" in text
    assert "FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_OK_BUT_TRADING_NOT_AUTHORIZED" in text
    assert "FAIL_CLOSED_FREE_LOCAL_READ_ONLY_DEMO_DEPLOYMENT_READINESS_UNVERIFIED_NO_TRADING_AUTHORIZED" in text
    assert "read_only_demo_ready" in text
    assert "PASS means the free local Windows no-console read-only observer is demo-ready for status observation only." in text


def test_builder_validates_no_console_scheduler_contract():
    text = read(BUILDER)

    assert "H024 Read Only VPS Observer" in text
    assert "wscript.exe" in text
    assert "run_h024_read_only_vps_observer_scheduled_hidden.vbs" in text
    assert "scheduled_task_execute_not_wscript" in text
    assert "scheduled_task_argument_mismatch" in text
    assert "scheduled_task_interval_unverified" in text
    assert "ExpectedIntervalMinutes = 5" in text


def test_builder_consumes_required_upstream_packets():
    text = read(BUILDER)

    required = [
        "h024_read_only_vps_observer_healthcheck.json",
        "h024_read_only_vps_observer_task_state.json",
        "h024_read_only_vps_recovery_drill_preview.json",
        "h024_read_only_vps_observer_evidence_bundle.json",
        "h024_read_only_vps_observer_continuity_summary.json",
        "h024_read_only_vps_observer_scheduled_cadence_summary.json",
        "last_run_summary.json",
    ]

    for item in required:
        assert item in text


def test_builder_enforces_strict_extended_cadence_and_last_run_summary():
    text = read(BUILDER)

    assert "MinScheduledRunCount = 12" in text
    assert "MinScheduledSpanMinutes = 55" in text
    assert "scheduled_cadence_run_count_insufficient" in text
    assert "scheduled_cadence_span_insufficient" in text
    assert "scheduled_cadence_latest_run_stale" in text
    assert "last_run_not_completed" in text
    assert "last_run_exit_nonzero" in text
    assert "last_run_not_marked_read_only" in text


def test_builder_fails_closed_on_stale_missing_nonpass_unsafe_and_tracked_reports():
    text = read(BUILDER)

    required = [
        "packet_missing",
        "packet_malformed_json",
        "packet_timestamp_missing",
        "packet_stale",
        "packet_not_pass",
        "packet_unsafe_true_flags",
        "last_run_unsafe_true_flags",
        "reports_tracked_in_git",
        "git -C $RepoRoot ls-files -- reports",
    ]

    for item in required:
        assert item in text


def test_builder_and_verifier_do_not_contain_order_capable_calls_or_trade_request_shapes():
    combined = read(BUILDER) + "\n" + read(VERIFIER)

    forbidden_call_fragments = [
        "order_send(",
        ".order_send",
        "order_check(",
        ".order_check",
        "symbol_select(",
        ".symbol_select",
        "TRADE_ACTION",
        "ORDER_TYPE_BUY",
        "ORDER_TYPE_SELL",
        "MqlTradeRequest",
    ]

    for fragment in forbidden_call_fragments:
        assert fragment not in combined


def test_verifier_refreshes_prerequisites_and_runs_builder():
    text = read(VERIFIER)

    assert "check_h024_read_only_vps_observer_health.ps1" in text
    assert "check_h024_read_only_vps_observer_task_state.ps1" in text
    assert "run_h024_read_only_vps_recovery_drill_preview.ps1" in text
    assert "build_h024_read_only_vps_observer_evidence_bundle.ps1" in text
    assert "build_h024_read_only_vps_observer_continuity_summary.ps1" in text
    assert "build_h024_read_only_vps_observer_scheduled_cadence_summary.ps1" in text
    assert "build_h024_free_local_read_only_demo_deployment_readiness.ps1" in text
    assert "H024 FREE LOCAL READ-ONLY DEMO DEPLOYMENT READINESS: PASS" in text
    assert "No trading authorized. No broker mutation authorized." in text


def test_runbook_is_concise_and_preserves_safety_boundary():
    text = read(RUNBOOK)

    assert "free local Windows" in text
    assert "capstone" in text.lower()
    assert "does not authorize trading" in text
    assert "Do not commit reports/" in text
    assert "No Oracle VPS" in text
    assert "No paid VPS" in text