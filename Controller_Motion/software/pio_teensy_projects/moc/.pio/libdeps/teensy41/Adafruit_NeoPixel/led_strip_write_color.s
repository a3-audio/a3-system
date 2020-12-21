    AREA asm_func, CODE, READONLY
    EXPORT led_strip_write_color
    IMPORT led_strip_write_delays

    MACRO
    delay $id
    ldr r5, =led_strip_write_delays
    ldrb r5, [r5, $id]
    ldr r4, =delay_region_end
    subs r4, r4, r5
    blx r4
    MEND

led_strip_write_color
    ; Register usage:
    ; These are the first 4 arguments to the method:
    ;   R0:  pointer to the color to send
    ;   R1:  pointer to the register for setting the pin
    ;   R2:  pointer to the register for clearing the pin
    ;   R3:  pin mask
    ; Additionally, we use these registers:
    ;   R4:  temporary register
    ;   R5:  temporary register
    ;   R6:  shift register that holds the 24-bit color
    ;   R7:  the number of bits we still need to send
    ;   R13: Link Register, holds return addresses.

    ; Push those registers so we can restore them later.
    push {r4, r5, r6, r7, lr}

    ldrb r6, [r0, #1]  ; Load green.
    lsls r6, r6, #24   ; Put green in MSB of r6.
    ldrb r4, [r0, #0]  ; Load red.
    lsls r4, r4, #16
    orrs r6, r6, r4    ; Put red in r6.
    ldrb r4, [r0, #2]  ; Load blue.
    lsls r4, r4, #8
    orrs r6, r6, r4    ; Put blue in r6.
   
    ; On the Cortex-M3 we simply did:
    ;    ldr r6, [r0]       ; Read the color.  Now we have:     xxBbGgRr
    ;    rbit r6, r6        ; Reverse the order of the bits:    rRgGbBxx
    ;    rev r6, r6         ; Reverse the order of the bytes:   xxbBgGrR
    ; and then we used rrxs for shifting to the right through carry.
    
    ldr r7, =24        ; Initialize the loop counter register.
    
send_led_strip_bit
    str r3, [r1]       ; Drive the line high.
    
    ; It doesn't really matter exactly how long we delay here as long as it is
    ; less than 540 microseconds.
    nop
    nop
    nop
    nop
    nop
    nop
    
    ldr r4, =0x80000000
    tst r6, r4
    bne delay0
    str r3, [r2]       ; If the bit to send it 0, drive the line low.
delay0

    delay #0

    tst r6, r7
    ldr r4, =0x80000000
    tst r6, r4
    beq delay1
    str r3, [r2]       ; If the bit to send is 1, drive the line low.
delay1
    
    delay #1
    
    lsls r6, r6, #1           ; Shift color bits.
    subs r7, r7, #1           ; Decrement the loop counter.
    bne send_led_strip_bit    ; Send another bit if we have not reached zero.   
    pop {r4, r5, r6, r7, pc}  ; Otherwise, restore the registers and return.
    bx lr;

delay_region
    ; The following is 128 nops.
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
delay_region_end
    bx lr    ; return
    
    END