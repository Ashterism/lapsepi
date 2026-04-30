import subprocess
from .storage import Storage


class NetworkManager:
    def __init__(self):
        self.storage = Storage()
        self.network_settings = self.storage.meta_dir / "network_settings.json"

        self.network_modes = {
            "auto": "WiFi with hotspot fallback",
            "hotspot": "Hotspot only",
        }

    # FOR POPULATING FE OPTIONS
    def get_network_options(self):
        return {
            "modes": self.network_modes,
        }

    def update_network_settings(self, data):
        settings = {
            "target_mode": data.get("mode", "hotspot"),
        }

        self.storage.write_json(self.network_settings, settings)
        return settings

    def get_network_settings(self):
        saved = self.storage.read_json(self.network_settings)
        return saved or {"target_mode": "hotspot"}

    def get_current_network_mode(self):
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "NAME", "connection", "show", "--active"],
                capture_output=True,
                text=True,
            )

            for name in result.stdout.splitlines():
                if "potshot" in name.lower():
                    return "hotspot"

                if "wlan" in name.lower() or "wifi" in name.lower():
                    return "auto"

            return "unknown"

        except FileNotFoundError:
            return "unknown"

    def enable_hotspot(self):
        try:
            subprocess.run(
                ["nmcli", "connection", "down", "potshot-hotspot"],
                capture_output=True,
                text=True,
            )

            result = subprocess.run(
                ["nmcli", "connection", "up", "potshot-hotspot"],
                capture_output=True,
                text=True,
            )

            return result.returncode == 0

        except FileNotFoundError:
            return False

    def connect_to_wifi(self, ssid):
        try:
            subprocess.run(
                ["nmcli", "connection", "down", "potshot-hotspot"],
                capture_output=True,
                text=True,
            )

            result = subprocess.run(
                ["nmcli", "connection", "up", ssid],
                capture_output=True,
                text=True,
            )

            return result.returncode == 0

        except FileNotFoundError:
            return False

    def apply_target_mode(self):
        settings = self.get_network_settings()
        target_mode = settings.get("target_mode", "hotspot")

        if target_mode == "hotspot":
            return self.enable_hotspot()

        if target_mode == "auto":
            saved_networks = self.get_saved_wifi_networks()

            for network in saved_networks:
                connection_name = network.get("connection_name")
                if connection_name and self.connect_to_wifi(connection_name):
                    return True

            return self.enable_hotspot()

        return self.enable_hotspot()

    def get_wifi_ssid(self, connection_name):
        try:
            result = subprocess.run(
                ["nmcli", "connection", "show", connection_name],
                capture_output=True,
                text=True,
            )

            for line in result.stdout.splitlines():
                if line.startswith("802-11-wireless.ssid:"):
                    return line.split(":", 1)[1].strip()

            return connection_name.replace("netplan-wlan0-", "")

        except FileNotFoundError:
            return connection_name

    def get_saved_wifi_networks(self):
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "NAME", "connection", "show"],
                capture_output=True,
                text=True,
            )

            networks = []

            for connection_name in result.stdout.splitlines():
                if not connection_name.startswith("netplan-wlan"):
                    continue

                ssid = self.get_wifi_ssid(connection_name)

                networks.append(
                    {
                        "ssid": ssid,
                        "connection_name": connection_name,
                    }
                )

            return networks

        except FileNotFoundError:
            # running on non-Pi (e.g. Mac)
            return [{"ssid": "(nmcli not available)", "connection_name": ""}]
