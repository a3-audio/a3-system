/*
 * File:   i2cAlternative.c
 * Author: tiri
 *
 * Created on March 23, 2023, 1:12 AM
 */


#include "i2cAlternative.h"



// I2C slave registers
uint8_t I2C_REG[16]; // register array
uint8_t i2c_wrt_i; // register pointer
uint8_t i2c_read_i = 0; // register pointer
uint8_t i2c_read_n = 0; // how many bytes are to read
uint8_t led_buttons[4] = {0}; // how many bytes are to read
uint8_t led_color_buf = 0; //
volatile uint8_t I2C_REG_changed = 0; // register change flag
volatile uint8_t I2C_busy = 0; // I2C busy flag
//when led_tripple_to_change is zero no button will be changed



// I2C slave init

void I2C_init(uint8_t i2cAdrr) {
    TWI0.SADDR = i2cAdrr << 1; // set address (LSB is R/W bit)
    TWI0.SCTRLA = TWI_DIEN_bm // data interrupt enable
            | TWI_APIEN_bm // address or stop interrupt enable
            | TWI_PIEN_bm // stop interrupt enable
            | TWI_ENABLE_bm; // enable I2C slave
}

typedef enum {
    idle, receive_led_1, receive_led_2
} I2C_receive_state;
I2C_receive_state receive_state = idle;

#define SET_LEDS 5

void reset_states() {
    receive_state=idle;
    i2c_read_i=0;
    i2c_read_n=0;
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
                        case SET_LEDS:
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
                    setLedData(led_buttons[i2c_read_i], r, g, b);
                    i2c_read_i++;
                    if (i2c_read_i >= i2c_read_n) {
                        reset_states();
                    } else {
                        receive_state = receive_led_1;
                    }
                }
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

/*
void i2c_interrupt() {
    // Address match interrupt handler
    if (I2C_isAddr()) { // address match?
        I2C_sendACK(); // send ACK to master
        I2C_msg_bytes_i = 0; // reset register pointer
        I2C_msg_bytes_n = 0;
        I2C_busy = 1; // set I2C busy flag
        return; // quit ISR
    }

    // Data interrupt handler
    if (I2C_isData()) { // data transmission?
        if (I2C_isOut()) { // slave writing to master?
            I2C_put(42);//read_cb(I2C_msg_bytes_i++)); //              // send register value to master
            //CALL Function get data
            I2C_response(); // no ACK needed here
        } else { // slave reading from master?
            uint8_t msg = I2C_get(); // read register value from master
            I2C_sendACK(); // send ACK to master
            if (I2C_msg_bytes_ptr == 0) { //we have the first message
                switch (msg >> 4) {
                    case I2C_msg_setLed:
                        for (int i = 0; i < 4; i++) {
                            if (msg & 1 << i)
                                I2C_msg_bytes_to_read += 2;
                        }
                        I2C_msg_led_trippels_to_read=BITMASK_CLEAR(msg,0b11110000);
                        I2C_state=I2C_state_setLed1;
                        I2C_sendACK(); // send ACK to master
                        break;
                    default:
                        I2C_sendNACK(); // send NACK to master
                }


            }else{
               switch(I2C_state){
                    case I2C_state_setLed1:
                        I2C_msg_led_trippel=I2C_get()<<8;
                        I2C_msg_bytes_to_read--;
                        I2C_sendACK(); // send ACK to master
                        break;
                    case I2C_state_setLed2:
                        I2C_msg_led_trippel|=I2C_get();
                        I2C_msg_bytes_to_read--;
                        if(I2C_msg_bytes_to_read==0)
                            I2C_state=I2C_state_idle;
                        else
                            I2C_state=I2C_state_setLed1;
                        for (int i = 3; i >= 0; i--) {
                            if(I2C_msg_led_trippels_to_read&1<<1){
                                i2c_led.tripple_to_change|=1<<i;
                                i2c_led.colors[2]=I2C_msg_led_trippel>>12;
                                i2c_led.colors[1]=(uint8_t)(I2C_msg_led_trippel>>4);
                                i2c_led.colors[0]=BITMASK_CLEAR(((uint8_t)I2C_msg_led_trippel),0b11110000)<<4;
                            }

                        }

                        I2C_sendACK(); // send ACK to master
                        break;
                    default:
                        I2C_sendNACK(); // send ACK to master
                        break;
                
            

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

 */