/*
* MCU1626.c
*
* Created: 23/02/2022 13:06:16
* Author : tirii
*/
#include "main.h"


/*
(MALE)
1	 2	 3	 4	 5
GND	SDC	SDA	UPD	VCW
--- PB0	PB1

10	 9	 8	 7	 6	 4	 3	 2
SDA	SHU	ENB	BU3	AD1	AD0	ESW	BU1
PB1	PB2	PB3	PB4	PB5	PA6	PA5	PA4



11	 12	 13	 15	 16	 17	 19		 1	 2	 3
SCL	BU2	ENA	BU0	UPD	SHD	SHC		VCW	UPD	GND
PB0	PC0	PC1	PC3	PA0	PA1	PA3
*/

volatile uint16_t i2c_responseValue;
volatile uint8_t counter=0;
volatile uint8_t counterNew=0;
volatile uint8_t test=0;
volatile i2cOrderStrct	orderStrct;
int aaa=0;
volatile uint8_t i2cBuffer[16];
volatile uint8_t r_i2cBuffer;
volatile uint8_t w_i2cBuffer;
//ADC sample is ready
ISR(ADC0_SAMPRDY_vect){
	uint8_t tL=ADC0_SAMPLEL;
	uint8_t tH=ADC0_SAMPLEH;
	ADC0.INTFLAGS|=ADC_RESOVR_bm;
	adc_setValue((uint16_t)((tH<<8)|tL));
}

//Led snet interrupt
//updates the shift register
ISR(SPI0_INT_vect){
	if(SPI0.INTFLAGS&SPI_TXCIF_bm){
		BIT_SET(LED_SHU_PT.OUTSET,LED_SHU_BP);//ACK BIT ON
		BITMASK_SET(SPI0.INTFLAGS,SPI_TXCIF_bm);
		BITMASK_CLEAR(SPI0.INTCTRL,SPI_TXCIE_bm);
		BIT_SET(LED_SHU_PT.OUTCLR,LED_SHU_BP);//ACK BIT OFF
	}
}

//LED Shift counter
//clock cycle 3ms/255
ISR(TCA0_OVF_vect){
	TCA0.SINGLE.INTFLAGS|=TCA_SINGLE_OVF_bm;//clear interrupt flag
	ledEvent rgbEvent=led_getNextEvent();
	TCA0.SINGLE.PER=rgbEvent.time;
	led_shiftSend(rgbEvent.shiftVal);
}
//100us
ISR(TCB0_INT_vect){
	TCB0.INTFLAGS|=TCB_CAPT_bm;
	counterNew++;
	counterNew%=7;
}

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
		if(TWI0.SSTATUS & TWI_DIR_bm)
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
		else
		{
			i2c_set_message(TWI0.SDATA);
			TWI0_SCTRLB = TWI_SCMD_RESPONSE_gc;
		}
	}
}


int main(void)
{	ccp_write_io((void *) & (CLKCTRL.MCLKCTRLB), 0); //protected write to disable prescaler of CPU clock
	debug_init();
	timer0_init();
	timer1_init();
	i2c_init();
	led_init();
	but_init();
	adc_init();
	enc_init();
	sei();
	
	while (1)
	{
	
		if(counter!=counterNew){
			
			counter=counterNew;
			switch(counter){
				case 0:;//strange error but the semicolon has to be there
				orderStrct=i2c_get_order();
				if(orderStrct.order>-1){
					uint8_t		val=orderStrct.msg[2];
					val*=2;
					uint16_t	angle=(orderStrct.msg[1]<<7)|(orderStrct.msg[0]&0xFF);
					switch (orderStrct.order)
					{
						case ordRgb0:
						led_updateRGB(0,angle,val);
						break;
						
						case ordRgb1:
						led_updateRGB(1,angle,val);
						break;
						
						case ordRgb2:
						led_updateRGB(2,angle,val);
						break;
						
						case ordRgb3:
						led_updateRGB(3,angle,val);
						break;
						default:
						break;
					}
					
				}
				break;
				case 1:
				enc_start();
				break;
				case 2:
				adc_start(0);
				
				break;
				case 3:
				but_start();
				
				break;
				case 4:
				adc_start(1);
				
				break;
				case 5:
				adc_filterValues(0);
				break;
				case 6:
				adc_filterValues(1);
				break;
				default:
				break;
			}
		}
	}
}





/*
if(counter==0||counter==64||counter==128||counter==192){
if(BIT_CHECK(PORTC.IN,PIN3_bp)){
BIT_CLEAR(buttons[0].sample,buttonCount);
}else{
BIT_SET(buttons[0].sample,buttonCount);
}
if(buttons[0].state==STATE_BUT_PRESSED&&buttons[0].sample==STATE_BUT_RELEASED){
buttons[0].state=STATE_BUT_RELEASED;
leds[0]=hsvtoRGB(tLed0Count,255);
}else
if(buttons[0].state==STATE_BUT_RELEASED&&buttons[0].sample==STATE_BUT_PRESSED){
buttons[0].state=STATE_BUT_PRESSED;
tLed0Count+=10;
tLed0Count%=360;
leds[0]=hsvtoRGB(100,255);
}

//... andere buttons
buttonCount=(buttonCount+1)&0b00000111;
}else*/

/*else{



enc_delta=0;
if(encoder_val!=tLed0Count){
tLed0Count+=10;
encoder_val=tLed0Count;
leds[0]=hsvtoRGB(tLed0Count,255);



}
}*/