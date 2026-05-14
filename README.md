# Liquid Handler Automation

Single-file coordinator (`main.py`) that drives two motors of a lab liquid-handling rig in parallel. The MKS SERVO57D (Z / vertical stepper, USB→CAN) and the Panasonic MINAS A6 linear stage (RS485) move concurrently on their own threads, then the run prints their final positions and closes the channels.

Hardware drivers live as upstream-of-record git submodules under [`submodules/`](submodules/) and are loaded by an inlined `sys.path` bootstrap at the top of `main.py` — there is no separate `coordinator/` package.

## Modules

| Module | Role | Channel | Source |
|---|---|---|---|
| MKSMotor | Z / vertical stepper | USB → CAN (FTDI FT245) | [`submodules/MKSServo57DCANController`](https://github.com/coport-uni/MKSServo57DCANController) |
| LinearMotorController | Linear stage (Panasonic MINAS A6) | RS485 / MINAS protocol | [`submodules/LinearMotorController`](https://github.com/coport-uni/LinearMotorController) |

**Planned (not yet wired into `main.py`)**: SyringePumpController — liquid dispensing, channel TBD, repo not yet created.

## How it runs

`python main.py` executes the following sequence:

1. **Open hardware**: `MKSMotor.open(port=mks_port)` and `LinearMotorController(linear_serial)`.
2. **Start two threads in parallel** (`threading.Thread`):
   - MKS thread: `setup()` → `home()` → `move_to(mks_target_mm, mks_speed_pct, mks_accel_pct)`.
   - Linear thread: `move_to_mm(linear_target_mm, tolerance_mm=linear_tolerance_mm)` — the MINAS A6 reads its position at power-up, so no separate home is performed.
3. **Join both threads**, then read the linear stage's final position and print:
   ```
   MKS  target: <mks_target_mm> mm
   Linear final: <linear_final_mm> mm
   ```
4. **Always close** both channels in a `finally` block, even on exception.

## Layout

```
LiquidHandlerAutomation/
├── main.py                       # entry point (inlines submodules sys.path bootstrap)
├── submodules/                   # git submodules
│   ├── MKSServo57DCANController/
│   └── LinearMotorController/
├── requirements.txt
├── CLAUDE.md                     # CommonClaude conventions
├── LearnedPatterns.md
├── ToDo.md
├── ruff.toml
└── .claude/                      # hooks + settings.json
```

## Quick start

```bash
git clone --recurse-submodules https://github.com/coport-uni/LiquidHandlerAutomation
cd LiquidHandlerAutomation
pip install -r requirements.txt
python main.py
```

If the repo was already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Configuration

Edit the constants at the top of `main.py`:

- `mks_port` — FTDI device index for the USB-CAN adapter (use `submodules/MKSServo57DCANController/CAN2USBAdapterDeviceRecognition.py` to identify it when multiple FTDI devices are attached).
- `linear_serial` — serial device path for the MINAS A6 (e.g., `/dev/ttyUSB0`).
- `mks_target_mm`, `mks_speed_pct`, `mks_accel_pct` — MKS motion target and motion-profile knobs.
- `linear_target_mm`, `linear_tolerance_mm` — linear stage absolute target and the convergence band used by `move_to_mm`.

## Conventions

This repo follows the CommonClaude conventions in [CLAUDE.md](CLAUDE.md). Hardware library submodules are upstream-of-record and must not be edited from this repo; changes belong in their own repos and land here via `git submodule update`.
