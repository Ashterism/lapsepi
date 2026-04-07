import time

from .utils.environment_detector import detect_runmode
from .capture.camera import Camera




def main():
    runmode = detect_runmode()
    camera = Camera(mode=runmode)

    print(runmode)


    interval = 10
    runtime = 20
    photos = int(runtime/interval)

    for i in range(photos):
        camera.take_image()
        if i < photos - 1:
            time.sleep(interval)


if __name__ == "__main__":
    main()
