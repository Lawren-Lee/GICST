from __future__ import annotations
from typing import Dict, Any, List, Protocol
from dataclasses import dataclass, field
from gicst.tc_ir import TCIR


@dataclass
class FlowIntent:
    """Abstract network intent derived from TC-IR and protocol specifics."""
    acl: Dict[str, Any] = field(default_factory=dict)
    qos: Dict[str, Any] = field(default_factory=dict)
    mirror: Dict[str, Any] = field(default_factory=dict)
    p4_profile: Dict[str, Any] = field(default_factory=dict)


class ProtocolAdapter(Protocol):
    name: str

    def compile_intents(self, tc: TCIR) -> List[FlowIntent]:
        ...