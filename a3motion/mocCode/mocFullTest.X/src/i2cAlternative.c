/*
 * File:   i2cAlternative.c
 * Author: tiri
 *
 * Created on March 23, 2023, 1:12 AM
 */


#include "i2cAlternative.h"

//MSG codes
//FIRST BYTE 
//        xxxx        xxxx
//      MSG type     MSG Specific*
//MSG SET LEDS       BUTTON NR 1-4
//MSG SET ENCODER    STEP SIZE
//MSG SET ID         SECOND BYTE GETS ID      

#define MSG_SET_LEDS 0b0101         //5
#define MSG_SETUP_ENCODER 0b1011    //11
#define MSG_SET_ID 0b1100           //12

// I2C slave registers
//uint8_t I2C_REG[16]; // register array
volatile uint8_t i2c_wrt_i; // register pointer
volatile uint8_t i2c_read_i = 0; // register pointer
volatile uint8_t i2c_read_n = 0; // how many bytes are to read
volatile uint8_t led_buttons[4] = {0}; // how many bytes are to read
volatile uint8_t led_color_buf = 0; //
volatile uint8_t I2C_REG_changed = 0; // register change flag
volatile uint8_t I2C_busy = 0; // I2C busy flag
//when led_tripple_to_change is zero no button will be changed

typedef enum {
    idle, receive_led_1, receive_led_2, receive_i2c_addr
} I2C_receive_state;
volatile I2C_receive_state receive_state = idle;

// I2C slave init

void i2c_init(uint8_t i2cAdrr) {
    TWI0.SADDR = i2cAdrr << 1; // set address (LSB is R/W bit)
    TWI0.SCTRLA = TWI_DIEN_bm // data interrupt enable
            | TWI_APIEN_bm // address or stop interrupt enable
            | TWI_PIEN_bm // stop interrupt enable
            | TWI_ENABLE_bm; // enable I2C slave
}






void reset_states() {
    receive_state = idle;
    i2c_read_i = 0;
    i2c_read_n = 0;
}

ISR(TWI0_TWIS_vect) {
    // Address match interrupt handler
    if (I2C_isAddr()) { // address match?
        I2C_sendACK(); // send ACK to master
        i2c_wrt_i = 0; // reset register pointer
        I2C_busy = 1; // set I2C busy flag
        reset_states();
        return; // quit ISR
    }

    // Data interrupt handler
    if (I2C_isData()) { // data transmission?
        if (I2C_isOut()) { // slave writing to master?
            receive_state = idle;
            I2C_put(getSensorData(i2c_wrt_i)); // send register value to master
            I2C_response(); // no ACK needed here
            if (++i2c_wrt_i >= 6) // increase pointer...
                i2c_wrt_i = 0; // ...or wrap around
        } else { // slave reading from master?
            uint8_t msg = I2C_get();
            switch (receive_state) {
                case idle:
                    switch (msg >> 4) {
                        case MSG_SET_ID:
                            receive_state = receive_i2c_addr;
                            break;
                        case MSG_SETUP_ENCODER:
                            BITMASK_CLEAR(msg, 0b11110000);
                            i2c_setEncoder(msg);
                            reset_states();
                            break;
                        case MSG_SET_LEDS:
                            receive_state = receive_led_1;
                            BITMASK_CLEAR(msg, 0b11110000);
                            for (int i = 0; i < 4; i++) {
                                if (msg & (1 << i)) {
                                    led_buttons[i2c_read_n] = i;
                                    i2c_read_n++;
                                }
                            }
                            if (i2c_read_n > 0)
                                break;
                        default:
                            reset_states();
                            I2C_sendNACK();
                            return;
                    }
                    break;
                case receive_led_1:
                    led_color_buf = msg;
                    receive_state = receive_led_2;
                    break;
                case receive_led_2: //rrrr rrgg gggg bbbb
                {
                    uint8_t r, g, b;
                    r = led_color_buf >> 2;
                    BITMASK_CLEAR(led_color_buf, 0b11111100);
                    g = led_color_buf << 4 | msg >> 4;
                    BITMASK_CLEAR(msg, 0b11110000);
                    b = msg << 2;
                    i2c_setLedData(led_buttons[i2c_read_i], r, g, b);
                    i2c_read_i++;
                    if (i2c_read_i >= i2c_read_n) {
                        reset_states();
                    } else {
                        receive_state = receive_led_1;
                    }
                }
                    break;
                case receive_i2c_addr:
                    if (msg < 0x7F){
                        TWI0.SADDR = msg << 1; // set address (LSB is R/W bit)
                        i2c_setID(msg);
                    }
                    reset_states();
                    break;

            }
            I2C_sendACK(); // send ACK to master
            I2C_REG_changed = 1; // set register changed flag
        }

        return; // quit ISR
    }

    // Stop condition interrupt handler
    if (I2C_isStop()) { // stop condition?
        I2C_complete(); // complete transaction
        I2C_busy = 0; // clear I2C busy flag
    }
}
