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

~b = NetAddr.new("192.168.43.130", 7771);    // create the NetAddr
~b.sendMsg("/vu_1-16", "peak, rms");

(
{SendPeakRMS.kr(In.ar(2, 1), 20, 3, "/reply1")}.play;
{SendPeakRMS.kr(In.ar(3, 1), 20, 3, "/reply2")}.play;
{SendPeakRMS.kr(In.ar(4, 1), 20, 3, "/reply3")}.play;
{SendPeakRMS.kr(In.ar(5, 1), 20, 3, "/reply4")}.play;
{SendPeakRMS.kr(In.ar(6, 1), 20, 3, "/reply5")}.play;
{SendPeakRMS.kr(In.ar(7, 1), 20, 3, "/reply6")}.play;
{SendPeakRMS.kr(In.ar(8, 1), 20, 3, "/reply7")}.play;
{SendPeakRMS.kr(In.ar(9, 1), 20, 3, "/reply8")}.play;
{SendPeakRMS.kr(In.ar(10, 1), 20, 3, "/reply9")}.play;
{SendPeakRMS.kr(In.ar(11, 1), 20, 3, "/reply10")}.play;
{SendPeakRMS.kr(In.ar(12, 1), 20, 3, "/reply11")}.play;
{SendPeakRMS.kr(In.ar(13, 1), 20, 3, "/reply12")}.play;
{SendPeakRMS.kr(In.ar(14, 1), 20, 3, "/reply13")}.play;
{SendPeakRMS.kr(In.ar(15, 1), 20, 3, "/reply14")}.play;
{SendPeakRMS.kr(In.ar(16, 1), 20, 3, "/reply15")}.play;
{SendPeakRMS.kr(In.ar(17, 1), 20, 3, "/reply16")}.play;
)


(
OSCFunc({ |msg| ~b.sendMsg("/vu/1", msg[3], msg[4]);}, '/reply1');
OSCFunc({ |msg| ~b.sendMsg("/vu/2", msg[3], msg[4]);}, '/reply2');
OSCFunc({ |msg| ~b.sendMsg("/vu/3", msg[3], msg[4]);}, '/reply3');
OSCFunc({ |msg| ~b.sendMsg("/vu/4", msg[3], msg[4]);}, '/reply4');
OSCFunc({ |msg| ~b.sendMsg("/vu/5", msg[3], msg[4]);}, '/reply5');
OSCFunc({ |msg| ~b.sendMsg("/vu/6", msg[3], msg[4]);}, '/reply6');
OSCFunc({ |msg| ~b.sendMsg("/vu/7", msg[3], msg[4]);}, '/reply7');
OSCFunc({ |msg| ~b.sendMsg("/vu/8", msg[3], msg[4]);}, '/reply8');
OSCFunc({ |msg| ~b.sendMsg("/vu/9", msg[3], msg[4]);}, '/reply9');
OSCFunc({ |msg| ~b.sendMsg("/vu/10", msg[3], msg[4]);}, '/reply10');
OSCFunc({ |msg| ~b.sendMsg("/vu/11", msg[3], msg[4]);}, '/reply11');
OSCFunc({ |msg| ~b.sendMsg("/vu/12", msg[3], msg[4]);}, '/reply12');
OSCFunc({ |msg| ~b.sendMsg("/vu/13", msg[3], msg[4]);}, '/reply13');
OSCFunc({ |msg| ~b.sendMsg("/vu/14", msg[3], msg[4]);}, '/reply14');
OSCFunc({ |msg| ~b.sendMsg("/vu/15", msg[3], msg[4]);}, '/reply15');
OSCFunc({ |msg| ~b.sendMsg("/vu/16", msg[3], msg[4]);}, '/reply16');
)

s.freeAll;