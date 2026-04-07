# run by typing the following in the terminal: 
# PYTHONPATH=src pytest -q

from motionpi.camera import Camera
from motionpi.storage import Storage

storage = Storage()
cam = Camera("dev")

img_dir = storage.images_dir

def test_mock_camera_img_file_created():
    count1 = img_dir.glob("*")
    cam.take_image()
    count2 = img_dir.glob("*")
    assert count2 == count1 + 1
    
