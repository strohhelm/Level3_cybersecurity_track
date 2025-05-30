# Format String Vulnerabilities

## this challenge consists of three challenges chall0, chall1, chall2

Chall0  
- 1st goal: find the base pointer of the program!
  - use `objdump -d chall0` to see the whole disasembly content.
  - execute in a seperate terminal `./chall0` and input `%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p`
  - in the output i could compare some pointers and through research i learned that base pointers of PIE enabled executables commonly start with 0x64... or 0x55...
  - i found the pointer 0x6494088f635e and saw that in the objdump the offset of main function is 135e. this fits well so i must be the return pointer to main from printf.
  - after some tries i found that a offset of 21 will print this pointer. `AAAA%21$p`
  - This means the base pointer of the program is `0x6494088f635e - 135e = 0x6494088f5000`

- 2nd goal: leak the base address of libc
  - the address of libc can be found through any known function address and calculating it with a known offset. Since the program uses printf, which i confirmed in gdb i can use  
  - from here on out i upsolved the solutions, since i had to learn basic stack and elf functionality first to understand the solutions. But through that, i learned to automate this in python scipts.
  - i went through the program in gdb started through python so i can compare the actual values to the ones im printing.
  - the libc base address can be seen with vmmap in gdb. A very close pointer is at offset 19 when the payload is 'AAA%19$p'. so i see if it is everytime the same, which is true. So i take the offset from this pointer to the one shown in gdb and find an offset of 0x29d90.
  - I have the same approach to finding rip in the first instruction of printf. I saw the actual value using `info frame` in gdb. then found a really close pointer on the stack which sayed the same every iteration. It was surprisingly close in offset 23. The payload is `AAAA%23$p'.
  - The canary value can be seen in gdb using the `canary` command, and then spotted in the stack at offset `AAAA$17$p'.
  - Interestingly enough all asked values are in a row, always 8 byte between them.

