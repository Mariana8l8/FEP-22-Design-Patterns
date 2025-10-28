from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from devices.base_device import Device

class CurtainState(BaseModel):
    is_open: bool = False
    position: int = 0  # 0 = closed, 100 = fully open

class SmartCurtainsDevice(Device):
    def __init__(self, device_id: str, host="127.0.0.1", port=8003):
        super().__init__(device_id, host, port)
        self.state = CurtainState()
        self.app = FastAPI(title=f"Smart Curtains {device_id}")
        self._setup_routes()

    def _setup_routes(self):
        app = self.app

        @app.get("/status")
        async def get_status():
            return self.get_status()

        @app.post("/power/{state}")
        async def set_power(state: str):
            if not self.perform_action("power", state=state):
                raise HTTPException(status_code=400, detail="Invalid curtain state")
            return {"status": "success"}

        @app.post("/position/{value}")
        async def set_position(value: int):
            if not self.perform_action("position", value=value):
                raise HTTPException(status_code=400, detail="Invalid position")
            return {"status": "success"}

    def get_status(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": "smart_curtains",
            "is_open": self.state.is_open,
            "position": self.state.position,
            "connection": f"{self.host}:{self.port}"
        }

    def perform_action(self, action: str, **kwargs) -> bool:
        if action == "power":
            state = kwargs.get("state")
            if state == "open":
                self.state.is_open = True
                self.state.position = 100
                return True
            elif state == "close":
                self.state.is_open = False
                self.state.position = 0
                return True
        elif action == "position":
            value = kwargs.get("value")
            if value is None:
                return False
            v = int(value)
            if 0 <= v <= 100:
                self.state.position = v
                self.state.is_open = v > 0
                return True
        return False

    def run_server(self):
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")

if __name__ == "__main__":
    curtains = SmartCurtainsDevice("curtains_001")
    curtains.run_server()
