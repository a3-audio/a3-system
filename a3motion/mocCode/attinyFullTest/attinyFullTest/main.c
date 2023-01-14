/*
 * attinyFullTest.c
 *
 * Created: 11/01/2023 12:41:46
 * Author : tiri
 */

#include <avr/io.h>
#include "main.h"
#define sRED 0
#define sGREEN 120
#define sBLUE 240
#define sOFF  -1
#define vOFF  0
#define vON  LED_MAX
#define sBUT_PRESSED 1
#define sBUT_RELEASED 0
#define NUM_CASES 3
uint8_t butStates = 0;
uint8_t ledStates[] = {sRED, sRED, sRED, sRED};
const uint8_t STATES[] = {sRED, sGREEN, sBLUE, sOFF};
volatile uint8_t counter = 0;
volatile uint8_t counterNew = 0;
uint16_t secondsCounter = 0;
//LED Shift counter
//clock cycle 3ms/255
//Led snet interrupt
//updates the shift register

ISR(SPI0_INT_vect) {
    if (SPI0.INTFLAGS & SPI_TXCIF_bm) {
        BIT_SET(LED_SHU_PT.OUTSET, LED_SHU_BP); //ACK BIT ON
        BITMASK_SET(SPI0.INTFLAGS, SPI_TXCIF_bm);
        //BITMASK_CLEAR(SPI0.INTCTRL,SPI_TXCIE_bm);
        BIT_SET(LED_SHU_PT.OUTCLR, LED_SHU_BP); //ACK BIT OFF
    }
}

ISR(TCA0_OVF_vect) {
    TCA0.SINGLE.INTFLAGS |= TCA_SINGLE_OVF_bm; //clear interrupt flag
    //ledEvent rgbEvent = led_getNextEvent();
    TCA0.SINGLE.PER = 1;
    //TCA0.SINGLE.PER = rgbEvent.time;
    //led_shiftSend(rgbEvent.shiftVal);
}
//100us
uint16_t tBCnt = 0;

ISR(TCB0_INT_vect) {
    TCB0.INTFLAGS |= TCB_CAPT_bm;
    tBCnt++;
    enc_start();
}
uint8_t tButStates = 0;
int test = 0;
uint8_t testCnt = 0;

void sendLedAndIncrement(int16_t step) {
    testCnt += step;
    led_shiftSend(0b1 << testCnt % 16);
}

int main(void) {
    ccp_write_io((void *) & (CLKCTRL.MCLKCTRLB), 0); //protected write to disable prescaler of CPU clock
    BITMASK_SET(PORTB.DIR, PIN1_bm | PIN0_bm); //PB1 and PB0 as output
    uint8_t tog = 0;

    //debug_init();
    time_t0Init();
    time_t1Init();
    //i2c_init();
    //led_init();
    BITMASK_SET(LED_SHD_PT.DIR, (1 << LED_SHD_BP) | (1 << LED_SHC_BP));
    BIT_SET(LED_SHU_PT.DIR, LED_SHU_BP);
    SPI0.CTRLA = SPI_MASTER_bm | SPI_PRESC_DIV4_gc;
    SPI0.CTRLB = SPI_BUFEN_bm | SPI_SSD_bm;
    SPI0.CTRLA |= SPI_ENABLE_bm;
    but_init();
    //adc_init();
    enc_init();
    sei();
    led_shiftSend(0);
    while (1) {
        counter++;
        counter %= NUM_CASES;
        switch (counter) {
            case 0:
                but_updateStates();
                break;
            case 1:
                tButStates = but_getStates();
                if (tButStates != butStates) {

                    for (int i = 0; i < 4; i++) {
                        if ((tButStates & (1 << i)) > (butStates & (1 << i))) {
                            sendLedAndIncrement(1);

                            //ledStates[i]++;
                            //ledStates[i] %= 4;

                            //led_updateRGB(i, STATES[ledStates[i]], (ledStates[i] == sOFF) ? vOFF : vON);
                        }
                    }
                    butStates = tButStates;
                }
                break;
            case 2:;
                int16_t encVal = enc_getValue();
                if (encVal != 0)
                    //led_shiftSend(encVal);
                    sendLedAndIncrement(encVal);
                break;
        }
        if (tBCnt > 100) {
            tBCnt = 0;
            //sendLedAndIncrement(1);
        }

    }


    //_delay_ms(500);		  // delay 1/2 second

}

