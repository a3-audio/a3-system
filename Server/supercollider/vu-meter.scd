// This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
// © Copyright 2021-2022 Raphael Eismann

s.options.numInputBusChannels  = 12;
s.options.numOutputBusChannels = 2;

s.options.memSize = 65536;
s.options.numBuffers = 4096;

s.boot;

~mic = NetAddr.new("192.168.43.51", 7771);    // create the NetAddr

s.waitForBoot({

//~mic.sendMsg("/vu_1-16", "peak, rms");

{SendPeakRMS.ar(In.ar(2, 1), 10, 3, "/reply0")}.play;
{SendPeakRMS.ar(In.ar(3, 1), 10, 3, "/reply1")}.play;
{SendPeakRMS.ar(In.ar(4, 1), 10, 3, "/reply2")}.play;
{SendPeakRMS.ar(In.ar(5, 1), 10, 3, "/reply3")}.play;
{SendPeakRMS.ar(In.ar(6, 1), 10, 5, "/reply4")}.play;
{SendPeakRMS.ar(In.ar(7, 1), 10, 5, "/reply5")}.play;
{SendPeakRMS.ar(In.ar(8, 1), 10, 5, "/reply6")}.play;
{SendPeakRMS.ar(In.ar(9, 1), 10, 5, "/reply7")}.play;
{SendPeakRMS.ar(In.ar(10, 1), 10, 5, "/reply8")}.play;
{SendPeakRMS.ar(In.ar(11, 1), 10, 5, "/reply9")}.play;
{SendPeakRMS.ar(In.ar(12, 1), 10, 5, "/reply10")}.play;
{SendPeakRMS.ar(In.ar(13, 1), 10, 5, "/reply11")}.play;

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

