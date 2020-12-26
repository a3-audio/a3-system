#!/usr/bin/python
"""
The script communicates between MixerControllerTeensy and server.py 

"""

import serial  # pySerial https://pyserial.readthedocs.io/
import numpy
import time
from pythonosc.udp_client import SimpleUDPClient


# OSC-Clients
osc_router = SimpleUDPClient('192.168.43.142', 9000)


def sendData(data):
    data += "\r\n"
    ser.write(data.encode())


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()

            words = line.split(":")
            identifier = words[0]
            value = words[1]

          # Porty
            if identifier == "P0":
                print("p1 " + value)
                osc_router.send_message(
                    "/ambijockey/mic/ch/1/gain/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P1":
                osc_router.send_message(
                    "/ambijockey/moc/ch/2/width", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P2":
                osc_router.send_message(
                    "/ambijockey/moc/ch/3/width/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P3":
                osc_router.send_message(
                    "/ambijockey/moc/ch/4/width/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P4":
                osc_router.send_message(
                    "/ambijockey/moc/ch/1/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P5":
                osc_router.send_message(
                    "/ambijockey/moc/ch/2/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P6":
                osc_router.send_message(
                    "/ambijockey/moc/ch/3/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P7":
                osc_router.send_message(
                    "/ambijockey/moc/ch/4/reverb/", numpy.interp(value, [0, 1023], [0, 1]))

          # Encoder
            if identifier == "Enc0":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/0/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "Enc1":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/1/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "Enc2":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/2/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "Enc3":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/3/", numpy.interp(value, [0, 1023], [0, 1]))

          # Encoder Buttens
            if identifier == "EB0":
                osc_router.send_message(
                    "/ambijockey/moc/EB/0/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "EB1":
                osc_router.send_message(
                    "/ambijockey/moc/EB/1/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "EB2":
                osc_router.send_message(
                    "/ambijockey/moc/EB/2/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "EB3":
                osc_router.send_message(
                    "/ambijockey/moc/EB/3/", numpy.interp(value, [0, 1023], [0, 1]))

          # Butten Matrix
            if identifier == "B0":
                osc_router.send_message("/ambijockey/moc/B/4/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/0/", value)
#                sendData("L1")
            if identifier == "B1":
                osc_router.send_message("/ambijockey/moc/B/3/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/0/", value)
            if identifier == "B2":
                osc_router.send_message("/ambijockey/moc/B/2/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/0/", value)
            if identifier == "B3":
                osc_router.send_message("/ambijockey/moc/B/1/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/0/", value)
            if identifier == "B4":
                osc_router.send_message("/ambijockey/moc/B/4/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/1/", value)
            if identifier == "B5":
                osc_router.send_message("/ambijockey/moc/B/3/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/1/", value)
            if identifier == "B6":
                osc_router.send_message("/ambijockey/moc/B/2/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/1/", value)
            if identifier == "B7":
                osc_router.send_message("/ambijockey/moc/B/1/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/1/", value)
            if identifier == "B8":
                osc_router.send_message("/ambijockey/moc/B/4/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/2/", value)
            if identifier == "B9":
                osc_router.send_message("/ambijockey/moc/B/3/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/2/", value)
            if identifier == "B10":
                osc_router.send_message("/ambijockey/moc/B/2/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/2/", value)
            if identifier == "B11":
                osc_router.send_message("/ambijockey/moc/B/1/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/2/", value)
            if identifier == "B12":
                osc_router.send_message("/ambijockey/moc/B/4/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/3/", value)
            if identifier == "B13":
                osc_router.send_message("/ambijockey/moc/B/3/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/3/", value)
            if identifier == "B14":
                osc_router.send_message("/ambijockey/moc/B/2/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/3/", value)
            if identifier == "B15":
                osc_router.send_message("/ambijockey/moc/B/1/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/3/", value)
            
        time.sleep(0.001)


