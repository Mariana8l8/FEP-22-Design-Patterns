from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any
from devices.base_device import BaseDevice


class LightState(BaseModel):
    is_on: bool = False
    brightness: int = 0
    rgb: tuple[int, int, int] = (0, 0, 0)


class SmartLightDevice(BaseDevice):
    def __init__(self, device_id: str, device_type: str = "Smart Light", host="127.0.0.1", port=8002):
        super().__init__(device_id, device_type, host, port)
        self.state = LightState()

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
                    detail="Invalid light state. Allowed values: 'on' or 'off'."
                )
            return {"status": "success"}

        @app.post("/brightness/{brightness}")
        async def set_brightness(brightness: int):
            if not self.perform_action("brightness", brightness=brightness):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid brightness. Must be an integer between 0 and 100."
                )
            return {"status": "success"}

        @app.post("/rgb/{r}/{g}/{b}")
        async def set_rgb(r: int, g: int, b: int):
            if not self.perform_action("rgb", rgb=(r, g, b)):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid RGB values. Must be integers between 0 and 255."
                )
            return {"status": "success"}

    def _get_status(self) -> dict[str, Any]:
        return {
            "status": "online",
            "device_id": self.device_id,
            "device_type": self.device_type,
            "is_on": self.state.is_on,
            "brightness": self.state.brightness,
            "rgb": self.state.rgb,
            "connection": f"{self.host}:{self.port}"
        }

    def get_capabilities(self) -> list[str]:
        return ["status", "power", 'brightness', 'rgb']

    def perform_action(self, action: str, **kwargs) -> bool:
        if action == "power":
            power_state = kwargs.get("power_state")
            if power_state == "on":
                self.state.is_on = True
                self.state.brightness = 100
                return True
            elif power_state == "off":
                self.state.is_on = False
                self.state.brightness = 0
                return True
        elif action == "brightness":
            brightness = kwargs.get("brightness")
            if 0 <= brightness <= 100:
                self.state.brightness = brightness
                self.state.is_on = brightness > 0
                return True
        elif action == "rgb":
            rgb = kwargs.get("rgb")
            if all(0 <= c <= 255 for c in rgb):
                self.state.rgb = rgb
                self.state.is_on = any(c > 0 for c in rgb)
                return True
        return False


if __name__ == "__main__":
    light = SmartLightDevice("Light001")
    light.register()
    light.run_server()
