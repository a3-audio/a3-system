//#include "mbed.h"
//#include "PololuLedStrip.h"
//
//PololuLedStrip ledStrip(PTC8);
//
//#define LED_COUNT 60
//rgb_color colors[LED_COUNT];
//
//Timer timer;
//
//int main()
//{
//    timer.start();
//
//    while(1)
//    {
//        // Update the colors array.
//        uint8_t time = timer.read_ms() >> 2;
//        for(uint32_t i = 0; i < LED_COUNT; i++)
//        {
//            uint8_t x = time - 8*i;
//            colors[i] = (rgb_color){ x, 255 - x, x };
//        }
//    
//        // Send the colors to the LED strip.
//        ledStrip.write(colors, LED_COUNT);
//        wait_ms(10);        
//    }
//}
