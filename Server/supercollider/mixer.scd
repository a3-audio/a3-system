(
ServerOptions.new;
t = Server(\local, NetAddr("127.0.0.1", 9001));
Server.local = Server.default;
t = Server.local.options; // Get the local server's options
t.numInputBusChannels = 8;
t.numOutputBusChannels = 8;
t.numAudioBusChannels = 2048 * 8;
t.blockSize = 512;
t.numWireBufs = 1024 * 16;
t.memSize = 2.pow(18);
t.sampleRate = 44100;
//t.scope;
//s.makeWindow;
s.plotTree;
s.meter;
s.boot
)

s.quit;
s.freeAll;
s.reboot;
s.queryAllNodes;

(
// OUTPUTMAPPING TO HARDWARE IS:
// PHONES = 1+2
// MONO = 3
// SUBWOOFER = 4
// NUMBER OF SPEAKERS =

~speaker = 5;
~order = 3;

// GENERATING AUDIO-BUSSES
~null = Bus.audio(s, 8);
~outputBus = Bus.audio(s, 3 + ~speaker);
~outputSubBus = Bus.audio(s, 16);
~masterBusSub = Bus.audio(s, 1);
~masterBus = Bus.audio(s, 40);
~masterAmbisonicBus = Bus.audio(s, 16);
~masterReverbBus = Bus.audio(s, 16);
~masterStereoBus = Bus.audio(s, ~speaker);
~masterSubBus = Bus.audio(s, 1);
~masterMonoBus = Bus.audio(s, ~speaker);

~phonesBus = Bus.audio(s, 2);
~phonesAmbisonicBus = Bus.audio(s, 16);
~phonesStereoBus = Bus.audio(s, 2);
~phonesMonoBus = Bus.audio(s, 2);
~phonesReverbBus = Bus.audio(s, 16);

~chMasterBus = Bus.audio(s, 40);

~ch1MasterBus = Bus.audio(s, 40);
~ch1AmbisonicBus = Bus.audio(s, 16);
~ch1StereoBus = Bus.audio(s, 2);
~ch1SubBus = Bus.audio(s, 1);
~ch1MonoBus = Bus.audio(s, 1);
~ch1InputBus = Bus.audio(s, 2);

~ch2MasterBus = Bus.audio(s, 40);
~ch2AmbisonicBus = Bus.audio(s, 16);
~ch2StereoBus = Bus.audio(s, 2);
~ch2SubBus = Bus.audio(s, 1);
~ch2MonoBus = Bus.audio(s, 1);
~ch2InputBus = Bus.audio(s, 2);

~ch3MasterBus = Bus.audio(s, 40);
~ch3AmbisonicBus = Bus.audio(s, 16);
~ch3StereoBus = Bus.audio(s, 2);
~ch3SubBus = Bus.audio(s, 1);
~ch3MonoBus = Bus.audio(s, 1);
~ch3InputBus = Bus.audio(s, 2);

~ch4MasterBus = Bus.audio(s, 40);
~ch4AmbisonicBus = Bus.audio(s, 16);
~ch4StereoBus = Bus.audio(s, 2);
~ch4SubBus = Bus.audio(s, 1);
~ch4MonoBus = Bus.audio(s, 1);
~ch4InputBus = Bus.audio(s, 2);

// GENERATING GROUPS - HELP: ORDER OF EXECUTION
~outputGrp = Group.new(s);
~masterGrp = Group.new(s);
~masterAmbisonicGroup = Group.new(s);
~masterStereoGrp = Group.new(s);
~masterSubGrp = Group.new(s);
~masterMonoGrp = Group.new(s);

~phonesGrp = Group.new(s);

~reverbGrp = Group.new(s);
~reverbChannelGrp = Group.new(s);

~chMasterGrp = Group.new(s);
~ambisonicGrp = Group.new(s);
~stereoGrp = Group.new(s);
~subGrp = Group.new(s);
~monoGrp = Group.new(s);
~inputGrp = Group.new(s);

//OSC-Adresses
~adr_dj1_gain = "/track/dj1_in/gain";
~adr_dj1_high = "/track/dj1_in/fxeq/hishelf/gain";
~adr_dj1_mid = "/track/dj1_in/fxeq/band/0/gain";
~adr_dj1_lo = "/track/dj1_in/fxeq/loshelf/gain";
~adr_dj1_vol = "/track/dj1_in/volume";
~adr_dj1_pfl = "/track/mainmixbus/mute";

~adr_master_vol = "/master/volume";
~adr_master_hi = "/track/masterbus/fxeq/hishelf/gain";
~adr_master_mid = "/track/masterbus/fxeq/band/0/gain";
~adr_master_lo = "/track/masterbus/fxeq/loshelf/gain";
~adr_master_pfl = "/track/mainmixbus/mute";

~val_dj1_gain = 1;
~val_dj1_high = 1;
~val_dj1_mid = 1;
~val_dj1_lo = 1;
~val_dj1_vol = 1;
~val_dj1_pfl = 0;

~val_master_vol = 1;
~val_master_hi = 1;
~val_master_mid = 1;
~val_master_lo = 1;
~val_master_pfl = 1;

// GENERATING SYNTHS FOR AUDIO-PROCESSING

// OutputSynth
SynthDef.new(\outputSynth, {
	var amp, phones, mono, sub, main;
	//phones =
	//mono =
	//sub = In.ar(~outputSubBus, 1);
	sub = In.ar(~masterBusSub, 1);
	main = In.ar(~masterBus, ~speaker);
	Out.ar(2, sub);
	Out.ar(3, main);
}).add;

// MasterSynth
SynthDef.new(\masterSynth, {
	arg amp;
	var mainMix, mono, monoMix, monoSingle, sub, stereo, stereoMix, ambisonic, reverb, out;
	amp = 1;
	sub = In.ar(~masterSubBus, 1);
	mono = In.ar(~masterMonoBus, ~speaker);
	stereo = In.ar(~masterStereoBus, 2);
	ambisonic = In.ar(~masterAmbisonicBus, ~speaker);

//	monoMix = SplayAz.ar(~speaker, [mono], 1, 1, ~speaker, 0, 1, false);
//	monoMix = Array.fill(~speaker, mono);
//	stereoMix = Array.fill(~speaker, {stereo});
	mainMix = Mix.new([mono, stereo]);

	Out.ar(~masterBusSub, sub);
	Out.ar(~masterBus, mono);
	//sub = sub * amp;
	//Out.ar(~outputSubBus, sub);
	//monoSingle = Mix.new(mono);
	//Out.ar(~outputMonoBus, monoSingle);
}).add;

// MasterAmbisonicSynth
SynthDef.new(\ambisonicSynth, {
	var mix, ch;
	ch = InBus.ar(~chMasterBus, 16, 4, 20);
	mix = Mix.new([ch]);
	Out.ar(~masterAmbisonicBus, mix);
}).add;

// MasterStereoSynth
SynthDef.new(\stereoSynth, {
	var stereoSplay, ch,
	spread = 0.1,
	width = ~speaker,
	amp = 1;
	ch = InBus.ar(~chMasterBus, 2, 2, 4);
	stereoSplay = SplayAz.ar(~speaker, ch, spread: spread, level: amp, width: width, center: 0, orientation:  0.5, levelComp: true);
	Out.ar(~masterBus, stereoSplay);
}).add;

// MasterMonoSynth
SynthDef.new(\monoSynth, {
	arg amp;
	var sum, mix, ch;
	amp = 0.5;
	ch = InBus.ar(~chMasterBus, 1, 1, 1);
	ch = ch * amp;
	mix = Array.fill(~speaker, ch);
	Out.ar(~masterMonoBus, mix);
}).add;

// MasterSubSynth
SynthDef.new(\subSynth, {
	arg amp;
	var mix, ch;
	amp = 0.5;
	ch = InBus.ar(~chMasterBus, 1, 0, 0);
	mix = ch * amp;
	Out.ar(~masterSubBus, mix);
}).add;

/*
// PhonesSynth
SynthDef.new(\phonesSynth, {
	var amp, mono, stereo, ambisonic, ch, reverb;
	mono = InBus.ar(~phonesMonoBus, 1, 0, 1);
	stereo = InBus.ar(~phonesStereoBus, 2, 0, 2);
	ambisonic = InBus.ar(~masterAmbisonicBus, 16, 0, 16);
	reverb = InBus.ar(~phonesrReverbBus, 16, 15, 32);
	Out.ar(~phonesBus, mono);
}).add;

// PhonesMonoSynth
SynthDef.new(\monoSynth, {
	var ch1;
	ch1 = InBus.ar(~ch1MasterBus, 1, 0, 0);
	Out.ar(~phonesMonoBus, ch1);
}).add;

// PhonesStereoSynth
SynthDef.new(\stereoSynth, {
	var ch1;
	ch1 = InBus.ar(~ch1MasterBus, 2, 2, 3);
	Out.ar(~phonesStereoBus, ch1);
}).add;

// PhonesAmbisonicSynth
SynthDef.new(\ambisonicSynth, {
	var ch1;
	ch1 = InBus.ar(~ch1MasterBus, 16, 4);
	Out.ar(~phonesAmbisonicBus, ch1);
}).add;


// ReverbSynth
SynthDef.new(\reverbSynth, {
	arg amp, masterReverb, phonesReverb;
	masterReverb = InBus.ar(~phonesMonoBus, 1, 0, 1);
	phonesReverb = InBus.ar(~phonesStereoBus, 2, 0, 2);
	Out.ar(~masterReverbBus, masterReverb);
	Out.ar(~phonesReverbBus, phonesReverb);
}).add;

// MasterReverbSynth
SynthDef.new(\monoSynth, {
	var ch1;
	ch1 = InBus.ar(~ch1MasterBus, 1, 0, 0);
	Out.ar(~phonesMonoBus, ch1);
}).add;

// PhonesReverbSynth
SynthDef.new(\stereoSynth, {
	var ch1;
	ch1 = InBus.ar(~ch1MasterBus, 2, 2, 3);
	Out.ar(~phonesStereoBus, ch1);
}).add;
*/


// ChannelMasterSynth
SynthDef.new(\chMasterSynth, {
	arg mix, inMono, inSub, inStereo, inAmbisonic, amp;
	var phones, mono, sub, stereo, ambisonic, sig;
	mono = In.ar(inMono, 1);
	sub = In.ar(inSub, 1);
	stereo = In.ar(inStereo, 2);
	ambisonic = In.ar(inAmbisonic, 16);
	//sig =  sig * amp;
	//mix = Array.with(sub, mono);
	Out.ar(~chMasterBus, [sub, mono, stereo]);
}).add;

// AmbisonicSynth
SynthDef.new(\chAmbisonicSynth, {
	arg source, dest;
	var sig;
	sig = In.ar(source, 2);

	Out.ar(dest, sig);
}).add;

// StereoSynth
SynthDef.new(\chStereoSynth, {
	arg source, dest, amp;
	var sig;
	amp = 0.5;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

// MonoSynth
SynthDef.new(\chMonoSynth, {
	arg source, dest;
	var sig, amp;
	amp = 0.5;
	sig = In.ar(source, 2);
	sig = Mix.new(sig);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

// SubSynth
SynthDef.new(\chSubSynth, {
	arg source, dest;
	var sig, amp;
	amp = 0.5;
	sig = In.ar(source, 2);
	sig = Mix.new(sig);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;

// InputSynth
SynthDef.new(\inputSynth, {
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;
)
s.freeAll;
(
~output = Synth.new(\outputSynth, [\amp, 1], ~outputGrp);
~master = Synth.new(\masterSynth, [\amp, 1], ~masterGrp);
~masterAmbisonic = Synth.new(\ambisonicSynth, [], ~masterAmbisonicGroup);
~masterStereo = Synth.new(\stereoSynth, [], ~masterStereoGrp);
~masterSub = Synth.new(\subSynth, [], ~masterSubGrp);
~masterMono = Synth.new(\monoSynth, [], ~masterMonoGrp);

~ch1Master = Synth.new(\chMasterSynth, [\inMono, ~ch1MonoBus, \inSub, ~ch1SubBus, \inStereo, ~ch1StereoBus, \inAmbisonic, ~ch1AmbisonicBus], ~chMasterGrp);

~ch1Ambisonic = Synth.new(\chAmbisonicSynth, [\source, ~ch1InputBus, \dest, ~ch1AmbisonicBus], ~ambisonicGrp);
//~ch1Stereo = Synth.new(\chStereoSynth, [\source, ~ch1InputBus, \dest, ~ch1StereoBus], ~stereoGrp);
//~ch1Mono = Synth.new(\chMonoSynth, [\source, ~ch1InputBus, \dest, ~ch1MonoBus], ~monoGrp);
//~ch1Sub = Synth.new(\chSubSynth, [\source, ~ch1InputBus, \dest, ~ch1SubBus,], ~subGrp);
~ch1Input = Synth.new(\inputSynth, [\source, 8, \dest, ~ch1InputBus, \amp, 1], ~inputGrp);

//~output;
//~master;
//~masterAmbisonic;
//~masterStereo;
//~masterSub;
//~masterMono;

//~ch1Master;
//~ch1Ambisonic;
//~ch1Stereo;
//~ch1Sub;
//~ch1Mono;
//~ch1Input;
)

//OSCFunc.trace(true); // Turn posting on
//OSCFunc.trace(false); // Turn posting off

o.free;
m.free;
c.free;

s.freeAll;
t.boot;
s.reboot;
t.freeAll;
t.queryAllNodes;
t.options.numAudioBusChannels;
t.options.numOutputBusChannels;
t.options.numInputBusChannels;
s.quit;
t.freeAll;

//Quarks.install("https://github.com/florian-grond/SC-HOA");
Quarks.gui;
