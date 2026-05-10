from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyIntentInputs:
    copied_h4_bars: int
    closed_h4_time: str = "2026.05.08 13:00:00"
    long_signal_observed: bool = False
    short_signal_observed: bool = False


def h024_strategy_intent_detail_reference(inputs: StrategyIntentInputs) -> str:
    """Reference-only harness for EA log-only strategy intent decision ordering.

    This intentionally mirrors the final branch ordering and output shape of
    H024StrategyIntentDetail() without MT5, sizing, order-send, or execution code.
    """

    if inputs.copied_h4_bars < 10:
        return "NO_ACTION:strategy_unavailable_insufficient_h4_warmup"

    if inputs.long_signal_observed and inputs.short_signal_observed:
        return "BLOCKED:strategy_conflict_log_only"

    if inputs.long_signal_observed:
        return (
            "WOULD_OPEN:side=long;"
            f"closed_h4_time={inputs.closed_h4_time};"
            "source=H024_STATE_OBSERVATION;"
            "mode=log_only_no_execution"
        )

    if inputs.short_signal_observed:
        return (
            "WOULD_OPEN:side=short;"
            f"closed_h4_time={inputs.closed_h4_time};"
            "source=H024_STATE_OBSERVATION;"
            "mode=log_only_no_execution"
        )

    return (
        "NO_ACTION:strategy_no_signal;"
        f"closed_h4_time={inputs.closed_h4_time};"
        "mode=log_only_no_execution"
    )


def test_h024_strategy_intent_reference_warmup_fails_to_no_action() -> None:
    assert (
        h024_strategy_intent_detail_reference(StrategyIntentInputs(copied_h4_bars=9))
        == "NO_ACTION:strategy_unavailable_insufficient_h4_warmup"
    )


def test_h024_strategy_intent_reference_conflict_blocks_before_would_open() -> None:
    assert (
        h024_strategy_intent_detail_reference(
            StrategyIntentInputs(
                copied_h4_bars=10,
                long_signal_observed=True,
                short_signal_observed=True,
            )
        )
        == "BLOCKED:strategy_conflict_log_only"
    )


def test_h024_strategy_intent_reference_long_signal_is_log_only_would_open() -> None:
    assert (
        h024_strategy_intent_detail_reference(
            StrategyIntentInputs(copied_h4_bars=10, long_signal_observed=True)
        )
        == (
            "WOULD_OPEN:side=long;"
            "closed_h4_time=2026.05.08 13:00:00;"
            "source=H024_STATE_OBSERVATION;"
            "mode=log_only_no_execution"
        )
    )


def test_h024_strategy_intent_reference_short_signal_is_log_only_would_open() -> None:
    assert (
        h024_strategy_intent_detail_reference(
            StrategyIntentInputs(copied_h4_bars=10, short_signal_observed=True)
        )
        == (
            "WOULD_OPEN:side=short;"
            "closed_h4_time=2026.05.08 13:00:00;"
            "source=H024_STATE_OBSERVATION;"
            "mode=log_only_no_execution"
        )
    )


def test_h024_strategy_intent_reference_no_signal_is_log_only_no_action() -> None:
    assert (
        h024_strategy_intent_detail_reference(StrategyIntentInputs(copied_h4_bars=10))
        == (
            "NO_ACTION:strategy_no_signal;"
            "closed_h4_time=2026.05.08 13:00:00;"
            "mode=log_only_no_execution"
        )
    )


def test_h024_strategy_intent_reference_warmup_overrides_signal_flags() -> None:
    assert (
        h024_strategy_intent_detail_reference(
            StrategyIntentInputs(
                copied_h4_bars=9,
                long_signal_observed=True,
                short_signal_observed=True,
            )
        )
        == "NO_ACTION:strategy_unavailable_insufficient_h4_warmup"
    )
