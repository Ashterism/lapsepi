import time


from .capture.camera import Camera




def main():
   
   # check for lockfile
        # if lockfile, note there was an issue
        # and clear lockfile
    
    # start webserver (while... until told to stop?)

    interval = 10
    runtime = 20
    photos = int(runtime/interval)

    for i in range(photos):
        camera.take_image()
        if i < photos - 1:
            time.sleep(interval)


if __name__ == "__main__":
    main()
