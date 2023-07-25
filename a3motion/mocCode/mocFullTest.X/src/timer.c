/*
 * timer.c
 *
 * Created: 22/03/2022 15:18:50
 *  Author: tirii
 */ 
#include "timer.h"

/*
	timerA init
	is used to divide the color mixture. The more often it is execudted in one period,the higher is the color variation.
	writing a top value to .. .PER gives the period
	the clock is divided by 256 so that interrupt is executed every 256 clk cycle
*/ 
//LED Counter
void time_t0Init(){
	TCA0.SINGLE.PER=23;//255;//&0xFF;
	//TCA0.SINGLE.PERH=(255>>8)&0xFF;
	TCA0.SINGLE.INTCTRL|=TCA_SINGLE_OVF_bm; //enable counter intterrupt on overflow
	TCA0.SINGLE.CTRLA|=TCA_SINGLE_CLKSEL_DIV64_gc|TCA_SINGLE_ENABLE_bm;
}
/*
	timerB init
	timerB is used to segment the main loop
	on every timer event the counter is updated. On every new count the main loop is updated
*/

//Sensor counter
void time_t1Init(){
	TCB0.CCMP=2500;//8;
    //TCA0.SINGLE.PERH=(255>>8)&0xFF;
	TCB0.INTCTRL|=TCB_CAPT_bm; //enable counter intterrupt on overflow
	TCB0.CTRLA|=TCB_CLKSEL_DIV2_gc|TCB_ENABLE_bm;
}

#define time_cnt_start TCB1.CTRLA|=TCB_ENABLE_bm;
#define time_cnt_stop TCB1.CTRLA|=TCB_ENABLE_bm;

void time_counter(){
    TCB1.CCMP=100;
    TCB1.INTCTRL|=TCB_CAPT_bm;
    TCB1.CTRLA|=TCB_CLKSEL_DIV2_gc;
}

