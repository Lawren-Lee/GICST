from __future__ import annotations
from pathlib import Path
import typer
from gicst.core.orchestration import compile_and_stage

app = typer.Typer(help="GICST pre-scenario compiler")


@app.command()
def compile(
    tc: Path = typer.Argument(..., help="Path to TC-IR JSON"),
    out: Path = typer.Option(Path("./out"), help="Output directory for plans"),
    controller: str | None = typer.Option(None, help="Controller endpoint or offline")
):
    compile_and_stage(tc, out, controller_endpoint=controller)


if __name__ == "__main__":
    app()
