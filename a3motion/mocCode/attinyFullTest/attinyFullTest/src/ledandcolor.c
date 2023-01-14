/*
 * colormath.c
 *
 * Created: 16/03/2022 13:14:21
 *  Author: tirii
 */

#include "ledandcolor.h"
/*const uint8_t PROGMEM gam[] = {
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
	1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
	2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
	5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
	10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
	17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
	25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
	37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
	51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
	69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
	90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
	115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
	144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
	177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ,255,255,255,255};*/
volatile uint8_t iLedEvent = 0;
rgbLed rgbButtons[4];
ledStruct leds[12]; //TODO removed volatile qualifier
volatile ledEvent ledEventsUpdate[12];
bool isNewLedEventReady=false;
volatile ledEvent ledEvents[12];
volatile uint8_t nLedEventUpdate = 1;
volatile uint8_t nLedEvent = 1;
/*	
	sends the 16bit value to the shift register
	every output pin of the shift register corespondents to one LED
	
*/
void led_shiftSend(uint16_t data) {
	if (SPI0.INTFLAGS & SPI_DREIF_bm) {			//transfer complete flag
		SPI0.INTCTRL = SPI_TXCIE_bm;
		SPI0.DATA = (uint8_t) ((data >> 8) & 0xFF);
		SPI0.DATA = (uint8_t) data;
	}
}

/*
	initializes the spi communication to the shift register
	
*/
void led_init() {
	BITMASK_SET(LED_SHD_PT.DIR, (1<<LED_SHD_BP)|(1<<LED_SHC_BP));
	BIT_SET(LED_SHU_PT.DIR, LED_SHU_BP);
	SPI0.CTRLA = SPI_MASTER_bm | SPI_PRESC_DIV4_gc;
	SPI0.CTRLB = SPI_BUFEN_bm | SPI_SSD_bm;
	SPI0.CTRLA |= SPI_ENABLE_bm;
	led_rgbInit();
	led_updateRGB(0,0,0);
	led_updateRGB(1,0,0);
	led_updateRGB(2,0,0);
	led_updateRGB(3,0,0);
}
ledEvent led_getNextEvent() {

	if(isNewLedEventReady&&iLedEvent==0){
		//memcpy(ledEvents,ledEventsUpdate,sizeof ledEvents[0]*nLedEventUpdate);
		for (int i=0;i<nLedEventUpdate;i++)
		{
			ledEvents[i].shiftVal=ledEventsUpdate[i].shiftVal;
			ledEvents[i].time=ledEventsUpdate[i].time;
		}
		nLedEvent=nLedEventUpdate;
		isNewLedEventReady=false;
	}
	ledEvent retVal = ledEvents[iLedEvent];
	iLedEvent++;
	iLedEvent %= nLedEvent;
	return retVal;
}

/*
	updates the color of one button (buttonNum)
	colorAngle is the color in 360 degree. Every degree represents one color
	0 is RED
	120 is GREEN
	240 is Blue
	value is the intensity. 0 is dark and 
	
*/
void led_updateRGB(uint8_t buttonNum, uint16_t colorAngle, uint8_t value) {
	isNewLedEventReady=false;
	led_hsvToRGB(&rgbButtons[buttonNum], (float) colorAngle, value);
	led_updateColorSystem();
	//We have a new version for our shift register
	cli();
	isNewLedEventReady=true;
	sei();
}
int led_Compare(const void *a, const void *b) {

	ledStruct *a1 = (ledStruct*) a;
	ledStruct *a2 = (ledStruct*) b;
	return a1->ledVal.time - a2->ledVal.time;
}
void led_hsvToRGB(rgbLed *rgbBut, float angle, uint8_t val) {
	#define cRED 0
	#define cGREEN 1
	#define cBLUE 2
	
	float fAngle = angle * 0.016667;
	uint8_t c[3];
	if (angle < 60) {//max1
		float x2 = val * fAngle;

		c[cRED] = val;
		c[cGREEN] = x2;
		c[cBLUE] = 0;
		} else if (angle < 120) {
		float x2 = val * (2 - fAngle);//max 2
		c[cRED] = x2;
		c[cGREEN] = val;
		c[cBLUE] = 0;
		} else if (angle < 180) {
		float x2 = val * (fAngle - 2);//max 3
		c[cRED] = 0;
		c[cGREEN] = val;
		c[cBLUE] = x2;
		} else if (angle < 240) {
		float x2 = val * (4 - fAngle);//max 4
		c[cRED] = 0;
		c[cGREEN] = x2;
		c[cBLUE] = val;
		} else if (angle < 300) {
		float x2 = val * (fAngle - 4); //max 5
		c[cRED] = x2;
		c[cGREEN] = 0;
		c[cBLUE] = val;
		} else {
		float x2 = val * (6 - fAngle);//max 6
		c[cRED] = val;
		c[cGREEN] = 0;
		c[cBLUE] = x2;
	}
	rgbBut->red.time = c[0];//pgm_read_byte(&gam[c[0]]);
	rgbBut->green.time = c[1];//pgm_read_byte(&gam[c[1]]);
	rgbBut->blue.time = c[2];//pgm_read_byte(&gam[c[2]]);
}
void led_rgbInit() {
	rgbButtons[0].red.position = POS_LEDS1R;
	leds[0].ledVal.position = POS_LEDS1R;
	leds[0].newTime=&(rgbButtons[0].red.time);
	rgbButtons[0].green.position = POS_LEDS1G;
	leds[1].ledVal.position = POS_LEDS1G;
	leds[1].newTime=&(rgbButtons[0].green.time);
	rgbButtons[0].blue.position = POS_LEDS1B;
	leds[2].ledVal.position = POS_LEDS1B;
	leds[2].newTime=&(rgbButtons[0].blue.time);

	rgbButtons[1].red.position = POS_LEDS2R;
	leds[3].ledVal.position = POS_LEDS2R;
	leds[3].newTime=&(rgbButtons[1].red.time);
	rgbButtons[1].green.position = POS_LEDS2G;
	leds[4].ledVal.position = POS_LEDS2G;
	leds[4].newTime=&(rgbButtons[1].green.time);
	rgbButtons[1].blue.position = POS_LEDS2B;
	leds[5].ledVal.position = POS_LEDS2B;
	leds[5].newTime=&(rgbButtons[1].blue.time);

	rgbButtons[2].red.position = POS_LEDS3R;
	leds[6].ledVal.position = POS_LEDS3R;
	leds[6].newTime=&(rgbButtons[2].red.time);
	rgbButtons[2].green.position = POS_LEDS3G;
	leds[7].ledVal.position = POS_LEDS3G;
	leds[7].newTime=&(rgbButtons[2].green.time);
	rgbButtons[2].blue.position = POS_LEDS3B;
	leds[8].ledVal.position = POS_LEDS3B;
	leds[8].newTime=&(rgbButtons[2].blue.time);

	rgbButtons[3].red.position = POS_LEDS4R;
	leds[9].ledVal.position = POS_LEDS4R;
	leds[9].newTime=&(rgbButtons[3].red.time);
	rgbButtons[3].green.position = POS_LEDS4G;
	leds[10].ledVal.position = POS_LEDS4G;
	leds[10].newTime=&(rgbButtons[3].green.time);
	rgbButtons[3].blue.position = POS_LEDS4B;
	leds[11].ledVal.position = POS_LEDS4B;
	leds[11].newTime=&(rgbButtons[3].blue.time);


	ledEventsUpdate[0].shiftVal=0;
	ledEventsUpdate[0].time=0;
}

/*
	updates the shift value system

*/


//http://alienryderflex.com/quicksort/
void led_updateColorSystem() {
	//exchange values in led array
	for (int i = 0; i < 12; i++) {
		//the l
		leds[i].ledVal.time=*leds[i].newTime;
	}
	//sort the leds by their time value
	qsort(leds, 12, sizeof(ledStruct), led_Compare);
	uint16_t shift = 0b1110011111100111;
	nLedEventUpdate = 0;
	ledEventsUpdate[0].time=0;
	//combining time events to shift values
	//it's smaller then LED_MAX because LED_MAX is full on already
	for (int i = 0; i < 12 && leds[i].ledVal.time < LED_MAX; i++) {
		if (leds[i].ledVal.time > ledEventsUpdate[nLedEventUpdate].time) {
			//we have a new time event
			nLedEventUpdate++;
			ledEventsUpdate[nLedEventUpdate].time = leds[i].ledVal.time;
		}
		//if bit is cleared led will be switched off at this time
		BIT_CLEAR(shift, leds[i].ledVal.position);
		ledEventsUpdate[nLedEventUpdate].shiftVal = shift;
	}
	nLedEventUpdate++;
#ifdef ECLIPSE_DEBUG
	for (int i = 0; i < nLedEventUpdate; i++) {
		printf("%d	%04X\n", ledEventsUpdate[i].time, ledEventsUpdate[i].shiftVal);
	}
#endif

	//building the delta between send events
	uint8_t lastTime = 0;
		for (int i = 0; i < nLedEventUpdate; i++) {
			//the last event is untill LED_MAX
			if (i == (nLedEventUpdate - 1))
				ledEventsUpdate[i].time = LED_MAX - lastTime;
			else
				ledEventsUpdate[i].time = ledEventsUpdate[i + 1].time - lastTime;
			lastTime += ledEventsUpdate[i].time;
		}
#ifdef ECLIPSE_DEBUG
	for (int i = 0; i < nLedEventUpdate; i++) {
		printf("%d	%04X\n", ledEventsUpdate[i].time, ledEventsUpdate[i].shiftVal);
	}
#endif
}
