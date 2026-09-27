from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GuardDecision:
    action: str  # "allow" | "throttle" | "kill" | "rollback"
    reason: str


def evaluate_guards(metrics: Dict[str, Any], tc_safety: Dict[str, Any]) -> GuardDecision:
    """Very simple guard evaluator for now."""
    max_rate = tc_safety.get("max_write_rate")
    writes_per_sec = metrics.get("write_rate", 0)
    if max_rate is not None and writes_per_sec > max_rate:
        return GuardDecision(action="kill", reason=f"write_rate {writes_per_sec} > {max_rate}")
    # Add more rules as needed
    return GuardDecision(action="allow", reason="within limits")