#!/usr/bin/python2

A = 0
X = 0
Y = 0
C = 0
addr_3b = 0

stack = list()

# '0' is padding to 5
instr = "00000N" + "A"*23
"""
70 30 53 A1 D3 70 3F 64  B3 16 E4 04 5F 3A EE 42
B1 A1 37 15 6E 88 2A AB  20 AC 7A 25 D7 9C C2 1D
58 D0 13 25 96 6A DC 7E  2E B4 B4 10 CB 1D C2 66
"""
XOR_955E = [0x70, 0x30, 0x53, 0xA1, 0xD3, 0x70, 0x3F, 0x64, 0xB3, 0x16, 0xE4, 0x04, 0x5f, 0x3a, 0xEE, 0x42, 0xb1, 0xa1, 0x37, 0x15, 0x6e, 0x88, 0x2a, 0xab, 0x20, 0xac, 0x7a, 0x25, 0xd7, 0x9c, 0xc2, 0x1d, 0x58, 0xd0, 0x13]
XOR_9576 = [0x20, 0xac, 0x7a, 0x25, 0xd7, 0x9c, 0xc2, 0x1d, 0x58, 0xd0, 0x13, 0x25, 0x96, 0x6a, 0xdc, 0x7e, 0x2e, 0xb4, 0xb4, 0x10, 0xcb, 0x1d, 0xc2, 0x66, 0x3b, 0x4c, 0x4f, 0x43, 0x4b, 0x44, 0x4f, 0x57, 0x4e, 0x3d, 0x00]
OUT = []
KEY = ""

def ROL_b(b):
  return ((int(b)<<1) | ((b&0x80)>>7)) & 0xFF

def ROR_b(b):
  return ((b>>1) | ((b&1) << 7)) & 0xFF

def ROR():
  global A
  A = ROR_b(A)

def ROL():
  global A
  A = ROL_b(A)

def TAX():
  global A
  global X
  X = A

def TXA():
  global A
  global X
  A = X

def PHA():
  global A
  stack.append(A)

def PLA():
  global A
  A = stack.pop()

#for i in range(0, 0x18):
  #LDA 5, y
def round(i, ch):
  global Y
  Y = i
  global A
  global X
  global addr_3b

#  print "round " + str(i)
#  A = ord(instr[Y+5])
  A = ord(ch)
  TAX()
  ROL()
  TXA()
  ROL()
  TAX()
  ROL()
  TXA()
  ROL()
  TAX()
  ROL()
  TXA()
  ROL()
  PHA()
  A = addr_3b
  TAX()
  ROR()
  TXA()
  ROR()
  TAX()
  ROR()
  TXA()
  ROR()
  addr_3b = A & 0xFF 
  PLA()
  #print "A = " + hex(A) + "; addr_3b = " + hex(addr_3b) + "; XOR_955E[y] = " + hex(XOR_955E[Y])
  A = (A + addr_3b)  & 0xFF
  A = (A ^ XOR_955E[Y]) & 0xFF
  addr_3b = A 
  TAX()
  ROL()
  TXA()
  ROL()
  TAX()
  ROL()
  TXA()
  ROL()
  TAX()
  ROL()
  TXA()
  ROL()
  TAX()
  ROL()
  TXA()
  ROL()
  A = A ^ XOR_9576[Y]

  Y = Y + 1
  return A


A = 0
X = 0
Y = 0
addr_3b = 0


A_o = 0
X_o = 0
Y_o = 0
addr_3b_o = 0

for i in range(0, 0x18):
  for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    if round(i, ch) == 0:
      print "char  = " + ch
      KEY += ch
      A_o = A
      X_o = X
      Y_o = Y
      addr_3b_o = addr_3b
      break
    else:
      A = A_o
      X = X_o
      Y = Y_o
      addr_3b = addr_3b_o


print "KEY = " + KEY
