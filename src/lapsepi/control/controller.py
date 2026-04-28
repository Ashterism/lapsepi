import time, sys, subprocess


from ..process import pid_manager as pid
from ..capture.camera import Camera
from ..capture.timelapse import stop_timelapse
from ..process.storage import Storage
from ..process.video_maker import create_timelapse_video
from ..process.settings_man import SettingsManager
from ..process.network_man import NetworkManager


# runmode = detect_runmode()
camera = Camera()
storage = Storage()
settings_manager = SettingsManager()
network_manager = NetworkManager()


# CONTROL POINTS

### PREVIEW IMAGE ###
# TAKE TEST PHOTO
def get_photo():
    directory = use_camera("single_image")
    if directory == None:
        return
    camera.take_image(directory)
    camera.close_camera()
    storage.delete_lockfile("camera_in_use")


### TIMELAPSE CONTROLS ###
# RUN TIMELAPSE
def get_timelapse(interval, runtime):
    if not interval or not runtime:
        return

    directory = use_camera("timelapse")
    if directory == None:
        return

    timelapse_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "lapsepi.capture.timelapse",
            str(directory),
            str(interval),
            str(runtime),
        ]
    )

    pid.write_pid(timelapse_process.pid)

# STOP TIMELAPSE
def get_timelapse_stopped():
    stop_timelapse()

# CREATE TIMELAPSE VIDEO
def get_timelapse_video(session_path, fps):
    return create_timelapse_video(session_path, fps)


### MANAGE IMAGE SETTINGS ###

def get_camera_options():
    return settings_manager.get_camera_options()


def get_camera_settings():
    return settings_manager.get_camera_settings()


def update_camera_settings(data):
    return settings_manager.update_camera_settings(data)


# NETWORKING CONTROLS

def get_network_options():
    return network_manager.get_network_options()


def get_network_settings():
    return network_manager.get_network_settings()


def get_current_network_mode():
    return network_manager.get_current_network_mode()


def update_network_settings(data):
    return network_manager.update_network_settings(data)



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
    # get_photo()
    get_timelapse(5, 15)
    print(pid.read_pid())
