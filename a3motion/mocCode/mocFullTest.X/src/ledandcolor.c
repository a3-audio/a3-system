/*
 * colormath.c
 *
 * Created: 16/03/2022 13:14:21
 *  Author: tirii
 */

#include "ledandcolor.h"

volatile rgbLed rgbButtons[4];
led leds[57];
led leds_t[57];
volatile bool isNewLedEventReady = false;
ledEvent led_events[59];
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
    for(int i=0;i<=18;i++)
        led_updateRGB(i, 0, 0, 0);
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

    
    
    leds[12].hw_position = POS_LEDS1R;
    rgbButtons[4].r = &leds[12].time;
    leds[13].hw_position = POS_LEDS1G;
    rgbButtons[4].g = &leds[13].time;
    leds[14].hw_position = POS_LEDS1B;
    rgbButtons[4].b = &leds[14].time;

    leds[15].hw_position = POS_LEDS2R;
    rgbButtons[5].r = &leds[15].time;
    leds[16].hw_position = POS_LEDS2G;
    rgbButtons[5].g = &leds[16].time;
    leds[17].hw_position = POS_LEDS2B;
    rgbButtons[5].b = &leds[17].time;

    leds[18].hw_position = POS_LEDS3R;
    rgbButtons[6].r = &leds[18].time;
    leds[19].hw_position = POS_LEDS3G;
    rgbButtons[6].g = &leds[19].time;
    leds[20].hw_position = POS_LEDS3B;
    rgbButtons[6].b = &leds[20].time;

    leds[21].hw_position = POS_LEDS4R;
    rgbButtons[7].r = &leds[21].time;
    leds[22].hw_position = POS_LEDS4G;
    rgbButtons[7].g = &leds[22].time;
    leds[23].hw_position = POS_LEDS4B;
    rgbButtons[7].b = &leds[23].time;
    
    
    leds[24].hw_position = POS_LEDS1R;
    rgbButtons[8].r = &leds[24].time;
    leds[25].hw_position = POS_LEDS1G;
    rgbButtons[8].g = &leds[25].time;
    leds[26].hw_position = POS_LEDS1B;
    rgbButtons[8].b = &leds[26].time;

    leds[27].hw_position = POS_LEDS2R;
    rgbButtons[9].r = &leds[27].time;
    leds[28].hw_position = POS_LEDS2G;
    rgbButtons[9].g = &leds[28].time;
    leds[29].hw_position = POS_LEDS2B;
    rgbButtons[9].b = &leds[29].time;

    leds[30].hw_position = POS_LEDS3R;
    rgbButtons[10].r = &leds[30].time;
    leds[31].hw_position = POS_LEDS3G;
    rgbButtons[10].g = &leds[31].time;
    leds[32].hw_position = POS_LEDS3B;
    rgbButtons[10].b = &leds[32].time;

    leds[33].hw_position = POS_LEDS4R;
    rgbButtons[11].r = &leds[33].time;
    leds[34].hw_position = POS_LEDS4G;
    rgbButtons[11].g = &leds[34].time;
    leds[35].hw_position = POS_LEDS4B;
    rgbButtons[11].b = &leds[35].time;
    
    
    leds[36].hw_position = POS_LEDS1R;
    rgbButtons[12].r = &leds[36].time;
    leds[37].hw_position = POS_LEDS1G;
    rgbButtons[12].g = &leds[37].time;
    leds[38].hw_position = POS_LEDS1B;
    rgbButtons[12].b = &leds[38].time;

    leds[39].hw_position = POS_LEDS2R;
    rgbButtons[13].r = &leds[39].time;
    leds[40].hw_position = POS_LEDS2G;
    rgbButtons[13].g = &leds[40].time;
    leds[41].hw_position = POS_LEDS2B;
    rgbButtons[13].b = &leds[41].time;

    leds[42].hw_position = POS_LEDS3R;
    rgbButtons[14].r = &leds[42].time;
    leds[43].hw_position = POS_LEDS3G;
    rgbButtons[14].g = &leds[43].time;
    leds[44].hw_position = POS_LEDS3B;
    rgbButtons[14].b = &leds[44].time;

    leds[45].hw_position = POS_LEDS4R;
    rgbButtons[15].r = &leds[45].time;
    leds[46].hw_position = POS_LEDS4G;
    rgbButtons[15].g = &leds[46].time;
    leds[47].hw_position = POS_LEDS4B;
    rgbButtons[15].b = &leds[47].time;
    
    
    leds[48].hw_position = POS_LEDS1R;
    rgbButtons[16].r = &leds[48].time;
    leds[49].hw_position = POS_LEDS1G;
    rgbButtons[16].g = &leds[49].time;
    leds[50].hw_position = POS_LEDS1B;
    rgbButtons[16].b = &leds[50].time;

    leds[51].hw_position = POS_LEDS2R;
    rgbButtons[17].r = &leds[51].time;
    leds[52].hw_position = POS_LEDS2G;
    rgbButtons[17].g = &leds[52].time;
    leds[53].hw_position = POS_LEDS2B;
    rgbButtons[17].b = &leds[53].time;

    leds[54].hw_position = POS_LEDS3R;
    rgbButtons[18].r = &leds[54].time;
    leds[55].hw_position = POS_LEDS3G;
    rgbButtons[18].g = &leds[55].time;
    leds[56].hw_position = POS_LEDS3B;
    rgbButtons[18].b = &leds[56].time;
    
    
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
        for (int i = 0; i < 57; i++) {
            leds_t[i].hw_position = leds[i].hw_position;
            leds_t[i].time = leds[i].time;
        }
        //exchange values in led array
        //sort the leds by their time value
        qsort(leds_t, 57, 2, led_Compare);
        //uint16_t shift = 0b1110011111100111;
        led_event_n = 0;
        led_events[0].time = 0;
        led_events[0].shift = 0b1110011111100111;
        //combining time events to shift values
        //it's smaller then LED_MAX because LED_MAX is full on already
        for (int i = 0; i < 57 && leds_t[i].time < LED_MAX; i++) {
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

