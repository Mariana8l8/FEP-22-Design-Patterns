from typing import Dict, List, Any, Optional
import requests
from requests.exceptions import RequestException

class IOTFacade:
    """Handles HTTP requests to device microservices"""

    def __init__(self, timeout: float = 1.0):
        # device_id -> device (any object with device_id, host, port)
        self._devices = {}
        self.timeout = timeout

    def register_device(self, device) -> str:
        device_id = getattr(device, "device_id", None)
        if not device_id:
            raise ValueError("Device must have device_id")
        self._devices[device_id] = device
        return device_id

    def _base_url(self, device_id: str) -> Optional[str]:
        device = self._devices.get(device_id)
        if not device:
            return None
        host = getattr(device, "host", "127.0.0.1")
        port = getattr(device, "port", 8000)
        return f"http://{host}:{port}"

    def get_device_status(self, device_id: str) -> Dict[str, Any]:
        base = self._base_url(device_id)
        if not base:
            return {}
        url = f"{base}/status"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except RequestException:
            return {"device_id": device_id, "error": "unreachable"}

    def perform_device_action(self, device_id: str, action: str, **kwargs) -> bool:
        base = self._base_url(device_id)
        if not base:
            return False

        try:
            if action == "power":
                state = kwargs.get("state")
                if state is None:
                    return False
                url = f"{base}/power/{state}"
                r = requests.post(url, timeout=self.timeout)
                r.raise_for_status()
                return True

            if action == "set_volume":
                value = kwargs.get("value")
                if value is None:
                    return False
                url = f"{base}/volume/{int(value)}"
                r = requests.post(url, timeout=self.timeout)
                r.raise_for_status()
                return True

            if action == "set_brightness":
                value = kwargs.get("value")
                if value is None:
                    return False
                url = f"{base}/brightness/{int(value)}"
                r = requests.post(url, timeout=self.timeout)
                r.raise_for_status()
                return True

            if action == "position":
                value = kwargs.get("value")
                if value is None:
                    return False
                url = f"{base}/position/{int(value)}"
                r = requests.post(url, timeout=self.timeout)
                r.raise_for_status()
                return True

            # generic fallback: try POST to /{action}
            url = f"{base}/{action}"
            r = requests.post(url, json=kwargs, timeout=self.timeout)
            r.raise_for_status()
            return True
        except RequestException:
            return False

    def get_all_status(self) -> List[Dict[str, Any]]:
        statuses = []
        for device_id in self._devices:
            statuses.append(self.get_device_status(device_id))
        return statuses
