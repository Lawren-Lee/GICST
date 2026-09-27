from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class P4Profile:
    name: str
    parse: str
    counters: list[str] = field(default_factory=list)
    mirror_on: list[Any] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "parse": self.parse, "counters": self.counters, "mirror_on": self.mirror_on}
