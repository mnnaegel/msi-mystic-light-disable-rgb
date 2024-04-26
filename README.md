# msi-mystic-light-disable-rgb
Sends signal to turn off RGB for computers with an MSI motherboard which typically use Mystic Light.

The purpose of the application is to allow operating systems without support for Mystic Light to still disable RGB settings.

# How to use
---
1. Get your Vendor ID and Product ID (referred to as VID and PID in the script) 
![image](https://github.com/mnnaegel/msi-mystic-light-disable-rgb/assets/86453692/9c9affd9-ed06-4ee4-8b36-632c4a7a86e5)
In this case, the VID and PID are in hexadecimal format and correspond to the MysticLight entry 1462:1563 as listed by `lsusb`

2. Replace your VID and PID in the `main.py`

The script can now be ran via `python main.py` to disable the backlight, but to make it so that it runs at startup you can follow these steps:
1. Run `sudo nano /etc/systemd/system/kill-led.service` and insert the following, ensuring that the user and /path/to/script are adjusted accordingly
```
[Unit]
Description=Kill Keyboard Backlight
After=multi-user.target

[Service]
Type=simple
User=user
ExecStart=/usr/bin/python3 /path/to/script

[Install]
WantedBy=multi-user.target
```
2. Enable the service via `sudo systemctl enable kill-led.service`
