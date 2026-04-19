from flask import Flask, render_template, send_from_directory
from flask import redirect

from ..controller.controller import get_photo, get_timelapse
from ..process.storage import Storage

storage = Storage()

app = Flask(__name__)


@app.route("/")
def home():
    last_image_record = storage.read_json(storage.meta_dir / "last_image_taken.json")

    if not last_image_record:
        image_path = "/static/imgs/no_image.png"
        taken_time = "-"
    else:
        image_path = f"/data/{last_image_record['file_location']}"
        raw_time = last_image_record.get("last_updated")
        if raw_time:
            from datetime import datetime
            dt = datetime.strptime(raw_time, "%Y-%m-%d_%H-%M-%S")
            taken_time = dt.strftime("%y/%m/%d %H:%M:%S")
        else:
            taken_time = "-"

    return render_template(
        "index.html",
        image_path=image_path,
        taken_time=taken_time,
    )


# Serve images from /data/images
@app.route("/data/<path:filename>")
def serve_image(filename):
    return send_from_directory(storage.data_dir, filename)


@app.route("/take_photo", methods=["POST"])
def take_photo():
    get_photo()
    return redirect("/")


@app.route("/take_timelapse", methods=["POST"])
def take_timelapse():
    get_timelapse()
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