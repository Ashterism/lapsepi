import time


from .capture.camera import Camera


def main():

    # check for lockfile
    # if lockfile, note there was an issue
    # and clear lockfile
    # same for pid

    # start webserver (while... until told to stop?)

    # if system tries to shut you down... do it gracefully and log it
    # guessing it's just going to be the power being pulled as no button..
    # to which, i guess thee is no real defence.


if __name__ == "__main__":
    main()
