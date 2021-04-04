s.plotTree;
s.meter;

s.boot;

~b = NetAddr.new("192.168.43.130", 7771);    // create the NetAddr
~b.sendMsg("/vu_1-16", "peak, rms");

(
{
    SendPeakRMS.ar(In.ar(3, 2), 20, 3, "/replyAddress")
}.play;
)

(
o = OSCFunc({ |msg|
	var peak, rms;
	peak = msg[3];
	rms = msg[4];
	~b.sendMsg("/vu", peak, rms);
}, '/replyAddress');
)

s.freeAll;