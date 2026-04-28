# lapsepi

Simple timelapse camera app for Raspberry Pi.

This project prioritises reliability and simplicity over polish.

---

## What this needs

There are two kinds of dependencies here:

- system packages installed with `apt`
- Python packages installed with `pip`

Do not mix them up. `requirements.txt` only covers the Python bits.

---

## Python requirements

These are installed from `requirements.txt`:

- Flask
- Pillow

---

## System packages

These are not in `requirements.txt`, and need installing separately:

- Python 3
- Python virtual environment support (`python3-venv`)
- `python3-pip`
- `git`
- `ffmpeg`
- `python3-picamera2`

Install them with:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git ffmpeg python3-picamera2
```

---

## Optional: Hotspot mode (Access Point)

To allow direct connection without WiFi, set up a hotspot:

```bash
sudo nmcli connection add type wifi ifname wlan0 con-name potshot-hotspot autoconnect yes ssid potshot

sudo nmcli connection modify potshot-hotspot \
  802-11-wireless.mode ap \
  802-11-wireless.band bg \
  ipv4.method shared \
  wifi-sec.key-mgmt wpa-psk \
  wifi-sec.psk "badgerCaptain10"
```

Disable autoconnect on other networks:

```bash
nmcli connection modify "<connection-name>" connection.autoconnect no
```

---

## Installation (Pi)

This assumes a Raspberry Pi running a Debian-based OS.

## Camera

This project expects a Raspberry Pi camera using `picamera2`.

Ensure:
- the camera is enabled in `raspi-config`
- `python3-picamera2` is installed

### 1. Clone the repo

```bash
cd ~
git clone https://github.com/Ashterism/lapsepi.git
cd lapsepi
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python requirements

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Test it runs

```bash
python -m lapsepi
```

Then open it in a browser using the Pi's IP address, e.g.:

```text
http://<pi-ip>:5002
```

### Accessing the app

If running in hotspot mode, connect to:

- SSID: `potshot`
- then open:

```
http://192.168.4.1:5002
```

If running on a local network, you can access via:

- http://<pi-ip>:5002
- or (recommended, if available):

```
http://potshot.local:5002
```

### 5. Set up auto-start (systemd)

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

You should also explicitly set the user the service runs as, so files are created with the correct permissions:

```ini
User=ash
```

Make sure this matches your actual username on the Pi. If your username is different, update both the paths and the `User` value accordingly.

If your username or install path is different, update the paths and the `User` value before installing the service.

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

## Optional: SSH access

If you want to access your Pi remotely, enable SSH:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

---

## Data storage

Images, sessions, and metadata are stored under:

```
data/
  images/
  sessions/
  meta/
```

Do not manually edit files in `meta/` unless you know what you are doing.

## Behaviour notes

- Changing network mode may disconnect your current session
- Video generation on lower-powered devices can be slow

---

## Notes

- If you get `No module named picamera2`, you have not installed `python3-picamera2`
- If the service does not start, the first thing to check is the paths in `lapsepi.service`
- `ffmpeg` must be installed or video generation will fail
- This is currently built to behave more like a small appliance than a polished app: boot, run, recover if needed
- More README detail can come later once Pi-side validation is done