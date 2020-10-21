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
/button/1 (Channel 1 pfl)       >>  Sets vol=1 for stereo and binaural headphone send.
/button/2 (Channel 2 pfl)           Also it sets vol 0 for every other headphone send.
/button/3 (Channel 3 pfl)           send the value to Controller_Mixer /led/*
/button/4 (Channel 4 pfl)
/button/5 (Master pfl)

CONTROLLER_MOTION                   IEM COORDINATECONVERTER HOSTET BY REAPER
/ctrlMotion/track/1/xyz         >>  /CoordinateConverter/1/xPos
/ctrlMotion/track/2/xyz             /CoordinateConverter/1/yPos
/ctrlMotion/track/3/xyz             /CoordinateConverter/1/zPos
/ctrlMotion/track/4/xyz             ... same for 2-4

/ctrlMotion/track/1/width       >>  /CoordinateConverter/1/radius
/ctrlMotion/track/2/width       >>  /CoordinateConverter/2/radius
/ctrlMotion/track/3/width       >>  /CoordinateConverter/3/radius
/ctrlMotion/track/4/width       >>  /CoordinateConverter/4/radius

IEM COORDINATECONVERTER             CONTROLLER_MOTION
/CoordinateConverter/1/xPos     >>  /track/1/xy
/CoordinateConverter/1/yPos     >>  /track/1/xy
/CoordinateConverter/2/xPos     >>  /track/2/xy
/CoordinateConverter/2/yPos     >>  /track/2/xy
/CoordinateConverter/3/xPos     >>  /track/3/xy
/CoordinateConverter/3/yPos     >>  /track/3/xy
/CoordinateConverter/4/xPos     >>  /track/4/xy
/CoordinateConverter/4/yPos     >>  /track/4/xy

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
import re
from typing import List, Any
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

# OSC-Server
oscRouterPort  = 9000

# OSC-Clients
ctrl_mixer  = SimpleUDPClient('192.168.43.139', 8500) # Set IP Adress
ctrl_motion = SimpleUDPClient('192.168.43.140', 8600) # Set IP Adress
reaper      = SimpleUDPClient('127.0.0.1', 9001)
iem_1       = SimpleUDPClient('127.0.0.1', 1337)
iem_2       = SimpleUDPClient('127.0.0.1', 1338)
iem_3       = SimpleUDPClient('127.0.0.1', 1339)
iem_4       = SimpleUDPClient('127.0.0.1', 1340)

def ctrlMotionToIem_handler(address: str,
                 *osc_arguments: List[Any]) -> None:
    words = address.split("/")
    track = words[3]
    param = words[4]

    #value = osc_arguments[0]
    #print("/ctrlMotion/track/" + track + "/" + param + "/ : " + str(value))

    if track == "1":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_1.send_message("/CoordinateConverter/xPos", osc_arguments[0])
            iem_1.send_message("/CoordinateConverter/yPos", osc_arguments[1])
            iem_1.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        match_radius = re.match(param, "radius")
        if match_radius:
            iem_1.send_message("/CoordinateConverter/radius", osc_arguments[0])

    if track == "2":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_2.send_message("/CoordinateConverter/xPos", osc_arguments[0])
            iem_2.send_message("/CoordinateConverter/yPos", osc_arguments[1])
            iem_2.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        match_radius = re.match(param, "radius")
        if match_radius:
            iem_2.send_message("/CoordinateConverter/radius", osc_arguments[0])

    if track == "3":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_3.send_message("/CoordinateConverter/xPos", osc_arguments[0])
            iem_3.send_message("/CoordinateConverter/yPos", osc_arguments[1])
            iem_3.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        match_radius = re.match(param, "radius")
        if match_radius:
            iem_3.send_message("/CoordinateConverter/radius", osc_arguments[0])

    if track == "4":
        match_xyz = re.match(param, "xyz")
        if match_xyz:
            iem_4.send_message("/CoordinateConverter/xPos", osc_arguments[0])
            iem_4.send_message("/CoordinateConverter/yPos", osc_arguments[1])
            iem_4.send_message("/CoordinateConverter/zPos", osc_arguments[2])
        match_radius = re.match(param, "radius")
        if match_radius:
            iem_4.send_message("/CoordinateConverter/radius", osc_arguments[0])


def iemToCtrlMotion_handler(address: str,
                 *osc_arguments: List[Any])->None:
    words = address.split("/")
    track = words[2]
    param = words[3]

    value = osc_arguments[0]
    print("/CoordinateConverter/" + track + "/" + param + " : " + str(value))

    if track == "1":
        val_send=[]
        match_x = re.match(param, "xPos")
        if match_x:
           val_send.append(osc_arguments[0])
        match_y = re.match(param, "yPos")
        if match_y:
           val_send.append(osc_arguments[0])
        match_z = re.match(param, "zPos")
        if match_z:
           val_send.append(osc_arguments[0])
        ctrl_motion.send_message("/ctrlMotion/track/1/xyz", val_send)
        match_radius = re.match(param, "radius")
        if match_radius:
            ctrl_motion.send_message("/ctrlMotion/track/1/width", osc_arguments[0])

    if track == "2":
        val_send=[]
        match_x = re.match(param, "xPos")
        if match_x:
           val_send.append(osc_arguments[0])
        match_y = re.match(param, "yPos")
        if match_y:
           val_send.append(osc_arguments[0])
        match_z = re.match(param, "zPos")
        if match_z:
           val_send.append(osc_arguments[0])
        ctrl_motion.send_message("/ctrlMotion/track/2/xyz", val_send)
        match_radius = re.match(param, "radius")
        if match_radius:
            ctrl_motion.send_message("/ctrlMotion/track/2/width", osc_arguments[0])

    if track == "3":
        val_send=[]
        match_x = re.match(param, "xPos")
        if match_x:
           val_send.append(osc_arguments[0])
        match_y = re.match(param, "yPos")
        if match_y:
           val_send.append(osc_arguments[0])
        match_z = re.match(param, "zPos")
        if match_z:
           val_send.append(osc_arguments[0])
        ctrl_motion.send_message("/ctrlMotion/track/3/xyz", val_send)
        match_radius = re.match(param, "radius")
        if match_radius:
            ctrl_motion.send_message("/ctrlMotion/track/3/width", osc_arguments[0])

    if track == "4":
        val_send=[]
        match_x = re.match(param, "xPos")
        if match_x:
           val_send.append(osc_arguments[0])
        match_y = re.match(param, "yPos")
        if match_y:
           val_send.append(osc_arguments[0])
        match_z = re.match(param, "zPos")
        if match_z:
           val_send.append(osc_arguments[0])
        ctrl_motion.send_message("/ctrlMotion/track/4/xyz", val_send)
        match_radius = re.match(param, "radius")
        if match_radius:
            ctrl_motion.send_message("/ctrlMotion/track/4/width", osc_arguments[0])


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
        ctrl_mixer.send_message("/led/1", 1)
        ctrl_mixer.send_message("/led/2", 0)
        ctrl_mixer.send_message("/led/3", 0)
        ctrl_mixer.send_message("/led/4", 0)
        ctrl_mixer.send_message("/led/5", 0)

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
        ctrl_mixer.send_message("/led/1", 0)
        ctrl_mixer.send_message("/led/2", 1)
        ctrl_mixer.send_message("/led/3", 0)
        ctrl_mixer.send_message("/led/4", 0)
        ctrl_mixer.send_message("/led/5", 0)

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
        ctrl_mixer.send_message("/led/1", 0)
        ctrl_mixer.send_message("/led/2", 0)
        ctrl_mixer.send_message("/led/3", 1)
        ctrl_mixer.send_message("/led/4", 0)
        ctrl_mixer.send_message("/led/5", 0)

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
        ctrl_mixer.send_message("/led/1", 0)
        ctrl_mixer.send_message("/led/2", 0)
        ctrl_mixer.send_message("/led/3", 0)
        ctrl_mixer.send_message("/led/4", 1)
        ctrl_mixer.send_message("/led/5", 0)

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
        ctrl_mixer.send_message("/led/1", 0)
        ctrl_mixer.send_message("/led/2", 0)
        ctrl_mixer.send_message("/led/3", 0)
        ctrl_mixer.send_message("/led/4", 0)
        ctrl_mixer.send_message("/led/5", 1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=oscRouterPort, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #  dispatcher.map("/track/*", print)
    dispatcher.map("/track/*", poti_handler)
    dispatcher.map("/button/*", button_handler)
    dispatcher.map("/CoordinateConverter/*", iemToCtrlMotion_handler)
    dispatcher.map("/ctrlMotion/track/*", ctrlMotionToIem_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
