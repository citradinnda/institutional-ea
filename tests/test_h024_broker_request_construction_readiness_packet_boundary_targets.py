from __future__ import annotations

from pathlib import Path


def test_adapter_boundary_static_verifier_includes_broker_request_construction_readiness_targets() -> None:
    source = Path("quantcore/execution/h024_demo_adapter_boundary_static_verifier.py").read_text(
        encoding="utf-8"
    )

    assert "quantcore/execution/h024_broker_request_construction_readiness_packet.py" in source
    assert "scripts/build_h024_broker_request_construction_readiness_packet_jsonl.py" in source
    assert "scripts/verify_h024_broker_request_construction_readiness_packet_jsonl.py" in source