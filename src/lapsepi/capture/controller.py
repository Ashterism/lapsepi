from .camera import Camera
from ..process.storage import Storage


camera = Camera()
storage = Storage()



#@ wrapper
def use_camera():
    ...
    # check lockfil
    # exit if in use
    # USE CAMERA OR TIMELAPSE
    # remove lockfile



def take_photo():
    ...
    # set path as one off image path
    # create session file with relevnt imputs
    # call camera once with path
    # update session file


def take_timelapse():
    ...
    # set path as sessions / images / date-time
    # create session file with relevnt imputs
    # call camera once with path
    # update session file


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








    



