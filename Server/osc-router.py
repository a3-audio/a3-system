"""
this version is just a steady hardcoded version of osc-router. It will
transform into more dynamic code with external configfiles for osc in-
and output mappings.

For now it takes OSC-Adresses, interpolates values and sends them to
destinations:

SOURCE                          >>  DESTINATION
----------------------------------------------------------------------
CONTROLLER_MIXER POTIS              REAPER
/track/1/1 (Channel 1 gain)     >>  /track/15/ie/gain
/track/1/2 (Channel 1 hi)       >>  /track/15/fxeq/hishelf/gain
/track/1/3 (Channel 1 mid)      >>  /track/15/fxeq/band/0/gain
/track/1/4 (Channel 1 low)      >>  /track/15/fxeq/loshelf/gain
/track/1/5 (Channel 1 volume)   >>  /track/14/volume

... same for track 2-4

CONTROLLER_MIXER POTIS              REAPER
/track/5/1 (Master volume)      >>  /master/volume
/track/5/2 (Master hi)          >>  /track/7/fxeq/hishelf/gain
/track/5/3 (Master mid)         >>  /track/7/fxeq/band/0/gain
/track/5/4 (Master low)         >>  /track/7/fxeq/loshelf/gain

CONTROLLER_MIXER BUTTONS            REAPER
/button/1 (Channel 1 pfl)       >>  turns vol 1 for stereo and binaural headphone send.
/button/2 (Channel 2 pfl)           Also it sets vol 0 for every other headphone send.
/button/3 (Channel 3 pfl)           TODO: send the value to Controller_Mixer /led/*
/button/4 (Channel 4 pfl)
/button/5 (Master pfl)

CONTROLLER_MOTION                   IEM COORDINATECONVERTER HOSTET BY REAPER
/track/1/xy                     >>  this osc data will be send by different oscClients
/track/2/xy                         to different ports
/track/3/xy
/track/4/xy

IEM COORDINATECONVERTER             CONTROLLER_MOTION
/CoordinateConverter/xPos       >>  osc data is send to different ports
/CoordinateConverter/yPos
... same for track 2-4

REAPER                              CONTROLLER_MIXER
/track/14/vu (VU-Meter)         >>  /vu/1
/track/20/vu (VU-Meter)         >>  /vu/2
/track/26/vu (VU-Meter)         >>  /vu/3
/track/32/vu (VU-Meter)         >>  /vu/4
/track/master/vu (VU-Meter)     >>  /vu/5
"""

import argparse
import math
import numpy
from typing import List, Any
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

# OSC-Server
OSC-Router-Port  = 9000
IEM-Port_1  = 8610
IEM-Port_2  = 8620
IEM-Port_3  = 8630
IEM-Port_4  = 8640

# OSC-Clients
ctrl_mixer  = SimpleUDPClient('192.168.43.139', 8500) # Set IP Adress
ctrl_motion = SimpleUDPClient('192.168.43.140', 8600) # Set IP Adress
reaper      = SimpleUDPClient('127.0.0.1', 9001)
iem_1       = SimpleUDPClient('127.0.0.1', 1337)
iem_2       = SimpleUDPClient('127.0.0.1', 1338)
iem_3       = SimpleUDPClient('127.0.0.1', 1339)
iem_4       = SimpleUDPClient('127.0.0.1', 1340)

def poti_handler(address: str,
                 *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[2]
    poti = words[4]

    value = osc_arguments[0]
    print(track + "." + poti + " : " + str(value))

    if track == "1":
        if poti == "1":
            reaper.send_message("/track/15/fxeq/hishelf/freq", value)
        if poti == "2":
            val = numpy.interp(value,[0,1],[0,0.50])
            reaper.send_message("/track/15/fxeq/hishelf/gain", val)
        if poti == "3":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/15/fxeq/band/0/gain", val)
        if poti == "4":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/15/fxeq/loshelf/gain", val)
        if poti == "5":
            reaper.send_message("/track/14/volume", value)
    elif track == "2":
        if poti == "1":
            reaper.send_message("/track/21/fxeq/hishelf/freq", value)
        if poti == "2":
            val = numpy.interp(value,[0,1],[0,0.50])
            reaper.send_message("/track/21/fxeq/hishelf/gain", val)
        if poti == "3":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/21/fxeq/band/0/gain", val)
        if poti == "4":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/21/fxeq/loshelf/gain", val)
        if poti == "5":
            reaper.send_message("/track/20/volume", value)
    elif track == "3":
        if poti == "1":
            reaper.send_message("/track/27/fxeq/hishelf/freq", value)
        if poti == "2":
            val = numpy.interp(value,[0,1],[0,0.50])
            reaper.send_message("/track/27/fxeq/hishelf/gain", val)
        if poti == "3":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/27/fxeq/band/0/gain", val)
        if poti == "4":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/27/fxeq/loshelf/gain", val)
        if poti == "5":
            reaper.send_message("/track/26/volume", value)
    elif track == "4":
        if poti == "1":
            reaper.send_message("/track/33/fxeq/hishelf/freq", value)
        if poti == "2":
            val = numpy.interp(value,[0,1],[0,0.50])
            reaper.send_message("/track/33/fxeq/hishelf/gain", val)
        if poti == "3":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/33/fxeq/band/0/gain", val)
        if poti == "4":
            val = numpy.interp(value,[0,1],[0.01,0.50])
            reaper.send_message("/track/33/fxeq/loshelf/gain", val)
        if poti == "5":
            reaper.send_message("/track/32/volume", value)
    elif  track == "5":
        if poti == "1":
            reaper.send_message("/master/volume", value)
        if poti == "2":
            val = numpy.interp(value,[0,1],[0.01,0.5])
            reaper.send_message("/track/7/fxeq/hishelf/gain", val)
        if poti == "3":
            val = numpy.interp(value,[0,1],[0.01,0.5])
            reaper.send_message("/track/7/fxeq/band/0/gain", val)
        if poti == "4":
            val = numpy.interp(value,[0,1],[0.01,0.5])
            reaper.send_message("/track/7/fxeq/loshelf/gain", val)

def button_handler(address: str,
                   *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    button = words[2]

    value = osc_arguments[0]
    if button == "1":
        reaper.send_message("/track/2/volume", 0)
        reaper.send_message("/track/18/send/1/volume", 1) #dj1 m/s
        reaper.send_message("/track/19/send/1/volume", 1) #dj1 b-format
        reaper.send_message("/track/24/send/1/volume", 0) #dj2 m/s
        reaper.send_message("/track/25/send/1/volume", 0) #..
        reaper.send_message("/track/30/send/1/volume", 0)
        reaper.send_message("/track/31/send/1/volume", 0)
        reaper.send_message("/track/36/send/1/volume", 0)
        reaper.send_message("/track/37/send/1/volume", 0)

    if button == "2":
        reaper.send_message("/track/2/volume", 0)
        reaper.send_message("/track/18/send/1/volume", 0) #dj1 m/s
        reaper.send_message("/track/19/send/1/volume", 0) #dj1 b-format
        reaper.send_message("/track/24/send/1/volume", 1) #dj2 ..
        reaper.send_message("/track/25/send/1/volume", 1) #..
        reaper.send_message("/track/30/send/1/volume", 0)
        reaper.send_message("/track/31/send/1/volume", 0)
        reaper.send_message("/track/36/send/1/volume", 0)
        reaper.send_message("/track/37/send/1/volume", 0)

    if button == "3":
        reaper.send_message("/track/2/volume", 0)
        reaper.send_message("/track/18/send/1/volume", 0) #dj1 m/s
        reaper.send_message("/track/19/send/1/volume", 0) #dj1 b-format
        reaper.send_message("/track/24/send/1/volume", 0) #dj2 ..
        reaper.send_message("/track/25/send/1/volume", 0) #..
        reaper.send_message("/track/30/send/1/volume", 1)
        reaper.send_message("/track/31/send/1/volume", 1)
        reaper.send_message("/track/36/send/1/volume", 0)
        reaper.send_message("/track/37/send/1/volume", 0)

    if button == "4":
        reaper.send_message("/track/2/volume", 0)
        reaper.send_message("/track/18/send/1/volume", 0) #dj1 m/s
        reaper.send_message("/track/19/send/1/volume", 0) #dj1 b-format
        reaper.send_message("/track/24/send/1/volume", 0) #dj2 ..
        reaper.send_message("/track/25/send/1/volume", 0) #..
        reaper.send_message("/track/30/send/1/volume", 0)
        reaper.send_message("/track/31/send/1/volume", 0)
        reaper.send_message("/track/36/send/1/volume", 1)
        reaper.send_message("/track/37/send/1/volume", 1)

    if button == "5":
        reaper.send_message("/track/2/volume", 1)
        reaper.send_message("/track/18/send/1/volume", 0)
        reaper.send_message("/track/19/send/1/volume", 0)
        reaper.send_message("/track/24/send/1/volume", 0)
        reaper.send_message("/track/25/send/1/volume", 0)
        reaper.send_message("/track/30/send/1/volume", 0)
        reaper.send_message("/track/31/send/1/volume", 0)
        reaper.send_message("/track/36/send/1/volume", 0)
        reaper.send_message("/track/37/send/1/volume", 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", "0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=OSC-Router-Port, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #  dispatcher.map("/track/*", print)
    dispatcher.map("/track/*", poti_handler)
    dispatcher.map("/button/*", button_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

