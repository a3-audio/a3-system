(
Server.supernova;
ServerOptions.new;
t = Server(\mic, NetAddr("127.0.0.1", 9001));
Server.local = Server.default;
t = Server.local.options; // Get the local server's options
t.numInputBusChannels = 8;
t.numOutputBusChannels = 2;
t.numAudioBusChannels = 2048 * 8;
t.blockSize = 64;
//t.numWireBufs = 1024 * ~hoaNumChannels;
t.memSize = 2.pow(18);
t.sampleRate = 44100;
s.boot
)

s.plotTree;
s.meter;

~b = NetAddr.new("127.0.0.1", 7771);    // create the NetAddr
~b.sendMsg("/vu_1-16", "peak, rms");

(
{SendPeakRMS.kr(In.ar(2, 1) *9, 20, 3, "/reply1")}.play;
{SendPeakRMS.kr(In.ar(3, 1) *9, 20, 3, "/reply2")}.play;
{SendPeakRMS.kr(In.ar(4, 1) *9, 20, 3, "/reply3")}.play;
{SendPeakRMS.kr(In.ar(5, 1) *9, 20, 3, "/reply4")}.play;
{SendPeakRMS.kr(In.ar(6, 1) *32, 20, 3, "/reply5")}.play;
{SendPeakRMS.kr(In.ar(7, 1) *32, 20, 3, "/reply6")}.play;
{SendPeakRMS.kr(In.ar(8, 1) *32, 20, 3, "/reply7")}.play;
{SendPeakRMS.kr(In.ar(9, 1) *32, 20, 3, "/reply8")}.play;
{SendPeakRMS.kr(In.ar(10, 1) *32, 20, 3, "/reply9")}.play;
{SendPeakRMS.kr(In.ar(11, 1) *32, 20, 3, "/reply10")}.play;
{SendPeakRMS.kr(In.ar(12, 1) *32, 20, 3, "/reply11")}.play;
{SendPeakRMS.kr(In.ar(13, 1) *32, 20, 3, "/reply12")}.play;
)

(
OSCFunc({ |msg| ~b.sendMsg("/vu/1", msg[3].(msg[3]>0.0).floor, msg[4].floor);}, '/reply1');
OSCFunc({ |msg| ~b.sendMsg("/vu/2", msg[3].floor, msg[4].floor);}, '/reply2');
OSCFunc({ |msg| ~b.sendMsg("/vu/3", msg[3].floor, msg[4].floor);}, '/reply3');
OSCFunc({ |msg| ~b.sendMsg("/vu/4", msg[3].floor, msg[4].floor);}, '/reply4');
OSCFunc({ |msg| ~b.sendMsg("/vu/5", msg[3].floor, msg[4].floor);}, '/reply5');
OSCFunc({ |msg| ~b.sendMsg("/vu/6", msg[3].floor, msg[4].floor);}, '/reply6');
OSCFunc({ |msg| ~b.sendMsg("/vu/7", msg[3].floor, msg[4].floor);}, '/reply7');
OSCFunc({ |msg| ~b.sendMsg("/vu/8", msg[3].floor, msg[4].floor);}, '/reply8');
OSCFunc({ |msg| ~b.sendMsg("/vu/9", msg[3].floor, msg[4].floor);}, '/reply9');
OSCFunc({ |msg| ~b.sendMsg("/vu/10", msg[3].floor, msg[4].floor);}, '/reply10');
OSCFunc({ |msg| ~b.sendMsg("/vu/11", msg[3].floor, msg[4].floor);}, '/reply11');
OSCFunc({ |msg| ~b.sendMsg("/vu/12", msg[3].floor, msg[4].floor);}, '/reply12');
)

s.freeAll;