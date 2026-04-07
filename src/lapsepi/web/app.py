from flask import Flask, render_template, send_from_directory
from flask import redirect

from ..capture.camera import Camera
from ..process.storage import Storage

camera = Camera(mode="dev")
storage = Storage()

app = Flask(__name__)


@app.route("/")
def home():
    image_path = storage.read_last_image_taken()

    if image_path is None:
        image_path = "/static/imgs/no_image.png"
    else:
        image_path = f"/data/images/{image_path}"

    return render_template(
        "index.html",
        image_path=image_path
    )


# Serve images from /data/images
@app.route("/data/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(storage.images_dir, filename)


@app.route("/take_photo", methods=["POST"])
def take_photo():
    filepath = camera.take_image()
    return redirect("/")


@app.route("/styleguide")
def styleguide():
    return render_template(
        "styleguide.html"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5002)

"""
python -m lapsepi.web.app
"""