/*
 * colormath.c
 *
 * Created: 16/03/2022 13:14:21
 *  Author: tirii
 */

#include "ledandcolor.h"
#include "debug.h"

volatile rgbLed rgbButtons[4];
led leds[12];
led leds_t[12];
//volatile ledEvent ledEventsUpdate[12];
volatile bool isNewLedEventReady = false;
ledEvent led_events[14];
uint8_t led_event_n = 1;
uint8_t led_event_i = 0;
//volatile uint8_t nLedEvent = 1;

/*	
    sends the 16bit value to the shift register
    every output pin of the shift register corespondents to one LED
	
 */
void led_shiftSend(uint16_t data) {
    if (SPI0.INTFLAGS & SPI_DREIF_bm) { //transfer complete flag
        SPI0.INTCTRL = SPI_TXCIE_bm;
        SPI0.DATA = (uint8_t) ((data >> 8) & 0xFF);
        SPI0.DATA = (uint8_t) data;
    }
}
ledEvent led_getNextEvent(){
    led_event_i++;
    return led_events[led_event_i-1];
}
/*
    initializes the spi communication to the shift register
	
 */
void led_init() {
    BITMASK_SET(LED_SHD_PT.DIR, (1 << LED_SHD_BP) | (1 << LED_SHC_BP));
    BIT_SET(LED_SHU_PT.DIR, LED_SHU_BP);
    SPI0.CTRLA = SPI_MASTER_bm | SPI_PRESC_DIV4_gc;
    SPI0.CTRLB = SPI_BUFEN_bm | SPI_SSD_bm;
    SPI0.CTRLA |= SPI_ENABLE_bm;
    led_rgbInit();
    led_updateRGB(0, 0, 0, 0);
    led_updateRGB(1, 0, 0, 0);
    led_updateRGB(2, 0, 0, 0);
    led_updateRGB(3, 0, 0, 0);
    led_updateColorSystem();
}



void led_updateRGB(uint8_t buttonNum, uint8_t r, uint8_t g, uint8_t b) {
    *rgbButtons[buttonNum].r = r;
    *rgbButtons[buttonNum].g = g;
    *rgbButtons[buttonNum].b = b;
    isNewLedEventReady = true;
}

void led_rgbInit() {
    leds[0].hw_position = POS_LEDS1R;
    rgbButtons[0].r = &leds[0].time;
    leds[1].hw_position = POS_LEDS1G;
    rgbButtons[0].g = &leds[1].time;
    leds[2].hw_position = POS_LEDS1B;
    rgbButtons[0].b = &leds[2].time;

    leds[3].hw_position = POS_LEDS2R;
    rgbButtons[1].r = &leds[3].time;
    leds[4].hw_position = POS_LEDS2G;
    rgbButtons[1].g = &leds[4].time;
    leds[5].hw_position = POS_LEDS2B;
    rgbButtons[1].b = &leds[5].time;

    leds[6].hw_position = POS_LEDS3R;
    rgbButtons[2].r = &leds[6].time;
    leds[7].hw_position = POS_LEDS3G;
    rgbButtons[2].g = &leds[7].time;
    leds[8].hw_position = POS_LEDS3B;
    rgbButtons[2].b = &leds[8].time;

    leds[9].hw_position = POS_LEDS4R;
    rgbButtons[3].r = &leds[9].time;
    leds[10].hw_position = POS_LEDS4G;
    rgbButtons[3].g = &leds[10].time;
    leds[11].hw_position = POS_LEDS4B;
    rgbButtons[3].b = &leds[11].time;


    led_events[0].shift = 0;
    led_events[0].time = 0;
}

/*
    updates the shift value system

 */


//http://alienryderflex.com/quicksort/

int led_Compare(const void *a, const void *b) {

    led *a1 = (led *) a;
    led *a2 = (led *) b;
    return (a1->time > a2->time) - (a1->time < a2->time);
}

ledEvent led_updateColorSystem() {
    if (isNewLedEventReady) {
        isNewLedEventReady = false;
        for (int i = 0; i < 12; i++) {
            leds_t[i].hw_position = leds[i].hw_position;
            leds_t[i].time = leds[i].time;
        }
        //exchange values in led array
        //sort the leds by their time value
        qsort(leds_t, 12, 2, led_Compare);
        //uint16_t shift = 0b1110011111100111;
        led_event_n = 0;
        led_events[0].time = 0;
        led_events[0].shift = 0b1110011111100111;
        //combining time events to shift values
        //it's smaller then LED_MAX because LED_MAX is full on already
        for (int i = 0; i < 12 && leds_t[i].time < LED_MAX; i++) {
            if (leds_t[i].time > led_events[led_event_n ].time) {
                //we have a new time event
                led_event_n++;
                led_events[led_event_n].time = leds_t[i].time;
                led_events[led_event_n].shift=led_events[led_event_n-1].shift;
            }
            //if bit is cleared led will be switched off at this time
            BIT_CLEAR(led_events[led_event_n].shift, leds_t[i].hw_position);
            
        }
        led_event_n++;
        led_events[led_event_n].time =LED_MAX;
        led_event_n++;
    }
    led_event_i=1;
    return led_events[0];
}

