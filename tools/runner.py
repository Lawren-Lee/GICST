
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, time, subprocess, shlex, sys, pathlib, datetime, re
from typing import Any, Dict, List

def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))

def now():
    return datetime.datetime.now().isoformat(timespec="milliseconds")

def format_cmd(tmpl: str, step: dict, mapping: dict) -> str:
    # allow mapping-based address/function translation
    addr_map = mapping.get("address_map", {})
    func_map = mapping.get("func_map", {})
    safe = dict(step)
    if step.get("addr") in addr_map:
        safe["addr_mapped"] = addr_map[step["addr"]]
    else:
        safe["addr_mapped"] = step.get("addr")
    if step.get("func") in func_map:
        safe["func_mapped"] = func_map[step["func"]]
    else:
        safe["func_mapped"] = step.get("func")
    # Fill template
    return tmpl.format(**safe)

def run_step(cmd: str, timeout: float|None):
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(shlex.split(cmd), capture_output=True, timeout=timeout, text=True)
        dt = (time.perf_counter() - t0)*1000.0
        return {"rc": proc.returncode, "latency_ms": round(dt,2), "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-4000:]}
    except Exception as e:
        dt = (time.perf_counter() - t0)*1000.0
        return {"rc": -1, "latency_ms": round(dt,2), "error": str(e)}

def main():
    ap = argparse.ArgumentParser(description="GICST Exec Runner")
    ap.add_argument("--exec", dest="exec_path", required=True, help="exec_<tcid>.json path")
    ap.add_argument("--template", required=True, help="command template json (protocol-specific)")
    ap.add_argument("--out", required=True, help="results jsonl output path")
    ap.add_argument("--rate-limit", type=float, default=0.0, help="max steps per second (0=unlimited)")
    ap.add_argument("--timeout", type=float, default=5.0, help="per-step timeout (seconds)")
    args = ap.parse_args()

    exec_steps = load_json(pathlib.Path(args.exec_path))
    tmpl_cfg = load_json(pathlib.Path(args.template))
    tmpl = tmpl_cfg.get("command_template")
    if not tmpl:
        print("Template missing 'command_template'", file=sys.stderr); sys.exit(2)

    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", encoding="utf-8") as fout:
        last_ts = 0.0
        for i, step in enumerate(exec_steps, 1):
            if args.rate_limit and last_ts>0:
                sleep_needed = max(0.0, (1.0/args.rate_limit) - (time.perf_counter() - last_ts))
                if sleep_needed>0: time.sleep(sleep_needed)
            cmd = format_cmd(tmpl, step, tmpl_cfg)
            start = now()
            res = run_step(cmd, args.timeout)
            rec = {"ts": start, "i": i, "cmd": cmd, "step": step, **res}
            fout.write(json.dumps(rec, ensure_ascii=False)+"\n")
            fout.flush()
            print(f"[{i}] rc={res.get('rc')} latency={res.get('latency_ms')} ms")
            last_ts = time.perf_counter()

if __name__ == "__main__":
    main()
