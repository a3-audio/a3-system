/*
 * File:   newmain.c
 * Author: tiri
 *
 * Created on March 23, 2023, 1:01 AM
 */
#include "main.h"
#define sBUT_PRESSED 1
#define sBUT_RELEASED 0
#define NUM_CASES 3
ledEvent event;
volatile uint8_t led_cnt1 = 0;
uint8_t led_cnt2 = 0;
volatile uint8_t sensor_cnt1 = 0;
uint8_t sensor_cnt2 = 1;
volatile sensor sensor_data = {3, 4, 5, 6};
uint8_t *sensor_data_ptr = (uint8_t *) & sensor_data;
volatile uint8_t adc_finished = 1;
volatile uint8_t adc_i = 0;


//ADC sample is ready

ISR(ADC0_SAMPRDY_vect) {
    adc_finished = 1;
    ADC0.INTFLAGS |= ADC_RESOVR_bm;
    //adc_i=adc_setValue((uint16_t)((ADC0_SAMPLEH<<8)|ADC0_SAMPLEL));
    adc_i = adc_setValue(ADC0_SAMPLE);
    adc_i = (adc_i == 0);
    adc_start_prepare(adc_i);
}

ISR(SPI0_INT_vect) {

    if (SPI0.INTFLAGS & SPI_TXCIF_bm) {
        //toggleCh1();
        BIT_SET(LED_SHU_PT.OUTSET, LED_SHU_BP); //ACK BIT ON
        BITMASK_SET(SPI0.INTFLAGS, SPI_TXCIF_bm);
        BIT_SET(LED_SHU_PT.OUTCLR, LED_SHU_BP); //ACK BIT OFF
    }
}

//75us
uint16_t test_ses1 = 0;
uint16_t test_ses2 = 0;
uint16_t test_ses_i = 0;

ISR(TCA0_OVF_vect) {

    TCA0.SINGLE.INTFLAGS |= TCA_SINGLE_OVF_bm; //clear interrupt flag
    test_ses1++;
    if (test_ses1 == 14000)
        test_ses1 = 0;


    led_cnt1++;
    if (led_cnt1 == LED_MAX)
        led_cnt1 = 0;
}


//250us

ISR(TCB0_INT_vect) {

    TCB0.INTFLAGS |= TCB_CAPT_bm;
    if (sensor_cnt1 == sensor_cnt2) {
        sensor_cnt1++;
        if (sensor_cnt1 == 4)
            sensor_cnt1 = 0;
    }

}

uint8_t getSensorData(uint8_t byte_i) {
    switch (byte_i) {
        case 0:
            sensor_data.button = but_getStates();
            break;
        case 1:
            sensor_data.adc0 = adc_getValue(0);
            break;
        case 3:
            sensor_data.adc1 = adc_getValue(1);
            break;
        case 5:
            sensor_data.encoder = (uint8_t) enc_getValue();
            break;
        default:
            break;
    }
    return sensor_data_ptr[byte_i];
}

void i2c_setEncoder(uint8_t dat) {
    eep_set_enc_step(dat);
    enc_set_step(dat);
}

void i2c_setLedData(uint8_t button_i, uint8_t r, uint8_t g, uint8_t b) {
    led_updateRGB(button_i, r, g, b);
}

void i2c_setID(uint8_t dat) {
    eep_set_i2c_addr(dat);
}

int main(void) {
    ccp_write_io((void *) & (CLKCTRL.MCLKCTRLB), 0); //protected write to disable prescaler of CPU clock

    eep_init(); //must come first
    time_t0Init();
    time_t1Init();
    i2c_init(eep_get_i2c_addr());
    led_init();
    but_init();
    enc_init(eep_get_enc_step());
    adc_init();
    sei();
    adc_start_prepare(adc_i);
    adc_start_go(adc_i);
    while (1) {
        /*if (test_ses1 != test_ses2) {
            test_ses2 = test_ses1;
            if (test_ses1 == 0) {
                switch (test_ses_i) {
                    case 0:
                        i2c_setLedData(1, LED_MAX, 0, 0);
                        i2c_setLedData(0, 0, 0, 0);
                        i2c_setLedData(2, 0, 0, 0);
                        i2c_setLedData(3, 0, 0, 0);
                        test_ses_i++;
                        break;
                    case 1:
                        i2c_setLedData(2, 0, LED_MAX, 0);
                        i2c_setLedData(1, 0, 0, 0);
                        i2c_setLedData(0, 0, 0, 0);
                        i2c_setLedData(3, 0, 0, 0);
                        test_ses_i++;
                        break;
                    case 2:
                        i2c_setLedData(3, 0, 0, LED_MAX);
                        i2c_setLedData(1, 0, 0, 0);
                        i2c_setLedData(2, 0, 0, 0);
                        i2c_setLedData(0, 0, 0, 0);
                        test_ses_i++;
                        break;
                    default:
                        i2c_setLedData(0, LED_MAX, LED_MAX/4, 0);
                        i2c_setLedData(1, 0, 0, 0);
                        i2c_setLedData(2, 0, 0, 0);
                        i2c_setLedData(3, 0, 0, 0);
                        test_ses_i = 0;
                        break;

                }
            }
        }*/
        if (led_cnt1 != led_cnt2) {
            if (led_cnt1 < led_cnt2) {
                event = led_updateColorSystem();
            }
            if (event.time <= led_cnt1) {
                led_shiftSend(event.shift);
                event = led_getNextEvent();
            }
            led_cnt2 = led_cnt1;
        }

        if (sensor_cnt1 != sensor_cnt2) {
            sensor_cnt2 = sensor_cnt1 + 1;
            switch (sensor_cnt1) {
                case 0:
                    but_updateStates();
                    break;
                case 1:
                    enc_update();
                    break;
                case 2:
                    if (adc_finished) {
                        cli();
                        adc_start_go();
                        adc_finished = 0;
                        sei();
                    }
                    break;
                case 3:
                    break;

            }
            sensor_cnt2 = sensor_cnt1;
        }
    }
}
