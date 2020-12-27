#!/usr/bin/python
"""
The script communicates between MixerControllerTeensy and server.py

"""

import serial  # pySerial https://pyserial.readthedocs.io/
import numpy
import time
from pythonosc.udp_client import SimpleUDPClient


# OSC-Clients
osc_router = SimpleUDPClient('127.0.0.1', 9000)


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
            track = words[1]
            mode = words[2]
            potNr = words[3]
            value = words[4]


          # Buttons
            if mode == "B":
                if track == "1":
                    osc_router.send_message("/ambijockey/mic/ch/1/pfl/", value)
                    sendData("L1")
                if track == "2":
                    osc_router.send_message("/ambijockey/mic/ch/2/pfl/", value)
                    sendData("L2")
                if track == "3":
                    osc_router.send_message("/ambijockey/mic/ch/3/pfl/", value)
                    sendData("L3")
                if track == "4":
                    osc_router.send_message("/ambijockey/mic/ch/4/pfl/", value)
                    sendData("L4")
                if track == "5":
                    osc_router.send_message("/ambijockey/mic/ch/master/pfl/", value)
                    sendData("L5")
          # Potis
            if mode == "P":
                if track == "1":
                    if potNr == "1":
                        osc_router.send_message("/ambijockey/mic/ch/1/gain/", value)
                    if potNr == "2":
                        osc_router.send_message("/ambijockey/mic/ch/1/hi/", value)
                    if potNr == "3":
                        osc_router.send_message("/ambijockey/mic/ch/1/mid/", value)
                    if potNr == "4":
                        osc_router.send_message("/ambijockey/mic/ch/1/lo/", value)
                    if potNr == "5":
                        osc_router.send_message("/ambijockey/mic/ch/1/volume/", value)
                if track == "2":
                    if potNr == "1":
                        osc_router.send_message("/ambijockey/mic/ch/2/gain/", value)
                    if potNr == "2":
                        osc_router.send_message("/ambijockey/mic/ch/2/hi/", value)
                    if potNr == "3":
                        osc_router.send_message("/ambijockey/mic/ch/2/mid/", value)
                    if potNr == "4":
                        osc_router.send_message("/ambijockey/mic/ch/2/lo/", value)
                    if potNr == "5":
                        osc_router.send_message("/ambijockey/mic/ch/2/volume/", value)
                if track == "3":
                    if potNr == "1":
                        osc_router.send_message("/ambijockey/mic/ch/3/gain/", value)
                    if potNr == "2":
                        osc_router.send_message("/ambijockey/mic/ch/3/hi/", value)
                    if potNr == "3":
                        osc_router.send_message("/ambijockey/mic/ch/3/mid/", value)
                    if potNr == "4":
                        osc_router.send_message("/ambijockey/mic/ch/3/lo/", value)
                    if potNr == "5":
                        osc_router.send_message("/ambijockey/mic/ch/3/volume/", value)
                if track == "4":
                    if potNr == "1":
                        osc_router.send_message("/ambijockey/mic/ch/4/gain/", value)
                    if potNr == "2":
                        osc_router.send_message("/ambijockey/mic/ch/4/hi/", value)
                    if potNr == "3":
                        osc_router.send_message("/ambijockey/mic/ch/4/mid/", value)
                    if potNr == "4":
                        osc_router.send_message("/ambijockey/mic/ch/4/lo/", value)
                    if potNr == "5":
                        osc_router.send_message("/ambijockey/mic/ch/4/volume/", value)
                if track == "5":
                    if potNr == "1":
                        osc_router.send_message("/ambijockey/mic/ch/master/volume/", value)
                    if potNr == "2":
                        osc_router.send_message("/ambijockey/mic/ch/master/hi/", value)
                    if potNr == "3":
                        osc_router.send_message("/ambijockey/mic/ch/master/mid/", value)
                    if potNr == "4":
                        osc_router.send_message("/ambijockey/mic/ch/master/lo/", value)

        time.sleep(0.001)

