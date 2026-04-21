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
# lapsepi

Simple timelapse camera app for Raspberry Pi.

This is currently focused on getting something that just works, rather than being overly polished.

---

## Requirements

- Python 3
- Python virtual environment support (`python3-venv`)
- `ffmpeg`
- `git`

---

## Installation (Pi)

This assumes a Raspberry Pi running a Debian-based OS.

### 1. Install system packages

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip ffmpeg git
```

### 2. Clone the repo

```bash
cd ~
git clone https://github.com/Ashterism/lapsepi.git
cd lapsepi
```

### 3. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Python requirements

```bash
pip install -r requirements.txt
pip install -e .
```

### 5. Test it runs

```bash
python -m lapsepi
```

Then open it in a browser using the Pi's IP address, e.g.:

```text
http://<pi-ip>:5002
```

### 6. Set up auto-start (systemd)

The app is designed to run on boot via a systemd service.

Open:

```text
src/lapsepi/utils/lapsepi.service
```

Update the paths to match your setup.

Using your current setup, the service file will want to look something like this:

```ini
WorkingDirectory=/home/ash/lapsepi
ExecStart=/home/ash/lapsepi/.venv/bin/python3 -m lapsepi
```

If your username or install path is different, update those paths before installing the service.

Then copy it into place:

```bash
sudo cp src/lapsepi/utils/lapsepi.service /etc/systemd/system/lapsepi.service
```

Enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable lapsepi.service
sudo systemctl start lapsepi.service
```

Check logs:

```bash
journalctl -u lapsepi.service -f
```

---

## Notes

- If the service does not start, the first thing to check is the paths in `lapsepi.service`
- `ffmpeg` must be installed or video generation will fail
- This is currently built to behave more like a small appliance than a polished app: boot, run, recover if needed
- More README detail can come later once Pi-side validation is done