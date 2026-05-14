# ToDo

## Repo bootstrap — coordinator skeleton with MKS + LinearMotor

### Background
Phase B of the lab-coordinator architecture decided in
`coport-uni/MKSServo57DCANController` issue #3 and plan file
`validated-moseying-lark.md`. This repo (`LiquidHandlerAutomation`)
is the new coordinator that orchestrates the lab's hardware
modules from a single `main.py`. Decisions captured 2026-05-14:

- Coordinator location: this new public repo
  `coport-uni/LiquidHandlerAutomation`.
- Hardware modules linked as git submodules under `vendor/`.
- ESP32S3WebMonitor: read-only HTTP polling only (firmware
  changes deferred to a future task).
- Initial `main.py` scenario: MKS motor and linear motor moving
  together in a single coordinated run.

### Work items
- [x] Scaffold governance: copy `CLAUDE.md`, `ruff.toml`,
      `LearnedPatterns.md`, `.claude/`, `.gitignore` from MKS
      repo (landed in 2d6561e)
- [x] Add submodules
      `vendor/MKSServo57DCANController` and
      `vendor/LinearMotorController`
- [x] Create `coordinator/` package: `__init__.py`,
      `paths.py` (sys.path bootstrap), `esp32_client.py`
      (read-only HTTP polling, tolerant of unreachable host)
- [x] Write `main.py` exercising MKS + LinearMotor together
      (open, home/setup, move in parallel, print final
      positions, poll ESP32 status, close); `# ruff: noqa:
      I001` documented because the path-bootstrap import must
      precede the vendor imports
- [x] Add `requirements.txt`: `ftd2xx`, `pyserial`, `requests`
- [x] Run `ruff check` and `ruff format --check` on
      `coordinator/` and `main.py` — all clean
- [x] Verified path bootstrap with
      `python3 -c 'import coordinator.paths'`: both vendor
      directories injected into sys.path. Actual hardware
      module imports fail only because `pyserial`/`ftd2xx` are
      not installed in this container, which `pip install -r
      requirements.txt` resolves.
- [x] GitHub issue register (#1)
- [ ] Commit and push
- [ ] GitHub issue update (close)
