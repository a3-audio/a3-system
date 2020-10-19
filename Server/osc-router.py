#!/usr/bin/python3
"""
Das ist ein tool umd unseremn server nach ausen eine konsistent OSC Adressierung zu geben.
@TODO wir mussen uns uns noch malüber die OSC-Adressen convention unter halten
Vorschlag jendrik:
template: /AmbiJocky/CH#/{contoler}/{funktion}/.../{args}
exampel: /AmbiJocky/CH1/Mixer/EQ/MID/[0-1]

Alle von ausen eingehenden und ausgehenden Volias sind Sollen Normaliesiert sein
"""

import argparse
import math
import numpy
from typing import List, Any
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

client = SimpleUDPClient('127.0.0.1', 9001)

### Mixer-Contoler
def poti_handler(address: str,
                 *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[2]
    poti = words[4]

    value = osc_arguments[0]
    print(track + "." + poti + " : " + str(value))

    if track == "1":
        if poti == "1":
            client.send_message("/track/15/fxeq/hishelf/freq", value)
        if poti == "2":
            ph_vol = numpy.interp(value,[0,1],[0,0.50])
            client.send_message("/track/15/fxeq/hishelf/gain", ph_vol)
        if poti == "3":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/15/fxeq/band/0/gain", ph_vol)
        if poti == "4":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/15/fxeq/loshelf/gain", ph_vol)
        if poti == "5":
            client.send_message("/track/14/volume", value)
    elif track == "2":
        if poti == "1":
            client.send_message("/track/21/fxeq/hishelf/freq", value)
        if poti == "2":
            ph_vol = numpy.interp(value,[0,1],[0,0.50])
            client.send_message("/track/21/fxeq/hishelf/gain", ph_vol)
        if poti == "3":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/21/fxeq/band/0/gain", ph_vol)
        if poti == "4":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/21/fxeq/loshelf/gain", ph_vol)
        if poti == "5":
            client.send_message("/track/20/volume", value)
    elif track == "3":
        if poti == "1":
            client.send_message("/track/27/fxeq/hishelf/freq", value)
        if poti == "2":
            ph_vol = numpy.interp(value,[0,1],[0,0.50])
            client.send_message("/track/27/fxeq/hishelf/gain", ph_vol)
        if poti == "3":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/27/fxeq/band/0/gain", ph_vol)
        if poti == "4":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/27/fxeq/loshelf/gain", ph_vol)
        if poti == "5":
            client.send_message("/track/26/volume", value)
    elif track == "4":
        if poti == "1":
            client.send_message("/track/33/fxeq/hishelf/freq", value)
        if poti == "2":
            ph_vol = numpy.interp(value,[0,1],[0,0.50])
            client.send_message("/track/33/fxeq/hishelf/gain", ph_vol)
        if poti == "3":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/33/fxeq/band/0/gain", ph_vol)
        if poti == "4":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.50])
            client.send_message("/track/33/fxeq/loshelf/gain", ph_vol)
        if poti == "5":
            client.send_message("/track/32/volume", value)
    elif  track == "5":
        if poti == "1":
            client.send_message("/master/volume", value)
        if poti == "2":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.5])
            client.send_message("/track/7/fxeq/hishelf/gain", ph_vol)
        if poti == "3":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.5])
            client.send_message("/track/7/fxeq/band/0/gain", ph_vol)
        if poti == "4":
            ph_vol = numpy.interp(value,[0,1],[0.01,0.5])
            client.send_message("/track/7/fxeq/loshelf/gain", ph_vol)

def button_handler(address: str,
                   *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    button = words[2]

    value = osc_arguments[0]
    if button == "1":
        client.send_message("/track/2/volume", 0)
        client.send_message("/track/18/send/1/volume", 1) #dj1 m/s
        client.send_message("/track/19/send/1/volume", 1) #dj1 b-format
        client.send_message("/track/24/send/1/volume", 0) #dj2 ..
        client.send_message("/track/25/send/1/volume", 0) #..
        client.send_message("/track/30/send/1/volume", 0)
        client.send_message("/track/31/send/1/volume", 0)
        client.send_message("/track/36/send/1/volume", 0)
        client.send_message("/track/37/send/1/volume", 0)

    if button == "2":
        client.send_message("/track/2/volume", 0)
        client.send_message("/track/18/send/1/volume", 0) #dj1 m/s
        client.send_message("/track/19/send/1/volume", 0) #dj1 b-format
        client.send_message("/track/24/send/1/volume", 1) #dj2 ..
        client.send_message("/track/25/send/1/volume", 1) #..
        client.send_message("/track/30/send/1/volume", 0)
        client.send_message("/track/31/send/1/volume", 0)
        client.send_message("/track/36/send/1/volume", 0)
        client.send_message("/track/37/send/1/volume", 0)

    if button == "3":
        client.send_message("/track/2/volume", 0)
        client.send_message("/track/18/send/1/volume", 0) #dj1 m/s
        client.send_message("/track/19/send/1/volume", 0) #dj1 b-format
        client.send_message("/track/24/send/1/volume", 0) #dj2 ..
        client.send_message("/track/25/send/1/volume", 0) #..
        client.send_message("/track/30/send/1/volume", 1)
        client.send_message("/track/31/send/1/volume", 1)
        client.send_message("/track/36/send/1/volume", 0)
        client.send_message("/track/37/send/1/volume", 0)

    if button == "4":
        client.send_message("/track/2/volume", 0)
        client.send_message("/track/18/send/1/volume", 0) #dj1 m/s
        client.send_message("/track/19/send/1/volume", 0) #dj1 b-format
        client.send_message("/track/24/send/1/volume", 0) #dj2 ..
        client.send_message("/track/25/send/1/volume", 0) #..
        client.send_message("/track/30/send/1/volume", 0)
        client.send_message("/track/31/send/1/volume", 0)
        client.send_message("/track/36/send/1/volume", 1)
        client.send_message("/track/37/send/1/volume", 1)

    if button == "5":
        client.send_message("/track/2/volume", 1)
        client.send_message("/track/18/send/1/volume", 0)
        client.send_message("/track/19/send/1/volume", 0)
        client.send_message("/track/24/send/1/volume", 0)
        client.send_message("/track/25/send/1/volume", 0)
        client.send_message("/track/30/send/1/volume", 0)
        client.send_message("/track/31/send/1/volume", 0)
        client.send_message("/track/36/send/1/volume", 0)
        client.send_message("/track/37/send/1/volume", 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=9000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #  dispatcher.map("/track/*", print)
    dispatcher.map("/track/*", poti_handler)
    dispatcher.map("/button/*", button_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

