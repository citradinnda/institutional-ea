import pytest

from quantcore.execution.h024_demo_order_plan import (
    H024DemoAccountContext,
    H024DemoOrderPlanError,
    build_h024_demo_order_plan,
)


def valid_request(**overrides):
    request = {
        "schema_version": "h024_dry_run_execution_request_v1",
        "request_kind": "DRY_RUN_MARKET_OPEN",
        "source_schema_version": "h024_intended_action_log_v1",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "timeframe": "H4",
        "side": "SELL",
        "entry_price": 4930.041,
        "stop_loss": 5019.068,
        "risk_usd": 100.0,
        "volume_lots": 0.01,
        "timestamp": "2026.05.11 07:45:49",
        "source_reason": (
            "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;"
            "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
        ),
    }
    request.update(overrides)
    return request


def valid_context(**overrides):
    context = {
        "server": "Exness-MT5Trial6",
        "account_currency": "USD",
        "account_balance": 10000.0,
        "account_equity": 10000.0,
        "broker": "Exness Technologies Ltd",
        "account_login": "demo-redacted",
    }
    context.update(overrides)
    return context


def test_builds_review_only_demo_order_plan_from_verified_dry_run_request():
    plan = build_h024_demo_order_plan(valid_request(), valid_context())

    assert plan.schema_version == "h024_demo_order_plan_v1"
    assert plan.plan_kind == "PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY"
    assert plan.source_schema_version == "h024_intended_action_log_v1"
    assert plan.source_request_kind == "DRY_RUN_MARKET_OPEN"
    assert plan.symbol == "XAUUSDm"
    assert plan.normalized_symbol == "XAUUSD"
    assert plan.timeframe == "H4"
    assert plan.side == "SELL"
    assert plan.entry_price == pytest.approx(4930.041)
    assert plan.stop_loss == pytest.approx(5019.068)
    assert plan.volume_lots == pytest.approx(0.01)
    assert plan.risk_usd == pytest.approx(100.0)
    assert plan.source_timestamp == "2026.05.11 07:45:49"
    assert "mode=log_only_no_execution" in plan.source_reason
    assert plan.account_server == "Exness-MT5Trial6"
    assert plan.account_currency == "USD"
    assert plan.account_balance == pytest.approx(10000.0)
    assert plan.account_equity == pytest.approx(10000.0)


def test_accepts_explicit_dataclass_context_and_allowlist():
    context = H024DemoAccountContext(
        server="Research-Demo-Only",
        account_currency="USD",
        account_balance=10000.0,
        account_equity=9999.0,
    )

    plan = build_h024_demo_order_plan(
        valid_request(
            symbol="USDJPYm",
            normalized_symbol="USDJPY",
            side="BUY",
            entry_price=150.0,
            stop_loss=149.0,
        ),
        context,
        allowed_demo_servers={"Research-Demo-Only"},
    )

    assert plan.symbol == "USDJPYm"
    assert plan.normalized_symbol == "USDJPY"
    assert plan.side == "BUY"
    assert plan.account_server == "Research-Demo-Only"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema_version", "wrong"),
        ("request_kind", "WRONG_KIND"),
        ("source_schema_version", "wrong"),
        ("timeframe", "M1"),
        ("side", "HOLD"),
        ("entry_price", 0),
        ("stop_loss", -1),
        ("risk_usd", 0),
        ("volume_lots", 0),
        ("source_reason", "WOULD_OPEN:side=short"),
    ],
)
def test_rejects_invalid_dry_run_request_fields(field, value):
    with pytest.raises(H024DemoOrderPlanError):
        build_h024_demo_order_plan(valid_request(**{field: value}), valid_context())


def test_rejects_unknown_symbol():
    with pytest.raises(H024DemoOrderPlanError, match="unsupported symbol"):
        build_h024_demo_order_plan(
            valid_request(symbol="EURUSDm", normalized_symbol="EURUSD"),
            valid_context(),
        )


def test_rejects_mismatched_symbol_normalization():
    with pytest.raises(H024DemoOrderPlanError, match="normalized_symbol"):
        build_h024_demo_order_plan(
            valid_request(symbol="XAUUSDm", normalized_symbol="USDJPY"),
            valid_context(),
        )


@pytest.mark.parametrize(
    "candidate_request",
    [
        valid_request(side="SELL", entry_price=4930.0, stop_loss=4929.0),
        valid_request(side="BUY", entry_price=150.0, stop_loss=150.0),
        valid_request(side="BUY", entry_price=150.0, stop_loss=151.0),
    ],
)
def test_rejects_invalid_stop_geometry(candidate_request):
    with pytest.raises(H024DemoOrderPlanError):
        build_h024_demo_order_plan(candidate_request, valid_context())


def test_rejects_unknown_server_even_if_it_sounds_demo_like():
    with pytest.raises(H024DemoOrderPlanError, match="demo allowlist"):
        build_h024_demo_order_plan(
            valid_request(),
            valid_context(server="Unknown-Demo-Server"),
        )


@pytest.mark.parametrize("server", ["Exness-Live", "Research-Real", "Prod-Demo"])
def test_rejects_live_like_server_names_before_allowlist(server):
    with pytest.raises(H024DemoOrderPlanError, match="live-like"):
        build_h024_demo_order_plan(
            valid_request(),
            valid_context(server=server),
            allowed_demo_servers={server},
        )


def test_rejects_non_usd_account_context():
    with pytest.raises(H024DemoOrderPlanError, match="account_currency"):
        build_h024_demo_order_plan(
            valid_request(),
            valid_context(account_currency="EUR"),
        )


def test_requires_non_empty_allowlist_when_overridden():
    with pytest.raises(H024DemoOrderPlanError, match="allowed_demo_servers"):
        build_h024_demo_order_plan(
            valid_request(),
            valid_context(),
            allowed_demo_servers=[],
        )

