(

~server_ADDRESS = 57122;
~input_OSC      = 8989;

Server.supernova;

Server.default = Server(\a3core, NetAddr("127.0.0.1", ~server_ADDRESS));

s.options.device               = "default";
s.options.numInputBusChannels  = 8;
s.options.numOutputBusChannels = 8;
s.options.maxLogins            = 2;
s.options.memSize              = 65536;
s.options.numBuffers           = 4096;

// get script's directory for relative paths
~root_DIR = thisProcess.nowExecutingPath.dirname++"/";

s.boot;
)

(
// SETUP
~stereo_input_channels = 4;

~main_speakers = 6;
~booth_speakers = 6;

~hoa_order = 3;
~hoa_channels = (~hoa_order+1).pow(2);

~st_in_1_ch = 8;
~st_in_2_ch = 10;
~st_in_3_ch = 12;
~st_in_4_ch = 14;

// SYNTHS DEFINITIONS
/// FOH
SynthDef.new(\foh_main_synth, { // FOH GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\foh_booth_synth, { // FOH GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\foh_phones_synth, { // FOH GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

/// MAIN
SynthDef.new(\master_main_synth, { // MASTER GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\master_booth_synth, { // MASTER GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\master_phones_synth, { // MASTER GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

/// DECODE
SynthDef.new(\decode_main_bformat_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\decode_main_stereo_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = SplayAz.ar(~main_speakers, sig, spread: 0.1, level: amp, width: ~main_speakers, center: 0, orientation:  0.5, levelComp: true);
	Out.ar(dest, sig);
}).add;

SynthDef.new(\decode_main_sub_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\decode_booth_bformat_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\decode_booth_stereo_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\decodce_booth_sub_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\decode_phones_binaural_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\decode_phones_stereo_synth, { // MIX GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

/// PHONES
SynthDef.new(\phones_pfl_synth, { // PFL GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

/// ENCODE
SynthDef.new(\encode_bformat_synth, { // ENCODE GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\encode_ms_synth, { // ENCODE GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

SynthDef.new(\encode_stereo_synth, { // ENCODE GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

/// INPUT
SynthDef.new(\input_synth, { // INPUT GROUP
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

// -------------------------------------------------------------------------------- \\

// PROCESSGROUPS (ORDER OF EXECUTION DESCENDING SC OUTPUT TO INPUT)
~foh_group = Group.new(s);
~master_group = Group.new(s);
~decode_group = Group.new(s);
~pfl_group = Group.new(s);
~encode_group = Group.new(s);
~input_group = Group.new(s);
)

// CHANNELSTRIP
(
~sc_input_channels = Array.with(8,10,12,14);
~encode_stereo_bus = Bus.audio(s, 2);

for (0, ~stereo_input_channels -1, {
	arg i,
	input_channel = format("~input_channel_%", ~sc_input_channels[i]),
	encode_stereo = format("~encode_stereo_%", i),

	input_bus = format("~input_bus_%", i),
	encode_stereo_bus = format("~encode_stereo_bus_%", i);

		// AUDIOBUSSES
	input_bus = Bus.audio(s, 2);
	encode_stereo_bus = Bus.audio(s, 2);

	// INIT AUDIO SYNTHS
	input_channel = Synth.new(\input_synth, [\source, ~input_channels[i], \dest, input_bus, \amp, 1], ~input_group);
	encode_stereo = Synth.new(\encode_stereo_synth, [\source, input_bus, \dest, ~encode_stereo_bus, \amp, 1], ~encode_group);

});

~decode_main_stereo = Synth.new(\decode_main_stereo_synth, [\source, ~encode_stereo_bus, \dest, 0, \amp, 1], ~decode_group);
)


(
~in_1 = Synth.new(\input_synth, [\source, 8, \dest, 0, \amp, 1], ~input_group);

	OSCdef.new(
		\test,
		{
			arg msg, time, addr, port;
			~in_1.set(\amp, msg[1]);
		},
		'/test'
	);
)



~st_in_1_patch = Synth.new(\input_synth, [\source, ~st_in_1, \dest, ~input_bus_1, \amp, 1], ~input_group);
~decode_main_stereo.set(\amp, 1);
~encode_stereo_0.set(\amp, 0);
~input_channel_1.set(\amp, 0);

// RELEASE
~sc_input_stereo.free;
~encode_stereo.free;
~main_master.free;
~mix_main_stereo.free;
~input_bformat_1.free;
~input_ms_1.free;
~input_stereo_1.free;

// SERVER CONTROL
s.freeAll;
s.meter;
s.plotTree;
s.quit;
s.boot;
NetAddr.langPort;
// NOTE: SC DESTINATIONS ARE MAPPED BEFORE SOURCES
// EXAMPLE: IF SC HAS 2 IN AND 4 OUT, THE SC OUTPUTS ARE CH 0,1,2,3 AND THE SC INPUTS ARE 4,5

// -------------------------------------------------------------------------------- \\

// SPAWN AUDIO-BUSSES
/// FOH
~foh_main_bus = Bus.audio(s, ~main_speakers);
~foh_booth_bus = Bus.audio(s, ~booth_speakers);
~foh_phones_bus = Bus.audio(s, 2);

/// MASTER
~master_main_bus = Bus.audio(s, ~hoa_channels);
~master_booth_bus = Bus.audio(s, ~hoa_channels);
~master_phones_bus = Bus.audio(s, 2);

/// DECODE
~decode_main_bformat_decoder_bus = Bus.audio(s, ~hoa_channels);
~decode_main_stereo_bus = Bus.audio(s, 2);
~decode_main_sub_bus = Bus.audio(s, 2);
~decode_booth_bformat_decoder_bus = Bus.audio(s, ~hoa_channels);
~decode_booth_stereo_bus = Bus.audio(s, 2);
~decode_booth_sub_bus = Bus.audio(s, 2);
~decode_phones_binaural_bus = Bus.audio(s, ~hoa_channels);
~decode_phones_stereo_bus = Bus.audio(s, 2);

/// PHONES
~pfl_phones_bus = Bus.audio(s, 2);

/// ENCODE <-- FROM HERE DESCENDING TO INPUT ALL BUSSES MUST BE GENERATED PER MIXERCHANNEL --> TODO
~encode_bformat_bus = Bus.audio(s, ~hoa_channels);
~encode_ms_bus = Bus.audio(s, 2);
~encode_stereo_bus = Bus.audio(s, 2);

/// INPUT
~input_bus_1 = Bus.audio(s, 2);

// -------------------------------------------------------------------------------- \\

// SPAWN CONNECTION-SYNTHS
/// FOH

/// MASTER
~main_master = Synth.new(\master_main_synth, [\source, ~master_main_bus, \dest, 0, \amp, 1], ~master_group);

/// DECODE
~decode_main_stereo = Synth.new(\decode_main_stereo_synth, [\source, 0, \dest, 0, \amp, 1], ~decode_group);

/// ENCODE <-- FROM HERE DESCENDING TO INPUT ALL SYNTHS MUST BE GENERATED PER MIXERCHANNEL --> TODO
~encode_bformat = Synth.new(\encode_bformat_synth, [\source, ~input_bus, \dest, ~encode_bformat_bus, \amp, 1], ~encode_group);
~encode_ms = Synth.new(\encode_ms_synth, [\source, ~input_bus, \dest, ~encode_ms_bus, \amp, 1], ~encode_group);
~encode_stereo = Synth.new(\encode_stereo_synth, [\source, ~input_bus, \dest, ~encode_stereo_bus, \amp, 1], ~encode_group);
