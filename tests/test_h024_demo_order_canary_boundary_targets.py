from pathlib import Path


def test_canary_boundary_static_verifier_includes_new_pure_python_surfaces():
    source = Path("quantcore/execution/h024_demo_adapter_boundary_static_verifier.py").read_text(
        encoding="utf-8-sig"
    ).replace("\\", "/")

    expected_targets = {
        "quantcore/execution/h024_demo_order_canary_readiness_human_decision.py",
        "quantcore/execution/h024_demo_order_canary_hard_controls_preflight_packet.py",
        "scripts/build_h024_demo_order_canary_readiness_human_decision_jsonl.py",
        "scripts/verify_h024_demo_order_canary_readiness_human_decision_jsonl.py",
        "scripts/build_h024_demo_order_canary_hard_controls_preflight_packet_jsonl.py",
        "scripts/verify_h024_demo_order_canary_hard_controls_preflight_packet_jsonl.py",
    }
    missing = sorted(target for target in expected_targets if target not in source)
    assert missing == []