from __future__ import annotations

from pathlib import Path

import pytest

from quantcore.data.preflight import (
    RequiredFilesReport,
    assess_required_files,
    require_existing_files,
)


def test_assess_required_files_reports_all_present(tmp_path: Path) -> None:
    existing = tmp_path / "USDJPY" / "H4.csv"
    existing.parent.mkdir()
    existing.write_text("fake mt5 export", encoding="utf-8")

    result = assess_required_files([existing])

    assert isinstance(result, RequiredFilesReport)
    assert result.all_present is True
    assert result.missing_paths == ()
    assert result.statuses[0].path == existing
    assert result.statuses[0].exists is True


def test_assess_required_files_reports_missing_paths(tmp_path: Path) -> None:
    existing = tmp_path / "USDJPY" / "H4.csv"
    missing = tmp_path / "XAUUSD" / "M1.csv"
    existing.parent.mkdir()
    existing.write_text("fake mt5 export", encoding="utf-8")

    result = assess_required_files([existing, missing])

    assert result.all_present is False
    assert result.missing_paths == (missing,)
    assert [status.exists for status in result.statuses] == [True, False]


def test_require_existing_files_returns_report_when_all_files_exist(tmp_path: Path) -> None:
    existing = tmp_path / "USDJPY" / "M1.csv"
    existing.parent.mkdir()
    existing.write_text("fake mt5 export", encoding="utf-8")

    result = require_existing_files([existing], label="MT5 export")

    assert result.all_present is True
    assert result.missing_paths == ()


def test_require_existing_files_raises_clear_error_for_missing_files(tmp_path: Path) -> None:
    missing = tmp_path / "USDJPY" / "M1.csv"

    with pytest.raises(FileNotFoundError, match="MT5 export not found") as excinfo:
        require_existing_files([missing], label="MT5 export")

    assert str(missing) in str(excinfo.value)


def test_assess_required_files_accepts_string_paths(tmp_path: Path) -> None:
    existing = tmp_path / "XAUUSD" / "H4.csv"
    existing.parent.mkdir()
    existing.write_text("fake mt5 export", encoding="utf-8")

    result = assess_required_files([str(existing)])

    assert result.all_present is True
    assert result.statuses[0].path == existing


def test_assess_required_files_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="at least one required file"):
        assess_required_files([])
