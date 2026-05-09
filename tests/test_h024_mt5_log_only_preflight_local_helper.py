from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from scripts.run_h024_mt5_log_only_preflight_local import (
    EA_FILENAME,
    RUNTIME_LOG_FILENAME,
    LocalPreflightPaths,
    collect_runtime_log,
    compile_ea,
    copy_ea_source,
    reset_runtime_log,
    run_verify,
)


HEADER = (
    "generated_at_server,schema_version,ea_version,source_version,timer_seconds,"
    "runtime_mode,run_label,event,kill_switch_blocked,symbol,"
    "account_company,account_server,account_currency,account_balance,"
    "account_equity,account_leverage,account_trade_allowed,account_trade_expert,"
    "terminal_connected,terminal_trade_allowed,mql_trade_allowed,bid,ask,"
    "spread_points,volume_min,volume_max,volume_step,stops_level,freeze_level,"
    "point,digits,detail\n"
)


def valid_row(event: str = "INIT", symbol: str = "USDJPYm", detail: str = "blocked_by_default") -> str:
    return (
        "2026.05.09 22:00:00,h024_ea_log_only_preflight_v2,0.2,manual,1,"
        f"log_only_preflight,H024_LOG_ONLY_PREFLIGHT,{event},true,{symbol},"
        "Exness Technologies Ltd,Exness-MT5Trial6,USD,1246.45,1246.45,2000,"
        "true,true,true,false,true,156.676,156.694,18,0.01,300.00,0.01,0,0,"
        f"0.0010000000,3,{detail}\n"
    )


def test_local_paths_resolve_terminal_locations(tmp_path: Path) -> None:
    paths = LocalPreflightPaths(terminal_data_dir=tmp_path)

    assert paths.terminal_experts_dir == tmp_path / "MQL5" / "Experts"
    assert paths.terminal_files_dir == tmp_path / "MQL5" / "Files"
    assert paths.terminal_ea_source == tmp_path / "MQL5" / "Experts" / EA_FILENAME
    assert paths.terminal_ea_binary == tmp_path / "MQL5" / "Experts" / "H024_LogOnly_Preflight.ex5"
    assert paths.terminal_runtime_log == tmp_path / "MQL5" / "Files" / RUNTIME_LOG_FILENAME


def test_copy_ea_source_copies_repo_source_to_terminal_experts(tmp_path: Path) -> None:
    repo_source = tmp_path / "repo" / EA_FILENAME
    repo_source.parent.mkdir()
    repo_source.write_text("#property strict\n", encoding="utf-8")

    paths = LocalPreflightPaths(
        terminal_data_dir=tmp_path / "terminal",
        repo_ea_source=repo_source,
    )

    copied_to = copy_ea_source(paths)

    assert copied_to == paths.terminal_ea_source
    assert copied_to.read_text(encoding="utf-8") == "#property strict\n"


def test_copy_ea_source_rejects_missing_repo_source(tmp_path: Path) -> None:
    paths = LocalPreflightPaths(
        terminal_data_dir=tmp_path / "terminal",
        repo_ea_source=tmp_path / "missing.mq5",
    )

    with pytest.raises(FileNotFoundError, match="missing repo EA source"):
        copy_ea_source(paths)


def test_reset_runtime_log_removes_existing_terminal_csv(tmp_path: Path) -> None:
    paths = LocalPreflightPaths(terminal_data_dir=tmp_path / "terminal")
    paths.terminal_files_dir.mkdir(parents=True)
    paths.terminal_runtime_log.write_text("old\n", encoding="utf-8")

    assert reset_runtime_log(paths)
    assert not paths.terminal_runtime_log.exists()


def test_reset_runtime_log_returns_false_when_no_terminal_csv_exists(tmp_path: Path) -> None:
    paths = LocalPreflightPaths(terminal_data_dir=tmp_path / "terminal")

    assert not reset_runtime_log(paths)


def test_compile_ea_invokes_metaeditor_without_shell_and_accepts_zero_return(tmp_path: Path) -> None:
    metaeditor = tmp_path / "MetaEditor64.exe"
    source = tmp_path / EA_FILENAME
    ex5 = tmp_path / "H024_LogOnly_Preflight.ex5"
    metaeditor.write_text("stub", encoding="utf-8")
    source.write_text("#property strict\n", encoding="utf-8")
    ex5.write_text("compiled", encoding="utf-8")

    completed = Mock(returncode=0, stdout="", stderr="")

    with patch("scripts.run_h024_mt5_log_only_preflight_local.subprocess.run", return_value=completed) as run:
        result = compile_ea(metaeditor, source, timeout_seconds=7)

    assert result.return_code == 0
    assert result.accepted
    run.assert_called_once_with(
        [str(metaeditor), f"/compile:{source}"],
        capture_output=True,
        text=True,
        timeout=7,
        check=False,
    )


def test_compile_ea_accepts_nonzero_return_when_ex5_is_refreshed(tmp_path: Path) -> None:
    metaeditor = tmp_path / "MetaEditor64.exe"
    source = tmp_path / EA_FILENAME
    ex5 = tmp_path / "H024_LogOnly_Preflight.ex5"
    metaeditor.write_text("stub", encoding="utf-8")
    source.write_text("#property strict\n", encoding="utf-8")

    def fake_run(*_args: object, **_kwargs: object) -> Mock:
        ex5.write_text("compiled after warning", encoding="utf-8")
        return Mock(returncode=1, stdout="", stderr="")

    with patch("scripts.run_h024_mt5_log_only_preflight_local.subprocess.run", side_effect=fake_run):
        result = compile_ea(metaeditor, source, timeout_seconds=7)

    assert result.return_code == 1
    assert result.ex5_refreshed
    assert result.accepted


def test_compile_ea_rejects_nonzero_return_when_ex5_is_not_refreshed(tmp_path: Path) -> None:
    metaeditor = tmp_path / "MetaEditor64.exe"
    source = tmp_path / EA_FILENAME
    metaeditor.write_text("stub", encoding="utf-8")
    source.write_text("#property strict\n", encoding="utf-8")

    completed = Mock(returncode=2, stdout="", stderr="")

    with patch("scripts.run_h024_mt5_log_only_preflight_local.subprocess.run", return_value=completed):
        result = compile_ea(metaeditor, source, timeout_seconds=7)

    assert result.return_code == 2
    assert not result.ex5_refreshed
    assert not result.accepted


def test_compile_ea_rejects_missing_metaeditor(tmp_path: Path) -> None:
    source = tmp_path / EA_FILENAME
    source.write_text("#property strict\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="missing MetaEditor executable"):
        compile_ea(tmp_path / "missing.exe", source)


def test_collect_runtime_log_copies_terminal_csv_to_report_path(tmp_path: Path) -> None:
    terminal_data_dir = tmp_path / "terminal"
    runtime_log = terminal_data_dir / "MQL5" / "Files" / RUNTIME_LOG_FILENAME
    runtime_log.parent.mkdir(parents=True)
    runtime_log.write_text("header\nrow\n", encoding="utf-8")

    report_path = tmp_path / "repo" / "reports" / RUNTIME_LOG_FILENAME
    paths = LocalPreflightPaths(
        terminal_data_dir=terminal_data_dir,
        report_path=report_path,
    )

    collected = collect_runtime_log(paths)

    assert collected == report_path
    assert collected.read_text(encoding="utf-8") == "header\nrow\n"


def test_collect_runtime_log_rejects_missing_terminal_csv(tmp_path: Path) -> None:
    paths = LocalPreflightPaths(terminal_data_dir=tmp_path / "terminal")

    with pytest.raises(FileNotFoundError, match="missing terminal runtime log"):
        collect_runtime_log(paths)


def test_run_verify_accepts_valid_collected_runtime_log(tmp_path: Path) -> None:
    path = tmp_path / RUNTIME_LOG_FILENAME
    path.write_text(
        HEADER
        + valid_row(symbol="USDJPYm")
        + valid_row(event="INTENT", symbol="USDJPYm", detail="NO_ACTION:kill_switch_blocked")
        + valid_row(symbol="XAUUSDm")
        + valid_row(event="INTENT", symbol="XAUUSDm", detail="NO_ACTION:kill_switch_blocked"),
        encoding="utf-8",
    )

    rows, violations = run_verify(path)

    assert rows == 4
    assert violations == []
