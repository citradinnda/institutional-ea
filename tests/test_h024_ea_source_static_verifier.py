from __future__ import annotations

from pathlib import Path

from scripts.verify_h024_ea_source_static import verify_source


def test_current_h024_log_only_ea_source_passes_static_verifier() -> None:
    violations = verify_source(Path("ea_mt5/Experts/H024_LogOnly_Preflight.mq5"))

    assert violations == []


def test_static_verifier_rejects_order_send(tmp_path: Path) -> None:
    source = tmp_path / "bad.mq5"
    source.write_text(
        """
        int OnInit() { return INIT_SUCCEEDED; }
        void OnTick() { OrderSend(request, result); }
        void OnDeinit(const int reason) {}
        input bool InpKillSwitchBlocked = true;
        string file_name = "h024_ea_log_only_preflight.csv";
        """,
        encoding="utf-8",
    )

    violations = verify_source(source)

    assert any("OrderSend" in violation for violation in violations)


def test_static_verifier_rejects_trade_include(tmp_path: Path) -> None:
    source = tmp_path / "bad_include.mq5"
    source.write_text(
        """
        #include <Trade/Trade.mqh>
        int OnInit() { return INIT_SUCCEEDED; }
        void OnTick() {}
        void OnDeinit(const int reason) {}
        input bool InpKillSwitchBlocked = true;
        string file_name = "h024_ea_log_only_preflight.csv";
        """,
        encoding="utf-8",
    )

    violations = verify_source(source)

    assert any("Trade include" in violation for violation in violations)


def test_static_verifier_ignores_comments(tmp_path: Path) -> None:
    source = tmp_path / "comment_only.mq5"
    source.write_text(
        """
        // OrderSend must remain forbidden.
        /*
           CTrade must remain forbidden.
        */
        input bool InpKillSwitchBlocked = true;
        string file_name = "h024_ea_log_only_preflight.csv";
        int OnInit() { return INIT_SUCCEEDED; }
        void OnTick() {}
        void OnDeinit(const int reason) {}
        """,
        encoding="utf-8",
    )

    violations = verify_source(source)

    assert violations == []


def test_static_verifier_requires_log_file_name(tmp_path: Path) -> None:
    source = tmp_path / "missing_log_file.mq5"
    source.write_text(
        """
        input bool InpKillSwitchBlocked = true;
        int OnInit() { return INIT_SUCCEEDED; }
        void OnTick() {}
        void OnDeinit(const int reason) {}
        """,
        encoding="utf-8",
    )

    violations = verify_source(source)

    assert any("log file name" in violation for violation in violations)
