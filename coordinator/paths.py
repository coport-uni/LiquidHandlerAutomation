"""Add vendored hardware repos to sys.path.

Each repo under ``vendor/`` publishes its modules at the repo
root (not inside a package). The coordinator owns the path
injection so upstream repos can stay unmodified and reusable
on their own.

Import this module exactly once, before importing any vendored
module:

    import coordinator.paths  # noqa: F401
    from mks_motor import MKSMotor
"""

import sys
from pathlib import Path

vendor_dir = Path(__file__).resolve().parent.parent / "vendor"

vendor_subdirs = (
    "MKSServo57DCANController",
    "LinearMotorController",
    # "SyringePumpController" will be added when the library lands.
)

for sub in vendor_subdirs:
    path = vendor_dir / sub
    if path.is_dir() and str(path) not in sys.path:
        sys.path.insert(0, str(path))
