from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any
from devices.base_device import BaseDevice


class SpeakerState(BaseModel):
    is_on: bool = False
    volume: int = 50
    current_track: str = ""


class SmartSpeakerDevice(BaseDevice):
    def __init__(self, device_id: str, device_type: str = "Smart Speaker", host="127.0.0.1", port=8001):
        super().__init__(device_id, device_type, host, port)
        self.state = SpeakerState()

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
                    detail="Invalid power state. Allowed values: 'on' or 'off'."
                )
            return {"status": "success"}

        @app.post("/volume/{volume_level}")
        async def set_volume(volume_level: int):
            if not self.perform_action("volume", volume_level=volume_level):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid volume level. Must be an integer between 0 and 100."
                )
            return {"status": "success"}

        @app.post("/track/{track_name}")
        async def set_track(track_name: str):
            if not self.perform_action("track", track_name=track_name):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid track name. Must be a non-empty string."
                )
            return {"status": "success"}

    def _get_status(self) -> dict[str, Any]:
        return {
            "status": "online",
            "device_id": self.device_id,
            "device_type": self.device_type,
            "is_on": self.state.is_on,
            "volume": self.state.volume,
            "current_track": self.state.current_track,
            "connection": f"{self.host}:{self.port}"
        }

    def get_capabilities(self) -> list[str]:
        return ["status", "power", 'volume', 'track']

    def perform_action(self, action: str, **kwargs) -> bool:
        if action == "power":
            power_state = kwargs.get("power_state")
            if power_state == "on":
                self.state.is_on = True
                return True
            elif power_state == "off":
                self.state.is_on = False
                return True
        elif action == "volume":
            volume_level = kwargs.get("volume_level")
            if 0 <= volume_level <= 100:
                self.state.volume = volume_level
                return True
        elif action == "track":
            track_name = kwargs.get("track_name")
            if track_name:
                self.state.current_track = track_name
                return True
        return False


if __name__ == "__main__":
    speaker = SmartSpeakerDevice("Speaker001")
    speaker.register()
    speaker.run_server()
