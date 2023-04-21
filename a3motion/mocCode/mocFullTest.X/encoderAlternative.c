

#include "encoderAlternative.h"



volatile int8_t enc_delta; // -128 ... 127
static int8_t last;
volatile uint8_t step = 4;
void enc_set_step(uint8_t stepNew){
    step=stepNew;
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
    };
}

int8_t enc_getValue(void) { // Encoder auslesen
    int8_t val;

    // atomic access to enc_delta
    cli();
    val = enc_delta;
    switch (step) {
        case 2: enc_delta = val & 1;
            val >>= 1;
            break;
        case 4: enc_delta = val & 3;
            val >>= 2;
            break;
        default: enc_delta = 0;
            break;
    }
    sei();
    return val; // counts since last call
}

void enc_init(uint8_t enc_step) {
    enc_set_step(enc_step);
    // init encoder
    BIT_CLEAR(ENC_A_PT.DIR, ENC_A_BP);
    BIT_SET(ENC_A_PT.PIN1CTRL, PORT_PULLUPEN_bp); //Button1 PA4
    BIT_CLEAR(ENC_B_PT.DIR, ENC_B_BP);
    BIT_SET(ENC_B_PT.PIN3CTRL, PORT_PULLUPEN_bp); //Button1 PA4

    int8_t new;
    new = 0;
    if (BIT_CHECK(ENC_A_PT.IN, ENC_A_BP)) new = 3;
    if (BIT_CHECK(ENC_B_PT.IN, ENC_B_BP)) new ^= 1; // convert gray to binary
    last = new; // power on state
    enc_delta = 0;
}