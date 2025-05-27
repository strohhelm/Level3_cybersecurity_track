# Format String Vulnerabilities

## this challenge consists of three challenges chall0, chall1, chall2

Chall0  
- 1st goal: find the base pointer of the program!
  - use `objdump -d chall0` to see the whole disasembly content.
  - execute in a seperate terminal `./chall0` and input `%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p`
  - in the output i could compare some pointers and through research i learned that base pointers of PIE enabled executables commonly start with 0x64... or 0x55...
  - i found the pointer 0x6494088f635e and saw that in the objdump the offset of main function is 135e. this fits well so i must be the return pointer to main from printf.
  - after some tries i found that a offset of 21 will print this pointer. `%21$p`
  - This means the base pointer of the program is `0x6494088f635e - 135e = 0x6494088f5000`

- 2nd goal: leak the base address of libc
  - the address of libc can be found through any known function address and calculating it with a known offset. Since the program uses printf, which i confirmed in gdb i can use  
    `nm -D /lib/x86_64-linux-gnu/libc.so.6 | grep printf` to find the offset of `00000000000606f0`
    
