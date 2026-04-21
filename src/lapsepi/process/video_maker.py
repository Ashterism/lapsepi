# This file takes a folder of images from a timelapse session and turn them into an MP4 using ffmpeg.
#
# Important bit:
# We are NOT doing video processing in Python. We are just building a command
# and asking the system to run ffmpeg (same as if you typed it in Terminal).
#
# Flow is basically:
# 1. Get ordered list of images for a session
# 2. Write them into a temporary "file_list.txt" (format ffmpeg expects)
# 3. Build an ffmpeg command
# 4. Run it via subprocess.run()
# 5. Clean up temp file
#
# So: Python = orchestration
#     ffmpeg = actual video creation


from pathlib import Path
import subprocess

from .storage import Storage

storage = Storage()


def create_timelapse_video(session_path, fps=30):
    if not session_path:
        return None

    session_dir = storage.data_dir / session_path

    if not session_dir.exists() or not session_dir.is_dir():
        return None

    # get ordered images from storage
    media = storage.list_session_media(session_path)

    if not media:
        return None

    # create a temporary file list for ffmpeg
    file_list_path = session_dir / "file_list.txt"

    with open(file_list_path, "w") as f:
        for item in media:
            # ffmpeg expects paths relative to working dir or absolute
            img_path = storage.data_dir / item["path"]
            f.write(f"file '{img_path}'\n")

    output_path = session_dir / f"timelapse_{fps}.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(file_list_path),
        "-vf",
        f"fps={fps}",
        "-pix_fmt",
        "yuv420p",
        str(output_path),
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return None
    finally:
        if file_list_path.exists():
            file_list_path.unlink()

    return str(output_path)
