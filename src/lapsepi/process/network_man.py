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
                ["nmcli", "-t", "-f", "NAME", "connection", "show"],
                capture_output=True,
                text=True,
            )

            networks = []

            for name in result.stdout.splitlines():
                if name.startswith("netplan-wlan"):
                    networks.append(name)

            return networks

        except FileNotFoundError:
            # running on non-Pi (e.g. Mac)
            return ["(nmcli not available)"]