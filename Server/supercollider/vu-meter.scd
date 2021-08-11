# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
# © Copyright 2021 Raphael Eismann 

Server.supernova;
ServerOptions.new;
t = Server(\mic, NetAddr("127.0.0.1", 9001));
Server.local = Server.default;
t = Server.local.options; // Get the local server's options
t.numInputBusChannels = 12;
t.numOutputBusChannels = 2;
t.numAudioBusChannels = 2048 * 8;
t.blockSize = 64;
//t.numWireBufs = 1024 * ~hoaNumChannels;
t.memSize = 2048;
t.sampleRate = 44100;
s.boot;

~b = NetAddr.new("192.168.43.51", 7771);    // create the NetAddr

s.waitForBoot({

//~b.sendMsg("/vu_1-16", "peak, rms");


{SendPeakRMS.kr(In.ar(2, 1), 10, 3, "/reply01")}.play;
{SendPeakRMS.kr(In.ar(3, 1), 10, 3, "/reply02")}.play;
{SendPeakRMS.kr(In.ar(4, 1), 10, 3, "/reply03")}.play;
{SendPeakRMS.kr(In.ar(5, 1), 10, 3, "/reply04")}.play;
{SendPeakRMS.kr(In.ar(6, 1), 10, 3, "/reply05")}.play;
{SendPeakRMS.kr(In.ar(7, 1), 10, 3, "/reply06")}.play;
{SendPeakRMS.kr(In.ar(8, 1), 10, 3, "/reply07")}.play;
{SendPeakRMS.kr(In.ar(9, 1), 10, 3, "/reply08")}.play;
{SendPeakRMS.kr(In.ar(10, 1), 10, 3, "/reply09")}.play;
{SendPeakRMS.kr(In.ar(11, 1), 10, 3, "/reply10")}.play;
{SendPeakRMS.kr(In.ar(12, 1), 10, 3, "/reply11")}.play;
{SendPeakRMS.kr(In.ar(13, 1), 10, 3, "/reply12")}.play;

OSCFunc({ |msg| ~b.sendMsg("/vu/01", msg[3], msg[4]);}, '/reply01');
OSCFunc({ |msg| ~b.sendMsg("/vu/02", msg[3], msg[4]);}, '/reply02');
OSCFunc({ |msg| ~b.sendMsg("/vu/03", msg[3], msg[4]);}, '/reply03');
OSCFunc({ |msg| ~b.sendMsg("/vu/04", msg[3], msg[4]);}, '/reply04');
OSCFunc({ |msg| ~b.sendMsg("/vu/05", msg[3], msg[4]);}, '/reply05');
OSCFunc({ |msg| ~b.sendMsg("/vu/06", msg[3], msg[4]);}, '/reply06');
OSCFunc({ |msg| ~b.sendMsg("/vu/07", msg[3], msg[4]);}, '/reply07');
OSCFunc({ |msg| ~b.sendMsg("/vu/08", msg[3], msg[4]);}, '/reply08');
OSCFunc({ |msg| ~b.sendMsg("/vu/09", msg[3], msg[4]);}, '/reply09');
OSCFunc({ |msg| ~b.sendMsg("/vu/10", msg[3], msg[4]);}, '/reply10');
OSCFunc({ |msg| ~b.sendMsg("/vu/11", msg[3], msg[4]);}, '/reply11');
OSCFunc({ |msg| ~b.sendMsg("/vu/12", msg[3], msg[4]);}, '/reply12');

s.meter;
});

