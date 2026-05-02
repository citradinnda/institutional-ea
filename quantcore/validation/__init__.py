from quantcore.validation.lookahead import (
    FeatureFn,
    LookaheadReport,
    LookaheadViolation,
    assert_no_lookahead,
)
from quantcore.validation.metrics import (
    BootstrapCI,
    bootstrap_metric,
    calmar_ratio,
    max_drawdown,
    profit_factor,
    sharpe_ratio,
    sortino_ratio,
    stationary_bootstrap_indices,
    tail_ratio,
)
from quantcore.validation.purged_kfold import PurgedKFold, PurgedSplit
from quantcore.validation.cpcv import CombinatorialPurgedKFold, CPCVSplit
from quantcore.validation.walk_forward import WalkForward, WalkForwardSplit
from .deflated_sharpe import (
    DSRResult,
    MinTRLResult,
    PSRResult,
    deflated_sharpe_ratio,
    min_track_record_length,
    min_track_record_length_from_returns,
    probabilistic_sharpe_ratio,
)
from .reality_check import RealityCheckResult, whites_reality_check
from .multiple_testing import (
    MultipleTestingResult,
    benjamini_hochberg,
    bonferroni_correction,
    holm_correction,
)
# Phase 1.14 — Validator orchestrator
from quantcore.validation.validator import Validator, ValidatorReport

__all__ = [
    # lookahead
    "FeatureFn",
    "LookaheadReport",
    "LookaheadViolation",
    "assert_no_lookahead",
    # metrics
    "BootstrapCI",
    "bootstrap_metric",
    "calmar_ratio",
    "max_drawdown",
    "profit_factor",
    "sharpe_ratio",
    "sortino_ratio",
    "stationary_bootstrap_indices",
    "tail_ratio",
    # purged k-fold
    "PurgedKFold",
    "PurgedSplit",
    # cpcv
    "CombinatorialPurgedKFold",
    "CPCVSplit",
    # walk-forward
    "WalkForward",
    "WalkForwardSplit",
    # deflated sharpe
    "DSRResult",
    "PSRResult",
    "deflated_sharpe_ratio",
    "probabilistic_sharpe_ratio",
    "MinTRLResult",
    "min_track_record_length",
    "min_track_record_length_from_returns",
    # reality check
    "RealityCheckResult",
    "whites_reality_check",
    "MultipleTestingResult",
    "benjamini_hochberg",
    "bonferroni_correction",
    "holm_correction",
    # validator
    "Validator",
    "ValidatorReport"
]