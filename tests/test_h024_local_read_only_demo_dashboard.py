from pathlib import Path

LAUNCHER = Path("scripts/start_h024_local_read_only_demo_dashboard.ps1")
RUNBOOK = Path("docs/operations/H024_LOCAL_READ_ONLY_DEMO_DASHBOARD_RUNBOOK.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_dashboard_files_exist():
    assert LAUNCHER.exists()
    assert RUNBOOK.exists()


def test_launcher_is_demo_ux_layer_over_existing_readiness_verifier():
    text = read(LAUNCHER)

    assert "verify_h024_free_local_read_only_demo_deployment_readiness.ps1" in text
    assert "h024_free_local_read_only_demo_deployment_readiness.json" in text
    assert "reports" in text
    assert "demo" in text
    assert "h024_local_read_only_demo_dashboard.html" in text
    assert "READ-ONLY DEMO ONLY " in text
    assert "[char]0x2014" in text
    assert " NO TRADING AUTHORIZED" in text


def test_launcher_does_not_create_another_readiness_packet_name():
    text = read(LAUNCHER)

    assert "h024_local_read_only_demo_dashboard.json" not in text
    assert "local_read_only_demo_dashboard_readiness" not in text
    assert "free_local_read_only_demo_deployment_readiness" in text


def test_launcher_shows_required_operator_fields():
    text = read(LAUNCHER)

    required = [
        "Demo readiness",
        "No-console scheduled task",
        "Scheduled cadence",
        "Latest scheduled run",
        "Upstream packet summary",
        "Canary / account observation summary",
        "observed_execute",
        "observed_argument",
        "interval_ok",
        "observed_run_count",
        "observed_span_minutes",
        "exit_code",
    ]

    for item in required:
        assert item in text


def test_launcher_consumes_existing_reports_only_for_dashboard_content():
    text = read(LAUNCHER)

    expected_reports = [
        "h024_read_only_vps_observer_scheduled_cadence_summary.json",
        "last_run_summary.json",
        "h024_unified_post_canary_runtime_supervision",
        "h024_runtime_safety_aggregate",
        "h024_exposure_inventory_supervisor",
        "h024_account_risk_margin_supervisor",
    ]

    for item in expected_reports:
        assert item in text


def test_launcher_and_runbook_do_not_contain_order_capable_calls_or_broker_mutation_paths():
    combined = read(LAUNCHER) + "\n" + read(RUNBOOK)

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


def test_runbook_explains_launch_and_untracked_reports_boundary():
    text = read(RUNBOOK)

    assert "one-click operator console" in text
    assert "start_h024_local_read_only_demo_dashboard.ps1" in text
    assert "reports/demo/" in text
    assert "Do not commit reports/" in text
    assert "does not authorize trading" in text
    assert "No Oracle VPS" in text
    assert "No paid VPS" in text