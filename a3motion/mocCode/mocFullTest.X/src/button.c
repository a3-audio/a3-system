/*
 * button.c
 *
 * Created: 22/03/2022 15:18:23
 *  Author: tirii
 */
#include "button.h"

uint8_t buttons[4];
uint8_t butFilterCnt = 0;
uint8_t buttonStatesNew = 0;
uint8_t buttonStates = 0;

uint8_t but_getStates() {
    return buttonStates;
}

/*
 * checks the button states
 * filter:
 * if buttons[x] value is '0000 0000' it counts as released
 * if buttons[x] value is '1111 1111' it counts as pressed
 * anything in between doesn't change the former state
 */
void but_updateStates() {
    if (BIT_CHECK(BU0_PT.IN, BU0_BP))
        BIT_CLEAR(buttons[0], butFilterCnt);
    else
        BIT_SET(buttons[0], butFilterCnt);

    if (buttons[0] == STATE_BUT_RELEASED)
        BIT_CLEAR(buttonStatesNew, BU0_STAT_BP);
    else {
        if (buttons[0] == STATE_BUT_PRESSED)
            BIT_SET(buttonStatesNew, BU0_STAT_BP);
    }


    if (BIT_CHECK(BU1_PT.IN, BU1_BP)) {
        BIT_CLEAR(buttons[1], butFilterCnt);
    } else {
        BIT_SET(buttons[1], butFilterCnt);
    }
    if (buttons[1] == STATE_BUT_RELEASED) {
        BIT_CLEAR(buttonStatesNew, BU1_STAT_BP);
    } else
        if (buttons[1] == STATE_BUT_PRESSED) {
        BIT_SET(buttonStatesNew, BU1_STAT_BP);
    }

    if (BIT_CHECK(BU2_PT.IN, BU2_BP)) {
        BIT_CLEAR(buttons[2], butFilterCnt);
    } else {
        BIT_SET(buttons[2], butFilterCnt);
    }
    if (buttons[2] == STATE_BUT_RELEASED) {
        BIT_CLEAR(buttonStatesNew, BU2_STAT_BP);
    } else
        if (buttons[2] == STATE_BUT_PRESSED) {
        BIT_SET(buttonStatesNew, BU2_STAT_BP);
    }

    if (BIT_CHECK(BU3_PT.IN, BU3_BP)) {
        BIT_CLEAR(buttons[3], butFilterCnt);
    } else {
        BIT_SET(buttons[3], butFilterCnt);
    }
    if (buttons[3] == STATE_BUT_RELEASED) {
        BIT_CLEAR(buttonStatesNew, BU3_STAT_BP);
    } else
        if (buttons[3] == STATE_BUT_PRESSED) {
        BIT_SET(buttonStatesNew, BU3_STAT_BP);
    }
    butFilterCnt = (butFilterCnt + 1)&0b111;
    cli();
    buttonStates = buttonStatesNew;
    sei();

}

void but_init() {
    for (int i = 0; i < 4; i++) {
        buttons[i] = STATE_BUT_RELEASED;
    }

    BITMASK_CLEAR(BU0_PT.DIR, BU0_BM);
    BIT_SET(BU0_PT.PIN3CTRL, PORT_PULLUPEN_bp); //BUtton0 PC3
    BITMASK_CLEAR(BU1_PT.DIR, PIN4_bm);
    BIT_SET(BU1_PT.PIN4CTRL, PORT_PULLUPEN_bp); //Button1 PA4
    BITMASK_CLEAR(BU2_PT.DIR, BU2_BM);
    BIT_SET(BU2_PT.PIN0CTRL, PORT_PULLUPEN_bp); //Button2 PC0
    BITMASK_CLEAR(BU3_PT.DIR, BU3_BM);
    BIT_SET(BU3_PT.PIN4CTRL, PORT_PULLUPEN_bp); //Button3 PB4
    for (int i = 0; i < 20; i++)
        for (int i1 = 0; i1 < 1000; i1++)
            _NOP();
}