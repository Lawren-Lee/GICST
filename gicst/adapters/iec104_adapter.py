from __future__ import annotations
from typing import List
from gicst.tc_ir import TCIR
from gicst.adapters.base import ProtocolAdapter, FlowIntent
from gicst.core.registry import AdapterRegistry


class IEC104Adapter(ProtocolAdapter):
    name = "IEC-104"

    def compile_intents(self, tc: TCIR) -> List[FlowIntent]:
        intents: List[FlowIntent] = []
        # IEC-104 uses TCP/2404
        acl = {"allow": [{"proto": "tcp", "port": 2404, "roles": ["master", "outstation"]}]}
        qos = {}
        if tc.sla and tc.sla.realtime in {"rtof", "tsn"}:
            qos["realtime"] = tc.sla.realtime
            if tc.sla.period_ms:
                qos["period_ms"] = tc.sla.period_ms
        mirror = {"match": {"tcp_port": 2404, "asdu_types": ["C_SC_NA_1", "C_DC_NA_1"]}, "to": "ids"}
        p4 = {"parse": "iec104", "counters": ["asdu", "cause"], "mirror_on": ["select", "command"]}
        intents.append(FlowIntent(acl=acl, qos=qos, mirror=mirror, p4_profile=p4))
        return intents

AdapterRegistry.register(IEC104Adapter.name, IEC104Adapter)


    def compile_exec_plan(self, tc: TCIR) -> list[dict]:
        """Translate high-level actions into an *execution plan*.
        This keeps protocol details abstract; concrete command mapping is supplied by runner templates.
        Returns a list of steps with fields:
          - endpoint (ip/host)
          - op (read/write/inject)
          - func (e.g., C_SC_NA_1)
          - addr (business var; map to info address externally)
          - value (optional)
          - rate (optional)
        """
        endpoint = tc.preconditions.devices.get("outstation") or tc.preconditions.devices.get("server")
        steps: list[dict] = []
        for a in tc.actions:
            step = {"endpoint": endpoint, "op": a.type, "addr": a.target, "rate": a.rate_per_sec}
            if a.type == "inject" and a.command == "trip":
                step.update({"func": "C_SC_NA_1", "value": 1})
            elif a.type == "write":
                step.update({"func": "C_SE_NA_1", "value": a.value})
            elif a.type == "read":
                step.update({"func": "M_ME_NA_1"})
            else:
                step.update({"func": a.command or ""})
            steps.append(step)
        return steps
