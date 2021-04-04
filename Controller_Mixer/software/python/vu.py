""" vu-metering script: osc in -> usb out """

import argparse
import math
import re
from typing import List, Any
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

# OSC-Server
oscRouterPort = 7771

def vu_handler(address: str,
               *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    vu = words[2]

    value = osc_arguments[0]
#   print(str(value))

    if vu == "1":
#        sendData("VU1")
        print("vu 1 - " + str(value))
    if vu == "2":
#        sendData("VU2")
        print("vu 2 - " + str(value))
    if vu == "3":
#        sendData("VU3")
        print("vu 3 - " + str(value))
    if vu == "4":
#        sendData("VU4")
        print("vu 4 - " + str(value))
    if vu == "5":
#        sendData("VU5")
        print("vu 5 - " + str(value))
    if vu == "6":
#        sendData("VU6")
        print("vu 6 - " + str(value))
    if vu == "7":
#        sendData("VU7")
        print("vu 7 - " + str(value))
    if vu == "8":
#        sendData("VU8")
        print("vu 8 - " + str(value))
    if vu == "9":
#        sendData("VU9")
        print("vu 9 - " + str(value))
    if vu == "10":
#        sendData("VU10")
        print("vu 10 - " + str(value))
    if vu == "11":
#        sendData("VU11")
        print("vu 11 - " + str(value))
    if vu == "12":
#        sendData("VU12")
        print("vu 12 - " + str(value))
    if vu == "13":
#        sendData("VU13")
        print("vu 13 - " + str(value))
    if vu == "14":
#        sendData("VU14")
        print("vu 14 - " + str(value))
    if vu == "15":
#        sendData("VU15")
        print("vu 15 - " + str(value))
    if vu == "16":
#        sendData("VU16")
        print("vu 16 - " + str(value))


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
