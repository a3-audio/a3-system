/*
 * adc.h
 *
 * Created: 20/03/2022 22:54:14
 *  Author: tirii
 */ 


#ifndef ADC_H_
#define ADC_H_
#include "hardware.h"
#define MYAD0	6
#define MYAD1	8
#define ADC_TIMEBASE	((uint8_t)ceil(F_CPU*0.000001))


//hallo

void adc_init();
uint8_t adc_updateHysteresis(uint16_t inputLevel);
uint8_t  adc_setValue(uint16_t newValue);
uint16_t adc_getValue(uint8_t adcNum);
void adc_filterValues(uint8_t adcNum);
void	adc_start_prepare(uint8_t adcNum);
void	adc_start_go();
uint16_t adc_filter(uint16_t input);
uint16_t adc_increaseBitDepth(uint16_t in,uint8_t Bits_in,uint8_t Bits_out);

#endif /* ADC_H_ */
