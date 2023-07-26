/*
 * encoder.c
 *
 * Created: 22/03/2022 15:17:52
 *  Author: tirii
 */
#include "encoder.h"
int8_t enc_delta; // -128 ... 127
int16_t enc_valNew = 0;
int16_t enc_val = 0;
static int8_t last;



int16_t enc_getValue() {
    return enc_val;
}

void enc_update() {
    int8_t new, diff;
    new = 0;
    if (BIT_CHECK(ENC_A_PT.IN, ENC_A_BP)) new = 3;
    if (BIT_CHECK(ENC_B_PT.IN, ENC_B_BP)) new ^= 1; // convert gray to binary
    diff = last - new; // difference last - new
    if (diff & 1) { // bit 0 = value (1)
        last = new; // store new as next last
        enc_delta += (diff & 2) - 1; // bit 1 = direction (+/-)
    }
    if (enc_delta != 0) {
        enc_val += (enc_delta); // read a single step encoder
        enc_delta = 0;
    }
}

void enc_init() {
    int8_t new;

    // init encoder
    BIT_CLEAR(ENC_A_PT.DIR, ENC_A_BP);
    BIT_SET(ENC_A_PT.PIN1CTRL, PORT_PULLUPEN_bp); //Button1 PA4
    BIT_CLEAR(ENC_B_PT.DIR, ENC_B_BP);
    BIT_SET(ENC_B_PT.PIN3CTRL, PORT_PULLUPEN_bp); //Button1 PA4
    //_delay_ms(1);

    new = 0;
    if (BIT_CHECK(ENC_A_PT.IN, ENC_A_BP)) new = 3;
    if (BIT_CHECK(ENC_B_PT.IN, ENC_B_BP)) new ^= 1; // convert gray to binary
    last = new; // power on state
    enc_delta = 0;
}