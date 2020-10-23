Schematic of Audio and OSC signalflow for ambijockey project.

masterbus (

    receives    name                sends           
    ----------------------------------------------------------
    [1,2]       phonesbus           master
    [3]         monobus             master
    [4]         subwooferbus        master    
    [5-20]      spare               master
    [21-inf]    monobus             master
    [21-inf]    stereobus           master
    [21-inf]    decoderbus          master
)

phonesmasterbus (

    receives    name                sends           
    ----------------------------------------------------------
    [1,2]       monobus(ph)         masterbus
    [1,2]       stereobus(ph)       masterbus
    [1,2]       binauralbus(ph)     masterbus
)

reverbmasterbus (

    receives    name                sends           
    ----------------------------------------------------------
    [1-16]      reverbbus           decoderbus
    [17-32]     reverbbus(ph)       binauralbus
)

channelmasterbus (per channel)(

    receives    name                sends
    --------------------------------------------------------------
    [1]         mono                monobus
    [2]         subwoofer           subwooferbus
    [3,4]       stereo              stereobus + reverbbus
    [5-20]      b-format            decoderbus +  reverbbus
    [21,22]     mono(preF)          monobus(ph)
    [23,24]     stereo(preF)        stereobus(ph) + reverbbus(ph)
    [25-41]     b-format(preF)      binauralbus(ph) + reverbbus(ph)
)
