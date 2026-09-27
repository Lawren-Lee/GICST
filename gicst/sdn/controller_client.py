from __future__ import annotations
from typing import Any, Dict
import logging

log = logging.getLogger(__name__)

class ControllerClient:
    """Abstract client placeholder.
    - If endpoint is None -> offline mode: log the plan.
    - If endpoint is set -> best-effort POST to {endpoint}/api/v1/slices with plan["slice"].
      (Falls back to logging if requests is unavailable.)
    """
    def __init__(self, endpoint: str | None = None):
        self.endpoint = endpoint

    def apply_plan(self, plan: Dict[str, Any]) -> None:
        if not self.endpoint:
            log.info("[SDN] Offline mode. Plan not pushed.
%s", plan)
            return
        try:
            import requests  # optional dependency
        except Exception as e:
            log.warning("[SDN] requests not available (%s). Logging instead.
Endpoint=%s
Plan=%s", e, self.endpoint, plan)
            return
        try:
            url = f"{self.endpoint.rstrip('/')}/api/v1/slices"
            payload = plan.get("slice") or {}
            res = requests.post(url, json=payload, timeout=10)
            res.raise_for_status()
            log.info("[SDN] Slice applied to %s: %s", url, res.text)
        except Exception as e:
            log.error("[SDN] Failed to apply slice to %s: %s", self.endpoint, e, exc_info=True)
