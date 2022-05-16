# A³ Mix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# A³ Mix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with A³ Mix.  If not, see <https://www.gnu.org/licenses/>.

# © Copyright 2021 A³ Raphael Eismann 

# vu-meter script: osc in -> usb out

import argparse
import math
import re
from typing import List, Any
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient
import serial
import time

def sendData(data):
    ser = serial.Serial('/dev/ttyACM0', 115200)
    data += "\r\n"
    ser.write(data.encode())

# OSC-Server
oscRouterPort = 7771

def vu_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    vu = words[2]

    peak = osc_arguments[0]
    rms = osc_arguments[1]
    print(str(peak) + " - " + str(rms))

    if vu == "1":
        sendData("VU01," + str(peak) + "," + str(rms))
        #print("VU01," + str(peak) + "," + str(rms))
    if vu == "2":
        sendData("VU02," + str(peak) + "," + str(rms))
    if vu == "3":
        sendData("VU03," + str(peak) + "," + str(rms))
    if vu == "4":
        sendData("VU04," + str(peak) + "," + str(rms))
"""
    if vu == "3":
#        sendData("VU3")
        print("vu3," + str(peak) + "," + str(rms))
    if vu == "4":
#        sendData("VU4")
        print("vu4," + str(peak) + "," + str(rms))
    if vu == "5":
#        sendData("VU5")
        print("vu5," + str(peak) + "," + str(rms))
    if vu == "6":
#        sendData("VU6")
        print("vu6," + str(peak) + "," + str(rms))
    if vu == "7":
#        sendData("VU7")
        print("vu7," + str(peak) + "," + str(rms))
    if vu == "8":
#        sendData("VU8")
        print("vu8," + str(peak) + "," + str(rms))
    if vu == "9":
#        sendData("VU9")
        print("vu9," + str(peak) + "," + str(rms))
    if vu == "10":
#        sendData("VU10")
        print("vu10," + str(peak) + "," + str(rms))
    if vu == "11":
#        sendData("VU11")
        print("vu11," + str(peak) + "," + str(rms))
    if vu == "12":
#        sendData("VU12")
        print("vu12," + str(peak) + "," + str(rms))
    if vu == "13":
#        sendData("VU13")
        print("vu13," + str(peak) + "," + str(rms))
    if vu == "14":
#        sendData("VU14")
        print("vu14," + str(peak) + "," + str(rms))
    if vu == "15":
#        sendData("VU15")
        print("vu15," + str(peak) + "," + str(rms))
    if vu == "16":
#        sendData("VU16")
        print("vu16," + str(peak) + "," + str(rms))
   """

time.sleep(1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int,
                        default=oscRouterPort, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/vu/*", vu_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
