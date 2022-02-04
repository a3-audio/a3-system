# This file is part of A³Pandemic.

# A³Pandemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# A³Pandemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with A³Pandemic.  If not, see <https://www.gnu.org/licenses/>.

# © Copyright 2021 Raphael Eismann, Patric Schmitz

"""
This version is a static hardcoded version of osc-router. It will
transform into more dynamic code with external configfiles for osc in-
and output mappings.  For now it takes OSC adresses, interpolates
values and sends them to destinations.
"""

import argparse
import numpy as np
# import re

from typing import List, Any

from enum import Enum
from dataclasses import dataclass

from pythonosc import dispatcher  # type: ignore
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient  # type: ignore

# OSC server config
OSC_ROUTER_PORT: int = 9000

FX_INDEX_HIPASS: int = 3
FX_INDEX_LOPASS: int = 4


# OSC clients
ctrl_mixer = SimpleUDPClient('192.168.43.51', 8500)
ctrl_motion = SimpleUDPClient('192.168.43.52', 8700)
reaper = SimpleUDPClient('127.0.0.1', 9001)

udp_clients_iem = tuple(SimpleUDPClient('127.0.0.1', 1337 + index)
                        for index in range(4))


@dataclass
class MasterInfo:
    track_masterbus: int = 1
    track_mainmixbus: int = 12
    track_booth: int = 100
    track_phones: int = 5

    class FXMode(Enum):
        LOW_PASS = 0
        HIGH_PASS = 1
    fx_mode: FXMode = FXMode.LOW_PASS


master_info = MasterInfo()


@dataclass
class ChannelInfo:
    track_input: int
    track_stereo: int
    track_3d: int
    track_channelbus: int
    track_pfl: int

    fx_enabled: bool = False
    pfl_enabled: bool = False
    position_xyz: tuple[int, int, int] = (0, 0, 0)


channel_infos = (
    # Channel 1
    ChannelInfo(
        track_input=14,
        track_stereo=15,
        track_3d=16,
        track_channelbus=13,
        track_pfl=8,
    ),
    # Channel 2
    ChannelInfo(
        track_input=18,
        track_stereo=19,
        track_3d=20,
        track_channelbus=17,
        track_pfl=9,
    ),
    # Channel 3
    ChannelInfo(
        track_input=22,
        track_stereo=23,
        track_3d=24,
        track_channelbus=21,
        track_pfl=10,
    ),
    # Channel 4
    ChannelInfo(
        track_input=26,
        track_stereo=27,
        track_3d=28,
        track_channelbus=25,
        track_pfl=11,
    ),
)


def set_filters() -> None:
    for channel_index in range(4):
        for fx_index, bypass_active in (
                (FX_INDEX_LOPASS,
                 (not channel_infos[channel_index].fx_enabled or
                  master_info.fx_mode == MasterInfo.FXMode.HIGH_PASS)),
                (FX_INDEX_HIPASS,
                 (not channel_infos[channel_index].fx_enabled or
                  master_info.fx_mode == MasterInfo.FXMode.LOW_PASS))):

            message = ("/track/"
                       f"{channel_infos[channel_index].track_input}"
                       f"/fx/{fx_index}/bypass")

            # reaper expects 1 for "plugin active" and 0 for bypass
            reaper.send_message(message, float(not bypass_active))


def param_handler_channel(channel_index: int, parameter: str,
                          value: float) -> None:

    track_input = channel_infos[channel_index].track_input

    if parameter == "gain":
        # ad hoc mapping function that smoothly approximates the
        # trial-and-error value mapping for prototype 0.1 with wrong
        # poti weighting in hardware.
        val = value ** (1/16) * 0.5
        # reaper.send_message(f"/track/{track_input}/gain", val)
        reaper.send_message(
            f"/track/{track_input}/fx/1/fxparam/1/value", val)

    elif parameter == "hi":
        val = np.interp(value, [0, 1], [0.05, 0.50])
        reaper.send_message(f"/track/{track_input}/fxeq/hishelf/gain", val)

    elif parameter == "mid":
        val = np.interp(value, [0, 1], [0.01, 0.50])
        reaper.send_message(f"/track/{track_input}/fxeq/band/0/gain", val)

    elif parameter == "lo":
        val = np.interp(value, [0, 1], [0.01, 0.50])
        reaper.send_message(f"/track/{track_input}/fxeq/loshelf/gain", val)

    elif parameter == "volume":
        val = np.interp(value, [0, 1], [0.01, 1])
        track_channelbus = channel_infos[channel_index].track_channelbus
        reaper.send_message(f"/track/{track_channelbus}/volume", val)

    elif parameter == "width":
        udp_client = udp_clients_iem[channel_index]
        udp_client.send_message("/StereoEncoder/width", value)
        # print(str(value))

    elif parameter == "side":
        reaper.send_message(
            f"/track/{track_input}/fx/2/fxparam/1/value", value)


def param_handler_master(parameter: str, value: float) -> None:

    if parameter == "volume":
        val = np.interp(value, [0, 1], [0.01, 1])
        track = master_info.track_masterbus
        reaper.send_message(f"/track/{track}/volume", val)

    if parameter == "booth":
        val = np.interp(value, [0, 1], [0.01, 1])
        track = master_info.track_booth
        reaper.send_message(f"/track/{track}/volume", val)

    if parameter == "phMix":
        val = np.interp(value, [0, 1], [0.01, 1])
        track_mainmixbus = master_info.track_mainmixbus
        reaper.send_message(f"/track/{track_mainmixbus}/volume", val)
        for channel_index in range(4):
            track_pfl = channel_infos[channel_index].track_pfl
            reaper.send_message(f"/track/{track_pfl}/volume", 1 - val)

    if parameter == "phVol":
        val = np.interp(value, [0, 1], [0.01, 1])
        track_phones = master_info.track_phones
        reaper.send_message(f"/track/{track_phones}/volume", val)


def param_handler_fx(section: str, parameter: str, value: float) -> None:

    if section == "fxmode" and value == 1:
        if parameter == "hipass":
            master_info.fx_mode = MasterInfo.FXMode.HIGH_PASS
        elif parameter == "lopass":
            master_info.fx_mode = MasterInfo.FXMode.LOW_PASS
        set_filters()

    elif section == "fxparm":
        if parameter == "fxfreq":
            for channel_index in range(4):
                track_input = channel_infos[channel_index].track_input
                reaper.send_message(
                    f"/track/{track_input}"  # Hi-Pass Freq
                    f"/fx/{FX_INDEX_HIPASS}/fxparam/7/value", value)
                reaper.send_message(
                    f"/track/{track_input}"  # Lo-Pass Freq
                    f"/fx/{FX_INDEX_LOPASS}/fxparam/2/value", value)

        if parameter == "fxres":
            val = np.interp(value, [0, 1], [0, 0.8])
            for channel_index in range(4):
                track_input = channel_infos[channel_index].track_input
                reaper.send_message(
                    f"/track/{track_input}"  # Hi-pass Resonance
                    f"/fx/{FX_INDEX_HIPASS}/fxparam/8/value", val)
                reaper.send_message(
                    f"/track/{track_input}"  # Lo-Pass Resonance
                    f"/fx/{FX_INDEX_LOPASS}/fxparam/3/value", val)


def param_handler(address: str,
                  *osc_arguments: List[Any]) -> None:

    words: List[str] = address.split("/")
    section: str = words[3]
    parameter: str = words[4]

    #  mypy 0.920 reports a false positive, retest!
    value: float = float(osc_arguments[0])  # type: ignore
    assert type(value) == float
    print(section + "." + parameter + " : " + str(value))

    for channel_index in range(4):
        if section == str(channel_index+1):
            param_handler_channel(channel_index, parameter, value)

    if section == "master":
        param_handler_master(parameter, value)

    elif section.startswith("fx"):
        param_handler_fx(section, parameter, value)


def button_handler(address: str,
                   *osc_arguments: List[Any]) -> None:

    words: List[str] = address.split("/")
    section: str = words[3]
    parameter: str = words[4]

    #  mypy 0.920 reports a false positive, retest!
    value: float = float(osc_arguments[0])  # type: ignore
    assert type(value) == float

    for channel_index in range(4):
        if section == str(channel_index+1):
            if parameter == "pfl":
                channel_infos[channel_index].pfl_enabled = (
                    not channel_infos[channel_index].pfl_enabled)
                track_pfl = channel_infos[channel_index].track_pfl
                muted = not channel_infos[channel_index].pfl_enabled
                reaper.send_message(f"/track/{track_pfl}/mute", float(muted))

            elif parameter == "fx":
                channel_infos[channel_index].fx_enabled = bool(value)
                set_filters()

            elif parameter == "3d":
                track_stereo = channel_infos[channel_index].track_stereo
                track_3d = channel_infos[channel_index].track_3d
                reaper.send_message(
                    f"/track/{track_stereo}/mute", float(value))
                reaper.send_message(
                    f"/track/{track_3d}/mute", float(1 - value))


def moc_poti_handler(address: str, *osc_arguments: List[Any]) -> None:

    words = address.split("/")
    section = words[3]
    parameter = words[4]

    #  mypy 0.920 reports a false positive, retest!
    value: float = float(osc_arguments[0])  # type: ignore
    assert type(value) == float
    # print(track + "." + poti + " : " + str(value))

    for channel_index in range(4):
        if section == str(channel_index+1):
            if parameter == "width":
                val = np.interp(value, [0, 1], [30, 145])
                udp_client = udp_clients_iem[channel_index]
                udp_client.send_message("/StereoEncoder/width", val)
                # print(value)
            if parameter == "side":
                val = np.interp(value, [0, 1], [0.5, 0.65])
                track_input = channel_infos[channel_index].track_input
                reaper.send_message(
                    f"/track/{track_input}/fx/2/fxparam/1/value", val)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int,
                        default=OSC_ROUTER_PORT, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #  dispatcher.map("/track/*", print)

    # Mixer-Controller
    dispatcher.map("/mic/channel/*", param_handler)
    dispatcher.map("/mic/channel/*", button_handler)
    # dispatcher.map("/reaper/vu/*", vu_handler)

    # Motion-Controller
    dispatcher.map("/moc/channel/*", moc_poti_handler)
    # dispatcher.map("/CoordinateConverter/*", iemToCtrlMotion_handler)
    # dispatcher.map("/moc/channel/*", ctrlMotionToIem_handler)
    # dispatcher.map("/moc/channel/*", ctrlMotionToIem_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


# def vu_handler(address: str, *osc_arguments: List[Any]) -> None:

#     words = address.split("/")
#     section: str = words[3]

#     #  mypy 0.920 reports a false positive, retest!
#     value: float = float(osc_arguments[0])  # type: ignore
#     assert type(value) == float

#     fp = [0, 0.05, 0.10, 0.15, 0.20, 0.40, 0.60, 0.65, 0.75, 0.90]
#     xp = [0, 0.25, 0.30, 0.37, 0.43, 0.50, 0.55, 0.58, 0.60, 0.64]
#     val = np.interp(value, xp, fp)
#     ctrl_mixer.send_message(f"/track/{section}/vu", val)
#     # print(str(value))


# def ctrlMotionToIem_handler(address: str,
#                             *osc_arguments: List[Any]) -> None:
#     words = address.split("/")
#     track = words[3]
#     param = words[4]

#     # print(words)
#     # value = osc_arguments
#     # print("/ctrlMotion/track/" + track + "/" + param + "/ : " + str(value))

#     if track == "1":
#         if param == "xyz":
#             iem_1.send_message("/CoordinateConverter/xPos",
#                                np.interp(osc_arguments[1], [0, 1], [-1, 1]))
#             iem_1.send_message("/CoordinateConverter/yPos",
#                                np.interp(osc_arguments[0], [0, 1], [1, -1]))

#     if track == "2":
#         match_xyz = re.match(param, "xyz")
#         if match_xyz:
#             iem_2.send_message("/CoordinateConverter/xPos",
#                                np.interp(osc_arguments[1], [0, 1], [-1, 1]))
#             iem_2.send_message("/CoordinateConverter/yPos",
#                                np.interp(osc_arguments[0], [0, 1], [1, -1]))
#             # iem_2.send_message("/CoordinateConverter/zPos", osc_arguments[2])
#         if param == "width":
#             iem_2.send_message("/CoordinateConverter/radius", osc_arguments[0])
#         if param == "side":
#             reaper.send_message("/track/" + dj2_in + "/fx/2/fxparam/1/value",
#                                 osc_arguments[0])

#     if track == "3":
#         match_xyz = re.match(param, "xyz")
#         if match_xyz:
#             iem_3.send_message("/CoordinateConverter/xPos",
#                                np.interp(osc_arguments[1], [0, 1], [-1, 1]))
#             iem_3.send_message("/CoordinateConverter/yPos",
#                                np.interp(osc_arguments[0], [0, 1], [1, -1]))
#             # iem_3.send_message("/CoordinateConverter/zPos", osc_arguments[2])
#         if param == "width":
#             iem_3.send_message("/CoordinateConverter/radius", osc_arguments[0])
#         if param == "side":
#             reaper.send_message("/track/" + dj3_in + "/fx/2/fxparam/1/value",
#                                 osc_arguments[0])

#     if track == "4":
#         match_xyz = re.match(param, "xyz")
#         if match_xyz:
#             iem_4.send_message("/CoordinateConverter/xPos",
#                                np.interp(osc_arguments[1], [0, 1], [-1, 1]))
#             iem_4.send_message("/CoordinateConverter/yPos",
#                                np.interp(osc_arguments[0], [0, 1], [1, -1]))
#             # iem_4.send_message("/CoordinateConverter/zPos", osc_arguments[2])
#         if param == "width":
#             iem_4.send_message("/CoordinateConverter/radius", osc_arguments[0])
#         if param == "side":
#             reaper.send_message("/track/" + dj4_in + "/fx/2/fxparam/1/value",
#                                 osc_arguments[0])


# def iemToCtrlMotion_handler(address: str,
#                             *osc_arguments: List[Any]) -> None:
#     words = address.split("/")
#     track = words[1]
#     param = words[2]

#     print(words)
#     # value = osc_arguments[0]
#     # print("/CoordinateConverter/" + track + "/" + param + " : " + str(value))

#     if track == "1":
#         if (param == "xPos" or param == "yPos" or param == "yPos"):
#             if param == "xPos":
#                 val_send_ch1_xyz[1] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             if param == "yPos":
#                 val_send_ch1_xyz[0] = (np.interp(
#                     osc_arguments[0], [-1, 1], [1, 0]))
#             else:
#                 val_send_ch1_xyz[2] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             ctrl_motion.send_message(
#                 "/moc/channel/1/pos/xyz", val_send_ch1_xyz)

#         if param == "radius":
#             ctrl_motion.send_message(
#                 "/ctrlMotion/track/1/width", osc_arguments[0])

#     if track == "2":
#         if (param == "xPos" or param == "yPos" or param == "yPos"):
#             if param == "xPos":
#                 val_send_ch2_xyz[1] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             if param == "yPos":
#                 val_send_ch2_xyz[0] = (np.interp(
#                     osc_arguments[0], [-1, 1], [1, 0]))
#             else:
#                 val_send_ch2_xyz[2] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             ctrl_motion.send_message(
#                 "/moc/channel/2/pos/xyz", val_send_ch2_xyz)

#         if param == "radius":
#             ctrl_motion.send_message(
#                 "/ctrlMotion/track/2/width", osc_arguments[0])

#     if track == "3":
#         if (param == "xPos" or param == "yPos" or param == "yPos"):
#             if param == "xPos":
#                 val_send_ch3_xyz[1] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             if param == "yPos":
#                 val_send_ch3_xyz[0] = (np.interp(
#                     osc_arguments[0], [-1, 1], [1, 0]))
#             else:
#                 val_send_ch3_xyz[2] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             ctrl_motion.send_message(
#                 "/moc/channel/3/pos/xyz", val_send_ch3_xyz)

#         if param == "radius":
#             ctrl_motion.send_message(
#                 "/ctrlMotion/track/3/width", osc_arguments[0])

#     if track == "4":
#         if (param == "xPos" or param == "yPos" or param == "yPos"):
#             if param == "xPos":
#                 val_send_ch4_xyz[1] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             if param == "yPos":
#                 val_send_ch4_xyz[0] = (np.interp(
#                     osc_arguments[0], [-1, 1], [1, 0]))
#             else:
#                 val_send_ch4_xyz[2] = (np.interp(
#                     osc_arguments[0], [-1, 1], [0, 1]))
#             ctrl_motion.send_message(
#                 "/moc/channel/4/pos/xyz", val_send_ch4_xyz)

#         if param == "radius":
#             ctrl_motion.send_message(
#                 "/ctrlMotion/track/4/width", osc_arguments[0])


