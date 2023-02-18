import json
import os

from .commander import Commander


class DeviceManager:
    def __init__(self):
        self._commander = Commander()
        self.devices = {}
        self._check_file()

    def _check_file(self):
        path = "devices.json"
        if not os.path.exists(path):
            self._save_devices()
        self._load_devices()

    def _save_devices(self):
        with open("devices.json", "w") as outfile:
            outfile.write(json.dumps(self.devices))

    def _load_devices(self):
        with open("devices.json", "r") as openfile:
            self.devices = json.load(openfile)

    def get_list_of_devices(self):
        devices = []
        for key, value in self.devices.items():
            devices.append(value.get("name", key))
        return devices

    def add_device(self, ip, name):
        self.devices[ip] = {"name": name}
        self._save_devices()

    def _find_ip(self, device):
        for key, values in self.devices.items():
            if key == device:
                return key
            if values.get("name") == device:
                return key

    def install_app(self, device, app):
        ip = self._find_ip(device=device)
        connected = self._commander.use_system_command("adb connect " + str(ip))
        if connected:
            installed = self._commander.use_system_command(
                f"adb -s {ip} install-multiple -r {app}"
            )
            return installed
        print(f"Cant connect to {device}")
        return False
