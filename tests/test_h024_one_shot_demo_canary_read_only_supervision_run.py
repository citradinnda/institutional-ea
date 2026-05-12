from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from quantcore.execution.h024_one_shot_demo_canary_read_only_supervision_run import (
    SupervisionStage,
    assert_stage_commands_are_read_only,
    default_stages,
    run_read_only_supervision,
    verify_supervision_run_record,
)


@dataclass
class FakeCompleted:
    returncode: int
    stdout: str = ""
    stderr: str = ""


def test_read_only_supervision_passes_all_default_stages() -> None:
    called: list[str] = []

    def runner(command: tuple[str, ...], cwd: Path) -> FakeCompleted:
        called.append(command[1])
        return FakeCompleted(returncode=0, stdout="ok\n")

    record = run_read_only_supervision(command_runner=runner, generated_at_utc="2026-05-12T00:00:00Z")

    assert record["verdict"] == "PASS"
    assert record["violations"] == []
    assert record["completed_stage_count"] == record["stage_count"] == 8
    assert record["first_failed_stage"] is None
    assert record["broker_mutation_authorized"] is False
    assert record["trading_loop_authorized"] is False
    assert record["automation_boundary"]["read_only_stack_automated"] is True
    assert record["automation_boundary"]["broker_mutation_automated"] is False
    assert record["automation_boundary"]["usd_jpy_requires_separate_readiness"] is True
    assert record["automation_boundary"]["kill_switches_required_before_trading_loop"] is True
    assert record["automation_boundary"]["black_swan_guards_required_before_trading_loop"] is True
    assert called == [stage.command[1] for stage in default_stages()]


def test_read_only_supervision_fails_closed_and_stops_after_failed_stage() -> None:
    calls = 0

    def runner(command: tuple[str, ...], cwd: Path) -> FakeCompleted:
        nonlocal calls
        calls += 1
        if calls == 3:
            return FakeCompleted(returncode=7, stdout="", stderr="failed")
        return FakeCompleted(returncode=0, stdout="ok")

    record = run_read_only_supervision(command_runner=runner)

    assert record["verdict"] == "FAIL"
    assert record["first_failed_stage"] == "build_lifecycle_decision"
    assert record["completed_stage_count"] == 2
    assert len(record["stages"]) == 3
    assert record["operator_next_action"] == "stop_and_investigate_failed_read_only_stage_no_broker_mutation"
    assert record["broker_mutation_authorized"] is False
    assert any("stage failed: build_lifecycle_decision" in violation for violation in record["violations"])


def test_read_only_supervision_preflight_rejects_send_command() -> None:
    stages = (
        SupervisionStage(
            name="bad_send",
            command=("python", "scripts/run_h024_one_shot_demo_canary.py", "--send"),
            description="bad",
            mt5_access="mutation",
        ),
    )

    record = run_read_only_supervision(stages=stages, command_runner=lambda command, cwd: FakeCompleted(0))

    assert record["verdict"] == "FAIL"
    assert record["completed_stage_count"] == 0
    assert record["first_failed_stage"] is None
    assert any("forbidden fragment" in violation for violation in record["violations"])


def test_default_stage_commands_are_read_only() -> None:
    assert assert_stage_commands_are_read_only(default_stages()) == []


def test_supervision_verifier_rejects_tampered_broker_mutation_flag() -> None:
    record = run_read_only_supervision(command_runner=lambda command, cwd: FakeCompleted(0))
    record["broker_mutation_authorized"] = True

    violations = verify_supervision_run_record(record, require_pass=True)

    assert "broker_mutation_authorized must be False" in violations


def test_supervision_verifier_rejects_tampered_automation_boundary() -> None:
    record = run_read_only_supervision(command_runner=lambda command, cwd: FakeCompleted(0))
    record["automation_boundary"]["broker_mutation_automated"] = True

    violations = verify_supervision_run_record(record, require_pass=True)

    assert "broker_mutation_automated must be False" in violations


def test_supervision_module_is_not_direct_mt5_or_mutation_code() -> None:
    source = Path("quantcore/execution/h024_one_shot_demo_canary_read_only_supervision_run.py").read_text(encoding="utf-8")

    assert "import MetaTrader5" not in source
    assert "MetaTrader5 as" not in source
    assert "mt5." not in source
    assert ".order_send(" not in source
    assert ".order_check(" not in source
