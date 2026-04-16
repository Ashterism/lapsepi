import time

from .camera import Camera
from ..process.storage import Storage
from ..utils.environment_detector import detect_runmode

runmode = detect_runmode()
camera = Camera(mode=runmode)
storage = Storage()


# CONTROL POINTS

def get_photo():
    use_camera("single_image")

def get_timelapse():
    use_camera("timelapse")


"""
1. add a sessions file - probs easiest for all camera usage
2. sort out use of dates and times in file / folder naming
3. wire up front end for single image (image and time) display
4. wire up timelapse to run 
5. grey out timelapse button



"""

# HELPERS

def run_timelapse(directory, interval=None, runtime=None):
    interval = 5
    runtime = 15
    photos_to_take = int(runtime/interval)

    for i in range(photos_to_take):
        camera.take_image(directory)
        if i < photos_to_take - 1:
            time.sleep(interval)


# ORCHESTRATION

def use_camera(session_type="single_image"):

    # CHECK AND SET LOCKFILE
    if storage.check_lockfile("camera_in_use"):
        return
    
    storage.create_lockfile("camera_in_use")

    # get the folder to save into
    directory = storage.build_folder_path(session_type)

    # then the filenames the camera gets from storage 

    if session_type == "single_image":
        camera.take_image(directory)

    elif session_type == "timelapse":
        run_timelapse(directory)
        ...





if __name__ == "__main__":
    storage.delete_lockfile("camera_in_use")
    #use_camera()
    get_timelapse()







    



