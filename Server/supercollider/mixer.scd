# This file is a part of A³Pandemic. License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
(
~speaker = 5;
~order = 3;
~hoaNumChannels = (~order+1).pow(2);
Server.supernova;
ServerOptions.new;
t = Server(\mic, NetAddr("127.0.0.1", 9001));
Server.local = Server.default;
t = Server.local.options; // Get the local server's options
t.numInputBusChannels = 8;
t.numOutputBusChannels = 8;
t.numAudioBusChannels = 2048 * 8;
t.blockSize = 512;
//t.numWireBufs = 1024 * ~hoaNumChannels;
t.memSize = 2.pow(18);
t.sampleRate = 48000;
s.boot
)

//s.supernova=2;

t.scope;
s.makeWindow;
s.plotTree;
s.meter;
Quarks.gui;
s.quit;
s.freeAll;
s.reboot;
s.queryAllNodes;
s.sync;
(
// OUTPUTMAPPING TO HARDWARE IS:
// PHONES = 1+2
// MONO = 3
// SUBWOOFER = 4
// NUMBER OF SPEAKERS =


//s.scope(5); // let's use 5 as we play back via ITU 5.0


// DECLARE AUDIO-BUSSES
~null = Bus.audio(s, 8);
~outputBus = Bus.audio(s, 3 + ~speaker);
~outputSubBus = Bus.audio(s, ~hoaNumChannels);
~mainSub = Bus.audio(s, 1);
~masterBus = Bus.audio(s, 40);
~masterAmbisonicBus = Bus.audio(s, ~hoaNumChannels);
~masterReverbBus = Bus.audio(s, ~hoaNumChannels);
~masterStereoBus = Bus.audio(s, ~speaker);
~masterSubBus = Bus.audio(s, 1);
~masterMonoBus = Bus.audio(s, ~speaker);

~phonesBus = Bus.audio(s, 2);
~phonesAmbisonicBus = Bus.audio(s, ~hoaNumChannels);
~phonesStereoBus = Bus.audio(s, 2);
~phonesMonoBus = Bus.audio(s, 2);
~phonesReverbBus = Bus.audio(s, ~hoaNumChannels);

~chMasterBus = Bus.audio(s, 8+(2*~hoaNumChannels));

~ch1MasterBus = Bus.audio(s, 8+(2*~hoaNumChannels));
~ch1AmbisonicBus = Bus.audio(s, ~hoaNumChannels);
~ch1StereoBus = Bus.audio(s, 2);
~ch1SubBus = Bus.audio(s, 1);
~ch1MonoBus = Bus.audio(s, 1);
~ch1InputBus = Bus.audio(s, 2);

~ch2MasterBus = Bus.audio(s, 40);
~ch2AmbisonicBus = Bus.audio(s, ~hoaNumChannels);
~ch2StereoBus = Bus.audio(s, 2);
~ch2SubBus = Bus.audio(s, 1);
~ch2MonoBus = Bus.audio(s, 1);
~ch2InputBus = Bus.audio(s, 2);

~ch3MasterBus = Bus.audio(s, 40);
~ch3AmbisonicBus = Bus.audio(s, ~hoaNumChannels);
~ch3StereoBus = Bus.audio(s, 2);
~ch3SubBus = Bus.audio(s, 1);
~ch3MonoBus = Bus.audio(s, 1);
~ch3InputBus = Bus.audio(s, 2);

~ch4MasterBus = Bus.audio(s, 40);
~ch4AmbisonicBus = Bus.audio(s, ~hoaNumChannels);
~ch4StereoBus = Bus.audio(s, 2);
~ch4SubBus = Bus.audio(s, 1);
~ch4MonoBus = Bus.audio(s, 1);
~ch4InputBus = Bus.audio(s, 2);

// DECLARE PROCESSGROUPS - HELP: ORDER OF EXECUTION
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
~monoGrp = Group.new(s);
~subGrp = Group.new(s);
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
)
// GENERATING BUSSES

// MAINBUS
SynthDef.new(\outputSynth, {
	var amp, phones, mono, sub, main;
	//phones =
	//mono =
	//sub = In.ar(~outputSubBus, 1);
	sub = In.ar(~mainSub, 1);
	main = In.ar(~masterBus, ~speaker);
	Out.ar(2, sub);
	Out.ar(3, main);
}).add;
HOAAmbiDecoderHelper
// MASTERBUS
SynthDef.new(\masterSynth, {
	arg amp;
	var mainMix, mono, monoMix, monoSingle, sub, stereo, stereoMix, ambisonic, reverb, out;
	amp = 1;
	sub = In.ar(~masterSubBus, 1);
	mono = In.ar(~masterMonoBus, ~speaker);
	stereo = In.ar(~masterStereoBus, ~speaker);
	ambisonic = In.ar(~masterAmbisonicBus, ~speaker);

//	monoMix = SplayAz.ar(~speaker, [mono], 1, 1, ~speaker, 0, 1, false);
//	monoMix = Array.fill(~speaker, mono);
//	stereoMix = Array.fill(~speaker, {stereo});
	mainMix = Mix.new([mono, stereo, ambisonic]);

	Out.ar(~mainSub, sub);
	//Out.ar(~masterBus, mono);
	Out.ar(~masterBus, mainMix);
	//sub = sub * amp;
	//Out.ar(~outputSubBus, sub);
	//monoSingle = Mix.new(mono);
	//Out.ar(~outputMonoBus, monoSingle);
}).add;
(
(
// AMBISONIC BUS
SynthDef.new(\ambisonicSynth, {
	var mix, ch;
	ch = InBus.ar(~chMasterBus, ~hoaNumChannels, 4, 20);
	mix = HOADec5_0.ar(~order, ch, 1, 0, 400, 0);
	Out.ar(~masterAmbisonicBus, mix);
}).add;
)
)
(
// STEREO BUS
SynthDef.new(\stereoSynth, {
	var stereoSplay, ch,
	spread = 0.1,
	width = ~speaker,
	amp = 1;
	ch = InBus.ar(~chMasterBus, 2, 2, 4);
	stereoSplay = SplayAz.ar(~speaker, ch, spread: spread, level: amp, width: width, center: 0, orientation:  0.5, levelComp: true);
	Out.ar(~masterStereoBus, stereoSplay);
}).add;

// MONO BUS
SynthDef.new(\monoSynth, {
	arg amp;
	var sum, mix, ch;
	amp = 1;
	ch = InBus.ar(~chMasterBus, 1, 1, 1);
	ch = ch * amp;
	mix = Array.fill(~speaker, ch);
	Out.ar(~masterMonoBus, mix);
}).add;

// SUBWOOFER BUS
SynthDef.new(\subSynth, {
	arg amp;
	var mix, ch;
	amp = 1;
	ch = InBus.ar(~chMasterBus, 1, 0, 0);
	mix = ch * amp;
	Out.ar(~masterSubBus, mix);
}).add;
)
/*
// PhonesSynth
SynthDef.new(\phonesSynth, {
	var amp, mono, stereo, ambisonic, ch, reverb;
	mono = InBus.ar(~phonesMonoBus, 1, 0, 1);
	stereo = InBus.ar(~phonesStereoBus, 2, 0, 2);
	ambisonic = InBus.ar(~masterAmbisonicBus, ~hoaNumChannels, 0, ~hoaNumChannels);
	reverb = InBus.ar(~phonesrReverbBus, ~hoaNumChannels, 15, 32);
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
	ch1 = InBus.ar(~ch1MasterBus, ~hoaNumChannels, 4);
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

(
// CHANNEL BUS
SynthDef.new(\chMasterSynth, {
	arg mix, inMono, inSub, inStereo, inAmbisonic, amp;
	var phones, mono, sub, stereo, ambisonic, sig;
	sub = In.ar(inSub, 1);
	mono = In.ar(inMono, 1);
	stereo = In.ar(inStereo, 2);
	ambisonic = In.ar(inAmbisonic, 16);
	//sig =  sig * amp;
	//mix = Array.with(sub, mono);
	Out.ar(~chMasterBus, [sub, mono, stereo, ambisonic] * amp);
	//Out.ar(~chMasterBus, ambisonic);
}).add;

// AMBISONIC ENCODER CHANNEL
SynthDef.new(\chAmbisonicSynth, {
	arg source, dest, amp,
	azL = -1.5,
	azR = 1.5,
	elev = 0,
	gain = -0.5;
	var sig, enc, encL, encR, encMix, inL, inR;
	sig = In.ar(source, 2);
	sig = sig * amp;
	inL = Balance2.ar(sig, sig, pos: -1, level: 1.0);
	inL = Mix.new(inL);
	inR = Balance2.ar(sig, sig, pos: 1, level: 1.0);
	inR = Mix.new(inR);
	encL = HOAEncoder.ar(~order, inL, az: azL, elev: elev, gain: gain, plane_spherical: 0, radius: 2, speaker_radius: 1.07);
	encR = HOAEncoder.ar(~order, inR, az: azR, elev: elev, gain: gain, plane_spherical: 0, radius: 2, speaker_radius: 1.07);
	encMix = Mix.new(encL, encR);
	Out.ar(dest, encMix);
}).add;

// STEREO CHANNEL
SynthDef.new(\chStereoSynth, {
	arg source, dest, amp;
	var sig, gain;
	gain = 0.5;
	sig = In.ar(source, 2);
	sig = sig * gain * amp;
	Out.ar(dest, sig);
}).add;

// MONO CHANNEL
SynthDef.new(\chMonoSynth, {
	arg source, dest, amp;
	var sig, gain;
	gain = 0.5;
	sig = In.ar(source, 2);
	sig = Mix.new(sig);
	sig = sig * gain * amp;
	Out.ar(dest, sig);
}).add;

// SUBWOOFER CHANNEL
SynthDef.new(\chSubSynth, {
	arg source, dest, amp;
	var sig, gain;
	gain = 0.5;
	sig = In.ar(source, 2);
	sig = Mix.new(sig);
	sig = sig * amp * gain;
	Out.ar(dest, sig);
}).add;

// INPUT CHANNEL
SynthDef.new(\inputSynth, {
	arg source, dest, amp;
	var sig;
	sig = In.ar(source, 2);
	sig = sig * amp;
	Out.ar(dest, sig);
}).add;
)
s.freeAll;
Quarks.gui;
Platform.userExtensionDir;
(
~output = Synth.new(\outputSynth, [\amp, 1], ~outputGrp);
~master = Synth.new(\masterSynth, [\amp, 1], ~masterGrp);
~masterAmbisonic = Synth.new(\ambisonicSynth, [], ~masterAmbisonicGroup);
~masterStereo = Synth.new(\stereoSynth, [], ~masterStereoGrp);
~masterMono = Synth.new(\monoSynth, [], ~masterMonoGrp);
~masterSub = Synth.new(\subSynth, [], ~masterSubGrp);

~ch1Master = Synth.new(\chMasterSynth, [\inMono, ~ch1MonoBus, \inSub, ~ch1SubBus, \inStereo, ~ch1StereoBus, \inAmbisonic, ~ch1AmbisonicBus, \amp, 1], ~chMasterGrp);

~ch1Ambisonic = Synth.new(\chAmbisonicSynth, [\source, ~ch1InputBus, \dest, ~ch1AmbisonicBus, \amp, 0], ~ambisonicGrp);
~ch1Stereo = Synth.new(\chStereoSynth, [\source, ~ch1InputBus, \dest, ~ch1StereoBus, \amp, 1], ~stereoGrp);
~ch1Mono = Synth.new(\chMonoSynth, [\source, ~ch1InputBus, \dest, ~ch1MonoBus, \amp, 0], ~monoGrp);
~ch1Sub = Synth.new(\chSubSynth, [\source, ~ch1InputBus, \dest, ~ch1SubBus, \amp, 0], ~subGrp);
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
s.freeAll;

//Quarks.install("https://github.com/florian-grond/SC-HOA");
Quarks.gui;
