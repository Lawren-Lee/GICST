from __future__ import annotations
from pathlib import Path
from pydantic import ValidationError
from gicst.tc_ir.schema import TCIR
import orjson


def load_tc_ir(path: Path) -> TCIR:
    data = orjson.loads(path.read_bytes())
    return TCIR.model_validate(data)