from .storage import Storage


class SettingsManager:

    def __init__(self):
        self.storage = Storage()
        self.camera_settings_file = self.storage.meta_dir / "camera_settings.json"
        self.default_camera_settings = {
            "preset": "default",
            "resolution": "2304x1296",
        }
        self.camera_presets = {
            "default": "Default (standard daytime)",
            "sunset": "Sunset",
            "nightscape": "Nightscape",
            "astro": "Astro",
            "custom": "Custom",
        }
        self.camera_resolutions = {
            "1920x1080": "1920 x 1080",
            "2304x1296": "2304 x 1296 (default)",
            "4608x2592": "4608 x 2592",
        }

    def get_camera_options(self):
        return {
            "presets": self.camera_presets,
            "resolutions": self.camera_resolutions,
            "defaults": self.default_camera_settings,
        }

    def get_camera_settings(self):

        saved_settings = (
            self.storage.read_json(self.camera_settings_file)
            or self.default_camera_settings
        )
        return saved_settings

    def update_camera_settings(self, data):
        settings = {
            "preset": data.get("preset", "default"),
            "resolution": data.get("resolution", "2304x1296"),
        }

        self.storage.write_json(self.camera_settings_file, settings)
        return settings
