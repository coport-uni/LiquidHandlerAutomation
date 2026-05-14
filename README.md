# Liquid Handler Automation

Coordinator that drives a lab liquid-handling rig from a single `main.py`. Wraps the hardware modules as git submodules under `submodules/`.

## Modules

| Module | Role | Channel | Source |
|---|---|---|---|
| MKSMotor | Z / vertical stepper | USB → CAN (FTDI FT245) | [`submodules/MKSServo57DCANController`](https://github.com/coport-uni/MKSServo57DCANController) |
| LinearMotorController | Linear stage (Panasonic MINAS A6) | RS485 / MINAS protocol | [`submodules/LinearMotorController`](https://github.com/coport-uni/LinearMotorController) |
| SyringePumpController | Liquid dispensing (planned) | TBD | not yet created |

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

- `MKS_PORT` — FTDI device index for the USB-CAN adapter (use `submodules/MKSServo57DCANController/CAN2USBAdapterDeviceRecognition.py` to identify).
- `LINEAR_SERIAL` — serial device path for the MINAS A6 (e.g., `/dev/ttyUSB0`).
- Motion targets, speeds, accelerations.

## Conventions

This repo follows the CommonClaude conventions in [CLAUDE.md](CLAUDE.md). Hardware library submodules are upstream-of-record and must not be edited from this repo; changes belong in their own repos and land here via `git submodule update`.
