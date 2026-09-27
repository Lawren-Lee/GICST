from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List
from gicst.adapters.base import FlowIntent
from gicst.sdn.p4_profile import P4Profile


@dataclass
class SliceSpec:
    name: str
    acl: List[Dict[str, Any]] = field(default_factory=list)
    qos: Dict[str, Any] = field(default_factory=dict)
    mirror: List[Dict[str, Any]] = field(default_factory=list)
    p4_profiles: List[P4Profile] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "acl": self.acl,
            "qos": self.qos,
            "mirror": self.mirror,
            "p4_profiles": [p.to_dict() for p in self.p4_profiles],
        }


def intents_to_slice(name: str, intents: List[FlowIntent]) -> SliceSpec:
    spec = SliceSpec(name=name)
    for it in intents:
        if it.acl:
            spec.acl.extend(it.acl.get("allow", []))
        if it.qos:
            spec.qos.update(it.qos)
        if it.mirror:
            spec.mirror.append(it.mirror)
        if it.p4_profile:
            spec.p4_profiles.append(P4Profile(name=f"p4-{len(spec.p4_profiles)+1}", **it.p4_profile))
    return spec
