.section .init
.globl _start

_start:
ldr r0,=0x20200000 ; put address of GPIO controller in r0
b main

.section .text
main:
mov sp,#0x8000

;set gpio pin
pinNum .req r0
pinFunc .req r1
mov pinNum,#16
mov pinFunc,#1
bl SetGpioFunction
.unreq pinNum
.unreq pinFunc

;led on
pinNum .req r0
pinVal .req r1
mov pinNum,#16
mov pinVal,#0
bl SetGpio
.unreq pinNum
.unreq pinVal

;implementing a wait between light on and off
mov r2,$0x3f0000
wait1$:
sub r2,#1
cmp r2,#0
bne wait1$

;led off
pinNum .req r0
pinVal .req r1
mov pinNum,#16
mov pinVal,#1
bl SetGpio
.unreq pinNum
.unreq pinVal

