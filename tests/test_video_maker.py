from lapsepi.process.storage import Storage
from lapsepi.process.video_maker import create_timelapse_video
from lapsepi.control.controller import get_timelapse_video

storage = Storage()

date = "2026-04-21"
time = "13-48-46"
session_path = storage.session_dir / date / time
fps = 30

def test_video_maker_basic():
    create_timelapse_video(session_path)


def test_via_controller():
    get_timelapse_video(session_path,fps)


if __name__ == "__main__":
   # test_video_maker_basic()
   test_via_controller()
