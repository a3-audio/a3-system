/*
 * timer.c
 *
 * Created: 22/03/2022 15:18:50
 *  Author: tirii
 */ 
#include "timer.h"

void timer0_init(){
	TCA0.SINGLE.PER=1;//255;//&0xFF;
	//TCA0.SINGLE.PERH=(255>>8)&0xFF;
	TCA0.SINGLE.INTCTRL|=TCA_SINGLE_OVF_bm; //enable counter intterrupt on overflow
	TCA0.SINGLE.CTRLA|=TCA_SINGLE_CLKSEL_DIV256_gc|TCA_SINGLE_ENABLE_bm;
}
void timer1_init(){
	TCB0.CCMP=8;
	//TCA0.SINGLE.PERH=(255>>8)&0xFF;
	TCB0.INTCTRL|=TCB_CAPT_bm; //enable counter intterrupt on overflow
	TCB0.CTRLA|=TCB_CLKSEL_TCA0_gc|TCA_SINGLE_ENABLE_bm;
}