from .camera import Camera
from ..process.storage import Storage


camera = Camera()
storage = Storage()

""" not setting the camera run mode?   maybe just do in camera?
    or in here?
"""

def take_single_photo():
    use_camera("single_image")


def run_timelapse():
    use_camera("timelapse")
   

"""
Thinking is can be function takes duration to run and interval
calcs photos to take.  if 1... save to single shot folder, else... create session

could be a "helper" function that means UI can call "take photo"
and that just sets to 1 shot and 0 interval
"""

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
        # loop through iterations
        ...





if __name__ == "__main__":
    use_camera()








    



