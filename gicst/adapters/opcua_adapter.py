from __future__ import annotations
from typing import List
from gicst.tc_ir import TCIR
from gicst.adapters.base import ProtocolAdapter, FlowIntent
from gicst.core.registry import AdapterRegistry


class OPCUAAdapter(ProtocolAdapter):
    name = "OPC-UA"

    def compile_intents(self, tc: TCIR) -> List[FlowIntent]:
        intents: List[FlowIntent] = []
        # TCP (4840) between HMI and PLC nodes
        acl = {"allow": [{"proto": "tcp", "port": 4840, "roles": ["hmi", "plc"]}]}
        qos = {}
        if tc.sla and tc.sla.latency_99p_ms:
            qos["latency_99p_ms"] = tc.sla.latency_99p_ms
        mirror = {"match": {"tcp_port": 4840}, "to": "ids"}
        p4 = {"parse": "opcua", "counters": ["method_call", "write"]}
        intents.append(FlowIntent(acl=acl, qos=qos, mirror=mirror, p4_profile=p4))
        return intents

# Auto-register
AdapterRegistry.register(OPCUAAdapter.name, OPCUAAdapter)