# A³ Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# A³ Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with A³ Core.  If not, see <https://www.gnu.org/licenses/>.

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

OSC_PORT_CORE: int = 9000

FX_INDEX_HIPASS: int = 3
FX_INDEX_LOPASS: int = 4


# OSC clients
osc_mic = SimpleUDPClient('192.168.43.51', 7771)
osc_moc = SimpleUDPClient('192.168.43.52', 8700)
osc_reaper = SimpleUDPClient('127.0.0.1', 9001)

udp_clients_iem = tuple(SimpleUDPClient('127.0.0.1', 1337 + index)
                        for index in range(4))


@dataclass
class MasterInfo:
    track_masterbus: int = 1
    track_mainmixbus: int = 16
    track_booth: int = 5
    track_phones: int = 9
    track_reverb_aux_nr: int = 11

    class FXMode(Enum):
        LOW_PASS = 0
        HIGH_PASS = 1
    fx_mode: FXMode = FXMode.LOW_PASS


master_info = MasterInfo()


@dataclass
class ChannelInfo:
    track_input: int
    track_stereo: int
    track_channelbus: int
    track_pfl: int
    track_bformat: int

    toggle_fx: bool = False
    toggle_pfl: bool = False
    toggle_3d: bool = False
    position_xyz: tuple[int, int, int] = (0, 0, 0)

channel_infos = (
    # Channel 1
    ChannelInfo(
        track_input=20,
        track_stereo=19,
        track_bformat=18,
        track_channelbus=17,
        track_pfl=12,
    ),
    # Channel 2
    ChannelInfo(
        track_input=24,
        track_stereo=23,
        track_bformat=22,
        track_channelbus=21,
        track_pfl=13,
    ),
    # Channel 3
    ChannelInfo(
        track_input=28,
        track_stereo=27,
        track_bformat=26,
        track_channelbus=25,
        track_pfl=14,
    ),
    # Channel 4
    ChannelInfo(
        track_input=32,
        track_stereo=31,
        track_bformat=30,
        track_channelbus=29,
        track_pfl=15,
    ),
)


def set_filters() -> None:
    for channel_index in range(4):
        for fx_index, bypass_active in (
                (FX_INDEX_LOPASS,
                 (not channel_infos[channel_index].toggle_fx or
                  master_info.fx_mode == MasterInfo.FXMode.HIGH_PASS)),
                (FX_INDEX_HIPASS,
                 (not channel_infos[channel_index].toggle_fx or
                  master_info.fx_mode == MasterInfo.FXMode.LOW_PASS))):

            message = ("/track/"
                       f"{channel_infos[channel_index].track_input}"
                       f"/fx/{fx_index}/bypass")

            # osc_reaper expects 1 for "plugin active" and 0 for bypass
            osc_reaper.send_message(message, float(not bypass_active))


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
        if section == str(channel_index):
            param_handler_channel(channel_index, parameter, value)

    if section == "master":
        param_handler_master(parameter, value)

    elif section.startswith("fx"):
        param_handler_fx(section, parameter, value)


def osc_handler_channel(address: str,
                        *osc_arguments: List[Any]) -> None:

    #  mypy 0.920 reports a false positive, retest!
    value: float = float(osc_arguments[0])  # type: ignore
    assert type(value) == float

    print(address + " : " + str(value))

    words: List[str] = address.split("/")
    channel: str = words[2]
    parameter: str = words[3]

    channel_index = int(channel)
    track_input = channel_infos[channel_index].track_input

    if parameter == "gain":
        # ad hoc mapping function that smoothly approximates the
        # trial-and-error value mapping for prototype 0.1 with wrong
        # poti weighting in hardware.
        val = value ** (1/16) * 0.5
        # osc_reaper.send_message(f"/track/{track_input}/gain", val)
        osc_reaper.send_message(
            f"/track/{track_input}/fx/1/fxparam/1/value", val)

    elif parameter == "volume":
        val = np.interp(value, [0, 1], [0.01, 1])
        track_channelbus = channel_infos[channel_index].track_channelbus
        osc_reaper.send_message(f"/track/{track_channelbus}/volume", val)

    elif parameter == "eq":
        eq_parameter : str = words[4]
        if eq_parameter == "high":
            val = np.interp(value, [0, 1], [0.05, 0.50])
            osc_reaper.send_message(f"/track/{track_input}/fxeq/hishelf/gain", val)

        elif eq_parameter == "mid":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            osc_reaper.send_message(f"/track/{track_input}/fxeq/band/0/gain", val)

        elif eq_parameter == "low":
            val = np.interp(value, [0, 1], [0.01, 0.50])
            osc_reaper.send_message(f"/track/{track_input}/fxeq/loshelf/gain", val)

    elif parameter == "width":
        val = np.interp(value, [0, 1], [0.01, 179])
        udp_client = udp_clients_iem[channel_index]
        udp_client.send_message("/StereoEncoder/width", val)
        # print(str(value))

    elif parameter == "reverb":
        track_channelbus = channel_infos[channel_index].track_channelbus
        reverb_value = master_info.track_reverb_aux_nr
        osc_reaper.send_message(
            f"/track/{track_channelbus}/send/{reverb_value}/volume", value)

    elif parameter == "pfl" and value == 1:
        channel_infos[channel_index].toggle_pfl = (
            not channel_infos[channel_index].toggle_pfl)
        track_pfl = channel_infos[channel_index].track_pfl
        muted = not channel_infos[channel_index].toggle_pfl
        osc_reaper.send_message(f"/track/{track_pfl}/mute", float(muted))
        osc_mic.send_message(f"/channel/{channel_index}/led/pfl", float(muted))

    elif parameter == "fx" and value == 1:
        channel_infos[channel_index].toggle_fx = (
            not channel_infos[channel_index].toggle_fx)
        is_enabled = channel_infos[channel_index].toggle_fx
        osc_mic.send_message(f"/channel/{channel_index}/led/fx", float(is_enabled))
        set_filters()

    elif parameter == "3d" and value == 1:
        channel_infos[channel_index].toggle_3d = (
            not channel_infos[channel_index].toggle_3d)
        track_stereo = channel_infos[channel_index].track_stereo
        track_bformat = channel_infos[channel_index].track_bformat

        is_enabled = channel_infos[channel_index].toggle_3d
        osc_mic.send_message(f"/channel/{channel_index}/led/3d", float(is_enabled))
        osc_reaper.send_message(
            f"/track/{track_stereo}/mute", float(is_enabled))
        osc_reaper.send_message(
            f"/track/{track_bformat}/mute", float(not is_enabled))


def osc_handler_master(address: str,
                       *osc_arguments: List[Any]) -> None:

    #  mypy 0.920 reports a false positive, retest!
    value: float = float(osc_arguments[0])  # type: ignore
    assert type(value) == float

    print(address + " : " + str(value))

    words: List[str] = address.split("/")
    parameter: str = words[2]

    if parameter == "volume":
        val = np.interp(value, [0, 1], [0.01, 1])
        track = master_info.track_masterbus
        track_b = master_info.track_booth
        osc_reaper.send_message(f"/track/{track}/volume", val)
        osc_reaper.send_message(f"/track/{track_b}/volume", val)

    if parameter == "booth":
        val = np.interp(value, [0, 1], [0.01, 1])
        track = master_info.track_booth
        osc_reaper.send_message(f"/track/{track + 1}/volume", val)
        osc_reaper.send_message(f"/track/{track + 2}/volume", val)
        osc_reaper.send_message(f"/track/{track + 3}/volume", val)

    if parameter == "phones_mix":
        val = np.interp(value, [0, 1], [0.01, 1])
        track_mainmixbus = master_info.track_mainmixbus
        osc_reaper.send_message(f"/track/{track_mainmixbus}/volume", val)
        for channel_index in range(4):
            track_pfl = channel_infos[channel_index].track_pfl
            osc_reaper.send_message(f"/track/{track_pfl}/volume", 1 - val)

    if parameter == "phones_volume":
        val = np.interp(value, [0, 1], [0.01, 1])
        track_phones = master_info.track_phones
        osc_reaper.send_message(f"/track/{track_phones}/volume", val)


def osc_handler_fx(address: str,
                   *osc_arguments: List[Any]) -> None:

    value = osc_arguments[0]

    print(address + " : " + str(value))

    words: List[str] = address.split("/")
    parameter: str = words[2]

    if parameter == "mode":
        high_pass = value == "high_pass"
        master_info.fx_mode = MasterInfo.FXMode.HIGH_PASS if high_pass else MasterInfo.FXMode.LOW_PASS
        osc_mic.send_message("/fx/led", "high_pass" if high_pass else "low_pass")
        set_filters()

    elif parameter == "frequency":
        for channel_index in range(4):
            track_input = channel_infos[channel_index].track_input
            osc_reaper.send_message(
                f"/track/{track_input}"  # Hi-Pass Freq
                f"/fx/{FX_INDEX_HIPASS}/fxparam/7/value", float(value))
            osc_reaper.send_message(
                f"/track/{track_input}"  # Lo-Pass Freq
                f"/fx/{FX_INDEX_LOPASS}/fxparam/7/value", float(value))

    elif parameter == "resonance":
        val = np.interp(float(value), [0, 1], [0, 0.8])
        for channel_index in range(4):
            track_input = channel_infos[channel_index].track_input
            osc_reaper.send_message(
                f"/track/{track_input}"  # Hi-pass Resonance
                f"/fx/{FX_INDEX_HIPASS}/fxparam/6/value", val)
            osc_reaper.send_message(
                f"/track/{track_input}"  # Lo-Pass Resonance
                f"/fx/{FX_INDEX_LOPASS}/fxparam/6/value", val)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port", type=int,
                        default=OSC_PORT_CORE, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()

    dispatcher.map("/channel/*", osc_handler_channel)
    dispatcher.map("/master/*", osc_handler_master)
    dispatcher.map("/fx/*", osc_handler_fx)

    # # Motion-Controller
    # # dispatcher.map("/CoordinateConverter/*", iemToCtrlMotion_handler)
    # # dispatcher.map("/moc/channel/*", ctrlMotionToIem_handler)
    # # dispatcher.map("/moc/channel/*", ctrlMotionToIem_handler)

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
#     osc_mic.send_message(f"/track/{section}/vu", val)
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
#             osc_reaper.send_message("/track/" + dj2_in + "/fx/2/fxparam/1/value",
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
#             osc_reaper.send_message("/track/" + dj3_in + "/fx/2/fxparam/1/value",
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
#             osc_reaper.send_message("/track/" + dj4_in + "/fx/2/fxparam/1/value",
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
#             osc_moc.send_message(
#                 "/moc/channel/1/pos/xyz", val_send_ch1_xyz)

#         if param == "radius":
#             osc_moc.send_message(
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
#             osc_moc.send_message(
#                 "/moc/channel/2/pos/xyz", val_send_ch2_xyz)

#         if param == "radius":
#             osc_moc.send_message(
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
#             osc_moc.send_message(
#                 "/moc/channel/3/pos/xyz", val_send_ch3_xyz)

#         if param == "radius":
#             osc_moc.send_message(
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
#             osc_moc.send_message(
#                 "/moc/channel/4/pos/xyz", val_send_ch4_xyz)

#         if param == "radius":
#             osc_moc.send_message(
#                 "/ctrlMotion/track/4/width", osc_arguments[0])


