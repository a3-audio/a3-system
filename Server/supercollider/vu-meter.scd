// This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
// © Copyright 2021 Raphael Eismann 

s.options.numInputBusChannels  = 12;
s.options.numOutputBusChannels = 2;

s.options.memSize = 65536;
s.options.numBuffers = 4096;

s.boot;

~b = NetAddr.new("192.168.43.51", 7771);    // create the NetAddr
~c = NetAddr.new("192.168.43.101", 1999);    // create the NetAddr

s.waitForBoot({

//~b.sendMsg("/vu_1-16", "peak, rms");

{SendPeakRMS.ar(In.ar(2, 1), 10, 3, "/reply01")}.play;
{SendPeakRMS.ar(In.ar(3, 1), 10, 3, "/reply02")}.play;
{SendPeakRMS.ar(In.ar(4, 1), 10, 3, "/reply03")}.play;
{SendPeakRMS.ar(In.ar(5, 1), 10, 3, "/reply04")}.play;
{SendPeakRMS.ar(In.ar(6, 1), 10, 5, "/reply05")}.play;
{SendPeakRMS.ar(In.ar(7, 1), 10, 5, "/reply06")}.play;
{SendPeakRMS.ar(In.ar(8, 1), 10, 5, "/reply07")}.play;
{SendPeakRMS.ar(In.ar(9, 1), 10, 5, "/reply08")}.play;
{SendPeakRMS.ar(In.ar(10, 1), 10, 5, "/reply09")}.play;
{SendPeakRMS.ar(In.ar(11, 1), 10, 5, "/reply10")}.play;
{SendPeakRMS.ar(In.ar(12, 1), 10, 5, "/reply11")}.play;
{SendPeakRMS.ar(In.ar(13, 1), 10, 5, "/reply12")}.play;

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

//OSCFunc({ |msg| ~c.sendMsg("/vu/01", msg[3], msg[4]);}, '/reply01');
//OSCFunc({ |msg| ~c.sendMsg("/vu/02", msg[3], msg[4]);}, '/reply02');
//OSCFunc({ |msg| ~c.sendMsg("/vu/03", msg[3], msg[4]);}, '/reply03');
//OSCFunc({ |msg| ~c.sendMsg("/vu/04", msg[3], msg[4]);}, '/reply04');
//OSCFunc({ |msg| ~c.sendMsg("/vu/05", msg[3], msg[4]);}, '/reply05');
//OSCFunc({ |msg| ~c.sendMsg("/vu/06", msg[3], msg[4]);}, '/reply06');
//OSCFunc({ |msg| ~c.sendMsg("/vu/07", msg[3], msg[4]);}, '/reply07');
//OSCFunc({ |msg| ~c.sendMsg("/vu/08", msg[3], msg[4]);}, '/reply08');
//OSCFunc({ |msg| ~c.sendMsg("/vu/09", msg[3], msg[4]);}, '/reply09');
//OSCFunc({ |msg| ~c.sendMsg("/vu/10", msg[3], msg[4]);}, '/reply10');
//OSCFunc({ |msg| ~c.sendMsg("/vu/11", msg[3], msg[4]);}, '/reply11');
//OSCFunc({ |msg| ~c.sendMsg("/vu/12", msg[3], msg[4]);}, '/reply12');
//s.meter;
});

