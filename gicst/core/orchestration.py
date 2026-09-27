from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import logging
from gicst.core.logging_config import setup_logging
from gicst.tc_ir.validate import load_tc_ir
from gicst.core.registry import AdapterRegistry
from gicst.sdn.slice_manager import intents_to_slice
from gicst.sdn.controller_client import ControllerClient
from gicst.core.utils import dump_json

log = logging.getLogger(__name__)


def compile_and_stage(tc_path: Path, out_dir: Path, controller_endpoint: str | None = None) -> Dict[str, Any]:
    setup_logging()
    tc = load_tc_ir(tc_path)
    adapter_cls = AdapterRegistry.get(tc.preconditions.protocol)
    adapter = adapter_cls()
    intents = adapter.compile_intents(tc)
    slice_spec = intents_to_slice(name=f"slice-{tc.id}", intents=intents)
    exec_plan = getattr(adapter, 'compile_exec_plan', lambda tc: [])(tc)
    plan = {
        "tc_id": tc.id,
        "slice": slice_spec.to_dict(),
        "safety": tc.safetyGuards.model_dump(),
        "sla": tc.sla.model_dump() if tc.sla else None,
        "exec": exec_plan,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    dump_json(plan, out_dir / f"plan_{tc.id}.json")
    dump_json(exec_plan, out_dir / f"exec_{tc.id}.json")
    log.info("[PLAN] Staged plan → %s", out_dir / f"plan_{tc.id}.json")

    # Apply (offline: just log)
    ControllerClient(controller_endpoint).apply_plan(plan)
    return plan