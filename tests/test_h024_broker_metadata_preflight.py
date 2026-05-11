import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path

import pytest

from quantcore.execution.h024_broker_metadata_preflight import (
    H024BrokerMetadataPreflightError,
    H024SymbolMetadata,
    build_h024_broker_metadata_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_h024_broker_metadata_preflight_jsonl.py"
VERIFY_SCRIPT = ROOT / "scripts" / "verify_h024_broker_metadata_preflight_jsonl.py"


def run_cli(args):
    return subprocess.run(
        [sys.executable, *[str(arg) for arg in args]],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def write_jsonl(path, records):
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def valid_plan(**overrides):
    record = {
        "schema_version": "h024_demo_order_plan_v1",
        "plan_kind": "PROPOSED_DEMO_MARKET_OPEN_REVIEW_ONLY",
        "source_schema_version": "h024_intended_action_log_v1",
        "source_request_kind": "DRY_RUN_MARKET_OPEN",
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "timeframe": "H4",
        "side": "SELL",
        "entry_price": 4930.041,
        "stop_loss": 5019.068,
        "risk_usd": 100.0,
        "volume_lots": 0.01,
        "source_timestamp": "2026.05.11 07:45:49",
        "source_reason": (
            "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;"
            "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
        ),
        "account_server": "Exness-MT5Trial6",
        "account_currency": "USD",
        "account_balance": 10000.0,
        "account_equity": 10000.0,
        "broker": "Exness Technologies Ltd",
        "account_login": None,
    }
    record.update(overrides)
    return record


def valid_metadata(**overrides):
    record = {
        "symbol": "XAUUSDm",
        "normalized_symbol": "XAUUSD",
        "account_server": "Exness-MT5Trial6",
        "account_currency": "USD",
        "tick_size": 0.001,
        "tick_value": 0.1,
        "min_volume": 0.01,
        "max_volume": 200.0,
        "volume_step": 0.01,
        "volume_digits": 2,
        "price_digits": 3,
        "spread_points": 16.0,
        "metadata_source": "standard_demo_manual_snapshot",
    }
    record.update(overrides)
    return record


def test_builds_broker_metadata_preflight_for_standard_demo_plan():
    preflight = build_h024_broker_metadata_preflight(valid_plan(), valid_metadata())

    assert preflight.schema_version == "h024_broker_metadata_preflight_v1"
    assert preflight.preflight_kind == "BROKER_METADATA_PREFLIGHT_REVIEW_ONLY"
    assert preflight.symbol == "XAUUSDm"
    assert preflight.normalized_symbol == "XAUUSD"
    assert preflight.account_server == "Exness-MT5Trial6"
    assert preflight.tick_size == pytest.approx(0.001)
    assert preflight.tick_value == pytest.approx(0.1)
    assert preflight.estimated_loss_usd == pytest.approx(89.027)
    assert preflight.risk_fraction_of_balance == pytest.approx(0.01)
    assert "review_only_no_execution" in preflight.checks


@pytest.mark.parametrize(
    ("plan_override", "metadata_override", "match"),
    [
        ({"entry_price": 4930.0415}, {}, "entry_price is not aligned"),
        ({"volume_lots": 0.02}, {"min_volume": 0.015}, "volume_lots is not aligned"),
        ({"volume_lots": 0.001}, {}, "below min_volume"),
        ({"risk_usd": 100.01}, {}, "max risk fraction"),
        (
            {"risk_usd": 50.0},
            {},
            "metadata-estimated loss exceeds intended risk_usd",
        ),
        ({"account_server": "Exness-Live"}, {"account_server": "Exness-Live"}, "live-like"),
        ({}, {"symbol": "USDJPYm"}, "metadata symbol does not match"),
        ({"ticket": 12345}, {}, "execution-like key"),
    ],
)
def test_rejects_bad_preflight_inputs(plan_override, metadata_override, match):
    with pytest.raises(H024BrokerMetadataPreflightError, match=match):
        build_h024_broker_metadata_preflight(
            valid_plan(**plan_override),
            valid_metadata(**metadata_override),
            allowed_demo_servers={"Exness-MT5Trial6", "Exness-Live"},
        )


def test_builder_and_verifier_accept_standard_demo_jsonl(tmp_path):
    plan_jsonl = tmp_path / "plans.jsonl"
    metadata_json = tmp_path / "metadata.json"
    preflight_jsonl = tmp_path / "preflight.jsonl"

    write_jsonl(plan_jsonl, [valid_plan()])
    metadata_json.write_text(
        json.dumps(
            {
                "metadata_source": "standard_demo_manual_snapshot",
                "symbols": [valid_metadata()],
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    build = run_cli(
        [
            BUILD_SCRIPT,
            plan_jsonl,
            "--metadata-json",
            metadata_json,
            "--output-jsonl",
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )
    assert build.returncode == 0, build.stdout + build.stderr

    records = [
        json.loads(line)
        for line in preflight_jsonl.read_text(encoding="utf-8").splitlines()
    ]
    assert len(records) == 1
    assert records[0]["schema_version"] == "h024_broker_metadata_preflight_v1"
    assert records[0]["estimated_loss_usd"] == pytest.approx(89.027)

    verify = run_cli(
        [
            VERIFY_SCRIPT,
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )
    assert verify.returncode == 0, verify.stdout + verify.stderr


def test_builder_rejects_missing_symbol_metadata(tmp_path):
    plan_jsonl = tmp_path / "plans.jsonl"
    metadata_json = tmp_path / "metadata.json"
    preflight_jsonl = tmp_path / "preflight.jsonl"

    write_jsonl(plan_jsonl, [valid_plan(symbol="USDJPYm", normalized_symbol="USDJPY")])
    metadata_json.write_text(
        json.dumps({"symbols": [valid_metadata()]}),
        encoding="utf-8",
    )

    build = run_cli(
        [
            BUILD_SCRIPT,
            plan_jsonl,
            "--metadata-json",
            metadata_json,
            "--output-jsonl",
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )

    combined = build.stdout + build.stderr
    assert build.returncode == 1
    assert "missing metadata for symbol" in combined
    assert not preflight_jsonl.exists()


def test_verifier_rejects_execution_like_key(tmp_path):
    preflight_jsonl = tmp_path / "preflight.jsonl"
    record = asdict(build_h024_broker_metadata_preflight(valid_plan(), valid_metadata()))
    record["ticket"] = 123456
    write_jsonl(preflight_jsonl, [record])

    verify = run_cli(
        [
            VERIFY_SCRIPT,
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )

    combined = verify.stdout + verify.stderr
    assert verify.returncode == 1
    assert "execution-like key is forbidden" in combined


def test_verifier_rejects_mutated_estimated_loss(tmp_path):
    preflight_jsonl = tmp_path / "preflight.jsonl"
    record = asdict(build_h024_broker_metadata_preflight(valid_plan(), valid_metadata()))
    record["estimated_loss_usd"] = 1.0
    write_jsonl(preflight_jsonl, [record])

    verify = run_cli(
        [
            VERIFY_SCRIPT,
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )

    combined = verify.stdout + verify.stderr
    assert verify.returncode == 1
    assert "estimated_loss_usd mismatch" in combined


def test_verifier_rejects_missing_required_check(tmp_path):
    preflight_jsonl = tmp_path / "preflight.jsonl"
    record = asdict(build_h024_broker_metadata_preflight(valid_plan(), valid_metadata()))
    record["checks"] = ["review_only_no_execution"]
    write_jsonl(preflight_jsonl, [record])

    verify = run_cli(
        [
            VERIFY_SCRIPT,
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )

    combined = verify.stdout + verify.stderr
    assert verify.returncode == 1
    assert "checks is missing required checks" in combined


def test_builder_accepts_utf8_bom_metadata_json(tmp_path):
    plan_jsonl = tmp_path / "plans.jsonl"
    metadata_json = tmp_path / "metadata.json"
    preflight_jsonl = tmp_path / "preflight.jsonl"

    write_jsonl(plan_jsonl, [valid_plan()])
    metadata_payload = json.dumps(
        {
            "metadata_source": "standard_demo_manual_snapshot",
            "symbols": [valid_metadata()],
        },
        sort_keys=True,
    )
    metadata_json.write_bytes(("\ufeff" + metadata_payload).encode("utf-8"))

    build = run_cli(
        [
            BUILD_SCRIPT,
            plan_jsonl,
            "--metadata-json",
            metadata_json,
            "--output-jsonl",
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )

    assert build.returncode == 0, build.stdout + build.stderr
    assert preflight_jsonl.exists()


def test_builder_rejects_literal_backslash_n_after_metadata_json(tmp_path):
    plan_jsonl = tmp_path / "plans.jsonl"
    metadata_json = tmp_path / "metadata.json"
    preflight_jsonl = tmp_path / "preflight.jsonl"

    write_jsonl(plan_jsonl, [valid_plan()])
    metadata_payload = json.dumps(
        {
            "metadata_source": "standard_demo_manual_snapshot",
            "symbols": [valid_metadata()],
        },
        sort_keys=True,
    )
    metadata_json.write_text(metadata_payload + "\\n", encoding="utf-8")

    build = run_cli(
        [
            BUILD_SCRIPT,
            plan_jsonl,
            "--metadata-json",
            metadata_json,
            "--output-jsonl",
            preflight_jsonl,
            "--allowed-demo-server",
            "Exness-MT5Trial6",
            "--require-preflight",
        ]
    )

    assert build.returncode == 1
    assert "invalid metadata JSON" in (build.stdout + build.stderr)
    assert not preflight_jsonl.exists()
