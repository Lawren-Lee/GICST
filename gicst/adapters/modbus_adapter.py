from __future__ import annotations
from typing import List
from gicst.tc_ir import TCIR
from gicst.adapters.base import ProtocolAdapter, FlowIntent
from gicst.core.registry import AdapterRegistry


class ModbusAdapter(ProtocolAdapter):
    name = "Modbus"

    def compile_intents(self, tc: TCIR) -> List[FlowIntent]:
        intents: List[FlowIntent] = []
        acl = {"allow": [{"proto": "tcp", "port": 502, "roles": ["hmi", "plc"]}]}
        qos = {}
        mirror = {"match": {"tcp_port": 502, "fcodes": [3, 5, 6, 16]}, "to": "ids"}
        p4 = {"parse": "modbus", "counters": ["fc"], "mirror_on": [5, 6, 16]}  # write ops
        intents.append(FlowIntent(acl=acl, qos=qos, mirror=mirror, p4_profile=p4))
        return intents

AdapterRegistry.register(ModbusAdapter.name, ModbusAdapter)