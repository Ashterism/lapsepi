# lapsepi

Simple timelapse camera app for Raspberry Pi.

This is currently focused on getting something that just works, rather than being overly polished.

---

## Requirements

- Python (running in a venv is recommended)
- ffmpeg installed and available on PATH

On Raspberry Pi (Debian-based), install ffmpeg with:

```
sudo apt update
sudo apt install ffmpeg
```

Verify install:

```
ffmpeg -version
```

---

## Installation (Pi)

Make sure ffmpeg is installed (see above), otherwise video creation will fail.

Clone the repo somewhere sensible, e.g.:

```
~/lapsepi
```

Create and activate a virtual environment, install requirements as needed.

---

## Set up auto-start (systemd)

The app is designed to run on boot via a systemd service.

### 1. Update the service file

Open:

```
src/lapsepi/utils/lapsepi.service
```

Update the paths to match your setup:

- username (e.g. `pi`, `ash`, etc)
- project directory
- venv python path

Example:

```
WorkingDirectory=/home/pi/lapsepi
ExecStart=/home/pi/lapsepi/.venv/bin/python3 -m lapsepi
```

### 2. Copy the service file

```
sudo cp src/lapsepi/utils/lapsepi.service /etc/systemd/system/lapsepi.service
```

### 3. Enable + start

```
sudo systemctl daemon-reload
sudo systemctl enable lapsepi.service
sudo systemctl start lapsepi.service
```

### 4. Check logs

```
journalctl -u lapsepi.service -f
```

---

## Notes

- The service assumes your paths are correct — if it fails, this is the first thing to check
- ffmpeg must be installed or video generation will fail
- This is currently built as a "small appliance" style app — boot → run → recover if needed

More to come once Pi-side validation is complete.