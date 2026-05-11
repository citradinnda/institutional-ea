from __future__ import annotations

from pathlib import Path


NEW_BOUNDARY_TARGETS = {
    "quantcore/execution/h024_mt5_request_shape_construction_approval.py",
    "quantcore/execution/h024_mt5_request_shape_preview_envelope.py",
    "scripts/build_h024_mt5_request_shape_construction_approval_jsonl.py",
    "scripts/verify_h024_mt5_request_shape_construction_approval_jsonl.py",
    "scripts/build_h024_mt5_request_shape_preview_envelope_jsonl.py",
    "scripts/verify_h024_mt5_request_shape_preview_envelope_jsonl.py",
}


def test_new_mt5_shape_preview_files_exist() -> None:
    for path in NEW_BOUNDARY_TARGETS:
        assert Path(path).exists(), path


def test_boundary_static_verifier_mentions_new_mt5_shape_preview_files() -> None:
    source = Path("quantcore/execution/h024_demo_adapter_boundary_static_verifier.py").read_text(encoding="utf-8")
    for path in NEW_BOUNDARY_TARGETS:
        assert path.replace("/", "\\") in source or path in source