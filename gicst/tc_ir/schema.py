from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional, Dict, Any

class SLA(BaseModel):
    latency_99p_ms: Optional[int] = Field(default=None, description="p99 latency budget")
    jitter_99p_ms: Optional[int] = None
    loss_99p_ppm: Optional[int] = Field(default=None, description="packet loss in ppm")
    realtime: Optional[Literal["none", "tsn", "rtof"]] = "none"
    period_ms: Optional[int] = None

class Preconditions(BaseModel):
    protocol: Literal["OPC-UA", "IEC-104", "Modbus"]
    topology: Optional[Literal["star", "ring", "mesh"]] = None
    devices: Dict[str, str]
    initial_state: Dict[str, Any] = Field(default_factory=dict)

class Action(BaseModel):
    type: Literal["inject", "write", "read", "replay", "time_shift"]
    target: str
    command: Optional[str] = None
    value: Optional[Any] = None
    rate_per_sec: Optional[float] = None
    node: Optional[str] = None

class Observation(BaseModel):
    metric: str
    expected: str
    comparator: Literal["eq","ne","gt","lt","ge","le","regex"] = "eq"

class Oracle(BaseModel):
    rule: str
    description: Optional[str] = None

class SafetyGuards(BaseModel):
    max_write_rate: Optional[float] = None
    allowed_methods: Optional[List[str]] = None
    kill_switch_on: List[str] = Field(default_factory=list)
    rollback: Dict[str, Any] = Field(default_factory=dict)

class TCIR(BaseModel):
    id: str
    name: str
    version: str = "0.1"
    preconditions: Preconditions
    sla: Optional[SLA] = None
    actions: List[Action]
    observations: List[Observation] = Field(default_factory=list)
    oracles: List[Oracle] = Field(default_factory=list)
    safetyGuards: SafetyGuards = Field(default_factory=SafetyGuards)

    @field_validator("actions")
    @classmethod
    def _non_empty_actions(cls, v):
        if not v:
            raise ValueError("actions cannot be empty")
        return v
