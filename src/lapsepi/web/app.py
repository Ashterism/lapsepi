from flask import Flask, render_template
from flask import redirect

from ..capture.camera import Camera

camera = Camera(mode="dev")

app = Flask(__name__)


@app.route("/")
def home():

    return render_template(
        "index.html",
    )


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