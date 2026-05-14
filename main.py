"""Coordinator entry point.

Drives the MKS SERVO57D (USB-CAN) and the LinearMotorController
(RS485 / MINAS protocol) through a single coordinated scenario.
Both motors move in parallel via threads.
"""

# ruff: noqa: I001, E402
# Import order is load-bearing: the sys.path injection below must
# run before the submodule imports so their modules resolve. isort
# would reorder it after the third-party block and break the
# runtime. E402 is suppressed because the submodule imports are
# intentionally after a small non-import block (the sys.path loop).

import sys
import threading
from pathlib import Path

submodules_dir = Path(__file__).resolve().parent / "submodules"
for sub in ("MKSServo57DCANController", "LinearMotorController"):
    path = submodules_dir / sub
    if path.is_dir() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from LinearMotorController import LinearMotorController
from mks_motor import MKSMotor

# --- Hardware connection settings -----------------------------
# MKS_PORT is the FTDI device index for the USB-CAN adapter.
# Identify it with submodules/MKSServo57DCANController/
# CAN2USBAdapterDeviceRecognition.py when more than one FTDI
# device is attached.
mks_port = 0

# Serial device path for the Panasonic MINAS A6 amplifier.
linear_serial = "/dev/ttyUSB0"

# --- Motion targets -------------------------------------------
mks_target_mm = 100.0
mks_speed_pct = 25
mks_accel_pct = 10

linear_target_mm = 50.0
linear_tolerance_mm = 0.1


def run_mks(motor: MKSMotor) -> None:
    """Setup, home, and move the MKS motor to its target."""
    motor.setup()
    motor.home()
    motor.move_to(mks_target_mm, mks_speed_pct, mks_accel_pct)


def run_linear(motor: LinearMotorController) -> None:
    """Move the linear motor to its absolute target.

    The MINAS A6 reads its position at power-up; no separate
    home cycle is required for this scenario.
    """
    motor.move_to_mm(linear_target_mm, tolerance_mm=linear_tolerance_mm)


def main() -> None:
    """Run the MKS + LinearMotor co-motion scenario."""
    mks = MKSMotor.open(port=mks_port)
    linear = LinearMotorController(linear_serial)

    try:
        mks_thread = threading.Thread(target=run_mks, args=(mks,))
        linear_thread = threading.Thread(target=run_linear, args=(linear,))

        mks_thread.start()
        linear_thread.start()
        mks_thread.join()
        linear_thread.join()

        linear_final_mm = linear.read_position_mm()
        print(f"MKS  target: {mks_target_mm:.3f} mm")
        print(f"Linear final: {linear_final_mm} mm")

    finally:
        mks.close()
        linear.ser.close()


if __name__ == "__main__":
    main()
