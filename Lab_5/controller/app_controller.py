from typing import Any

from controller.iot_facade import IotFacade
from devices.base_device import DeviceInfo


class AppController:
    def __init__(self):
        self.facade = IotFacade()

    def register_device(self, device_info: DeviceInfo) -> None:
        self.facade.register_device(device_info)

    def get_all_statuses(self) -> list[dict[str, Any]]:
        return self.facade.get_all_statuses()

    def _perform_action_by_type(self, device_type: str, action: str, *values) -> None:
        for item in self.get_all_statuses():
            try:
                if item['device_type'] == device_type:
                    success = self.facade.perform_action(item['device_id'], action, *values)
                    if not success:
                        print(f"ERROR: Failed to perform '{action}' for {item['device_id']}")

            except (AttributeError, KeyError):
                pass

    def _toggle_power_by_type(self, device_type: str, state_key: str, on_value: str, off_value: str) -> None:
        for item in self.get_all_statuses():
            try:
                if item['device_type'] == device_type:
                    action_value = off_value if item[state_key] else on_value
                    success = self.facade.perform_action(item['device_id'], 'power', action_value)
                    if not success:
                        print(f"ERROR: Failed to perform 'power' for {item['device_id']}")
            except (AttributeError, KeyError):
                pass

    def toggle_speaker(self) -> None:
        self._toggle_power_by_type("Smart Speaker", "is_on", "on", "off")

    def set_speaker_volume(self, volume_level: int) -> None:
        self._perform_action_by_type("Smart Speaker", "volume", volume_level)

    def set_speaker_track(self, track_name: str) -> None:
        self._perform_action_by_type("Smart Speaker", "track", track_name)

    def toggle_light(self) -> None:
        self._toggle_power_by_type("Smart Light", "is_on", "on", "off")

    def set_light_brightness(self, brightness_level: int) -> None:
        self._perform_action_by_type("Smart Light", "brightness", brightness_level)

    def set_light_rgb(self, r: int, g: int, b: int) -> None:
        self._perform_action_by_type("Smart Light", "rgb", r, g, b)

    def toggle_curtain(self) -> None:
        self._toggle_power_by_type("Smart Curtain", "is_open", "open", "close")

    def set_curtain_position(self, position: int) -> None:
        self._perform_action_by_type("Smart Curtain", "position", position)
