from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/summarize_h024_blocked_sizing_diagnostics.py")


def run_script(csv_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(csv_path)],
        check=False,
        text=True,
        capture_output=True,
    )


def test_h024_blocked_sizing_diagnostics_script_accepts_positive_blocked_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "runtime.csv"
    csv_path.write_text(
        "\n".join(
            [
                "schema_version,timestamp,symbol,check,verdict",
                "h024_ea_log_only_preflight_v2,2026-05-10,USDJPYm,preflight,PASS",
                "schema_version,timestamp,symbol,normalized_symbol,decision,reason,entry_price,stop_price,stop_distance_price,raw_lots,lots,min_volume",
                "h024_intended_action_log_v1,2026-05-10,USDJPYm,USDJPY,BLOCKED,BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short,155.821,158.163,2.342,0.0083395062,0,0.01",
                "schema_version,timestamp,symbol,check,verdict",
                "h024_ea_log_only_preflight_v2,2026-05-10,XAUUSDm,preflight,PASS",
                "schema_version,timestamp,symbol,normalized_symbol,decision,reason,entry_price,stop_price,stop_distance_price,raw_lots,lots,min_volume",
                "h024_intended_action_log_v1,2026-05-10,XAUUSDm,XAUUSD,BLOCKED,BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=long,4593.801,4525.492,68.309,0.001824723,0,0.01",
            ]
        ),
        encoding="utf-8",
    )

    result = run_script(csv_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "BLOCKED rows checked: 2" in result.stdout
    assert "Verdict: PASS" in result.stdout


def test_h024_blocked_sizing_diagnostics_script_rejects_zeroed_raw_lots(tmp_path: Path) -> None:
    csv_path = tmp_path / "runtime.csv"
    csv_path.write_text(
        "\n".join(
            [
                "schema_version,timestamp,symbol,normalized_symbol,decision,reason,entry_price,stop_price,stop_distance_price,raw_lots,lots,min_volume",
                "h024_intended_action_log_v1,2026-05-10,USDJPYm,USDJPY,BLOCKED,BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short,155.821,158.163,2.342,0,0,0.01",
            ]
        ),
        encoding="utf-8",
    )

    result = run_script(csv_path)

    assert result.returncode == 1
    assert "raw_lots not positive" in result.stdout
    assert "Verdict: FAIL" in result.stdout


def test_h024_blocked_sizing_diagnostics_script_rejects_executable_blocked_lots(tmp_path: Path) -> None:
    csv_path = tmp_path / "runtime.csv"
    csv_path.write_text(
        "\n".join(
            [
                "schema_version,timestamp,symbol,normalized_symbol,decision,reason,entry_price,stop_price,stop_distance_price,raw_lots,lots,min_volume",
                "h024_intended_action_log_v1,2026-05-10,USDJPYm,USDJPY,BLOCKED,BLOCKED:volume_below_min_for_would_open;WOULD_OPEN:side=short,155.821,158.163,2.342,0.008,0.01,0.01",
            ]
        ),
        encoding="utf-8",
    )

    result = run_script(csv_path)

    assert result.returncode == 1
    assert "final lots should be 0" in result.stdout
    assert "Verdict: FAIL" in result.stdout
