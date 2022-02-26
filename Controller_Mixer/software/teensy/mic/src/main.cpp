// This file is a part of A³Mix.
// License is GPLv3: https://github.com/ambisonics-audio-association/Ambijockey/blob/main/COPYING
// © Copyright 2021-2022 Raphael Eismann, Patric Schmitz

// Made for A³Mix PCB v0.2

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <LedControl.h>

#include <Bounce.h>

//////////// PIN ASSIGNMENTS //////////////
const uint8_t pinstates[2] = { HIGH, LOW };
const int pflleds [] = {26, 38, 39, 40};
const int pflButtonPins [] = {33, 34, 35, 36};

const int debounce_ms = 10; // 10 ms debounce
Bounce pflButtons [] = {
    Bounce(pflButtonPins[0], debounce_ms),
    Bounce(pflButtonPins[1], debounce_ms),
    Bounce(pflButtonPins[2], debounce_ms),
    Bounce(pflButtonPins[3], debounce_ms)
};


const int multiplexer[6] = {5, 6, 7, 8, 9, 13}; // Channelpotis [1-4], Masterpotis [5], fx buttons [6]
const int multiplexer_enc = 12; // Encoderswitches (digital)
const int selectPins[3] = {30, 31, 32}; // Multiplexer abc

const int display_sda1 = 17;
const int display_scl1 = 16;
const int display_sda2 = 25;
const int display_scl2 = 24;

// last sent states (potis)
const int num_tracks = 6;
const int num_pots = 8;
const int num_pfl_tracks = 4;

int pots_sent[num_tracks][num_pots];

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

    // Configure digital pins
    // pfl buttons
    for(int track = 0 ; track < num_pfl_tracks ; ++track) {
        pinMode(pflButtonPins[track], INPUT);
    }
    //pfl leds
    for(int track = 0 ; track < num_pfl_tracks ; ++track) {
        pinMode(pflleds[track], OUTPUT);
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
    // hc4051 reading potis
    for (byte pot=0 ; pot < 8 ; ++pot)
    {
        // hc4051 pinselector abc (binary)
        for (int i=0; i<3; i++) {
            digitalWrite(selectPins[i], pot & (1 << i) ? HIGH : LOW); // select hc4051
        }
        delayMicroseconds(10);
        // filter analog inputs
        for (int track=0 ; track < 6; track++) {
            int analog = analogRead(multiplexer[track]);
            int difference = pots_sent[track][pot] - analog;

            // send osc when difference larger than noise on
            // last bits
            if(abs(difference) > 8) {
                pots_sent[track][pot] = analog;
                float sendValue = float(analog) / 1023.f;
                Serial.print("T");
                Serial.print(":");
                Serial.print(track+1);
                Serial.print(":");
                Serial.print("P");
                Serial.print(":");
                Serial.print(pot+1);
                Serial.print(":");
                Serial.println(sendValue);
            }
        }
    }
    delayMicroseconds(10);

    // PFL Buttons
    for(int track = 0 ; track < num_pfl_tracks ; ++track) {
        pflButtons[track].update();

        // on rising edge send toggle
        if(pflButtons[track].risingEdge()) {
            Serial.print("T");
            Serial.print(":");
            Serial.print(track+1);
            Serial.print(":");
            Serial.print("B");
            Serial.print(":");
            Serial.print("0");
            Serial.print(":");
            Serial.println("0");
        }
    }

    if (Serial.available()) {
        String command = Serial.readStringUntil(',');

        if(command.startsWith("PFL")) {
            String mute = Serial.readStringUntil('\n');
            int track_index = command.substring(3, 4).toInt();
            int mute_index = mute.toInt();
            digitalWrite(pflleds[track_index - 1], pinstates[mute_index]);
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
