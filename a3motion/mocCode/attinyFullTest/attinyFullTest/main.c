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

ISR(TWI0_TWIS_vect)
{
	if(TWI0.SSTATUS & TWI_APIF_bm)					//Address match/stop interrupt
	{
		if (TWI0.SSTATUS & TWI_COLL_bm)
		{
			TWI0.SSTATUS |= TWI_COLL_bm;			//Clear Collision flag
			TWI0_SCTRLB = TWI_SCMD_COMPTRANS_gc;	//complete transaction
			return;
		}
		if(TWI0.SSTATUS & TWI_AP_bm)
		TWI0_SCTRLB = TWI_SCMD_RESPONSE_gc;		//Send ACK after address match
		else
		TWI0_SCTRLB = TWI_SCMD_COMPTRANS_gc;	//complete transaction after Stop
	}
	
	if(TWI0.SSTATUS & TWI_DIF_bm)					//Data interrupt
	{
		if(TWI0.SSTATUS & TWI_DIR_bm)               //Master reading from client
		{
			i2cResponseStrct resp = i2c_get_response();
			switch(resp.response){
				case sendADC0:
				if(resp.index==0){
					i2c_responseValue=adc_getValue(0);
					
					TWI0.SDATA = (uint8_t)i2c_responseValue;
					}else{
					
					TWI0.SDATA =(uint8_t)(i2c_responseValue>>8);
				}
				break;
				case sendADC1:
				if(resp.index==0){
					i2c_responseValue=adc_getValue(1);
					TWI0.SDATA = (uint8_t)i2c_responseValue;
					}else{
					
					TWI0.SDATA =(uint8_t)(i2c_responseValue>>8);
				}
				break;
				case sendENC:
				if(resp.index==0){
					i2c_responseValue=enc_getValue();
					TWI0.SDATA = (uint8_t)i2c_responseValue;
					}else{
					
					TWI0.SDATA =(uint8_t)(i2c_responseValue>>8);
				}
				break;
				case sendBUT:
	
				TWI0.SDATA=but_getValue();
				default:
				TWI0.SDATA = 11;
				break;
			}
			// spi_get_response();						//Transmit data for Master to read
			
			TWI0_SCTRLB = TWI_SCMD_RESPONSE_gc;
		}
		else                                            //Master sending to slave
		{
			i2c_set_message(TWI0.SDATA);
			TWI0_SCTRLB = TWI_SCMD_RESPONSE_gc;
		}
	}
}


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
}
int test = 0;
uint8_t testCnt = 0;

void sendLedAndIncrement(int16_t step) {
    testCnt += step;
    led_shiftSend(0b1 << testCnt % 16);
}

int main(void) {
    int tog=0;
    ccp_write_io((void *) & (CLKCTRL.MCLKCTRLB), 0); //protected write to disable prescaler of CPU clock
   BITMASK_SET(PORTB.DIR, PIN1_bm | PIN0_bm); //PB1 and PB0 as output
    time_t0Init();
    time_t1Init();
    i2c_init(1);
    //led_init();
    BITMASK_SET(LED_SHD_PT.DIR, (1 << LED_SHD_BP) | (1 << LED_SHC_BP));
    BIT_SET(LED_SHU_PT.DIR, LED_SHU_BP);
    SPI0.CTRLA = SPI_MASTER_bm | SPI_PRESC_DIV4_gc;
    SPI0.CTRLB = SPI_BUFEN_bm | SPI_SSD_bm;
    SPI0.CTRLA |= SPI_ENABLE_bm;
    
    
    sei();
   // led_shiftSend(0);
    while (1) {
        //if (tBCnt > 100) {
            tBCnt = 0;
           sendLedAndIncrement(1);
            if(tog==1){
			tog=0;
			BITMASK_SET(PORTB.OUT,PIN1_bm|PIN0_bm); //PB1 and PB0 as output
		}else{
			tog=1;
			BITMASK_CLEAR(PORTB.OUT,PIN1_bm|PIN0_bm); //PB1 and PB0 as output
		}
            _delay_ms(1000);
        //}

    }


    //_delay_ms(500);		  // delay 1/2 second

}

