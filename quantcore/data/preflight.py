from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class RequiredFileStatus:
    """Record one required local file check so operational failures are explicit."""

    path: Path
    exists: bool


@dataclass(frozen=True)
class RequiredFilesReport:
    """Summarize preflight checks before an expensive real-data process starts."""

    statuses: tuple[RequiredFileStatus, ...]
    missing_paths: tuple[Path, ...]
    all_present: bool


def assess_required_files(paths: Sequence[str | Path]) -> RequiredFilesReport:
    """Check required local files without raising so callers can decide how to report failures."""

    if not paths:
        raise ValueError("paths must contain at least one required file.")

    statuses = tuple(
        RequiredFileStatus(path=Path(path), exists=Path(path).exists())
        for path in paths
    )
    missing_paths = tuple(status.path for status in statuses if not status.exists)

    return RequiredFilesReport(
        statuses=statuses,
        missing_paths=missing_paths,
        all_present=not missing_paths,
    )


def require_existing_files(
    paths: Sequence[str | Path],
    *,
    label: str = "Required file",
) -> RequiredFilesReport:
    """Fail before loading data because missing MT5 exports should produce clear operator errors."""

    report = assess_required_files(paths)

    if report.all_present:
        return report

    missing_lines = "\n".join(f"- {path}" for path in report.missing_paths)
    plural = "s" if len(report.missing_paths) != 1 else ""
    raise FileNotFoundError(
        f"{label}{plural} not found:\n{missing_lines}"
    )

    return report
