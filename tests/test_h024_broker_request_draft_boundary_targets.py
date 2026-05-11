from __future__ import annotations

from pathlib import Path


NEW_BOUNDARY_TARGETS = {
    "quantcore/execution/h024_broker_request_draft_construction_approval.py",
    "quantcore/execution/h024_broker_request_draft_envelope.py",
    "scripts/build_h024_broker_request_draft_construction_approval_jsonl.py",
    "scripts/verify_h024_broker_request_draft_construction_approval_jsonl.py",
    "scripts/build_h024_broker_request_draft_envelope_jsonl.py",
    "scripts/verify_h024_broker_request_draft_envelope_jsonl.py",
}


def test_new_draft_files_are_present_for_boundary_scanning() -> None:
    for path in NEW_BOUNDARY_TARGETS:
        assert Path(path).exists(), path


def test_boundary_static_verifier_mentions_new_draft_files() -> None:
    source = Path("quantcore/execution/h024_demo_adapter_boundary_static_verifier.py").read_text(encoding="utf-8")
    for path in NEW_BOUNDARY_TARGETS:
        assert path.replace("/", "\\") in source or path in source