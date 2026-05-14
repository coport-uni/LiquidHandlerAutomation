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
- [x] Commit and push (2f5b98b)
- [x] GitHub issue update (#1 closed)

## Submodule sync — pull latest LinearMotor and MKSServo

### Background
User requested removing all submodules except
`LinearMotorController` and `MKSServo57DCANController`, then
updating remaining ones to latest. Inspection showed the repo
already has exactly those two submodules, so the removal step
is a no-op and only the update remains.

### Work items
- [x] Validate current submodule list (only the two target
      modules present; nothing to remove)
- [x] `git submodule update --remote --recursive` to fast-
      forward each submodule to its tracked branch tip
      (no-op: already at upstream tip)
- [x] Inspect `git status` for new submodule pointer commits
      and record old vs. new SHAs
      (LinearMotorController stays at 6d4e9223;
      MKSServo57DCANController stays at 2d1f1683)
- [x] Sanity check: `git -C vendor/<each> log -1` confirms the
      checked-out commit matches the upstream branch tip
- [x] GitHub issue register (#2)
- [ ] Commit submodule pointer bumps and push
- [ ] GitHub issue update (close on success)
