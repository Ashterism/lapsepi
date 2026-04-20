import json, shutil

from datetime import datetime
from pathlib import Path


class Storage:
    def __init__(self):
        # save directories into temp memory)
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.data_dir = base_dir / "data"  # /data directory (e.g /lapsepi/data)
        self.single_img_dir = self.data_dir / "images"
        self.session_dir = self.data_dir / "sessions"  # taken images directory
        self.videos_dir = self.data_dir / "videos"  # recorded video directory
        self.meta_dir = self.data_dir / "meta"  # metadata directory

    # HELPERS
    def create_timestamp(self):
        return datetime.now().strftime("%H-%M-%S")

    def create_datestamp(self):
        return datetime.now().strftime("%Y-%m-%d")

    # CREATE FOLDER PATHS
    def build_folder_path(self, session_type):
        if session_type == "single_image":
            directory = self.single_img_dir
        elif session_type == "timelapse":
            base_directory = self.session_dir

            # date folder (YYYY-MM-DD)
            date_folder = self.create_datestamp()
            time_folder = self.create_timestamp()
            directory = base_directory / date_folder / time_folder

        directory.mkdir(parents=True, exist_ok=True)
        return directory

    # CREATE FILE PATH
    def build_image_filepath(self, directory):
        prefix = "img_"
        extension = ".jpg"

        filename = prefix + self.create_timestamp() + extension
        return directory / filename

    # READ / WRITE JSON
    def write_json(self, file_path, content):
        with open(file_path, "w") as json_file:
            json.dump(content, json_file)

    def read_json(self, file_path):
        if not file_path.exists():
            return None
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    # LOCKFILE HANDLING
    def create_lockfile(self, name):
        lock_path = self.meta_dir / f"{name}.lock"
        self.meta_dir.mkdir(parents=True, exist_ok=True)

        with open(lock_path, "w"):
            pass

    def check_lockfile(self, name):
        lock_path = self.meta_dir / f"{name}.lock"
        return lock_path.exists()

    def delete_lockfile(self, name):
        lock_path = self.meta_dir / f"{name}.lock"
        if lock_path.exists():
            lock_path.unlink()

    # CLEAR IMAGES
    def clear_directory(self, directory):
        if not directory.exists():
            return
        for item in directory.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    def clear_images(self):
        self.clear_directory(self.single_img_dir)

    def clear_sessions(self):
        self.clear_directory(self.session_dir)

    def clear_all_media(self):
        self.clear_images()
        self.clear_sessions()
