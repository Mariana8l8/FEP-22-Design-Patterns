from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any
from devices.base_device import BaseDevice


class CurtainState(BaseModel):
    is_open: bool = False
    position: int = 0


class SmartCurtainsDevice(BaseDevice):
    def __init__(self, device_id: str, device_type: str = "Smart Curtain", host="127.0.0.1", port=8003):
        super().__init__(device_id, device_type, host, port)
        self.state = CurtainState()

    def _setup_routes(self):
        app = self.app

        @app.get("/status")
        async def get_status():
            return self._get_status()

        @app.post("/power/{power_state}")
        async def set_power(power_state: str):
            if not self.perform_action("power", power_state=power_state):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid curtain state. Allowed values: 'open' or 'close'."
                )
            return {"status": "success"}

        @app.post("/position/{position}")
        async def set_position(position: int):
            if not self.perform_action("position", position=position):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid position. Must be an integer between 0 and 100."
                )
            return {"status": "success"}

    def _get_status(self) -> dict[str, Any]:
        return {
            "status": "online",
            "device_id": self.device_id,
            "device_type": self.device_type,
            "is_open": self.state.is_open,
            "position": self.state.position,
            "connection": f"{self.host}:{self.port}"
        }

    def get_capabilities(self) -> list[str]:
        return ["status", "power", 'position']

    def perform_action(self, action: str, **kwargs) -> bool:
        if action == "power":
            power_state = kwargs.get("power_state")
            if power_state == "open":
                self.state.is_open = True
                self.state.position = 100
                return True
            elif power_state == "close":
                self.state.is_open = False
                self.state.position = 0
                return True
        elif action == "position":
            position = kwargs.get("position")
            if 0 <= position <= 100:
                self.state.position = position
                self.state.is_open = position > 0
                return True
        return False


if __name__ == "__main__":
    curtains = SmartCurtainsDevice("Curtains001")
    curtains.register()
    curtains.run_server()
