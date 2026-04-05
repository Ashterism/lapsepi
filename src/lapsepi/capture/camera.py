import time
from ..process.storage import Storage
from ..mocks.mock_file_maker import create_mock_jpg

storage = Storage()


""" later on... move cam start from init to take image to save battery """


# handles image/video capture; delegates file paths to Storage; switches between real and mock based on mode
class Camera:

    def __init__(self, mode="dev"):
        self.mode = mode
        if self.mode == "prod":
            # setup for REAL camera
            from picamera2 import Picamera2
            self.cam = Picamera2()

            # Configure once for still capture and start camera
            still_config = self.cam.create_still_configuration()
            self.cam.configure(still_config)
            self.cam.start()

        # dev mode > nothing to set up
        

    # capture a single image; uses real camera in prod, mock file in dev
    def take_image(self):
        if self.mode == "prod":
            filepath = storage.build_media_path("image")
            self.cam.capture_file(filepath)

        elif self.mode == "dev":
            time.sleep(0.1)
            filepath = storage.build_media_path("image")
            create_mock_jpg(filepath)


    # record a short video clip; uses real camera in prod, mock file in dev
    def take_video(self, duration=10):
        if self.mode == "prod":
            from picamera2.encoders import H264Encoder
            from picamera2.outputs import FfmpegOutput

            filepath = storage.build_media_path("video")

            # Configure the camera for video capture before recording
            video_config = self.cam.create_video_configuration(main={"size": (1920, 1080)})
            self.cam.configure(video_config)
            self.cam.start()

            encoder = H264Encoder(bitrate=8_000_000)
            output = FfmpegOutput(filepath)

            self.cam.start_recording(encoder, output)
            time.sleep(duration)
            self.cam.stop_recording()
            self.cam.stop()

        elif self.mode == "dev":   
            filepath = storage.build_media_path("video")
            with open(filepath, "wb"):
                pass
