from __future__ import annotations
from typing import Dict, Any


def merge_telemetry(*parts: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for p in parts:
        merged.update(p)
    return merged