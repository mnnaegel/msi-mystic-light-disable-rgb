#!/bin/python3

import hid
import argparse
import itertools as it

MYSTIC_VID = 0x1462
MYSTIC_PID = 0x1563

ap = argparse.ArgumentParser(description="A simple script to change the lighting effects of the MSI Mystic Light MS-1563 RGB controller")
ap.add_argument("-S", "--speed", type=int, help="Cycle speed of the light effect (if applicable) [0..2]")
ap.add_argument("-B", "--brightness", type=int, default=10, help="(Max) Brightness of the lighting [0..10]")
ap_modes = ap.add_mutually_exclusive_group(required=True)
ap_modes.add_argument("-o", "--off", action="store_true", help="Turn the lighting off")
ap_modes.add_argument("-c", "--steady-color", type=str, help="Single steady color (color code like '#RRGGBB')")
ap_modes.add_argument("-b", "--breathing", type=str, nargs="+", help="Breathing (fade in and out) color(s), if multiple colors are provided, cycles through in order (color code like '#RRGGBB')")
ap_modes.add_argument("-s", "--color-shift", type=str, nargs="+", help="Shift trough multiple colors (color code like '#RRGGBB')")

args = ap.parse_args()

report = bytearray(64)
report[0] = 0x02  # USB HID report ID

if args.speed is not None:
    if args.speed <= 2 and args.speed >= 0:
        report[3] = args.speed
    else:
        raise ValueError("speed has to be between 0 and 2")
if args.brightness is not None:
    if args.brightness <= 10 and args.brightness >= 0:
        report[4] = args.brightness
    else:
        raise ValueError("brightness has to be between 0 and 10")

def parse_color_str(cs: str) -> tuple[int]:
    cs = cs.lstrip("#")
    red = int(cs[0:2], 16)
    green = int(cs[2:4], 16)
    blue = int(cs[4:6], 16)
    return red, green, blue

if args.off is not None and args.off:
    pass
elif args.steady_color is not None:
    report[2] = 0x01
    report[5] = 0x01
    report[6:9] = parse_color_str(args.steady_color)
elif args.breathing is not None:
    report[2] = 0x02
    report[5] = min(7, len(args.breathing))
    for i, c in zip(it.count(6, 3), args.breathing[:7]):
        report[i:i+3] = parse_color_str(c)
elif args.color_shift is not None:
    report[2] = 0x05
    report[5] = min(7, len(args.color_shift))
    for i, c in zip(it.count(6, 3), args.color_shift[:7]):
        report[i:i+3] = parse_color_str(c)

print("Sending HID Report: ", report.hex(" "))

with hid.device(MYSTIC_VID, MYSTIC_PID) as mlight:
    mlight.send_feature_report(bytes(report))


