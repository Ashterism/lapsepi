from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
    jsonify,
    request,
)

from ..control.controller import get_photo, get_timelapse, get_timelapse_stopped, get_timelapse_video
from ..process.storage import Storage

storage = Storage()

app = Flask(__name__)


# route to homepage
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

    is_running = storage.check_lockfile("camera_in_use")

    return render_template(
        "index.html",
        image_path=image_path,
        taken_time=taken_time,
        is_running=is_running,
    )


# Serve images from /data/images
@app.route("/data/<path:filename>")
def serve_image(filename):
    return send_from_directory(storage.data_dir, filename)


# route to check if camera in use (lockfile check)
@app.route("/status")
def status():
    is_running = storage.check_lockfile("camera_in_use")
    state = "RUNNING" if is_running else "IDLE"

    return jsonify(
        {
            "state": state,
            "latest_frame": None,
            "frames_taken": None,
        }
    )


# route to call "take single image" function
@app.route("/take_photo", methods=["POST"])
def take_photo():
    get_photo()
    return redirect("/")


# route to call get timelapse (which runs in own process)
@app.route("/take_timelapse", methods=["POST"])
def take_timelapse():
    interval = request.form.get("interval")
    runtime = request.form.get("runtime")

    get_timelapse(interval, runtime)
    return redirect("/")


# route to kill the timelapse process
@app.route("/stop_timelapse", methods=["POST"])
def stop_timelapse():
    get_timelapse_stopped()
    return redirect("/")


@app.route("/gallery")
def gallery():

    sessions = storage.list_sessions()
    selected_session = request.args.get("session")
    session_media = storage.list_session_media(selected_session)

    timelapse_videos = storage.list_timelapse_vids()

    return render_template(
    "gallery.html",
    sessions=sessions,
    selected_session=selected_session,
    session_media=session_media,
    timelapse_videos=timelapse_videos,
    )


@app.route("/create_video", methods=["POST"])
def create_video():
    session_path = request.form.get("session")
    fps = request.form.get("fps")

    get_timelapse_video(session_path, fps)

    return redirect(f"/gallery?session={session_path}")

    
if __name__ == "__main__":
    app.run(debug=True, port=5002)


"""
python -m lapsepi.web.app
"""
