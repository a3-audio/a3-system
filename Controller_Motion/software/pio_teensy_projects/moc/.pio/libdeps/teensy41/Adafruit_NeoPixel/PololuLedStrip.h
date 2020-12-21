#include "mbed.h"

#ifndef _POLOLU_LED_STRIP_H
#define _POLOLU_LED_STRIP_H

namespace Pololu
{
    #ifndef _POLOLU_RGB_COLOR
    #define _POLOLU_RGB_COLOR
    
    /** Represents an RGB color. */
    typedef struct rgb_color
    {
        uint8_t red;   /*!< A number between 0 and 255 that represents the brightness of the red component. */
        uint8_t green; /*!< A number between 0 and 255 that represents the brightness of the green component. */
        uint8_t blue;  /*!< A number between 0 and 255 that represents the brightness of the blue component. */
    } rgb_color;
    #endif

    extern "C" int led_strip_write_color(rgb_color *, volatile uint32_t * set, volatile uint32_t * clear, uint32_t mask);

    /** This class lets you control the addressable RGB LED strips from Pololu</a>,
    or any other LED strip based on the TM1804 chip. */
    class PololuLedStrip
    {
        gpio_t gpio;
        
        public:
        
        /** This constructor lets you make an led strip object by specifying the pin name.
        There are no restrictions on what pin you can choose.
        
        Example:
        @code
PololuLedStrip ledStrip(p8);
        @endcode
        */
        PololuLedStrip(PinName pin);
        
        /** Writes the specified series of colors to the LED strip.
        @param colors should be a pointer to an array of rgb_color structs.
        @param count should be the number of colors to write.
        
        The first color in the array will be written to the LED closest to the data input connector.
        To update all the LEDs in the LED strip, count should be equal to or greater than the number of LEDs in the strip.
        If count is less than the number of LEDs in the strip, then some LEDs near the end of the strip will not be updated.
        
        The colors are sent in series and each color takes about 45 microseconds to send.
        This function disables interrupts temporarily while it is running.
        This function waits for over 10 us at the end before returning to allow the colors to take effect.
        */
        void write(rgb_color * colors, unsigned int count);
               
        /** This option defaults to <code>false</code>.
        Setting this to true changes the behavior of the write function, making it enable interrupts
        after each color is sent, about every 60 microseconds.
        This allows your program to respond to interrupts faster, but makes it possible for an interrupt
        that takes longer than 8 microseconds to screw up the transmission of colors to the LED strip.
        
        Example:
        @code
        PololuLedStrip::interruptFriendly = true;
        @endcode
        */
        static bool interruptFriendly;
        
        static void calculateDelays();
    };
}

using namespace Pololu;

#endif