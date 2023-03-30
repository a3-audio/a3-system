/*
 * adc.c
 *
 * Created: 20/03/2022 22:54:00
 *  Author: FElix Dahmen
 */
#include "adc.h"
#define HYST_WIDTH	3
#define SELECTED_ADC	(ADC0.MUXPOS&0x3F)//compare it to MYAD0 or MYAD1
#define ADC_READY_FOR_NEW	(!BITMASK_CHECK_ALL(ADC0.INTFLAGS,ADC_SAMPRDY_bm)&&!BITMASK_CHECK_ALL(ADC0.STATUS,ADC_ADCBUSY_bm));
#define MARGIN  ((1 << HYST_WIDTH) - 1)
#define OFFSET  (1 << (HYST_WIDTH - 1))
#define MAX_IN	((uint16_t)-1)
#define MAX_OUT	(((uint16_t)MAX_IN) >> HYST_WIDTH)	//uint16_t max_out = static_cast<uint16_t>(MAX_IN >> HYST_WIDTH);
uint16_t adcValuesNew[2]={0,0};
uint16_t adcValues[2];
uint32_t filtered[2]={0,0};
uint8_t adcNumG=0;


#define K 5
#define  fixedPointAHalf  ((uint32_t)(1 << (K - 1)))

//adcNum must be one or zero
void adc_start_prepare(uint8_t adcNum){
    adcNumG=adcNum;
    ADC0.MUXPOS=(adcNum==0)?MYAD0:MYAD1;
}
void adc_start_go(){
		ADC0.COMMAND|=ADC_START_IMMEDIATE_gc;
}
/**
 * @brief   Get the current output level.
 *
 * @return  The output level.
 */
uint16_t adc_getValue(uint8_t adcNum) { 
	return adcValues[adcNum]; 
}
uint8_t adc_setValue(uint16_t newValue){
	adcValuesNew[adcNumG]=newValue;
    adc_filterValues(adcNumG);
    return adcNumG;
}
void adc_filterValues(uint8_t adcNum){
	//add some filter functions here
	adcValues[adcNum]=adcValuesNew[adcNum];
}
/**
     * @brief   Update the hysteresis output with a new input value.
     *
     * @param   inputLevel
     *          The input to calculate the output level from.
     * @return  true
     *          The output level has changed.
     * @return  false
     *          The output level is still the same.
     */
/**
 * @brief   A class for applying hysteresis to a given input.
 *
 * This reduces the noise by decreasing the resolution, and it prevents flipping
 * back and forth between two values.
 *
 * <b>An example for `BITS` = 7 and an input from 0 to 1023</b>
 * ```
 *    7                                                     ┌───◄───┬───
 * o  6                                             ┌───◄───┼───►───┘
 * u  5                                     ┌───◄───┼───►───┘
 * t  4                             ┌───◄───┼───►───┘
 * p  3                     ┌───◄───┼───►───┘
 * u  2             ┌───◄───┼───►───┘
 * t  1     ┌───◄───┼───►───┘
 *    0 ────┴───►───┘
 *      0      128     256     384     512     640     768     896    1023
 *                                  i n p u t
 * ```
 *
 * @tparam  BITS
 *          The number of bits to decrease in resolution.
 *          Increasing this number will result in a decrease in fluctuations.
 */
uint8_t adc_updateHysteresis(uint16_t inputLevel) {
	uint16_t prevLevelFull = ((uint16_t)adcValuesNew[adcNumG] << HYST_WIDTH) | OFFSET;//
	uint16_t lowerbound = adcValuesNew[adcNumG] > 0 ? prevLevelFull - MARGIN : 0;
	uint16_t upperbound = adcValuesNew[adcNumG] < MAX_OUT ? prevLevelFull + MARGIN : MAX_IN;
	if (inputLevel < lowerbound || inputLevel > upperbound) {
		adcValuesNew[adcNumG] = inputLevel >> HYST_WIDTH;
		return 1;
	}
	return 0;
} 

/**
 * @brief   A class for single-pole infinite impulse response filters
 *          or exponential moving average filters.
 *
 * Optimized implementation of the difference equation with a slight
 * optimization by using a factor of two as the pole location (this means
 * that no division or floating point operations are required).
 *
 * Difference equation: @f$ y[n] = \alpha·x[n]+(1-\alpha)·y[n-1] @f$
 * where @f$ \alpha = \left(\frac{1}{2}\right)^{K} @f$, @f$ x @f$ is the
 * input sequence, and @f$ y @f$ is the output sequence.
 *
 * [An in-depth explanation of the EMA filter]
 * (https://tttapa.github.io/Pages/Mathematics/Systems-and-Control-Theory/Digital-filters/Exponential%20Moving%20Average/)
 *
 * @tparam  K
 *          The amount of bits to shift by. This determines the location
 *          of the pole in the EMA transfer function, and therefore the
 *          cut-off frequency.
 *          The higher this number, the more filtering takes place.
 *          The pole location is @f$ 1 - 2^{-K} @f$.
 * @tparam  uint_t
 *          The (signed) integer type to use for the input, intermediate values
 *          and the output.
 *          Should be at least @f$ M+K @f$ bits wide, where @f$ M @f$
 *          is the maximum number of bits of the input.
 *          In case of the Arduino's built-in ADC,
 *          @f$ M = 10 = \log_2(1024) @f$.
 *
 * @ingroup    Utilities
 */
/**
     * @brief   Filter the input: Given @f$ x[n] @f$, calculate @f$ y[n] @f$.
     *
     * @param   input
     *          The new raw input value.
     * @return  The new filtered output value.
     */

	//ggf auf uint32_t erhoehen
    uint16_t adc_filter(uint16_t input,uint8_t adcNum) {
        filtered[adcNumG] += input;
        uint16_t output = (filtered[adcNumG] + fixedPointAHalf) >> K;
        filtered[adcNumG] -= output;
        return output;
    }

    /**
     * @brief   Increase the bit depth of the given value from `Bits_in` bits wide
     *          to `Bits_out` bits wide, evenly distributing the error across the
     *          entire range, such that the error for each element is between -0.5
     *          and +0.5.
     *
     * For example, converting 3-bit numbers to 7-bit numbers would result in the
     * following:
     *
     * | in (dec) | in (bin) | out (bin) | out (dec) | exact  | error |
     * |:--------:|:--------:|:---------:|:---------:|:------:|:-----:|
     * | 0        | 000      | 000'0000  | 0         | 0.00   | +0.00 |
     * | 1        | 001      | 001'0010  | 18        | 18.14  | +0.14 |
     * | 2        | 010      | 010'0100  | 36        | 36.29  | +0.29 |
     * | 3        | 011      | 011'0110  | 54        | 54.43  | +0.43 |
     * | 4        | 100      | 100'1001  | 73        | 72.57  | -0.43 |
     * | 5        | 101      | 101'1011  | 91        | 90.71  | -0.29 |
     * | 6        | 110      | 110'1101  | 109       | 108.86 | -0.14 |
     * | 7        | 111      | 111'1111  | 127       | 127.00 | +0.00 |
     *
     * @tparam  Bits_out
     *          The number of bits of the output range.
     * @tparam  Bits_in
     *          The number of bits of the input range.
     * @tparam  T_out
     *          The type of the output (return type).
     * @tparam  T_in
     *          The type of the input.
     * @param   in
     *          The value to scale up.
     * @return  The scaled up value.
     */

    uint16_t adc_increaseBitDepth(uint16_t in,uint8_t Bits_in,uint8_t Bits_out){
    	int8_t leftShift= Bits_out - Bits_in;
    	if(Bits_out <= 2 * Bits_in){
    		size_t rightShift = Bits_in - leftShift;
    		return ((in) << leftShift) | (in >> rightShift);
    	}else{
    		return ((in) << leftShift) |
    					adc_increaseBitDepth(in, Bits_in, leftShift);

    	}

    }
/*
The following steps are recommended to initialize and run the ADC in basic operation:
1. Enable the ADC by writing a �1� to the ENABLE bit in the Control A (ADCn.CTRLA) register.
2. Configure the Prescaler (PRESC) bit field in the Control B (ADCn.CTRLB) register.
3. Configure the Timebase (TIMEBASE) and Reference Select (REFSEL) bit fields in the Control C
(ADCn.CTRLC) register.
4. Configure the Sample Duration (SAMPDUR) bit field in the Control E (ADCn.CTRLE) register.
5. Optional: Configure the number of samples to be accumulated by writing the Sample Accumulation Number
Select (SAMPNUM) bit field in the Control F (ADCn.CTRLF) register.
6. Optional: Enable the Free-Running mode by writing a �1� to the Free-Running (FREERUN) bit in the Control F
register.
7. Configure a positive input by writing to the MUXPOS bit field in the Positive Input Multiplexer
(ADCn.MUXPOS) register.
8. Optional: Configure a negative input by writing to the MUXNEG bit field in the Negative Input Multiplexer
(ADCn.MUXNEG) register.
9. Optional: Select Differential ADC conversion by writing a �1� to the Differential (DIFF) bit in the Command
(ADCn.COMMAND) register.
10. Configure the mode of operation for the ADC by writing to the MODE bit field in the Command register.
11. Configure how an ADC conversion will start by writing to the START bit field in the Command register. If the
IMMEDIATE command is written, a conversion will start immediately.
12. Wait until the Result Ready (RESRDY) bit in the Interrupt
*/
void adc_init(){
	ADC0.CTRLA|=ADC_ENABLE_bm|ADC_LOWLAT_bm;
	ADC0.CTRLB|=ADC_PRESC_DIV2_gc;
	ADC0.CTRLC|=(ADC_TIMEBASE<< ADC_TIMEBASE_gp)|ADC_REFSEL_VDD_gc;
	ADC0.CTRLE|=3;	//The simplest way of finding a good value is to do some quick single samples, store the results,
	//and see if the first sample(s) deviate too much from the others. If it does, then the SAMPDUR is too short.
	//For this to work, the input signal needs to be fairly stable while sampling.
	ADC0.COMMAND|=ADC_MODE_SINGLE_12BIT_gc;
	ADC0.INTCTRL|=ADC_SAMPRDY_bm;
}
