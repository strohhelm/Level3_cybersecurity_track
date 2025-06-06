## Writeup to Level3 Cybersecurity track topic "auto reversing" challenge: Baby
### This challenge is the hackthebox challenge "Spooky Licence"

After learning about z3 and angr for a day, i finally understood how these tools help me solve this challenge.  
Since the binary is incredibly convoluted, i tried decompiling it first using dogbolt.org.  

It showed me that the program expected a single argumwent with a length of 0x20 which is 32 bytes.  
From there it expected an insane amount of if contitions to be true to accept the input.  

I used angr-management GUI to see a graphical representation of the control flow, and i could retrieve the address on which the "Licence Correct " is printed.  

From there it was sipmle: write a script that tests what input variable leads to the execution stepping into this address.  

It took me a bit to understand how to make it do exactly what i want, but the wonders of modern technology could help me with that quickly.

The script is provided as solution.py and results in the string "HTB{The_sp0000000key_liC3nC3K3Y}" to be the solution for this challenge.