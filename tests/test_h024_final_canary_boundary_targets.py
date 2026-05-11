from pathlib import Path


def test_final_canary_boundary_static_verifier_includes_approval_and_audit_surfaces():
    source = Path("quantcore/execution/h024_demo_adapter_boundary_static_verifier.py").read_text(
        encoding="utf-8-sig"
    ).replace("\\", "/")

    expected_targets = {
        "quantcore/execution/h024_demo_order_canary_human_approval.py",
        "quantcore/execution/h024_final_pre_dispatch_audit_packet.py",
        "scripts/build_h024_demo_order_canary_human_approval_jsonl.py",
        "scripts/verify_h024_demo_order_canary_human_approval_jsonl.py",
        "scripts/build_h024_final_pre_dispatch_audit_packet_jsonl.py",
        "scripts/verify_h024_final_pre_dispatch_audit_packet_jsonl.py",
    }
    missing = sorted(target for target in expected_targets if target not in source)
    assert missing == []