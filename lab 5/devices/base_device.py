from typing import Dict

class Device:
    """Base class representing a device description for HTTP-based microservice."""
    def __init__(self, device_id: str, host: str = "127.0.0.1", port: int = 8000):
        self.device_id = device_id
        self.host = host
        self.port = port

    def get_base_url(self) -> str:
        """Return the base URL for this device."""
        return f"http://{self.host}:{self.port}"

    def __repr__(self):
        return f"<Device id={self.device_id} url={self.get_base_url()}>"

class LoggingDeviceDecorator:
    """
    Decorator that wraps a Device and logs each access.
    Does not inherit from Device to avoid property setter conflicts.
    """
    def __init__(self, device: Device):
        self._inner = device  # reference to the wrapped device

    @property
    def device_id(self):
        return self._inner.device_id

    @property
    def host(self):
        return self._inner.host

    @property
    def port(self):
        return self._inner.port

    def get_base_url(self) -> str:
        url = self._inner.get_base_url()
        print(f"[LoggingDeviceDecorator] Accessing {self.device_id} at {url}")
        return url

    def __repr__(self):
        return f"<LoggingDeviceDecorator wrap={repr(self._inner)}>"
