from __future__ import annotations
import logging
from rich.logging import RichHandler

_DEF_FMT = "%(message)s"

def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format=_DEF_FMT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)],
    )