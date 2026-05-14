# Liquid Handler Automation

Coordinator that drives a lab liquid-handling rig from a single `main.py`. Wraps four hardware modules as git submodules under `vendor/`, plus a read-only HTTP client for the ESP32S3 status board.

## Modules

| Module | Role | Channel | Source |
|---|---|---|---|
| MKSMotor | Z / vertical stepper | USB → CAN (FTDI FT245) | [`vendor/MKSServo57DCANController`](https://github.com/coport-uni/MKSServo57DCANController) |
| LinearMotorController | Linear stage (Panasonic MINAS A6) | RS485 / MINAS protocol | [`vendor/LinearMotorController`](https://github.com/coport-uni/LinearMotorController) |
| SyringePumpController | Liquid dispensing (planned) | TBD | not yet created |
| ESP32S3WebMonitor (read-only) | Rig status / telemetry | HTTP polling | [`coport-uni/ESP32S3WebMonitor`](https://github.com/coport-uni/ESP32S3WebMonitor) |

## Layout

```
LiquidHandlerAutomation/
├── main.py                       # entry point
├── coordinator/
│   ├── __init__.py
│   ├── paths.py                  # adds vendor/ subdirs to sys.path
│   └── esp32_client.py           # read-only HTTP polling
├── vendor/                       # git submodules
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

- `MKS_PORT` — FTDI device index for the USB-CAN adapter (use `vendor/MKSServo57DCANController/CAN2USBAdapterDeviceRecognition.py` to identify).
- `LINEAR_SERIAL` — serial device path for the MINAS A6 (e.g., `/dev/ttyUSB0`).
- `ESP32_BASE_URL` — base URL for the ESP32 status endpoint (placeholder until the actual host:port is finalized).
- Motion targets, speeds, accelerations.

## Conventions

This repo follows the CommonClaude conventions in [CLAUDE.md](CLAUDE.md). Hardware library submodules are upstream-of-record and must not be edited from this repo; changes belong in their own repos and land here via `git submodule update`.
