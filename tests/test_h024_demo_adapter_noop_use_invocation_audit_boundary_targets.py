from __future__ import annotations

from pathlib import Path


def test_adapter_boundary_static_verifier_includes_noop_use_invocation_audit_targets() -> None:
    source = Path("quantcore/execution/h024_demo_adapter_boundary_static_verifier.py").read_text(
        encoding="utf-8"
    )

    assert "quantcore/execution/h024_demo_adapter_noop_use_invocation_audit.py" in source
    assert "scripts/build_h024_demo_adapter_noop_use_invocation_audit_jsonl.py" in source
    assert "scripts/verify_h024_demo_adapter_noop_use_invocation_audit_jsonl.py" in source