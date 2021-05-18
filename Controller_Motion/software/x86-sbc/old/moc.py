#!/usr/bin/python
"""
Das ist unser script um die komunikation zwischen teensy und GUI herzystellen.

"""

import serial  # pySerial https://pyserial.readthedocs.io/
import numpy
import time
from pythonosc.udp_client import SimpleUDPClient


# OSC-Clients
osc_router = SimpleUDPClient('192.168.43.52', 9000)
osc_gui = SimpleUDPClient('127.0.0.1', 8600)


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
                # print("p1 " + value)
                osc_router.send_message(
                    "/ambijockey/moc/ch/1/width/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/1/width/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P1":
                osc_router.send_message(
                    "/ambijockey/moc/ch/2/width", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/2/width", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P2":
                osc_router.send_message(
                    "/ambijockey/moc/ch/3/width/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/3/width/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P3":
                osc_router.send_message(
                    "/ambijockey/moc/ch/4/width/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/4/width/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P4":
                osc_router.send_message(
                    "/ambijockey/moc/ch/1/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/1/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P5":
                osc_router.send_message(
                    "/ambijockey/moc/ch/2/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/2/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P6":
                osc_router.send_message(
                    "/ambijockey/moc/ch/3/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/3/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "P7":
                osc_router.send_message(
                    "/ambijockey/moc/ch/4/reverb/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/ch/4/reverb/", numpy.interp(value, [0, 1023], [0, 1]))

          # Encoder
          # TODO hier sollten wir noch die logig ueberarbeiten encoder imput ist anders als ein Poti
            if identifier == "Enc0":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/0/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/Enc/0/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "Enc1":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/1/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/Enc/1/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "Enc2":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/2/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/Enc/2/", numpy.interp(value, [0, 1023], [0, 1]))
            if identifier == "Enc3":
                osc_router.send_message(
                    "/ambijockey/moc/Enc/3/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/Enc/3/", numpy.interp(value, [0, 1023], [0, 1]))

          # Encoder Buttons
            if identifier == "EB0":
                osc_router.send_message(
                    "/ambijockey/moc/EB/0/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/EB/0/", numpy.interp(value, [0,1], [1,0]))
            if identifier == "EB1":
                osc_router.send_message(
                    "/ambijockey/moc/EB/1/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/EB/1/",  numpy.interp(value, [0,1], [1,0]))
            if identifier == "EB2":
                osc_router.send_message(
                    "/ambijockey/moc/EB/2/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/EB/2/",  numpy.interp(value, [0,1], [1,0]))
            if identifier == "EB3":
                osc_router.send_message(
                    "/ambijockey/moc/EB/3/", numpy.interp(value, [0, 1023], [0, 1]))
                osc_gui.send_message(
                    "/ambijockey/moc/EB/3/", numpy.interp(value, [0,1], [1,0]))

          # Button Matrix - Button to led matrix
          #
          # -------------------------
          # | B3  | B2  | B1  | B0  |  
          # | L15 | L8  | L7  | L0  |
          # ------------------------- 
          # | B7  | B6  | B5  | B4  |
          # | L14 | L9  | L6  | L1  |
          # ------------------------- 
          # | B11 | B10 | B9  | B8  |
          # | L13 | L10 | L5  | L2  |
          # -------------------------
          # | B15 | B14 | B13 | B1  |
          # | L12 | L11 | L4  | L3  |
          # -------------------------

            if identifier == "B0":
                osc_router.send_message("/ambijockey/moc/B/4/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/0/", value)
                sendData("L,0,255,255,255")
            if identifier == "B1":
                osc_router.send_message("/ambijockey/moc/B/3/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/0/", value)
                sendData("L,7,255,255,255")
            if identifier == "B2":
                osc_router.send_message("/ambijockey/moc/B/2/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/0/", value)
                sendData("L,8,255,255,255")
            if identifier == "B3":
                osc_router.send_message("/ambijockey/moc/B/1/0/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/0/", value)
                sendData("L,15,255,255,255")
            if identifier == "B4":
                osc_router.send_message("/ambijockey/moc/B/4/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/1/", value)
                sendData("L,1,255,255,255")
            if identifier == "B5":
                osc_router.send_message("/ambijockey/moc/B/3/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/1/", value)
                sendData("L,6,255,255,255")
            if identifier == "B6":
                osc_router.send_message("/ambijockey/moc/B/2/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/1/", value)
                sendData("L,9,255,255,255")
            if identifier == "B7":
                osc_router.send_message("/ambijockey/moc/B/1/1/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/1/", value)
                sendData("L,14,255,255,255")
            if identifier == "B8":
                osc_router.send_message("/ambijockey/moc/B/4/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/2/", value)
                sendData("L,2,255,255,255")
            if identifier == "B9":
                osc_router.send_message("/ambijockey/moc/B/3/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/2/", value)
                sendData("L,5,255,255,255")
            if identifier == "B10":
                osc_router.send_message("/ambijockey/moc/B/2/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/2/", value)
                sendData("L,10,255,255,255")
            if identifier == "B11":
                osc_router.send_message("/ambijockey/moc/B/1/2/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/2/", value)
                sendData("L,13,255,255,255")
            if identifier == "B12":
                osc_router.send_message("/ambijockey/moc/B/4/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/4/3/", value)
                sendData("L,3,255,255,255")
            if identifier == "B13":
                osc_router.send_message("/ambijockey/moc/B/3/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/3/3/", value)
                sendData("L,4,255,255,255")
            if identifier == "B14":
                osc_router.send_message("/ambijockey/moc/B/2/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/2/3/", value)
                sendData("L,11,255,255,255")
            if identifier == "B15":
                osc_router.send_message("/ambijockey/moc/B/1/3/", value)
                osc_gui.send_message("/ambijockey/moc/B/1/3/", value)
                sendData("L,12,255,255,255")

        time.sleep(0.001)
