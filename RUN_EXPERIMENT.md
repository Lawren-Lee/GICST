
# Run an end-to-end experiment with GICST

## 1) Compile a plan (already supported)
```bash
source .venv/bin/activate
python gicst/cli.py compile gicst/gicst/examples/sample_tc_ir_iec104.json --out out/
# -> out/plan_iec104-001.json + out/exec_iec104-001.json
```

## 2) Execute the actions (replace template's `command_template` with your real IEC-104 client)
- Edit `gicst/tools/templates/iec104.json`:
  - `command_template`: the shell command to send an IEC-104 action, e.g. a wrapper around your client tool.
    Available placeholders: `{endpoint}`, `{func}`, `{func_mapped}`, `{addr}`, `{addr_mapped}`, `{value}`, `{rate}`
  - `address_map`: map business names like `breaker1` -> protocol info-object address
  - `func_map`: map abstract function -> your tool's argument name

### Example dry-run (uses `echo` so it works anywhere)
```bash
python gicst/tools/runner.py       --exec out/exec_iec104-001.json       --template gicst/tools/templates/iec104.json       --out out/results_iec104-001.jsonl       --rate-limit 2       --timeout 5
```

The runner writes JSON lines to `out/results_*.jsonl` including return code, latency, stdout/stderr.

## 3) Getting real results
- Replace the `echo ...` in the template with your actual IEC-104 client invocation.
  For example, if you have a CLI `iec104_client` that can send C_SC_NA_1:
  ```json
  { "command_template": "iec104_client --host {endpoint} --func {func_mapped} --addr {addr_mapped} --value {value}" }
  ```
- Keep `address_map` and `func_map` in the template to bridge naming differences.

## 4) (Optional) Push slice to controller
If you have a controller endpoint:
```bash
python gicst/cli.py compile gicst/gicst/examples/sample_tc_ir_iec104.json --out out/ --controller http://controller:8181
```
