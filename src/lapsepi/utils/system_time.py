from datetime import datetime
import subprocess

def get_system_time():
    now = datetime.now().astimezone()

    return {
        "datetime": now,
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": str(now.tzinfo),
    }


def set_system_time(new_time):
# i.e. set_system_time("2026-05-22 14:52:00")
    subprocess.run([
        "sudo",
        "date",
        "-s",
        new_time
    ])