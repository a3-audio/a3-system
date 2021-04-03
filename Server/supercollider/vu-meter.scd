(
Server.supernova;
ServerOptions.new;
t = Server(\mic, NetAddr("127.0.0.1", 9001));
Server.local = Server.default;
t = Server.local.options; // Get the local server's options
t.numInputBusChannels = 16;
t.numAudioBusChannels = 2048 * 8;
t.blockSize = 64;
//t.numWireBufs = 1024 * ~hoaNumChannels;
t.memSize = 2.pow(18);
t.sampleRate = 44100;
s.boot
)
s.plotTree;
s.freeAll;
s.meter;

b = NetAddr.new("127.0.0.1", 7771);    // create the NetAddr
// b.sendMsg("/vu_1-16", "peak, rms");

(
{
    SendPeakRMS.kr(In.ar(8, 2), 20, 3, "/replyAddress")
}.play;
)

(
o = OSCFunc({ |msg|
	"peak: %, rms: %".format(msg[3], msg[4]).postln
}, '/replyAddress', b);
)
o.free;