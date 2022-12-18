/*
 Test for moc platine
 it will blink the SCL SDA line
 pin 11 or 12
 */ 

#ifndef F_CPU			// if F_CPU was not defined in Project -> Properties
#define F_CPU 1000000UL			  // define it now as 1 MHz unsigned long
#endif

#include <avr/io.h>			  // this is always included in AVR programs
#include <util/delay.h>			  // add this to use the delay function
/*
(MALE)
1	 2	 3	 4	 5											10	 9	 8	 7	 6	 4	 3	 2
GND	SDC	SDA	UPD	VCW											SDA	SHU	ENB	BU3	AD1	AD0	ESW	BU1				(Poti Connector)
--- PB0	PB1													PB1	PB2	PB3	PB4	PB5	PA6	PA5	PA4				1	AD1
																										2	GND
																	(Attiny1626)						3	AD0
(FEMALE)					(programming interface)														4	GND	
1	 2	 3	 4	 5			 1	 2	 3						11	 12	 13	 15	 16	 17	 19					5	VCC
GND	SDC	SDA	UPD	VCW			VCW	UPD	GND						SCL	BU2	ENA	BU0	UPD	SHD	SHC		
--- PB0	PB1													PB0	PC0	PC1	PC3	PA0	PA1	PA3
															
*/

int main(void)
{
	ccp_write_io((void *) & (CLKCTRL.MCLKCTRLB), 0); //protected write to disable prescaler of CPU clock
    PORTB.DIR
	DDRB |= (1 << PB0);		  // set Port C pin PC5 for output
	
	while (1) {	                  // begin infinite loop
		PORTB ^= (1 << PB5);	  // flip state of LED on PC5
		_delay_ms(500);		  // delay 1/2 second
	}
	return(0);	// should never get here, this is to prevent a compiler warning
}

