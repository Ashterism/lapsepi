

requires ffmeg


at install...

open lapsepi.service
>
edit the path to reflect where you installed the app

i.e. update username/path before copying to /etc/systemd/system/

then...run it...

then...

sudo systemctl daemon-reload
sudo systemctl enable monipi.service
sudo systemctl start monipi.servic