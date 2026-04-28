import subprocess
from .storage import Storage


class NetworkManager():
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
                ["nmcli", "-t", "-f", "NAME,TYPE,DEVICE", "connection", "show", "--active"],
                capture_output=True,
                text=True,
            )

            for line in result.stdout.splitlines():
                parts = line.split(":")
                if len(parts) < 2:
                    continue

                connection_name = parts[0]
                connection_type = parts[1]

                if connection_name == "potshot-hotspot":
                    return "hotspot"

                if connection_type == "wifi":
                    return "auto"

            return "unknown"

        except FileNotFoundError:
            return "unknown"


    def enable_hotspot(self):
        try:
            subprocess.run(["nmcli", "connection", "down", "potshot-hotspot"])
            subprocess.run(["nmcli", "connection", "up", "potshot-hotspot"])
        except FileNotFoundError:
            return None
        
    def connect_to_wifi(self, ssid):
        try:
            subprocess.run(["nmcli", "connection", "down", "potshot-hotspot"])
            subprocess.run(["nmcli", "connection", "up", ssid])
        except FileNotFoundError:
            return None


    def get_saved_wifi_networks(self):
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"],
                capture_output=True,
                text=True,
            )

            networks = []

            for line in result.stdout.splitlines():
                name, conn_type = line.split(":")
                if conn_type == "wifi":
                    networks.append(name)

            return networks

        except FileNotFoundError:
            # running on non-Pi (e.g. Mac)
            return ["(nmcli not available)"]