"""Read-only HTTP client for the ESP32S3 status board.

The device firmware in ``coport-uni/ESP32S3WebMonitor`` is
strictly device-to-host: the ESP32 pulls data from a small HTTP
server on the host. The coordinator never commands the device,
only observes status it has exposed. If a real command surface
is needed later, the firmware must add the endpoints first.

The client is intentionally tolerant of an unreachable endpoint:
the rig must run even if the status board is offline.
"""

from typing import Any

import requests

_default_timeout_s = 2.0


class Esp32Client:
    """Polls a status URL on the ESP32 firmware or its companion
    host-side HTTP server.

    Args:
        base_url: Scheme-qualified base URL such as
            ``http://192.168.1.42`` or
            ``http://localhost:8080``. No trailing slash.
        timeout_s: Request timeout per call.
    """

    def __init__(
        self,
        base_url: str,
        timeout_s: float = _default_timeout_s,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    def get_status(self, path: str = "/status") -> dict[str, Any] | None:
        """Fetch the device status as a JSON object.

        Returns the decoded JSON on success, or ``None`` if the
        endpoint is unreachable or returns a non-2xx response.
        The caller decides how to react; the coordinator should
        not crash when the status board is offline.
        """
        url = f"{self.base_url}{path}"
        try:
            response = requests.get(url, timeout=self.timeout_s)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
