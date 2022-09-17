// A³ Core is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// A³ Core is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with A³ Core.  If not, see <https://www.gnu.org/licenses/>.

// © Copyright 2021 Raphael Eismann

s.options.numInputBusChannels  = 12;
s.options.numOutputBusChannels = 2;

s.options.memSize = 65536;
s.options.numBuffers = 4096;

s.boot;

~mic = NetAddr.new("192.168.43.51", 7771);    // create the NetAddr

s.waitForBoot({

//SendPeakRMS.ar(sig, replyRate: 20.0, peakLag: 3, cmdName: '/reply', replyID: -1)

{SendPeakRMS.ar(In.ar(2, 1), 20, 5, "/reply0")}.play;
{SendPeakRMS.ar(In.ar(3, 1), 20, 5, "/reply1")}.play;
{SendPeakRMS.ar(In.ar(4, 1), 20, 5, "/reply2")}.play;
{SendPeakRMS.ar(In.ar(5, 1), 20, 5, "/reply3")}.play;
{SendPeakRMS.ar(In.ar(6, 1), 20, 5, "/reply4")}.play;
{SendPeakRMS.ar(In.ar(7, 1), 20, 5, "/reply5")}.play;
{SendPeakRMS.ar(In.ar(8, 1), 20, 5, "/reply6")}.play;
{SendPeakRMS.ar(In.ar(9, 1), 20, 5, "/reply7")}.play;
{SendPeakRMS.ar(In.ar(10, 1), 20, 4, "/reply8")}.play;
{SendPeakRMS.ar(In.ar(11, 1), 20, 4, "/reply9")}.play;
{SendPeakRMS.ar(In.ar(12, 1), 20, 4, "/reply10")}.play;
{SendPeakRMS.ar(In.ar(13, 1), 20, 4, "/reply11")}.play;

//~mic.sendMsg("/vu_1-16", "peak, rms");

OSCFunc({ |msg| ~mic.sendMsg("/vu/0", msg[3], msg[4]);}, '/reply0');
OSCFunc({ |msg| ~mic.sendMsg("/vu/1", msg[3], msg[4]);}, '/reply1');
OSCFunc({ |msg| ~mic.sendMsg("/vu/2", msg[3], msg[4]);}, '/reply2');
OSCFunc({ |msg| ~mic.sendMsg("/vu/3", msg[3], msg[4]);}, '/reply3');
OSCFunc({ |msg| ~mic.sendMsg("/vu/4", msg[3], msg[4]);}, '/reply4');
OSCFunc({ |msg| ~mic.sendMsg("/vu/5", msg[3], msg[4]);}, '/reply5');
OSCFunc({ |msg| ~mic.sendMsg("/vu/6", msg[3], msg[4]);}, '/reply6');
OSCFunc({ |msg| ~mic.sendMsg("/vu/7", msg[3], msg[4]);}, '/reply7');
OSCFunc({ |msg| ~mic.sendMsg("/vu/8", msg[3], msg[4]);}, '/reply8');
OSCFunc({ |msg| ~mic.sendMsg("/vu/9", msg[3], msg[4]);}, '/reply9');
OSCFunc({ |msg| ~mic.sendMsg("/vu/10", msg[3], msg[4]);}, '/reply10');
OSCFunc({ |msg| ~mic.sendMsg("/vu/11", msg[3], msg[4]);}, '/reply11');
});

