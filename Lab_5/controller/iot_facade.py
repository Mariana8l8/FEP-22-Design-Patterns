from typing import Any

import requests

from devices.base_device import DeviceInfo


class IotFacade:
    def __init__(self):
        self.devices: dict[str, DeviceInfo] = {}

    def register_device(self, device: DeviceInfo) -> None:
        self.devices[device.device_id] = device

    def get_all_statuses(self) -> list[dict[str, Any]]:
        statuses_list: list[dict[str, Any]] = []

        for device_id, device in self.devices.items():
            url = f"http://{device.host}:{device.port}/status"
            try:
                response = requests.get(url, timeout=1)
                statuses_list.append(response.json())
            except requests.exceptions.ConnectionError:
                statuses_list.append({
                    'status': 'offline',
                    'device_id': device_id,
                    'device_type': device.device_type
                })

        return statuses_list

    def perform_action(self, device_id: str, action: str, *values) -> bool:
        device = self.devices.get(device_id)

        if action not in device.capabilities:
            print(f"Action failed: Device {device.device_type} does not support '{action}'.")
            return False

        status_string = "/".join([str(value) for value in values])
        url = f"http://{device.host}:{str(device.port)}/{action}/{status_string}"

        try:
            requests.post(url, timeout=2)
            return True
        except requests.exceptions.ConnectionError:
            print(f"Action failed: Device {device_id} is offline.")
            return False
