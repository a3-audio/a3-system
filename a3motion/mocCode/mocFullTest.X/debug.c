#include "src/debug.h"

uint8_t tog_ch1 = 0;
void toggleCh1() {
    if (tog_ch1 == 0) {
        tog_ch1 = 1;
        BIT_SET(PORTB_OUT, ADC1_BP);
    } else {
        BIT_CLEAR(PORTB_OUT, ADC1_BP);
        tog_ch1 = 0;
    }
}


uint8_t tog_ch2 = 0;

void toggleCh2() {
    if (tog_ch2 == 0) {
        tog_ch2 = 1;
        BIT_SET(PORTA_OUT, ADC0_BP);
    } else {
        tog_ch2 = 0;
        BIT_CLEAR(PORTA_OUT, ADC0_BP);

    }
}
