import time, sys
from pathlib import Path

from .camera import Camera
from ..process.storage import Storage

camera = Camera()
storage = Storage()

def run_timelapse(directory=None, interval=None, runtime=None):
    
    directory = Path(sys.argv[1])
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else (interval or 5)
    runtime = int(sys.argv[3]) if len(sys.argv) > 3 else (runtime or 15)

    photos_to_take = int(runtime/interval)

    for i in range(photos_to_take):
        camera.take_image(directory)
        if i < photos_to_take - 1:
            time.sleep(interval)

    storage.delete_lockfile("camera_in_use")


def stop_timelapse():
    ...


if __name__ == "__main__":
    run_timelapse()