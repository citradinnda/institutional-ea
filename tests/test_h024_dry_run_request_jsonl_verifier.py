import json
from pathlib import Path

from scripts.verify_h024_dry_run_request_jsonl import verify_h024_dry_run_request_jsonl


def _valid_request(**overrides):
    row = {
        "entry_price": 4930.041,
        "normalized_symbol": "XAUUSD",
        "request_kind": "DRY_RUN_MARKET_OPEN",
        "risk_usd": 100.0,
        "schema_version": "h024_dry_run_execution_request_v1",
        "side": "SELL",
        "source_reason": (
            "WOULD_OPEN:side=short;closed_h4_time=2026.03.18 08:00:00;"
            "source=H024_STATE_OBSERVATION;mode=log_only_no_execution"
        ),
        "source_schema_version": "h024_intended_action_log_v1",
        "stop_loss": 5019.068,
        "symbol": "XAUUSDm",
        "timeframe": "H4",
        "timestamp": "2026.05.11 07:45:49",
        "volume_lots": 0.01,
    }
    row.update(overrides)
    return row


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )


def test_verify_h024_dry_run_request_jsonl_accepts_valid_request(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    _write_jsonl(path, [_valid_request()])

    result = verify_h024_dry_run_request_jsonl(path, require_request=True)

    assert result.passed
    assert result.requests == 1
    assert result.violations == []


def test_verify_h024_dry_run_request_jsonl_rejects_empty_when_required(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    path.write_text("", encoding="utf-8")

    result = verify_h024_dry_run_request_jsonl(path, require_request=True)

    assert not result.passed
    assert "JSONL must contain at least one dry-run request" in result.violations


def test_verify_h024_dry_run_request_jsonl_rejects_sell_stop_below_entry(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    _write_jsonl(path, [_valid_request(stop_loss=4900.0)])

    result = verify_h024_dry_run_request_jsonl(path)

    assert not result.passed
    assert any("SELL request stop_loss must be above entry_price" in item for item in result.violations)


def test_verify_h024_dry_run_request_jsonl_rejects_execution_like_keys(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    _write_jsonl(path, [_valid_request(order_ticket=123)])

    result = verify_h024_dry_run_request_jsonl(path)

    assert not result.passed
    assert any("execution-like keys" in item for item in result.violations)


def test_verify_h024_dry_run_request_jsonl_rejects_bad_normalization(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    _write_jsonl(path, [_valid_request(symbol="XAUUSDm", normalized_symbol="USDJPY")])

    result = verify_h024_dry_run_request_jsonl(path)

    assert not result.passed
    assert any("XAUUSD broker symbol must normalize to XAUUSD" in item for item in result.violations)


def test_verify_h024_dry_run_request_jsonl_rejects_missing_log_only_reason(tmp_path: Path) -> None:
    path = tmp_path / "requests.jsonl"
    _write_jsonl(path, [_valid_request(source_reason="WOULD_OPEN:side=short")])

    result = verify_h024_dry_run_request_jsonl(path)

    assert not result.passed
    assert any("mode=log_only_no_execution" in item for item in result.violations)
