import time, sys, subprocess

from ..capture.camera import Camera
from ..process.storage import Storage


# runmode = detect_runmode()
camera = Camera()
storage = Storage()


# CONTROL POINTS

def get_photo():
    directory = use_camera("single_image")
    if directory == None:
        return
    camera.take_image(directory)
    storage.delete_lockfile("camera_in_use")
    

def get_timelapse(interval, runtime):
    if not interval or not runtime:
        return
    
    directory = use_camera("timelapse")
    if directory == None:
        return
    
    timelapse_process = subprocess.Popen([
        sys.executable,
        "-m",
        "lapsepi.capture.timelapse",
        str(directory),
        str(interval),
        str(runtime),
    ])

    timelapse_pid = timelapse_process.pid


"""
	1.	move timelapse to its own runner file and get Popen working
	2.	pass interval + runtime from UI into it
	3.	add PID save/read/kill
	4.	add stop button in UI using that
	5.	align single-shot camera flow if needed

"""


# HELPER

def use_camera(session_type="single_image"):

    # CHECK AND SET LOCKFILE
    if storage.check_lockfile("camera_in_use"):
        return
    
    storage.create_lockfile("camera_in_use")

    # get the folder to save into
    # then the filenames the camera gets from storage 
    directory = storage.build_folder_path(session_type)

    return directory



if __name__ == "__main__":
    storage.delete_lockfile("camera_in_use")
    #get_photo()
    get_timelapse()







    



