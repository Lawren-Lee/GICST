from __future__ import annotations
from typing import Dict, Type
from gicst.adapters.base import ProtocolAdapter


class AdapterRegistry:
    """Runtime registry for protocol adapters."""

    _REG: Dict[str, Type[ProtocolAdapter]] = {}

    @classmethod
    def register(cls, name: str, adapter: Type[ProtocolAdapter]):
        key = name.lower()
        if key in cls._REG:
            raise ValueError(f"adapter already registered: {name}")
        cls._REG[key] = adapter

    @classmethod
    def get(cls, name: str) -> Type[ProtocolAdapter]:
        try:
            return cls._REG[name.lower()]
        except KeyError:
            raise KeyError(f"No adapter for protocol '{name}'. Registered: {list(cls._REG)}")
