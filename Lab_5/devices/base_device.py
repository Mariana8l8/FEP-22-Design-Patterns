from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import requests


class DeviceInfo(BaseModel):
    device_id: str
    device_type: str
    host: str
    port: int
    capabilities: list[str]


@dataclass
class BaseDevice(ABC):
    device_id: str
    device_type: str
    host: str
    port: int

    def __post_init__(self):
        self.base_url: str = f"http://{self.host}:{self.port}"
        self.api_base: str = f"/api/{self.device_type}"
        self.app: FastAPI = FastAPI(
            title=f"{self.device_type.title()} - {self.device_id}",
        )
        self._setup_routes()

    @abstractmethod
    def _setup_routes(self):
        ...

    @abstractmethod
    def _get_status(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_capabilities(self) -> list[str]:
        ...

    @abstractmethod
    def perform_action(self, action: str, **kwargs) -> bool:
        ...

    def register(self, register_url: str = "http://127.0.0.1:8000"):
        device_info: DeviceInfo = DeviceInfo(
            device_id=self.device_id,
            device_type=self.device_type,
            host=self.host,
            port=self.port,
            capabilities=self.get_capabilities(),
        )

        try:
            response = requests.post(
                f"{register_url}/api/device/register",
                json=device_info.model_dump(),
            )
            if response.status_code == 200:
                print(f"Registered device {self.device_id} successfully")
            else:
                print(f"Failed to register device {self.device_id}")
        except Exception as e:
            print(f"Registry connection failed: {e}")

    def run_server(self):
        print(f"Starting server of {self.device_type} on {self.host}:{self.port}")
        uvicorn.run(
            self.app, host=self.host, port=self.port, log_level="info"
        )
