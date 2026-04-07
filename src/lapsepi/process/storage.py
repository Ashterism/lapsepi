import json

from datetime import datetime
from pathlib import Path


class Storage:
    def __init__(self):
        # save directories into temp memory)
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        data_dir = base_dir / "data"            # /data directory (e.g /lapsepi/data)
        self.images_dir = data_dir / "images"   # taken images directory
        self.videos_dir = data_dir / "videos"   # recorded video directory
        self.meta_dir = data_dir / "meta"       # metadata directory

    # HELPERS
    def create_timestamp(self):
        return(datetime.now().strftime("%H-%M-%S"))

    def create_datestamp(self):
        return(datetime.now().strftime("%Y-%m-%d"))


    # CREATE FILE PATHS
    def build_media_path(self, file_type):
        if file_type == "image":
            base_directory = self.images_dir
            prefix = "img_"
            extension = ".jpg"
        else:
            file_type == "video"
            base_directory = self.videos_dir
            prefix = "vid_"
            extension = ".mp4"

        # date folder (YYYY-MM-DD)
        date_folder = self.create_datestamp()
        directory = base_directory / date_folder
        directory.mkdir(parents=True, exist_ok=True)

        filename = prefix + self.create_timestamp() + extension
        return directory / filename

    
    # READ / WRITE JSON
    def write_json(self, file_path, content):
        with open(file_path, "w") as json_file:
            json.dump(content, json_file)
        

    # MANAGE LAST IMAGE TAKEN JSON
    def update_last_image_taken(self, content):
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.meta_dir / "last_image_taken.json"

        datestamp = self.create_datestamp() + "_" + self.create_timestamp()

        # store path relative to images_dir for portability
        relative_path = Path(content).relative_to(self.images_dir)

        full_content = {
            "last_updated" : datestamp,
            "file_location" : str(relative_path),
        }

        self.write_json(file_path, full_content)


    def read_last_image_taken(self):
        file_path = self.meta_dir / "last_image_taken.json"

        if not file_path.exists():
            return None

        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data.get("file_location")