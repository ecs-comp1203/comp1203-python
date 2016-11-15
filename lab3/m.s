@@@@@@@@ file m.s - COMP1203 2016/17 lab3 @@@@@@@@@@@@@@@@@@@@@@@@@@@
@@ This "main" file wraps up a simple call to printf for your code
@@ which is kept in a separate file and compiled with this one
	.syntax unified
        .arch armv8-a
        .eabi_attribute 27, 3
        .eabi_attribute 28, 1
        .fpu vfpv3-d16
        .eabi_attribute 20, 1
        .eabi_attribute 21, 1
        .eabi_attribute 23, 3
        .eabi_attribute 24, 1
        .eabi_attribute 25, 1
        .eabi_attribute 26, 2
        .eabi_attribute 30, 6
        .eabi_attribute 34, 1
        .eabi_attribute 18, 4
        .file   "m.c"
        .section        .rodata
.align  2
.LC0:
        .ascii  "result of x(%d, %d) is %d\012\000"
        .text
        .align  2
        .global main
        .thumb
        .thumb_func
        .type   main, %function
main:
        push    {r7, lr}
        sub     sp, sp, #24
        add     r7, sp, #0
        str     r0, [r7, #4]
        str     r1, [r7, #0]
        mov     r3, #0
        str     r3, [r7, #12]
        mov     r3, #1
        str     r3, [r7, #16]
        ldr     r3, [r7, #4]
        cmp     r3, #1
        ble     .L2
        ldr     r3, [r7, #0]
        add     r3, r3, #4
        ldr     r3, [r3, #0]
        mov     r0, r3
        bl      atoi
        str     r0, [r7, #12]
.L2:
        ldr     r3, [r7, #4]
        cmp     r3, #2
        ble     .L3
        ldr     r3, [r7, #0]
        add     r3, r3, #8
        ldr     r3, [r3, #0]
        mov     r0, r3
        bl      atoi
        str     r0, [r7, #16]
.L3:
        ldr     r0, [r7, #12]
        ldr     r1, [r7, #16]
        bl      x
        str     r0, [r7, #20]
	movw r3,#:lower16:.LC0
	movt r3,#:upper16:.LC0
        mov     r0, r3
        ldr     r1, [r7, #12]
        ldr     r2, [r7, #16]
        ldr     r3, [r7, #20]
        bl      printf
        mov     r0, r3
        add     r7, r7, #24
        mov     sp, r7
        pop     {r7, pc}
        .size   main, .-main

