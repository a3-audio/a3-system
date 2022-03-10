// This file is a part of A³Mix.
// License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
// © Copyright 2021-2022 Raphael Eismann, Patric Schmitz

// Made for A³Mix PCB v0.2

#include <array>

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <LedControl.h>

#include <Bounce.h>

const int debounce_ms = 10; // 10 ms debounce
const uint8_t pin_states[2] = { HIGH, LOW };

//////////// PIN ASSIGNMENTS //////////////

const int PINS_LED_PER_CHANNEL [] = {26, 38, 39, 40};
const int PINS_BUTTON_0_PER_CHANNEL [] = {33, 34, 35, 36};
Bounce button_0_per_channel [] = {
    Bounce(PINS_BUTTON_0_PER_CHANNEL[0], debounce_ms),
    Bounce(PINS_BUTTON_0_PER_CHANNEL[1], debounce_ms),
    Bounce(PINS_BUTTON_0_PER_CHANNEL[2], debounce_ms),
    Bounce(PINS_BUTTON_0_PER_CHANNEL[3], debounce_ms)
};

const int multiplexer[6] = {5, 6, 7, 8, 9}; // Channel pots [0-3],
                                            // Master pots [4]
const int multiplexer_enc = 12; // Encoderswitches (digital)
const int selectPins[3] = {30, 31, 32}; // Multiplexer abc

// track the bounce state for 8 buttons on the multiplexer, which are
// all connected to the same teensy pin.
const int PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL = 27;
Bounce buttons_1_2_multiplex_per_channel [] = {
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
    Bounce(PIN_BUTTONS_1_2_MULTIPLEX_PER_CHANNEL, debounce_ms),
};

const int num_fx_buttons = 2;
const int PINS_BUTTON_FX [] = {28, 29};
Bounce buttons_fx [] = {
    Bounce(PINS_BUTTON_FX[0], debounce_ms),
    Bounce(PINS_BUTTON_FX[1], debounce_ms),
};

const int display_sda1 = 17;
const int display_scl1 = 16;
const int display_sda2 = 25;
const int display_scl2 = 24;

// last sent states (potis)
const int num_channels = 4;
const int num_tracks = 6; // including master and fx sections
const int num_pots = 8;

int pots_sent[num_tracks][num_pots];

const std::array<std::string, 6> track_names = {
    "0",
    "1",
    "2",
    "3",
    "master",
    "fx",
};


// vu-meter neopixel
const int npxl_pin = 13; // pcb pin
const int npxl_leds = 48;// striplength
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(npxl_leds, npxl_pin, NEO_GRB + NEO_KHZ800);

int vupxlstrips[4][9] = {
    {11,10,9,8,7,6,5,4,3},
    {23,22,21,20,19,18,17,16,15},
    {35,34,33,32,31,30,29,28,27},
    {47,46,45,44,43,42,41,40,39}
};

// LED-Matrix
LedControl lc=LedControl(18,14,15,4); // led-matrix pins
int modePxl[4][3] = {
    {0,1,2},
    {12,13,14},
    {24,25,26},
    {36,37,38}
};

// NeoPixel Arrays
String vuVars[4] = { "VU01", "VU02", "VU03", "VU04" };
String vuVarsM[8] = { "VU05", "VU06", "VU07", "VU08", "VU09", "VU10", "VU11", "VU12" };

// fx mode buttons are connected to $multiplexer [1,2] last physical connector on chip
// fx potis are connected to $multiplexer channel [3,4] last physical connector on chip

// Rotary Encoder
const int rEnc0_DT = 0;
const int rEnc0_clk = 1;
const int rEnc1_DT = 2;
const int rEnc1_clk = 3;
const int rEnc2_DT = 4;
const int rEnc2_clk = 5;
const int rEnc3_DT = 6;
const int rEnc3_clk = 7;
const int rEnc4_DT = 8;
const int rEnc4_clk = 9;
const int rEnc5_DT = 10;
const int rEnc5_clk = 11;

const int spare_1 = 28;
const int spare_2 = 29;

void setup() {

    // initialize sent values to 0
    for(int track = 0 ; track < num_tracks ; ++track) {
        for(int pot = 0 ; pot < num_pots ; ++pot) {
            pots_sent[track][pot] = 0;
        }
    }

    Serial.begin(115200);       // starting Serial
    pixels.begin(); 		// INITIALIZE NeoPixel
    pixels.clear();
    pixels.setBrightness(10);

    // Configure per-channel digital pins
    for(int channel = 0 ; channel < num_channels ; ++channel) {
        pinMode(PINS_BUTTON_0_PER_CHANNEL[channel], INPUT);
        pinMode(PINS_LED_PER_CHANNEL[channel], OUTPUT);
    }

    for(int button = 0 ; button < num_fx_buttons ; ++button) {
        pinMode(PINS_BUTTON_FX[button], INPUT);
    }

    lc.shutdown(0,false);
    lc.shutdown(1,false);
    lc.shutdown(2,false);
    lc.shutdown(3,false);

    // Set brightness
    lc.setIntensity(0,1);
    lc.setIntensity(1,1);
    lc.setIntensity(2,1);
    lc.setIntensity(3,1);
}

void loop(){
    // first read per-track button 0 directly (no mux)
    for(int channel = 0 ; channel < num_channels ; ++channel) {
        if(button_0_per_channel[channel].update()) {
            Serial.print("T");
            Serial.print(":");
            Serial.print(channel);
            Serial.print(":");
            Serial.print("B");
            Serial.print(":0:");
            Serial.println(button_0_per_channel[channel].risingEdge() ? "1" : "0");
        }
    }

    // read pots and fx/3d buttons via hc4051 multiplexer
    for (byte pin=0 ; pin < 8 ; ++pin)
    {
        // hc4051 pinselector abc (binary)
        for (int i=0; i<3; i++) {
            digitalWrite(selectPins[i], pin & (1 << i) ? HIGH : LOW); // select hc4051
        }
        delayMicroseconds(10);

        // the four tracks [0-3] and the master track [4] are read
        // as fully analog inputs.
        for (int track=0 ; track < 5; ++track) {
            int analog = analogRead(multiplexer[track]);
            int difference = pots_sent[track][pin] - analog;

            // filter analog inputs
            // send osc when difference larger than noise on
            // last bits
            // @TODO this needs to be solved in hardware!
            if(abs(difference) > 8) {
                pots_sent[track][pin] = analog;
                float sendValue = float(analog) / 1023.f;
                Serial.print("T");
                Serial.print(":");
                Serial.print(track_names[track].c_str());
                Serial.print(":");
                Serial.print("P");
                Serial.print(":");
                Serial.print(pin);
                Serial.print(":");
                Serial.println(sendValue, 6);
            }
        }

        // read buttons 1, 2 per channel
        if(buttons_1_2_multiplex_per_channel[pin].update()) {
            Serial.print("T:");
            Serial.print(pin%4);
            Serial.print(":B:");
            Serial.print(1 + pin/4);
            Serial.print(":");
            Serial.println(buttons_1_2_multiplex_per_channel[pin].risingEdge() ? "1" : "0");
        }
    }

    // read buttons separately for FX track [5]
    for(int button = 0 ; button < num_fx_buttons ; ++button) {
        if(buttons_fx[button].update()) {
            Serial.print("T:");
            Serial.print(track_names[5].c_str());
            Serial.print(":B:");
            Serial.print(button);
            Serial.print(":");
            Serial.println(buttons_fx[button].risingEdge() ? "1" : "0");
        }
    }

    delayMicroseconds(10);

    if (Serial.available()) {
        String command = Serial.readStringUntil(',');

        if(command.startsWith("PFL")) {
            String mute = Serial.readStringUntil('\n');
            int track_index = command.substring(3, 4).toInt();
            int mute_index = mute.toInt();
            digitalWrite(PINS_LED_PER_CHANNEL[track_index], pin_states[mute_index]);
        }

        for (int i = 0; i < 4; i++) { // filter serial inputstream VU01-VU04
            if(command.startsWith(vuVars[i])) {
                String peak = Serial.readStringUntil(',');
                String rms = Serial.readStringUntil('\n');

                int peak_index = peak.toInt();// convert string to int
                int rms_index = rms.toInt();

                for(int j = 0 ; j < 9 ; j++) {
                    uint32_t color;
                    if(j == peak_index)
                        color = pixels.Color(255,0,0);
                    else if(j <= rms_index)
                        color = pixels.Color(0,255,0);
                    else
                        color = pixels.Color(0,0,0);

                    pixels.setPixelColor(vupxlstrips[i][j], color);
                }
            }
        }

        for (int i = 0 ; i < 8 ; i++) { // filter serial inputstream VU05-VU12
            if(command.startsWith(vuVarsM[i]))
            {
                String peak = Serial.readStringUntil(',');
                String rms = Serial.readStringUntil('\n');
                // String peak = "31";
                // String rms = "31";

                int peak_index = peak.toInt();
                int rms_index = rms.toInt();
                //Serial.println(rms1);

                // rms-meter plus peak over all leds
                for(int j = 0 ; j < 32 ; j++){
                    int module_index = j / 8;
                    int x = 8 - 1 - i;
                    int y = 8 - 1 - j % 8;

                    bool led_on = j <= rms_index || j == peak_index;
                    lc.setLed(module_index, x, y, led_on);
                }
            }
        }
        pixels.show(); // send to hardware.
    }
}
