from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from scripts.verify_h024_ea_preflight_log import (
    ALLOWED_SYMBOLS,
    EXPECTED_EA_VERSION,
    EXPECTED_SCHEMA_VERSION,
    verify_h024_ea_preflight_log,
)
from scripts.verify_h024_ea_source_static import verify_source


REPO_EA_SOURCE = Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5")
EA_FILENAME = "H024_LogOnly_Preflight.mq5"
RUNTIME_LOG_FILENAME = "h024_ea_log_only_preflight.csv"
DEFAULT_REPORT_PATH = Path("reports") / RUNTIME_LOG_FILENAME
EXPECTED_EA_SOURCE_TOKENS = (
    f'InpSchemaVersion = "{EXPECTED_SCHEMA_VERSION}"',
    f'InpEaVersion = "{EXPECTED_EA_VERSION}"',
    'InpKillSwitchBlocked = true',
    'InpRuntimeMode = "log_only_preflight"',
)


@dataclass(frozen=True)
class CompileOutcome:
    return_code: int
    stdout: str
    stderr: str
    ex5_path: Path
    ex5_refreshed: bool

    @property
    def accepted(self) -> bool:
        return self.return_code == 0 or self.ex5_refreshed


@dataclass(frozen=True)
class LocalPreflightPaths:
    terminal_data_dir: Path
    repo_ea_source: Path = REPO_EA_SOURCE
    report_path: Path = DEFAULT_REPORT_PATH

    @property
    def terminal_experts_dir(self) -> Path:
        return self.terminal_data_dir / "MQL5" / "Experts"

    @property
    def terminal_files_dir(self) -> Path:
        return self.terminal_data_dir / "MQL5" / "Files"

    @property
    def terminal_ea_source(self) -> Path:
        return self.terminal_experts_dir / EA_FILENAME

    @property
    def terminal_ea_binary(self) -> Path:
        return self.terminal_experts_dir / EA_FILENAME.replace(".mq5", ".ex5")

    @property
    def terminal_runtime_log(self) -> Path:
        return self.terminal_files_dir / RUNTIME_LOG_FILENAME


def copy_ea_source(paths: LocalPreflightPaths) -> Path:
    if not paths.repo_ea_source.exists():
        raise FileNotFoundError(f"missing repo EA source: {paths.repo_ea_source}")

    paths.terminal_experts_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(paths.repo_ea_source, paths.terminal_ea_source)
    return paths.terminal_ea_source


def reset_runtime_log(paths: LocalPreflightPaths) -> bool:
    if not paths.terminal_runtime_log.exists():
        return False

    paths.terminal_runtime_log.unlink()
    return True


def _mtime(path: Path) -> float | None:
    if not path.exists():
        return None
    return path.stat().st_mtime


def compile_ea(metaeditor: Path, source_path: Path, *, timeout_seconds: int = 60) -> CompileOutcome:
    if not metaeditor.exists():
        raise FileNotFoundError(f"missing MetaEditor executable: {metaeditor}")

    if not source_path.exists():
        raise FileNotFoundError(f"missing EA source to compile: {source_path}")

    ex5_path = source_path.with_suffix(".ex5")
    before_mtime = _mtime(ex5_path)
    started_at = datetime.now().timestamp()

    completed = subprocess.run(
        [str(metaeditor), f"/compile:{source_path}"],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )

    after_mtime = _mtime(ex5_path)
    ex5_refreshed = after_mtime is not None and (
        before_mtime is None
        or after_mtime > before_mtime
        or after_mtime >= started_at
    )

    return CompileOutcome(
        return_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        ex5_path=ex5_path,
        ex5_refreshed=ex5_refreshed,
    )


def collect_runtime_log(paths: LocalPreflightPaths) -> Path:
    if not paths.terminal_runtime_log.exists():
        raise FileNotFoundError(f"missing terminal runtime log: {paths.terminal_runtime_log}")

    paths.report_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(paths.terminal_runtime_log, paths.report_path)
    return paths.report_path


def run_verify(report_path: Path) -> tuple[int, list[str]]:
    result = verify_h024_ea_preflight_log(report_path)
    return result.rows, result.violations


def validate_automation_target(paths: LocalPreflightPaths, metaeditor: Path | None = None) -> list[str]:
    """Validate the local MT5 target before any future profile/template automation.

    This is intentionally read-only. It does not attach EAs, launch GUI automation,
    place orders, modify orders, close orders, or call MT5 trade APIs.
    """

    violations: list[str] = []

    if not paths.terminal_data_dir.exists():
        violations.append(f"terminal data dir does not exist: {paths.terminal_data_dir}")

    if not paths.terminal_experts_dir.exists():
        violations.append(f"terminal Experts dir does not exist: {paths.terminal_experts_dir}")

    if not paths.terminal_files_dir.exists():
        violations.append(f"terminal Files dir does not exist: {paths.terminal_files_dir}")

    if metaeditor is not None and not metaeditor.exists():
        violations.append(f"MetaEditor executable does not exist: {metaeditor}")

    if not paths.repo_ea_source.exists():
        violations.append(f"repo EA source does not exist: {paths.repo_ea_source}")
        return violations

    violations.extend(verify_source(paths.repo_ea_source))

    source = paths.repo_ea_source.read_text(encoding="ascii")
    for token in EXPECTED_EA_SOURCE_TOKENS:
        if token not in source:
            violations.append(f"repo EA source missing expected token: {token}")

    for symbol in sorted(ALLOWED_SYMBOLS):
        if symbol not in {"USDJPYm", "XAUUSDm"}:
            violations.append(f"unexpected verifier symbol configured: {symbol}")

    return violations


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Local helper for H024 MT5 log-only EA preflight. "
            "Copies source, optionally compiles, optionally resets/collects runtime CSV, and verifies it. "
            "Does not attach EAs, place orders, modify orders, close orders, or call MT5 trade APIs."
        )
    )
    parser.add_argument(
        "--terminal-data-dir",
        type=Path,
        required=True,
        help="MT5 terminal data directory containing MQL5/Experts and MQL5/Files.",
    )
    parser.add_argument(
        "--metaeditor",
        type=Path,
        help="Optional path to MetaEditor64.exe. If provided, the copied EA source is compiled.",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Destination path for collected runtime CSV.",
    )
    parser.add_argument(
        "--reset-runtime-log",
        action="store_true",
        help="Delete the terminal runtime CSV before manual EA attachment.",
    )
    parser.add_argument(
        "--collect",
        action="store_true",
        help="Copy terminal MQL5/Files runtime CSV to the repo report path and verify it.",
    )
    parser.add_argument(
        "--compile-timeout-seconds",
        type=int,
        default=60,
        help="MetaEditor compile timeout in seconds.",
    )
    parser.add_argument(
        "--automation-target-preflight",
        action="store_true",
        help=(
            "Read-only safety preflight for future MT5 profile/template automation. "
            "Validates paths, source invariants, expected schema/version, and symbols. "
            "Does not attach/detach EAs or automate the MT5 GUI."
        ),
    )
    parser.add_argument(
        "--attach-detach",
        action="store_true",
        help="Reserved. Always rejected; attach/detach automation is not approved.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    paths = LocalPreflightPaths(
        terminal_data_dir=args.terminal_data_dir,
        report_path=args.report_path,
    )

    print("H024 MT5 log-only EA local preflight helper")
    print("=" * 72)
    print("Research only. No demo/live/Phase 4 approval.")
    print("No EA attachment automation. No order-send capability.")
    print()

    if args.attach_detach:
        print("Attach/detach automation is not approved for this helper.")
        return 2

    if args.automation_target_preflight:
        violations = validate_automation_target(paths, args.metaeditor)
        print("Automation target preflight:")
        print(f"- terminal_data_dir: {paths.terminal_data_dir}")
        print(f"- terminal_experts_dir: {paths.terminal_experts_dir}")
        print(f"- terminal_files_dir: {paths.terminal_files_dir}")
        print(f"- repo_ea_source: {paths.repo_ea_source}")
        print(f"- expected_schema_version: {EXPECTED_SCHEMA_VERSION}")
        print(f"- expected_ea_version: {EXPECTED_EA_VERSION}")
        print(f"- expected_symbols: {', '.join(sorted(ALLOWED_SYMBOLS))}")
        print(f"Violations: {len(violations)}")
        for violation in violations:
            print(f"- {violation}")
        print()
        print("Verdict: PASS" if not violations else "Verdict: FAIL")
        if violations:
            return 1
        print()

    copied_to = copy_ea_source(paths)
    print(f"Copied EA source to: {copied_to}")

    if args.reset_runtime_log:
        removed = reset_runtime_log(paths)
        print(f"Runtime CSV reset: {'removed existing file' if removed else 'no existing file'}")

    if args.metaeditor is not None:
        compile_outcome = compile_ea(
            args.metaeditor,
            copied_to,
            timeout_seconds=args.compile_timeout_seconds,
        )
        print(f"MetaEditor compile return code: {compile_outcome.return_code}")
        print(f"EX5 path: {compile_outcome.ex5_path}")
        print(f"EX5 refreshed: {compile_outcome.ex5_refreshed}")
        if compile_outcome.stdout.strip():
            print("MetaEditor stdout:")
            print(compile_outcome.stdout.strip())
        if compile_outcome.stderr.strip():
            print("MetaEditor stderr:")
            print(compile_outcome.stderr.strip())
        if not compile_outcome.accepted:
            return compile_outcome.return_code if compile_outcome.return_code != 0 else 1
        if compile_outcome.return_code != 0:
            print("Compile accepted because EX5 was refreshed despite nonzero MetaEditor return code.")

    if not args.collect:
        print()
        print("Skipped runtime CSV collection. Attach/remove the EA manually, then rerun with --collect.")
        return 0

    report_path = collect_runtime_log(paths)
    rows, violations = run_verify(report_path)

    print(f"Collected runtime CSV to: {report_path}")
    print(f"Rows: {rows}")
    print(f"Violations: {len(violations)}")
    for violation in violations:
        print(f"- {violation}")

    print()
    print("Verdict: PASS" if not violations else "Verdict: FAIL")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
