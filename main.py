import hid

VID = 0x1462
PID = 0x1563

# Try to open the device
try:
    h = hid.device()
    h.open(VID, PID)  # open by VID and PID

    report = bytearray(64)
    report[0] = 0x02

    h.send_feature_report(bytes(report))

    h.close()

except IOError as ex:
    print("Error:", ex)