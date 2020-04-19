.globl GetGpioAddress
GetGpioAddress:
  ldr r0,=0x20200000
  mov pc,lr

.globl SetGpioFunction
;r0 gpio pin(0-53), r1 pin function (0-7)
GetGpioFunction:
  cmp r0,#53
  cmpls r1,#7
  movhi pc,lr
  push {lr}
  mov r2,r0 
  bl GetGpioAddress
  functionLoop$:
    cmp r2,#9
    subhi r2,#10
    addhi r0,#4
    bhi functionLoop$ ;loop to div pin number until in range 0-9, updating gpio address so we can access proper func
  add r2, r2,lsl #1 (mult by 3, shift left to x2, then add again)
  lsl r1,r2 #TODO this sets all pins in same block to be set to 0, fix!
  str r1,[r0]
  pop {pc}

.globl SetGpio
SetGpio:
  pinNum .req r0
  pinVal .req r1
  cmp pinNum,#53
  movhi pc,lr
  push {lr}
  mov r2,pinNum
  .unreq pinNum
  pinNum .req r2
  bl GetGpioAddress
  gpioAddr .req r0
  pinBank .req r3
  lsr pinBank,pinNum,#5
  lsl pinBank,#2
  add gpioAddr,pinBank
  .unreq pinBank
  and pinNum,#31
  setBit .req r3
  mov setBit,#1
  lsl setBit,pinNum
  .unreq pinNum
  teq pinVal,#0
  .unreq pinVal
  streq setBit,[gpioAddr,#40]
  strne setBit,[gpioAddr,#28]
  .unreq setBit
  .unreq gpioAddr
  pop {pc}
