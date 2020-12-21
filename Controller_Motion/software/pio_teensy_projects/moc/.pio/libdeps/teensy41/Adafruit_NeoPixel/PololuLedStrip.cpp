#include "PololuLedStrip.h"

bool PololuLedStrip::interruptFriendly = false;

// The two timed delays, in units of half-cycles.
uint8_t led_strip_write_delays[2];

void PololuLedStrip::calculateDelays()
{
    int f_mhz = SystemCoreClock / 1000000;   // Clock frequency in MHz.

    if (f_mhz <= 48)
    {
        // The delays below result in 360/1120 ns pulses and a 1880 ns period on the mbed NXP LPC11U24.        
        led_strip_write_delays[0] = 0;
        led_strip_write_delays[1] = 0;
    }
    else
    {
        // Try to generally compute what the delays should be for a ide range of clock frequencies.
        
        // The fudge factors below were experimentally chosen so that we would have
        // ~100/840 ns pulses and a ~1430 ns period on the mbed NXP LPC1768 (96 MHz Cortex-M3).
        // There seem to be some ~100 ns inconsistencies in the timing depending on which example program is
        // running; the most likely explanation is some kind of flash caching that affects the timing.
        // If you ever change these numbers, it is important to check the the subtractions below
        // will not overflow in the worst case (smallest possible f_mhz).
        led_strip_write_delays[0] = 750*f_mhz/1000 - 33;
        led_strip_write_delays[1] = 550*f_mhz/1000 - 20;    
    }
 
    // Convert from units of cycles to units of half-cycles; it makes the assembly faster.   
    for(int i = 0; i < 2; i++)
    {
        led_strip_write_delays[i] <<= 1;
    }
}

PololuLedStrip::PololuLedStrip(PinName pinName)
{
    gpio_init_out(&gpio, pinName);
}

void PololuLedStrip::write(rgb_color * colors, unsigned int count)
{
    calculateDelays();

    __disable_irq();   // Disable interrupts temporarily because we don't want our pulse timing to be messed up.

    while(count--)
    {
        led_strip_write_color(colors, gpio.reg_set, gpio.reg_clr, gpio.mask);
        colors++;
         
        if (interruptFriendly)
        {
            __enable_irq();
            __nop();
            __nop();
            __nop();
            __disable_irq();
        }
    }
        
    __enable_irq();   // Re-enable interrupts now that we are done.
    wait_us(24);      // Hold the line low for 24 microseconds to send the reset signal.
    
    //*(gpio.reg_set) = gpio.mask;
    //*(gpio.reg_clr) = gpio.mask;

}